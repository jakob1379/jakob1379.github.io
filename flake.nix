{
  inputs = {
    git-hooks = {
      url = "github:cachix/git-hooks.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    nixpkgs.url = "github:NixOS/nixpkgs/c5296fdd05cfa2c187990dd909864da9658df755";
    utils.url = "github:numtide/flake-utils";
  };
  outputs =
    {
      self,
      git-hooks,
      nixpkgs,
      utils,
    }:
    utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        lib = pkgs.lib;

        # A zero-byte file matched by the git-crypt filter breaks every commit:
        # git's ce_match_stat_basic() marks any zero-size worktree file whose
        # blob is not the empty blob as permanently changed, without consulting
        # the filter, and git-crypt never stores the empty blob. pre-commit then
        # snapshots a patch of changes that do not exist and cannot re-apply it,
        # failing with "No valid patches in input" after every hook has passed.
        # Without this guard the next empty file rediscovers that from scratch.
        gitCryptEmptyGuard = pkgs.writeShellApplication {
          name = "git-crypt-empty-guard";
          runtimeInputs = [
            pkgs.git
            pkgs.gnused
          ];
          text = ''
            status=0
            for f in "$@"; do
              [ -f "$f" ] || continue
              [ -s "$f" ] && continue
              if [ "$(git check-attr filter -- "$f" | sed 's/.*: //')" = "git-crypt" ]; then
                echo "error: $f is empty and matched by the git-crypt filter" >&2
                status=1
              fi
            done
            if [ "$status" -ne 0 ]; then
              cat >&2 <<'EOF'

            git cannot round-trip a zero-byte file through a clean filter, so the
            files above read as permanently modified and every commit will fail in
            pre-commit with "No valid patches in input".

            Fix it either way:
              - give the file content (preferred for real source files), or
              - unset the filter for it in .gitattributes, alongside the existing
                .codex exception, then: git add --renormalize -- cv/vault
            EOF
            fi
            exit "$status"
          '';
        };

        devPackages = with pkgs; [
          act
          git-crypt
          gnupg
          minhtml
          pinentry-gtk2
          ruby
          uv
          # Playwright requirements
          nodejs # Required to run the driver without patching
          stdenv.cc.cc.lib # For greenlet module
          # cv
          rendercv
          texliveFull # lualatex for CVs, xelatex for cover_letters/cover.cls
          poppler-utils # pdftotext, for the ATS text-layer check
        ];

        preCommitCheck = git-hooks.lib.${system}.run {
          src = ./.;
          default_stages = [
            "pre-commit"
            "commit-msg"
            "pre-push"
          ];
          hooks = {
            check-added-large-files.enable = true;
            check-case-conflicts.enable = true;
            check-merge-conflicts.enable = true;
            check-toml.enable = true;
            detect-private-keys.enable = true;
            end-of-file-fixer.enable = true;
            fix-byte-order-marker.enable = true;
            mixed-line-endings = {
              enable = true;
              args = [ "--fix=auto" ];
            };
            trim-trailing-whitespace.enable = true;

            # Replaces codespell, which was monolingual and ran with
            # --write-changes, so it rewrote Danish words it did not recognise.
            # cspell has no write mode at all: it reports instead of corrupting,
            # and cspell.config.yaml enables Danish only on the paths that are
            # actually Danish.
            #
            # Deliberately no Danish examples in this comment: flake.nix is
            # English-scope, so quoting them here would force them into the
            # global project-words.txt and undo the per-path scoping.
            cspell = {
              enable = true;
              name = "cspell";
              package = pkgs.cspell;
              entry = "${pkgs.cspell}/bin/cspell lint --config cspell.config.yaml --no-config-search --no-progress --no-summary --no-must-find-files --show-suggestions";
              # The built-in hook has no file filter and would otherwise run on
              # lockfiles, fonts and binaries. ignorePaths in the config is the
              # second line of defence.
              files = "\\.(md|mdown|markdown|txt|tex|cls|html|ts|js|py|nix|ya?ml|json|toml)$";
            };

            git-crypt-empty-guard = {
              enable = true;
              name = "no empty files under git-crypt";
              package = gitCryptEmptyGuard;
              entry = "${gitCryptEmptyGuard}/bin/git-crypt-empty-guard";
            };

            gitleaks = {
              enable = true;
              name = "Detect hardcoded secrets";
              package = pkgs.gitleaks;
              entry = "${lib.getExe pkgs.gitleaks} git --pre-commit --redact --staged --verbose";
              pass_filenames = false;
            };

            markdownlint-cli2 = {
              enable = true;
              name = "markdownlint-cli2";
              package = pkgs.markdownlint-cli2;
              entry = "${pkgs.markdownlint-cli2}/bin/markdownlint-cli2 --fix --config .markdownlint.yml";
              files = "\\.(md|mdown|markdown)$";
              # Same rationale as codespell above: cv/ holds vendored upstream
              # trees whose markdown does not meet this repo's rules (500
              # unfixable MD025/MD040 errors), and reformatting them would make
              # every upstream diff unreadable.
              excludes = [ "^cv/" ];
            };

            toml-sort-fix = {
              enable = true;
              name = "toml-sort-fix";
              package = pkgs.toml-sort;
              entry = "${lib.getExe pkgs.toml-sort} --in-place";
              files = "\\.toml$";
              excludes = [ "^zensical\\.toml$" ];
            };

            validate-pyproject = {
              enable = true;
              name = "validate-pyproject";
              package = pkgs.uv;
              entry = "${pkgs.uv}/bin/uvx --from validate-pyproject==0.24.1 --with 'validate-pyproject-schema-store[all]' validate-pyproject pyproject.toml";
              files = "^pyproject\\.toml$";
              pass_filenames = false;
              stages = [ "pre-push" ];
            };

            yamlfix = {
              enable = true;
              name = "yamlfix";
              package = pkgs.yamlfix;
              entry = lib.getExe pkgs.yamlfix;
              files = "\\.(yml|yaml)$";
            };

            zensical-build-check = {
              enable = true;
              name = "Check zensical builds";
              package = pkgs.zensical;
              entry = "${lib.getExe pkgs.zensical} build";
              pass_filenames = false;
            };
          };
        };

        formatter = pkgs.writeShellScriptBin "pre-commit-run" ''
          ${lib.getExe pkgs.pre-commit} run --all-files --config ${preCommitCheck.config.configFile}
        '';

        devShell = pkgs.mkShell {
          packages = devPackages ++ preCommitCheck.enabledPackages;

          shellHook = ''
            ${preCommitCheck.shellHook}

            # 1. Use the pre-patched browsers from Nixpkgs
            export PLAYWRIGHT_BROWSERS_PATH=${pkgs.playwright-driver.browsers}

            # 2. Use the system Node.js (which works on Nix) instead of the
            #    bundled Node binary (which fails)
            export PLAYWRIGHT_NODEJS_PATH=${pkgs.nodejs}/bin/node

            # 3. Skip validations
            export PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=true
            export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1

            # 4. Ensure greenlet can find libstdc++
            export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
          '';
        };
      in
      {
        checks.pre-commit-check = preCommitCheck;
        formatter = formatter;
        devShells.default = devShell;
      }
    );

}

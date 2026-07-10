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

            codespell = {
              enable = true;
              name = "codespell";
              package = pkgs.codespell;
              entry = "${lib.getExe pkgs.codespell} --write-changes";
              excludes = [ "^cv/" ];
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

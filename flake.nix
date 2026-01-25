{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/c5296fdd05cfa2c187990dd909864da9658df755";
    utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, utils }: utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
    in
      {
           devShell = pkgs.mkShell {
            packages = with pkgs; [
              # Tools
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

            shellHook = ''
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
      }
  );

}

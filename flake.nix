{
  inputs = {
    utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, utils }: utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
    in
      {
        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            act
            git-crypt
            gnupg
            minhtml
            pinentry-gtk2
            ruby
            uv
          ];

          LD_LIBRARY_PATH = "${pkgs.lib.makeLibraryPath [
            pkgs.cairo
          ]}:$LD_LIBRARY_PATH";
        };
      }
  );

}

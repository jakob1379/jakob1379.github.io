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
            uv
            act
            ruby
            gnupg
            git-crypt
            pinentry-gtk2
          ];

          LD_LIBRARY_PATH = "${pkgs.lib.makeLibraryPath [
            pkgs.cairo
          ]}:$LD_LIBRARY_PATH";
        };
      }
  );

}

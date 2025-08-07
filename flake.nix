{
  inputs = {
    utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, utils }: utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
      # pythonEnv = pkgs.python312.withPackages ( ps: with ps; [] );
    in
      {
        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            uv
            ruby
          ];

          LD_LIBRARY_PATH = "${pkgs.lib.makeLibraryPath [
          ]}:$LD_LIBRARY_PATH";


          shellHook = ''
            export UV_PYTHON_PREFERENCE="managed"
            '';
        };
      }
  );

}

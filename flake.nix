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
            act
            ruby
            cacert
            gnupg
            git-crypt
            pinentry-gtk2
          ];

          LD_LIBRARY_PATH = "${pkgs.lib.makeLibraryPath [
            pkgs.cairo
          ]}:$LD_LIBRARY_PATH";


          shellHook = ''
            export SSL_CERT_FILE=${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt
            export UV_PYTHON_PREFERENCE="managed"
            '';
        };
      }
  );

}

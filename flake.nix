{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
    systems.url = "github:nix-systems/default";
  };

  outputs = {
    self,
    nixpkgs,
    systems,
    ...
  } @ inputs: let
    forEachSystem = nixpkgs.lib.genAttrs (import systems);
  in {
    devShells = forEachSystem (system:
      let
        pkgs = import nixpkgs {inherit system; };
        python = pkgs.python313;
        node = pkgs.nodejs_24;
      in {
        default = pkgs.mkShell {
          packages = with pkgs; [
            zlib
            stdenv.cc.cc.lib
            uv
            python
            esbuild
            node
          ];

          env.LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
            pkgs.zlib
            pkgs.stdenv.cc.cc.lib
          ];

          shellHook = ''
            source .venv/bin/activate
            uv sync
            echo "Python: ${python.version} | Node: ${node.version} | uv: $(uv --version 2>/dev/null || true) | esbuild: ${pkgs.esbuild.version}"
          '';
        };
      }
    );
  };
}

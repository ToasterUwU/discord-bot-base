{
  description = "Use `nix develop` to temp install everything you need for working on this project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        overlays = [ ];
        pkgs = import nixpkgs {
          inherit system overlays;
        };
      in
      {
        devShells.default = with pkgs; mkShell {
          buildInputs = [
            python3
          ];
          shellHook = "python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt";
        };
      }
    );
}

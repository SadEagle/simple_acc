{
  description = "Backend flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      pythonModule =
        with pkgs;
        python313.withPackages (
          python-pkgs: with python-pkgs; [
            alembic
            fastapi
            fastapi-cli
            sqlalchemy
            asyncpg
            pytest
            httpx
            python-multipart
            email-validator
            pydantic-settings
          ]
        );
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = [ pythonModule ];
      };
    };
}

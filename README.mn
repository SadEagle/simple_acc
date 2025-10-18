# About

Current project is the realization of a small backend application.

The project contain current points:
- [x] FastAPI
- [x] SQLAlchemy ORM + Pydantic
- [x] Alembic migrations
- [x] Docker/Compose
- [x] Async
- [ ] Web UI

Note, `flake.nix` and `flake.lock` are NixOS specific package manager files

# Run
For API usage it's essential to use alembic db initialization

- Program run
```
docker compose up
``` 

- DB initialization with alembic script:
```
docker exec *backend_container_name* uv run alembic upgrade head 
```

# Reference projects:
- [full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template)


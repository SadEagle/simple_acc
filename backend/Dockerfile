FROM docker.io/library/python:3.13.7-alpine3.22

# Install uv
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /backend
ENV PYTHONPATH=./

# Compile bytecode
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
ENV UV_COMPILE_BYTECODE=1

COPY ./uv.lock ./pyproject.toml ./
RUN uv sync --frozen

COPY ./app/ ./app/
# TODO: add tests
# COPY ./tests/ ./tests/

COPY ./alembic.ini ./
COPY ./alembic_async/ ./alembic_async/

EXPOSE 8000

CMD ["uv", "run", "fastapi", "run", "--workers", "4", "./app/main.py"]


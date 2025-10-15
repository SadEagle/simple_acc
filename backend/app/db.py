import os

from sqlalchemy.ext.asyncio import create_async_engine

from app.config import settings


# NOTE: Create dev/test engine by pytest env variable check
# REF: https://docs.pytest.org/en/latest/example/simple.html#pytest-current-test-environment-variable
if "PYTEST_CURRENT_TEST" in os.environ:
    async_engine = create_async_engine(str(settings.TEST_DB_URL))
else:
    async_engine = create_async_engine(str(settings.DB_URL))

# NOTE: Tables init via alembic

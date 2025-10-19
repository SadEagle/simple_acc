from sqlalchemy.ext.asyncio import create_async_engine

from app.config import settings

async_engine = create_async_engine(str(settings.DB_URL))
# NOTE: Tables init via alembic

from pydantic import computed_field, PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEVICE_MAX_CONNECTIONS: int = 5

    # DEBUG
    # DB_URL: str = "postgresql+asyncpg://postgres"

    # DB PARAMS
    POSTGRES_DEV_SERVER: str
    POSTGRES_DEV_PORT: int = 5432
    POSTGRES_DEV_USER: str
    POSTGRES_DEV_PASSWORD: str = ""
    POSTGRES_DEV_DB: str

    POSTGRES_TEST_SERVER: str
    POSTGRES_TEST_PORT: int = 5432
    POSTGRES_TEST_USER: str
    POSTGRES_TEST_PASSWORD: str = ""
    POSTGRES_TEST_DB: str

    @computed_field
    @property
    def DB_URL(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_DEV_USER,
            password=self.POSTGRES_DEV_PASSWORD,
            host=self.POSTGRES_DEV_SERVER,
            port=self.POSTGRES_DEV_PORT,
            path=self.POSTGRES_DEV_DB,
        )

    @computed_field
    @property
    def TEST_DB_URL(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_TEST_USER,
            password=self.POSTGRES_TEST_PASSWORD,
            host=self.POSTGRES_TEST_SERVER,
            port=self.POSTGRES_TEST_PORT,
            path=self.POSTGRES_TEST_DB,
        )


settings = Settings()  # type: ignore

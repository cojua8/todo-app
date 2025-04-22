import pytest
from pydantic import Field
from pydantic_settings import BaseSettings

from app.infrastructure.sql_database_service.engine import engine
from app.infrastructure.sql_database_service.models import metadata_obj


class SqlDBTestSettings(BaseSettings):
    db_dialect: str = Field("postgresql", validation_alias="DB_TEST_DIALECT")
    db_username: str = Field("postgres", validation_alias="DB_TEST_USERNAME")
    db_password: str = Field("postgres", validation_alias="DB_TEST_PASSWORD")
    db_host: str = Field("postgres_db", validation_alias="DB_TEST_HOST")
    db_port: int = Field(5432, validation_alias="DB_TEST_PORT")
    db_name: str = Field("app_db", validation_alias="DB_TEST_NAME")


@pytest.fixture
def sqlalchemy_settings():
    return SqlDBTestSettings()  # type:ignore [reportCallIssue]


@pytest.fixture
async def db_engine(sqlalchemy_settings):
    db_engine = await engine(sqlalchemy_settings)
    yield db_engine
    async with db_engine.begin() as conn:
        await conn.run_sync(metadata_obj.drop_all)

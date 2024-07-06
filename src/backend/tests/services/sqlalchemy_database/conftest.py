import pytest

from app.infrastructure.sql_database_service.engine import engine
from app.infrastructure.sql_database_service.models import metadata_obj
from app.settings import SqlDBSettings


@pytest.fixture
def sqlalchemy_settings():
    return SqlDBSettings.model_construct(
        db_dialect="postgresql",
        db_username="postgres",
        db_password="postgres",  # noqa: S106
        db_host="postgres_db",
        db_port=5432,
        db_name="app_db",
    )


@pytest.fixture
async def db_engine(sqlalchemy_settings):
    db_engine = await engine(sqlalchemy_settings)
    yield db_engine
    async with db_engine.begin() as conn:
        await conn.run_sync(metadata_obj.drop_all)

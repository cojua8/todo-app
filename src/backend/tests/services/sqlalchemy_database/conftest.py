import os

import pytest
from testcontainers.postgres import PostgresContainer

from app.infrastructure.sql_database_service.engine import engine
from app.infrastructure.sql_database_service.models import metadata_obj
from app.settings import SqlDBSettings


@pytest.fixture(scope="session")
def sqlalchemy_settings():
    # this makes testcontainers work in windows
    # https://github.com/testcontainers/testcontainers-python/issues/108#issuecomment-1540584987
    os.environ["TC_HOST"] = "localhost"

    with PostgresContainer("postgres:16.2-alpine") as postgres:
        yield SqlDBSettings.model_construct(
            db_dialect="postgresql",
            db_username=postgres.POSTGRES_USER,
            db_password=postgres.POSTGRES_PASSWORD,
            db_host=postgres.get_container_host_ip(),
            db_port=int(postgres.get_exposed_port(5432)),
            db_name=postgres.POSTGRES_DB,
        )


@pytest.fixture
async def db_engine(sqlalchemy_settings):
    db_engine = await engine(sqlalchemy_settings)
    yield db_engine
    async with db_engine.begin() as conn:
        await conn.run_sync(metadata_obj.drop_all)

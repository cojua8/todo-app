import asyncio

import pytest
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.services.sql_database_service.models import metadata_obj


@pytest.fixture(scope="session")
def sqlalchemy_connect_url():
    return "postgresql+asyncpg://postgres:postgres@localhost:2345/test_todo_db"


@pytest.fixture(scope="session")
def event_loop():  # used by pytest-asyncio
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def db_engine(sqlalchemy_connect_url):
    yield async_engine_from_config({"sqlalchemy.url": sqlalchemy_connect_url})


@pytest.fixture(autouse=True)
async def _create(db_engine):  # noqa: ANN202
    async with db_engine.begin() as conn:
        await conn.run_sync(metadata_obj.create_all)
    yield
    async with db_engine.begin() as conn:
        await conn.run_sync(metadata_obj.drop_all)

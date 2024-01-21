import asyncio

import pytest
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine

from app.services.sql_database_service.models import metadata_obj


@pytest.fixture(scope="session")
def sqlalchemy_connect_url():
    return URL.create(
        drivername="postgresql+asyncpg",
        username="postgres",
        password="postgres",  # noqa: S106
        host="localhost",
        port=2345,
        database="test_todo_db",
    )


@pytest.fixture(scope="session")
def event_loop():  # used by pytest-asyncio
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def db_engine(sqlalchemy_connect_url):
    yield create_async_engine(sqlalchemy_connect_url)


@pytest.fixture(autouse=True)
async def _create(db_engine):
    async with db_engine.begin() as conn:
        await conn.run_sync(metadata_obj.create_all)
    yield
    async with db_engine.begin() as conn:
        await conn.run_sync(metadata_obj.drop_all)

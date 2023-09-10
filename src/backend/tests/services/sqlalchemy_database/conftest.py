import pytest
from sqlalchemy import engine_from_config

from app.services.sql_database_service.models import metadata_obj


@pytest.fixture(scope="session")
def sqlalchemy_connect_url():
    return "postgresql+psycopg://postgres:postgres@localhost:2345/test_todo_db"


@pytest.fixture
def db_engine(sqlalchemy_connect_url):
    engine = engine_from_config({"sqlalchemy.url": sqlalchemy_connect_url})
    metadata_obj.create_all(engine)
    yield engine
    metadata_obj.drop_all(engine)

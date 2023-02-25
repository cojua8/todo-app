import pytest
from app.services.sql_database_service.models import metadata_obj
from sqlalchemy import engine_from_config


@pytest.fixture(scope="session")
def sqlalchemy_connect_url():
    return "postgresql://postgres:postgres@localhost:5432/todo_db"


@pytest.fixture
def db_engine(sqlalchemy_connect_url):
    engine = engine_from_config({"sqlalchemy.url": sqlalchemy_connect_url})
    metadata_obj.create_all(engine)
    yield engine
    metadata_obj.drop_all(engine)

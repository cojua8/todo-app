from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.infrastructure.sql_database_service.models import metadata_obj
from app.settings import SqlDBSettings


async def engine(config: SqlDBSettings) -> AsyncEngine:
    db_url = URL.create(
        f"{config.db_dialect}+asyncpg",
        username=config.db_username,
        password=config.db_password,
        host=config.db_host,
        port=config.db_port,
        database=config.db_name,
    )
    engine = create_async_engine(db_url)  # use for debugging echo=True)

    SQLAlchemyInstrumentor().instrument(engine=engine.sync_engine)

    async with engine.begin() as conn:
        await conn.run_sync(metadata_obj.create_all)

    return engine

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.services.sql_database_service.models import metadata_obj


async def engine() -> AsyncEngine:
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:postgres@postgres_db:5432/todo_db",
        echo=True,
        future=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(metadata_obj.create_all)

    return engine

from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    "postgresql+asyncpg://postgres:postgres@localhost:5432/todo_db",
    echo=True,
    future=True,
)

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine

from app.domain.models.todo import Todo
from app.domain.services.todo_service_protocol import TodoServiceProtocol
from app.infrastructure.sql_database_service.base_service import BaseService
from app.infrastructure.sql_database_service.models import todo_table


class TodosService(BaseService[Todo], TodoServiceProtocol):
    def __init__(self, engine: AsyncEngine) -> None:
        super().__init__(engine, todo_table, Todo)

    async def get_all_by_user_id(self, user_id: UUID) -> list[Todo]:
        async with self._engine.connect() as conn:
            rows = await conn.execute(
                select(self._table).where(self._table.c.owner_id == user_id)
            )
        return [
            self._mappers.entity_to_model(entity, self._model)
            for entity in rows
        ]

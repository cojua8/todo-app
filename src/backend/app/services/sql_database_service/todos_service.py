from uuid import UUID

from app.models.todo import Todo
from app.services.service_protocols.todo_service_protocol import (
    TodoServiceProtocol,
)
from app.services.sql_database_service.base_service import BaseService
from app.services.sql_database_service.models import todo_table
from sqlalchemy import select
from sqlalchemy.engine import Engine


class TodosService(BaseService[Todo], TodoServiceProtocol):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, todo_table, Todo)

    def get_all_by_user_id(self, user_id: UUID):
        with self._engine.connect() as conn:
            rows = conn.execute(
                select(self._table).where(self._table.c.owner_id == user_id)
            )
        return [
            self._mappers.entity_to_model(entity, self._model)
            for entity in rows
        ]

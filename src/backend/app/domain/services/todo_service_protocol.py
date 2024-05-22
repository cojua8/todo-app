from typing import Protocol
from uuid import UUID

from app.domain.models.todo import Todo
from app.domain.services.database_service_protocol import (
    DatabaseServiceProtocol,
)


class TodoServiceProtocol(DatabaseServiceProtocol[Todo], Protocol):
    async def get_all_by_user_id(self, user_id: UUID) -> list[Todo]: ...

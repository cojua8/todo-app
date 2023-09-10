from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from app.models.todo import Todo
from app.services.service_protocols.database_service_protocol import (
    DatabaseServiceProtocol,
)

if TYPE_CHECKING:
    from uuid import UUID


class TodoServiceProtocol(DatabaseServiceProtocol[Todo], Protocol):
    async def get_all_by_user_id(self, user_id: UUID) -> list[Todo]:
        ...

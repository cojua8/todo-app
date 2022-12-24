from typing import Protocol
from uuid import UUID

from app.models.todo import Todo
from app.services.service_protocols.database_service_protocol import (
    DatabaseServiceProtocol,
)


class TodoServiceProtocol(DatabaseServiceProtocol[Todo], Protocol):
    def get_all_by_user_id(self, user_id: UUID):
        ...

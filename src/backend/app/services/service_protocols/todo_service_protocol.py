from typing import Protocol

from app.models.todo import Todo
from app.services.service_protocols.database_service_protocol import (
    DatabaseServiceProtocol,
)


class TodoServiceProtocol(DatabaseServiceProtocol[Todo], Protocol):
    ...

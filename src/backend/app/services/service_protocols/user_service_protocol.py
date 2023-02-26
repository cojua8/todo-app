from typing import Protocol

from app.models.user import User
from app.services.service_protocols.database_service_protocol import (
    DatabaseServiceProtocol,
)


class UserServiceProtocol(DatabaseServiceProtocol[User], Protocol):
    def get_by_email(self, email: str) -> User | None:
        ...

    def get_by_username(self, username: str) -> User | None:
        ...

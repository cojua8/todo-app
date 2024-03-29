from typing import Protocol

from app.models.user import User
from app.services.service_protocols.database_service_protocol import (
    DatabaseServiceProtocol,
)


class UserServiceProtocol(DatabaseServiceProtocol[User], Protocol):
    async def get_by_email(self, email: str) -> User | None:
        ...

    async def get_by_username(self, username: str) -> User | None:
        ...

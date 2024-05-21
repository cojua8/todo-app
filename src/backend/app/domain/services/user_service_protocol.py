from typing import Protocol

from app.domain.models.user import User
from app.domain.services.database_service_protocol import (
    DatabaseServiceProtocol,
)


class UserServiceProtocol(DatabaseServiceProtocol[User], Protocol):
    async def get_by_email(self, email: str) -> User | None:
        ...

    async def get_by_username(self, username: str) -> User | None:
        ...

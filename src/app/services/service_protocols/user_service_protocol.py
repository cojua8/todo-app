from typing import Optional, Protocol

from app.models.user import User
from app.services.service_protocols.database_service_protocol import (
    DatabaseServiceProtocol,
)


class UserServiceProtocol(DatabaseServiceProtocol[User], Protocol):
    def get_by_email(self, email: str) -> Optional[User]:
        ...

    def get_by_username(self, username: str) -> Optional[User]:
        ...

import asyncio
from typing import Optional

from app.models.user import User
from app.services.json_database_service.json_database_service import (
    JsonDatabaseService,
)
from app.services.service_protocols.user_service_protocol import (
    UserServiceProtocol,
)


class UsersJsonDatabaseService(JsonDatabaseService[User], UserServiceProtocol):
    def __init__(self, directory_path: str) -> None:
        model_type = User
        filename = "users.json"

        super().__init__(directory_path, filename, model_type)

    def get_by_email(self, email: str) -> Optional[User]:
        users = asyncio.run(self._get_data())

        for user in users:
            if user.email == email:
                return user

        return None

    def get_by_username(self, username: str) -> Optional[User]:
        users = asyncio.run(self._get_data())

        for user in users:
            if user.name == username:
                return user

        return None

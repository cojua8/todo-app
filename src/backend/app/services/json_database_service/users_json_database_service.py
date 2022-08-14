import asyncio
from typing import Optional

from app.models.user import User
from app.services.json_database_service.json_database_service import (
    JsonDatabaseService,
)
from app.services.service_protocols.io_service_protocol import (
    IOServiceProtocol,
)
from app.services.service_protocols.user_service_protocol import (
    UserServiceProtocol,
)


class UsersJsonDatabaseService(JsonDatabaseService[User], UserServiceProtocol):
    def __init__(self, io_service: IOServiceProtocol) -> None:
        model_type = User
        super().__init__(io_service, model_type)

    def get_by_email(self, email: str) -> Optional[User]:
        users = asyncio.run(self.__get_data())

        for user in users:
            if user.email == email:
                return user

        return None

    def get_by_username(self, username: str) -> Optional[User]:
        users = asyncio.run(self.__get_data())

        for user in users:
            if user.username == username:
                return user

        return None

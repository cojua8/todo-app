from app.domain.models.user import User
from app.domain.services.user_service_protocol import UserServiceProtocol
from app.services.json_database_service.json_database_service import (
    JsonDatabaseService,
)
from app.services.service_protocols.io_service_protocol import (
    IOServiceProtocol,
)


class UsersJsonDatabaseService(JsonDatabaseService[User], UserServiceProtocol):
    def __init__(self, io_service: IOServiceProtocol) -> None:
        model_type = User
        super().__init__(io_service, model_type)

    async def get_by_email(self, email: str) -> User | None:
        users = await self._get_data()
        return next((user for user in users if user.email == email), None)

    async def get_by_username(self, username: str) -> User | None:
        users = await self._get_data()
        return next(
            (user for user in users if user.username == username), None
        )

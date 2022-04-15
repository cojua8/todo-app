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

from app.models.user import User
from app.services.json_database_service.json_database_service import (
    JsonDatabaseService,
)


class UsersJsonDatabaseService(JsonDatabaseService[User]):
    T = User
    filename = "users.json"
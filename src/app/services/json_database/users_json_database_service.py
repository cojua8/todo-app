from models.user import User
from services.json_database.json_database_service import JsonDatabaseService


class UsersJsonDatabaseService(JsonDatabaseService[User]):
    T = User

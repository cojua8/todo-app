from models.todo import Todo
from services.json_database.json_database_service import JsonDatabaseService


class TodosJsonDatabaseService(JsonDatabaseService[Todo]):
    T = Todo

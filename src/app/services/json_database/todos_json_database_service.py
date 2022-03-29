from app.models.todo import Todo
from app.services.json_database.json_database_service import (
    JsonDatabaseService,
)


class TodosJsonDatabaseService(JsonDatabaseService[Todo]):
    T = Todo
    filename = "todos.json"

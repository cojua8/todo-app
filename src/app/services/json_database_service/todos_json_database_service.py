from app.models.todo import Todo
from app.services.json_database_service.json_database_service import (
    JsonDatabaseService,
)


class TodosJsonDatabaseService(JsonDatabaseService[Todo]):
    model_type = Todo
    filename = "todos.json"

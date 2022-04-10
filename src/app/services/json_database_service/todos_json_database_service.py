from app.models.todo import Todo
from app.services.json_database_service.json_database_service import (
    JsonDatabaseService,
)
from app.services.service_protocols.database_service_protocol import (
    DatabaseServiceProtocol,
)


class TodosJsonDatabaseService(
    JsonDatabaseService[Todo], DatabaseServiceProtocol[Todo]
):
    def __init__(self, directory_path: str) -> None:
        filename = "todos.json"
        model_type = Todo

        super().__init__(directory_path, filename, model_type)

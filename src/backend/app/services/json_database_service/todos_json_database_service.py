from app.models.todo import Todo
from app.services.json_database_service.json_database_service import (
    JsonDatabaseService,
)
from app.services.service_protocols.io_service_protocol import (
    IOServiceProtocol,
)
from app.services.service_protocols.todo_service_protocol import (
    TodoServiceProtocol,
)


class TodosJsonDatabaseService(JsonDatabaseService[Todo], TodoServiceProtocol):
    def __init__(self, io_service: IOServiceProtocol) -> None:
        model_type = Todo
        super().__init__(io_service, model_type)

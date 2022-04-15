from http import HTTPStatus
from typing import Any

from dependency_injector.wiring import Provide, inject
from flask_restful import Resource

from app.containers import Container
from app.models.todo import Todo
from app.services.service_protocols.database_service_protocol import (
    DatabaseServiceProtocol,
)


class TodoListing(Resource):
    @inject
    def __init__(
        self,
        db_service: DatabaseServiceProtocol[Todo] = (
            Provide[Container.todos_database]
        ),
    ) -> None:
        super().__init__()
        self.todo_db_service = db_service
        self.T = Todo

    def get(self):
        response: dict[str, Any] = {}
        try:
            users = self.todo_db_service.get_all()

            response["status"] = HTTPStatus.OK
            response["response"] = users
        except Exception as e:
            response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            response["response"] = str(e)

        return response

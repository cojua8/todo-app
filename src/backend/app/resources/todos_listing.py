from http import HTTPStatus
from typing import Any

from app.containers import Container
from app.services.service_protocols.todo_service_protocol import (
    TodoServiceProtocol,
)
from dependency_injector.wiring import Provide, inject
from flask_restful import Resource


class TodoListing(Resource):
    @inject
    def __init__(
        self,
        todo_service: TodoServiceProtocol = Provide[Container.todos_service],
    ) -> None:
        self.todo_service = todo_service

    def get(self):
        response: dict[str, Any] = {}
        try:
            users = self.todo_service.get_all()

            response["status"] = HTTPStatus.OK
            response["response"] = users
        except Exception as e:
            response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            response["response"] = str(e)

        return response

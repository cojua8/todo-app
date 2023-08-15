from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any

from dependency_injector.wiring import Provide, inject
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs

from app.containers import Container
from app.models.todo import Todo

if TYPE_CHECKING:
    from app.services.service_protocols.todo_service_protocol import (
        TodoServiceProtocol,
    )


class Todos(Resource):
    @inject
    def __init__(
        self,
        todo_service: TodoServiceProtocol = Provide[Container.todos_service],
    ) -> None:
        self.todo_service = todo_service

    @use_kwargs({"id": fields.UUID()}, location="json")
    def get(self, **kwargs) -> dict[str, Any]:
        response: dict[str, Any] = {}
        id_ = kwargs["id"]
        try:
            todo = self.todo_service.get(id_)

            response["status"] = HTTPStatus.OK
            response["response"] = todo
        except Exception as e:
            response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            response["response"] = str(e)

        return response

    @use_kwargs(
        {
            "owner_id": fields.UUID(),
            "description": fields.Str(),
            "due_date": fields.Date(),
        },
        location="json",
    )
    def post(self, **kwargs) -> dict[str, Any]:
        response: dict[str, Any] = {}
        new = Todo(**kwargs)

        try:
            self.todo_service.create(new)
            response["status"] = HTTPStatus.OK
        except Exception as e:
            response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            response["response"] = str(e)

        return response

    @use_kwargs({"id": fields.UUID()}, location="json")
    def delete(self, **kwargs) -> dict[str, Any]:
        response: dict[str, Any] = {}
        id_ = kwargs["id"]
        try:
            self.todo_service.delete(id_)
            response["status"] = HTTPStatus.OK
        except Exception as e:
            response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            response["response"] = str(e)

        return response

    @use_kwargs(
        {
            "id": fields.UUID(),
            "owner_id": fields.UUID(),
            "description": fields.Str(),
            "date_created": fields.Date(),
            "due_date": fields.Date(),
            "completed": fields.Bool(),
        },
        location="json",
    )
    def put(self, **kwargs) -> dict[str, Any]:
        response: dict[str, Any] = {}
        id_ = kwargs["id"]
        new = Todo(**kwargs)
        try:
            self.todo_service.put(id_, new)
            response["status"] = HTTPStatus.OK
        except Exception as e:
            response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            response["response"] = str(e)

        return response

from http import HTTPStatus
from typing import Any

from flask_restful import Resource
from app.models.todo import Todo
from app.services.base_database_service.base_database_service import (
    IDatabaseService,
)
from webargs import fields
from webargs.flaskparser import use_kwargs


class Todos(Resource):
    def __init__(self, db_service: IDatabaseService[Todo]) -> None:
        super().__init__()
        self.todo_db_service = db_service
        self.T = Todo

    @use_kwargs(
        {
            "id": fields.UUID(),
        },
        location="json",
    )
    def get(self, **kwargs) -> dict[str, Any]:
        response: dict[str, Any] = {}
        id = kwargs["id"]
        try:
            todo = self.todo_db_service.get(id)

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
        new = self.T(**kwargs)

        try:
            self.todo_db_service.create(new)
            response["status"] = HTTPStatus.OK
        except Exception as e:
            response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            response["response"] = str(e)

        return response

    @use_kwargs(
        {
            "id": fields.UUID(),
        },
        location="json",
    )
    def delete(self, **kwargs) -> dict[str, Any]:
        response: dict[str, Any] = {}
        id = kwargs["id"]
        try:
            self.todo_db_service.delete(id)
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
        id = kwargs["id"]
        new = self.T(**kwargs)
        try:
            self.todo_db_service.put(id, new)
            response["status"] = HTTPStatus.OK
        except Exception as e:
            response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            response["response"] = str(e)

        return response

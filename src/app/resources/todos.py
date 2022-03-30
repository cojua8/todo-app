from http import HTTPStatus
import os
from typing import Any

from flask_restful import Resource
from app.models.todo import Todo
from app.services.base_database_service.base_database_service import (
    IDatabaseService,
)
from app.services.json_database_service.todos_json_database_service import (
    TodosJsonDatabaseService,
)
from webargs import fields
from webargs.flaskparser import use_kwargs


class Todos(Resource):
    T = Todo
    todo_db_service: IDatabaseService[Todo] = TodosJsonDatabaseService(
        os.environ["DATABASE_PATH"]
    )

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

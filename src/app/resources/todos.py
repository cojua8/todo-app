from http import HTTPStatus
import os
from typing import Any
from urllib.error import HTTPError
from flask_restful import Resource
from app.models.todo import Todo
from app.services.json_database.todos_json_database_service import (
    TodosJsonDatabaseService,
)
from webargs import fields
from webargs.flaskparser import use_kwargs


class Todos(Resource):
    T = Todo
    todo_db_service = TodosJsonDatabaseService(os.environ["DATABASE_PATH"])

    def get(self) -> dict[str, Any]:
        response = {}
        try:
            users = self.todo_db_service.get_all()

            response["status"] = HTTPStatus.OK
            response["response"] = users
        except HTTPError as e:
            response["status"] = HTTPStatus(e.code)

        return response

    @use_kwargs(
        {
            "id": fields.Int(),
            "owner_id": fields.Int(),
            "description": fields.Str(),
            "date_created": fields.Date(),
            "due_date": fields.Date(),
            "completed": fields.Bool(),
        },
        location="json",
    )
    def post(self, **kwargs) -> dict[str, str]:
        status_message = ""

        new = self.T(**kwargs)

        try:
            self.todo_db_service.create(new)
            status_message = "Success!"
        except Exception as e:
            status_message = str(e)

        return {"status": status_message}

    @use_kwargs({"id": fields.Int()}, location="json")
    def delete(self, **kwargs) -> dict[str, str]:
        status_message = ""
        id = kwargs["id"]
        try:
            self.todo_db_service.delete(id)
            status_message = "Success!"
        except Exception as e:
            status_message = str(e)

        return {"status": status_message}

    @use_kwargs(
        {
            "id": fields.Int(),
            "owner_id": fields.Int(),
            "description": fields.Str(),
            "date_created": fields.Date(),
            "due_date": fields.Date(),
            "completed": fields.Bool(),
        },
        location="json",
    )
    def put(self, **kwargs) -> dict[str, str]:
        status_message = ""
        id = kwargs["id"]
        new = self.T(**kwargs)
        try:
            self.todo_db_service.put(id, new)
            status_message = "Success!"
        except Exception as e:
            status_message = str(e)

        return {"status": status_message}

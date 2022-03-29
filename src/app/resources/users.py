from http import HTTPStatus
import os

from typing import Any
from urllib.error import HTTPError

from app.services.json_database.users_json_database_service import (
    UsersJsonDatabaseService,
)
from app.models.user import User

from flask_restful import Resource
from webargs.flaskparser import use_kwargs
from webargs import fields


class Users(Resource):
    T = User
    user_db_service = UsersJsonDatabaseService(os.getenv("DATABASE_PATH"))

    def get(self) -> dict[str, Any]:
        response = {}
        try:
            users = self.user_db_service.get_all()

            response["status"] = HTTPStatus.OK
            response["response"] = users
        except HTTPError as e:
            response["status"] = e.code

        return response

    @use_kwargs(
        {
            "id": fields.Int(),
            "name": fields.String(),
            "email": fields.Email(),
        },
        location="json",
    )
    def post(self, **kwargs) -> dict[str, str]:
        status_message = ""
        user = self.T(**kwargs)
        try:
            self.user_db_service.create(user)
            status_message = "Success!"
        except Exception as e:
            status_message = str(e)

        return {"status": status_message}

    @use_kwargs({"id": fields.Int()}, location="json")
    def delete(self, **kwargs) -> dict[str, str]:
        status_message = ""
        id = kwargs["id"]
        try:
            self.user_db_service.delete(id)
            status_message = "Success!"
        except Exception as e:
            status_message = str(e)

        return {"status": status_message}

    @use_kwargs(
        {"id": fields.Int(), "name": fields.String(), "email": fields.Email()},
        location="json",
    )
    def put(self, **kwargs) -> dict[str, str]:
        status_message = ""
        id = kwargs["id"]
        new = self.T(**kwargs)
        try:
            self.user_db_service.put(id, new)
            status_message = "Success!"
        except Exception as e:
            status_message = str(e)

        return {"status": status_message}

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
    user_db_service = UsersJsonDatabaseService(os.environ["DATABASE_PATH"])

    def get(self) -> dict[str, Any]:
        response: dict[str, Any] = {}
        try:
            users = self.user_db_service.get_all()

            response["status"] = HTTPStatus.OK
            response["response"] = users
        except Exception as e:
            response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            response["response"] = str(e)

        return response

    @use_kwargs(
        {
            "id": fields.Int(),
            "name": fields.String(),
            "email": fields.Email(),
        },
        location="json",
    )
    def post(self, **kwargs) -> dict[str, Any]:
        response: dict[str, Any] = {}
        user = self.T(**kwargs)
        try:
            self.user_db_service.create(user)
            response["status"] = HTTPStatus.OK
        except Exception as e:
            response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            response["response"] = str(e)

        return response

    @use_kwargs(
        {
            "id": fields.Int(),
        },
        location="json",
    )
    def delete(self, **kwargs) -> dict[str, Any]:
        response: dict[str, Any] = {}
        id = kwargs["id"]
        try:
            self.user_db_service.delete(id)
            response["status"] = HTTPStatus.OK
        except Exception as e:
            response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            response["response"] = str(e)

        return response

    @use_kwargs(
        {
            "id": fields.Int(),
            "name": fields.String(),
            "email": fields.Email(),
        },
        location="json",
    )
    def put(self, **kwargs) -> dict[str, Any]:
        response: dict[str, Any] = {}
        id = kwargs["id"]
        new = self.T(**kwargs)
        try:
            self.user_db_service.put(id, new)
            response["status"] = HTTPStatus.OK
        except Exception as e:
            response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            response["response"] = str(e)

        return response

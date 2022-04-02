from http import HTTPStatus


from typing import Any


from app.services.base_database_service.base_database_service import (
    IDatabaseService,
)


from app.models.user import User

from flask_restful import Resource
from webargs.flaskparser import use_kwargs
from webargs import fields


class Users(Resource):
    def __init__(self, db_service: IDatabaseService[User]) -> None:
        super().__init__()
        self.user_db_service = db_service
        self.T = User

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
            user = self.user_db_service.get(id)

            response["status"] = HTTPStatus.OK
            response["response"] = user
        except Exception as e:
            response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            response["response"] = str(e)

        return response

    @use_kwargs(
        {
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
            "id": fields.UUID(),
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
            "id": fields.UUID(),
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

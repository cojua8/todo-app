from http import HTTPStatus
from typing import Any

from dependency_injector.wiring import Provide, inject
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs

from app.containers import Container
from app.models.user import User
from app.services.service_protocols.database_service_protocol import (
    DatabaseServiceProtocol,
)


class Users(Resource):
    @inject
    def __init__(
        self,
        db_service: DatabaseServiceProtocol[User] = (
            Provide[Container.users_database]
        ),
    ) -> None:
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

from http import HTTPStatus
from typing import Any

from app.containers import Container
from app.models.user import User
from app.services.service_protocols.user_service_protocol import (
    UserServiceProtocol,
)
from dependency_injector.wiring import Provide, inject
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs


class Users(Resource):
    @inject
    def __init__(
        self,
        user_service: UserServiceProtocol = (Provide[Container.users_service]),
    ) -> None:
        self.user_service = user_service

    @use_kwargs(
        {
            "id": fields.UUID(),
        },
        location="json",
    )
    def get(self, **kwargs) -> dict[str, Any]:
        response: dict[str, Any] = {}
        id_ = kwargs["id"]
        try:
            user = self.user_service.get(id_)

            response["status"] = HTTPStatus.OK
            response["response"] = user
        except Exception as e:
            response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            response["response"] = str(e)

        return response

    @use_kwargs(
        {
            "username": fields.String(),
            "email": fields.Email(),
            "password": fields.String(),
        },
        location="json",
    )
    def post(self, **kwargs) -> dict[str, Any]:
        response: dict[str, Any] = {}
        user = User(**kwargs)
        try:
            self.user_service.create(user)
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
        id_ = kwargs["id"]
        try:
            self.user_service.delete(id_)
            response["status"] = HTTPStatus.OK
        except Exception as e:
            response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            response["response"] = str(e)

        return response

    @use_kwargs(
        {
            "id": fields.UUID(),
            "username": fields.String(),
            "email": fields.Email(),
            "password": fields.String(),
        },
        location="json",
    )
    def put(self, **kwargs) -> dict[str, Any]:
        response: dict[str, Any] = {}
        id_ = kwargs["id"]
        new = User(**kwargs)
        try:
            self.user_service.put(id_, new)
            response["status"] = HTTPStatus.OK
        except Exception as e:
            response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            response["response"] = str(e)

        return response

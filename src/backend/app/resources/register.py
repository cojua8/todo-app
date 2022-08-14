from http import HTTPStatus
from typing import Any

from app.containers import Container
from app.services.service_protocols.authentication_service_protocol import (
    AuthenticationServiceProtocol,
)
from dependency_injector.wiring import Provide, inject
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs


class Register(Resource):
    @inject
    def __init__(
        self,
        authentication_service: AuthenticationServiceProtocol = Provide[
            Container.authentication_service
        ],
    ) -> None:
        self.authentication_service = authentication_service

    @use_kwargs(
        {
            "username": fields.String(),
            "email": fields.Email(),
            "password": fields.String(),
            "confirm_password": fields.String(),
        },
        location="json",
    )
    def post(
        self, username, email, password, confirm_password
    ) -> dict[str, Any]:
        response: dict[str, Any] = {}
        try:
            result = self.authentication_service.register(
                username=username,
                email=email,
                password=password,
                confirm_password=confirm_password,
            )

            response["status"] = HTTPStatus.OK
            response["response"] = result.name
        except Exception as e:
            response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            response["response"] = str(e)

        return response

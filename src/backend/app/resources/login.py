from http import HTTPStatus
from typing import Any

from app.containers import Container
from app.exceptions.login_exception import LoginException
from app.services.service_protocols.authentication_service_protocol import (
    AuthenticationServiceProtocol,
)
from dependency_injector.wiring import Provide, inject
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs


class Login(Resource):
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
            "password": fields.String(),
        },
        location="json",
    )
    def post(self, username, password) -> dict[str, Any]:
        response: dict[str, Any] = {}
        try:
            user = self.authentication_service.login(
                username=username, password=password
            )

            response["status"] = HTTPStatus.OK
            response["response"] = user
        except LoginException as e:
            response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            response["response"] = str(e)

        return response

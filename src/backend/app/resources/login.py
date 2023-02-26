from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any

from dependency_injector.wiring import Provide, inject
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs

from app.containers import Container
from app.exceptions.login_exception import LoginError

if TYPE_CHECKING:
    from app.services.service_protocols.authentication_service_protocol import (  # noqa: E501
        AuthenticationServiceProtocol,
    )


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
    def post(self, username: str, password: str) -> dict[str, Any]:
        response: dict[str, Any] = {}
        try:
            user = self.authentication_service.login(
                username=username, password=password
            )

            response["status"] = HTTPStatus.OK
            response["response"] = user
        except LoginError as e:
            response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
            response["response"] = str(e)

        return response

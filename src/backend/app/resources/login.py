from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any

from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from webargs import fields
from webargs.flaskparser import use_kwargs

from app.containers import Container
from app.exceptions.login_exception import LoginError

if TYPE_CHECKING:
    from app.services.service_protocols.authentication_service_protocol import (  # noqa: E501
        AuthenticationServiceProtocol,
    )

login_blueprint = Blueprint("login", __name__)


@login_blueprint.post("/login")
@inject
@use_kwargs(
    {"username": fields.String(), "password": fields.String()}, location="json"
)
async def post(
    username: str,
    password: str,
    authentication_service: AuthenticationServiceProtocol = Provide[
        Container.authentication_service
    ],
) -> dict[str, Any]:
    response: dict[str, Any] = {}
    try:
        user = await authentication_service.login(
            username=username, password=password
        )

        response["status"] = HTTPStatus.OK
        response["response"] = user
    except LoginError as e:
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
        response["response"] = str(e)

    return response

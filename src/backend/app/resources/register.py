from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any

from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from webargs import fields
from webargs.flaskparser import use_kwargs

from app.containers import Container

if TYPE_CHECKING:
    from app.services.service_protocols.authentication_service_protocol import (  # noqa: E501
        AuthenticationServiceProtocol,
    )

register_blueprint = Blueprint("register", __name__)


@register_blueprint.post("/register")
@inject
@use_kwargs(
    {
        "username": fields.String(),
        "email": fields.Email(),
        "password": fields.String(),
        "confirm_password": fields.String(),
    },
    location="json",
)
async def post(
    username: str,
    email: str,
    password: str,
    confirm_password: str,
    authentication_service: AuthenticationServiceProtocol = Provide[
        Container.authentication_service
    ],
) -> dict[str, Any]:
    response: dict[str, Any] = {}
    try:
        result = await authentication_service.register(
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

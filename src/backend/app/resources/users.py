from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any

from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from webargs import fields
from webargs.flaskparser import use_kwargs

from app.containers import Container
from app.models.user import User

if TYPE_CHECKING:
    from app.services.service_protocols.user_service_protocol import (
        UserServiceProtocol,
    )

users_blueprint = Blueprint("user", __name__)


@users_blueprint.get("/user")
@inject
@use_kwargs({"id": fields.UUID()}, location="json")
async def get(
    user_service: UserServiceProtocol = Provide[Container.users_service],
    **kwargs,
) -> dict[str, Any]:
    response: dict[str, Any] = {}
    id_ = kwargs["id"]
    try:
        user = await user_service.get(id_)

        response["status"] = HTTPStatus.OK
        response["response"] = user
    except Exception as e:
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
        response["response"] = str(e)

    return response


@users_blueprint.post("/user")
@inject
@use_kwargs(
    {
        "username": fields.String(),
        "email": fields.Email(),
        "password": fields.String(),
    },
    location="json",
)
async def post(
    user_service: UserServiceProtocol = Provide[Container.users_service],
    **kwargs,
) -> dict[str, Any]:
    response: dict[str, Any] = {}
    user = User(**kwargs)
    try:
        await user_service.create(user)
        response["status"] = HTTPStatus.OK
    except Exception as e:
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
        response["response"] = str(e)

    return response


@users_blueprint.delete("/user")
@inject
@use_kwargs({"id": fields.UUID()}, location="json")
async def delete(
    user_service: UserServiceProtocol = Provide[Container.users_service],
    **kwargs,
) -> dict[str, Any]:
    response: dict[str, Any] = {}
    id_ = kwargs["id"]
    try:
        await user_service.delete(id_)
        response["status"] = HTTPStatus.OK
    except Exception as e:
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
        response["response"] = str(e)

    return response


@users_blueprint.put("/user")
@inject
@use_kwargs(
    {
        "id": fields.UUID(),
        "username": fields.String(),
        "email": fields.Email(),
        "password": fields.String(),
    },
    location="json",
)
async def put(
    user_service: UserServiceProtocol = Provide[Container.users_service],
    **kwargs,
) -> dict[str, Any]:
    response: dict[str, Any] = {}
    id_ = kwargs["id"]
    new = User(**kwargs)
    try:
        await user_service.put(id_, new)
        response["status"] = HTTPStatus.OK
    except Exception as e:
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
        response["response"] = str(e)

    return response

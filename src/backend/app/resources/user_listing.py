from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any

from dependency_injector.wiring import Provide, inject
from flask import Blueprint

from app.containers import Container

if TYPE_CHECKING:
    from app.services.service_protocols.user_service_protocol import (
        UserServiceProtocol,
    )

user_listing_blueprint = Blueprint("users", __name__)


@user_listing_blueprint.get("/users")
@inject
async def get(
    user_service: UserServiceProtocol = Provide[Container.users_service],
) -> dict[str, Any]:
    response: dict[str, Any] = {}
    try:
        users = await user_service.get_all()

        response["status"] = HTTPStatus.OK
        response["response"] = users
    except Exception as e:
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
        response["response"] = str(e)

    return response

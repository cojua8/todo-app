from http import HTTPStatus
from typing import Any

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter

from app.containers import Container
from app.services.service_protocols.user_service_protocol import (
    UserServiceProtocol,
)

user_listing_router = APIRouter()


@user_listing_router.get("/users")
@inject
async def get(
    user_service: UserServiceProtocol = fastapi.Depends(
        Provide[Container.users_service]
    ),
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

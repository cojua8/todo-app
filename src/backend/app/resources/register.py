from http import HTTPStatus
from typing import Annotated, Any

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body

from app.containers import Container
from app.services.service_protocols.authentication_service_protocol import (
    AuthenticationServiceProtocol,
)

register_router = APIRouter()


@register_router.post("/register")
@inject
async def post(
    username: Annotated[str, Body()],
    email: Annotated[str, Body()],
    password: Annotated[str, Body()],
    confirm_password: Annotated[str, Body()],
    authentication_service: AuthenticationServiceProtocol = fastapi.Depends(
        Provide[Container.authentication_service]
    ),
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

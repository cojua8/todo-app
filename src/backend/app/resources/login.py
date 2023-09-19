from http import HTTPStatus
from typing import Annotated, Any

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body

from app.containers import Container
from app.exceptions.login_exception import LoginError
from app.services.service_protocols.authentication_service_protocol import (
    AuthenticationServiceProtocol,
)

login_router = APIRouter()


@login_router.post("/login")
@inject
async def post(
    username: Annotated[str, Body()],
    password: Annotated[str, Body()],
    authentication_service: AuthenticationServiceProtocol = fastapi.Depends(
        Provide[Container.authentication_service]
    ),
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

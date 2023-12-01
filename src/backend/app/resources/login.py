from http import HTTPStatus
from typing import Annotated, Any

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Response

from app.containers import Container
from app.exceptions.login_exception import LoginError
from app.models.user import User
from app.services.service_protocols.authentication_service_protocol import (
    AuthenticationServiceProtocol,
)

login_router = APIRouter()


@login_router.post("/login")
@inject
async def post(
    username: Annotated[str, Body()],
    password: Annotated[str, Body()],
    response: Response,
    authentication_service: AuthenticationServiceProtocol = fastapi.Depends(
        Provide[Container.authentication_service]
    ),
) -> User | dict[str, Any]:
    try:
        user = await authentication_service.login(
            username=username, password=password
        )
    except LoginError as e:
        response.status_code = HTTPStatus.BAD_REQUEST
        return {"result": str(e)}
    else:
        return user

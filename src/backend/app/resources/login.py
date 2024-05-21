from http import HTTPStatus
from typing import Annotated

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Response

from app.containers import Container
from app.domain.models.user import User
from app.domain.services.authentication_service_protocol import (
    AuthenticationServiceProtocol,
)
from app.exceptions.login_exception import LoginError

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
) -> User | None:
    try:
        user = await authentication_service.login(
            username=username, password=password
        )
    except LoginError:
        response.status_code = HTTPStatus.BAD_REQUEST
        return None
    else:
        return user

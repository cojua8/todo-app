from http import HTTPStatus
from typing import Annotated, Any

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from app.containers import Container
from app.domain.exceptions.login_exception import LoginError
from app.domain.services.authentication_service_protocol import (
    AuthenticationServiceProtocol,
)
from app.presentation.fastapi.exceptions.login_error import (
    LoginError as ApiLoginError,
)
from app.presentation.fastapi.models.login_data import LoginData
from app.presentation.fastapi.models.user import User as ApiUser

login_router = APIRouter()


@login_router.post(
    "/login",
    response_model=ApiUser,
    responses={HTTPStatus.BAD_REQUEST: {"model": ApiLoginError}},
)
@inject
async def post(
    logged_user: Annotated[LoginData, Body()],
    authentication_service: AuthenticationServiceProtocol = fastapi.Depends(
        Provide[Container.authentication_service]
    ),
) -> Any:  # noqa: ANN401
    try:
        user = await authentication_service.login(
            username=logged_user.username, password=logged_user.password
        )
    except LoginError:
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST, content=ApiLoginError()
        )
    else:
        return user

from http import HTTPStatus
from typing import Annotated, Any

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse

from app.containers import Container
from app.domain.services.authentication_service_protocol import (
    AuthenticationServiceProtocol,
    RegistrationResult,
)
from app.presentation.fastapi.exceptions.register_error import RegisterError
from app.presentation.fastapi.models.register_data import RegisterData
from app.presentation.fastapi.models.user import User as ApiUser

register_router = APIRouter()


@register_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiUser,
    responses={HTTPStatus.BAD_REQUEST: {"model": RegisterError}},
)
@inject
async def post(
    register_data: Annotated[RegisterData, Body()],
    authentication_service: AuthenticationServiceProtocol = fastapi.Depends(
        Provide[Container.authentication_service]
    ),
) -> Any:  # noqa: ANN401
    result, user = await authentication_service.register(
        username=register_data.username,
        email=register_data.email,
        password=register_data.password,
        confirm_password=register_data.confirm_password,
    )

    if result != RegistrationResult.SUCCESS:
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content=RegisterError(result=result),
        )

    return user

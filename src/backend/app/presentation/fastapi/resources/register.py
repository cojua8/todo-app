from typing import Annotated, Any

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, status

from app.containers import Container
from app.domain.models.user import User
from app.domain.services.authentication_service_protocol import (
    AuthenticationServiceProtocol,
    RegistrationResult,
)
from app.presentation.fastapi.exceptions.register_error import RegisterError
from app.presentation.fastapi.models.register_data import RegisterData

register_router = APIRouter()


@register_router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=User
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
        raise RegisterError(result)

    return user

from dataclasses import asdict
from http import HTTPStatus
from typing import Annotated, Any, cast

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Response, status
from pydantic import EmailStr

from app.containers import Container
from app.models.user import User
from app.services.service_protocols.authentication_service_protocol import (
    AuthenticationServiceProtocol,
    RegistrationResult,
)

register_router = APIRouter()


@register_router.post("/register", status_code=status.HTTP_201_CREATED)
@inject
async def post(  # noqa: PLR0913
    username: Annotated[str, Body()],
    email: Annotated[EmailStr, Body()],
    password: Annotated[str, Body()],
    confirm_password: Annotated[str, Body(alias="confirmPassword")],
    response: Response,
    authentication_service: AuthenticationServiceProtocol = fastapi.Depends(
        Provide[Container.authentication_service]
    ),
) -> dict[str, Any]:
    result, user = await authentication_service.register(
        username=username,
        email=email,
        password=password,
        confirm_password=confirm_password,
    )

    if result != RegistrationResult.SUCCESS:
        response.status_code = HTTPStatus.BAD_REQUEST
        return {"result": result.name}

    return asdict(cast(User, user))

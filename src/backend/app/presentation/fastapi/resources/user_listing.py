from typing import Any

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter

from app.containers import Container
from app.domain.services.user_service_protocol import UserServiceProtocol
from app.presentation.fastapi.models.user import User as ApiUser

user_listing_router = APIRouter()


@user_listing_router.get("/users", response_model=list[ApiUser])
@inject
async def get(
    user_service: UserServiceProtocol = fastapi.Depends(
        Provide[Container.users_service]
    ),
) -> Any:  # noqa: ANN401
    return await user_service.get_all()

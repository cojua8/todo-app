import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter

from app.containers import Container
from app.domain.models.user import User
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
) -> list[User]:
    return await user_service.get_all()

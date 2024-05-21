from typing import Annotated
from uuid import UUID

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Query

from app.containers import Container
from app.domain.models.todo import Todo
from app.domain.services.todo_service_protocol import TodoServiceProtocol

todo_listing_router = APIRouter()


@todo_listing_router.get("/todos")
@inject
async def get(
    user_id: Annotated[UUID, Query()],
    todo_service: TodoServiceProtocol = fastapi.Depends(
        Provide[Container.todos_service]
    ),
) -> list[Todo]:
    return await todo_service.get_all_by_user_id(user_id)

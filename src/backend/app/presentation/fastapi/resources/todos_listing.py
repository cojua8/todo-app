from typing import Annotated, Any
from uuid import UUID

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Query

from app.containers import Container
from app.domain.services.todo_service_protocol import TodoServiceProtocol
from app.presentation.fastapi.models.todo import Todo as ApiTodo

todo_listing_router = APIRouter()


@todo_listing_router.get("/todos", response_model=list[ApiTodo])
@inject
async def get(
    user_id: Annotated[UUID, Query()],
    todo_service: TodoServiceProtocol = fastapi.Depends(
        Provide[Container.todos_service]
    ),
) -> Any:  # noqa: ANN401
    return await todo_service.get_all_by_user_id(user_id)

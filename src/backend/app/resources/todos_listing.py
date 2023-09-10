from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any

from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from webargs import fields
from webargs.flaskparser import use_kwargs

from app.containers import Container

if TYPE_CHECKING:
    from uuid import UUID

    from app.services.service_protocols.todo_service_protocol import (
        TodoServiceProtocol,
    )

todo_listing_blueprint = Blueprint("todos", __name__)


@todo_listing_blueprint.get("/todos")
@inject
@use_kwargs({"user_id": fields.UUID()}, location="query")
async def get(
    user_id: UUID,
    todo_service: TodoServiceProtocol = Provide[Container.todos_service],
) -> dict[str, Any]:
    response: dict[str, Any] = {}
    try:
        users = await todo_service.get_all_by_user_id(user_id)

        response["status"] = HTTPStatus.OK
        response["response"] = users
    except Exception as e:
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
        response["response"] = str(e)

    return response

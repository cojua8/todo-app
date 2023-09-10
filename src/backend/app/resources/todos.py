from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any

from dependency_injector.wiring import Provide, inject
from flask import Blueprint
from webargs import fields
from webargs.flaskparser import use_kwargs

from app.containers import Container
from app.models.todo import Todo

if TYPE_CHECKING:
    from app.services.service_protocols.todo_service_protocol import (
        TodoServiceProtocol,
    )

todo_blueprint = Blueprint("todo", __name__)


@todo_blueprint.get("/todo")
@inject
@use_kwargs({"id": fields.UUID()}, location="json")
async def get(
    todo_service: TodoServiceProtocol = Provide[Container.todos_service],
    **kwargs,
) -> dict[str, Any]:
    response: dict[str, Any] = {}
    id_ = kwargs["id"]
    try:
        todo = await todo_service.get(id_)

        response["status"] = HTTPStatus.OK
        response["response"] = todo
    except Exception as e:
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
        response["response"] = str(e)

    return response


@todo_blueprint.post("/todo")
@inject
@use_kwargs(
    {
        "owner_id": fields.UUID(),
        "description": fields.Str(),
        "due_date": fields.Date(),
    },
    location="json",
)
async def post(
    todo_service: TodoServiceProtocol = Provide[Container.todos_service],
    **kwargs,
) -> dict[str, Any]:
    response: dict[str, Any] = {}
    new = Todo(**kwargs)

    try:
        await todo_service.create(new)
        response["status"] = HTTPStatus.OK
    except Exception as e:
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
        response["response"] = str(e)

    return response


@todo_blueprint.delete("/todo")
@inject
@use_kwargs({"id": fields.UUID()}, location="json")
async def delete(
    todo_service: TodoServiceProtocol = Provide[Container.todos_service],
    **kwargs,
) -> dict[str, Any]:
    response: dict[str, Any] = {}
    id_ = kwargs["id"]
    try:
        await todo_service.delete(id_)
        response["status"] = HTTPStatus.OK
    except Exception as e:
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
        response["response"] = str(e)

    return response


@todo_blueprint.put("/todo")
@inject
@use_kwargs(
    {
        "id": fields.UUID(),
        "owner_id": fields.UUID(),
        "description": fields.Str(),
        "date_created": fields.Date(),
        "due_date": fields.Date(),
        "completed": fields.Bool(),
    },
    location="json",
)
async def put(
    todo_service: TodoServiceProtocol = Provide[Container.todos_service],
    **kwargs,
) -> dict[str, Any]:
    response: dict[str, Any] = {}
    id_ = kwargs["id"]
    new = Todo(**kwargs)
    try:
        await todo_service.put(id_, new)
        response["status"] = HTTPStatus.OK
    except Exception as e:
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
        response["response"] = str(e)

    return response

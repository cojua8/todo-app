from typing import NamedTuple
from uuid import uuid4

import pytest

from app.infrastructure.io_service import IOServiceProtocol
from app.infrastructure.json_database_service.todos_json_database_service import (  # noqa: E501
    TodosJsonDatabaseService,
)
from app.utils import json_utils
from tests.factories.todo_factory import TodoFactory


class SetupParams(NamedTuple):
    expected_values: dict
    created_count: int


@pytest.fixture
def setup_todos(todo_factory: TodoFactory):
    default_params = SetupParams({}, 2)

    def _setup_todos(params: SetupParams = default_params):
        expected_values = params.expected_values
        expected_todo = todo_factory.create(**expected_values)

        existing_todo = todo_factory.create_batch(params.created_count)

        db_todos = [expected_todo, *existing_todo]

        return db_todos, expected_todo

    return _setup_todos


@pytest.fixture
def setup_service(mocker):
    io_service = mocker.MagicMock(spec=IOServiceProtocol)
    service = TodosJsonDatabaseService(io_service)

    yield service, io_service


@pytest.mark.parametrize(
    "params",
    [SetupParams({}, 4), SetupParams({}, 0)],
    ids=["return_todo", "return_empty"],
)
async def test_get_all_ok(params, setup_todos, setup_service):
    # arrange
    todos, _ = setup_todos(params)
    todo_service, io_service = setup_service
    io_service.read.return_value = json_utils.dumps(todos)

    # act
    actual_todos = await todo_service.get_all()

    # assert
    assert actual_todos == todos


async def test_get_returns_todo(setup_todos, setup_service):
    # arrange
    todos, expected_todo = setup_todos(SetupParams({"id": uuid4()}, 2))
    todo_service, io_service = setup_service
    io_service.read.return_value = json_utils.dumps(todos)

    # act
    actual_todo = await todo_service.get(expected_todo.id)

    # assert
    assert actual_todo.id == expected_todo.id


async def test_get_returns_none(setup_todos, setup_service):
    # arrange
    todos, _ = setup_todos(SetupParams({}, 1))
    todo_service, io_service = setup_service
    io_service.read.return_value = json_utils.dumps(todos)
    searched_id = uuid4()

    # act
    actual_todo = await todo_service.get(searched_id)

    # assert
    assert actual_todo is None


async def test_create_returns_todo(setup_service, todo_factory):
    # arrange
    todo = todo_factory.create()
    todo_service, io_service = setup_service
    io_service.read.return_value = "[]"

    # act
    new_item = await todo_service.create(todo)

    # assert
    assert new_item == todo
    io_service.write.assert_called_once_with(
        json_utils.dumps([todo], indent=4)
    )


async def test_delete_returns_true(setup_service, setup_todos):
    # arrange
    todos, expected_todo = setup_todos()
    todo_service, io_service = setup_service
    io_service.read.return_value = json_utils.dumps(todos)

    # act
    result = await todo_service.delete(expected_todo.id)

    # assert
    assert result is True
    io_service.write.assert_called_once_with(
        json_utils.dumps(todos[1:], indent=4)
    )


async def test_delete_returns_false(setup_service):
    # arrange
    todo_service, io_service = setup_service
    io_service.read.return_value = "[]"

    # act
    result = await todo_service.delete(uuid4())

    # assert
    assert result is False
    io_service.write.assert_not_called()


async def test_put_updates_record(setup_todos, setup_service, todo_factory):
    # arrange
    todos, expected_todo = setup_todos()
    expected_updated_todo = todo_factory.create(id=expected_todo.id)
    expected_todos = [expected_updated_todo, *todos[1:]]

    todo_service, io_service = setup_service
    io_service.read.return_value = json_utils.dumps(todos)

    # act
    updated_todo = await todo_service.put(
        expected_todo.id, expected_updated_todo
    )

    # assert
    io_service.write.assert_called_once_with(
        json_utils.dumps(expected_todos, indent=4)
    )
    assert updated_todo in expected_todos


async def test_put_returns_none(setup_todos, setup_service, todo_factory):
    # arrange
    todos, expected_todo = setup_todos()
    expected_updated_todo = todo_factory.create(id=expected_todo.id)

    todo_service, io_service = setup_service
    io_service.read.return_value = json_utils.dumps(todos)

    # act
    updated_todo = await todo_service.put(uuid4(), expected_updated_todo)

    # assert
    assert updated_todo is None


async def test_get_all_by_user_id_ok(setup_service, setup_todos, todo_factory):
    # arrange
    todos, expected_todo = setup_todos()
    owner_id = expected_todo.owner_id
    second_todo = todo_factory.create(owner_id=owner_id)
    expected_todos = [second_todo, *todos]

    todos_service, io_service = setup_service
    io_service.read.return_value = json_utils.dumps(expected_todos)

    # act
    actual_todos = await todos_service.get_all_by_user_id(owner_id)

    # assert
    assert actual_todos == [second_todo, expected_todo]

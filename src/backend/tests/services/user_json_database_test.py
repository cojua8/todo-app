from typing import cast
from uuid import uuid4

import pytest
from app.models.user import User
from app.services.json_database_service.users_json_database_service import (
    UsersJsonDatabaseService,
)
from app.services.service_protocols.io_service_protocol import (
    IOServiceProtocol,
)
from app.utils import json_utils
from tests.factories.user_factory import UserFactory


@pytest.fixture
def setup(request):
    expected_values = request.param[0]
    expected_user = UserFactory(**expected_values)

    existing_users = request.param[1]

    db_users = [expected_user, *existing_users]

    yield json_utils.dumps(db_users), expected_user


@pytest.mark.parametrize(
    "setup",
    [
        ({"email": "some@email.com"}, UserFactory.create_batch(4)),
        (
            {"email": "some@email.com"},
            UserFactory.create_batch(4, email="some@email.com"),
        ),
    ],
    indirect=True,
    ids=["return_user", "return_first_match"],
)
def test_get_by_email_returns_user(mocker, setup):
    # arrange
    users, expected_user = setup
    io_service = mocker.MagicMock(spec=IOServiceProtocol)
    io_service.read.return_value = users

    service = UsersJsonDatabaseService(io_service)
    # act
    user = cast(User, service.get_by_email("some@email.com"))

    # assert
    assert user.id == expected_user.id


def test_get_by_email_returns_none(mocker):
    # arrange
    io_service = mocker.MagicMock(spec=IOServiceProtocol)
    io_service.read.return_value = json_utils.dumps(
        UserFactory.create_batch(4)
    )

    service = UsersJsonDatabaseService(io_service)
    # act
    user = cast(User, service.get_by_email("some@email.com"))

    # assert
    assert user is None


@pytest.mark.parametrize(
    "setup",
    [
        ({"username": "someusername"}, UserFactory.create_batch(4)),
        (
            {"username": "someusername"},
            UserFactory.create_batch(4, username="someusername"),
        ),
    ],
    indirect=True,
    ids=["return_user", "return_first_match"],
)
def test_get_by_username_returns_user(mocker, setup):
    # arrange
    users, expected_user = setup
    io_service = mocker.MagicMock(spec=IOServiceProtocol)
    io_service.read.return_value = users

    service = UsersJsonDatabaseService(io_service)
    # act
    user = cast(User, service.get_by_username("someusername"))

    # assert
    if user:
        assert user.id == expected_user.id


def test_get_by_username_returns_none(mocker):
    # arrange
    username = "username"
    users = UserFactory.create_batch(4)

    io_service = mocker.MagicMock(spec=IOServiceProtocol)
    io_service.read.return_value = json_utils.dumps(users)

    service = UsersJsonDatabaseService(io_service)
    # act
    actual_user = cast(User, service.get_by_username(username))

    # assert
    assert actual_user is None


@pytest.mark.parametrize(
    "setup",
    [({}, UserFactory.create_batch(4)), ({}, [])],
    indirect=True,
    ids=["return_users", "return_empty"],
)
def test_get_all_ok(mocker, setup):
    # arrange
    users, _ = setup
    expected_users = [User(**v) for v in json_utils.loads(users)]
    io_service = mocker.MagicMock(spec=IOServiceProtocol)
    io_service.read.return_value = users

    service = UsersJsonDatabaseService(io_service)
    # act
    actual_users = service.get_all()

    # assert
    assert actual_users == expected_users


@pytest.mark.parametrize(
    "setup",
    [({"id": uuid4()}, UserFactory.create_batch(4)), ({}, [])],
    indirect=True,
    ids=["return_user", "return_none"],
)
def test_get_returns_user(mocker, setup):
    # arrange
    users, expected_user = setup
    io_service = mocker.MagicMock(spec=IOServiceProtocol)
    io_service.read.return_value = users

    service = UsersJsonDatabaseService(io_service)
    # act
    actual_user = cast(User, service.get(expected_user.id))

    # assert
    if actual_user:
        assert actual_user.id == expected_user.id


def test_get_returns_none(mocker):
    # arrange
    id = uuid4()
    users = UserFactory.create_batch(4)

    io_service = mocker.MagicMock(spec=IOServiceProtocol)
    io_service.read.return_value = json_utils.dumps(users)

    service = UsersJsonDatabaseService(io_service)
    # act
    actual_user = cast(User, service.get(id))

    # assert
    assert actual_user is None


def test_create_ok(mocker):
    # arrange
    user = UserFactory.create()
    io_service = mocker.MagicMock(spec=IOServiceProtocol)
    io_service.read.return_value = "[]"

    service = UsersJsonDatabaseService(io_service)
    # act
    service.create(user)

    # assert
    io_service.write.assert_called_once_with(
        json_utils.dumps([user], indent=4)
    )


@pytest.mark.parametrize(
    "setup",
    [({}, UserFactory.create_batch(4))],
    indirect=True,
)
def test_delete_ok(mocker, setup):
    # arrange
    users, expected_user = setup
    io_service = mocker.MagicMock(spec=IOServiceProtocol)
    io_service.read.return_value = users

    service = UsersJsonDatabaseService(io_service)
    # act
    service.delete(expected_user.id)

    # assert
    io_service.write.assert_called_once_with(
        json_utils.dumps(json_utils.loads(users)[1:], indent=4)
    )


@pytest.mark.parametrize(
    "setup",
    [({}, UserFactory.create_batch(4))],
    indirect=True,
)
def test_put_ok(mocker, setup):
    # arrange
    users, expected_user = setup
    updated_user = UserFactory.create(id=expected_user.id)
    expected_users = [updated_user, *json_utils.loads(users)[1:]]

    io_service = mocker.MagicMock(spec=IOServiceProtocol)
    io_service.read.return_value = users

    service = UsersJsonDatabaseService(io_service)
    # act
    service.put(expected_user.id, updated_user)

    # assert
    io_service.write.assert_called_once_with(
        json_utils.dumps(expected_users, indent=4)
    )

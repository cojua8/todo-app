from typing import NamedTuple, cast
from uuid import uuid4

import pytest

from app.domain.models.user import User
from app.infrastructure.io_service import IOServiceProtocol
from app.infrastructure.json_database_service.users_json_database_service import (  # noqa: E501
    UsersJsonDatabaseService,
)
from app.utils import json_utils
from tests.factories.user_factory import UserFactory


class SetupParams(NamedTuple):
    expected_values: dict
    created_count: int
    existing_users_values: dict


@pytest.fixture
def setup(user_factory: UserFactory):
    default_params = SetupParams({}, 4, {})

    def _setup(params: SetupParams = default_params):
        expected_user = user_factory.create(**params.expected_values)

        existing_users = user_factory.create_batch(
            params.created_count, **params.existing_users_values
        )

        db_users = [expected_user, *existing_users]

        return json_utils.dumps(db_users), expected_user

    return _setup


@pytest.mark.parametrize(
    "params",
    [
        SetupParams({"email": "some@email.com"}, 4, {}),
        SetupParams(
            {"email": "some@email.com"}, 4, {"email": "some@email.com"}
        ),
    ],
    ids=["return_user", "return_first_match"],
)
async def test_get_by_email_returns_user(mocker, params, setup):
    # arrange
    users, expected_user = setup(params)
    io_service = mocker.Mock(spec=IOServiceProtocol)
    io_service.read.return_value = users

    service = UsersJsonDatabaseService(io_service)
    # act
    user = cast(User, await service.get_by_email("some@email.com"))

    # assert
    assert user.id == expected_user.id


async def test_get_by_email_returns_none(mocker, user_factory: UserFactory):
    # arrange
    io_service = mocker.Mock(spec=IOServiceProtocol)
    io_service.read.return_value = json_utils.dumps(
        user_factory.create_batch(4)
    )

    service = UsersJsonDatabaseService(io_service)
    # act
    user = cast(User, await service.get_by_email("some@email.com"))

    # assert
    assert user is None


@pytest.mark.parametrize(
    "params",
    [
        SetupParams({"username": "someusername"}, 4, {}),
        SetupParams(
            {"username": "someusername"}, 4, {"username": "someusername"}
        ),
    ],
    ids=["return_user", "return_first_match"],
)
async def test_get_by_username_returns_user(mocker, params, setup):
    # arrange
    users, expected_user = setup(params)
    io_service = mocker.Mock(spec=IOServiceProtocol)
    io_service.read.return_value = users

    service = UsersJsonDatabaseService(io_service)
    # act
    user = cast(User, await service.get_by_username("someusername"))

    # assert
    if user:
        assert user.id == expected_user.id


async def test_get_by_username_returns_none(mocker, user_factory: UserFactory):
    # arrange
    username = "username"
    users = user_factory.create_batch(4)

    io_service = mocker.Mock(spec=IOServiceProtocol)
    io_service.read.return_value = json_utils.dumps(users)

    service = UsersJsonDatabaseService(io_service)
    # act
    actual_user = cast(User, await service.get_by_username(username))

    # assert
    assert actual_user is None


@pytest.mark.parametrize(
    "params",
    [SetupParams({}, 4, {}), SetupParams({}, 0, {})],
    ids=["return_users", "return_empty"],
)
async def test_get_all_ok(mocker, params, setup):
    # arrange
    users, _ = setup(params)
    expected_users = [User(**v) for v in json_utils.loads(users)]
    io_service = mocker.Mock(spec=IOServiceProtocol)
    io_service.read.return_value = users

    service = UsersJsonDatabaseService(io_service)
    # act
    actual_users = await service.get_all()

    # assert
    assert actual_users == expected_users


async def test_get_returns_user(mocker, setup):
    # arrange
    users, expected_user = setup(SetupParams({"id": uuid4()}, 4, {}))
    io_service = mocker.Mock(spec=IOServiceProtocol)
    io_service.read.return_value = users

    service = UsersJsonDatabaseService(io_service)
    # act
    actual_user = cast(User, await service.get(expected_user.id))

    # assert
    assert actual_user.id == expected_user.id


async def test_get_returns_none(mocker, user_factory: UserFactory):
    # arrange
    id_ = uuid4()
    users = user_factory.create_batch(4)

    io_service = mocker.Mock(spec=IOServiceProtocol)
    io_service.read.return_value = json_utils.dumps(users)

    service = UsersJsonDatabaseService(io_service)
    # act
    actual_user = cast(User, await service.get(id_))

    # assert
    assert actual_user is None


async def test_create_ok(mocker, user_factory: UserFactory):
    # arrange
    user = user_factory.create()
    io_service = mocker.Mock(spec=IOServiceProtocol)
    io_service.read.return_value = "[]"

    service = UsersJsonDatabaseService(io_service)
    # act
    created_user = await service.create(user)

    # assert
    io_service.write.assert_called_once_with(
        json_utils.dumps([user], indent=4)
    )
    assert user == created_user


async def test_delete_returns_true(mocker, setup):
    # arrange
    users, expected_user = setup()
    io_service = mocker.Mock(spec=IOServiceProtocol)
    io_service.read.return_value = users

    service = UsersJsonDatabaseService(io_service)
    # act
    result = await service.delete(expected_user.id)

    # assert
    assert result is True
    io_service.write.assert_called_once_with(
        json_utils.dumps(json_utils.loads(users)[1:], indent=4)
    )


async def test_delete_returns_false(mocker, setup):
    # arrange
    users, _ = setup()
    io_service = mocker.Mock(spec=IOServiceProtocol)
    io_service.read.return_value = users

    service = UsersJsonDatabaseService(io_service)
    # act
    result = await service.delete(uuid4())

    # assert
    assert result is False


async def test_put_updates_existing_record(
    mocker, setup, user_factory: UserFactory
):
    # arrange
    users, expected_user = setup()
    updated_user = user_factory.create(id=expected_user.id)
    expected_users = [updated_user, *json_utils.loads(users)[1:]]

    io_service = mocker.Mock(spec=IOServiceProtocol)
    io_service.read.return_value = users

    service = UsersJsonDatabaseService(io_service)
    # act
    await service.put(expected_user.id, updated_user)

    # assert
    io_service.write.assert_called_once_with(
        json_utils.dumps(expected_users, indent=4)
    )


async def test_put_returns_none(mocker, setup, user_factory: UserFactory):
    # arrange
    users, expected_user = setup()
    expected_updated_user = user_factory.create(id=expected_user.id)

    io_service = mocker.Mock(spec=IOServiceProtocol)
    io_service.read.return_value = users

    service = UsersJsonDatabaseService(io_service)
    # act
    updated_user = await service.put(uuid4(), expected_updated_user)

    # assert
    assert updated_user is None

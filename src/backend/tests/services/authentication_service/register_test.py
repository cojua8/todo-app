from typing import TYPE_CHECKING

import pytest

from app.services.authentication_service import AuthenticationService
from app.services.service_protocols.authentication_service_protocol import (  # noqa: E501
    RegistrationResult,
)
from app.services.service_protocols.user_service_protocol import (
    UserServiceProtocol,
)

if TYPE_CHECKING:
    from app.models.user import User


@pytest.mark.asyncio()
async def test_passwords_not_matching(faker, mocker):
    # arrange
    mock_user_service = mocker.MagicMock(spec=UserServiceProtocol)
    auth_service = AuthenticationService(mock_user_service)

    username = faker.user_name()
    email = faker.email()
    password = "password"  # noqa: S105
    confirm_password = "other_password"  # noqa: S105

    # act
    result = await auth_service.register(username, email, password, confirm_password)

    # assert
    assert result == RegistrationResult.PASSWORD_NOT_MATCHING


@pytest.mark.asyncio()
async def test_username_already_exists(user_factory, mocker):
    # arrange
    mock_user: User = user_factory()

    mock_user_service = mocker.MagicMock(spec=UserServiceProtocol)
    mock_user_service.get_by_username = mocker.AsyncMock(return_value=mock_user)

    auth_service = AuthenticationService(mock_user_service)

    # act
    result = await auth_service.register(
        mock_user.username,
        mock_user.email,
        mock_user.password,
        mock_user.password,
    )

    # assert
    assert result == RegistrationResult.USERNAME_ALREADY_EXISTS


@pytest.mark.asyncio()
async def test_email_already_exists(mocker, user_factory):
    # arrange
    mock_user: User = user_factory()

    mock_user_service = mocker.MagicMock(spec=UserServiceProtocol)
    mock_user_service.get_by_username = mocker.AsyncMock(return_value=None)
    mock_user_service.get_by_email = mocker.AsyncMock(return_value=mock_user)

    auth_service = AuthenticationService(mock_user_service)

    # act
    result = await auth_service.register(
        mock_user.username,
        mock_user.email,
        mock_user.password,
        mock_user.password,
    )

    # assert
    assert result == RegistrationResult.EMAIL_ALREADY_EXISTS


@pytest.mark.asyncio()
async def test_success_creates_user(mocker, user_factory):
    # arrange
    user: User = user_factory()

    mock_user_service = mocker.MagicMock(spec=UserServiceProtocol)
    mock_user_service.get_by_username = mocker.AsyncMock(return_value=None)
    mock_user_service.get_by_email = mocker.AsyncMock(return_value=None)

    auth_service = AuthenticationService(mock_user_service)

    # act
    result = await auth_service.register(
        user.username, user.email, user.password, user.password
    )

    # assert
    assert result == RegistrationResult.SUCCESS

    mock_user_service.create.assert_called_once()

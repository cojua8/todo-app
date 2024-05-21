import pytest

from app.domain.services.user_service_protocol import UserServiceProtocol
from app.exceptions.login_exception import LoginError
from app.services.authentication_service import AuthenticationService


async def test_inexistent_user_raises_login_exception(mocker, faker):
    # arrange
    login_username = faker.user_name()
    login_password = faker.password()

    mock_user_service = mocker.MagicMock(spec=UserServiceProtocol)
    mock_user_service.get_by_username = mocker.AsyncMock(return_value=None)

    auth_service = AuthenticationService(mock_user_service)

    # act
    # assert
    with pytest.raises(LoginError) as exc_info:
        await auth_service.login(login_username, login_password)

    assert str(exc_info.value) == "Login error wrong user or password."


async def test_wrong_password_raises_login_exception(
    mocker, faker, user_factory
):
    # arrange
    login_username = faker.user_name()
    login_password = "a_password"  # noqa: S105

    user = user_factory(password="another_password")  # noqa: S106

    mock_user_service = mocker.MagicMock(spec=UserServiceProtocol)
    mock_user_service.get_by_username = mocker.AsyncMock(return_value=user)

    auth_service = AuthenticationService(mock_user_service)

    # act
    # assert
    with pytest.raises(LoginError):
        await auth_service.login(login_username, login_password)


async def test_login_user_ok(mocker, faker, user_factory):
    # arrange
    login_username = faker.user_name()
    login_password = "a_password"  # noqa: S105

    expected_user = user_factory(password=login_password)

    mock_user_service = mocker.MagicMock(spec=UserServiceProtocol)
    mock_user_service.get_by_username = mocker.AsyncMock(
        return_value=expected_user
    )

    auth_service = AuthenticationService(mock_user_service)

    # act
    actual_user = await auth_service.login(login_username, login_password)

    # assert
    assert actual_user == expected_user

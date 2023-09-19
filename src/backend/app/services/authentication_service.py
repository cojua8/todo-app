from __future__ import annotations

from typing import TYPE_CHECKING

from app.exceptions.login_exception import LoginError
from app.models.user import User
from app.services.service_protocols.authentication_service_protocol import (
    AuthenticationServiceProtocol,
    RegistrationResult,
)

if TYPE_CHECKING:
    from app.services.service_protocols.user_service_protocol import (
        UserServiceProtocol,
    )


class AuthenticationService(AuthenticationServiceProtocol):
    def __init__(self, user_service: UserServiceProtocol) -> None:
        self.user_service = user_service

    async def register(
        self, username: str, email: str, password: str, confirm_password: str
    ) -> RegistrationResult:
        result = RegistrationResult.SUCCESS

        if password != confirm_password:
            result = RegistrationResult.PASSWORD_NOT_MATCHING
        elif await self.user_service.get_by_username(username):
            result = RegistrationResult.USERNAME_ALREADY_EXISTS
        elif await self.user_service.get_by_email(email):
            result = RegistrationResult.EMAIL_ALREADY_EXISTS

        if result == RegistrationResult.SUCCESS:
            new = User(username=username, email=email, password=password)
            await self.user_service.create(new)

        return result

    async def login(self, username: str, password: str) -> User:
        user = await self.user_service.get_by_username(username)

        if not user or password != user.password:
            raise LoginError

        return user

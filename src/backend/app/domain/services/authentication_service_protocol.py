from enum import StrEnum, auto
from typing import Protocol

from app.domain.models.user import User


class RegistrationResult(StrEnum):
    SUCCESS = auto()
    PASSWORD_NOT_MATCHING = auto()
    USERNAME_ALREADY_EXISTS = auto()
    EMAIL_ALREADY_EXISTS = auto()


class AuthenticationServiceProtocol(Protocol):
    async def register(
        self, username: str, email: str, password: str, confirm_password: str
    ) -> tuple[RegistrationResult, User | None]: ...

    async def login(self, username: str, password: str) -> User: ...

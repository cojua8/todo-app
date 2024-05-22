from http import HTTPStatus

from fastapi import HTTPException


class LoginError(HTTPException):
    def __init__(self) -> None:
        super().__init__(HTTPStatus.BAD_REQUEST)

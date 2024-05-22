from http import HTTPStatus

from fastapi import HTTPException


class UserNotFoundError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=HTTPStatus.NOT_FOUND)

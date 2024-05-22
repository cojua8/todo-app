from http import HTTPStatus

from fastapi import HTTPException


class TodoNotFoundError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=HTTPStatus.NOT_FOUND)

from pydantic import BaseModel


class UserNotFoundError(BaseModel):
    detail: str = "User not found."

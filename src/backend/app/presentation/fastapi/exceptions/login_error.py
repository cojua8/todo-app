from pydantic import BaseModel


class LoginError(BaseModel):
    detail: str = "Login error wrong user or password."

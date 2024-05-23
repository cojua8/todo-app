from pydantic import EmailStr

from app.domain.models.base_model import BaseModel


class User(BaseModel):
    username: str
    email: EmailStr
    password: str

from pydantic import BaseModel, EmailStr


class UserCreateData(BaseModel):
    username: str
    password: str
    email: EmailStr

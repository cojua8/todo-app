from pydantic import BaseModel, EmailStr


class UserCreateData(BaseModel):
    username: str
    email: EmailStr
    password: str

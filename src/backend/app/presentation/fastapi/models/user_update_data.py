from pydantic import BaseModel, EmailStr


class UserUpdateData(BaseModel):
    username: str
    email: EmailStr
    password: str

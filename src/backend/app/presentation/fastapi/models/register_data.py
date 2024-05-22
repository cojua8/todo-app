from pydantic import BaseModel, EmailStr, Field


class RegisterData(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str = Field(..., validation_alias="confirmPassword")

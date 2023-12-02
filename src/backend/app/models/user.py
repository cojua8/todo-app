from app.models.base_model import BaseModel


class User(BaseModel):
    username: str
    email: str
    password: str

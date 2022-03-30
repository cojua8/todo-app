from dataclasses import dataclass


from app.models.base_model import BaseModel


@dataclass(kw_only=True)
class User(BaseModel):
    name: str
    email: str

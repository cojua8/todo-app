from uuid import UUID

from pydantic import BaseModel, Field


class User(BaseModel):
    id_: UUID = Field(..., serialization_alias="id", validation_alias="id")
    username: str
    email: str

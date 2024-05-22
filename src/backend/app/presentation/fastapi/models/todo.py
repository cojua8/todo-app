import datetime as dt
from uuid import UUID

from pydantic import BaseModel, Field


class Todo(BaseModel):
    id_: UUID = Field(..., alias="id")
    owner_id: UUID = Field(..., serialization_alias="ownerId")
    description: str
    due_date: dt.date = Field(..., serialization_alias="dueDate")
    completed: bool
    date_created: dt.date = Field(..., serialization_alias="dateCreated")

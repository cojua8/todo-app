import datetime as dt
from uuid import UUID

from pydantic import BaseModel, Field


class Todo(BaseModel):
    id_: UUID = Field(..., validation_alias="id", serialization_alias="id")
    owner_id: UUID
    description: str
    due_date: dt.date
    completed: bool
    date_created: dt.date

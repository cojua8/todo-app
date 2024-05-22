import datetime as dt
from uuid import UUID

from pydantic import BaseModel, Field


class TodoUpdateData(BaseModel):
    owner_id: UUID = Field(..., validation_alias="ownerId")
    description: str
    date_created: dt.date = Field(..., validation_alias="dateCreated")
    due_date: dt.date = Field(..., validation_alias="dueDate")
    completed: bool

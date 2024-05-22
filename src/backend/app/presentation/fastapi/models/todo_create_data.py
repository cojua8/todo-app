import datetime as dt
from uuid import UUID

from pydantic import Field

from app.domain.models.base_model import BaseModel


class TodoCreateData(BaseModel):
    owner_id: UUID = Field(..., validation_alias="ownerId")
    description: str
    due_date: dt.date = Field(..., validation_alias="dueDate")

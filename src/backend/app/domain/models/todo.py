import datetime as dt
from uuid import UUID

from pydantic import Field

from app.domain.models.base_model import BaseModel


class Todo(BaseModel):
    owner_id: UUID
    description: str
    due_date: dt.date
    completed: bool = Field(default=False)
    date_created: dt.date = Field(
        default_factory=lambda: dt.datetime.now(tz=dt.UTC).date()
    )

import datetime as dt
from dataclasses import dataclass, field
from uuid import UUID

from app.models.base_model import BaseModel


@dataclass(kw_only=True)
class Todo(BaseModel):
    owner_id: UUID
    description: str
    due_date: dt.date
    completed: bool = field(default=False)
    date_created: dt.date = field(
        default_factory=lambda: dt.datetime.now(tz=dt.UTC).date()
    )

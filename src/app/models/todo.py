from dataclasses import dataclass, field
from datetime import date
from uuid import UUID

from app.models.base_model import BaseModel


@dataclass(kw_only=True)
class Todo(BaseModel):
    owner_id: UUID
    description: str
    due_date: date
    completed: bool = field(default=False)
    date_created: date = field(default_factory=date.today)

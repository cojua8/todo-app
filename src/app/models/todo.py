from dataclasses import dataclass, field
from datetime import date
from app.models.base_model import BaseModel
from uuid import UUID


@dataclass(kw_only=True)
class Todo(BaseModel):
    owner_id: UUID
    description: str
    due_date: date
    completed: bool = field(default=False)
    date_created: date = field(default_factory=lambda: date.today())

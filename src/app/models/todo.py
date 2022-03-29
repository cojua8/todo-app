from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4


@dataclass
class Todo:
    owner_id: UUID
    description: str
    date_created: date
    due_date: date
    completed: bool
    id: UUID = field(default_factory=uuid4)

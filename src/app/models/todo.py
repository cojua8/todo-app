from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4


@dataclass
class Todo:
    owner_id: UUID
    description: str
    due_date: date
    completed: bool = field(default=False)
    date_created: date = field(default_factory=date.today)
    id: UUID = field(default_factory=uuid4)

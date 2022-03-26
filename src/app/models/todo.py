from dataclasses import dataclass
from datetime import date


@dataclass
class Todo:
    id: int
    owner_id: int
    description: str
    date_created: date
    due_date: date
    completed: bool

from dataclasses import dataclass, field
from uuid import UUID, uuid4

from app.models.base_model import BaseModel


@dataclass
class User(BaseModel):
    name: str
    email: str
    id: UUID = field(default_factory=uuid4)

from uuid import UUID

from pydantic import BaseModel


class TodosQuery(BaseModel):
    user_id: UUID

from uuid import UUID

from pydantic import BaseModel


class PathId(BaseModel):
    id: UUID

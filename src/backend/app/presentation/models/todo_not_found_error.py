from pydantic import BaseModel


class TodoNotFoundError(BaseModel):
    detail: str = "Todo not found"

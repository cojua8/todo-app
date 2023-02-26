from typing import TYPE_CHECKING

from sqlalchemy import select

from app.models.user import User
from app.services.service_protocols.user_service_protocol import (
    UserServiceProtocol,
)
from app.services.sql_database_service.base_service import BaseService
from app.services.sql_database_service.models import user_table

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine


class UsersService(BaseService[User], UserServiceProtocol):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, user_table, User)

    def get_by_email(self, email: str) -> User | None:
        with self._engine.connect() as conn:
            rows = conn.execute(
                select(self._table)
                .where(self._table.c.email == email)
                .limit(1)
            )
        if entity := next(rows, None):
            return self._mappers.entity_to_model(entity, self._model)

    def get_by_username(self, username: str) -> User | None:
        with self._engine.connect() as conn:
            rows = conn.execute(
                select(self._table)
                .where(self._table.c.username == username)
                .limit(1)
            )
        if entity := next(rows, None):
            return self._mappers.entity_to_model(entity, self._model)

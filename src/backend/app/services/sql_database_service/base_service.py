from abc import ABC
from collections import namedtuple
from typing import Generic, Iterable, Type
from uuid import UUID

from app.models.base_model import BaseModel
from app.services.service_protocols.database_service_protocol import (
    BMT,
    DatabaseServiceProtocol,
)
from sqlalchemy import Row, Table, delete, insert, select, update
from sqlalchemy.engine import Engine

Mapper = namedtuple("Mapper", ["model_to_entity", "entity_to_model"])


class Mappers:
    def model_to_entity(self, model: BaseModel) -> dict:
        return model.__dict__

    def entity_to_model(self, entity: Row, model_type: Type[BMT]) -> BMT:
        return model_type(**entity._asdict())


class BaseService(DatabaseServiceProtocol[BMT], Generic[BMT], ABC):
    def __init__(self, engine: Engine, table: Table, model: Type[BMT]) -> None:
        self._engine = engine
        self._table = table
        self._model = model
        self._mappers = Mappers()

    def get_all(self) -> Iterable[BMT]:
        with self._engine.connect() as conn:
            results = conn.execute(select(self._table))
        return [
            self._mappers.entity_to_model(result, self._model)
            for result in results
        ]

    def get(self, id: UUID) -> BMT | None:
        with self._engine.connect() as conn:
            bmt = conn.execute(
                select(self._table).where(self._table.c.id == id).limit(1)
            )

        if bmt := next(bmt, None):
            return self._mappers.entity_to_model(bmt, self._model)

    def create(self, new: BMT) -> None:
        entity = self._mappers.model_to_entity(new)
        with self._engine.connect() as conn:
            conn.execute(insert(self._table).values(**entity))
            conn.commit()

    def delete(self, id: UUID) -> None:
        with self._engine.connect() as conn:
            conn.execute(delete(self._table).where(self._table.c.id == id))
            conn.commit()

    def put(self, id: UUID, new: BMT) -> None:
        entity = self._mappers.model_to_entity(new)
        with self._engine.connect() as conn:
            conn.execute(
                update(self._table)
                .where(self._table.c.id == id)
                .values(**entity)
            )
            conn.commit()

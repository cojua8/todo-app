from abc import ABC
from typing import Generic, cast
from uuid import UUID

from sqlalchemy import Row, Table, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncEngine

from app.domain.models.base_model import BaseModel
from app.domain.services.database_service_protocol import (
    BMT,
    DatabaseServiceProtocol,
)


class Mappers:
    def model_to_entity(self, model: BaseModel) -> dict:
        return model.model_dump()

    def entity_to_model(self, entity: Row, model_type: type[BMT]) -> BMT:
        return model_type.model_validate(entity, from_attributes=True)


class BaseService(DatabaseServiceProtocol[BMT], Generic[BMT], ABC):
    def __init__(
        self, engine: AsyncEngine, table: Table, model: type[BMT]
    ) -> None:
        self._engine = engine
        self._table = table
        self._model = model
        self._mappers = Mappers()

    async def get_all(self) -> list[BMT]:
        async with self._engine.connect() as conn:
            results = await conn.execute(select(self._table))
            await conn.commit()
        return [
            self._mappers.entity_to_model(result, self._model)
            for result in results
        ]

    async def get(self, id_: UUID) -> BMT | None:
        async with self._engine.connect() as conn:
            result = await conn.execute(
                select(self._table)
                .where(self._table.columns.id == id_)
                .limit(1)
            )

        if entity := result.fetchone():
            return self._mappers.entity_to_model(entity, self._model)

    async def create(self, new: BMT) -> BMT:
        entity = self._mappers.model_to_entity(new)
        async with self._engine.connect() as conn:
            stmt = (
                insert(self._table)
                .values(**entity)
                .returning(*self._table.columns)
            )
            result = await conn.execute(stmt)
            await conn.commit()

        return self._mappers.entity_to_model(
            cast(Row, result.fetchone()), self._model
        )

    async def delete(self, id_: UUID) -> bool:
        async with self._engine.connect() as conn:
            result = await conn.execute(
                delete(self._table).where(self._table.columns.id == id_)
            )
            await conn.commit()

        return result.rowcount > 0

    async def put(self, id_: UUID, new: BMT) -> BMT | None:
        entity = self._mappers.model_to_entity(new)
        async with self._engine.connect() as conn:
            stmt = (
                update(self._table)
                .where(self._table.columns.id == id_)
                .values(**entity)
                .returning(*self._table.columns)
            )
            result = await conn.execute(stmt)
            await conn.commit()

        if updated_entity := result.fetchone():
            return self._mappers.entity_to_model(updated_entity, self._model)

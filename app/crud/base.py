from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import delete, func, insert, update

M = TypeVar("M")
S = TypeVar("S")


class CrudBase(Generic[M, S]):
    """
    Base CRUD class with common operations for database models.
    """

    def __init__(self, model: M, schema: S):
        """
        Initialize with model and schema.
        """
        self.model = model
        self.schema = schema

    async def execute_get_one(self, session: AsyncSession, stmt) -> M:
        """
        Execute a statement and return a single result or None.
        """
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_paginated(
        self, session: AsyncSession, page: int = 1, page_size: int = 2
    ) -> list[S]:
        """
        Retrieve a paginated list of objects.
        """
        offset = (page - 1) * page_size
        result = await session.execute(
            select(self.model).offset(offset).limit(page_size)
        )
        objs = result.scalars().all()
        return [self.schema.model_validate(obj) for obj in objs]

    async def get_count(self, session: AsyncSession) -> int:
        """
        Get the total count of records in the model.
        """
        result = await session.execute(select(func.count()).select_from(self.model))
        return result.scalar_one()

    async def get_by_id(self, session: AsyncSession, id: int) -> S | None:
        """
        Retrieve a record by its ID.
        """
        result = await session.execute(select(self.model).where(self.model.id == id))
        obj = result.scalar_one_or_none()
        return self.schema.model_validate(obj) if obj else None

    async def create(self, session: AsyncSession, create_obj: S) -> S | None:
        """
        Create a new record and return it.
        """
        stmt = insert(self.model).values(create_obj.model_dump()).returning(self.model)
        result = await self.execute_get_one(session, stmt)
        return self.schema.model_validate(result) if result else None

    async def delete(self, session: AsyncSession, id: int) -> S | None:
        """
        Delete a record by its ID and return it.
        """
        stmt = delete(self.model).where(self.model.id == id).returning(self.model)
        result = await self.execute_get_one(session, stmt)
        return self.schema.model_validate(result) if result else None

    async def update(self, session: AsyncSession, id: int, update_obj: S) -> S | None:
        """
        Update a record by its ID and return it.
        """
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(update_obj.model_dump(exclude_none=True))
            .returning(self.model)
        )
        result = await self.execute_get_one(session, stmt)
        return self.schema.model_validate(result) if result else None

    async def batch_create(self, session: AsyncSession, create_objs: list[S]):
        """
        Create multiple records in a batch.
        """
        create_dicts = [obj.model_dump() for obj in create_objs]
        stmt = insert(self.model).values(create_dicts)
        await session.execute(stmt)
        return None

    async def batch_delete(self, session: AsyncSession, ids: list[int]):
        """
        Delete multiple records by their IDs.
        """
        stmt = delete(self.model).where(self.model.id.in_(ids)).returning(True)
        result = await session.execute(stmt)
        return result.scalars().all() if result else None

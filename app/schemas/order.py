from datetime import datetime

from pydantic import Field

from .base import BaseSchema


class OrderSchemaCreate(BaseSchema):
    product_ids: list[int] = Field(...)
    amounts: list[int] = Field(...)


class OrderSchema(OrderSchemaCreate):
    id: int = Field(..., gt=0)
    created_at: datetime = Field(...)


class OrderReturnSchema(BaseSchema):
    id: int = Field(..., gt=0)
    created_at: datetime = Field(...)

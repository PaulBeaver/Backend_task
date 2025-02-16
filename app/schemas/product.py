from datetime import datetime

from pydantic import Field

from .base import BaseSchema


class ProductSchemaCreate(BaseSchema):
    product_name: str | None = Field(None, max_length=100)
    price: float | None = Field(None, ge=0)
    cost: float | None = Field(None, ge=0)
    stock: int | None = Field(None, ge=0)


class ProductSchema(ProductSchemaCreate):
    id: int = Field(..., gt=0)
    created_at: datetime | None = Field(None)



# field(default = None)

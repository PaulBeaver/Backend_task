from datetime import datetime

from pydantic import Field

from .base import BaseSchema


class ProductSchemaCreate(BaseSchema):
    """
    Schema for creating a product.

    Attributes:
        product_name (str | None): Name of the product. Optional, max length is 100 characters.
        price (float | None): Price of the product. Optional, must be greater than or equal to 0.
        cost (float | None): Cost of the product. Optional, must be greater than or equal to 0.
        stock (int | None): Stock quantity of the product. Optional, must be greater than or equal to 0.
    """

    product_name: str | None = Field(default=None, max_length=100)
    price: float | None = Field(default=None, ge=0)
    cost: float | None = Field(default=None, ge=0)
    stock: int | None = Field(default=None, ge=0)


class ProductSchema(ProductSchemaCreate):
    """
    Schema representing a product with additional fields.

    Extends:
        ProductSchemaCreate

    Attributes:
        id (int): Unique identifier for the product. Must be greater than 0.
        created_at (datetime | None): Timestamp when the product was created. Optional.
    """

    id: int = Field(..., gt=0)
    created_at: datetime | None = Field(default=None)

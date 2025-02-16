from datetime import datetime

from pydantic import Field

from .base import BaseSchema


class OrderProductsSchemaCreate(BaseSchema):
    """
    Schema for creating an order-product association.

    Attributes:
        order_id (int | None): ID of the order. Optional, must be greater than or equal to 0.
        product_id (int | None): ID of the product. Optional, must be greater than or equal to 0.
        amount (int | None): Quantity of the product in the order. Optional, must be greater than or equal to 0.
    """

    order_id: int | None = Field(default=None, ge=0)
    product_id: int | None = Field(default=None, ge=0)
    amount: int | None = Field(default=None, ge=0)


class OrderProductsSchema(OrderProductsSchemaCreate):
    """
    Schema representing an order-product relationship with additional fields.

    Extends:
        OrderProductsSchemaCreate

    Attributes:
        id (int): Unique identifier for the order-product relationship. Must be greater than 0.
        created_at (datetime | None): Timestamp when the record was created. Optional.
    """

    id: int = Field(..., gt=0)
    created_at: datetime | None = Field(default=None)

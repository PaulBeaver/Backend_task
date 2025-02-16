from datetime import datetime

from pydantic import Field

from .base import BaseSchema


class OrderSchemaCreate(BaseSchema):
    """
    Schema for creating a new order.

    Attributes:
        product_ids (list[int]): List of product IDs associated with the order.
        amounts (list[int]): List of quantities for each product in the order.
    """

    product_ids: list[int] = Field(...)
    amounts: list[int] = Field(...)


class OrderSchema(OrderSchemaCreate):
    """
    Schema representing an order with additional fields.

    Extends:
        OrderSchemaCreate

    Attributes:
        id (int): Unique identifier of the order (greater than 0).
        created_at (datetime): Timestamp when the order was created.
    """

    id: int = Field(..., gt=0)
    created_at: datetime = Field(...)


class OrderReturnSchema(BaseSchema):
    """
    Schema for returning basic order information.

    Attributes:
        id (int): Unique identifier of the order (greater than 0).
        created_at (datetime): Timestamp when the order was created.
    """

    id: int = Field(..., gt=0)
    created_at: datetime = Field(...)

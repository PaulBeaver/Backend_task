import datetime

from sqlalchemy import BigInteger, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Order(Base):
    """
    Represents the 'orders' table in the database.

    Attributes:
        id (int): The unique identifier for the order.
        created_at (datetime): Timestamp indicating when the order was created.
        orders_products: Relationship to the OrdersProducts table (one-to-many).
    """

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    orders_products = relationship("OrdersProducts", back_populates="orders")

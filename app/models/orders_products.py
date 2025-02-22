from sqlalchemy import (
    TIMESTAMP,
    BigInteger,
    ForeignKey,
    Index,
    Integer,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class OrdersProducts(Base):
    """
    Represents the 'orders_products' table in the database.
    This is a junction table for the many-to-many relationship between orders and products.

    Attributes:
        id (int): Unique identifier for the record.
        created_at (datetime): Timestamp indicating when the record was created.
        order_id (int): Foreign key referencing the 'orders' table.
        product_id (int): Foreign key referencing the 'products' table.
        amount (int): Quantity of the product in the order.

    Relationships:
        orders: Relationship to the 'Order' model.
        products: Relationship to the 'Product' model.
    """

    __tablename__ = "orders_products"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    created_at: Mapped[TIMESTAMP | None] = mapped_column(
        TIMESTAMP, nullable=True, default=func.now()
    )
    order_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("orders.id"), nullable=False
    )
    product_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("products.id"), nullable=False
    )
    amount: Mapped[int | None] = mapped_column(Integer, nullable=True)

    orders = relationship("Order", back_populates="orders_products")
    products = relationship("Product", back_populates="orders_products")

    # Table constraints and indexes for performance and uniqueness
    __table_args__ = (
        UniqueConstraint(
            "order_id", "product_id", name="uq_order_product"
        ),  # Ensures unique product per order
        Index("idx_order_id", "order_id"),  # Index for faster lookups by order_id
        Index("idx_product_id", "product_id"),  # Index for faster lookups by product_id
    )

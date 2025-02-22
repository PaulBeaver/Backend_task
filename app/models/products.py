from sqlalchemy import DECIMAL, TIMESTAMP, BigInteger, Index, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Product(Base):
    """
    Represents the 'products' table in the database.

    Attributes:
        id (int): Unique identifier for the product.
        created_at (datetime): Timestamp indicating when the product record was created.
        product_name (str): Name of the product.
        price (Decimal): Selling price of the product.
        cost (Decimal): Cost price of the product.
        stock (int): Quantity available in stock.

    Relationships:
        orders_products: Links to the 'OrdersProducts' model for order-product association.
    """

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    created_at: Mapped[TIMESTAMP | None] = mapped_column(
        TIMESTAMP, nullable=True, default=func.now()
    )
    product_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    price: Mapped[float | None] = mapped_column(DECIMAL(15, 2), nullable=True)
    cost: Mapped[float | None] = mapped_column(DECIMAL(15, 2), nullable=True)
    stock: Mapped[int | None] = mapped_column(Integer, nullable=True)

    orders_products = relationship("OrdersProducts", back_populates="products")

    # Optional: Index for product_name column to speed up search queries
    __table_args__ = (Index("idx_product_name", "product_name"),)

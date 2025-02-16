from sqlalchemy import TIMESTAMP, BigInteger, ForeignKey, Integer, func, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class OrdersProducts(Base):
    __tablename__ = "orders_products"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    created_at: Mapped[TIMESTAMP | None] = mapped_column(TIMESTAMP, nullable=True, default=func.now())
    order_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("products.id"), nullable=False)
    amount: Mapped[int | None] = mapped_column(Integer, nullable=True)

    orders = relationship("Order", back_populates="orders_products")
    products = relationship("Product", back_populates="orders_products")

    # __rw_fields__ =(...)
    __table_args__ = (
        UniqueConstraint("order_id", "product_id", name="uq_order_product"),
        Index("idx_order_id", "order_id"),
        Index("idx_product_id", "product_id"),
    )
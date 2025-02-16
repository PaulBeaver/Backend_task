from datetime import datetime

from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CrudBase, S
from app.models import Order, OrdersProducts, Product
from app.schemas.order import OrderReturnSchema


class CrudOrder(CrudBase):
    """
    CRUD operations specific to Order entity.
    """

    async def get_by_id(self, session: AsyncSession, id: int) -> S | None:
        """
        Retrieves an order by its ID along with the associated products.

        Args:
            session: The async database session.
            id: The ID of the order.

        Returns:
            A dictionary containing order details and associated products, or an empty dictionary if not found.
        """
        query = (
            select(
                Order.id.label("order_id"),
                Order.created_at.label("order_created_at"),
                func.json_agg(
                    func.jsonb_build_object(
                        "product_id",
                        Product.id,
                        "product_name",
                        Product.product_name,
                        "amount",
                        OrdersProducts.amount,
                        "price",
                        Product.price,
                        "cost",
                        Product.cost,
                    )
                ).label("products"),
            )
            .join(OrdersProducts, Order.id == OrdersProducts.order_id)
            .join(Product, OrdersProducts.product_id == Product.id)
            .filter(Order.id == id)
            .group_by(Order.id, Order.created_at)
        )

        result = await session.execute(query)
        return result.mappings().first() if result else {}

    async def create_order(self, session: AsyncSession, create_obj) -> int:
        """
        Creates an order and associated order products in the database.

        Args:
            session: The async database session.
            create_obj: Object containing product_ids and amounts for creating an order.

        Returns:
            The ID of the newly created order.

        Raises:
            ValueError: If the lengths of product_ids and amounts do not match.
        """
        if len(create_obj.product_ids) != len(create_obj.amounts):
            raise ValueError("The lengths of product_ids and amounts must match.")

        call_function_stmt = text(
            """
            SELECT create_order_with_products(
                :product_ids, 
                :amounts, 
                :order_created_at
            ) AS order_id;
            """
        )

        result = await session.execute(
            call_function_stmt,
            {
                "product_ids": create_obj.product_ids,
                "amounts": create_obj.amounts,
                "order_created_at": datetime.now(),
            },
        )

        order_id = result.scalar()
        return order_id


# Instance of CrudOrder to interact with the Order entity using its schema
order_crud: CrudOrder = CrudOrder(Order, OrderReturnSchema)

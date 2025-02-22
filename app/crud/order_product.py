from app.crud.base import CrudBase
from app.models.orders_products import OrdersProducts
from app.schemas.order_product import OrderProductsSchema


class CrudOrderProduct(CrudBase):
    """
    CRUD operations for the OrdersProducts entity.

    This class currently inherits base CRUD functionality from CrudBase
    without adding any custom methods.
    """

    pass


# Instance of CrudOrderProduct to interact with the OrdersProducts entity using its schema
orders_products_crud: CrudOrderProduct = CrudOrderProduct(
    OrdersProducts, OrderProductsSchema
)

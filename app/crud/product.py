from app.crud.base import CrudBase
from app.models import Product
from app.schemas.product import ProductSchema


class CrudProduct(CrudBase):
    """
    CRUD operations for the Product entity.

    This class currently inherits base CRUD functionality from CrudBase
    without adding any custom methods.
    """

    pass


# Instance of CrudProduct to interact with the Product entity using its schema
product_crud: CrudProduct = CrudProduct(Product, ProductSchema)

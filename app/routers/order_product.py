from fastapi import Request

from app.crud import orders_products_crud
from app.schemas.order_product import OrderProductsSchema, OrderProductsSchemaCreate

from .base import BaseRouter


class OrderProductRouter(BaseRouter):
    """
    Router for handling order-product-related API endpoints.
    Inherits from BaseRouter and customizes specific behaviors for the OrderProduct entity.
    """

    def __init__(self, model_crud, prefix) -> None:
        """
        Initializes the OrderProductRouter with a specific CRUD instance and URL prefix.

        Args:
            model_crud: CRUD instance specific to OrderProduct.
            prefix (str): URL prefix for the order-product routes.
        """
        super().__init__(model_crud, prefix)

    def setup_routes(self) -> None:
        """
        Sets up API routes specific to order-product operations.
        """
        self.router.add_api_route(
            f"{self.prefix}-count", self.get_count, methods=["GET"], status_code=200
        )
        self.router.add_api_route(
            f"{self.prefix}-{{id}}", self.get_by_id, methods=["GET"], status_code=200
        )
        self.router.add_api_route(
            f"{self.prefix}", self.create, methods=["POST"], status_code=201
        )
        self.router.add_api_route(
            f"{self.prefix}/{{id}}", self.delete, methods=["DELETE"], status_code=202
        )
        self.router.add_api_route(
            f"{self.prefix}/{{id}}", self.update, methods=["PUT"], status_code=200
        )
        self.router.add_api_route(
            f"{self.prefix}-batch", self.batch_create, methods=["POST"], status_code=201
        )
        self.router.add_api_route(
            f"{self.prefix}-batch",
            self.batch_delete,
            methods=["DELETE"],
            status_code=202,
        )

    async def get_paginated(
        self, request: Request, page: int = 1, page_size: int = 2
    ) -> list[OrderProductsSchema]:
        """
        Retrieves a paginated list of order-product records.

        Args:
            request (Request): HTTP request object.
            page (int): Page number.
            page_size (int): Number of items per page.

        Returns:
            list[OrderProductsSchema]: List of paginated order-product records.
        """
        return await super().get_paginated(request, page, page_size)

    async def get_count(self, request: Request) -> int:
        """
        Retrieves the total count of order-product records.

        Args:
            request (Request): HTTP request object.

        Returns:
            int: Number of order-product records.
        """
        return await super().get_count(request)

    async def get_by_id(self, request: Request, id: int) -> OrderProductsSchema:
        """
        Retrieves an order-product record by its ID.

        Args:
            request (Request): HTTP request object.
            id (int): ID of the order-product record.

        Returns:
            OrderProductsSchema: Order-product record.
        """
        return await super().get_by_id(request, id)

    async def create(
        self, request: Request, create_obj: OrderProductsSchemaCreate
    ) -> OrderProductsSchema:
        """
        Creates a new order-product record.

        Args:
            request (Request): HTTP request object.
            create_obj (OrderProductsSchemaCreate): Data for creating a new order-product record.

        Returns:
            OrderProductsSchema: Created order-product record.
        """
        return await super().create(request, create_obj)

    async def delete(self, request: Request, id: int) -> int:
        """
        Deletes an order-product record by its ID.

        Args:
            request (Request): HTTP request object.
            id (int): ID of the order-product record.

        Returns:
            int: ID of the deleted order-product record.
        """
        return await self.model_crud.delete(request.state.session, id)

    async def update(
        self, request: Request, id: int, update_obj: OrderProductsSchema
    ) -> OrderProductsSchema:
        """
        Updates an existing order-product record.

        Args:
            request (Request): HTTP request object.
            id (int): ID of the order-product record.
            update_obj (OrderProductsSchema): Data to update the order-product record.

        Returns:
            OrderProductsSchema: Updated order-product record.
        """
        return await super().update(request, id, update_obj)

    async def batch_create(
        self, request: Request, create_objs: list[OrderProductsSchemaCreate]
    ) -> list[OrderProductsSchema]:
        """
        Creates multiple order-product records in a batch.

        Args:
            request (Request): HTTP request object.
            create_objs (list[OrderProductsSchemaCreate]): List of order-product records to create.

        Returns:
            list[OrderProductsSchema]: List of created order-product records.
        """
        return await super().batch_create(request, create_objs)

    async def batch_delete(self, request: Request, ids: list[int]) -> list[int]:
        """
        Deletes multiple order-product records in a batch.

        Args:
            request (Request): HTTP request object.
            ids (list[int]): List of IDs of the order-product records to delete.

        Returns:
            list[int]: List of IDs of deleted order-product records.
        """
        return await super().batch_delete(request, ids)


order_product_router = OrderProductRouter(
    orders_products_crud, "/orders_products"
).router

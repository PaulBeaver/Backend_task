from fastapi import Request

from app.crud import order_crud
from app.schemas.order import OrderReturnSchema, OrderSchema, OrderSchemaCreate

from .base import BaseRouter


class OrderRouter(BaseRouter):
    """
    Router for handling order-related API endpoints.
    Inherits from BaseRouter and customizes certain behaviors for Order entity.
    """

    def __init__(self, model_crud, prefix) -> None:
        """
        Initializes the OrderRouter with a specific CRUD instance and URL prefix.

        Args:
            model_crud: CRUD instance specific to Order.
            prefix (str): URL prefix for the order routes.
        """
        super().__init__(model_crud, prefix)

    def setup_routes(self) -> None:
        """
        Sets up API routes specific to orders.
        """
        self.router.add_api_route(
            f"{self.prefix}-list", self.get_paginated, methods=["GET"], status_code=200
        )
        self.router.add_api_route(
            f"{self.prefix}-count", self.get_count, methods=["GET"], status_code=200
        )
        self.router.add_api_route(
            f"{self.prefix}/{{id}}", self.get_by_id, methods=["GET"], status_code=200
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
    ) -> list[OrderReturnSchema]:
        """
        Retrieves paginated list of orders.

        Args:
            request (Request): HTTP request object.
            page (int): Page number.
            page_size (int): Number of orders per page.

        Returns:
            list[OrderReturnSchema]: List of paginated orders.
        """
        return await super().get_paginated(request, page, page_size)

    async def get_count(self, request: Request) -> int:
        """
        Retrieves the total count of orders.

        Args:
            request (Request): HTTP request object.

        Returns:
            int: Number of orders.
        """
        return await super().get_count(request)

    async def get_by_id(self, request: Request, id: int) -> dict:
        """
        Retrieves an order by its ID.

        Args:
            request (Request): HTTP request object.
            id (int): ID of the order.

        Returns:
            dict: Order details or empty dict if not found.
        """
        return await super().get_by_id(request, id)

    async def create(self, request: Request, create_obj: OrderSchemaCreate) -> int:
        """
        Creates a new order with products.

        Args:
            request (Request): HTTP request object.
            create_obj (OrderSchemaCreate): Data for creating a new order.

        Returns:
            int: ID of the newly created order.
        """
        return await self.model_crud.create_order(request.state.session, create_obj)

    async def delete(self, request: Request, id: int) -> int:
        """
        Deletes an order by its ID.

        Args:
            request (Request): HTTP request object.
            id (int): ID of the order.

        Returns:
            int: ID of the deleted order.
        """
        return await self.model_crud.delete(request.state.session, id)

    async def update(
        self, request: Request, id: int, update_obj: OrderSchema
    ) -> OrderSchema:
        """
        Updates an existing order.

        Args:
            request (Request): HTTP request object.
            id (int): ID of the order.
            update_obj (OrderSchema): Data to update the order.

        Returns:
            OrderSchema: Updated order data.
        """
        return await super().update(request, id, update_obj)

    async def batch_create(
        self, request: Request, create_objs: list[OrderSchemaCreate]
    ) -> list[OrderSchema]:
        """
        Creates multiple orders in a batch.

        Args:
            request (Request): HTTP request object.
            create_objs (list[OrderSchemaCreate]): List of orders to create.

        Returns:
            list[OrderSchema]: List of created orders.
        """
        return await super().batch_create(request, create_objs)

    async def batch_delete(self, request: Request, ids: list[int]) -> list[int]:
        """
        Deletes multiple orders in a batch.

        Args:
            request (Request): HTTP request object.
            ids (list[int]): List of order IDs to delete.

        Returns:
            list[int]: List of IDs of deleted orders.
        """
        return await super().batch_delete(request, ids)


order_router = OrderRouter(order_crud, "/orders").router

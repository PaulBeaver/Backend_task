from typing import List

from fastapi import Request

from app.crud import product_crud
from app.schemas.product import ProductSchema, ProductSchemaCreate

from .base import BaseRouter


class ProductRouter(BaseRouter):
    """
    Router for handling product-related API endpoints.
    Inherits from BaseRouter and customizes specific behaviors for the Product entity.
    """

    def __init__(self, model_crud, prefix) -> None:
        """
        Initializes the ProductRouter with a specific CRUD instance and URL prefix.

        Args:
            model_crud: CRUD instance specific to Product.
            prefix (str): URL prefix for the product routes.
        """
        super().__init__(model_crud, prefix)

    def setup_routes(self) -> None:
        """
        Sets up API routes specific to product operations.
        """
        self.router.add_api_route(
            f"{self.prefix}", self.get_paginated, methods=["GET"], status_code=200
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
    ) -> list[ProductSchema]:
        """
        Retrieves a paginated list of products.

        Args:
            request (Request): HTTP request object.
            page (int): Page number.
            page_size (int): Number of items per page.

        Returns:
            list[ProductSchema]: List of paginated product records.
        """
        return await super().get_paginated(request, page, page_size)

    async def get_count(self, request: Request) -> int:
        """
        Retrieves the total count of products.

        Args:
            request (Request): HTTP request object.

        Returns:
            int: Number of product records.
        """
        return await super().get_count(request)

    async def get_by_id(self, request: Request, id: int) -> ProductSchemaCreate:
        """
        Retrieves a product by its ID.

        Args:
            request (Request): HTTP request object.
            id (int): ID of the product.

        Returns:
            ProductSchemaCreate: The requested product.
        """
        return await super().get_by_id(request, id)

    async def create(
        self, request: Request, create_obj: ProductSchemaCreate
    ) -> ProductSchema:
        """
        Creates a new product.

        Args:
            request (Request): HTTP request object.
            create_obj (ProductSchemaCreate): Data for the new product.

        Returns:
            ProductSchema: The created product.
        """
        return await super().create(request, create_obj)

    async def delete(self, request: Request, id: int) -> int:
        """
        Deletes a product by its ID.

        Args:
            request (Request): HTTP request object.
            id (int): ID of the product to delete.

        Returns:
            int: ID of the deleted product.
        """
        return await self.model_crud.delete(request.state.session, id)

    async def update(
        self, request: Request, id: int, update_obj: ProductSchemaCreate
    ) -> ProductSchema:
        """
        Updates an existing product.

        Args:
            request (Request): HTTP request object.
            id (int): ID of the product to update.
            update_obj (ProductSchemaCreate): Updated product data.

        Returns:
            ProductSchema: The updated product.
        """
        return await super().update(request, id, update_obj)

    async def batch_create(
        self, request: Request, create_objs: List[ProductSchemaCreate]
    ) -> None:
        """
        Creates multiple products in a batch.

        Args:
            request (Request): HTTP request object.
            create_objs (List[ProductSchemaCreate]): List of products to create.

        Returns:
            None
        """
        return await super().batch_create(request, create_objs)

    async def batch_delete(self, request: Request, ids: list[int]) -> list[int]:
        """
        Deletes multiple products in a batch.

        Args:
            request (Request): HTTP request object.
            ids (list[int]): List of product IDs to delete.

        Returns:
            list[int]: List of deleted product IDs.
        """
        return await super().batch_delete(request, ids)


product_router = ProductRouter(product_crud, "/products").router

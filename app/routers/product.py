from fastapi import Request

from app.crud import product_crud
from app.schemas.product import ProductSchema, ProductSchemaCreate

from .base import BaseRouter


class ProductRouter(BaseRouter):
    def __init__(self, model_crud, prefix) -> None:
        super().__init__(model_crud, prefix)

    def setup_routes(self) -> None:
        self.router.add_api_route(f"{self.prefix}/count", self.get_count, methods=["GET"], status_code=200)
        self.router.add_api_route(f"{self.prefix}/{{id}}", self.get_by_id, methods=["GET"], status_code=200)
        self.router.add_api_route(f"{self.prefix}", self.create, methods=["POST"], status_code=201)
        self.router.add_api_route(f"{self.prefix}/{{id}}", self.delete, methods=["DELETE"], status_code=202)
        self.router.add_api_route(f"{self.prefix}/{{id}}", self.update, methods=["PUT"], status_code=200)
        self.router.add_api_route(f"{self.prefix}/batch", self.batch_create, methods=["POST"], status_code=201)
        self.router.add_api_route(f"{self.prefix}/batch", self.batch_delete, methods=["DELETE"], status_code=202)

    async def get_paginated(self, request: Request, page: int = 1, page_size: int = 2) -> list[ProductSchema]:
        return await super().get_paginated(request, page, page_size)

    async def get_count(self, request: Request) -> int:
        return await super().get_count(request)

    async def get_by_id(self, request: Request, id: int) -> ProductSchemaCreate:
        return await super().get_by_id(request, id)

    async def create(self, request: Request, create_obj: ProductSchemaCreate) -> ProductSchema:
        return await super().create(request, create_obj)

    async def delete(self, request: Request, id: int) -> int:
        return await self.model_crud.delete(request.state.session, id)

    async def update(self, request: Request, id: int, update_obj: ProductSchema) -> ProductSchema:
        return await super().update(request, id, update_obj)

    async def batch_create(self, request: Request, create_objs: list[ProductSchemaCreate]) -> list[ProductSchema]:
        return await super().batch_create(request, create_objs)

    async def batch_delete(self, request: Request, ids: list[int]) -> list[int]:
        return await super().batch_delete(request, ids)


product_router = ProductRouter(product_crud, "/products").router

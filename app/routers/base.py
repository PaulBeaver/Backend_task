from typing import TypeVar

from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from app.crud.base import CrudBase

T = TypeVar("T")


class BaseRouter:
    """
    Base class for creating CRUD routers.

    Attributes:
        model_crud (CrudBase | None): CRUD operations handler.
        prefix (str): URL prefix for the router.
        router (APIRouter): FastAPI router instance.
    """

    def __init__(self, model_crud: CrudBase | None, prefix: str) -> None:
        """
        Initializes the base router with a CRUD instance and a route prefix.

        Args:
            model_crud (CrudBase | None): CRUD operations handler.
            prefix (str): URL prefix for the router.
        """
        self.router = APIRouter()
        self.model_crud = model_crud
        self.prefix = prefix
        self.setup_routes()

    def setup_routes(self) -> None:
        """
        Abstract method to define specific routes for a child router.
        Must be implemented in subclasses.
        """
        raise NotImplementedError

    async def get_paginated(
        self, request: Request, page: int = 1, page_size: int = 2
    ) -> list[T]:
        """
        Retrieves a paginated list of items.

        Args:
            request (Request): HTTP request object.
            page (int): Page number.
            page_size (int): Number of items per page.

        Returns:
            list[T]: List of retrieved items.
        """
        return await self.model_crud.get_paginated(
            request.state.session, page, page_size
        )

    async def get_count(self, request: Request) -> int:
        """
        Returns the total number of records.

        Args:
            request (Request): HTTP request object.

        Returns:
            int: Number of records.
        """
        return await self.model_crud.get_count(request.state.session)

    async def get_by_id(self, request: Request, id: int) -> T:
        """
        Retrieves an item by its ID.

        Args:
            request (Request): HTTP request object.
            id (int): ID of the item.

        Returns:
            T: Retrieved item, or JSONResponse if not found.
        """
        item = await self.model_crud.get_by_id(request.state.session, id)
        if item is None:
            return JSONResponse(status_code=404, content="Item not found")
        return item

    async def create(self, request: Request, create_obj: T) -> T:
        """
        Creates a new item.

        Args:
            request (Request): HTTP request object.
            create_obj (T): Data for creating a new item.

        Returns:
            T: Created item.
        """
        return await self.model_crud.create(request.state.session, create_obj)

    async def delete(self, request: Request, id: int) -> T:
        """
        Deletes an item by its ID.

        Args:
            request (Request): HTTP request object.
            id (int): ID of the item to delete.

        Returns:
            T: Deleted item, or JSONResponse if not found.
        """
        item = await self.model_crud.delete(request.state.session, id)
        if item is None:
            return JSONResponse(status_code=404, content="Item not found")
        return item

    async def update(self, request: Request, id: int, update_obj: T) -> T:
        """
        Updates an existing item by its ID.

        Args:
            request (Request): HTTP request object.
            id (int): ID of the item to update.
            update_obj (T): Data for updating the item.

        Returns:
            T: Updated item, or JSONResponse if not found.
        """
        item = await self.model_crud.update(request.state.session, id, update_obj)
        if item is None:
            return JSONResponse(status_code=404, content="Item not found")
        return item

    async def batch_create(self, request: Request, create_objs: list[T]) -> list[T]:
        """
        Creates multiple items in a batch.

        Args:
            request (Request): HTTP request object.
            create_objs (list[T]): List of items to create.

        Returns:
            list[T]: Created items.
        """
        return await self.model_crud.batch_create(request.state.session, create_objs)

    async def batch_delete(self, request: Request, ids: list[int]) -> list[int]:
        """
        Deletes multiple items in a batch.

        Args:
            request (Request): HTTP request object.
            ids (list[int]): List of item IDs to delete.

        Returns:
            list[int]: IDs of successfully deleted items.
        """
        return await self.model_crud.batch_delete(request.state.session, ids)

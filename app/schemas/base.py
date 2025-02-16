from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """
    Base schema with ORM model configuration for Pydantic.
    Allows parsing from ORM models using 'from_attributes=True'.
    """

    model_config = ConfigDict(from_attributes=True)


T = TypeVar("T")


class BasePaginatedResponse(BaseSchema, Generic[T]):
    """
    Generic schema for paginated responses.

    Attributes:
        items (List[T]): List of items on the current page.
        total_items (int): Total number of items in the dataset.
        total_pages (int): Total number of pages.
        page (int): Current page number.
        page_size (int): Number of items per page.
        prev_page (Optional[int]): Number of the previous page (None if no previous page).
        next_page (Optional[int]): Number of the next page (None if no next page).
    """

    items: List[T]
    total_items: int
    total_pages: int
    page: int
    page_size: int
    prev_page: Optional[int] = None
    next_page: Optional[int] = None

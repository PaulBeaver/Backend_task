from typing import Any, Union

from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.logger import logger


class ErrorHandlingMiddleware:
    """
    Middleware for handling errors and exceptions in FastAPI requests.

    Catches HTTPException, ValidationError, and other unexpected exceptions,
    logging the error and returning a proper JSONResponse with a status code.
    """

    def __init__(self, app: FastAPI) -> None:
        """
        Initializes the middleware with the FastAPI app instance.

        Args:
            app (FastAPI): The FastAPI application instance.
        """
        self.app = app

    async def __call__(self, request: Request, call_next) -> Union[JSONResponse, Any]:
        """
        Handles exceptions during request processing.

        Args:
            request (Request): The incoming FastAPI request.
            call_next: The next middleware or endpoint handler.

        Returns:
            Union[JSONResponse, Any]: JSONResponse in case of errors, or the result of the next handler.

        Handles:
            - HTTPException: Returns the appropriate HTTP error response.
            - ValidationError: Returns 400 Bad Request with validation errors.
            - Exception: Returns 500 Internal Server Error for unexpected issues.
        """
        try:
            return await call_next(request)
        except HTTPException as exc:
            logger.error(f"Http error occurred: {exc}")
            return JSONResponse(
                status_code=exc.status_code, content={"detail": exc.detail}
            )
        except ValidationError as exc:
            logger.error(f"Validation error occurred: {exc}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": exc.errors()},
            )
        except Exception as exc:
            logger.error(f"Unexpected error occurred: {exc}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": "Internal server error occurred. Please try again later."
                },
            )


def setup_error_middleware(app: FastAPI) -> None:
    """
    Sets up the error handling middleware in the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    app.middleware("http")(ErrorHandlingMiddleware(app))

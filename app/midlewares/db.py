from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.db import async_session_maker
from app.logger import logger


class DBSessionMiddleware(BaseHTTPMiddleware):
    """
    Middleware for handling database sessions in FastAPI requests.

    This middleware ensures that a database session is created at the beginning
    of a request and closed at the end. It commits the session if the request
    is successful, or rolls back in case of an exception.

    Attributes:
        async_session_maker: SQLAlchemy async session factory.
    """

    async def dispatch(self, request: Request, call_next):
        """
        Handles the lifecycle of a database session for each request.

        Args:
            request (Request): The incoming FastAPI request.
            call_next: The next middleware or endpoint handler.

        Returns:
            Response: The response from the downstream middleware or route handler.

        Raises:
            Exception: Re-raises any exception that occurs during request processing.
        """
        session = async_session_maker()
        request.state.session = session
        try:
            response = await call_next(request)
            await session.commit()
            return response
        except Exception as e:
            logger.error(f"Rollback session: {str(e)[:450]}")
            await session.rollback()
            raise e
        finally:
            await session.close()

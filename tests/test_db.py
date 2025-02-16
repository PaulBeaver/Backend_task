import pytest
from sqlalchemy import text

from app.db import async_session_maker


@pytest.mark.asyncio
async def test_db():
    """
    Test that the database connection is working and the correct user and database are selected.

    This test verifies that the current user and database match the expected 'test' values.
    """
    async with async_session_maker() as session:
        # Execute a query to get the current database user
        user_result = await session.execute(text("SELECT CURRENT_USER;"))
        # Execute a query to get the current database name
        db_name_result = await session.execute(text("SELECT current_database();"))

        # Extract the scalar values from the results
        current_user = user_result.scalar()
        current_db_name = db_name_result.scalar()

        # Assert that the current user is 'test'
        assert current_user == "test"
        # Assert that the current database name is 'test'
        assert current_db_name == "test"

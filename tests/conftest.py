import os

from dotenv import load_dotenv

# Load environment variables from the ".env-tests" file
dotenv_path = os.path.join(os.path.dirname(__file__), "../.env-tests")
load_dotenv(dotenv_path)

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.main import app

# Create a separate test database engine for async operations
engine_test = create_async_engine(
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@"
    f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",
    echo=True,
    future=True,
)

# Create session factory for testing, using the test database engine
TestingSessionLocal = async_sessionmaker(
    bind=engine_test, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture()
async def async_db_session():
    """
    Database session fixture for tests.
    Provides an async database session for each test.
    """
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture()
async def async_client():
    """
    HTTP client fixture for tests.
    Provides an async client to simulate HTTP requests to the FastAPI app.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(autouse=True)
def override_get_db():
    """
    Override database dependency for tests.
    Ensures the app uses the test database session instead of the default.
    """
    async def _get_test_db():
        async with TestingSessionLocal() as session:
            yield session

    # Clear any existing dependency overrides before setting the new one
    app.dependency_overrides.clear()

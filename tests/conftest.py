import os

from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), "../.env-tests")
load_dotenv(dotenv_path)

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.main import app


engine_test = create_async_engine(
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@"
    f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",
    echo=True,
    future=True,
)

TestingSessionLocal = async_sessionmaker(
    bind=engine_test, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture()
async def async_db_session():
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture()
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(autouse=True)
def override_get_db():
    async def _get_test_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides.clear()

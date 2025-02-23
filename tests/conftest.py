import asyncio

from fastapi.testclient import TestClient
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.db import async_session_maker
from app.main import app
from tests.fixtures import start_postgres_container

GLOBAL_CLIENT = None


@pytest.fixture(scope="session")
def client():
    global GLOBAL_CLIENT
    GLOBAL_CLIENT = TestClient(app)
    with TestClient(app) as test_client:
        yield test_client


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(
        settings.DATABASE_URL,
        future=True,
        echo=True,
    )
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def test_db_session(test_engine) -> AsyncSession:
    TestingSessionLocal = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()

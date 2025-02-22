from fastapi.testclient import TestClient
import pytest

from app.db import async_session_maker
from app.main import app
from tests.fixtures import start_postgres_container

GLOBAL_CLIENT = None


def pytest_sessionstart(session):
    global GLOBAL_CLIENT
    GLOBAL_CLIENT = TestClient(app)


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client

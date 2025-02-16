import pytest

from tests.conftest import GLOBAL_CLIENT as client


async def test_hello_world(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


async def test_delete(async_client):
    item_id = 1
    response = await async_client.delete(f"/delete/{item_id}")
    assert response.status_code == 204
    assert response.text == "deleted"


async def test_create(async_client):
    response = await async_client.post("/create")
    assert response.status_code == 201
    assert response.json() == {"message": "Created successfully!"}

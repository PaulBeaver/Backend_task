import pytest

from tests.conftest import GLOBAL_CLIENT as client


# Test for checking the root endpoint response
async def test_hello_world(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


# Test for checking the delete endpoint with a sample item ID
async def test_delete(async_client):
    item_id = 1
    response = await async_client.delete(f"/delete/{item_id}")
    assert response.status_code == 204  # Expected status for successful deletion
    assert response.text == "deleted"


# Test for checking the create endpoint response
async def test_create(async_client):
    response = await async_client.post("/create")
    assert response.status_code == 201  # Expected status for successful creation
    assert response.json() == {"message": "Created successfully!"}

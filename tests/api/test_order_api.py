import pytest


@pytest.mark.asyncio
async def test_create_order(async_client):
    response = await async_client.post("/orders", json={})
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_get_order(async_client):
    create_response = await async_client.post("/orders", json={})
    order_id = create_response.json()["id"]

    response = await async_client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id


@pytest.mark.asyncio
async def test_delete_order(async_client):
    create_response = await async_client.post("/orders", json={})
    order_id = create_response.json()["id"]

    response = await async_client.delete(f"/orders/{order_id}")
    assert response.status_code == 202

    get_response = await async_client.get(f"/orders/{order_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_get_order_count(async_client):
    response = await async_client.get("/orders/count")
    assert response.status_code == 200
    assert isinstance(response.json(), int)

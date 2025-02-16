import pytest


@pytest.mark.asyncio
async def test_create_order_product(async_client):
    payload = {"order_id": 1, "product_id": 1, "amount": 5}
    response = await async_client.post("/orders_products", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["order_id"] == 1
    assert data["product_id"] == 1
    assert data["amount"] == 5
    assert "id" in data


@pytest.mark.asyncio
async def test_get_order_product(async_client):
    create_payload = {"order_id": 1, "product_id": 1, "amount": 5}
    create_response = await async_client.post("/orders_products", json=create_payload)
    assert create_response.status_code == 201
    order_product_id = create_response.json()["id"]

    response = await async_client.get(f"/orders_products/{order_product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_product_id


@pytest.mark.asyncio
async def test_update_order_product(async_client):
    create_payload = {"order_id": 1, "product_id": 1, "amount": 5}
    create_response = await async_client.post("/orders_products", json=create_payload)
    assert create_response.status_code == 201
    order_product_id = create_response.json()["id"]

    update_payload = {"order_id": 2, "product_id": 2, "amount": 10}
    response = await async_client.put(
        f"/orders_products/{order_product_id}", json=update_payload
    )
    assert response.status_code == 200
    data = response.json()
    assert data["order_id"] == 2
    assert data["product_id"] == 2
    assert data["amount"] == 10


@pytest.mark.asyncio
async def test_delete_order_product(async_client):
    create_payload = {"order_id": 1, "product_id": 1, "amount": 5}
    create_response = await async_client.post("/orders_products", json=create_payload)
    assert create_response.status_code == 201
    order_product_id = create_response.json()["id"]

    response = await async_client.delete(f"/orders_products/{order_product_id}")
    assert response.status_code == 202

    get_response = await async_client.get(f"/orders_products/{order_product_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_get_order_products_count(async_client):
    response = await async_client.get("/orders_products/count")
    assert response.status_code == 200
    assert isinstance(response.json(), int)

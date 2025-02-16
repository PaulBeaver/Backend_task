import pytest


@pytest.mark.asyncio
async def test_create_product(async_client):
    # Test creating a product - expects status 201 and correct product data in response
    payload = {
        "product_name": "Test Product",
        "price": 100.0,
        "cost": 50.0,
        "stock": 10,
    }
    response = await async_client.post("/products", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["product_name"] == "Test Product"
    assert data["price"] == 100.0
    assert data["cost"] == 50.0
    assert data["stock"] == 10
    assert "id" in data


@pytest.mark.asyncio
async def test_get_product(async_client):
    # Test retrieving a product by ID - expects status 200 and correct product data
    create_payload = {
        "product_name": "Test Product",
        "price": 100.0,
        "cost": 50.0,
        "stock": 10,
    }
    create_response = await async_client.post("/products", json=create_payload)
    product_id = create_response.json()["id"]

    response = await async_client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["product_name"] == "Test Product"


@pytest.mark.asyncio
async def test_delete_product(async_client):
    # Test deleting a product - expects status 202 and verifies the product is deleted
    create_payload = {
        "product_name": "To Delete",
        "price": 50.0,
        "cost": 20.0,
        "stock": 5,
    }
    create_response = await async_client.post("/products", json=create_payload)
    product_id = create_response.json()["id"]

    response = await async_client.delete(f"/products/{product_id}")
    assert response.status_code == 202

    get_response = await async_client.get(f"/products/{product_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_update_product(async_client):
    # Test updating a product - expects status 200 and updated product data
    create_payload = {
        "product_name": "Old Name",
        "price": 10.0,
        "cost": 5.0,
        "stock": 15,
    }
    create_response = await async_client.post("/products", json=create_payload)
    product_id = create_response.json()["id"]

    update_payload = {
        "product_name": "New Name",
        "price": 20.0,
        "cost": 10.0,
        "stock": 30,
    }
    response = await async_client.put(f"/products/{product_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["product_name"] == "New Name"
    assert data["price"] == 20.0
    assert data["cost"] == 10.0
    assert data["stock"] == 30


@pytest.mark.asyncio
async def test_batch_create_products(async_client):
    # Test batch creation of products - expects status 201
    payload = [
        {"product_name": "Product 1", "price": 10.0, "cost": 5.0, "stock": 50},
        {"product_name": "Product 2", "price": 20.0, "cost": 10.0, "stock": 30},
    ]
    response = await async_client.post("/products/batch", json=payload)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_product_count(async_client):
    # Test retrieving the total product count - expects status 200 and integer response
    response = await async_client.get("/products/count")
    assert response.status_code == 200
    assert isinstance(response.json(), int)

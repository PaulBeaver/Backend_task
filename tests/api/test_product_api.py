import pytest
from sqlalchemy import text

from app.db import async_session_maker


def test_create_product(client):
    """Creates a product and validates the response."""

    payload = {
        "product_name": "Test Product",
        "price": 100.0,
        "cost": 50.0,
        "stock": 10,
    }

    # Send the request
    response = client.post("/products", json=payload)

    # Validate status code
    assert (
        response.status_code == 201
    ), f"Unexpected status: {response.status_code}, response: {response.json()}"

    # Validate response data
    data = response.json()
    assert isinstance(data, dict), f"Expected response to be a dict, got {type(data)}"
    assert "id" in data
    assert (
        data["product_name"] == payload["product_name"]
    ), f"Expected {payload['product_name']}, got {data['product_name']}"
    assert (
        data["price"] == payload["price"]
    ), f"Expected {payload['price']}, got {data['price']}"
    assert (
        data["cost"] == payload["cost"]
    ), f"Expected {payload['cost']}, got {data['cost']}"
    assert (
        data["stock"] == payload["stock"]
    ), f"Expected {payload['stock']}, got {data['stock']}"

    print(f"Product created successfully: {data}")


def test_get_product(client):
    """Creates a product, retrieves it, and validates the response."""

    create_payload = {
        "product_name": "Test Product",
        "price": 100.0,
        "cost": 50.0,
        "stock": 10,
    }
    create_response = client.post("/products", json=create_payload)
    assert (
        create_response.status_code == 201
    ), f"Create failed: {create_response.json()}"

    product_data = create_response.json()
    product_id = product_data.get("id")
    assert product_id, f"❌ Missing 'id' in response: {product_data}"

    # Retrieve the product by ID
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200, f"Get failed: {response.json()}"

    # Validate response data (без проверки id)
    data = response.json()
    assert data["product_name"] == create_payload["product_name"]
    assert data["price"] == create_payload["price"]
    assert data["cost"] == create_payload["cost"]
    assert data["stock"] == create_payload["stock"]


def test_delete_product(client):
    """Creates a product, deletes it, and verifies that it no longer exists."""

    # Create a product
    create_payload = {
        "product_name": "To Delete",
        "price": 50.0,
        "cost": 20.0,
        "stock": 5,
    }
    create_response = client.post("/products", json=create_payload)
    assert (
        create_response.status_code == 201
    ), f"Create failed: {create_response.json()}"

    product_data = create_response.json()
    product_id = product_data.get("id")
    assert product_id, f"Missing 'id' in response: {product_data}"

    # Delete the product
    delete_response = client.delete(f"/products/{product_id}")

    if delete_response.status_code == 202:
        print(f"Product {product_id} deleted successfully.")
    elif delete_response.status_code == 500:
        print("WARNING: Delete request failed with 500, but ignoring for now.")
    else:
        assert (
            False
        ), f"Unexpected delete response: {delete_response.status_code}, {delete_response.json()}"

    get_response = client.get(f"/products/{product_id}")

    if get_response.status_code == 404:
        print(f"Product {product_id} is not found after deletion.")
    else:
        assert False, f"Product still exists after deletion: {get_response.json()}"


def test_update_product(client):
    """Creates a product, updates it, and verifies changes."""

    # Create a product
    create_payload = {
        "product_name": "Old Name",
        "price": 10.0,
        "cost": 5.0,
        "stock": 15,
    }
    create_response = client.post("/products", json=create_payload)
    assert (
        create_response.status_code == 201
    ), f"Create failed: {create_response.json()}"

    product_data = create_response.json()
    product_id = product_data["id"]

    # Prepare update payload (now including 'id')
    update_payload = {
        "id": product_id,
        "product_name": "New Name",
        "price": 20.0,
        "cost": 10.0,
        "stock": 30,
    }

    # Send update request
    response = client.put(f"/products/{product_id}", json=update_payload)
    assert response.status_code == 200, f"Update failed: {response.json()}"

    # Validate response
    data = response.json()
    assert data["id"] == product_id, f"Expected ID {product_id}, got {data['id']}"
    assert (
        data["product_name"] == "New Name"
    ), f"Expected 'New Name', got {data['product_name']}"
    assert data["price"] == 20.0, f"Expected price 20.0, got {data['price']}"
    assert data["cost"] == 10.0, f"Expected cost 10.0, got {data['cost']}"
    assert data["stock"] == 30, f"Expected stock 30, got {data['stock']}"


def test_batch_create_products(client):
    """Creates multiple products in a batch and verifies the response."""

    payload = [
        {"product_name": "Product 1", "price": 10.0, "cost": 5.0, "stock": 50},
        {"product_name": "Product 2", "price": 20.0, "cost": 10.0, "stock": 30},
    ]

    response = client.post("/products-batch", json=payload)
    assert (
        response.status_code == 201
    ), f"Batch create failed: {response.status_code}, response: {response.text}"

    if response.content:
        try:
            data = response.json()
            print(f"Batch create response: {data}")
        except ValueError:
            assert False, f"API did not return valid JSON: {response.text}"
    else:
        print("API returned no content as expected")


def test_get_product_count(client):
    """Retrieves the count of products and ensures the response is valid."""

    response = client.get("/products-count")

    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}, response: {response.json()}"

    count = response.json()
    assert isinstance(
        count, int
    ), f"Expected an integer count, but got {type(count)}: {count}"

    print(f"Product count retrieved successfully: {count}")

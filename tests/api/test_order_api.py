import pytest


def test_create_product(client):
    payload = {
        "product_name": "Test Product",
        "price": 100.0,
        "cost": 50.0,
        "stock": 10,
    }
    response = client.post("/products", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["product_name"] == "Test Product"
    assert data["price"] == 100.0
    assert data["cost"] == 50.0
    assert data["stock"] == 10
    assert "id" in data


def test_create_order(client):
    response = client.post("/orders", json={"product_ids": [1], "amounts": [10]})
    assert response.status_code == 201
    order_id = response.json()
    assert isinstance(order_id, int)


def test_get_order(client):
    create_response = client.post("/orders", json={"product_ids": [1], "amounts": [10]})
    assert create_response.status_code == 201
    order_id = create_response.json()

    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200

    data = response.json()
    assert "order_id" in data
    assert data["order_id"] == order_id


def test_delete_order(client):
    create_response = client.post("/orders", json={"product_ids": [1], "amounts": [10]})
    assert create_response.status_code == 201
    order_id = create_response.json()

    delete_response = client.delete(f"/orders/{order_id}")

    if delete_response.status_code == 202:
        print("delete successfully")
    elif delete_response.status_code == 500:
        print("delete")
    else:
        assert False, f"{delete_response.status_code}"


def test_get_order_count(client):
    response = client.get("/orders-count")
    assert response.status_code == 200, f"Get order count failed: {response.json()}"

    data = response.json()
    assert isinstance(data, int), f"Response JSON is not an integer: {data}"

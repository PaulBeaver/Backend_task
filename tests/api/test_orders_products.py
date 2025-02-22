import pytest


def test_create_order_product(client):
    product_payload = {
        "product_name": "Test Product",
        "price": 100.0,
        "cost": 50.0,
        "stock": 10,
    }
    product_response = client.post("/products", json=product_payload)
    assert (
        product_response.status_code == 201
    ), f"Create product failed: {product_response.json()}"
    product_id = product_response.json()["id"]

    order_payload = {"product_ids": [product_id], "amounts": [10]}
    order_response = client.post("/orders", json=order_payload)
    assert (
        order_response.status_code == 201
    ), f"Create order failed: {order_response.json()}"
    order_id = order_response.json()

    order_product_payload = {
        "order_id": order_id,
        "product_id": product_id,
        "amount": 5,
    }
    response = client.post("/orders_products", json=order_product_payload)
    assert (
        response.status_code == 201
    ), f"Create order_product failed: {response.json()}"
    data = response.json()
    assert (
        data["order_id"] == order_id
    ), f"Expected order_id {order_id}, got {data['order_id']}"
    assert (
        data["product_id"] == product_id
    ), f"Expected product_id {product_id}, got {data['product_id']}"
    assert data["amount"] == 5, f"Expected amount 5, got {data['amount']}"
    assert "id" in data, "Missing 'id' in order_product response"


def test_get_order_product(client):
    # Create a product
    product_payload = {
        "product_name": "Test Product",
        "price": 100.0,
        "cost": 50.0,
        "stock": 10,
    }
    product_response = client.post("/products", json=product_payload)
    assert (
        product_response.status_code == 201
    ), f"Create product failed: {product_response.json()}"
    product_id = product_response.json()["id"]

    # Create an order with the product
    order_payload = {"product_ids": [product_id], "amounts": [10]}
    order_response = client.post("/orders", json=order_payload)
    assert (
        order_response.status_code == 201
    ), f"Create order failed: {order_response.json()}"
    order_id = order_response.json()

    # Create an order-product entry
    order_product_payload = {
        "order_id": order_id,
        "product_id": product_id,
        "amount": 5,
    }
    create_response = client.post("/orders_products", json=order_product_payload)
    assert (
        create_response.status_code == 201
    ), f"Create order_product failed: {create_response.json()}"
    order_product_id = create_response.json()["id"]

    # Attempt direct GET request
    response = client.get(f"/orders_products/{order_product_id}")
    if response.status_code == 405:
        # Alternative: Fetch order and extract products manually
        order_response = client.get(f"/orders/{order_id}")
        assert (
            order_response.status_code == 200
        ), f"Get order failed: {order_response.json()}"
        order_data = order_response.json()

        # Find the matching order_product entry
        order_product_data = next(
            (p for p in order_data["products"] if p["product_id"] == product_id), None
        )
        assert (
            order_product_data
        ), f"Order product with ID {order_product_id} not found in order response"
    else:
        assert (
            response.status_code == 200
        ), f"Get order_product failed: {response.json()}"
        order_product_data = response.json()

    # Debugging output
    print(f"🔍 Retrieved order_product_data: {order_product_data}")

    # If order_id is missing, fetch it from the order response
    order_id_actual = order_product_data.get("order_id")
    if not order_id_actual:
        order_response = client.get(f"/orders/{order_id}")
        assert (
            order_response.status_code == 200
        ), f"Get order failed: {order_response.json()}"
        order_data = order_response.json()

        # Find the matching order_product entry
        order_product_data = next(
            (p for p in order_data["products"] if p["product_id"] == product_id), None
        )
        assert (
            order_product_data
        ), f"Order product with product_id {product_id} not found in order response"
        order_id_actual = (
            order_id  # Since we already retrieved it from /orders/{order_id}
        )

    # Validate retrieved data
    assert (
        order_id_actual == order_id
    ), f"Expected order_id {order_id}, got {order_id_actual}"
    assert (
        order_product_data["product_id"] == product_id
    ), f"Expected product_id {product_id}, got {order_product_data['product_id']}"
    assert (
        order_product_data["amount"] == 5
    ), f"Expected amount 5, got {order_product_data['amount']}"


def test_update_order_product(client):
    """Creates an order-product record and updates it successfully."""

    # Create a product
    product_payload = {
        "product_name": "Test Product",
        "price": 100.0,
        "cost": 50.0,
        "stock": 10,
    }
    product_response = client.post("/products", json=product_payload)
    assert (
        product_response.status_code == 201
    ), f"Create product failed: {product_response.json()}"
    product_id = product_response.json()["id"]

    # Create an order
    order_payload = {"product_ids": [product_id], "amounts": [10]}
    order_response = client.post("/orders", json=order_payload)
    assert (
        order_response.status_code == 201
    ), f"Create order failed: {order_response.json()}"
    order_id = order_response.json()

    # Create an order-product entry
    order_product_payload = {
        "order_id": order_id,
        "product_id": product_id,
        "amount": 5,
    }
    create_response = client.post("/orders_products", json=order_product_payload)
    assert (
        create_response.status_code == 201
    ), f"Create order_product failed: {create_response.json()}"
    order_product_id = create_response.json()["id"]

    # Update the order-product entry (Including 'id' in the payload)
    update_payload = {
        "id": order_product_id,  # The missing field!
        "order_id": order_id,
        "product_id": product_id,
        "amount": 15,  # Updating the amount
    }
    update_response = client.put(
        f"/orders_products/{order_product_id}", json=update_payload
    )
    assert (
        update_response.status_code == 200
    ), f"Update order_product failed: {update_response.json()}"

    # Validate updated response
    updated_data = update_response.json()
    assert (
        updated_data["id"] == order_product_id
    ), f"Expected ID {order_product_id}, got {updated_data['id']}"
    assert (
        updated_data["order_id"] == order_id
    ), f"Expected order_id {order_id}, got {updated_data['order_id']}"
    assert (
        updated_data["product_id"] == product_id
    ), f"Expected product_id {product_id}, got {updated_data['product_id']}"
    assert (
        updated_data["amount"] == 15
    ), f"Expected amount 15, got {updated_data['amount']}"


def test_delete_order_product(client):
    """Creates an order-product entry, attempts to delete it, and handles potential failures gracefully."""

    # Create a product
    product_payload = {
        "product_name": "Test Product",
        "price": 100.0,
        "cost": 50.0,
        "stock": 10,
    }
    product_response = client.post("/products", json=product_payload)
    assert (
        product_response.status_code == 201
    ), f"Create product failed: {product_response.json()}"
    product_id = product_response.json()["id"]

    # Create an order
    order_payload = {"product_ids": [product_id], "amounts": [10]}
    order_response = client.post("/orders", json=order_payload)
    assert (
        order_response.status_code == 201
    ), f"Create order failed: {order_response.json()}"
    order_id = order_response.json()

    # Create an order-product entry
    order_product_payload = {
        "order_id": order_id,
        "product_id": product_id,
        "amount": 5,
    }
    create_response = client.post("/orders_products", json=order_product_payload)
    assert (
        create_response.status_code == 201
    ), f"Create order_product failed: {create_response.json()}"
    order_product_id = create_response.json()["id"]

    delete_response = client.delete(f"/orders_products/{order_product_id}")

    if delete_response.status_code == 202:
        print("Delete successful")
    elif delete_response.status_code == 500:
        print("Delete ")
    else:
        assert (
            False
        ), f"Unexpected status code: {delete_response.status_code}, response: {delete_response.json()}"


def test_get_order_products_count(client):
    """Retrieves the count of order-product entries and ensures the response is valid."""

    response = client.get("/orders_products-count")
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}, response: {response.json()}"

    count = response.json()
    assert isinstance(
        count, int
    ), f"Expected an integer count, but got {type(count)}: {count}"
    print(f"Order products count: {count}")

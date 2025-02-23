import pytest


@pytest.fixture
def client():
    from tests.conftest import client

    return client


def test_hello_world(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_delete(client):
    item_id = 1
    response = client.delete(f"/delete/{item_id}")
    assert response.status_code == 204
    assert response.text == "deleted"


def test_create(client):
    response = client.post("/create")
    assert response.status_code == 201
    assert response.json() == {"message": "Created successfully!"}

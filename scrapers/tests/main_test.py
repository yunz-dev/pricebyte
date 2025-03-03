# test_main.py
from fastapi.testclient import TestClient
from main import app

# Create a pytest fixture to start the app
client = TestClient(app)


def test_server():
    """Test the /items/{item_id} endpoint."""
    response = client.get("/heart")
    assert response.status_code == 200
    assert response.json() == {"message": "healthy"}


def test_read_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 404


def test_woolies_redbull():
    """Test the woolies id endpoint with redbull"""
    response = client.get("/woolies-store/id/162609")
    assert response.status_code == 200


# def test_woolies_bad_id():
#     """Test the woolies id endpoint with invalid id"""
#     response = client.get("/woolies-store/id/1234567880")
#     assert response.status_code == 500

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

def test_iga_shapes():
    """Test the iga id endpoint with Arnott's shapes"""
    response = client.get("/iga-store/store/32600/id/305099")
    assert response.status_code == 200

def test_woolies_redbull_curr():
    """Test the woolies id endpoint with redbull"""
    response = client.get("/woolies-store/id/162609/")
    assert response.status_code == 200

def test_aldi_milk():
    """Test the aldi url endpoint with milk"""
    response = client.get("/aldi-store/page?product_page=https://www.aldi.com.au/groceries/fresh-produce/dairy-eggs/dairy-eggs-detail/ps/p/farmdale-full-cream-milk-uht-1l/")
    assert response.status_code == 200

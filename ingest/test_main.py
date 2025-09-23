import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_create_coles_product(client):
    product_data = {
        "store": "coles",
        "id": "8909349",
        "name": "Japanese Infusion Salmon Portion",
        "price": 9.50,
        "details": {
            "brand": "Huon",
            "size": "200g",
            "description": "HUON JAPANESE FUSION SALMON 200G",
            "merchandiseHeir": {
                "category": "PREPACKAGED SEAFOOD"
            }
        }
    }
    
    response = client.post("/api/products", json=product_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert data["action"] == "created"
    assert data["matched_existing"] == False
    assert data["product_id"] > 0

def test_create_aldi_product(client):
    product_data = {
        "store": "aldi",
        "id": "123456",
        "name": "Simply Nature Almond Milk",
        "price": 3.99,
        "details": {
            "brand": "Simply Nature",
            "category": "Dairy",
            "weight": "1L",
            "description": "High quality simply nature almond milk"
        }
    }
    
    response = client.post("/api/products", json=product_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert data["action"] == "created"

def test_duplicate_product_matching(client):
    product_data = {
        "store": "coles",
        "id": "8909349",
        "name": "Japanese Infusion Salmon Portion",
        "price": 9.50,
        "details": {
            "brand": "Huon",
            "size": "200g",
            "merchandiseHeir": {
                "category": "PREPACKAGED SEAFOOD"
            }
        }
    }
    
    response1 = client.post("/api/products", json=product_data)
    assert response1.status_code == 200
    first_product_id = response1.json()["product_id"]
    
    similar_product_data = {
        "store": "aldi",
        "id": "999999",
        "name": "Huon Japanese Fusion Salmon 200g",
        "price": 10.00,
        "details": {
            "brand": "Huon",
            "weight": "200g",
            "category": "Seafood"
        }
    }
    
    response2 = client.post("/api/products", json=similar_product_data)
    assert response2.status_code == 200
    
    data2 = response2.json()
    assert data2["matched_existing"] == True
    assert data2["product_id"] == first_product_id

def test_price_update(client):
    product_data = {
        "store": "coles",
        "id": "test123",
        "name": "Test Product",
        "price": 5.00,
        "details": {"brand": "TestBrand"}
    }
    
    response1 = client.post("/api/products", json=product_data)
    assert response1.status_code == 200
    
    product_data["price"] = 6.50
    response2 = client.post("/api/products", json=product_data)
    assert response2.status_code == 200

def test_get_products(client):
    product_data = {
        "store": "coles",
        "id": "test123",
        "name": "Test Product",
        "price": 5.00,
        "details": {"brand": "TestBrand"}
    }
    
    client.post("/api/products", json=product_data)
    
    response = client.get("/api/products")
    assert response.status_code == 200
    
    products = response.json()
    assert len(products) >= 1
    assert products[0]["name"] == "Test Product"
    assert products[0]["store"] == "coles"

def test_get_products_with_filters(client):
    product_data = {
        "store": "coles",
        "id": "test123",
        "name": "Test Product",
        "price": 5.00,
        "details": {"brand": "TestBrand"}
    }
    
    client.post("/api/products", json=product_data)
    
    response = client.get("/api/products?store=coles&limit=10")
    assert response.status_code == 200
    
    products = response.json()
    assert all(product["store"] == "coles" for product in products)

def test_get_product_details(client):
    product_data = {
        "store": "coles",
        "id": "test123",
        "name": "Test Product",
        "price": 5.00,
        "details": {"brand": "TestBrand"}
    }
    
    response = client.post("/api/products", json=product_data)
    product_id = response.json()["product_id"]
    
    response = client.get(f"/api/products/{product_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == "Test Product"
    assert len(data["store_products"]) >= 1
    
    store_product = data["store_products"][0]
    assert store_product["store"] == "coles"
    assert store_product["store_product_id"] == "test123"
    assert store_product["current_price"] == 5.00
    assert len(store_product["price_history"]) >= 1

def test_get_store_product_details(client):
    product_data = {
        "store": "coles",
        "id": "test123",
        "name": "Test Product",
        "price": 5.00,
        "details": {"brand": "TestBrand"}
    }
    
    response = client.post("/api/products", json=product_data)
    product_id = response.json()["product_id"]
    
    response = client.get(f"/api/products/{product_id}/stores/coles")
    assert response.status_code == 200
    
    data = response.json()
    assert data["store"] == "coles"
    assert data["store_product_id"] == "test123"
    assert data["current_price"] == 5.00
    assert len(data["price_history"]) >= 1

def test_get_product_with_multiple_stores(client):
    # Create a product at Coles
    coles_data = {
        "store": "coles",
        "id": "coles123",
        "name": "Multi Store Product",
        "price": 10.00,
        "details": {"brand": "TestBrand"}
    }
    
    response = client.post("/api/products", json=coles_data)
    product_id = response.json()["product_id"]
    
    # Add the same product at ALDI (should match and associate)
    aldi_data = {
        "store": "aldi",
        "id": "aldi456", 
        "name": "Multi Store Product",
        "price": 9.50,
        "details": {"brand": "TestBrand", "weight": "1kg"}
    }
    
    response = client.post("/api/products", json=aldi_data)
    assert response.json()["product_id"] == product_id  # Should match existing product
    
    # Get comprehensive product details
    response = client.get(f"/api/products/{product_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == "Multi Store Product"
    assert len(data["store_products"]) == 2  # Should have both stores
    
    stores = {sp["store"] for sp in data["store_products"]}
    assert "coles" in stores
    assert "aldi" in stores
    
    # Check each store product has price history
    for store_product in data["store_products"]:
        assert len(store_product["price_history"]) >= 1
        assert "raw_details" in store_product
        assert "created_at" in store_product
        assert "updated_at" in store_product

def test_invalid_store(client):
    product_data = {
        "store": "invalid_store",
        "id": "123",
        "name": "Test",
        "price": 1.00,
        "details": {}
    }
    
    response = client.post("/api/products", json=product_data)
    assert response.status_code == 422

def test_negative_price(client):
    product_data = {
        "store": "coles",
        "id": "123",
        "name": "Test",
        "price": -1.00,
        "details": {}
    }
    
    response = client.post("/api/products", json=product_data)
    assert response.status_code == 422

def test_product_not_found(client):
    response = client.get("/api/products/99999")
    assert response.status_code == 404

def test_price_update_endpoint(client):
    # Create a product first
    product_data = {
        "store": "coles",
        "id": "price_update_test",
        "name": "Price Update Test Product",
        "price": 8.00,
        "details": {"brand": "TestBrand"}
    }
    
    response = client.post("/api/products", json=product_data)
    assert response.status_code == 200
    
    # Update the price
    price_update_data = {
        "store": "coles",
        "store_product_id": "price_update_test",
        "new_price": 9.50
    }
    
    response = client.post("/api/price-update", json=price_update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert data["old_price"] == 8.00
    assert data["new_price"] == 9.50
    assert "price_history_id" in data

def test_price_update_product_not_found(client):
    price_update_data = {
        "store": "coles",
        "store_product_id": "non_existent_product",
        "new_price": 15.00
    }
    
    response = client.post("/api/price-update", json=price_update_data)
    assert response.status_code == 404

def test_price_update_same_price(client):
    # Create a product
    product_data = {
        "store": "coles",
        "id": "same_price_test",
        "name": "Same Price Test",
        "price": 7.50,
        "details": {"brand": "TestBrand"}
    }
    
    client.post("/api/products", json=product_data)
    
    # Try to update to the same price
    price_update_data = {
        "store": "coles",
        "store_product_id": "same_price_test",
        "new_price": 7.50
    }
    
    response = client.post("/api/price-update", json=price_update_data)
    assert response.status_code == 400

def test_price_update_creates_history(client):
    # Create a product
    product_data = {
        "store": "coles",
        "id": "history_test",
        "name": "History Test Product", 
        "price": 5.00,
        "details": {"brand": "TestBrand"}
    }
    
    response = client.post("/api/products", json=product_data)
    product_id = response.json()["product_id"]
    
    # Update price multiple times
    prices = [6.00, 7.00, 8.50]
    for price in prices:
        price_update_data = {
            "store": "coles",
            "store_product_id": "history_test",
            "new_price": price
        }
        client.post("/api/price-update", json=price_update_data)
    
    # Check that history was created properly
    response = client.get(f"/api/products/{product_id}")
    assert response.status_code == 200
    
    data = response.json()
    store_product = data["store_products"][0]
    assert store_product["current_price"] == 8.50  # Latest price
    assert len(store_product["price_history"]) == 4  # Original + 3 updates
    
    # Check that the history contains all prices
    price_history = store_product["price_history"]
    prices_in_history = [ph["price"] for ph in price_history]
    expected_prices = {5.0, 6.0, 7.0, 8.5}  # All prices that should be in history
    actual_prices = set(prices_in_history)
    assert expected_prices == actual_prices, f"Expected {expected_prices}, got {actual_prices}"
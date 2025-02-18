import pytest
from pydantic import ValidationError
from schemas import ProductCreateRequest, ProductResponse, ProductInfo, ColesDetails, AldiDetails

class TestProductCreateRequest:
    def test_valid_coles_product(self):
        data = {
            "store": "coles",
            "id": "8909349",
            "name": "Japanese Infusion Salmon Portion",
            "price": 9.50,
            "details": {
                "brand": "Huon",
                "size": "200g"
            }
        }
        
        product = ProductCreateRequest(**data)
        assert product.store == "coles"
        assert product.id == "8909349"
        assert product.name == "Japanese Infusion Salmon Portion"
        assert product.price == 9.50
        assert product.details["brand"] == "Huon"
    
    def test_valid_aldi_product(self):
        data = {
            "store": "ALDI",
            "id": "123456",
            "name": "Simply Nature Almond Milk",
            "price": 3.99,
            "details": {
                "brand": "Simply Nature",
                "category": "Dairy"
            }
        }
        
        product = ProductCreateRequest(**data)
        assert product.store == "aldi"  # Should be normalized to lowercase
    
    def test_invalid_store(self):
        data = {
            "store": "invalid_store",
            "id": "123",
            "name": "Test Product",
            "price": 5.00,
            "details": {}
        }
        
        with pytest.raises(ValidationError) as exc_info:
            ProductCreateRequest(**data)
        
        assert "Store must be one of" in str(exc_info.value)
    
    def test_negative_price(self):
        data = {
            "store": "coles",
            "id": "123",
            "name": "Test Product",
            "price": -1.00,
            "details": {}
        }
        
        with pytest.raises(ValidationError) as exc_info:
            ProductCreateRequest(**data)
        
        assert "greater than or equal to 0" in str(exc_info.value)
    
    def test_price_rounding(self):
        data = {
            "store": "coles",
            "id": "123",
            "name": "Test Product",
            "price": 5.999,
            "details": {}
        }
        
        product = ProductCreateRequest(**data)
        assert product.price == 6.00
    
    def test_missing_required_fields(self):
        data = {
            "store": "coles",
            "name": "Test Product",
            "price": 5.00
            # Missing 'id'
        }
        
        with pytest.raises(ValidationError):
            ProductCreateRequest(**data)
    
    def test_empty_details(self):
        data = {
            "store": "coles",
            "id": "123",
            "name": "Test Product",
            "price": 5.00
            # Details should default to empty dict
        }
        
        product = ProductCreateRequest(**data)
        assert product.details == {}

class TestProductResponse:
    def test_valid_response(self):
        data = {
            "status": "success",
            "product_id": 123,
            "action": "created",
            "matched_existing": False,
            "message": "Product created successfully"
        }
        
        response = ProductResponse(**data)
        assert response.status == "success"
        assert response.product_id == 123
        assert response.action == "created"
        assert response.matched_existing == False
        assert response.message == "Product created successfully"
    
    def test_optional_message(self):
        data = {
            "status": "success",
            "product_id": 123,
            "action": "updated",
            "matched_existing": True
        }
        
        response = ProductResponse(**data)
        assert response.message is None

class TestColesDetails:
    def test_valid_coles_details(self):
        data = {
            "brand": "Huon",
            "size": "200g",
            "description": "HUON JAPANESE FUSION SALMON 200G",
            "merchandiseHeir": {
                "category": "PREPACKAGED SEAFOOD"
            },
            "pricing": {
                "now": 9.5,
                "was": 12,
                "saveAmount": 2.5
            },
            "gtin": "9315896103096"
        }
        
        details = ColesDetails(**data)
        assert details.brand == "Huon"
        assert details.size == "200g"
        assert details.merchandiseHeir["category"] == "PREPACKAGED SEAFOOD"
        assert details.pricing["now"] == 9.5
        assert details.gtin == "9315896103096"
    
    def test_optional_fields(self):
        data = {
            "brand": "Test Brand"
        }
        
        details = ColesDetails(**data)
        assert details.brand == "Test Brand"
        assert details.merchandiseHeir is None
        assert details.pricing is None

class TestAldiDetails:
    def test_valid_aldi_details(self):
        data = {
            "brand": "Simply Nature",
            "category": "Dairy",
            "weight": "1L",
            "ingredients": "Almondmilk (filtered water, almonds), vitamin E",
            "nutrition_facts": {
                "calories_per_serving": 256,
                "fat": "2.3g",
                "sodium": "109mg",
                "protein": "11.4g"
            },
            "barcode": "123456972658",
            "availability": "In Stock",
            "rating": 4.0
        }
        
        details = AldiDetails(**data)
        assert details.brand == "Simply Nature"
        assert details.category == "Dairy"
        assert details.weight == "1L"
        assert details.nutrition_facts["calories_per_serving"] == 256
        assert details.rating == 4.0
    
    def test_optional_fields(self):
        data = {
            "brand": "Test Brand"
        }
        
        details = AldiDetails(**data)
        assert details.brand == "Test Brand"
        assert details.nutrition_facts is None
        assert details.rating is None

class TestProductInfo:
    def test_valid_product_info(self):
        from datetime import datetime
        
        data = {
            "id": 1,
            "name": "Test Product",
            "brand": "Test Brand",
            "category": "test",
            "size": "200g",
            "current_price": 5.99,
            "store": "coles",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        info = ProductInfo(**data)
        assert info.id == 1
        assert info.name == "Test Product"
        assert info.current_price == 5.99
        assert info.store == "coles"
    
    def test_optional_fields(self):
        from datetime import datetime
        
        data = {
            "id": 1,
            "name": "Test Product",
            "current_price": 5.99,
            "store": "coles",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        info = ProductInfo(**data)
        assert info.brand is None
        assert info.category is None
        assert info.size is None
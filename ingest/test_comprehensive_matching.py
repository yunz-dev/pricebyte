import pytest
import json
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, get_db
from main import app

# Configure test verbosity - set to False to run silently
VERBOSE_TESTS = os.getenv("VERBOSE_TESTS", "true").lower() == "true"

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_comprehensive.db"

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

def log_test_action(action, data=None, response=None):
    """Helper function to log test actions when verbose mode is enabled"""
    if not VERBOSE_TESTS:
        return
    
    print(f"\n🔍 {action}")
    if data:
        print(f"📤 Request: {json.dumps(data, indent=2)}")
    if response:
        print(f"📥 Response ({response.status_code}): {json.dumps(response.json(), indent=2)}")

class TestComprehensiveFuzzyMatching:
    """Comprehensive tests for product fuzzy matching with extensive edge cases"""
    
    def test_exact_name_match(self, client):
        """Test exact product name matching"""
        # Create original product
        product1 = {
            "store": "coles",
            "id": "prod1",
            "name": "Organic Free Range Eggs",
            "price": 6.50,
            "details": {"brand": "Farmer Brown", "size": "12 pack"}
        }
        
        log_test_action("Creating original product", product1)
        response1 = client.post("/api/products", json=product1)
        log_test_action("Product created", response=response1)
        
        original_id = response1.json()["product_id"]
        
        # Try identical product at different store
        product2 = {
            "store": "aldi",
            "id": "prod2", 
            "name": "Organic Free Range Eggs",
            "price": 5.99,
            "details": {"brand": "Farmer Brown", "weight": "12pk"}
        }
        
        log_test_action("Creating identical product at different store", product2)
        response2 = client.post("/api/products", json=product2)
        log_test_action("Matching result", response=response2)
        
        assert response2.json()["matched_existing"] == True
        assert response2.json()["product_id"] == original_id
    
    def test_case_insensitive_matching(self, client):
        """Test case insensitive product matching"""
        product1 = {
            "store": "coles",
            "id": "prod1",
            "name": "premium greek yogurt",
            "price": 4.50,
            "details": {"brand": "chobani"}
        }
        
        log_test_action("Creating lowercase product", product1)
        response1 = client.post("/api/products", json=product1)
        original_id = response1.json()["product_id"]
        
        product2 = {
            "store": "woolworths",
            "id": "prod2",
            "name": "PREMIUM GREEK YOGURT",
            "price": 4.25,
            "details": {"brand": "CHOBANI"}
        }
        
        log_test_action("Creating uppercase variant", product2)
        response2 = client.post("/api/products", json=product2)
        log_test_action("Case matching result", response=response2)
        
        assert response2.json()["matched_existing"] == True
        assert response2.json()["product_id"] == original_id
    
    def test_punctuation_variations(self, client):
        """Test matching with different punctuation"""
        product1 = {
            "store": "coles",
            "id": "prod1",
            "name": "Smith's Original Potato Chips",
            "price": 3.50,
            "details": {"brand": "Smith's", "size": "170g"}
        }
        
        log_test_action("Creating product with apostrophe", product1)
        response1 = client.post("/api/products", json=product1)
        original_id = response1.json()["product_id"]
        
        # Test various punctuation variations
        variations = [
            "Smiths Original Potato Chips",  # No apostrophe
            "Smith's, Original Potato Chips!",  # Extra punctuation
            "Smith's - Original Potato Chips",  # Dash
            "Smith's 'Original' Potato Chips"  # Quotes
        ]
        
        for i, variant in enumerate(variations):
            product_variant = {
                "store": "aldi",
                "id": f"variant{i}",
                "name": variant,
                "price": 3.25,
                "details": {"brand": "Smith's", "weight": "170g"}
            }
            
            log_test_action(f"Testing punctuation variant: {variant}", product_variant)
            response = client.post("/api/products", json=product_variant)
            log_test_action("Punctuation matching result", response=response)
            
            assert response.json()["matched_existing"] == True, f"Failed to match variant: {variant}"
            assert response.json()["product_id"] == original_id
    
    def test_size_format_variations(self, client):
        """Test matching with different size format representations"""
        product1 = {
            "store": "coles",
            "id": "prod1",
            "name": "Fresh Milk",
            "price": 3.20,
            "details": {"brand": "Dairy Farmers", "size": "2L"}
        }
        
        log_test_action("Creating product with 2L size", product1)
        response1 = client.post("/api/products", json=product1)
        original_id = response1.json()["product_id"]
        
        # Test size variations that should match
        size_variations = [
            ("2000ml", "2000ml"),
            ("2 litres", "2 litres"),
            ("2.0L", "2.0L"),
            ("2000ML", "2000ML")
        ]
        
        for i, (size_variant, display_size) in enumerate(size_variations):
            product_variant = {
                "store": "aldi",
                "id": f"size_var_{i}",
                "name": "Fresh Milk",
                "price": 3.10,
                "details": {"brand": "Dairy Farmers", "size": size_variant}
            }
            
            log_test_action(f"Testing size variant: {display_size}", product_variant)
            response = client.post("/api/products", json=product_variant)
            log_test_action("Size matching result", response=response)
            
            assert response.json()["matched_existing"] == True, f"Failed to match size variant: {size_variant}"
            assert response.json()["product_id"] == original_id
    
    def test_weight_unit_conversions(self, client):
        """Test matching products with different but equivalent weight units"""
        product1 = {
            "store": "coles",
            "id": "prod1",
            "name": "Premium Pasta",
            "price": 2.50,
            "details": {"brand": "Barilla", "size": "500g"}
        }
        
        log_test_action("Creating product with 500g", product1)
        response1 = client.post("/api/products", json=product1)
        original_id = response1.json()["product_id"]
        
        # Test weight conversion (0.5kg should match 500g)
        product2 = {
            "store": "woolworths",
            "id": "prod2",
            "name": "Premium Pasta",
            "price": 2.45,
            "details": {"brand": "Barilla", "size": "0.5kg"}
        }
        
        log_test_action("Testing 0.5kg conversion", product2)
        response2 = client.post("/api/products", json=product2)
        log_test_action("Weight conversion result", response=response2)
        
        assert response2.json()["matched_existing"] == True
        assert response2.json()["product_id"] == original_id
    
    def test_word_order_variations(self, client):
        """Test matching with different word orders"""
        product1 = {
            "store": "coles",
            "id": "prod1",
            "name": "Red Delicious Apples Fresh",
            "price": 4.90,
            "details": {"brand": "Local Farm"}
        }
        
        log_test_action("Creating product with original word order", product1)
        response1 = client.post("/api/products", json=product1)
        original_id = response1.json()["product_id"]
        
        # Test different word orders
        word_variations = [
            "Fresh Red Delicious Apples",
            "Delicious Red Apples Fresh", 
            "Apples Red Delicious Fresh"
        ]
        
        for i, variant in enumerate(word_variations):
            product_variant = {
                "store": "aldi",
                "id": f"word_order_{i}",
                "name": variant,
                "price": 4.50,
                "details": {"brand": "Local Farm"}
            }
            
            log_test_action(f"Testing word order: {variant}", product_variant)
            response = client.post("/api/products", json=product_variant)
            log_test_action("Word order matching result", response=response)
            
            assert response.json()["matched_existing"] == True, f"Failed to match word order: {variant}"
            assert response.json()["product_id"] == original_id
    
    def test_brand_name_variations(self, client):
        """Test brand name matching with variations"""
        product1 = {
            "store": "coles",
            "id": "prod1",
            "name": "Chocolate Chip Cookies",
            "price": 3.50,
            "details": {"brand": "Arnott's", "size": "250g"}
        }
        
        log_test_action("Creating product with Arnott's brand", product1)
        response1 = client.post("/api/products", json=product1)
        original_id = response1.json()["product_id"]
        
        # Should match - same brand different format
        product2 = {
            "store": "woolworths",
            "id": "prod2",
            "name": "Chocolate Chip Cookies",
            "price": 3.25,
            "details": {"brand": "Arnotts", "weight": "250g"}  # No apostrophe
        }
        
        log_test_action("Testing brand without apostrophe", product2)
        response2 = client.post("/api/products", json=product2)
        log_test_action("Brand variation result", response=response2)
        
        # This might not match due to strict brand comparison, but let's see
        # The test will tell us how the matching behaves
        if VERBOSE_TESTS:
            print(f"Brand matching behavior: matched={response2.json()['matched_existing']}")
    
    def test_different_brands_no_match(self, client):
        """Test that different brands don't match even with similar names"""
        product1 = {
            "store": "coles",
            "id": "prod1",
            "name": "Vanilla Ice Cream",
            "price": 5.50,
            "details": {"brand": "Ben & Jerry's", "size": "458ml"}
        }
        
        log_test_action("Creating Ben & Jerry's product", product1)
        response1 = client.post("/api/products", json=product1)
        original_id = response1.json()["product_id"]
        
        # Different brand - should NOT match
        product2 = {
            "store": "aldi",
            "id": "prod2",
            "name": "Vanilla Ice Cream",
            "price": 3.99,
            "details": {"brand": "Häagen-Dazs", "size": "458ml"}
        }
        
        log_test_action("Testing different brand (should not match)", product2)
        response2 = client.post("/api/products", json=product2)
        log_test_action("Different brand result", response=response2)
        
        assert response2.json()["matched_existing"] == False
        assert response2.json()["product_id"] != original_id
    
    def test_similar_but_different_products(self, client):
        """Test products that are similar but should not match"""
        product1 = {
            "store": "coles",
            "id": "prod1",
            "name": "iPhone 15 Pro Max",
            "price": 1899.00,
            "details": {"brand": "Apple", "size": "256GB"}
        }
        
        log_test_action("Creating iPhone 15 Pro Max", product1)
        response1 = client.post("/api/products", json=product1)
        original_id = response1.json()["product_id"]
        
        # Similar but different products that should NOT match
        different_products = [
            ("iPhone 15 Pro", "Different model"),
            ("iPhone 15 Pro Max", "Different storage", "512GB"),
            ("Samsung Galaxy S24 Ultra", "Different brand", "256GB")
        ]
        
        for i, product_info in enumerate(different_products):
            name = product_info[0]
            reason = product_info[1]
            size = product_info[2] if len(product_info) > 2 else "256GB"
            brand = "Samsung" if "Samsung" in name else "Apple"
            
            different_product = {
                "store": "aldi",
                "id": f"different_{i}",
                "name": name,
                "price": 1799.00,
                "details": {"brand": brand, "size": size}
            }
            
            log_test_action(f"Testing different product: {name} ({reason})", different_product)
            response = client.post("/api/products", json=different_product)
            log_test_action("Different product result", response=response)
            
            # These should not match the original
            assert response.json()["matched_existing"] == False, f"Incorrectly matched different product: {name}"
    
    def test_typos_and_misspellings(self, client):
        """Test matching with minor typos and misspellings"""
        product1 = {
            "store": "coles",
            "id": "prod1",
            "name": "Strawberry Yoghurt",
            "price": 1.80,
            "details": {"brand": "Yoplait", "size": "175g"}
        }
        
        log_test_action("Creating product with 'Yoghurt' spelling", product1)
        response1 = client.post("/api/products", json=product1)
        original_id = response1.json()["product_id"]
        
        # American spelling
        product2 = {
            "store": "woolworths",
            "id": "prod2",
            "name": "Strawberry Yogurt",  # Different spelling
            "price": 1.75,
            "details": {"brand": "Yoplait", "weight": "175g"}
        }
        
        log_test_action("Testing American spelling 'Yogurt'", product2)
        response2 = client.post("/api/products", json=product2)
        log_test_action("Spelling variation result", response=response2)
        
        # Should match despite spelling difference
        assert response2.json()["matched_existing"] == True
        assert response2.json()["product_id"] == original_id
    
    def test_extra_words_and_descriptors(self, client):
        """Test matching when products have extra descriptive words"""
        product1 = {
            "store": "coles",
            "id": "prod1",
            "name": "Bread White",
            "price": 2.80,
            "details": {"brand": "Tip Top", "size": "680g"}
        }
        
        log_test_action("Creating simple bread product", product1)
        response1 = client.post("/api/products", json=product1)
        original_id = response1.json()["product_id"]
        
        # More descriptive version
        product2 = {
            "store": "aldi",
            "id": "prod2",
            "name": "Premium Fresh Baked White Sandwich Bread",
            "price": 2.50,
            "details": {"brand": "Tip Top", "weight": "680g"}
        }
        
        log_test_action("Testing product with extra descriptors", product2)
        response2 = client.post("/api/products", json=product2)
        log_test_action("Extra words matching result", response=response2)
        
        # Should match core product despite extra words
        assert response2.json()["matched_existing"] == True
        assert response2.json()["product_id"] == original_id
    
    def test_category_normalization(self, client):
        """Test that category normalization works across stores"""
        product1 = {
            "store": "coles",
            "id": "prod1",
            "name": "Atlantic Salmon Fillet",
            "price": 28.90,
            "details": {
                "brand": "Huon",
                "size": "1kg",
                "merchandiseHeir": {"category": "PREPACKAGED SEAFOOD"}
            }
        }
        
        log_test_action("Creating Coles seafood product", product1)
        response1 = client.post("/api/products", json=product1)
        original_id = response1.json()["product_id"]
        
        # ALDI with different category format
        product2 = {
            "store": "aldi",
            "id": "prod2",
            "name": "Atlantic Salmon Fillet",
            "price": 26.50,
            "details": {
                "brand": "Huon",
                "weight": "1kg",
                "category": "Seafood"  # Different format but same category
            }
        }
        
        log_test_action("Testing ALDI seafood with different category format", product2)
        response2 = client.post("/api/products", json=product2)
        log_test_action("Category normalization result", response=response2)
        
        assert response2.json()["matched_existing"] == True
        assert response2.json()["product_id"] == original_id
    
    def test_threshold_edge_cases(self, client):
        """Test products that are right at the similarity threshold"""
        product1 = {
            "store": "coles",
            "id": "prod1",
            "name": "Original Recipe Chicken",
            "price": 12.90,
            "details": {"brand": "KFC", "size": "3 pieces"}
        }
        
        log_test_action("Creating original chicken product", product1)
        response1 = client.post("/api/products", json=product1)
        original_id = response1.json()["product_id"]
        
        # Test products with varying similarity levels
        similarity_tests = [
            ("Original Recipe Chicken Pieces", "Should match - very similar"),
            ("Original Chicken Recipe", "Should match - word reorder"),
            ("Spicy Recipe Chicken", "May not match - different descriptor"),
            ("Original Recipe Beef", "Should not match - different protein")
        ]
        
        for i, (test_name, expectation) in enumerate(similarity_tests):
            test_product = {
                "store": "aldi",
                "id": f"threshold_{i}",
                "name": test_name,
                "price": 11.90,
                "details": {"brand": "KFC", "size": "3 pieces"}
            }
            
            log_test_action(f"Testing threshold case: {test_name} ({expectation})", test_product)
            response = client.post("/api/products", json=test_product)
            log_test_action("Threshold test result", response=response)
            
            if VERBOSE_TESTS:
                print(f"Similarity result for '{test_name}': matched={response.json()['matched_existing']}")
    
    def test_no_brand_products(self, client):
        """Test matching for products without brand information"""
        product1 = {
            "store": "coles",
            "id": "prod1",
            "name": "Organic Bananas",
            "price": 4.90,
            "details": {"size": "1kg"}  # No brand
        }
        
        log_test_action("Creating product without brand", product1)
        response1 = client.post("/api/products", json=product1)
        original_id = response1.json()["product_id"]
        
        product2 = {
            "store": "aldi",
            "id": "prod2",
            "name": "Organic Bananas",
            "price": 4.50,
            "details": {"weight": "1kg"}  # Also no brand
        }
        
        log_test_action("Testing matching without brands", product2)
        response2 = client.post("/api/products", json=product2)
        log_test_action("No brand matching result", response=response2)
        
        assert response2.json()["matched_existing"] == True
        assert response2.json()["product_id"] == original_id
    
    def test_complex_multi_store_scenario(self, client):
        """Test complex scenario with multiple stores and price updates"""
        # Create original product at Coles
        coles_product = {
            "store": "coles",
            "id": "complex_1",
            "name": "Premium Greek Style Yoghurt Natural",
            "price": 6.50,
            "details": {"brand": "Chobani", "size": "900g"}
        }
        
        log_test_action("Creating complex multi-store test - Coles product", coles_product)
        response1 = client.post("/api/products", json=coles_product)
        product_id = response1.json()["product_id"]
        
        # Add same product at ALDI (should match)
        aldi_product = {
            "store": "aldi",
            "id": "complex_2",
            "name": "Premium Greek Style Natural Yoghurt",  # Slightly different order
            "price": 5.99,
            "details": {"brand": "Chobani", "weight": "900g"}
        }
        
        log_test_action("Adding matching product at ALDI", aldi_product)
        response2 = client.post("/api/products", json=aldi_product)
        log_test_action("ALDI matching result", response=response2)
        
        assert response2.json()["matched_existing"] == True
        assert response2.json()["product_id"] == product_id
        
        # Add at Woolworths (should also match)
        woolworths_product = {
            "store": "woolworths",
            "id": "complex_3",
            "name": "Chobani Greek Yoghurt Natural Premium",  # Different word order
            "price": 6.25,
            "details": {"brand": "Chobani", "size": "900g"}
        }
        
        log_test_action("Adding matching product at Woolworths", woolworths_product)
        response3 = client.post("/api/products", json=woolworths_product)
        log_test_action("Woolworths matching result", response=response3)
        
        assert response3.json()["matched_existing"] == True
        assert response3.json()["product_id"] == product_id
        
        # Test price update
        price_update = {
            "store": "coles",
            "store_product_id": "complex_1",
            "new_price": 7.50
        }
        
        log_test_action("Testing price update", price_update)
        price_response = client.post("/api/price-update", json=price_update)
        log_test_action("Price update result", response=price_response)
        
        assert price_response.status_code == 200
        assert price_response.json()["old_price"] == 6.50
        assert price_response.json()["new_price"] == 7.50
        
        # Get comprehensive product details
        log_test_action("Getting comprehensive product details")
        details_response = client.get(f"/api/products/{product_id}")
        log_test_action("Product details", response=details_response)
        
        details = details_response.json()
        assert len(details["store_products"]) == 3  # All three stores
        
        # Check that Coles has price history with the update
        coles_store_product = next(sp for sp in details["store_products"] if sp["store"] == "coles")
        assert coles_store_product["current_price"] == 7.50
        assert len(coles_store_product["price_history"]) >= 2  # Original + updated price

class TestPriceUpdateEndpoint:
    """Comprehensive tests for the price update endpoint"""
    
    def test_successful_price_update(self, client):
        """Test successful price update"""
        # Create a product first
        product = {
            "store": "coles",
            "id": "price_test_1",
            "name": "Test Product",
            "price": 10.00,
            "details": {"brand": "TestBrand"}
        }
        
        log_test_action("Creating product for price update test", product)
        response = client.post("/api/products", json=product)
        
        # Update the price
        price_update = {
            "store": "coles",
            "store_product_id": "price_test_1",
            "new_price": 12.50
        }
        
        log_test_action("Updating price", price_update)
        update_response = client.post("/api/price-update", json=price_update)
        log_test_action("Price update response", response=update_response)
        
        assert update_response.status_code == 200
        result = update_response.json()
        assert result["status"] == "success"
        assert result["old_price"] == 10.00
        assert result["new_price"] == 12.50
    
    def test_price_update_not_found(self, client):
        """Test price update for non-existent product"""
        price_update = {
            "store": "coles",
            "store_product_id": "non_existent",
            "new_price": 15.00
        }
        
        log_test_action("Testing price update for non-existent product", price_update)
        response = client.post("/api/price-update", json=price_update)
        log_test_action("Non-existent product response", response=response)
        
        assert response.status_code == 404
    
    def test_same_price_update(self, client):
        """Test updating to the same price (should fail)"""
        # Create a product
        product = {
            "store": "coles",
            "id": "same_price_test",
            "name": "Same Price Test",
            "price": 5.00,
            "details": {"brand": "TestBrand"}
        }
        
        log_test_action("Creating product for same price test", product)
        client.post("/api/products", json=product)
        
        # Try to update to same price
        price_update = {
            "store": "coles",
            "store_product_id": "same_price_test",
            "new_price": 5.00
        }
        
        log_test_action("Testing same price update (should fail)", price_update)
        response = client.post("/api/price-update", json=price_update)
        log_test_action("Same price response", response=response)
        
        assert response.status_code == 400
    
    def test_negative_price_update(self, client):
        """Test updating to negative price (should fail validation)"""
        price_update = {
            "store": "coles",
            "store_product_id": "any_id",
            "new_price": -5.00
        }
        
        log_test_action("Testing negative price update (should fail)", price_update)
        response = client.post("/api/price-update", json=price_update)
        log_test_action("Negative price response", response=response)
        
        assert response.status_code == 422  # Validation error

def run_verbose_summary():
    """Print summary of what verbose mode shows"""
    if VERBOSE_TESTS:
        print("\n" + "="*80)
        print("🔍 VERBOSE TEST MODE ENABLED")
        print("="*80)
        print("This mode shows:")
        print("📤 Request data being sent to endpoints")
        print("📥 Response data received from endpoints") 
        print("🔍 Test actions and their purposes")
        print("🧪 Fuzzy matching behavior and results")
        print("\nTo run tests silently, set VERBOSE_TESTS=false")
        print("Example: VERBOSE_TESTS=false pytest test_comprehensive_matching.py")
        print("="*80)

if __name__ == "__main__":
    run_verbose_summary()
# Grocery Product Data Consolidation System - Quick Tutorial

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Initialize Database
```bash
python3 -c "from models import create_tables; create_tables()"
```

### 3. Start Server
```bash
python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 4. Open API Documentation
Visit: http://127.0.0.1:8000/docs

---

## 📝 API Endpoints Guide

### Create/Update Products
**POST /api/products**

```bash
# Create a Coles product
curl -X POST "http://127.0.0.1:8000/api/products" \
  -H "Content-Type: application/json" \
  -d '{
    "store": "coles",
    "id": "8909349",
    "name": "Japanese Infusion Salmon Portion",
    "price": 9.50,
    "details": {
      "brand": "Huon",
      "size": "200g",
      "description": "Premium salmon fillet"
    }
  }'
```

```bash
# Add same product at ALDI (will auto-match)
curl -X POST "http://127.0.0.1:8000/api/products" \
  -H "Content-Type: application/json" \
  -d '{
    "store": "aldi",
    "id": "aldi123",
    "name": "Huon Japanese Fusion Salmon",
    "price": 8.99,
    "details": {
      "brand": "Huon",
      "weight": "200g"
    }
  }'
```

### Update Product Price
**POST /api/price-update**

```bash
# Update price for specific store product
curl -X POST "http://127.0.0.1:8000/api/price-update" \
  -H "Content-Type: application/json" \
  -d '{
    "store": "coles",
    "store_product_id": "8909349",
    "new_price": 10.50
  }'
```

### Get All Products
**GET /api/products**

```bash
# Get all products
curl -X GET "http://127.0.0.1:8000/api/products"

# Filter by store
curl -X GET "http://127.0.0.1:8000/api/products?store=coles&limit=10"

# Filter by category
curl -X GET "http://127.0.0.1:8000/api/products?category=seafood"
```

### Get Comprehensive Product Details
**GET /api/products/{id}**

```bash
# Get product with ALL store associations and price history
curl -X GET "http://127.0.0.1:8000/api/products/1" | python3 -m json.tool
```

### Get Store-Specific Product Details
**GET /api/products/{id}/stores/{store}**

```bash
# Get product details for specific store only
curl -X GET "http://127.0.0.1:8000/api/products/1/stores/coles"
```

---

## 🧪 Testing Guide

### Run All Tests
```bash
# Quick test run
python3 -m pytest -v

# Detailed output
python3 -m pytest -v --tb=short

# Just test summaries
python3 -m pytest -v --tb=no
```

### Run Specific Test Categories
```bash
# API endpoint tests
python3 -m pytest test_main.py -v

# Fuzzy matching tests  
python3 -m pytest test_matcher.py -v

# Data processor tests
python3 -m pytest test_processors.py -v

# Database model tests
python3 -m pytest test_models.py -v

# Schema validation tests
python3 -m pytest test_schemas.py -v
```

### Comprehensive Fuzzy Matching Tests

#### Verbose Mode (See All Requests/Responses)
```bash
# See detailed test actions and API calls
VERBOSE_TESTS=true python3 -m pytest test_comprehensive_matching.py -v -s
```

#### Quiet Mode (Just Pass/Fail)
```bash
# Clean test results only
VERBOSE_TESTS=false python3 -m pytest test_comprehensive_matching.py -v
```

#### Test Specific Scenarios
```bash
# Test exact name matching
VERBOSE_TESTS=true python3 -m pytest test_comprehensive_matching.py::TestComprehensiveFuzzyMatching::test_exact_name_match -v -s

# Test punctuation variations
VERBOSE_TESTS=true python3 -m pytest test_comprehensive_matching.py::TestComprehensiveFuzzyMatching::test_punctuation_variations -v -s

# Test complex multi-store scenario
VERBOSE_TESTS=true python3 -m pytest test_comprehensive_matching.py::TestComprehensiveFuzzyMatching::test_complex_multi_store_scenario -v -s
```

---

## 🏪 Supported Store Formats

### Coles Format
```json
{
  "store": "coles",
  "id": "8909349",
  "name": "Product Name",
  "price": 9.50,
  "details": {
    "brand": "Brand Name",
    "size": "200g",
    "description": "Product description",
    "merchandiseHeir": {
      "category": "PRODUCT CATEGORY"
    },
    "images": [{"full": {"path": "/image.jpg"}}]
  }
}
```

### ALDI Format
```json
{
  "store": "aldi",
  "id": "aldi123",
  "name": "Product Name",
  "price": 8.99,
  "details": {
    "brand": "Brand Name",
    "weight": "200g",
    "category": "Category",
    "nutrition_facts": {
      "calories_per_serving": 256
    }
  }
}
```

### Woolworths Format
```json
{
  "store": "woolworths",
  "id": "wool456",
  "name": "Product Name", 
  "price": 9.25,
  "details": {
    "brand": "Brand Name",
    "size": "200g",
    "category": "Category"
  }
}
```

---

## 🎯 Fuzzy Matching Examples

### ✅ These Will Match
```bash
# Same product, different punctuation
"Smith's Original Chips" ↔ "Smiths Original Chips"

# Different word order
"Greek Style Yogurt Premium" ↔ "Premium Greek Style Yogurt"

# Size format variations
"2L" ↔ "2000ml" ↔ "2 litres"

# Weight conversions
"500g" ↔ "0.5kg"

# Case variations (with same brand)
"premium yogurt" ↔ "PREMIUM YOGURT"
```

### ❌ These Won't Match
```bash
# Different brands
"Ben & Jerry's Ice Cream" ↔ "Häagen-Dazs Ice Cream"

# Very different products
"iPhone 15 Pro" ↔ "Samsung Galaxy S24"

# Too many different words
"Bread" ↔ "Premium Artisan Sourdough Bread with Seeds"
```

---

## 📊 Response Examples

### Product Creation Response
```json
{
  "status": "success",
  "product_id": 1,
  "action": "created",
  "matched_existing": false,
  "message": "Product created successfully"
}
```

### Product Matching Response
```json
{
  "status": "success", 
  "product_id": 1,
  "action": "updated",
  "matched_existing": true,
  "message": "Product updated successfully"
}
```

### Price Update Response
```json
{
  "status": "success",
  "message": "Price updated from $9.50 to $10.50",
  "store_product_id": 1,
  "old_price": 9.50,
  "new_price": 10.50,
  "price_history_id": 5
}
```

### Comprehensive Product Response
```json
{
  "id": 1,
  "name": "Japanese Infusion Salmon Portion",
  "brand": "Huon",
  "category": "seafood",
  "size": "200g",
  "store_products": [
    {
      "id": 1,
      "store": "coles",
      "store_product_id": "8909349",
      "current_price": 10.50,
      "price_history": [
        {"price": 9.50, "start_date": "2025-09-24", "end_date": "2025-09-24"},
        {"price": 10.50, "start_date": "2025-09-24", "end_date": null}
      ]
    },
    {
      "id": 2,
      "store": "aldi", 
      "store_product_id": "aldi123",
      "current_price": 8.99,
      "price_history": [
        {"price": 8.99, "start_date": "2025-09-24", "end_date": null}
      ]
    }
  ]
}
```

---

## 🔧 Configuration

### Environment Variables
```bash
# Database URL (default: sqlite:///./database.db)
export DATABASE_URL="sqlite:///./database.db"

# Similarity threshold for matching (default: 0.8)
export SIMILARITY_THRESHOLD="0.8"

# Test verbosity (default: true)
export VERBOSE_TESTS="true"
```

### Supported Stores
- `coles`
- `aldi`  
- `woolworths`

---

## 🚨 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Kill existing process
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --port 8001
```

#### 2. Database Locked
```bash
# Remove database and recreate
rm database.db
python3 -c "from models import create_tables; create_tables()"
```

#### 3. Dependencies Not Installing
```bash
# Use pip3 specifically
pip3 install -r requirements.txt

# Or create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. Tests Failing with Import Errors
```bash
# Make sure you're in the correct directory
cd /path/to/ingest
export PYTHONPATH="."
python3 -m pytest
```

### Debug Mode
```bash
# Run server with debug info
uvicorn main:app --reload --log-level debug

# Run tests with verbose output
python3 -m pytest -v -s --tb=long
```

---

## 📈 Performance Tips

### Database Optimization
```bash
# For production, consider PostgreSQL
export DATABASE_URL="postgresql://user:pass@localhost/grocery_db"
```

### Batch Operations
```bash
# Create multiple products in sequence
for i in {1..10}; do
  curl -X POST "http://127.0.0.1:8000/api/products" \
    -H "Content-Type: application/json" \
    -d "{\"store\":\"coles\",\"id\":\"prod$i\",\"name\":\"Product $i\",\"price\":$(($i + 5)).99,\"details\":{\"brand\":\"TestBrand\"}}"
done
```

### Monitor Performance
```bash
# Check server logs
tail -f uvicorn.log

# Monitor database size
ls -lh database.db
```

---

## 🔗 API Documentation

**Interactive API Docs:** http://127.0.0.1:8000/docs
**OpenAPI Schema:** http://127.0.0.1:8000/openapi.json

---

This system provides intelligent product matching across grocery stores with comprehensive price tracking and extensive testing coverage!
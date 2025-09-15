# API Tests for Spring Boot CRUD Application

## Prerequisites
- Start the Spring Boot application
- Ensure the database is running and connected
- Default server should be running on `http://localhost:8080`

## Overview
This API provides comprehensive CRUD operations for:
- **Products** - Main product information
- **Store Products** - Product availability and pricing at different stores  
- **Price History** - Historical price tracking with automatic creation

### Key Features:
- ✅ Automatic price history creation when adding products
- ✅ Smart price updates (extend dates for same price, new records for different prices)
- ✅ Full CRUD operations for all entities
- ✅ Comprehensive search and filtering
- ✅ Proper error handling and JSON responses

## Test Cases for POST /product/

### Test 1: Create Product with Multiple Store Products
```bash
curl -X POST http://localhost:8080/product/ \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "name": "Coca Cola Classic",
    "brand": "Coca Cola",
    "category": "Beverages",
    "size": 1.25,
    "unit": "L",
    "imageUrl": "https://example.com/coke.jpg",
    "description": "Classic Coca Cola soft drink",
    "storeProducts": [
      {
        "id": 1,
        "store": "Coles",
        "standardPrice": 3.50,
        "productUrl": "https://coles.com.au/product/coke-125l",
        "isActive": true
      },
      {
        "id": 2,
        "store": "Woolworths",
        "standardPrice": 3.80,
        "productUrl": "https://woolworths.com.au/product/coke-125l",
        "isActive": true
      },
      {
        "id": 3,
        "store": "IGA",
        "standardPrice": 4.00,
        "productUrl": "https://iga.com.au/product/coke-125l",
        "isActive": false
      }
    ]
  }'
```

### Test 2: Create Product with Single Store Product
```bash
curl -X POST http://localhost:8080/product/ \
  -H "Content-Type: application/json" \
  -d '{
    "id": 2,
    "name": "Bread White Tip Top",
    "brand": "Tip Top",
    "category": "Bakery",
    "size": 680.0,
    "unit": "g",
    "imageUrl": "https://example.com/bread.jpg",
    "description": "Fresh white bread loaf",
    "storeProducts": [
      {
        "id": 4,
        "store": "Coles",
        "standardPrice": 2.80,
        "productUrl": "https://coles.com.au/product/tiptop-bread",
        "isActive": true
      }
    ]
  }'
```

### Test 3: Create Product with No Store Products
```bash
curl -X POST http://localhost:8080/product/ \
  -H "Content-Type: application/json" \
  -d '{
    "id": 3,
    "name": "Generic Milk",
    "brand": "Home Brand",
    "category": "Dairy",
    "size": 2.0,
    "unit": "L",
    "imageUrl": "https://example.com/milk.jpg",
    "description": "Fresh full cream milk",
    "storeProducts": []
  }'
```

### Test 4: Create Product with Null Store Products
```bash
curl -X POST http://localhost:8080/product/ \
  -H "Content-Type: application/json" \
  -d '{
    "id": 4,
    "name": "Organic Bananas",
    "brand": "Nature Way",
    "category": "Fresh Produce", 
    "size": 1.0,
    "unit": "kg",
    "imageUrl": "https://example.com/bananas.jpg",
    "description": "Fresh organic bananas"
  }'
```

### Test 5: Create Product with Mixed Active/Inactive Store Products
```bash
curl -X POST http://localhost:8080/product/ \
  -H "Content-Type: application/json" \
  -d '{
    "id": 5,
    "name": "Tim Tam Original",
    "brand": "Arnott'\''s",
    "category": "Snacks",
    "size": 200.0,
    "unit": "g",
    "imageUrl": "https://example.com/timtam.jpg",
    "description": "Chocolate biscuit with chocolate cream filling",
    "storeProducts": [
      {
        "id": 5,
        "store": "Coles",
        "standardPrice": 3.50,
        "productUrl": "https://coles.com.au/product/timtam-original",
        "isActive": true
      },
      {
        "id": 6,
        "store": "Woolworths",
        "standardPrice": 3.60,
        "productUrl": "https://woolworths.com.au/product/timtam-original",
        "isActive": true
      },
      {
        "id": 7,
        "store": "7-Eleven",
        "standardPrice": 5.00,
        "productUrl": "https://7eleven.com.au/product/timtam",
        "isActive": false
      }
    ]
  }'
```

## Test Cases for GET /product/

### Test 6: Get All Products
```bash
curl -X GET http://localhost:8080/product/ \
  -H "Accept: application/json"
```

## Expected Response Format

The POST endpoint should return a Product object like:
```json
{
  "id": 1,
  "name": "Coca Cola Classic",
  "brand": "Coca Cola",
  "category": "Beverages",
  "size": 1.25,
  "unit": "L",
  "imageUrl": "https://example.com/coke.jpg",
  "description": "Classic Coca Cola soft drink",
  "storeProducts": null
}
```

Note: The returned Product will have an auto-generated `id` and the `storeProducts` field will be `null` in the response (since it uses LAZY loading). To see the store products, you would need a separate endpoint that fetches the product with its store products.

## Testing Tips

1. **Check Database**: After each POST request, verify that both the product and store_product tables have the expected records
2. **Validation**: Try sending invalid data (missing required fields, null values) to test validation
3. **Duplicate Products**: Test creating products with the same name but different details
4. **Large Data**: Test with many store products to ensure performance is acceptable
5. **Special Characters**: Test with product names containing special characters or unicode

## Error Testing

### Test 7: Missing Required Field
```bash
curl -X POST http://localhost:8080/product/ \
  -H "Content-Type: application/json" \
  -d '{
    "id": 6,
    "brand": "Test Brand",
    "category": "Test Category",
    "size": 1.0,
    "unit": "kg"
  }'
```

### Test 8: Invalid JSON
```bash
curl -X POST http://localhost:8080/product/ \
  -H "Content-Type: application/json" \
  -d '{
    "id": 7,
    "name": "Test Product",
    "brand": "Test Brand"
    "category": "Test Category"
  }'
```

---

# 🆕 COMPREHENSIVE API ENDPOINTS

## 🛍️ Product Endpoints

### GET /product/ - Get All Products
```bash
curl -X GET http://localhost:8080/product/ -H "Accept: application/json"
```

### GET /product/{id} - Get Product by ID
```bash
curl -X GET http://localhost:8080/product/1 -H "Accept: application/json"
```

### GET /product/category/{category} - Get Products by Category
```bash
curl -X GET http://localhost:8080/product/category/Beverages -H "Accept: application/json"
```

### GET /product/brand/{brand} - Get Products by Brand
```bash
curl -X GET http://localhost:8080/product/brand/Coca%20Cola -H "Accept: application/json"
```

### GET /product/search?name={name} - Search Products by Name
```bash
curl -X GET "http://localhost:8080/product/search?name=coca" -H "Accept: application/json"
```

### PUT /product/{id} - Update Product
```bash
curl -X PUT http://localhost:8080/product/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Product Name",
    "brand": "Updated Brand",
    "category": "Updated Category",
    "size": 2.0,
    "unit": "L",
    "imageUrl": "https://example.com/updated.jpg",
    "description": "Updated description"
  }'
```

### DELETE /product/{id} - Delete Product
```bash
curl -X DELETE http://localhost:8080/product/1
```

## 💰 Price Update Endpoint

### PUT /product/price - Update Store Product Price
**✨ Smart Price Management:**
- Same price → Extends end date
- Different price → Creates new price history record

```bash
curl -X PUT http://localhost:8080/product/price \
  -H "Content-Type: application/json" \
  -d '{
    "productId": 1,
    "store": "Coles",
    "newPrice": 4.50
  }'
```

## 🏪 Store Product Endpoints

### GET /store-product/ - Get All Store Products
```bash
curl -X GET http://localhost:8080/store-product/ -H "Accept: application/json"
```

### GET /store-product/{id} - Get Store Product by ID
```bash
curl -X GET http://localhost:8080/store-product/1 -H "Accept: application/json"
```

### POST /store-product/ - Create Store Product
```bash
curl -X POST http://localhost:8080/store-product/ \
  -H "Content-Type: application/json" \
  -d '{
    "store": "Aldi",
    "standardPrice": 2.99,
    "productUrl": "https://aldi.com.au/product/test",
    "isActive": true
  }'
```

### PUT /store-product/{id} - Update Store Product
```bash
curl -X PUT http://localhost:8080/store-product/1 \
  -H "Content-Type: application/json" \
  -d '{
    "store": "Aldi",
    "standardPrice": 3.49,
    "productUrl": "https://aldi.com.au/product/updated",
    "isActive": true
  }'
```

### DELETE /store-product/{id} - Delete Store Product
```bash
curl -X DELETE http://localhost:8080/store-product/1
```

## 📈 Price History Endpoints

### GET /price-history/ - Get All Price Histories
```bash
curl -X GET http://localhost:8080/price-history/ -H "Accept: application/json"
```

### GET /price-history/{id} - Get Price History by ID
```bash
curl -X GET http://localhost:8080/price-history/1 -H "Accept: application/json"
```

### GET /price-history/store-product/{storeProductId} - Get Price History for Store Product
```bash
curl -X GET http://localhost:8080/price-history/store-product/1 -H "Accept: application/json"
```

### GET /price-history/store-product/{storeProductId}/current - Get Current Price
**Get current price for today:**
```bash
curl -X GET http://localhost:8080/price-history/store-product/1/current -H "Accept: application/json"
```

**Get price for specific date:**
```bash
curl -X GET "http://localhost:8080/price-history/store-product/1/current?date=2024-01-15" -H "Accept: application/json"
```

### POST /price-history/ - Create Price History
```bash
curl -X POST http://localhost:8080/price-history/ \
  -H "Content-Type: application/json" \
  -d '{
    "startDate": "2024-01-01",
    "endDate": "2024-01-31",
    "price": 3.99
  }'
```

### PUT /price-history/{id} - Update Price History
```bash
curl -X PUT http://localhost:8080/price-history/1 \
  -H "Content-Type: application/json" \
  -d '{
    "startDate": "2024-01-01",
    "endDate": "2024-02-15",
    "price": 4.29
  }'
```

### DELETE /price-history/{id} - Delete Price History
```bash
curl -X DELETE http://localhost:8080/price-history/1
```

---

## 🔧 Testing Workflow

### 1. Create a Product with Store Products
```bash
curl -X POST http://localhost:8080/product/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Product",
    "brand": "Test Brand", 
    "category": "Test Category",
    "size": 1.0,
    "unit": "kg",
    "imageUrl": "https://example.com/test.jpg",
    "description": "Test product for API testing",
    "storeProducts": [
      {
        "store": "Coles",
        "standardPrice": 3.50,
        "productUrl": "https://coles.com.au/test",
        "isActive": true
      },
      {
        "store": "Woolworths", 
        "standardPrice": 3.80,
        "productUrl": "https://woolworths.com.au/test",
        "isActive": true
      }
    ]
  }'
```

### 2. Update a Price (triggers smart price history)
```bash
curl -X PUT http://localhost:8080/product/price \
  -H "Content-Type: application/json" \
  -d '{
    "productId": 5,
    "store": "Coles",
    "newPrice": 4.00
  }'
```

### 3. Check Price History
```bash
curl -X GET http://localhost:8080/price-history/store-product/1 -H "Accept: application/json"
```

### 4. Get Current Price
```bash
curl -X GET http://localhost:8080/price-history/store-product/1/current -H "Accept: application/json"
```

---

## 🎯 Key Benefits

1. **Auto Price History**: Every store product gets automatic price history tracking from day one
2. **Smart Updates**: Price updates intelligently extend periods or create new records
3. **Full CRUD**: Complete create, read, update, delete operations for all entities
4. **Rich Queries**: Search by category, brand, name, or get specific price data
5. **Proper REST**: RESTful endpoints with appropriate HTTP methods and status codes
6. **Error Handling**: Comprehensive error responses with helpful messages
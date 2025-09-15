# PriceByte Backend API Documentation

## Table of Contents
- [Overview](#overview)
- [Base URL](#base-url)
- [Authentication](#authentication)
- [Product Endpoints](#product-endpoints)
- [Store Product Endpoints](#store-product-endpoints)
- [Price History Endpoints](#price-history-endpoints)
- [Data Models](#data-models)
- [Error Handling](#error-handling)
- [Examples](#examples)

## Overview

The PriceByte Backend API provides comprehensive product and price management functionality with automatic price history tracking. The API supports full CRUD operations for products, store-specific product information, and historical price data.

### Key Features
- **Automatic Price History**: Every store product automatically gets price history tracking from creation
- **Smart Price Updates**: Intelligent price change management that extends periods for same prices or creates new records for different prices
- **Comprehensive Search**: Filter products by category, brand, name, and more
- **RESTful Design**: Standard HTTP methods with proper status codes
- **Error Handling**: Detailed error responses with helpful messages

## Base URL
```
http://localhost:8080
```

## Authentication
Currently, no authentication is required for API access.

---

# Product Endpoints

## Create Product
**POST** `/product/`

Creates a new product with optional store product information. Automatically creates price history records for each store product.

### Request Body
```json
{
  "name": "string (required)",
  "brand": "string (required)",
  "category": "string (required)",
  "size": "number (required)",
  "unit": "string (required)",
  "imageUrl": "string",
  "description": "string",
  "storeProducts": [
    {
      "store": "string",
      "standardPrice": "number",
      "productUrl": "string",
      "isActive": "boolean"
    }
  ]
}
```

### Response
- **200 OK**: Returns created product
- **500 Internal Server Error**: Creation failed

### Example
```bash
curl -X POST http://localhost:8080/product/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Coca Cola Classic",
    "brand": "Coca Cola",
    "category": "Beverages",
    "size": 1.25,
    "unit": "L",
    "imageUrl": "https://example.com/coke.jpg",
    "description": "Classic Coca Cola soft drink",
    "storeProducts": [
      {
        "store": "Coles",
        "standardPrice": 3.50,
        "productUrl": "https://coles.com.au/product/coke-125l",
        "isActive": true
      }
    ]
  }'
```

## Get All Products
**GET** `/product/`

Retrieves all products with their store product information.

### Response
- **200 OK**: Array of products

### Example
```bash
curl -X GET http://localhost:8080/product/ -H "Accept: application/json"
```

## Get Product by ID
**GET** `/product/{id}`

Retrieves a specific product by its ID.

### Parameters
- `id` (path): Product ID

### Response
- **200 OK**: Product object
- **404 Not Found**: Product not found

### Example
```bash
curl -X GET http://localhost:8080/product/1 -H "Accept: application/json"
```

## Get Products by Category
**GET** `/product/category/{category}`

Retrieves all products in a specific category.

### Parameters
- `category` (path): Product category

### Response
- **200 OK**: Array of products

### Example
```bash
curl -X GET http://localhost:8080/product/category/Beverages -H "Accept: application/json"
```

## Get Products by Brand
**GET** `/product/brand/{brand}`

Retrieves all products from a specific brand.

### Parameters
- `brand` (path): Product brand

### Response
- **200 OK**: Array of products

### Example
```bash
curl -X GET http://localhost:8080/product/brand/Coca%20Cola -H "Accept: application/json"
```

## Search Products by Name
**GET** `/product/search?name={name}`

Searches products by name (case-insensitive, partial matches).

### Parameters
- `name` (query): Search term

### Response
- **200 OK**: Array of matching products

### Example
```bash
curl -X GET "http://localhost:8080/product/search?name=coca" -H "Accept: application/json"
```

## Update Product
**PUT** `/product/{id}`

Updates an existing product.

### Parameters
- `id` (path): Product ID

### Request Body
```json
{
  "name": "string",
  "brand": "string",
  "category": "string",
  "size": "number",
  "unit": "string",
  "imageUrl": "string",
  "description": "string"
}
```

### Response
- **200 OK**: Updated product
- **404 Not Found**: Product not found

### Example
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

## Delete Product
**DELETE** `/product/{id}`

Deletes a product and all associated store products and price history.

### Parameters
- `id` (path): Product ID

### Response
- **200 OK**: Deletion successful
- **500 Internal Server Error**: Deletion failed

### Example
```bash
curl -X DELETE http://localhost:8080/product/1
```

## Update Store Product Price
**PUT** `/product/price`

Updates the price for a specific store product with intelligent price history management.

**Smart Price Logic:**
- If new price equals current price: Extends the end date of current price record
- If new price differs from current price: Closes current price record and creates new one

### Request Body
```json
{
  "productId": "number (required)",
  "store": "string (required)",
  "newPrice": "number (required)"
}
```

### Response
- **200 OK**: Price updated successfully
- **404 Not Found**: Product or store not found

### Example
```bash
curl -X PUT http://localhost:8080/product/price \
  -H "Content-Type: application/json" \
  -d '{
    "productId": 1,
    "store": "Coles",
    "newPrice": 4.50
  }'
```

---

# Store Product Endpoints

## Get All Store Products
**GET** `/store-product/`

Retrieves all store products.

### Response
- **200 OK**: Array of store products

### Example
```bash
curl -X GET http://localhost:8080/store-product/ -H "Accept: application/json"
```

## Get Store Product by ID
**GET** `/store-product/{id}`

Retrieves a specific store product by its ID.

### Parameters
- `id` (path): Store product ID

### Response
- **200 OK**: Store product object
- **404 Not Found**: Store product not found

### Example
```bash
curl -X GET http://localhost:8080/store-product/1 -H "Accept: application/json"
```

## Create Store Product
**POST** `/store-product/`

Creates a new store product.

### Request Body
```json
{
  "store": "string (required)",
  "standardPrice": "number (required)",
  "productUrl": "string",
  "isActive": "boolean"
}
```

### Response
- **200 OK**: Created store product

### Example
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

## Update Store Product
**PUT** `/store-product/{id}`

Updates an existing store product.

### Parameters
- `id` (path): Store product ID

### Request Body
```json
{
  "store": "string",
  "standardPrice": "number",
  "productUrl": "string",
  "isActive": "boolean"
}
```

### Response
- **200 OK**: Updated store product
- **404 Not Found**: Store product not found

### Example
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

## Delete Store Product
**DELETE** `/store-product/{id}`

Deletes a store product and all associated price history.

### Parameters
- `id` (path): Store product ID

### Response
- **200 OK**: Deletion successful

### Example
```bash
curl -X DELETE http://localhost:8080/store-product/1
```

---

# Price History Endpoints

## Get All Price Histories
**GET** `/price-history/`

Retrieves all price history records.

### Response
- **200 OK**: Array of price history records

### Example
```bash
curl -X GET http://localhost:8080/price-history/ -H "Accept: application/json"
```

## Get Price History by ID
**GET** `/price-history/{id}`

Retrieves a specific price history record by its ID.

### Parameters
- `id` (path): Price history ID

### Response
- **200 OK**: Price history object
- **404 Not Found**: Price history not found

### Example
```bash
curl -X GET http://localhost:8080/price-history/1 -H "Accept: application/json"
```

## Get Price History for Store Product
**GET** `/price-history/store-product/{storeProductId}`

Retrieves all price history records for a specific store product, ordered by start date (most recent first).

### Parameters
- `storeProductId` (path): Store product ID

### Response
- **200 OK**: Array of price history records

### Example
```bash
curl -X GET http://localhost:8080/price-history/store-product/1 -H "Accept: application/json"
```

## Get Current Price
**GET** `/price-history/store-product/{storeProductId}/current`

Retrieves the current price for a store product on a specific date (defaults to today).

### Parameters
- `storeProductId` (path): Store product ID
- `date` (query, optional): Date in YYYY-MM-DD format (defaults to today)

### Response
- **200 OK**: Current price history record
- **404 Not Found**: No price found for the date

### Examples

**Get current price for today:**
```bash
curl -X GET http://localhost:8080/price-history/store-product/1/current -H "Accept: application/json"
```

**Get price for specific date:**
```bash
curl -X GET "http://localhost:8080/price-history/store-product/1/current?date=2024-01-15" -H "Accept: application/json"
```

## Create Price History
**POST** `/price-history/`

Creates a new price history record.

### Request Body
```json
{
  "startDate": "string (YYYY-MM-DD format)",
  "endDate": "string (YYYY-MM-DD format)",
  "price": "number"
}
```

### Response
- **200 OK**: Created price history record

### Example
```bash
curl -X POST http://localhost:8080/price-history/ \
  -H "Content-Type: application/json" \
  -d '{
    "startDate": "2024-01-01",
    "endDate": "2024-01-31",
    "price": 3.99
  }'
```

## Update Price History
**PUT** `/price-history/{id}`

Updates an existing price history record.

### Parameters
- `id` (path): Price history ID

### Request Body
```json
{
  "startDate": "string (YYYY-MM-DD format)",
  "endDate": "string (YYYY-MM-DD format)",
  "price": "number"
}
```

### Response
- **200 OK**: Updated price history record
- **404 Not Found**: Price history not found

### Example
```bash
curl -X PUT http://localhost:8080/price-history/1 \
  -H "Content-Type: application/json" \
  -d '{
    "startDate": "2024-01-01",
    "endDate": "2024-02-15",
    "price": 4.29
  }'
```

## Delete Price History
**DELETE** `/price-history/{id}`

Deletes a price history record.

### Parameters
- `id` (path): Price history ID

### Response
- **200 OK**: Deletion successful

### Example
```bash
curl -X DELETE http://localhost:8080/price-history/1
```

---

# Data Models

## Product
```json
{
  "id": "number (auto-generated)",
  "name": "string",
  "brand": "string",
  "category": "string",
  "size": "number",
  "unit": "string",
  "imageUrl": "string",
  "description": "string",
  "storeProducts": ["StoreProduct array (lazy-loaded)"]
}
```

## StoreProduct
```json
{
  "storeProductId": "number (auto-generated)",
  "store": "string",
  "standardPrice": "number",
  "productUrl": "string",
  "isActive": "boolean"
}
```

## PriceHistory
```json
{
  "id": "number (auto-generated)",
  "startDate": "string (YYYY-MM-DD)",
  "endDate": "string (YYYY-MM-DD)",
  "price": "number"
}
```

## UpdatePriceDto
```json
{
  "productId": "number",
  "store": "string",
  "newPrice": "number"
}
```

---

# Error Handling

The API returns standard HTTP status codes with JSON error responses:

## Success Responses
- **200 OK**: Request successful
- **201 Created**: Resource created successfully

## Error Responses
- **400 Bad Request**: Invalid request data
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

### Error Response Format
```json
{
  "timestamp": "2024-01-15T10:30:00.000+00:00",
  "status": 500,
  "error": "Internal Server Error",
  "path": "/product/"
}
```

### Custom Error Messages
For application-specific errors, the API returns plain text error messages:
```
"Error creating product: Validation failed"
"Product not found with id: 123"
"Product or store not found"
```

---

# Examples

## Complete Workflow Example

### 1. Create a Product with Store Products
```bash
curl -X POST http://localhost:8080/product/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 15 Pro",
    "brand": "Apple",
    "category": "Electronics",
    "size": 6.1,
    "unit": "inches",
    "imageUrl": "https://example.com/iphone15pro.jpg",
    "description": "Latest iPhone with advanced camera features",
    "storeProducts": [
      {
        "store": "Apple Store",
        "standardPrice": 1199.00,
        "productUrl": "https://apple.com/iphone-15-pro",
        "isActive": true
      },
      {
        "store": "JB Hi-Fi",
        "standardPrice": 1199.00,
        "productUrl": "https://jbhifi.com.au/iphone-15-pro",
        "isActive": true
      }
    ]
  }'
```

**Response:**
```json
{
  "id": 5,
  "name": "iPhone 15 Pro",
  "brand": "Apple",
  "category": "Electronics",
  "size": 6.1,
  "unit": "inches",
  "imageUrl": "https://example.com/iphone15pro.jpg",
  "description": "Latest iPhone with advanced camera features",
  "storeProducts": null
}
```

### 2. Update Price (Smart Price History)
```bash
curl -X PUT http://localhost:8080/product/price \
  -H "Content-Type: application/json" \
  -d '{
    "productId": 5,
    "store": "JB Hi-Fi",
    "newPrice": 1099.00
  }'
```

**Response:**
```
"Price updated successfully"
```

### 3. Check Price History
```bash
curl -X GET http://localhost:8080/price-history/store-product/2 -H "Accept: application/json"
```

**Response:**
```json
[
  {
    "id": 3,
    "startDate": "2024-01-15",
    "endDate": "2024-01-15",
    "price": 1099.00
  },
  {
    "id": 2,
    "startDate": "2024-01-15",
    "endDate": "2024-01-14",
    "price": 1199.00
  }
]
```

### 4. Search Products
```bash
curl -X GET "http://localhost:8080/product/search?name=iphone" -H "Accept: application/json"
```

### 5. Get Current Price
```bash
curl -X GET http://localhost:8080/price-history/store-product/2/current -H "Accept: application/json"
```

**Response:**
```json
{
  "id": 3,
  "startDate": "2024-01-15",
  "endDate": "2024-01-15",
  "price": 1099.00
}
```

---

## API Features Summary

✅ **Automatic Price History**: Every store product gets price tracking from creation  
✅ **Smart Price Updates**: Intelligent price change management  
✅ **Full CRUD Operations**: Complete create, read, update, delete for all entities  
✅ **Advanced Search**: Filter by category, brand, name  
✅ **Price Queries**: Get current prices and historical data  
✅ **RESTful Design**: Standard HTTP methods and status codes  
✅ **Error Handling**: Comprehensive error responses  
✅ **Data Relationships**: Proper entity relationships with lazy loading  

---

## Support

For issues or questions about the API, please check the application logs or contact the development team.
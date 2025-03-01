# Grocery Product Data Consolidation System

## Project Overview

This project aims to create a centralized system that aggregates product data from multiple grocery stores (Coles, ALDI, Woolworths, etc.) and intelligently consolidates duplicate products while tracking price histories across different retailers.

### Core Problem
- Web scrapers collect product data from various grocery stores
- Each store has different data formats and schemas
- Many products are identical but appear with slight naming/pricing differences
- Need to identify duplicate products and track price variations across stores
- Want to build recommendation systems based on product similarity

### Key Features
- **Product Deduplication**: Identify identical products across different stores
- **Price Tracking**: Historical price data for each product at each store
- **Product Similarity**: Vector-based matching for recommendations
- **Multi-Store Support**: Handle varying data schemas from different retailers

## Data Flow

```
Web Scrapers → POST /api/products → Processing Pipeline → SQLite Database
                                        ↓
                              Vector Generation & Matching
                                        ↓
                              Product Consolidation & Storage
```

## Database Schema

### `products` Table
- `id` (INTEGER, PRIMARY KEY)
- `name` (TEXT) - Standardized product name
- `brand` (TEXT)
- `category` (TEXT) - Normalized category
- `size` (TEXT) - Product size/weight
- `unit` (TEXT) - Unit of measurement
- `image_url` (TEXT)
- `description` (TEXT)
- `vector_embedding` (BLOB) - For similarity matching
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

*Index on: category*

### `store_products` Table
- `id` (INTEGER, PRIMARY KEY)
- `store` (TEXT) - Store identifier (coles, aldi, woolworths)
- `store_product_id` (TEXT) - Original store product ID
- `product_id` (INTEGER, FOREIGN KEY → products.id)
- `store_name` (TEXT) - Product name as it appears in store
- `current_price` (REAL)
- `product_url` (TEXT) - Link to product page
- `availability` (BOOLEAN)
- `raw_details` (JSON) - Original store data
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

### `price_history` Table
- `id` (INTEGER, PRIMARY KEY)
- `store_product_id` (INTEGER, FOREIGN KEY → store_products.id)
- `price` (REAL)
- `start_date` (DATE)
- `end_date` (DATE)
- `created_at` (TIMESTAMP)

## Current Store Data Formats

### Coles Format
```json
{
  "id": 8909349,
  "name": "Japanese Infusion Salmon Portion",
  "brand": "Huon",
  "description": "HUON JAPANESE FUSION SALMON 200G",
  "size": "200g",
  "imageUris": [
    {
      "altText": "",
      "type": "default",
      "uri": "/8/8909349.jpg"
    }
  ],
  "availabilityStatus": null,
  "minGuarantee": null,
  "merchandiseHeir": {
    "tradeProfitCentre": "MEAT",
    "categoryGroup": "SEAFOOD",
    "category": "PREPACKAGED SEAFOOD",
    "subCategory": "SALMON V-ADDED PPS",
    "className": "1 PACK"
  },
  "onlineHeirs": [
    {
      "aisle": "Japanese",
      "category": "World Foods",
      "subCategory": "Dietary & World Foods",
      "categoryId": "674113139",
      "aisleId": "675104352",
      "subCategoryId": "674112512"
    },
    {
      "aisle": "Prepacked Seafood",
      "category": "Seafood",
      "subCategory": "Meat & Seafood",
      "categoryId": "8892671",
      "aisleId": "8892677",
      "subCategoryId": "7238"
    }
  ],
  "associatedProductId": null,
  "continuity": null,
  "lifestyle": null,
  "lastUpdated": "2025-09-14T13:36:32Z",
  "locations": [
    {
      "aisleSide": "",
      "description": "Aisle information is not available for this product. Please ask a Team Member at $STORE to help you find this product.",
      "facing": 0,
      "aisle": "",
      "order": 9999,
      "shelf": null
    }
  ],
  "additionalInfo": [
    {
      "title": "Allergen",
      "description": "Contains Sesame, Soy"
    },
    {
      "title": "Dimensions",
      "description": "225.00 x 135.00 x 40.00 mm"
    }
  ],
  "excludeFromSubstitution": false,
  "brandDetails": {
    "id": 3313734012,
    "name": "Huon",
    "seoToken": "huon"
  },
  "collectableCampaign": "",
  "disclaimers": null,
  "internalDescription": "",
  "longDescription": "",
  "nutrition": null,
  "nutritionalClaims": null,
  "pricing": {
    "now": 9.5,
    "was": 12,
    "saveAmount": 2.5,
    "saveStatement": "save $2.50",
    "unit": {
      "quantity": 1,
      "ofMeasureQuantity": 1,
      "ofMeasureUnits": "kg",
      "price": 47.5,
      "ofMeasureType": null,
      "isWeighted": false,
      "isIncremental": false
    },
    "comparable": "$47.50 per 1kg",
    "promotionType": "SPECIAL",
    "onlineSpecial": false,
    "multiBuyPromotion": null,
    "priceDescription": null,
    "savePercent": 0,
    "specialType": null,
    "offerDescription": null
  },
  "gtin": "9315896103096",
  "variations": null,
  "images": [
    {
      "thumb": {
        "path": "/wcsstore/Coles-CAS/images/8/9/0/8909349-th.jpg",
        "description": null
      },
      "zoom": {
        "path": "/wcsstore/Coles-CAS/images/8/9/0/8909349-zm.jpg",
        "description": "Product Image of Huon Japanese Infusion Salmon Portion"
      },
      "full": {
        "path": "/wcsstore/Coles-CAS/images/8/9/0/8909349.jpg",
        "description": null
      }
    },
    {
      "thumb": {
        "path": "/wcsstore/Coles-CAS/images/8/9/0/8909349_B-th.jpg",
        "description": "Back of pack of Huon Japanese Infusion Salmon Portion"
      },
      "zoom": {
        "path": "/wcsstore/Coles-CAS/images/8/9/0/8909349_B-zm.jpg",
        "description": "Back of pack of Huon Japanese Infusion Salmon Portion"
      },
      "full": {
        "path": "/wcsstore/Coles-CAS/images/8/9/0/8909349_B.jpg",
        "description": "Back of pack of Huon Japanese Infusion Salmon Portion"
      }
    }
  ],
  "restrictions": {
    "retailLimit": 20,
    "promotionalLimit": 12,
    "liquorAgeRestrictionFlag": false,
    "tobaccoAgeRestrictionFlag": false,
    "delivery": [],
    "restrictedByOrganisation": false
  },
  "countryOfOrigin": {
    "logoRequired": true,
    "barcodeRequired": true,
    "descriptionRequired": true,
    "country": "Australia",
    "barcodePercentage": 80,
    "statement": "Made in Australia from at least 88% Australian ingredients",
    "description": "Made in Australia from at least 88% Australian ingredients"
  },
  "availability": true
}
```

### ALDI Format
```json
{
  "brand": "Simply Nature",
  "category": "Dairy",
  "description": "High quality simply nature almond milk available at Aldi",
  "weight": "187g",
  "ingredients": "Almondmilk (filtered water, almonds), vitamin E",
  "nutrition_facts": {
    "calories_per_serving": 256,
    "fat": "2.3g",
    "sodium": "109mg",
    "protein": "11.4g"
  },
  "barcode": "123456972658",
  "availability": "Out of Stock",
  "rating": 4.0
}
```

---

# Basic Version (MVP) Specification

## Scope
The basic version will focus on core functionality without advanced features like sophisticated product matching or real-time vector similarity search.

## Features

### 1. API Endpoint
- **POST /api/products**
- Accept data in format: `STORE | ID | NAME | PRICE | DETAILS`
- Automatic input validation with Pydantic models
- Auto-generated OpenAPI/Swagger documentation at `/docs`

### 2. Data Processing Pipeline
- Parse incoming store-specific JSON data
- Extract common fields (name, brand, price, category, size)
- Generate simple text representation for basic matching

### 3. Simple Product Matching
- Basic string similarity for duplicate detection
- No vector embeddings initially - use fuzzy string matching
- Manual threshold-based matching (e.g., 80% string similarity)

### 4. Database Operations
- Insert new products or update existing ones
- Create store_product associations
- Simple price history tracking (new entry when price changes)

### 5. Basic Response Format
```json
{
  "status": "success",
  "product_id": 123,
  "action": "created|updated",
  "matched_existing": true|false
}
```

## Technical Stack

### Core Technologies
- **Python** - Primary language
- **FastAPI** - Modern, fast web framework with automatic API documentation
- **SQLite** - Database (simple, file-based)
- **SQLAlchemy** - ORM for database operations

### Libraries
- `fastapi` - Web server and API framework
- `uvicorn` - ASGI server for FastAPI
- `sqlalchemy` - Database ORM
- `pydantic` - Data validation and serialization
- `fuzzywuzzy` - Basic string similarity matching
- `python-levenshtein` - String distance calculations
- `python-multipart` - For handling form data
- `datetime` - Timestamp handling

## File Structure
```
grocery-consolidator/
├── main.py             # Main FastAPI application
├── models.py           # SQLAlchemy database models
├── schemas.py          # Pydantic models for API validation
├── processors.py       # Store-specific data processors
├── matcher.py          # Product matching logic
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
└── database.db         # SQLite database file
```

## API Usage Example

### Request
```bash
curl -X POST http://localhost:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{
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
      },
      "pricing": {
        "now": 9.5,
        "was": 12,
        "saveAmount": 2.5
      }
    }
  }'
```

### Response
```json
{
  "status": "success",
  "product_id": 15,
  "action": "created",
  "matched_existing": false,
  "message": "New product created successfully"
}
```

## Limitations of Basic Version
- No vector embeddings or advanced ML matching
- Simple string-based similarity only
- No real-time price alerts
- No recommendation system
- Limited category standardization
- No advanced duplicate detection across different product formats

## Future Enhancements
1. Implement vector embeddings with sentence-transformers
2. Add sophisticated product matching algorithms
3. Build recommendation system
4. Add price alert system
5. Implement category standardization
6. Add product image processing
7. Create web dashboard for data visualization
8. Scale to PostgreSQL or dedicated vector database

---

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Initialize database: `python -c "from models import Base, engine; Base.metadata.create_all(engine)"`
3. Start server: `uvicorn main:app --reload`
4. Visit API documentation: `http://localhost:8000/docs`
5. Send test requests to `http://localhost:8000/api/products`

This basic version provides a solid foundation that can be incrementally enhanced with more sophisticated features as the project evolves.

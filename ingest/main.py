from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date, datetime
from typing import List

from models import get_db, create_tables, Product, StoreProduct, PriceHistory
from schemas import ProductCreateRequest, ProductResponse, ProductInfo, StoreProductInfo, ProductWithStores, StoreProductWithHistory, PriceHistoryInfo, PriceUpdateRequest, PriceUpdateResponse, ProductSearchResult, ProductSearchResponse
from processors import ProcessorFactory
from matcher import ProductMatcher
from config import API_TITLE, API_DESCRIPTION, API_VERSION

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)

@app.on_event("startup")
async def startup_event():
    create_tables()

@app.post("/api/products", response_model=ProductResponse)
async def create_product(
    product_request: ProductCreateRequest,
    db: Session = Depends(get_db)
):
    try:
        processor = ProcessorFactory.get_processor(product_request.store)
        
        name, brand, category, size, unit, image_url, description = processor.process(
            product_request.details
        )
        
        if not name:
            name = product_request.name
        
        normalized_category = ProcessorFactory.normalize_category(category)
        
        matcher = ProductMatcher(db)
        existing_product = matcher.find_matching_product(name, brand, normalized_category, size)
        
        if existing_product:
            product_id = existing_product.id
            action = "updated"
            matched_existing = True
            
            existing_product.updated_at = datetime.utcnow()
            if not existing_product.image_url and image_url:
                existing_product.image_url = image_url
            if not existing_product.description and description:
                existing_product.description = description
        else:
            new_product = Product(
                name=name,
                brand=brand,
                category=normalized_category,
                size=size,
                unit=unit,
                image_url=image_url,
                description=description
            )
            db.add(new_product)
            db.flush()
            
            product_id = new_product.id
            action = "created"
            matched_existing = False
        
        existing_store_product = db.query(StoreProduct).filter(
            StoreProduct.store == product_request.store,
            StoreProduct.store_product_id == product_request.id
        ).first()
        
        if existing_store_product:
            old_price = existing_store_product.current_price
            if old_price != product_request.price:
                latest_price_history = db.query(PriceHistory).filter(
                    PriceHistory.store_product_id == existing_store_product.id,
                    PriceHistory.end_date.is_(None)
                ).first()
                
                if latest_price_history:
                    latest_price_history.end_date = date.today()
                
                new_price_history = PriceHistory(
                    store_product_id=existing_store_product.id,
                    price=product_request.price,
                    start_date=date.today()
                )
                db.add(new_price_history)
            
            existing_store_product.current_price = product_request.price
            existing_store_product.product_id = product_id
            existing_store_product.store_name = product_request.name
            existing_store_product.raw_details = product_request.details
            existing_store_product.updated_at = datetime.utcnow()
        else:
            new_store_product = StoreProduct(
                store=product_request.store,
                store_product_id=product_request.id,
                product_id=product_id,
                store_name=product_request.name,
                current_price=product_request.price,
                raw_details=product_request.details
            )
            db.add(new_store_product)
            db.flush()
            
            initial_price_history = PriceHistory(
                store_product_id=new_store_product.id,
                price=product_request.price,
                start_date=date.today()
            )
            db.add(initial_price_history)
        
        db.commit()
        
        return ProductResponse(
            status="success",
            product_id=product_id,
            action=action,
            matched_existing=matched_existing,
            message=f"Product {action} successfully"
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )

@app.get("/api/products", response_model=List[ProductInfo])
async def get_products(
    store: str = None,
    category: str = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Product).join(StoreProduct)
    
    if store:
        query = query.filter(StoreProduct.store == store)
    
    if category:
        query = query.filter(Product.category == category)
    
    products = query.limit(limit).all()
    
    result = []
    for product in products:
        store_product = db.query(StoreProduct).filter(
            StoreProduct.product_id == product.id
        ).first()
        
        if store_product:
            result.append(ProductInfo(
                id=product.id,
                name=product.name,
                brand=product.brand,
                category=product.category,
                size=product.size,
                current_price=store_product.current_price,
                store=store_product.store,
                created_at=product.created_at,
                updated_at=product.updated_at
            ))
    
    return result

@app.get("/api/products/search", response_model=ProductSearchResponse)
async def search_products(
    q: str,
    offset: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Search for products by name similarity with pagination.
    
    Args:
        q: Search query (product name)
        offset: Number of results to skip (default: 0)
        limit: Maximum number of results to return (default: 10, max: 50)
        
    Returns:
        Paginated list of products ranked by name similarity with scores
    """
    if not q or not q.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Search query cannot be empty"
        )
    
    # Validate pagination parameters
    if offset < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Offset cannot be negative"
        )
    
    if limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be greater than 0"
        )
    
    # Limit the results to a reasonable number
    limit = min(limit, 50)
    
    matcher = ProductMatcher(db)
    # Get more results than needed to handle pagination properly
    max_results = offset + limit + 1  # +1 to check if there are more results
    search_results = matcher.search_products_by_name(q.strip(), max_results)
    
    total_count = len(search_results)
    
    # Apply pagination
    paginated_results = search_results[offset:offset + limit]
    has_next = total_count > offset + limit
    
    results = []
    for product, similarity_score in paginated_results:
        results.append(ProductSearchResult(
            id=product.id,
            name=product.name,
            brand=product.brand,
            category=product.category,
            size=product.size,
            unit=product.unit,
            image_url=product.image_url,
            description=product.description,
            similarity_score=round(similarity_score, 3),
            created_at=product.created_at,
            updated_at=product.updated_at
        ))
    
    return ProductSearchResponse(
        results=results,
        total_count=total_count,
        offset=offset,
        limit=limit,
        has_next=has_next
    )

@app.get("/api/products/{product_id}", response_model=ProductWithStores)
async def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """
    Get a product by ID with all associated store products and complete price history.
    
    Returns:
    - Product details
    - All store products associated with this product
    - Complete price history for each store product
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    store_products = db.query(StoreProduct).filter(
        StoreProduct.product_id == product_id
    ).all()
    
    store_products_with_history = []
    for store_product in store_products:
        price_history = db.query(PriceHistory).filter(
            PriceHistory.store_product_id == store_product.id
        ).order_by(PriceHistory.start_date.desc()).all()
        
        price_history_info = [
            PriceHistoryInfo(
                price=ph.price,
                start_date=ph.start_date.isoformat(),
                end_date=ph.end_date.isoformat() if ph.end_date else None
            )
            for ph in price_history
        ]
        
        store_products_with_history.append(StoreProductWithHistory(
            id=store_product.id,
            store=store_product.store,
            store_product_id=store_product.store_product_id,
            store_name=store_product.store_name,
            current_price=store_product.current_price,
            availability=store_product.availability,
            product_url=store_product.product_url,
            raw_details=store_product.raw_details,
            created_at=store_product.created_at,
            updated_at=store_product.updated_at,
            price_history=price_history_info
        ))
    
    return ProductWithStores(
        id=product.id,
        name=product.name,
        brand=product.brand,
        category=product.category,
        size=product.size,
        unit=product.unit,
        image_url=product.image_url,
        description=product.description,
        created_at=product.created_at,
        updated_at=product.updated_at,
        store_products=store_products_with_history
    )

@app.get("/api/products/{product_id}/stores/{store}", response_model=StoreProductInfo)
async def get_store_product_details(product_id: int, store: str, db: Session = Depends(get_db)):
    """
    Get details for a specific product at a specific store with price history.
    This is the original endpoint functionality, moved to a more specific path.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    store_product = db.query(StoreProduct).filter(
        StoreProduct.product_id == product_id,
        StoreProduct.store == store
    ).first()
    
    if not store_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found at {store}"
        )
    
    price_history = db.query(PriceHistory).filter(
        PriceHistory.store_product_id == store_product.id
    ).order_by(PriceHistory.start_date.desc()).all()
    
    price_history_info = [
        PriceHistoryInfo(
            price=ph.price,
            start_date=ph.start_date.isoformat(),
            end_date=ph.end_date.isoformat() if ph.end_date else None
        )
        for ph in price_history
    ]
    
    return StoreProductInfo(
        id=store_product.id,
        store=store_product.store,
        store_product_id=store_product.store_product_id,
        store_name=store_product.store_name,
        current_price=store_product.current_price,
        availability=store_product.availability,
        product_url=store_product.product_url,
        price_history=price_history_info
    )

@app.post("/api/price-update", response_model=PriceUpdateResponse)
async def update_product_price(
    price_update: PriceUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    Update the price for a specific store product.
    
    This endpoint:
    1. Finds the store product by store and store_product_id
    2. Ends the current price history record (sets end_date to today)
    3. Creates a new price history record with the new price
    4. Updates the current_price on the store product
    
    Args:
        price_update: Contains store, store_product_id, and new_price
        
    Returns:
        Details about the price update including old/new prices
    """
    try:
        # Find the store product
        store_product = db.query(StoreProduct).filter(
            StoreProduct.store == price_update.store,
            StoreProduct.store_product_id == price_update.store_product_id
        ).first()
        
        if not store_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {price_update.store_product_id} not found at {price_update.store}"
            )
        
        old_price = store_product.current_price
        
        # Only proceed if price is actually different
        if old_price == price_update.new_price:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"New price {price_update.new_price} is the same as current price"
            )
        
        # End the current price history record
        current_price_history = db.query(PriceHistory).filter(
            PriceHistory.store_product_id == store_product.id,
            PriceHistory.end_date.is_(None)
        ).first()
        
        if current_price_history:
            current_price_history.end_date = date.today()
        
        # Create new price history record
        new_price_history = PriceHistory(
            store_product_id=store_product.id,
            price=price_update.new_price,
            start_date=date.today()
        )
        db.add(new_price_history)
        db.flush()  # Get the ID
        
        # Update the store product current price
        store_product.current_price = price_update.new_price
        store_product.updated_at = datetime.utcnow()
        
        db.commit()
        
        return PriceUpdateResponse(
            status="success",
            message=f"Price updated from ${old_price} to ${price_update.new_price}",
            store_product_id=store_product.id,
            old_price=old_price,
            new_price=price_update.new_price,
            price_history_id=new_price_history.id
        )
        
    except Exception as e:
        db.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating price: {str(e)}"
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
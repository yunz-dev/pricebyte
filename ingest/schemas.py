from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from config import SUPPORTED_STORES

class ProductDetailsBase(BaseModel):
    brand: Optional[str] = None
    size: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    weight: Optional[str] = None
    ingredients: Optional[str] = None
    barcode: Optional[str] = None
    availability: Optional[str] = None
    rating: Optional[float] = None

class ColesDetails(ProductDetailsBase):
    merchandiseHeir: Optional[Dict[str, Any]] = None
    onlineHeirs: Optional[List[Dict[str, Any]]] = None
    pricing: Optional[Dict[str, Any]] = None
    images: Optional[List[Dict[str, Any]]] = None
    brandDetails: Optional[Dict[str, Any]] = None
    gtin: Optional[str] = None
    additionalInfo: Optional[List[Dict[str, Any]]] = None

class AldiDetails(ProductDetailsBase):
    nutrition_facts: Optional[Dict[str, Any]] = None

class ProductCreateRequest(BaseModel):
    store: str = Field(..., description="Store identifier")
    id: str = Field(..., description="Store-specific product ID")
    name: str = Field(..., description="Product name")
    price: float = Field(..., ge=0, description="Current price")
    details: Dict[str, Any] = Field(default_factory=dict, description="Store-specific product details")
    
    @field_validator('store')
    @classmethod
    def validate_store(cls, v):
        if v.lower() not in SUPPORTED_STORES:
            raise ValueError(f'Store must be one of: {", ".join(SUPPORTED_STORES)}')
        return v.lower()
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v < 0:
            raise ValueError('Price must be non-negative')
        return round(v, 2)

class ProductResponse(BaseModel):
    status: str
    product_id: int
    action: str
    matched_existing: bool
    message: Optional[str] = None

class ProductInfo(BaseModel):
    id: int
    name: str
    brand: Optional[str] = None
    category: Optional[str] = None
    size: Optional[str] = None
    current_price: float
    store: str
    created_at: datetime
    updated_at: datetime

class PriceHistoryInfo(BaseModel):
    price: float
    start_date: str
    end_date: Optional[str] = None
    
class StoreProductInfo(BaseModel):
    id: int
    store: str
    store_product_id: str
    store_name: str
    current_price: float
    availability: bool
    product_url: Optional[str] = None
    price_history: List[PriceHistoryInfo] = []

class StoreProductWithHistory(BaseModel):
    id: int
    store: str
    store_product_id: str
    store_name: str
    current_price: float
    availability: bool
    product_url: Optional[str] = None
    raw_details: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    price_history: List[PriceHistoryInfo] = []

class ProductWithStores(BaseModel):
    id: int
    name: str
    brand: Optional[str] = None
    category: Optional[str] = None
    size: Optional[str] = None
    unit: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    store_products: List[StoreProductWithHistory] = []

class PriceUpdateRequest(BaseModel):
    store: str = Field(..., description="Store identifier")
    store_product_id: str = Field(..., description="Store-specific product ID")
    new_price: float = Field(..., ge=0, description="New price")
    
    @field_validator('store')
    @classmethod
    def validate_store(cls, v):
        if v.lower() not in SUPPORTED_STORES:
            raise ValueError(f'Store must be one of: {", ".join(SUPPORTED_STORES)}')
        return v.lower()
    
    @field_validator('new_price')
    @classmethod
    def validate_price(cls, v):
        if v < 0:
            raise ValueError('Price must be non-negative')
        return round(v, 2)

class PriceUpdateResponse(BaseModel):
    status: str
    message: str
    store_product_id: int
    old_price: float
    new_price: float
    price_history_id: int

class ProductSearchResult(BaseModel):
    id: int
    name: str
    brand: Optional[str] = None
    category: Optional[str] = None
    size: Optional[str] = None
    unit: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    similarity_score: float
    created_at: datetime
    updated_at: datetime

class ProductSearchResponse(BaseModel):
    results: List[ProductSearchResult]
    total_count: int
    offset: int
    limit: int
    has_next: bool
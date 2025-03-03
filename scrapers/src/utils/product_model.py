from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):
    store: str
    product_name: str
    brand: str
    category: str
    price: float
    unit_price: float
    discount_price: Optional[float] = None
    original_price: float
    availability: str
    image_url: str
    product_url: str
    weight: str
    description: str

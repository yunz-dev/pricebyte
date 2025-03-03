from pydantic import BaseModel


class Product(BaseModel):
    store: str
    product_name: str
    brand: str
    category: str
    price: float
    unit_price: float
    original_price: float
    availability: bool
    image_url: str
    product_url: str
    weight: str
    description: str

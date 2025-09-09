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


class ApiProduct(BaseModel):
    store: str
    price: float
    product_name: str
    brand: str
    weight: str
    product_url: str


class ApiProducts(BaseModel):
    api_uses: int
    products: list[ApiProduct]


class ColesProductV1(BaseModel):
    id: int
    name: str
    brand: str
    price: float
    old_price: float
    on_sale: bool
    unit_price: float
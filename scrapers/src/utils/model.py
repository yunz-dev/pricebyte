from pydantic import BaseModel
from enum import Enum
from abc import ABC, abstractmethod
from typing import List, Tuple

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

# --------------------- Version 2 Models ---------------------

class Scraper(ABC):

    @abstractmethod
    def scrape_category(self) -> List[Tuple[int, float]]:
        # a list of (store_product_id, new_price)
        pass

    @abstractmethod
    def scrape_product(self, id: int) -> bool:
        # returns success/failure
        pass

    @abstractmethod
    def price_changed(self, product: Tuple[int, float]) -> bool:
        pass

    @abstractmethod
    def is_new_product(self, id: int) -> bool:
        pass


class Store(str, Enum):
    ALDI = "ALDI"
    Woolworths = "Woolworths"
    Coles = "Coles"
    IGA = "IGA"

class PriceUpdates(BaseModel):
    store_product_id: int
    store: Store
    new_price: int


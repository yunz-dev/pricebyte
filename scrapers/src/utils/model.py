import asyncio
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Tuple

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


# --------------------- Version 2 Models ---------------------


class Store(str, Enum):
    ALDI = "ALDI"
    Woolworths = "Woolworths"
    Coles = "Coles"
    IGA = "IGA"


class PriceUpdates(BaseModel):
    store_product_id: int
    store: Store
    product_name: str
    price: float


# we could inherirt here but i hate inheritence
class ProductInfo(BaseModel):
    store_product_id: int
    store: Store
    product_name: str
    price: float
    details: dict


class Scraper(ABC):
    @abstractmethod
    def scrape_category(self) -> List[PriceUpdates]:
        # a list of (store_product_id, new_price)
        pass

    @abstractmethod
    def scrape_product(self, product: PriceUpdates) -> ProductInfo:
        pass

    # might be useless lol
    @abstractmethod
    def price_changed(self, product: PriceUpdates) -> bool:
        pass

    # might be useless lol
    @abstractmethod
    def is_new_product(self, product: PriceUpdates) -> bool:
        pass

    @abstractmethod
    def get_store_name(self) -> str:
        pass
    

class ColesProductV1(BaseModel):
    store: str
    id: int
    name: str
    brand: str
    price: float
    old_price: float
    on_sale: bool
    unit_price: float

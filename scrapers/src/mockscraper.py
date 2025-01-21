from typing import List
from utils.model import PriceUpdates, ProductInfo, Scraper
from fake_data_generator import FakeDataGenerator


class MockScraperAldi(Scraper):
    """Mock scraper for Aldi using fake data generator."""

    def scrape_category(self) -> List[PriceUpdates]:
        return FakeDataGenerator.generate_price_updates_list()

    def scrape_product(self, product: PriceUpdates) -> ProductInfo:
        fake_details = FakeDataGenerator.generate_product_details(product)

        return ProductInfo(
            store_product_id=product.store_product_id,
            store=product.store,
            product_name=product.product_name,
            price=product.price,
            details=fake_details,
        )

    def price_changed(self, product: PriceUpdates) -> bool:
        return super().price_changed(product)

    def is_new_product(self, product: PriceUpdates) -> bool:
        return super().is_new_product(product)

    def get_store_name(self) -> str:
        return "Fake Aldi"


from database import MainDatabase, MockDatabase
from mockscraper import MockScraperAldi
from utils.model import PriceUpdates, ProductInfo, Scraper
from typing import List
from config import is_production, parse_and_set_env, is_mock
from log import log

main_db = MainDatabase()
test_db = MockDatabase()


def main():
    parse_and_set_env()
    scraper_list = (
        [
            # Add Mock Scrapers here
            MockScraperAldi()
        ]
        if is_mock()
        else [
            # Add real scrapers here
        ]
    )

    stores = category_scrape(scraper_list)

    for i, product_list in enumerate(stores):
        product_scrape(scraper_list[i], product_list)

    for i, product_list in enumerate(stores):
        product_price_check(scraper_list[i], product_list)

    log("SUCCESS ==========================================")


def category_scrape(scraper_list: List[Scraper]) -> List[List[PriceUpdates]]:
    log("scraping categories")
    stores = []

    for scraper in scraper_list:
        log(f"Scraping {scraper.get_store_name()}")
        stores.append(scraper.scrape_category())

    return stores


# List here is a list of product models
def product_scrape(scraper: Scraper, product_list: List[PriceUpdates]) -> int:
    """
    returns number of producst scraped and sent to scala
    """
    log(f"scraping products for {scraper.get_store_name()}")
    products_added = 0
    for product in product_list:
        store, id, name, price = (
            product.store,
            product.store_product_id,
            product.product_name,
            product.price,
        )
        if main_db.add_simple_product(store, id, name, price):
            productInfo = scraper.scrape_product(product)
            send_to_data_processer(productInfo)
            products_added += 1
    log(f"successfully added: {products_added} products")
    return products_added


def product_price_check(scraper: Scraper, product_list: List[PriceUpdates]) -> int:
    log(f"checking prices for {scraper.get_store_name()}")

    prices_changed = 0
    for product in product_list:
        store, id, price = (
            product.store, product.store_product_id, product.price)
        if main_db.check_price(store, id, price):
            update_price_remote(product)
            prices_changed += 1

    log(f"successfully changed: {prices_changed} prices")
    return prices_changed


def send_to_data_processer(data: ProductInfo):
    id, store, name, price, details = (
        data.store_product_id,
        data.store,
        data.product_name,
        data.price,
        data.details,
    )
    if is_production():
        send_to_scala(data)
        log(f"successfully sent product: {store}:{id} to scala")
    else:
        test_db.upsert_complex_product(store, id, name, price, details)
        log(f"successfully sent product: {store}:{id} to MockDB")


def update_price_remote(data: PriceUpdates):
    id, store, name, price = (
        data.store_product_id,
        data.store,
        data.product_name,
        data.price,
    )
    if is_production():
        send_to_spring(data)
        log(f"successfully updated product price for: {store}:{id} via spring")
    else:
        log(f"successfully updated product price for: {store}:{id} via MockDB")
        test_db.upsert_simple_product(store, id, name, price)


def send_to_spring(data) -> bool:
    raise NotImplementedError


def send_to_scala(data) -> bool:
    raise NotImplementedError


if __name__ == "__main__":
    main()

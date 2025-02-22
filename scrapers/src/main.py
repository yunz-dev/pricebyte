from typing import List

import requests
from config import is_mock, is_production, parse_and_set_env
from database import MainDatabase, MockDatabase
from log import detailed_log, log
from mockscraper import MockScraperAldi

# still not working i fix later ->>>>
# from scrapers.wooliesV2 import WoolworthsScraper
from utils.model import PriceUpdates, ProductInfo, Scraper

from scrapers.aldiV2 import AldiScraper
from scrapers.colesV2 import ColesScraper
import os

main_db = MainDatabase()
test_db = MockDatabase()
py_etl_url = os.environ["py_etl_url"]


def main():
    parse_and_set_env()
    scraper_list = (
        [
            # Add Mock Scrapers here
            MockScraperAldi()
        ]
        if is_mock()
        else [
            ColesScraper(),
            AldiScraper(),
            # Add real scrapers here
        ]
    )

    stores = category_scrape(scraper_list)

    for i, product_list in enumerate(stores):
        product_scrape(scraper_list[i], product_list)

    for i, product_list in enumerate(stores):
        product_price_check(scraper_list[i], product_list)

    log("SUCCESS ==========================================")


# i took away type hints temporarily for this cuz linter was going crazy
# def category_scrape(scraper_list: List[Scraper]) -> List[List[PriceUpdates]]:
def category_scrape(scraper_list) -> List[List[PriceUpdates]]:
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
        store, id, price = (product.store, product.store_product_id, product.price)
        if main_db.check_price(store, id, price):
            update_price_remote(product)
            prices_changed += 1

    log(f"successfully changed: {prices_changed} prices")
    return prices_changed


# TODO:
# change logs to detailed logs later
def send_to_data_processer(data: ProductInfo):
    id, store, name, price, details = (
        data.store_product_id,
        data.store,
        data.product_name,
        data.price,
        data.details,
    )
    if is_production():
        res = send_to_etl_v0(data)
        if res.ok:
            log(f"successfully sent product: {store}:{id} to etl")
        else:
            log(f"unsuccessfully sent product: {store}:{id} to etl")
            append_to_file(f"{res}")

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
        res = update_remote_v0(data)
        if res.ok:
            log(f"successfully sent product: {store}:{id} to update price")
        else:
            log(f"unsuccessfully sent product: {store}:{id} to update price")
            append_to_file(f"{res}")
    else:
        log(f"successfully updated product price for: {store}:{id} via MockDB")
        test_db.upsert_simple_product(store, id, name, price)


def update_remote_v0(data) -> requests.Response:
    return update_price(data)


def send_to_etl_v0(data) -> requests.Response:
    return create_product(data)


def send_to_spring(data) -> bool:
    raise NotImplementedError


def send_to_scala(data) -> bool:
    raise NotImplementedError


def append_to_file(content, filename="./log.txt"):
    """Append content to a file, creating it if it doesn't exist."""
    with open(filename, "a") as file:
        file.write(content + "\n")


def create_product(
    product_info: ProductInfo, base_url: str = "http://localhost:8000"
) -> requests.Response:
    payload = {
        "store": product_info.store.value
        if hasattr(product_info.store, "value")
        else str(product_info.store),
        "id": str(product_info.store_product_id),
        "name": product_info.product_name,
        "price": product_info.price,
        "details": product_info.details,
    }

    headers = {"accept": "application/json", "Content-Type": "application/json"}

    response = requests.post(f"{base_url}/api/products", json=payload, headers=headers)

    return response


def update_price(
    price_update: PriceUpdates, base_url: str = "http://localhost:8000"
) -> requests.Response:
    payload = {
        "store": price_update.store.value
        if hasattr(price_update.store, "value")
        else str(price_update.store),
        "store_product_id": str(price_update.store_product_id),
        "new_price": price_update.price,
    }

    headers = {"accept": "application/json", "Content-Type": "application/json"}

    response = requests.post(
        f"{base_url}/api/price-update", json=payload, headers=headers
    )

    return response


if __name__ == "__main__":
    main()

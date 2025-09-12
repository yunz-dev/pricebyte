from utils.model import Scraper
from typing import List, Tuple


def main():
    scraper_list = [
        # Add scrapers here
    ]

    stores = category_scrape(scraper_list)

    for i, product_list in enumerate(stores):
        product_scrape(scraper_list[i], product_list)

    for i, product_list in enumerate(stores):
        product_price_check(scraper_list[i], product_list)


def category_scrape(scraper_list: List[Scraper]) -> List[List[Tuple[int, float]]]:
    stores = []

    for scraper in scraper_list:
        print(f"Scraping {scraper.get_store_name()}")
        stores.append(scraper.scrape_category())

    return stores


# List here is a list of product models
def product_scrape(scraper: Scraper, product_list: List[Tuple[int, float]]) -> List:
    products = []

    for id, _ in product_list:
        if scraper.is_new_product(id):
            send_to_scala(scraper.scrape_product(id))

    return products


def product_price_check(
    scraper: Scraper, product_list: List[Tuple[int, float]]
) -> List[Tuple[int, float]]:
    products = []
    for id, price in product_list:
        if scraper.price_changed((id, price)):
            send_to_spring((scraper.get_store_name(), id, price))

    return products


def send_to_spring(data) -> bool:
    raise NotImplementedError


def send_to_scala(data) -> bool:
    raise NotImplementedError


if __name__ == "__main__":
    main()


# run a category scraper
# check each id with sqlite
# return a list a price_updates
# have a list of new_product_ids


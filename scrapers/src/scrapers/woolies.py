import json
import random
import re
import time

from selenium.webdriver.firefox.options import Options
from utils.model import Product

pages = [
    "https://www.woolworths.com.au/shop/productdetails/",
    "https://www.woolworths.com.au/api/v3/ui/schemaorg/product/",
    "https://www.woolworths.com.au/apis/ui/product/detail/",
]


# test
def load_page(w, product_id: int, page_id: int) -> str:
    w.get(pages[page_id] + str(product_id))
    # Give it some time to load the page
    time.sleep(random.randint(1000, 3000) / 1000)
    return w.page_source


def jsonify(s: str) -> object:
    """Takes string and converts to json"""
    # Delete everything until the first '{'
    index_open = s.find("{")
    if index_open != -1:
        s = s[index_open:]

    # Delete everything after the last '}'
    index_close = s.rfind("}")
    if index_close != -1:
        s = s[: index_close + 1]

    return json.loads(s)


def get_data(product_id: int) -> Product:
    from selenium import webdriver

    # Set up Firefox options
    options = Options()
    options.set_preference("devtools.jsonview.enabled", False)
    webdriver = webdriver.Firefox(options=options)
    load_page(webdriver, product_id, 0)
    brief, detailed = (
        jsonify(load_page(webdriver, product_id, 1)),
        jsonify(load_page(webdriver, product_id, 2)),
    )
    webdriver.quit()
    return Product(
        store="Woolies Store",
        product_name=detailed["Product"]["Name"],
        brand=brief["brand"]["name"],
        category=detailed["PrimaryCategory"]["Department"],
        price=detailed["Product"]["Price"],
        unit_price=detailed["Product"]["CupPrice"],
        original_price=detailed["Product"]["WasPrice"],
        availability=detailed["Product"]["IsAvailable"],
        image_url=brief["image"],
        product_url=pages[0] + str(product_id),
        weight=detailed["Product"]["PackageSize"],
        description=detailed["Product"]["FullDescription"],
    )


def get_data_from_url(url: str):
    match = re.search(r"productdetails/(\d+)/", url)
    return get_data(int(match.group(1))) if match else None

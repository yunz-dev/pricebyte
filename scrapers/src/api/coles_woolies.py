from utils.model import ApiProduct, ApiProducts
from os import getenv
import requests

MAX_PAGE_SIZE = 20

def query_products(store: str, product_name: str) -> ApiProducts:
    prefix = ""
    if store == "Woolies Store":
        prefix = "WOOLIES"
    elif store == "Coles Store":
        prefix = "COLES"
    else:
        return ApiProducts(api_uses=0, products=[])

    api_url = getenv(prefix + "_API_URL")
    api_host = getenv(prefix + "_API_HOST")
    api_key = getenv(prefix + "_API_KEY")

    if None in (api_url, api_host, api_key):
        return ApiProducts(api_uses=0, products=[])

    params = {
        "query": product_name,
        "size": MAX_PAGE_SIZE
    }
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": api_host
    }

    page_count = None
    page = 1
    api_uses = 0
    products = []
    while not page_count or page <= page_count:
        res = requests.get(api_url, headers=headers, params=params)
        api_uses += 1
        if res.status_code != 200:
            break
        res_json = res.json()
        if not page_count:
            page_count = res_json.get("total_pages", 0)
        for product in res_json.get("results", []):
            products.append(ApiProduct(
                store=store,
                price=product.get("current_price", 0),
                product_name=product.get("product_name", ""),
                brand=product.get("product_brand", ""),
                weight=product.get("product_size", ""),
                product_url=product.get("url", "")
            ))
        page += 1
    return ApiProducts(api_uses=api_uses, products=products)

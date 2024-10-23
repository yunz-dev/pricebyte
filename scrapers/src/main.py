from fastapi import FastAPI

from scrapers.woolies import get_data, get_data_from_url

app = FastAPI()


@app.get("/woolies-store/id/{product_id}")
def get_woolies_store_by_id(product_id: int):
    """
    Returns product details in json

    Parameters:
    - product_id (int): the id of the woolies product

    Returns:
    - json: product details
    """
    return get_data(product_id)


@app.get("/woolies-store/page/{product_page}")
def get_woolies_store_by_page(product_page: str):
    """
    Returns product details in json

    Parameters:
    - product page

    Returns:
    - json: product details
    """
    return get_data_from_url(product_page)

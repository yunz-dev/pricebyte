from fastapi import FastAPI

from scrapers.woolies import get_data
from scrapers.iga import get_iga_product
from scrapers.aldi import scrape_product

app = FastAPI(
    title="PriceByte Scraping API",
    description="Scrape Woolies, Coles and Aldi",
    version="0.1.0",
    contact={
        "name": "yunz-dev",
    },
    license_info={
        "name": "GNU GPL v3.0",
        "url": "https://www.gnu.org/licenses/gpl-3.0.en.html",
    },
)


@app.get("/heart")
def heart():
    return {"message": "healthy"}


@app.get("/woolies-store/id/{product_id}")
def get_woolies_store_by_id(product_id: int):
    """

    Parameters:
    - **product_id** (int): the id of the woolies product

    Returns:
    - **json**: product details

    #### NOTE: API has a ~5 second delay due to scraping limitations
    """
    return get_data(product_id)

@app.get("/iga-store/store/{store_id}/id/{product_id}")
def get_iga_product_by_id(product_id: int, store_id: int):
    """

    Parameters:
    - **product_id** (int): the id of the iga product

    Returns:
    - **json**: product details
    """
    return get_iga_product(product_id, store_id)

@app.get("/aldi-store/page")
def get_aldi_product_by_url(product_page: str):
    """

    Parameters:
    - **product_url** (string): the url of the aldi product

    Returns:
    - **json**: product details
    """
    return scrape_product(product_page)

# NOTE: USELESS
# @app.get("/woolies-store/page/")
# def get_woolies_store_by_page(product_page: str):
#     """
#     Returns product details in json
#     Parameters:
#     - product page
#     Returns:
#     - json: product details
#     """
#     return get_data_from_url(product_page)

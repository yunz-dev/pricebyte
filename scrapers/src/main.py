from fastapi import FastAPI

from scrapers.woolies import get_data, get_data_from_url

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

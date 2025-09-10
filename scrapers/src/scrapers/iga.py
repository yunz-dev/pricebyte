import re
import time
import requests
from utils.model import IGAProductV1

iga_categories = {
    "fruit-and-vegetable": ["fruit", "vegetables", "salads"],


}

def scrape_iga_category(subCategory: str):
    """
    Scrapes all products from a given IGA category.
    Parameters:
        category_name (str):    Name of the category to scrape
    Returns:
        all_products (list):    List of IGAProductV1 models each representing a product of the category
    """

    product_list = []

    # Construct the base URL for the API call
    base_url = f"https://www.igashop.com.au/api/storefront/stores/32600/categories/{subCategory}/search"
    
    curr_scraped = 0

    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }

    while True:

        if not curr_scraped:
            url = f"{base_url}?&take=100"
        else:
            url = f"{base_url}?skip={curr_scraped}&take=100"
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            results = data.get("items", [])
            total_results = len(results)

            print(f"Scraping products {curr_scraped + 1} to {curr_scraped + total_results}")
            
            for item in results:
                # description=item.get("description"),
                unitOfMeasure = item.get("unitOfMeasure")
                unitOfMeasure = f"{unitOfMeasure.get("size", "")} {unitOfMeasure.get("abbreviation") or "each"}"

                unitOfSize = item.get("unitOfSize")
                unitOfSize = f"{unitOfSize.get("size", "")} {unitOfSize.get("abbreviation") or "each"}"

                product = IGAProductV1(
                    id=int(item.get("productId")),
                    name=item.get("name"),
                    brand=item.get("brand"),
                    price=float(item.get("priceNumeric")),
                    old_price=float(item.get("wasPriceNumeric", item.get("priceNumeric"))),
                    on_sale=1 if item.get("priceLabel") == "Special" else 0,
                    available=item.get("available"),
                    image_url=item.get("image", {}).get("default", ""),
                    unit_price=float(item.get("pricePerUnit").strip("$").replace("/", " ").split(" ")[0]),
                    unitMeasure=unitOfMeasure,
                    unitSize=unitOfSize
                )
                product_list.append(product)

            if total_results != 100:
                break

            curr_scraped += total_results

            time.sleep(1)

        except Exception as e:
            print(f"Error scraping products {curr_scraped + 1} to {curr_scraped + 100}: {e}")
            break
    
    return product_list



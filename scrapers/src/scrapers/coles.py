from utils.model import ColesProductV1, PriceUpdates, Scraper
from typing import List, Tuple
import requests
import time
import math

build_id = "20250905.1-05c3ec1671ec3cc5e81508a6fa1ba52812155cc3" # Cannot be acquired with API, must be scraped with Selenium or PlayWright

coles_categories = {
    "Meat and Seafood": "meat-seafood", "Fruit and Vegtables": "fruit-vegetables", "Dairy Eggs and Fridge": "dairy-eggs-fridge", 
    "Bakery": "bakery", "Deli Foods": "deli", "Pantry": "pantry", "Dietary World Foods": "dietary-world-foods", 
    "Snacks and Chocolates": "chips-chocolates-snacks", "Drinks": "drinks", "Frozen": "frozen", "Household": "household", 
    "Health and Beauty": "health-beauty", "Baby": "baby", "Pet": "pet", "Liquorland": "liquorland", "Tobacco": "tobacco"
}

class ColesScraper(Scraper):

    def __init__(self, category_list, build_id):
        super().__init__(category_list)
        self.build_id = build_id
    
    def scrape_category(self) -> List[PriceUpdates]:
        """
        Scrapes all product ids and prices from all categories
        Parameters:
            category_list (List[str]):                  List of category names
        Returns:
            product_list (List[Tuple[int, float]]):    List of product_ids and their current price
        """
        price_update_list = []
        page_size = 48

        # Create API request headers
        headers = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'x-nextjs-data': '1'
        }
        for category_name in self.category_list:

            # Construct the base URL for the API call
            base_url = f"https://www.coles.com.au/_next/data/{build_id}/en/browse/{category_name}.json?slug={category_name}"

            page_number = 1
            total_pages = 1
            while page_number <= total_pages:
                
                # Create API url to send GET request
                url = f"{base_url}&page={page_number}" if page_number > 1 else base_url
                
                try:
                    response = requests.get(url, headers=headers)
                    response.raise_for_status()
                    data = response.json()
                    
                    # Find results list within the JSON
                    search_results = data.get('pageProps', {}).get('searchResults', {})
                    results = search_results.get('results', [])

                    # Calculate total number of pages on the first request
                    total_results = search_results.get('noOfResults', 0)
                    if page_number == 1: # Only print it once
                        total_pages = math.ceil(total_results / page_size)
                        print(f"Found {total_results} total results, across {total_pages} pages.")

                    print(f"Scraping page {page_number}")

                    for item in results:
                        # Only process product items
                        if item.get('_type') == 'PRODUCT':
                            priceUpdate = PriceUpdates(
                                store_product_id=item.get("id"),
                                store="Coles",
                                new_price=(item.get('pricing') or {}).get("now")
                            )
                            price_update_list.append(priceUpdate)
                    
                    # Increment the page number
                    page_number += 1
                    
                    time.sleep(1) 
                    
                except Exception as e:
                    print(f"Error scraping page {page_number} of {category_name}: {e}")
                    break

        return price_update_list

    
    def scrape_product(self, id):
        pass

    def price_changed(self, product: Tuple[int, float]) -> bool:
        pass

    def is_new_product(self, id: int) -> bool:
        pass

    def get_store_name(self) -> str:
        return "Woolworths"

def scrape_coles_category(category_name="deli") -> list[ColesProductV1]:
    """
    Scrapes all products from a given category.
    Parameters:
        category_name (str):    Name of the category to scrape
    Returns:
        all_products (list):    List of ColesProductV1 models each representing a product of the category
    """
    
    product_list = []

    # Construct the base URL for the API call
    base_url = f"https://www.coles.com.au/_next/data/{build_id}/en/browse/{category_name}.json?slug={category_name}"

    page_number = 1
    page_size = 48
    total_pages = 1

    # Create API request headers
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'x-nextjs-data': '1'
    }

    while page_number <= total_pages:
        
        # Create API url to send GET request
        url = f"{base_url}&page={page_number}" if page_number > 1 else base_url
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            # Find results list within the JSON
            search_results = data.get('pageProps', {}).get('searchResults', {})
            results = search_results.get('results', [])

            # Calculate total number of pages on the first request
            total_results = search_results.get('noOfResults', 0)
            if page_number == 1: # Only print it once
                total_pages = math.ceil(total_results / page_size)
                print(f"Found {total_results} total results, across {total_pages} pages.")

            print(f"Scraping page {page_number}")

            for item in results:
                # Only process product items
                if item.get('_type') == 'PRODUCT':
                    pricing = item.get('pricing') or {}
                    unit_pricing = pricing.get('unit', {})
                    product = ColesProductV1(
                        store="coles",
                        id=item.get("id"),
                        name=item.get("name"),
                        brand=item.get("brand", "N/A"),
                        price=pricing.get('now'),
                        old_price=pricing.get('was'),
                        on_sale=1 if pricing.get('onlineSpecial') else 0,
                        unit_price=unit_pricing.get('price')
                    )
                    product_list.append(product)
            
            # Increment the page number
            page_number += 1
            
            time.sleep(1) 
            
        except Exception as e:
            print(f"Error scraping page {page_number}: {e}")
            break

    return product_list

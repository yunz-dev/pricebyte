import time
from typing import List
from math import ceil
import requests
from utils.model import Scraper, PriceUpdates, ProductInfo, Store
from log import log, detailed_log
import re


class ColesScraper(Scraper):
    def __init__(self):
        self.build_id = "20250910.2-94eac02bf9675b685ea17b771023fada9319d0f3"
        self.base_url = f"https://www.coles.com.au/_next/data/{self.build_id}/en/browse/"
        self.detail_url = f"https://www.coles.com.au/_next/data/{self.build_id}/en/product/"
        self.limit = 48
        self.headers = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'x-nextjs-data': '1'
        }
        self.categories = {
            "Meat and Seafood": "meat-seafood", "Fruit and Vegtables": "fruit-vegetables", 
            "Dairy Eggs and Fridge": "dairy-eggs-fridge", "Bakery": "bakery", "Deli Foods": "deli", 
            "Pantry": "pantry", "Dietary World Foods": "dietary-world-foods", 
            "Snacks and Chocolates": "chips-chocolates-snacks", "Drinks": "drinks", 
            "Frozen": "frozen", "Household": "household", "Health and Beauty": "health-beauty", 
            "Baby": "baby", "Pet": "pet", "Liquorland": "liquorland", "Tobacco": "tobacco"
        }
        self.categories = {"Meat and Seafood": "meat-seafood"}

    def scrape_category(self) -> List[PriceUpdates]:
        """Scrape all categories and return a list of PriceUpdates"""
        all_products = []
        for cat_name, cat_key in self.categories.items():
            log(f"🗂️  Category: {cat_name} ({cat_key})")

            # Construct the category URL for the API call
            base_url = f"{self.base_url}{cat_key}.json?slug={cat_key}"

            page = 1
            total_pages = 1
            while page <= total_pages:
                
                url = f"{base_url}&page={page}" if page > 1 else base_url
                
                try:
                    response = requests.get(url, headers=self.headers)
                    if not response.ok:
                        log(
                            f"❌ HTTP {response.status_code} for {
                                cat_name} offset {page * (self.limit - 1)}"
                        )
                        break
                    
                    data = response.json()
                    
                    # Find results list within the JSON
                    search_results = data.get('pageProps', {}).get('searchResults', {})
                    items = search_results.get('results', [])
                    
                    # Calculate total number of pages on the first request
                    total_results = search_results.get('noOfResults', 0)
                    if page == 1: # Only print it once
                        total_pages = ceil(total_results / self.limit)
                        log(f"Found {total_results} total results, across {total_pages} pages.")


                    for item in items:
                        # Only process product items
                        
                        if item.get('_type') == 'PRODUCT':
                            # TODO: Solve items being unavailable having no price attribute (default set to -1 currently)
                            priceUpdate = PriceUpdates(
                                store_product_id=item.get("id"),
                                product_name=f"{item.get("brand")} {item.get("name")} {item.get("size")}",
                                store=Store.Coles,
                                price=(item.get('pricing') or {}).get("now") or -1
                            )
                            log(priceUpdate)
                            all_products.append(priceUpdate)
                    detailed_log(
                        f"  • grabbed {len(items):2}  (page={
                            page}, offset={page * (self.limit - 1)})"
                    )
                    
                    # Increment the page number
                    page += 1
                    
                    time.sleep(0.4) 
                    
                except Exception as e:
                    log(f"❌ Exception for {cat_name} page {page}: {e}")
                    break

        log(f"📦 Collected {len(all_products)} products total")
        return all_products

    def scrape_product(self, product: PriceUpdates) -> ProductInfo:
        """Fetch detailed information for a specific product"""

        try:
            product_name_url = "-".join(re.sub(r'[|&]', "", product.product_name).lower().split())
            log(product_name_url)
            url = f"{self.detail_url}{product_name_url}-{product.store_product_id}.json?slug={product_name_url}-{product.store_product_id}"
            response = requests.get(
                url, headers=self.headers, timeout=10
            )

            if not response.ok:
                log(f"❌ HTTP Error for product id {product.store_product_id}: {response.status_code}")
                return ProductInfo(
                    store_product_id=product.store_product_id,
                    store=product.store,
                    product_name=product.product_name,
                    price=product.price,
                    details={},
                )

            product_data = response.json().get("pageProps", {}).get("product")

            details = product_data

            current_price = product.price
            if product_data.get("price", {}).get("amountRelevantDisplay"):
                try:
                    api_price = float(product_data.get("pricing", {}).get("now") or -1)
                    current_price = api_price
                except (ValueError, AttributeError):
                    pass

            return ProductInfo(
                store_product_id=product.store_product_id,
                store=product.store,
                product_name=product.product_name,
                price=current_price,
                details=details,
            )

        except Exception as e:
            log(f"❌ Exception for product id {product.store_product_id}: {e}")
            return ProductInfo(
                store_product_id=product.store_product_id,
                store=product.store,
                product_name=product.product_name,
                price=product.price,
                details={},
            )  

    def price_changed(self, product: PriceUpdates) -> bool:
        """Redundant"""
        return False

    def is_new_product(self, product: PriceUpdates) -> bool:
        """Redundant"""
        return False

    def get_store_name(self) -> str:
        """Returns the supermarket name"""
        return "Coles"


# For testing
if __name__ == "__main__":
    scraper = ColesScraper()
    products = scraper.scrape_category()
    if products:
        detailed_info = scraper.scrape_product(products[0])
        log(f"Detailed info for {detailed_info.product_name}: {
            detailed_info.price}")

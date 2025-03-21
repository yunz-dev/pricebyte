import requests
import time
import json
import os
from typing import List, Dict, Any

class WoolworthsRapidAPIScraper:
    BASE_URL = "https://woolworths-products-api.p.rapidapi.com/woolworths/product-search/"
    HEADERS = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY", ""),
        "x-rapidapi-host": "woolworths-products-api.p.rapidapi.com"
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def search_products(self, query: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """Search for products with pagination"""
        params = {
            "query": query,
            "page": page,
            "pageSize": page_size
        }
        try:
            response = self.session.get(self.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error searching products: {e}")
            return {"results": [], "totalResults": 0, "totalPages": 0}

    def get_all_products(self, query: str = "") -> List[Dict[str, Any]]:
        """Get all products for a query by paginating through all pages"""
        all_products = []
        page = 1
        page_size = 20

        while True:
            print(f"Fetching page {page} for Woolworths...")
            data = self.search_products(query, page, page_size)
            products = data.get("results", [])
            all_products.extend(products)

            total_pages = data.get("totalPages", 0)
            if page >= total_pages or not products:
                break

            page += 1
            time.sleep(2)  # Rate limiting: 1 request every 2 seconds

        return all_products

    def transform_product(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Transform API response to standard format"""
        return {
            "store": "woolworths",
            "store_product_id": str(product.get("barcode", "")),
            "product_name": product.get("productName", ""),
            "brand": product.get("productBrand", ""),
            "category": "",  # API doesn't provide category
            "price": product.get("currentPrice", 0.0),
            "unit_price": "",  # API doesn't provide unit price
            "size": product.get("productSize", ""),
            "availability": True,  # Assume available if returned
            "image_url": "",  # API doesn't provide image
            "product_url": product.get("url", "")
        }

    def scrape_all(self) -> List[Dict[str, Any]]:
        """Scrape all products (using empty query to get everything)"""
        raw_products = self.get_all_products("")
        return [self.transform_product(p) for p in raw_products]

if __name__ == "__main__":
    scraper = WoolworthsRapidAPIScraper()
    products = scraper.scrape_all()
    print(f"Scraped {len(products)} products from Woolworths")
    with open("woolworths_products.json", "w") as f:
        json.dump(products, f, indent=2)
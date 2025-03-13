import requests
import json
from woolworths_rapidapi import WoolworthsRapidAPIScraper
from coles_rapidapi import ColesRapidAPIScraper
from typing import List, Dict, Any

INGEST_URL = "http://localhost:8000/api/products"

def post_products_to_ingest(products: List[Dict[str, Any]], store: str):
    """Post products to the ingest API in batches"""
    batch_size = 50  # Post in batches to avoid overwhelming
    for i in range(0, len(products), batch_size):
        batch = products[i:i + batch_size]
        payload = {
            "store": store,
            "products": batch
        }
        try:
            response = requests.post(INGEST_URL, json=payload)
            response.raise_for_status()
            print(f"Posted batch {i//batch_size + 1} for {store}: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error posting batch for {store}: {e}")
            # Continue with next batch

def main():
    print("Starting Woolworths scraper...")
    woolworths_scraper = WoolworthsRapidAPIScraper()
    woolworths_products = woolworths_scraper.scrape_all()
    print(f"Scraped {len(woolworths_products)} products from Woolworths")

    print("Posting Woolworths products to ingest...")
    post_products_to_ingest(woolworths_products, "woolworths")

    print("Starting Coles scraper...")
    coles_scraper = ColesRapidAPIScraper()
    coles_products = coles_scraper.scrape_all()
    print(f"Scraped {len(coles_products)} products from Coles")

    print("Posting Coles products to ingest...")
    post_products_to_ingest(coles_products, "coles")

    print("Scraping and ingestion complete!")

if __name__ == "__main__":
    main()
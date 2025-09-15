import requests
import time
from typing import List
from utils.model import Scraper, PriceUpdates, ProductInfo, Store
from log import log, detailed_log


class AldiScraper(Scraper):
    def __init__(self):
        self.base_url = "https://api.aldi.com.au/v3/product-search"
        self.detail_url = "https://api.aldi.com.au/v2/products"
        self.limit = 30
        self.max_pages = 120
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "origin": "https://www.aldi.com.au",
            "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
        }
        self.categories = {
            "fruit_veg": 950000000,
            "meat_seafood": 940000000,
            "deli_chilled_meats": 930000000,
            "dairy_eggs": 960000000,
            "pantry": 970000000,
            "bakery": 920000000,
            "freezer": 980000000,
            "drinks": 1000000000,
            "health_beauty": 1040000000,
            "baby": 1030000000,
            "cleaning_household": 1050000000,
            "pets": 1020000000,
            "liquor": 1010000000,
            "snacks": 1588161408332087,
            "front_of_store": 1588161408332092,
        }

    def scrape_category(self) -> List[PriceUpdates]:
        """Scrape all categories and return a list of PriceUpdates"""
        all_products = []

        for cat_name, cat_key in self.categories.items():
            log(f"🗂️  Category: {cat_name} ({cat_key})")

            for page in range(self.max_pages):
                offset = page * self.limit
                params = {
                    "currency": "AUD",
                    "serviceType": "walk-in",
                    "categoryKey": cat_key,
                    "limit": self.limit,
                    "offset": offset,
                    "sort": "relevance",
                    "testVariant": "A",
                    "servicePoint": "G452",
                }

                try:
                    resp = requests.get(
                        self.base_url, headers=self.headers, params=params, timeout=15
                    )
                    if not resp.ok:
                        log(
                            f"❌ HTTP {resp.status_code} for {
                                cat_name} offset {offset}"
                        )
                        break

                    items = resp.json().get("data", [])
                    if not items:
                        if page == 0:
                            log("⚠️  Empty category (no items returned).")
                        else:
                            detailed_log("✅ Reached end of list.")
                        break

                    for item in items:
                        price_data = item.get("price", {})
                        price = (
                            price_data.get("amountRelevantDisplay")
                            if price_data
                            else None
                        )

                        if not price or not item.get("sku"):
                            continue

                        try:
                            price_float = float(
                                price.replace("$", "").replace(",", ""))
                        except (ValueError, AttributeError):
                            continue

                        price_update = PriceUpdates(
                            store_product_id=int(item.get("sku")),
                            store=Store.ALDI,
                            product_name=item.get("name", ""),
                            price=price_float,
                        )
                        all_products.append(price_update)

                    detailed_log(
                        f"  • grabbed {len(items):2}  (page={
                            page}, offset={offset})"
                    )
                    time.sleep(0.4)  # be polite

                except Exception as e:
                    log(f"❌ Exception for {cat_name} page {page}: {e}")
                    break

        log(f"📦 Collected {len(all_products)} products total")
        return all_products

    def scrape_product(self, product: PriceUpdates) -> ProductInfo:
        """Fetch detailed information for a specific product"""
        sku = str(product.store_product_id).zfill(
            18)  # Ensure 18-digit string format

        try:
            url = f"{self.detail_url}/{sku}"
            params = {"servicePoint": "G452", "serviceType": "walk-in"}

            response = requests.get(
                url, headers=self.headers, params=params, timeout=10
            )

            if not response.ok:
                log(f"❌ HTTP Error for SKU {sku}: {response.status_code}")
                return ProductInfo(
                    store_product_id=product.store_product_id,
                    store=product.store,
                    product_name=product.product_name,
                    price=product.price,
                    details={},
                )

            product_data = response.json().get("data", {})

            details = {
                "sku": product_data.get("sku"),
                "name": product_data.get("name"),
                "brand": product_data.get("brandName"),
                "description": product_data.get("description"),
                "size": product_data.get("sellingSize"),
                "price_per_100g": product_data.get("price", {}).get(
                    "comparisonDisplay"
                ),
                "storage": product_data.get("storageInstructions"),
                "country_of_origin": product_data.get("countryOrigin"),
                "on_sale_display": product_data.get("onSaleDateDisplay"),
                "not_for_sale": product_data.get("notForSale"),
                "url_slug": product_data.get("urlSlugText"),
                "categories": [
                    cat.get("name") for cat in product_data.get("categories", [])
                ],
                "image_urls": [
                    asset["url"]
                    .replace("{width}", "800")
                    .replace("{slug}", product_data.get("urlSlugText", ""))
                    for asset in product_data.get("assets", [])
                ],
                "allergens": product_data.get("allergens"),
                "warnings": product_data.get("warnings"),
                "ingredients": product_data.get("ingredients"),
            }

            current_price = product.price
            if product_data.get("price", {}).get("amountRelevantDisplay"):
                try:
                    api_price = float(
                        product_data["price"]["amountRelevantDisplay"]
                        .replace("$", "")
                        .replace(",", "")
                    )
                    current_price = api_price
                except (ValueError, AttributeError):
                    pass

            return ProductInfo(
                store_product_id=product.store_product_id,
                store=product.store,
                product_name=product_data.get("name", product.product_name),
                price=current_price,
                details=details,
            )

        except Exception as e:
            log(f"❌ Exception for SKU {sku}: {e}")
            return ProductInfo(
                store_product_id=product.store_product_id,
                store=product.store,
                product_name=product.product_name,
                price=product.price,
                details={},
            )

    def price_changed(self, product: PriceUpdates) -> bool:
        return False

    def is_new_product(self, product: PriceUpdates) -> bool:
        return False

    def get_store_name(self) -> str:
        return "ALDI"


# For testing
if __name__ == "__main__":
    scraper = AldiScraper()
    products = scraper.scrape_category()
    if products:
        detailed_info = scraper.scrape_product(products[0])
        log(f"Detailed info for {detailed_info.product_name}: {
            detailed_info.price}")

import requests
import json
import pandas as pd
from time import sleep
import os

# Create directory if it doesn't exist
os.makedirs("raw/products", exist_ok=True)

# Read categories from Excel
categories_df = pd.read_csv("data.csv")

def clean_category_id(category_id):
    return category_id.replace("_", "-")

def clean_format_object(format_obj):
    cleaned = format_obj.replace('\\"', '"')
    try:
        json_obj = json.loads(cleaned)
        return json.dumps(json_obj)
    except:
        return format_obj

categories_df["categoryId"] = categories_df["categoryId"].apply(clean_category_id)
categories_df["formatObject"] = categories_df["formatObject"].apply(clean_format_object)

# URL endpoint
url = "https://www.woolworths.com.au/apis/ui/browse/category"

# Headers - updated to be less detectable
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "Origin": "https://www.woolworths.com.au",
    "Referer": "https://www.woolworths.com.au/shop/browse/fruit-veg",
    "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}

max_retries = 3
cookies = {}

def fetch_category_products(category_row):
    page_number = 1
    category_products = []

    payload = {
        "categoryId": category_row["categoryId"],
        "categoryVersion": "v2",
        "enableAdReRanking": False,
        "filters": [],
        "flags": {"EnablePersonalizationCategoryRestriction": True},
        "formatObject": category_row["formatObject"],
        "gpBoost": 0,
        "groupEdmVariants": False,
        "isBundle": False,
        "isHideUnavailableProducts": False,
        "isMobile": False,
        "isRegisteredRewardCardPromotion": False,
        "isSpecial": False,
        "location": category_row["location"],
        "pageNumber": 1,
        "pageSize": 12,
        "sortType": "TraderRelevance",
        "token": "",
        "url": category_row["url"],
    }

    print(f"\n📋 Debug Info for {category_row['L1_category']}:")
    print(f"Category ID: {payload['categoryId']}")
    print(f"Format Object: {payload['formatObject']}")
    print(f"Location: {payload['location']}")
    print(f"URL: {payload['url']}\n")

    # Only process first page for testing
    print(f"📃 Fetching {category_row['L1_category']} - Page {page_number}...")
    payload["pageNumber"] = page_number

    # Make request with retries and timeout
    response = None
    for attempt in range(max_retries):
        try:
            print(f"  📡 Attempt {attempt + 1}/{max_retries} with 15s timeout...")
            response = requests.post(
                url, 
                headers=headers, 
                data=json.dumps(payload), 
                cookies=cookies,
                timeout=15
            )
            response.raise_for_status()
            print(f"  ✅ Request successful (Status: {response.status_code})")
            break
        except requests.Timeout:
            print(f"  ⏰ Request timed out on attempt {attempt + 1}")
            if attempt < max_retries - 1:
                print("  🔄 Retrying in 5 seconds...")
                sleep(5)
            else:
                print("  ❌ All attempts timed out - skipping this category")
                return []
        except requests.RequestException as e:
            print(f"  ❌ Error on attempt {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:
                print("  🔄 Retrying in 5 seconds...")
                sleep(5)
            else:
                print("  ❌ Failed to fetch page after all retries")
                return []

    if not response:
        return []

    try:
        data = response.json()
        if not data.get("Bundles"):
            print("❌ API Response Debug:")
            print(json.dumps(data, indent=2)[:500])
            return []
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON response: {str(e)}")
        return []

    # Parse products
    for bundle in data.get("Bundles", []):
        for product in bundle.get("Products", []):
            try:
                product_data = {
                    "Category": category_row["L1_category"],
                    "Name": product.get("Name"),
                    "DisplayName": product.get("DisplayName"),
                    "Stockcode": product.get("Stockcode"),
                    "Barcode": product.get("Barcode"),
                    "Price": product.get("Price"),
                    "Unit": product.get("Unit"),
                    "CupPrice": product.get("CupString"),
                    "InStock": product.get("IsInStock"),
                    "IsOnSpecial": product.get("IsOnSpecial"),
                    "Image": product.get("LargeImageFile"),
                    "Description": product.get("Description", "").strip(),
                    "URL": f"https://www.woolworths.com.au/shop/productdetails/{product.get('Stockcode')}",
                }
                category_products.append(product_data)
            except Exception as e:
                print(f"❌ Error parsing product: {str(e)}")
                continue

    print(f"✅ Found {len(category_products)} products")
    return category_products

# Test just the first category (Fruit_Veg)
first_category = categories_df.iloc[0]
print(f"🧪 Testing category: {first_category['L1_category']}")

products = fetch_category_products(first_category)

if products:
    df = pd.DataFrame(products)
    df.to_csv("raw/products/test_products.csv", index=False)
    print(f"✅ Successfully saved {len(products)} products to test_products.csv")
else:
    print("❌ No products retrieved")
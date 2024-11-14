import requests
from model import Product


def fetch_product(url: str, store: int, product: int) -> dict:
    try:
        response = requests.get(f"{url}/stores/{store}/products/{product}")
        response.raise_for_status()  # Raise an error for bad status codes (4xx, 5xx)
        return response.json()  # Convert JSON response to a Python dictionary
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return {}


def parse_data(data: dict = None):
    price = data.get("price")
    unit_price = data.get("unitPrice")
    name = data.get("name")
    brand = data.get("brand")
    weight = data.get("unitsOfSize", {}).get("size")
    store = None
    category = data.get("defaultCategory")
    image_url = data.get("primaryImage", {}).get("default")
    product_url = None
    description = data.get("description")
    original_price = data.get("wasPrice")
    availability = data.get("available")
    print(f"Price: {price}")
    print(f"Unit Price: {unit_price}")
    print(f"Name: {name}")
    print(f"Brand: {brand}")
    print(f"Weight: {weight}g")
    print(f"Store: {store}")
    print(f"Category: {category}")
    print(f"Image URL: {image_url}")
    print(f"Product URL: {product_url}")
    print(f"Description: {description}")
    print(f"Original Price: {original_price}")
    print(f"Available: {availability}")


data = fetch_product("https://www.igashop.com.au/api/storefront", 32600, 777071)
parse_data(data)

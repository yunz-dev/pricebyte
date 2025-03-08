import re

import requests
from utils.model import Product


def fetch_product(url: str, store: int, product: int) -> dict:
    try:
        response = requests.get(f"{url}/stores/{store}/products/{product}")
        response.raise_for_status()  # Raise an error for bad status codes (4xx, 5xx)
        return response.json()  # Convert JSON response to a Python dictionary
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return {}


def get_product_link(product_name: str) -> str:
    product_name = product_name.replace("-", " ")
    product_name = re.sub(r"[^\w\s]", "", product_name).split()
    return "-".join(product_name).lower()


def get_iga_product(product_id: int, store_id: int = 32600) -> Product:
    data = fetch_product(
        "https://www.igashop.com.au/api/storefront", store_id, product_id
    )

    product_name = data.get("name")
    product_link = get_product_link(product_name)
    product_url = f"https://www.igashop.com.au/product/{product_link}-{product_id}"

    # combine weight and weight type
    weight_data = data.get("unitsOfSize", {})
    weight = weight_data.get("size")
    match weight_data.get("type"):
        case "kilogram":
            weight_type = "kg"
        case "gram":
            weight_type = "g"
        case "litre":
            weight_type = "L"
        case "millilitre":
            weight_type = "mL"
        case _:
            weight_type = "g"

    # replace all letters and symbols in price data

    try:
        price = float(re.sub(r"[^0-9.]", "", data.get("price", "")))
        try:
            unit_price = float(re.sub(r"[^0-9.]", "", data.get("unitPrice", "")))
        except ValueError:
            unit_price = price

        try:
            original_price = (
                float(re.sub(r"[^0-9.]", "", data.get("wasPrice", "")))
                if data.get("wasPrice")
                else price
            )
        except ValueError:
            original_price = price
    except ValueError:
        price = unit_price = original_price = -1

    return Product(
        store="IGA Store",
        product_name=data.get("name"),
        brand=data.get("brand"),
        category=data.get("defaultCategory"),
        price=price,
        unit_price=unit_price,
        original_price=original_price,
        availability=data.get("available"),
        image_url=data.get("primaryImage", {}).get("default"),
        product_url=product_url,
        weight=f"{weight}{weight_type}",
        description=data.get("description")
        .replace("<br/>", "")
        .replace("<br />", "")
        .replace("|", " |"),
    )

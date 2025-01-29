import random
from typing import List, Dict, Any
from utils.model import PriceUpdates, Store


class FakeDataGenerator:
    """Generator for fake Aldi product data for testing purposes."""

    # Fake product data
    FAKE_PRODUCTS = [
        {
            "store_product_id": 1001,
            "product_name": "Simply Nature Organic Bananas",
            "price": 1.99,
        },
        {
            "store_product_id": 1002,
            "product_name": "Never Any! Chicken Breast",
            "price": 4.99,
        },
        {
            "store_product_id": 1003,
            "product_name": "LiveGFree Gluten Free Bread",
            "price": 3.49,
        },
        {
            "store_product_id": 1004,
            "product_name": "Simply Nature Almond Milk",
            "price": 2.29,
        },
        {
            "store_product_id": 1005,
            "product_name": "Earth Grown Plant Based Burgers",
            "price": 3.99,
        },
        {
            "store_product_id": 1006,
            "product_name": "Livewell Greek Yogurt",
            "price": 4.49,
        },
        {
            "store_product_id": 1007,
            "product_name": "Dakota's Pride Pasta",
            "price": 0.95,
        },
        {"store_product_id": 1008, "product_name": "Carlini Olive Oil", "price": 2.99},
    ]

    @classmethod
    def generate_price_updates_list(cls) -> List[PriceUpdates]:
        """Generate a list of fake PriceUpdates objects."""
        products = []
        for product_data in cls.FAKE_PRODUCTS:
            products.append(
                PriceUpdates(
                    store_product_id=product_data["store_product_id"],
                    store=Store.ALDI,  # Assuming Store is an enum
                    product_name=product_data["product_name"],
                    price=product_data["price"],
                )
            )

        # Return a random subset for more realistic testing
        return random.sample(products, k=random.randint(3, len(products)))

    @classmethod
    def generate_product_details(cls, product: PriceUpdates) -> Dict[str, Any]:
        """Generate fake detailed product info based on the PriceUpdates input."""
        return {
            "brand": cls.get_brand_from_name(product.product_name),
            "category": cls.get_category_from_name(product.product_name),
            "description": f"High quality {product.product_name.lower()} available at Aldi",
            "weight": f"{random.uniform(100, 2000):.0f}g",
            "ingredients": cls.get_ingredients_from_name(product.product_name),
            "nutrition_facts": {
                "calories_per_serving": random.randint(50, 400),
                "fat": f"{random.uniform(0, 20):.1f}g",
                "sodium": f"{random.randint(0, 800)}mg",
                "protein": f"{random.uniform(1, 25):.1f}g",
            },
            "barcode": f"123456{random.randint(100000, 999999)}",
            "availability": random.choice(
                ["In Stock", "Limited Stock", "Out of Stock"]
            ),
            "rating": round(random.uniform(3.5, 5.0), 1),
        }

    @staticmethod
    def get_brand_from_name(product_name: str) -> str:
        """Extract brand name from product name."""
        if "Simply Nature" in product_name:
            return "Simply Nature"
        elif "Never Any!" in product_name:
            return "Never Any!"
        elif "LiveGFree" in product_name:
            return "LiveGFree"
        elif "Earth Grown" in product_name:
            return "Earth Grown"
        elif "Livewell" in product_name:
            return "Livewell"
        elif "Dakota's Pride" in product_name:
            return "Dakota's Pride"
        elif "Carlini" in product_name:
            return "Carlini"
        else:
            return "Aldi Brand"

    @staticmethod
    def get_category_from_name(product_name: str) -> str:
        """Determine product category from name."""
        name_lower = product_name.lower()
        if "banana" in name_lower or "fruit" in name_lower:
            return "Fresh Produce"
        elif "chicken" in name_lower or "meat" in name_lower:
            return "Meat & Poultry"
        elif "bread" in name_lower:
            return "Bakery"
        elif "milk" in name_lower or "yogurt" in name_lower:
            return "Dairy"
        elif "burger" in name_lower:
            return "Frozen Foods"
        elif "pasta" in name_lower:
            return "Pantry Staples"
        elif "oil" in name_lower:
            return "Cooking Essentials"
        else:
            return "General Grocery"

    @staticmethod
    def get_ingredients_from_name(product_name: str) -> str:
        """Generate fake ingredients based on product name."""
        name_lower = product_name.lower()
        if "banana" in name_lower:
            return "Organic bananas"
        elif "chicken" in name_lower:
            return "Chicken breast, water, sea salt"
        elif "bread" in name_lower:
            return "Water, rice flour, tapioca starch, potato starch, yeast, salt"
        elif "milk" in name_lower:
            return "Almondmilk (filtered water, almonds), vitamin E"
        elif "burger" in name_lower:
            return (
                "Water, pea protein, canola oil, refined coconut oil, natural flavors"
            )
        elif "yogurt" in name_lower:
            return "Cultured pasteurized grade A non-fat milk, live active cultures"
        elif "pasta" in name_lower:
            return "Durum wheat semolina, water"
        elif "oil" in name_lower:
            return "Extra virgin olive oil"
        else:
            return "Various ingredients"

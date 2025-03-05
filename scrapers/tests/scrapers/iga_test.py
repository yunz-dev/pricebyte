
from scrapers.iga import get_product_link

def test_get_product_link():
    """Convert product url to id"""
    assert get_product_link("A2 Milk Full Cream Milk") == "a2-milk-full-cream-milk"





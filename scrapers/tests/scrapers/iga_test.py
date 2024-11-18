import pytest

from scrapers.iga import get_iga_product, get_product_id

def test_get_product_id():
    """Convert product url to id"""
    assert get_product_id("https://www.igashop.com.au/product/a2-milk-full-cream-milk-726347") == 726347



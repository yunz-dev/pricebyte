import sys
import os
import pytest

# Add 'src/' to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from scrapers.coles import ColesScraper

@pytest.fixture
def coles_scraper():
    """
    Fixture to initialize and close ColesScraper properly.
    """
    scraper_instance = ColesScraper(headless=True)
    yield scraper_instance
    scraper_instance.browser.close()

def test_scrape_coles_milk(coles_scraper):
    """
    Test that the scraper correctly extracts milk name and price.
    """
    result = coles_scraper.scrape_coles_product("https://www.coles.com.au/product/coles-full-cream-milk-3l-8150288")

    assert isinstance(result, dict)
    assert "name" in result and result["name"] == "Coles Full Cream Milk | 3L"
    assert "price" in result and result["price"]

    if result["discounted"]:
        assert "original_price" in result and result["original_price"]
        assert result["original_price"] > result["price"]
    else:
        assert result["original_price"] is None

def test_scrape_coles_coke(coles_scraper):
    """
    Test that the scraper correctly extracts coke name, price and discount.
    """
    result = coles_scraper.scrape_coles_product("https://www.coles.com.au/product/coca-cola-classic-soft-drink-bottle-1.25l-123011")

    assert isinstance(result, dict)
    assert "name" in result and result["name"] == "Coca-Cola Classic Soft Drink Bottle | 1.25L"
    assert "price" in result and result["price"]

    if result["discounted"]:
        assert "original_price" in result and result["original_price"]
        assert result["original_price"] > result["price"]
    else:
        assert result["original_price"] is None
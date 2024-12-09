import scrapers.aldi as aldi
from bs4 import BeautifulSoup

def test_clean_str():
    assert aldi.clean_str("t\t\n\tt") == "tt"
    assert aldi.clean_str("   a\t\nl   ") == "al"
    assert aldi.clean_str("lorem ipsum dolar ") == "lorem ipsum dolar"


def test_parse_desc():
    assert aldi.parse_desc(desc_ul) == "Good, Cheap"


def test_parse_price():
    assert aldi.parse_price(pricebox) == 1.4


def test_parse_orig_price():
    assert aldi.parse_orig_price(pricebox) == 1.4


def test_parse_unit_price():
    assert aldi.parse_unit_price(pricebox) == 0.7


def test_parse_amount():
    assert aldi.parse_amount(pricebox) == "2L"


desc_ul = BeautifulSoup("""
<div>
 <h2>
  Product Description
 </h2>
 <ul>
  <li>
   Good
  </li>
  <li>
   Cheap
  </li>
 </ul>
</div>
""", "html.parser")

pricebox = BeautifulSoup("""
<div class="detail-box--price-box--price">
 <span>
  Unit
 </span>
 <span class="detail-box--price-box--price--amount box--amount">
  2L
 </span>
 <span>
  Current Price
 </span>
 <span class="box--value">
  $1.
 </span>
 <span class="box--decimal">
  40
 </span>
 <span>
  Unit price
 </span>
 <span class="detail-box--price-box--price--detailamount box--detailamount">
  70c per litre
 </span>
</div>
""", "html.parser")

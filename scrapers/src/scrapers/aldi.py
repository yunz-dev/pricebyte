import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from utils.model import Product

def clean_str(string: str) -> str:
    to_del = {ord(k): None for k in ['\n', '\t']}
    return string.strip().translate(to_del)


def get_all_content(tags: list[Tag]) -> list[str]:
    res = []
    for tag in tags:
        conts = tag.contents
        for child in conts:
            if isinstance(child, NavigableString):
                child = get_str_content(child)
                if child:
                    res.append(child)
    return res


def get_str_content(string: NavigableString | Tag) -> str:
    if not string:
        return ""
    return clean_str(str(string.string))


def parse_category(nav: Tag) -> str:
    if not nav:
        return ""
    categories = nav.find_all("li", class_="breadcrumb-nav--element")
    if len(categories) < 2:
        return ""
    category = categories[-2]
    text = category.find("span", itemprop="name")
    if not text:
        return ""
    return get_str_content(text)


def parse_price(pricebox: Tag) -> float:
    if not pricebox:
        return 0.0
    value = get_str_content(pricebox.find("span", "box--value"))
    decimal = get_str_content(pricebox.find("span", "box--decimal"))
    if not value or not decimal:
        return 0.0
    value = ''.join(c for c in value if c.isnumeric())
    return float(f"{value}.{decimal}")


def parse_unit_price(pricebox: Tag) -> float:
    if not pricebox:
        return 0.0
    full_unit_price = get_str_content(pricebox.find("span", "box--detailamount"))
    if not full_unit_price:
        return 0.0
    unit_price = full_unit_price.split(" ")[0]
    if unit_price.startswith("$"):
        return float(unit_price.replace("$", ""))
    if unit_price.endswith("c"):
        return float("0." + unit_price.replace("c", ""))


def parse_orig_price(pricebox: Tag) -> float:
    if not pricebox:
        return 0
    orig = get_str_content(pricebox.find("span", "box--former-price")).replace("$", "")
    if not orig:
        return parse_price(pricebox)
    return float(orig)


def parse_amount(pricebox: Tag) -> str:
    if not pricebox:
        return ""
    return get_str_content(pricebox.find("span", "box--amount")).replace("$", "")


def parse_image(detail: Tag) -> str:
    if not detail:
        return ""
    img = detail.find("img")
    if not img:
        return ""
    return img.get("src", "")


def parse_name(detail: Tag) -> str:
    if not detail:
        return ""
    title = detail.find("h1", "detail-box--price-box--title")
    if not title:
        return ""
    return get_str_content(title)


def parse_desc(desc_ul: Tag) -> str:
    if not desc_ul:
        return ""
    li_s = desc_ul.find_all("li")
    desc_arr = get_all_content(li_s)
    return ", ".join(desc_arr)


def scrape_product(url: str) -> Product | None:
    """
    Extracts product details from the given grocery product URL.

    :param url: URL of the product page
    :return: Dictionary containing structured product data
    """
    try:
        res = requests.get(url)
    except (requests.exceptions.ConnectionError, requests.exceptions.MissingSchema):
        return
    if res.status_code != 200:
        return
    page = BeautifulSoup(res.content, "html.parser")

    detail = page.find("div", "detail-box")
    desc_ul = page.find("div", "detail-tabcontent")
    nav = page.find("ul", "breadcrumb-nav")
    pricebox = detail.find("div", "detail-box--price-box--price")

    return Product(
        store="Aldi Store",
        product_name=parse_name(detail),
        brand=parse_name(detail),
        category=parse_category(nav),
        price=parse_price(pricebox),
        unit_price=parse_unit_price(pricebox),
        original_price=parse_orig_price(pricebox),
        availability=True,
        image_url=parse_image(detail),
        product_url=url,
        weight=parse_amount(pricebox),
        description=parse_desc(desc_ul)
    )

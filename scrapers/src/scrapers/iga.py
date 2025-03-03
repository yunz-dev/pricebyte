import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from model import Product

def get_price(driver: webdriver.Chrome) -> float:
    price = driver.find_element(By.CSS_SELECTOR, "span.font-bold.leading-none").text
    price = price.replace("$", "")
    return price
    try:
        return round(float(price), 2)
    except ValueError:
        return -1


def get_iga_product(url: str) -> Product:

    options = Options()
    options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())  # Auto-downloads ChromeDriver
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)


    print(driver)
    time.sleep(1)
    product_name = driver.find_element(By.CSS_SELECTOR, "span.line-clamp-3").text
    weight = driver.find_element(By.CSS_SELECTOR, "span.text-base.lg\\:text-lg").text.replace(" Gram", "g")
    image_url = driver.find_element(By.CSS_SELECTOR, "img.iiz__zoom-img").get_attribute("src")
    #category = driver.find_element(By.CSS_SELECTOR, "h2.pl-5.text-left.text-lg.font-bold.md\\:pl-0.md\\:text-center").text
    price = get_price(driver)

    print(product_name)
    print(weight)
    print(image_url)
    print(price)
    #print(category)
    # Close the browser
    driver.quit()

    return Product (
        store="IGA",
        product_name=product_name,
        brand=" ",
        category="",
        price=0,
        unit_price=0,
        original_price=0,
        availability=True,
        image_url=image_url,
        product_url="",
        weight=weight,
        description=""

    )





#get_iga_product("https://www.igashop.com.au/product/baked-provisions-homestyle-sausage-roll-256156") # gives 3 of the 4 results
get_iga_product("https://www.igashop.com.au/product/ccs-corn-chips-tasty-cheese-843319") # gives 2 of 4 results
#get_iga_product("https://www.igashop.com.au/product/ccs-nacho-cheese-corn-chips-24258") # gives all 4 results
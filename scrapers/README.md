## File Structure:
```
scrapers/
│── src/
│   ├── scrapers/             # Individual store scrapers
│   │   ├── coles.py          # Scraper for Coles
│   │   ├── woolworths.py     # Scraper for Woolworths
│   │   ├── aldi.py           # Scraper for Aldi
│   ├── utils/                # Helper functions
│   ├── database.py           # Logic for storing data in PostgreSQL
│   ├── main.py               # Entry point for running scrapers
│── tests/                    # Test suite for scrapers
│   ├── test_scrapers.py      # Unit tests for scrapers
│   ├── test_database.py      # Tests for database interactions
│── requirements.txt          # Dependencies
│── Dockerfile                # Scrapers containerization
│── README.md
```

## **Grocery Scraper Specification**

### **📥 Input**
The scraper should accept a **single URL** pointing to a grocery product page.

```plaintext
https://www.examplegrocery.com/product/1234
```

#### **Request Format**
- The scraper function/method should accept a URL as a parameter.
- Example:
  ```python
  scrape_product(url: str) -> dict
  ```

---

### **📤 Output**
The scraper should return a structured JSON object containing key product details.

#### **Response Format (JSON)**
```json
{
  "store": "Example Grocery",
  "product_name": "Organic Bananas",
  "brand": "Nature's Best",
  "category": "Fruits & Vegetables",
  "price": 3.99,
  "unit_price": 0.80,
  "original_price": 3.99,
  "availability": "In Stock",
  "image_url": "https://www.examplegrocery.com/images/bananas.jpg",
  "product_url": "https://www.examplegrocery.com/product/1234",
  "weight": "1kg",
  "description": "Fresh organic bananas, perfect for snacking or smoothies."
}
```

---

### **🛠️ Interface Definition**
#### **Function Signature** (Python Example)
```python
def scrape_product(url: str) -> dict:
    """
    Extracts product details from the given grocery product URL.

    :param url: URL of the product page
    :return: Dictionary containing structured product data
    """
```

#### **Expected Behavior**
- The scraper should **parse the given URL** and extract relevant product information.
- If the product is unavailable, return `"availability": "Out of Stock"`.
- Handle **missing data gracefully** (e.g., if no discount exists, return `null` for `discount_price`).
- Ensure **consistent JSON structure** across different stores.

---

### **📌 Notes**
- The scraper may be implemented using **BeautifulSoup, Scrapy, Selenium, or Playwright**, depending on the website structure.
- Consider adding **retry logic** in case of temporary failures (e.g., 429 Too Many Requests).
- Use **headless browsers** (e.g., Puppeteer, Playwright) for dynamic content loading if needed.
- Store extracted data in **PostgreSQL** or **cache it using Redis** for better performance.

---

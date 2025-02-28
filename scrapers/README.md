### File Structure:
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

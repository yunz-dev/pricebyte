import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/database.db")

SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.8"))

SUPPORTED_STORES = ["coles", "aldi", "woolworths"]

API_VERSION = "1.0.0"
API_TITLE = "Grocery Product Data Consolidation API"
API_DESCRIPTION = "A system that aggregates product data from multiple grocery stores and intelligently consolidates duplicate products"
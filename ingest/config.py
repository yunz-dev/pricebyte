import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_pFec60LRKvsf@ep-fragrant-block-a7lnk03h-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.8"))

# When STATIC is set, all POST requests will be blocked
STATIC_MODE = os.getenv("STATIC", "").lower() in ("true", "1", "yes", "on")

SUPPORTED_STORES = ["coles", "aldi", "woolworths"]

API_VERSION = "1.0.0"
API_TITLE = "Grocery Product Data Consolidation API"
API_DESCRIPTION = "A system that aggregates product data from multiple grocery stores and intelligently consolidates duplicate products"
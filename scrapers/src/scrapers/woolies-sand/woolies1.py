import pandas as pd
import requests
import os
import time
import random
import signal
import sys
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import asyncio
from playwright.async_api import async_playwright
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import gc

# === CONFIG ===
INPUT_CSV = "woolworths_products.csv"
OUTPUT_CSV = "processed/woolworths_product_info.csv"
BACKUP_DIR = "processed/backups"
CHECKPOINT_INTERVAL = 100  # Save backup every 100 products
MAX_RETRIES = 3  # Maximum number of retries for failed requests
RETRY_DELAY = 5  # Delay between retries in seconds
MEMORY_ERROR_DELAY = 60  # Delay in seconds when memory error occurs
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Android 6.0; Nexus 5)",
    "Referer": "https://www.woolworths.com.au",
    "Origin": "https://www.woolworths.com.au",
    "Accept": "application/json",
}
COOKIE_REFRESH_INTERVAL = 5000  # Refresh cookies every 5000 requests

# Define expected columns and their types
COLUMN_TYPES = {
    "id": "int64",
    "name": "str",
    "brand": "str",
    "description": "str",
    "long_description": "str",
    "size": "str",
    "gtin": "str",
    "price": "float64",
    "price_per_100g": "str",
    "country_of_origin": "str",
    "ingredients": "str",
    "allergens": "str",
    "dietary": "str",
    "storage": "str",
    "preparation": "str",
    "dimensions.height_mm": "float64",
    "dimensions.width_mm": "float64",
    "dimensions.depth_mm": "float64",
    "image_front_full": "str",
    "image_back_full": "str",
    "image_front_zoom": "str",
    "image_back_zoom": "str",
    "scrape_timestamp": "str",
}

# === SIGNAL HANDLING ===


def signal_handler(signum, frame):
    print("\n⚠️ Received interrupt signal. Saving progress before exit...")
    if "results_df" in globals() and not results_df.empty:
        backup_file = create_backup()
        print(f"✅ Progress saved to: {backup_file}")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# === BACKUP FUNCTIONS ===


def create_backup():
    """Create a backup and update main CSV file."""
    # First update the main output file
    if "results_df" in globals() and not results_df.empty:
        results_df.to_csv(OUTPUT_CSV, index=False)

        # Create/update backup file with fixed name
        backup_file = os.path.join(BACKUP_DIR, "woolworths_product_info_backup.csv")
        results_df.to_csv(backup_file, index=False)
    return backup_file


def load_latest_backup():
    """Load the backup file if it exists."""
    backup_file = os.path.join(BACKUP_DIR, "woolworths_product_info_backup.csv")
    if os.path.exists(backup_file):
        print(f"📂 Found backup file: {backup_file}")
        return pd.read_csv(backup_file)
    return None


# === COOKIE FETCHER ===


async def get_woolworths_cookies():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False, args=["--start-maximized"]
            )
            context = await browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            )
            page = await context.new_page()
            await page.goto(
                "https://www.woolworths.com.au/shop/productdetails/253366",
                wait_until="networkidle",
            )
            cookies_list = await context.cookies()
            await browser.close()
            return {cookie["name"]: cookie["value"] for cookie in cookies_list}
    except Exception as e:
        print(f"❌ Error fetching cookies: {str(e)}")
        print("⚠️ Waiting 30 seconds before retrying...")
        time.sleep(30)
        return await get_woolworths_cookies()


# === RUN ASYNC COOKIE FETCHER FIRST ===
print("🔄 Fetching initial cookies...")
cookies = asyncio.run(get_woolworths_cookies())

# === LOAD INPUT ===
try:
    df = pd.read_csv(INPUT_CSV)
    product_ids = df["Stockcode"].dropna().astype(int).tolist()
    print(f"📊 Loaded {len(product_ids)} products to process")
except Exception as e:
    print(f"❌ Error loading input CSV: {str(e)}")
    sys.exit(1)

# Ensure output directory exists
Path(os.path.dirname(OUTPUT_CSV)).mkdir(parents=True, exist_ok=True)


def initialize_dataframe():
    """Create an empty DataFrame with the correct column types."""
    df = pd.DataFrame(columns=COLUMN_TYPES.keys())
    for col, dtype in COLUMN_TYPES.items():
        if dtype == "str":
            df[col] = df[col].astype("str")
        elif dtype in ["int64", "float64"]:
            df[col] = df[col].astype(dtype)
    return df


def clean_results_df(df):
    """Clean the results dataframe and ensure consistent column types."""
    if df.empty:
        return initialize_dataframe()

    original_len = len(df)

    # Remove rows where id is not a valid integer
    df["id"] = pd.to_numeric(df["id"], errors="coerce")
    df = df.dropna(subset=["id"])

    # Ensure all expected columns exist with correct types
    for col, dtype in COLUMN_TYPES.items():
        if col not in df.columns:
            if dtype == "str":
                df[col] = ""
            else:
                df[col] = pd.NA

        # Convert to correct type
        try:
            if dtype == "str":
                df[col] = df[col].fillna("").astype(str)
            else:
                df[col] = pd.to_numeric(df[col], errors="coerce").astype(dtype)
        except Exception as e:
            print(f"⚠️ Error converting column {col} to {dtype}: {str(e)}")

    removed_count = original_len - len(df)
    if removed_count > 0:
        print(f"⚠️ Removed {removed_count} corrupted rows from results")

    return df


def add_row_to_results(results_df, row):
    """Add a new row to results_df with proper type handling."""
    # Create a single-row DataFrame with the correct structure
    new_row_df = initialize_dataframe()

    # Fill in the values we have
    for col in new_row_df.columns:
        if col in row:
            new_row_df.at[0, col] = row[col]

    # Concatenate with existing results
    return pd.concat([results_df, new_row_df], ignore_index=True)


# Try to load existing output or latest backup
if os.path.exists(OUTPUT_CSV):
    try:
        results_df = pd.read_csv(OUTPUT_CSV)
        print(f"📊 Loaded {len(results_df)} results from {OUTPUT_CSV}")
        results_df = clean_results_df(results_df)
    except Exception as e:
        print(f"⚠️ Error loading {OUTPUT_CSV}, trying backup: {str(e)}")
        results_df = pd.DataFrame()
else:
    backup_df = load_latest_backup()
    if backup_df is not None:
        results_df = clean_results_df(backup_df)
        print(f"📊 Loaded {len(results_df)} results from backup")
    else:
        results_df = pd.DataFrame()
        print("📊 Starting fresh scrape")

# Get scraped IDs after cleaning
scraped_ids = set(results_df["id"].astype(int)) if not results_df.empty else set()
remaining_ids = [pid for pid in product_ids if pid not in scraped_ids]
print(f"🎯 {len(remaining_ids)} products remaining to scrape")

# === SESSION SETUP ===


def create_session():
    """Create a new session with retry strategy and connection pooling."""
    session = requests.Session()

    # Configure retry strategy
    retry_strategy = Retry(
        total=3,  # number of retries
        backoff_factor=0.5,  # wait 0.5, 1, 2... seconds between retries
        # retry on these status codes
        status_forcelist=[429, 500, 502, 503, 504],
    )

    # Configure connection pooling
    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=10,  # number of connection pools to cache
        pool_maxsize=100,  # maximum number of connections to save in the pool
        pool_block=False,  # whether to block when pool is full
    )

    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


# Create global session
session = create_session()

# === MEMORY MANAGEMENT ===


def handle_memory_error(error_count):
    """Handle memory-related errors with increasing delays."""
    print(f"\n⚠️ Memory pressure detected. Cleaning up and waiting...")

    # Force garbage collection
    gc.collect()

    # Calculate delay with exponential backoff
    delay = min(MEMORY_ERROR_DELAY * (2**error_count), 20)  # max 5 minutes

    # Close and recreate session
    global session
    session.close()
    session = create_session()

    print(f"🔄 Waiting {delay} seconds before retrying...")
    time.sleep(delay)


# === SCRAPER FUNCTION ===


def scrape_product(product_id, retry_count=0, memory_error_count=0):
    url = f"https://www.woolworths.com.au/apis/ui/product/detail/{
        product_id
    }?isMobile=false&useVariant=true"
    HEADERS["Referer"] = (
        f"https://www.woolworths.com.au/shop/productdetails/{product_id}"
    )

    try:
        response = session.get(url, headers=HEADERS, cookies=cookies, timeout=30)

        if not response.ok:
            if retry_count < MAX_RETRIES:
                print(
                    f"⚠️ Attempt {retry_count + 1}/{MAX_RETRIES} failed for ID {
                        product_id
                    }: {response.status_code}"
                )
                time.sleep(RETRY_DELAY)
                return scrape_product(product_id, retry_count + 1, memory_error_count)
            print(f"❌ Failed for ID {product_id}: {response.status_code}")
            return None

        data = response.json()
        if not data:
            print(f"❌ Empty response for ID {product_id}")
            return None

        # Clear response data from memory
        response.close()

        product = data.get("Product", {})
        attrs = data.get("AdditionalAttributes", {})
        images = product.get("DetailsImagePaths", [])

        # Nutrition - with error handling
        nutrition_100g = {}
        nutrition_serving = {}
        try:
            for item in data.get("NutritionalInformation", []) or []:
                if not isinstance(item, dict):
                    continue
                name = (
                    item.get("Name", "")
                    .lower()
                    .replace(" ", "_")
                    .replace(",", "")
                    .replace("-", "")
                    .replace("/", "_")
                )
                if not name:
                    continue
                values = item.get("Values", {})
                nutrition_100g[f"nutr_{name}_100g"] = values.get(
                    "Quantity Per 100g / 100mL"
                )
                nutrition_serving[f"nutr_{name}_serving"] = values.get(
                    "Quantity Per Serving"
                )
        except Exception as e:
            print(f"⚠️ Error parsing nutritional info for ID {product_id}: {str(e)}")
            # Continue with empty nutrition data
            pass

        row = {
            "id": product.get("Stockcode"),
            "name": product.get("Name"),
            "brand": product.get("Brand"),
            "description": product.get("Description"),
            "long_description": product.get("RichDescription")
            or product.get("FullDescription"),
            "size": product.get("PackageSize"),
            "gtin": product.get("Barcode"),
            "price": product.get("Price"),
            "price_per_100g": product.get("CupString"),
            "country_of_origin": data.get("CountryOfOriginLabel", {}).get("AltText"),
            "ingredients": attrs.get("ingredients"),
            "allergens": attrs.get("allergencontains"),
            "dietary": attrs.get("lifestyleanddietarystatement"),
            "storage": attrs.get("storageinstructions"),
            "preparation": attrs.get("usageinstructions"),
            "dimensions.height_mm": attrs.get("productheightmm"),
            "dimensions.width_mm": attrs.get("productwidthmm"),
            "dimensions.depth_mm": attrs.get("productdepthmm"),
            "image_front_full": product.get("LargeImageFile"),
            "image_back_full": images[1] if len(images) > 1 else None,
            "image_front_zoom": images[0] if images else None,
            "image_back_zoom": images[2] if len(images) > 2 else None,
            "scrape_timestamp": datetime.now().isoformat(),
            **nutrition_100g,
            **nutrition_serving,
        }

        return row

    except (requests.exceptions.ConnectionError, OSError) as e:
        if "Cannot allocate memory" in str(e) or "Too many open files" in str(e):
            if memory_error_count < 5:  # Limit memory error retries
                handle_memory_error(memory_error_count)
                return scrape_product(product_id, retry_count, memory_error_count + 1)
            print(
                f"❌ Persistent memory issues for ID {product_id}, skipping: {str(e)}"
            )
            return None

        if retry_count < MAX_RETRIES:
            print(
                f"⚠️ Network error (attempt {retry_count + 1}/{MAX_RETRIES}) for ID {
                    product_id
                }: {str(e)}"
            )
            time.sleep(RETRY_DELAY)
            return scrape_product(product_id, retry_count + 1, memory_error_count)
        print(f"❌ Network error for ID {product_id}: {str(e)}")
        return None

    except Exception as e:
        print(f"❌ Error processing ID {product_id}: {str(e)}")
        return None


# === PROGRESS TRACKING ===


class ProgressTracker:
    def __init__(self, total_products):
        self.total_products = total_products
        self.start_time = datetime.now()
        self.products_processed = 0
        self.successful_scrapes = 0
        self.failed_scrapes = 0
        self.last_report_time = self.start_time
        self.last_report_count = 0

    def update(self, success=True):
        self.products_processed += 1
        if success:
            self.successful_scrapes += 1
        else:
            self.failed_scrapes += 1

    def should_report(self):
        return (self.products_processed % 100 == 0) or (
            self.products_processed == self.total_products
        )

    def get_progress_report(self):
        current_time = datetime.now()
        elapsed_time = current_time - self.start_time

        # Calculate scraping rate (products per minute)
        time_since_last_report = (current_time - self.last_report_time).total_seconds()
        products_since_last_report = self.products_processed - self.last_report_count

        if time_since_last_report > 0:
            current_rate = (products_since_last_report / time_since_last_report) * 60
        else:
            current_rate = 0

        # Calculate overall rate and estimated time remaining
        if elapsed_time.total_seconds() > 0:
            overall_rate = (self.products_processed / elapsed_time.total_seconds()) * 60
            remaining_products = self.total_products - self.products_processed
            if overall_rate > 0:
                estimated_remaining = timedelta(
                    minutes=remaining_products / overall_rate
                )
            else:
                estimated_remaining = timedelta(0)
        else:
            overall_rate = 0
            estimated_remaining = timedelta(0)

        # Update last report metrics
        self.last_report_time = current_time
        self.last_report_count = self.products_processed

        return f"""
📊 Progress Report:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Completed: {self.products_processed}/{self.total_products} ({(self.products_processed / self.total_products * 100):.1f}%)
✅ Successful: {self.successful_scrapes}
❌ Failed: {self.failed_scrapes}
⏱️ Elapsed Time: {str(elapsed_time).split(".")[0]}
🚀 Current Rate: {current_rate:.1f} products/minute
📈 Overall Rate: {overall_rate:.1f} products/minute
⏳ Estimated Time Remaining: {str(estimated_remaining).split(".")[0]}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""


# === MAIN LOOP ===
request_count = 0
products_since_checkpoint = 0
error_streak = 0  # Track consecutive errors

# Initialize progress tracker
progress = ProgressTracker(len(remaining_ids))

try:
    # Initialize results_df with correct structure if empty
    if results_df.empty:
        results_df = initialize_dataframe()

    for pid in remaining_ids:
        try:
            # Check if we need to refresh cookies
            if request_count > 0 and request_count % COOKIE_REFRESH_INTERVAL == 0:
                print("🔄 Refreshing cookies...")
                cookies = asyncio.run(get_woolworths_cookies())

            row = scrape_product(pid)
            if row:
                results_df = add_row_to_results(results_df, row)
                print(f"✅ Saved: {pid}")
                error_streak = 0  # Reset error streak on success
                progress.update(success=True)

                # Save progress every CHECKPOINT_INTERVAL products
                products_since_checkpoint += 1
                if products_since_checkpoint >= CHECKPOINT_INTERVAL:
                    backup_file = create_backup()
                    print(f"💾 Progress saved to main file and backup")
                    products_since_checkpoint = 0
            else:
                error_streak += 1
                progress.update(success=False)

            # If too many consecutive errors, take a longer break
            if error_streak >= 5:
                print(
                    f"⚠️ {error_streak} consecutive errors detected. Taking a longer break..."
                )
                time.sleep(60)  # 1 minute break
                error_streak = 0  # Reset after break

            # Show progress report
            if progress.should_report():
                print(progress.get_progress_report())

            request_count += 1
            # time.sleep(random.uniform(0.3, 0.8))

        except Exception as e:
            print(f"⚠️ Loop error for ID {pid}: {str(e)}")
            error_streak += 1
            progress.update(success=False)
            continue  # Continue with next product

except Exception as e:
    print(f"\n❌ Unexpected error: {str(e)}")
    backup_file = create_backup()
    print(f"💾 Emergency backup saved")
    raise

finally:
    # Clean up
    session.close()

    # Save final results
    if not results_df.empty:
        create_backup()
        print("\n✅ Final results saved")

    # Print final progress report
    print("\n🏁 Final Progress Report:")
    print(progress.get_progress_report())
    print("Done!")

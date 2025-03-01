import requests
import json
from time import sleep

# Test the specific request that's hanging
url = "https://www.woolworths.com.au/apis/ui/browse/category"

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin": "https://www.woolworths.com.au",
    "Referer": "https://www.woolworths.com.au/shop/browse/fruit-veg",
}

payload = {
    "categoryId": "1-E5BEE36E",
    "categoryVersion": "v2",
    "enableAdReRanking": False,
    "filters": [],
    "flags": {"EnablePersonalizationCategoryRestriction": True},
    "formatObject": "{\"name\":\"Fruit & Veg\"}",
    "gpBoost": 0,
    "groupEdmVariants": False,
    "isBundle": False,
    "isHideUnavailableProducts": False,
    "isMobile": False,
    "isRegisteredRewardCardPromotion": False,
    "isSpecial": False,
    "location": "/shop/browse/fruit-veg",
    "pageNumber": 1,
    "pageSize": 24,
    "sortType": "TraderRelevance",
    "token": "",
    "url": "/shop/browse/fruit-veg",
}

print("🔍 Testing request with 10 second timeout...")

try:
    response = requests.post(
        url, 
        headers=headers, 
        data=json.dumps(payload), 
        timeout=10  # 10 second timeout
    )
    
    print(f"✅ Status Code: {response.status_code}")
    print(f"📊 Response Size: {len(response.text)} characters")
    
    if response.status_code == 200:
        data = response.json()
        print(f"🔍 Response keys: {list(data.keys())}")
        
        if "Bundles" in data:
            total_bundles = len(data.get("Bundles", []))
            print(f"📦 Found {total_bundles} bundles")
            
            total_products = sum(len(bundle.get("Products", [])) for bundle in data.get("Bundles", []))
            print(f"🛒 Total products: {total_products}")
        else:
            print("❌ No 'Bundles' key in response")
            print("📄 First 500 chars of response:")
            print(json.dumps(data, indent=2)[:500])
    else:
        print(f"❌ Error response: {response.status_code}")
        print(f"📄 Response: {response.text[:500]}")
        
except requests.Timeout:
    print("⏰ Request timed out after 10 seconds")
except requests.ConnectionError as e:
    print(f"🚫 Connection error: {str(e)}")
except Exception as e:
    print(f"❌ Unexpected error: {str(e)}")
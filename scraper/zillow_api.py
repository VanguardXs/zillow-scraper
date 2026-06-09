import requests
import os
from dotenv import load_dotenv
from database.db import SessionLocal
from database.models import Listing

load_dotenv()

API_KEY = os.getenv("ZILLOW_API_KEY")
BASE_URL = "https://api.openwebninja.com/realtime-zillow-data/search"

CITIES = [
    "New York, NY",
    "Los Angeles, CA",
    "Chicago, IL",
    "Houston, TX",
    "Phoenix, AZ",
    "Miami, FL",
    "Seattle, WA",
    "Denver, CO",
    "Austin, TX",
    "Las Vegas, NV"
]

def fetch_listings(location: str, page: int = 1):
    headers = {"x-api-key": API_KEY}
    params = {
        "location": location,
        "page": page,
        "home_status": "FOR_SALE"
    }
    try:
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])
    except Exception as e:
        print(f"❌ Error fetching {location} page {page}: {e}")
        return []

def save_listings(listings: list):
    db = SessionLocal()
    saved = 0
    skipped = 0
    try:
        for item in listings:
            zpid = str(item.get("zpid", ""))
            if not zpid:
                continue

            exists = db.query(Listing).filter(Listing.zpid == zpid).first()
            if exists:
                skipped += 1
                continue

            listing = Listing(
                zpid=zpid,
                address=item.get("address", ""),
                city=item.get("city", ""),
                state=item.get("state", ""),
                zipcode=item.get("zipcode", ""),
                price=item.get("price", 0),
                bedrooms=item.get("bedrooms", 0),
                bathrooms=item.get("bathrooms", 0),
                living_area=item.get("livingArea", 0),
                home_type=item.get("homeType", ""),
                home_status=item.get("homeStatus", ""),
                zestimate=item.get("zestimate", 0),
                url=item.get("url", "")
            )
            db.add(listing)
            saved += 1

        db.commit()
        print(f"✅ Saved: {saved} | Duplicates skipped: {skipped}")
    except Exception as e:
        db.rollback()
        print(f"❌ Error saving: {e}")
    finally:
        db.close()

def run_scraper():
    print("🚀 Starting scraper...")
    total = 0
    for city in CITIES:
        print(f"\n📍 City: {city}")
        for page in range(1, 6):
            print(f"  📄 Page {page}...")
            listings = fetch_listings(city, page)
            if not listings:
                print(f"  ⚠️ No data, skipping")
                break
            save_listings(listings)
            total += len(listings)
    print(f"\n🎉 Done! Total fetched: {total} listings")

if __name__ == "__main__":
    run_scraper()
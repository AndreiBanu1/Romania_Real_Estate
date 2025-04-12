import sys
from curl_cffi import requests
from rich import print
import os
import json
import re
from bs4 import BeautifulSoup
from database import Database  # Import the database handler
from storia_cities import StoriaCity  # Import the ENUM for cities
import time
import random

# Headers & Cookies
cookies = {
    'PHPSESSID': 'o0h7vvmtnk91vr6m1eai7f2nfk',
    'mobile_default': 'desktop',
}

def get_headers(city):
    """Returns dynamically generated headers with the correct referer."""
    return {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.8',
        'priority': 'u=1, i',
        'referer': f'https://www.storia.ro/ro/rezultate/vanzare/apartament/{city}?priceMin=50000&priceMax=150000&viewType=listing',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Brave";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        'x-nextjs-data': '1',
    }

def new_session():
    """Creates a new session with optional proxy"""
    proxy = os.getenv("stickyproxy")
    if proxy:
        print(f"Using proxy: {proxy}")
        session = requests.Session(impersonate="chrome", proxy=proxy)
    else:
        print("Warning: Proxy is not set!")
        session = requests.Session(impersonate="chrome")
    return session

def get_latest_build_id(city):
    """Fetches the latest build ID from Storia for a specific city."""
    url = f"https://www.storia.ro/ro/rezultate/vanzare/apartament/{city}"
    session = requests.Session(impersonate="chrome")
    response = session.get(url, headers=get_headers(city), cookies=cookies)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        script_tag = soup.find("script", src=re.compile(r"_next/static/.*/_buildManifest.js"))
        if script_tag:
            match = re.search(r"_next/static/([^/]+)/_buildManifest.js", script_tag["src"])
            if match:
                return match.group(1)
    return None

def get_storia_api_url(build_id, city, price_min, price_max, num_rooms, page):
    """Generates the API URL dynamically for the selected city."""
    base_url = f"https://www.storia.ro/_next/data/{build_id}/ro/rezultate/vanzare/apartament/{city}.json"
    
    params = [
        f"priceMin={price_min}",
        f"priceMax={price_max}",
        "viewType=listing",
        "searchingCriteria=vanzare",
        "searchingCriteria=apartament",
        f"searchingCriteria={city}",
        f"page={page}"
    ]
    
    return f"{base_url}?{'&'.join(params)}"

def fetch_data_for_city(city, price_min=50000, price_max=150000, num_rooms=2):
    """Fetch data for a given city and insert into the database."""
    session = new_session()
    build_id = get_latest_build_id(city)
    if not build_id:
        print("❌ Failed to retrieve the latest build ID. Exiting...")
        return None

    print(f"🔄 Using build ID: {build_id}")
    db = Database()
    page = 1

    while True:
        api_url = get_storia_api_url(build_id, city, price_min, price_max, num_rooms, page)
        print(f"📡 Fetching data from: {api_url}")
        response = session.get(api_url, cookies=cookies, headers=get_headers(city))

        if response.status_code == 200:
            try:
                json_data = response.json()
                save_response_to_file(json_data, f"storia_{city}_page{page}.json")
                process_and_store_data(json_data, db)
                print(f"✅ Successfully fetched and stored page {page} for {city}")

                # Stop when no more listings are available
                if not json_data.get("pageProps", {}).get("data", {}).get("searchAds", {}).get("items", []):
                    break
                
                page += 1

                # 🕒 Randomized delay to avoid detection
                sleep_time = random.uniform(2, 5)  # Wait between 2 to 5 seconds
                print(f"⏳ Waiting {sleep_time:.2f} seconds before next request...")
                time.sleep(sleep_time)

            except Exception as e:
                print(f"❌ Error processing JSON for {city}, page {page}: {str(e)}")
                break
        else:
            print(f"❌ Failed to fetch page {page} for {city}! HTTP {response.status_code}")
            break

    db.close()

def process_and_store_data(json_data, db):
    print("📌 Processing data...")

    properties = json_data.get("pageProps", {}).get("data", {}).get("searchAds", {}).get("items", [])

    if not properties:
        print("⚠️ No properties found in the current page!")
        return
    
    for item in properties:
        print("🏡 Extracted property:", item)
        db.insert_property(item)

    print(f"✅ Inserted {len(properties)} properties into DB.")

def save_response_to_file(json_data, filename):
    """Saves the API response to a JSON file."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False)
        print(f"✅ JSON response saved to {filename}.")
    except Exception as e:
        print(f"❌ Error saving JSON to {filename}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please provide a city name.")
        sys.exit(1)

    city_name = sys.argv[1].lower()
    city_enum = StoriaCity.get_city_slug(city_name)

    if city_enum:
        print(f"🔍 Crawling data for {city_enum.value}...")
        fetch_data_for_city(city_enum.value)
    else:
        print(f"❌ Invalid city name: {city_name}. Check storia_cities.py for valid names.")

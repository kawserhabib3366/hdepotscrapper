import logging
import json
import pickle


import subprocess

import re,time


# =======================
# LOGGING CONFIGURATION
# =======================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler("scraper.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)





import requests
from bs4 import BeautifulSoup




HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_regions():
    """Scrape all state regions with their URLs"""
    url = "https://www.homedepot.com/l/storeDirectory"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    regions = []
    for a in soup.select("section a.sui-font-bold"):
        name = a.get_text(strip=True)
        href = a["href"]
        regions.append({"region": name, "url": href})
    return regions


def get_stores(state_url):
    """Scrape all unique stores for a given state"""
    response = requests.get(state_url, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    stores = []
    for a in soup.select("section a.sui-font-regular"):
        store_name = a.get_text(strip=True)
        store_url = a.get("href")  # returns None if no href
        if not store_url:
            continue


        # only main store link (ending in /storeId)
        parts = store_url.strip("/").split("/")
        if parts[-1].isdigit() and parts[-2].isdigit():
            store_id = parts[-1]
            store_zip = parts[-2]
            stores.append({
                "store": store_name,
                "url": store_url,
                "storeId": store_id,
                "storeZip":store_zip
            })
    return stores


def scrape_all_stores():
    """Scrape all states and their stores"""
    all_data = []
    regions = get_regions()

    for region in regions:
        print(f"🔎 Scraping {region['region']}...")
        stores = get_stores(region["url"])
        for s in stores:
            s["region"] = region["region"]  # add region info
            all_data.append(s)
    return all_data


import json
import pandas as pd

def export_entries(entries, jsonl_file="stores.jsonl", json_file="stores.json", excel_file="stores.xlsx"):
    # --- Export to JSONL ---
    # with open(jsonl_file, "a", encoding="utf-8") as f:  # append mode
    #     for entry in entries:
    #         f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    # --- Export to JSON ---
    with open(json_file, "w", encoding="utf-8") as f:  # overwrite with latest full dataset
        json.dump(entries, f, ensure_ascii=False, indent=4)
    
    # --- Export to Excel ---
    # df = pd.DataFrame(entries)
    # df.to_excel(excel_file, index=False)

    # print(f"✅ Exported {len(entries)} entries to {jsonl_file}, {json_file}, and {excel_file}")
    print(f"✅ Exported {len(entries)} entries to {json_file} ")





# Example usage
if __name__ == "__main__":
    all_stores = scrape_all_stores()
    export_entries(all_stores)
    print(f"\n✅ Found {len(all_stores)} stores total.")
    for s in all_stores[:10]:  # show sample
        print(s)




#/p/Kidde-10-Year-Battery-Powered-Smoke-and-Carbon-Monoxide-Detector-with-Alarm-LED-Warning-Lights-and-Voice-Alerts-21032779-21032779/328175570

#/p/Kidde-10-Year-Battery-Powered-Smoke-and-Carbon-Monoxide-Detector-with-Alarm-LED-Warning-Lights-and-Voice-Alerts-21032779-21032779/328175570


# try:
#     driver=get_driver()

# except Exception as e :
#     print(e)





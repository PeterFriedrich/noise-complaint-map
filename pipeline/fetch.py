"""
Fetches all noise complaint records from Edmonton Open Data (Socrata)
and writes them to data/raw_complaints.json.
"""

import json
import os
import requests
from pathlib import Path

SOCRATA_URL = "https://data.edmonton.ca/resource/ypje-j649.json"
PAGE_SIZE = 1000
OUTPUT_PATH = Path(__file__).parent.parent / "data" / "raw_complaints.json"


def load_credentials():
    env_path = Path(__file__).parent.parent / ".env"
    creds = {}
    with open(env_path) as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                creds[k] = v
    return creds["SOCRATA_API_KEY_ID"], creds["SOCRATA_API_KEY_SECRET"]


def fetch_all(auth):
    records = []
    offset = 0
    while True:
        resp = requests.get(
            SOCRATA_URL,
            auth=auth,
            params={
                "$where": "complaint_category='Noise'",
                "$limit": PAGE_SIZE,
                "$offset": offset,
                "$order": ":id",
            },
        )
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        records.extend(batch)
        print(f"  fetched {len(records)} records...", end="\r")
        offset += PAGE_SIZE
        if len(batch) < PAGE_SIZE:
            break
    print(f"  fetched {len(records)} records total")
    return records


def main():
    auth = load_credentials()
    print("Fetching noise complaints from Socrata...")
    records = fetch_all(auth)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(records, f)
    print(f"Written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

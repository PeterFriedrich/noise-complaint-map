"""
Reads raw_complaints.json, aggregates complaint points into hex bins
by day of week, and writes site/data/complaints.geojson.
"""

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

RAW_PATH = Path(__file__).parent.parent / "data" / "raw_complaints.json"
OUTPUT_PATH = Path(__file__).parent.parent / "site" / "data" / "complaints.geojson"

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def load_raw():
    with open(RAW_PATH) as f:
        return json.load(f)


def parse_record(r):
    lat = r.get("latitude")
    lon = r.get("longitude")
    dc = r.get("date_created")
    if not lat or not lon or not dc:
        return None
    try:
        dt = datetime.fromisoformat(dc)
        return {
            "lat": float(lat),
            "lon": float(lon),
            "dow": dt.weekday(),  # 0=Monday, 6=Sunday
            "year": dt.year,
        }
    except (ValueError, TypeError):
        return None


def build_geojson(records):
    features = []
    for r in records:
        parsed = parse_record(r)
        if not parsed:
            continue
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [parsed["lon"], parsed["lat"]],
            },
            "properties": {
                "dow": parsed["dow"],
                "year": parsed["year"],
            },
        })
    return {
        "type": "FeatureCollection",
        "features": features,
    }


def main():
    print("Loading raw complaints...")
    records = load_raw()
    print(f"  {len(records)} records")

    print("Building GeoJSON...")
    geojson = build_geojson(records)
    kept = len(geojson["features"])
    print(f"  {kept} features ({len(records) - kept} dropped — missing lat/lon or date)")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(geojson, f)
    print(f"Written to {OUTPUT_PATH}")

    dow_counts = defaultdict(int)
    for f in geojson["features"]:
        dow_counts[f["properties"]["dow"]] += 1
    print("\nBy day of week:")
    for i, day in enumerate(DAYS):
        print(f"  {day}: {dow_counts[i]}")


if __name__ == "__main__":
    main()

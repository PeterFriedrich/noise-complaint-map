"""
Writes site/data/meta.json with build timestamp and record count.
Called after transform.py has written complaints.geojson.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

GEOJSON_PATH = Path(__file__).parent.parent / "site" / "data" / "complaints.geojson"
META_PATH = Path(__file__).parent.parent / "site" / "data" / "meta.json"


def main():
    with open(GEOJSON_PATH) as f:
        geojson = json.load(f)

    record_count = len(geojson["features"])
    built_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    meta = {
        "built_at": built_at,
        "record_count": record_count,
    }

    with open(META_PATH, "w") as f:
        json.dump(meta, f, indent=2)

    print(f"Written {META_PATH}")
    print(f"  built_at: {built_at}")
    print(f"  record_count: {record_count}")


if __name__ == "__main__":
    main()

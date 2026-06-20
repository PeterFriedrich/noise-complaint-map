#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"

python3 pipeline/fetch.py
python3 pipeline/transform.py
python3 pipeline/generate.py

git add site/data/complaints.geojson site/data/meta.json
git commit -m "chore: update complaints data $(date -u +%Y-%m-%d)"
git push

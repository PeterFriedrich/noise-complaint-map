# noise-complaint-map

A static visualization of Edmonton noise complaints sourced from Edmonton Open Data (Socrata). A Python pipeline runs on a scheduled basis, fetches complaint data, and generates a static site hosted on GitHub Pages. Users can explore complaint density by neighbourhood and day of week — are noise complaints going up? Which days are worst?

## Setup

```bash
conda env create -f environment.yml
conda activate noise-complaint-map
cp .env.example .env  # then fill in your Socrata credentials
```

Socrata API credentials: generate at https://data.edmonton.ca/profile/edit/developer_settings

## Usage

```bash
# Run the full pipeline (fetch → transform → generate → commit → push)
bash pipeline/run.sh

# Or run steps individually
python3 pipeline/fetch.py      # fetches raw data to data/raw_complaints.json
python3 pipeline/transform.py  # converts to site/data/complaints.geojson
python3 pipeline/generate.py   # writes site/data/meta.json

# Run tests
python3 -m pytest tests/ -v
```

## Project Structure

```
pipeline/       ← Python data fetcher + static site generator
site/           ← generated static site (committed, served via GitHub Pages)
docs/           ← spec, architecture, phases
tests/          ← pipeline unit tests
session-summary/ ← per-session handoff docs
```

## Development

TODO — fill after stack is confirmed

## Testing

TODO — fill after stack is confirmed

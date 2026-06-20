# Architecture

## Overview

Two independent pieces: a Python pipeline (runs on Oracle Ampere) that fetches data and generates static files, and a static site (served from GitHub Pages) that loads those files at page load time. No communication between them at runtime — the pipeline pushes to the repo, GitHub Pages serves whatever is committed.

## Component Map

```
[Edmonton Open Data / Socrata API]
        |
        v
[Oracle Ampere — cron job]
  pipeline/
    fetch.py       ← pulls complaint records from Socrata
    transform.py   ← aggregates by day-of-week, neighbourhood, time period
    generate.py    ← writes JSON data files + renders site/ output
        |
        v (git push)
[GitHub repo — site/ directory]
        |
        v (GitHub Pages)
[Static site — browser]
  site/
    index.html
    data/          ← pre-generated JSON (one file per day-of-week slice)
    js/            ← map rendering logic
    css/
```

## Data Flow

1. Cron triggers `pipeline/run.sh` on Oracle server
2. `fetch.py` calls Socrata API, pages through results, writes raw cache
3. `transform.py` aggregates: complaints by neighbourhood × day-of-week, trend over time
4. `generate.py` writes `site/data/*.json` and updates `site/index.html` with new build timestamp
5. Pipeline commits and pushes `site/` to GitHub
6. GitHub Pages serves updated static files
7. Browser loads `index.html`, fetches day-of-week JSON on demand, renders map

## Key Interfaces

- **Socrata API**: `data.edmonton.ca` — dataset ID `ypje-j649`, filter `complaint_category = "Noise"`
- **Pipeline entry point**: `pipeline/run.sh` (called by cron)
- **Data contract**: `site/data/dow-{0..6}.json` — one file per day of week, schema TBD
- **Site entry point**: `site/index.html`

## Technology Choices

| Layer | Choice | Why |
|---|---|---|
| Pipeline | Python + sodapy or requests | Native Socrata client; user's primary language |
| Data wrangling | pandas | Standard for this workload |
| Map rendering | TBD (Leaflet or deck.gl stub) | See Open Questions |
| Static hosting | GitHub Pages | Free, zero config |
| Scheduler | cron on Oracle Ampere | Persistent, free, already available |

## Known Constraints & Tradeoffs

- **No real-time queries**: all data is pre-aggregated at pipeline run time; freshness limited by cron cadence
- **Static JSON size**: if complaint history is large, may need to limit lookback window or paginate JSON
- **ARM build**: any Python dependencies with C extensions must have ARM wheels available
- **Isometric deferred**: phase 1 uses a 2D map to keep scope tight; deck.gl HexagonLayer is the likely phase 2 path

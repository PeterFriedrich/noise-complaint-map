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
    generate.py    ← writes complaints.geojson + updates site/ output
        |
        v (git push — small, changes daily)
[GitHub repo — site/ directory]
        |
        v (GitHub Pages)
[Static site — browser]
  site/
    index.html
    data/
      complaints.geojson   ← pre-aggregated hex/grid bins (pushed by pipeline)
    js/            ← MapLibre GL + deck.gl rendering logic
    css/

[One-time setup — not touched by pipeline]
  edmonton.pmtiles  →  Cloudflare R2 (free tier, range-request-safe)
```

## Data Flow

### Pipeline (runs daily via cron)
1. Cron triggers `pipeline/run.sh` on Oracle server
2. `fetch.py` calls Socrata API, pages through all noise complaint records
3. `transform.py` aggregates: bin complaints into hex/grid cells, compute count per cell × day-of-week
4. `generate.py` writes `site/data/complaints.geojson` and updates build timestamp in `site/index.html`
5. Pipeline commits and pushes `site/` to GitHub
6. GitHub Pages serves updated files

### Browser (at page load)
7. Browser loads `index.html`, initialises MapLibre GL pointed at `edmonton.pmtiles` on R2
8. deck.gl `HexagonLayer` loads `complaints.geojson`, extrudes 3D columns by complaint count
9. User can rotate/zoom/pan; day-of-week filter updates column heights client-side

### One-time basemap setup (not part of daily pipeline)
- Run `pmtiles extract` to cut Edmonton bbox from Protomaps planet build
- Upload `edmonton.pmtiles` to Cloudflare R2, enable CORS
- Point MapLibre source URL at R2 — never needs to change unless OSM refresh is wanted

## Key Interfaces

- **Socrata API**: `data.edmonton.ca` — dataset ID `ypje-j649`, filter `complaint_category = "Noise"`, auth via basic auth (`SOCRATA_API_KEY_ID:SOCRATA_API_KEY_SECRET`)
- **Pipeline entry point**: `pipeline/run.sh` (called by cron)
- **Data contract**: `site/data/complaints.geojson` — schema TBD, one feature per complaint point with `date_created`, `latitude`, `longitude`; deck.gl bins at render time
- **Basemap**: `edmonton.pmtiles` on Cloudflare R2 — URL injected into `site/js/` config
- **Site entry point**: `site/index.html`

## Technology Choices

| Layer | Choice | Why |
|---|---|---|
| Pipeline | Python + requests | Socrata REST API; user's primary language |
| Data wrangling | pandas | Standard for this workload |
| Map basemap | MapLibre GL + Protomaps `.pmtiles` | Vector basemap, no tile server, self-controlled |
| 3D extrusion | deck.gl `HexagonLayer` (extruded) | Isometric-look 3D columns from point data, interactive |
| Basemap hosting | Cloudflare R2 (free tier) | Range requests work reliably; GitHub Pages has known range-request issues with `.pmtiles` |
| Static site hosting | GitHub Pages | Free, zero config |
| Scheduler | cron on Oracle Ampere | Persistent, free, already available |

## Known Constraints & Tradeoffs

- **No real-time queries**: all data is pre-aggregated at pipeline run time; freshness limited to daily cron cadence
- **Protomaps on GitHub Pages is flaky**: range requests for `.pmtiles` work inconsistently on GitHub Pages (browser-dependent). Basemap lives on R2 instead — cross-origin fine with CORS enabled.
- **ARM build**: any Python dependencies with C extensions must have ARM wheels available
- **geojson size**: ~14k point records is small (~2MB uncompressed) — no pagination needed for now

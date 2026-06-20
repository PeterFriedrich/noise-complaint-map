# Specification

> Read-only after first commit to main. Decisions live here; changes go in ARCHITECTURE.md.

## Problem

Edmonton residents and curious observers have no easy way to see where noise complaints are concentrated, whether complaints are trending up, or which days of the week are noisiest. This tool makes that data explorable without requiring any backend query infrastructure.

## Goals

- Fetch noise complaint data from Edmonton Open Data (Socrata) on a recurring schedule
- Generate a static map visualization broken down by day of week
- Host the result on GitHub Pages — zero backend, zero cost
- Show geographic density of complaints and basic trend information

## Non-Goals (explicitly out of scope)

- Real-time or on-demand querying (static only in phase 1)
- User accounts or saved searches
- Mobile-native app
- Complaints data outside Edmonton

## Constraints

- Static output only — no server-side rendering at query time
- Lightweight: site must load fast on a normal connection without a bundler pipeline
- Pipeline runs on Oracle Cloud Free Tier (Ampere ARM) — must work on ARM Linux, no paid services
- Data source: Edmonton Open Data via Socrata API

## Key Decisions

| Decision | Choice | Rationale | Alternatives Rejected |
|---|---|---|---|
| Hosting | GitHub Pages | Free, zero ops, fits static constraint | Vercel, Netlify (more setup) |
| Pipeline runtime | Oracle Free Tier (Ampere ARM) | Already available, free, persistent cron | GitHub Actions (limited minutes, less control) |
| Data source | Edmonton Open Data / Socrata | Official source, has update frequency, free API | Scraping (fragile) |
| Pipeline language | Python | User's primary data language | Node.js, Go |
| JS map library | deck.gl + MapLibre GL | 3D extruded hexbins (isometric look), real Edmonton basemap, interactive rotate/zoom/pan | Leaflet (no 3D extrusion), Three.js (loses geo context), Unity WebGL (massive build size, no auto data reload) |
| Map tiles | Protomaps (self-hosted `.pmtiles`) | No external tile service dependency, single file in repo, free | OpenStreetMap CDN (external dependency), Mapbox (paid) |

## Open Questions

- ~~Which specific Socrata dataset ID covers noise complaints?~~ **Resolved:** `ypje-j649` ("Bylaw Complaint Details") — filter on `Complaint Category = "Noise"`. 14,656 noise records as of confirmation.
- ~~What geographic granularity is available?~~ **Resolved:** lat/lon per complaint is available, plus `Neighbourhood` and `Neighbourhood ID`.
- ~~How frequently does the dataset update on Edmonton's end?~~ **Resolved:** Daily. Pipeline cron should run overnight once per day.
- ~~What map tile provider / JS visualization library?~~ **Resolved:** deck.gl + MapLibre GL with self-hosted Protomaps tiles.

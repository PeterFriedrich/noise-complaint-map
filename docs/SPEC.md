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
- Isometric / 3D rendering (deferred to phase 2)
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

## Open Questions

- ~~Which specific Socrata dataset ID covers noise complaints?~~ **Resolved:** `ypje-j649` ("Bylaw Complaint Details") — filter on `Complaint Category = "Noise"`. 14,656 noise records as of confirmation.
- ~~What geographic granularity is available?~~ **Resolved:** lat/lon per complaint is available, plus `Neighbourhood` and `Neighbourhood ID`.
- How frequently does the dataset update on Edmonton's end? (Affects cron schedule — check dataset metadata or contact open data team)
- What map tile provider should be used for the base map, if any? (OpenStreetMap/Leaflet vs. pure canvas)
- What JS visualization library for phase 1? (Leaflet + heatmap plugin, D3, or deck.gl stub for future isometric)

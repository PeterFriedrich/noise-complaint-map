# Phases

## Phase 0 — One-time Infrastructure Setup (prerequisite, not repeated by pipeline)

GitHub Pages has documented, browser-inconsistent failures serving `.pmtiles` range requests. The basemap lives on Cloudflare R2 instead, which is built for this. This is a one-time manual step — the daily pipeline never touches it.

**Steps:**
1. Create a Cloudflare R2 bucket (free tier: 10 GB storage, zero egress fees)
2. Enable CORS on the bucket (allow GET from `*` or the GitHub Pages domain)
3. Install the `pmtiles` CLI: `pip install pmtiles` or grab the binary from the Protomaps releases
4. Extract Edmonton from the Protomaps planet build:
   ```bash
   pmtiles extract https://build.protomaps.com/<latest-date>.pmtiles edmonton.pmtiles \
     --bbox=-113.7,53.4,-113.2,53.7 --maxzoom=14
   ```
   Expected size: ~40–80 MB for Edmonton at street level.
5. Upload `edmonton.pmtiles` to the R2 bucket and make it public
6. Note the public R2 URL — wire it into `site/js/config.js` as the `BASEMAP_URL`

**Done when:**
- [ ] `edmonton.pmtiles` is publicly accessible on R2
- [ ] CORS allows GET from GitHub Pages domain
- [ ] MapLibre GL can load the basemap from the R2 URL in a local browser test

---

## Phase 1 — Static Map with 3D Extrusion (MVP)

**In scope:**
- Python pipeline: fetch from Socrata, aggregate into hex bins, output `complaints.geojson`
- deck.gl `HexagonLayer` with `extruded: true` — 3D columns by complaint density, tilted/oblique view
- MapLibre GL basemap loaded from R2 (`edmonton.pmtiles`)
- Day-of-week filter — toggleable, updates column heights client-side
- Cron job on Oracle Ampere runs pipeline nightly, commits + pushes `site/` to GitHub

**Out of scope (deferred):**
- Interactive filtering beyond day-of-week
- Real-time or on-demand queries
- Mobile optimization beyond basic responsiveness

**Done when:**
- [ ] Phase 0 infrastructure is in place (basemap on R2)
- [ ] Pipeline runs end-to-end on Oracle Ampere without manual intervention
- [ ] `site/data/complaints.geojson` is generated with correct schema
- [ ] GitHub Pages serves `site/index.html`, MapLibre basemap loads from R2, deck.gl extrusion renders without console errors
- [ ] Day-of-week toggle updates the 3D layer
- [ ] Cron has run at least once unattended and pushed updated data
- [ ] Tests pass for `transform.py` aggregation logic
- [ ] README has accurate setup/run instructions

---

## Backlog (unscheduled)

- Time-of-day breakdown (morning / afternoon / night)
- Complaint category breakdown (construction, music, etc.) if available in dataset
- Neighbourhood search / highlight
- Embed mode for sharing individual day views
- Alert if complaint count spikes above threshold
- Normalize complaint counts by neighbourhood population (raw counts favour dense areas)

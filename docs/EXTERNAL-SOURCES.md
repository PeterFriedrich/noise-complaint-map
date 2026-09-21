# External Sources

Sources other than Edmonton Open Data that could complement this project. None of
these are wired into the pipeline. This file is evaluation notes — a source moves
into `docs/DATA.md` only if it is actually adopted.

---

## Edmonton Noise Watch (`sethdear.ca`)

Recon date: 2026-09-21. Status: **candidate, not adopted.**

### What it is

An independent, DIY noise-monitoring project for Edmonton — a small fleet of
roadside sensors ("noise-bots") measuring vehicle/traffic noise on three
corridors, published through a personal site with an advocacy framing (dBA
"violations", estimated tailpipe dBA, curfew/nighttime statistics, corridor
dispatches).

**Not a municipal source.** It is not run by the City of Edmonton, is not on
`edmonton.ca` or the Open Data portal, and carries no official standing. The
hardware sits at residential windows (stations are described by floor number and
setback from the road), not at municipal monitoring sites. Anything taken from
it is unofficial measurement data and must be labelled that way anywhere it
surfaces in the site.

### Stations

| Station | Corridor | Placement | Violations logged |
|---|---|---|---|
| Cloverdale | 98 Ave | floor 3, 7.8 m from road | 2,453 |
| Whyte Ave | 82 Ave / 110 St | floor 1, 5 m from road | 221 |
| Brewery District | 104 Ave / 124 St | floor 13, 36.3 m from road | 89 |

Counts are as observed on the recon date. Note how strongly placement appears to
drive the numbers — floor 1 at 5 m versus floor 13 at 36 m is not a like-for-like
comparison, and the raw violation counts are not comparable across stations
without normalizing for height and setback. Treat the per-station totals as
descriptive of the sensor, not of the corridor.

### Public endpoints (no auth, observed on recon date)

| Endpoint | Returns |
|---|---|
| `GET https://sethdear.ca/api/fleet-data` | JSON root feed: per-station `current_dba`, `last_peak_dba`, 20-point rolling `history`, `is_online`, firmware version; plus `recent_violations[]`, an `insights` block (dB distribution, peak event, peak hours, nighttime share, weekly summary, sound-energy multipliers) and `server_time` |
| `GET https://sethdear.ca/api/export-csv` | CSV of recent events: timestamp, station, corridor, recorded dBA, estimated tailpipe dBA, tag |
| `GET https://sethdear.ca/yegnoise` | Fuller hub page (Chart.js, unified feed) |
| `/recordings/*.wav` | Individual noise-event audio clips |

Other paths referenced in the site's JavaScript (per-station detail, violations,
newsletter and subscriber admin, a PIN-gated panel) return 404 from the public
root — they are gated or served elsewhere. The per-corridor subdomains referenced
in the front end do not resolve publicly. Do not go looking for them; the two
endpoints above are the whole usable surface.

The feed also exposes internal fleet plumbing — private-mesh addresses and
per-sensor poll URLs — alongside the public measurements. Deliberately not
reproduced here, and any parser we write should drop those fields on ingest
rather than carry them into `site/data/`.

### Stack (for reference)

Frameworkless single HTML page, vanilla JS templating, Tailwind play CDN, Chart.js
on the hub page, no build step. Back end is a small self-hosted Python web app
(Flask/FastAPI shape) serving JSON and CSV with unix-timestamp floats, behind
Cloudflare. Sensors are Raspberry-Pi-class, firmware v1.4, aggregated by a central
hub that polls each one over a private mesh.

### Why it is interesting here

This project maps **complaints** — a report that someone was bothered enough to
call. Noise Watch measures **sound** — dBA at a fixed point, continuously. They
answer different questions, and the gap between them is the interesting part:

- Do the corridors with sensors show complaint density proportional to measured
  dBA, or is there a reporting gap (loud but nobody calls, or quiet but heavily
  reported)?
- The weekday-over-weekend complaint pattern in `docs/FINDINGS.md` is
  counterintuitive. Continuous dBA on a traffic corridor would show whether the
  underlying *sound* follows the same weekday shape, which would point at traffic
  rather than at reporting behaviour.
- Time-of-day: the feed's peak-hours and nighttime-share fields are directly
  comparable to the time-of-day breakdown already in the backlog.

### Why it is not adopted

- **Three points, one noise type.** Three fixed sensors on traffic corridors
  cannot be mapped against a city-wide complaint surface. There is nothing to
  hexbin.
- **Provenance.** Unofficial, single-operator, self-published, with an explicit
  advocacy framing. Mixing it into a map built on the City's open data would blur
  a distinction worth keeping sharp.
- **Not comparable across stations.** See the placement note above.
- **No stability guarantee.** A personal project's undocumented endpoints can
  change or disappear without notice; the pipeline currently depends only on a
  versioned municipal API.
- **Live feed, static site.** A rolling 20-point history and "current dBA" are
  realtime-shaped data, and realtime querying is a stated non-goal in
  `docs/SPEC.md`. Only the aggregate `insights` and the CSV event history fit a
  daily static build at all.

### If it is ever adopted

- Ask the operator first. Unauthenticated does not mean licensed for reuse, and
  there is no published license or terms on the site.
- Ingest the CSV export, not the live station block — it is the only part with a
  static-build-shaped cadence.
- Keep it in a separate output file and a separate layer. Do not merge measured
  dBA into `complaints.geojson`; the data contract there is one feature per
  complaint (see `docs/ARCHITECTURE.md`).
- Label it in the UI as independent, unofficial, resident-operated measurement.
- Drop internal mesh fields at ingest.

### Follow-up, unrelated to the pipeline

The site serves an unauthenticated JSON feed and CSV export that include internal
fleet addressing alongside the public measurements. Everything was served openly —
nothing was bypassed to see it — but the operator may not have intended the
internal fields to be public. Worth a courtesy heads-up if there is a way to
reach them.

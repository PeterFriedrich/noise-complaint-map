# Decisions Index

Append-only. **One ROW per locked decision** — when, what, why (including what
was rejected), and a pointer to where the argument lives in full. When a decision
locks, add a row; when one is superseded, strike it (`~~...~~`) or mark it
`SUPERSEDED <date>` in place and add the successor — don't delete history.

**What a row owes you:**

1. ⚠️ **EVERY ROW CARRIES A POINTER TO A DOC** — not only to code. Code moves;
   the argument has to live somewhere prose can hold it.
   `scripts/check_doc_citations.py` checks that every pointer resolves.
2. **The row is a self-contained summary** and may paraphrase the argument.
3. **The pointer is the authority.** When a row and its target disagree, the
   target wins and the row gets fixed.
4. **A row names the test that protects it**, or carries `[unverifiable]`.
   `scripts/check_decisions_log.py` enforces this on the merge gate (and that a
   superseded row is marked where it stands).

| When | Decision | Full reasoning |
|------|----------|----------------|
| 2026-06-20 | **Hexbin the complaints in 3D with deck.gl over a MapLibre basemap**, rather than Leaflet (no extrusion) or Three.js (loses geo context). | `docs/SPEC.md`, Key Decisions table |
| 2026-06-20 | **Render with a standalone `deck.Deck` and a hand-made canvas, NOT `deck.MapboxOverlay`.** The overlay does not draw in Firefox at all — the canvas is created and nothing renders — with `interleaved` either way. | `session-summary/2026-06-20.md` §4 |
| 2026-06-20 | **Authenticate to Socrata with HTTP basic auth** (key id + secret), not the `X-App-Token` header, which does not work with these credentials. | `docs/DATA.md`, "Source" |
| 2026-06-20 | **Host the basemap on Cloudflare R2, not GitHub Pages.** Pages serves `.pmtiles` range requests inconsistently by browser. | `docs/PHASES.md`, Phase 0 |
| 2026-06-20 | **Deploy `site/` with a GitHub Actions workflow** rather than Pages' folder setting: Pages serves only `/` or `/docs`, and `docs/` is project documentation here. | `session-summary/2026-06-20.md` §4 |
| 2026-06-20 | **One GeoJSON feature per complaint; deck.gl bins at render time.** No pre-aggregation in the pipeline. | `docs/ARCHITECTURE.md`, Key Interfaces |
| 2026-09-21 | **Do not adopt the Edmonton Noise Watch sensor feed** as a data source: three fixed points can't be binned against a city-wide complaint surface, provenance is unofficial, stations aren't comparable to each other, and a live rolling feed conflicts with static-only. Recorded rather than discarded so the question isn't re-opened cold. `[unverifiable]` — a not-adopting decision has no number to protect. | `docs/EXTERNAL-SOURCES.md` |
| 2026-09-21 | **Adopt the workflow apparatus from `cc-data-project-template`**: merge gate, doc/decision guards, handoff-gap hooks, TODO archive discipline. Protected by `check_decisions_log.py` and `check_doc_citations.py` on the merge gate, plus `test_at_most_three_handoffs_at_top_level`. | `CONTRIBUTING.md`, "Before you push" |

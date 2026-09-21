# AUDIT LEDGER — what has been audited, when, and what came back

One row per **executed audit run**. This is the coverage map the audit docs
don't give individually: briefs are reusable *instruments*, findings docs record
*one run's output*, and the `project-audit` skill deliberately picks ONE target
per session — so nothing else says what has and hasn't been looked at. This does.

Rules: add a row when an audit **executes** (not when a brief is written); every
row carries a **pointer to the findings doc**; verdicts are **point-in-time** — a
row says the target was audited *as of that date*, not that it's still clean
after later changes. Not part of any session's mandatory reading — open it to
scope an audit or to check what has already been covered. Audits are framed
top-down, fundamental decisions first.

## Executed audits

| Date | Target / scope | Instrument | Output | Verdict (one line) | Outstanding |
|------|----------------|------------|--------|--------------------|-------------|

## Queued — briefed, not yet run

## Never audited (candidates, roughly ranked)

Roughly ranked, highest-leverage first. These are the numbers the site
publishes or implies — a wrong one here is wrong in public.

- **The download's completeness.** `fetch.py` pages until a short batch and
  never checks its count against the server's. Everything downstream inherits
  whatever it got. (`TODO.md` carries the fix; audit whether the fix holds.)
- **The weekday-over-weekend finding.** `docs/FINDINGS.md` calls it
  counterintuitive and the site surfaces it. Is it real, or an artifact of how
  `dow` is derived from `date_created` (timezone? a late-night Friday call
  logged Saturday)?
- **`dow` derivation and timezone handling** in `transform.py` — the input is a
  naive `date_created` string; nothing states what zone it is in.
- **The hexbin as a unit of analysis.** deck.gl bins at render time by radius;
  what the columns mean changes with zoom. Does the legend claim more than the
  binning supports?
- **Raw counts as the published measure.** Density favours dense areas;
  population normalization is in the `docs/PHASES.md` backlog, unshipped.
- **`meta.json` freshness.** A build timestamp is not a data timestamp —
  see `TODO.md`.

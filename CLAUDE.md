# noise-complaint-map

## Stack
Python 3.x, pandas, sodapy (Socrata client), HTML/CSS/JS (no bundler), GitHub Pages

## Key Commands
- Run pipeline: `TODO — fill after env confirmed`
- Test: `TODO — fill after env confirmed`
- Lint: `TODO — fill after env confirmed`

## Structure
```
pipeline/    ← data fetch, transform, site generation
site/        ← generated static output (committed to repo)
docs/        ← spec, architecture, phases
tests/       ← pipeline unit tests
session-summary/ ← handoff docs
```

## Hard Rules
- Do not add backend query infrastructure — static output only
- pipeline/ runs on ARM Linux (Oracle Ampere) — verify any new dependencies have ARM wheels
- site/ is generated output — never hand-edit files in site/
- Run tests before committing pipeline changes
- See docs/ARCHITECTURE.md before changing the data contract (site/data/*.json schema)

## Docs
- Spec (read-only): docs/SPEC.md
- Architecture: docs/ARCHITECTURE.md
- Phases: docs/PHASES.md
- Session handoff: session-summary/

## Session Loop
Work → /handoff → /clear → restore from session-summary/

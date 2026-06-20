# noise-complaint-map

## Stack
Python 3.11, requests, HTML/CSS/JS (no bundler), GitHub Pages

## Environment
```bash
conda env create -f environment.yml
conda activate noise-complaint-map
```

## Key Commands
- Run pipeline: `bash pipeline/run.sh`
- Run pipeline steps individually: `python3 pipeline/fetch.py && python3 pipeline/transform.py && python3 pipeline/generate.py`
- Test: `python3 -m pytest tests/ -v`

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
- Data sources & fields: docs/DATA.md
- Session handoff: session-summary/

## Session Loop
Work → /handoff → /clear → restore from session-summary/

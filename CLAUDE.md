# noise-complaint-map

## Project
Static map of Edmonton noise complaints. A Python pipeline on Oracle Ampere
fetches from Edmonton Open Data (Socrata), writes GeoJSON + JSON into `site/`,
and pushes; GitHub Pages serves it and deck.gl renders 3D hexbins by day of
week. It is deliberately **not** a queryable service — static output only.

## Stack
Python 3.11, requests, HTML/CSS/JS (no bundler), GitHub Pages

## Environment
```bash
conda env create -f environment.yml
conda activate noise-complaint-map
git config core.hooksPath .githooks   # hooks are NOT cloned — see Session Management
```
In a web/remote session there is no conda and no pytest — read `docs/REMOTE_VM.md` FIRST.

## Key Commands
- Run pipeline: `bash pipeline/run.sh`
- Run steps individually: `python3 pipeline/fetch.py && python3 pipeline/transform.py && python3 pipeline/generate.py`
- Test: `python3 -m pytest tests/ -v`
- Guards (also on the merge gate): `python3 scripts/check_doc_citations.py && python3 scripts/check_decisions_log.py`

## Structure
```
pipeline/    ← data fetch, transform, site generation
site/        ← generated static output (committed to repo)
docs/        ← spec, architecture, phases, ledgers
scripts/     ← guards (check_*.py) and operational scripts
tests/       ← pipeline unit tests + repo invariants
tools/       ← maintenance tooling (todo_archive, retrieval_report)
session-summary/ ← handoff docs; archive/ holds all but the newest 3
```

## Key Files
- `TODO.md` — living backlog and **the source of truth for progress**. Read it
  first to know what to work on; update in place. Session summaries narrate
  *what happened*; TODO.md owns *what's left*. Never redo a closed item without
  asking — `## Done` lists every closed item in one line. Conversely an *open*
  item can be stale: reproduce the symptom before acting on it. **When an item
  closes, move its body to `docs/TODO_archive.md`** (`python3 tools/todo_archive.py`).
- `docs/REMOTE_VM.md` — **read FIRST in a web/remote session**: what is missing
  from the container, the network policy, the branch and PR rules that differ.
- `docs/DECISIONS.md` — append-only index of locked decisions: one row + a
  pointer to the doc holding the reasoning. **Add a row whenever a decision
  locks.** Check it before reopening anything that feels already settled.
- `docs/DATA.md` — source, fields, quirks, and the download-completeness and
  vintage rules. **Read before touching data; update on any discovery.**
- `docs/DATA_ISSUES.md` — defects in data we do NOT control, and **whether the
  publisher has been told**. A finding that never leaves the repo is the
  standing failure mode; "the artifact exists" is not sent.
- `docs/TOKEN_EFFICIENCY.md` — **read before bulk-reading data or summaries.**
- `docs/AUDIT_LEDGER.md` — what has been audited, when, and what came back.
  Add a row when an audit executes; check it before scoping a new one.
- `docs/EXTERNAL-SOURCES.md` — candidate sources evaluated and not adopted.
- `docs/SPEC.md` (read-only), `docs/ARCHITECTURE.md`, `docs/PHASES.md`,
  `docs/FINDINGS.md`, `CONTRIBUTING.md` — spec, contracts, phases, data
  findings, workflow.
- `session-summary/` — read the **latest** before starting; older ones live in
  `archive/` (don't bulk-read them).

## Token Efficiency
- **Never `Read` raw data files** — `site/data/complaints.geojson` (~2 MB, 14.6k
  features) and `data/raw_complaints.json` will swamp the context. Inspect with
  a small python summary instead. See `docs/TOKEN_EFFICIENCY.md`.
- Read only the **latest** session summary; keep the 3 most recent at top level
  and archive older — enforced by `tests/test_loaded_path.py`.
- Many small reads cost more than a few large ones. Decide what you need, then
  batch it.

## Session Management
- Always run `/handoff` before `/clear` — never wipe context without a written
  record in `session-summary/`. **You do not need to be told when one is owed:**
  the `SessionStart`/`SessionEnd` hooks run `scripts/handoff_gap.py`, which
  names the commits and uncommitted files that landed after the newest handoff
  was last committed, and **says nothing when nothing is owed**. Silence means
  no code has moved — not that the record is good.
- Commit after each working unit with a descriptive message, rather than
  batching a session into one commit.
- **Pushing is normal — push proactively after committing.** In a remote
  container this is survival, not tidiness: unpushed work is lost when it is
  reclaimed (`docs/REMOTE_VM.md`).
- **⚠️ The owner merges PRs mid-session, often within minutes. Re-check before
  EVERY push to an existing branch.** Commits pushed after the PR merged land
  on a dead branch: on origin, not on main. After a merge, restart the branch
  from `origin/main` rather than stacking onto merged history.
  - `.githooks/pre-push` blocks a push to a branch whose PR is `MERGED`. **A
    fresh clone must enable it: `git config core.hooksPath .githooks`.** It
    fails OPEN (no `gh`, no auth, no network, no PR), so it can never be the
    reason work goes unsaved — and `gh` is absent in web containers, where it
    is therefore a no-op. Escape hatch: `git push --no-verify`.
  - After any merge, confirm the work landed:
    `git merge-base --is-ancestor <sha> origin/main`. A merged PR is necessary,
    not sufficient.

## Hard Rules
- Do not add backend query infrastructure — static output only
- `pipeline/` runs on ARM Linux (Oracle Ampere) — verify any new dependency has ARM wheels
- `site/` is generated output — never hand-edit files in `site/`
- Run tests before committing pipeline changes
- See `docs/ARCHITECTURE.md` before changing the data contract (`site/data/*.json` schema)

## Code Style
- **A decision that protects a number is a test first, prose second.** Write the
  guard, then the `DECISIONS.md` row cites it; a row with nothing to cite is
  tagged `[unverifiable]`. `scripts/check_decisions_log.py` gates new rows.
- **No silent data drops** — flag unmatched or missing records explicitly. A
  truncated download is the same class: verify the count, fail hard.
- Keep processing steps as separate, independently runnable modules in `pipeline/`
- Cite docs by `§N` or section title, never by line number — line citations rot
  silently and `scripts/check_doc_citations.py` rejects them.

## Comments & Scope
- Comments only where the *why* is non-obvious. Don't narrate what the code does.
- Make the **smallest change that satisfies the request**. Don't refactor,
  rename, or reformat code you weren't asked to touch.
- No abstractions for a single use case — inline until there are 3+ call sites.
- Deleting obsolete code is valid and **preferred** over leaving it behind.
- **Propose the plan first** for: a new pipeline module, a change to the data
  contract or output schema, or anything that changes CI behaviour.
- These are scope rules, not verification rules. They do **not** relax
  `no silent data drops`, the guard scripts, or reproducing a bug before fixing
  it — data projects fail by silent-correctness.

## Session Loop
Work → `/handoff` → `/clear` → restore from `session-summary/`

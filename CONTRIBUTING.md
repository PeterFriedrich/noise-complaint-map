# Contributing

## Development Pipeline

Work follows this sequence. Do not skip steps — each one informs the next.

| Step | Artifact | Purpose |
|------|----------|---------|
| 1. Spec | `docs/SPEC.md` (read-only after first commit) | What to build, inputs/outputs, acceptance criteria |
| 2. Architecture | `docs/ARCHITECTURE.md` | Module contracts, data flow, key technical decisions |
| 3. Implementation | `pipeline/*.py` | One module at a time, in data flow order |
| 4. Tests | `tests/*.py` | Per module, synthetic data only |

`docs/SPEC.md` is frozen: decisions that change it are recorded in
`docs/DECISIONS.md` and `docs/ARCHITECTURE.md`, not by editing the spec. New
phases get their scope written in `docs/PHASES.md` before any code.

### AI-assisted workflow

This project is worked on with Claude Code. The pipeline above is designed for it:

- **Spec first** — a written spec gives unambiguous scope. Without one, the gaps
  get filled with assumptions.
- **Architecture before implementation** — explicit module interfaces prevent
  different design decisions across separate conversations.
- **One module at a time** — implement, review, then move on.
- **Tests alongside each module** — while the design intent is still in context.
- **`CLAUDE.md` is the working memory** — a convention that is not written there
  does not survive the next `/clear`.
- **A decision is a test first, prose second** — `docs/DECISIONS.md` rows cite
  the guard that protects them.

## Getting Started

```bash
conda env create -f environment.yml
conda activate noise-complaint-map
git config core.hooksPath .githooks   # NOT cloned automatically; see CLAUDE.md
python3 -m pytest tests/ -q           # synthetic data only — no credentials needed
```

Raw data is not committed (`data/raw_complaints.json` is a pipeline cache). The
pipeline needs Socrata credentials in `.env` — see `.env.example` and
`docs/DATA.md`. The test suite does not.

## Code Conventions

- **One file per processing step** in `pipeline/` — each independently runnable
- **No silent data drops** — flag unmatched or missing records explicitly
  (count + examples). A truncated download is the same class: verify the count,
  fail hard.
- **No hardcoded paths** — constants at the top of the entry point, passed down
- **`site/` is generated output** — never hand-edit it; change the generator
- **No backend query infrastructure** — static output only (`docs/SPEC.md`)

## Before you push

The merge gate (`.github/workflows/tests.yml`) runs pytest and the two doc
guards on every PR. Run them locally first — they are offline and take a second:

```bash
python3 -m pytest tests/ -q
python3 scripts/check_doc_citations.py
python3 scripts/check_decisions_log.py
```

## Project Structure

```
/
├── pipeline/                 # One module per processing step (fetch/transform/generate)
├── site/                     # GENERATED static output — committed, never hand-edited
│   └── data/                 # complaints.geojson + meta.json, rewritten each run
├── docs/                     # Spec, architecture, ledgers — see CLAUDE.md
├── scripts/                  # Guards (check_*.py) and operational scripts
├── tests/                    # Synthetic-data tests + repo invariants
├── tools/                    # Maintenance tooling (todo_archive, retrieval_report)
├── session-summary/          # Handoffs; archive/ holds all but the newest 3
├── .githooks/pre-push        # Blocks pushing to a branch whose PR already merged
├── CLAUDE.md
├── TODO.md
└── README.md
```

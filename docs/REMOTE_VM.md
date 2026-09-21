# Remote VM sessions (Claude Code on the web) — read FIRST in one of these

A remote session is recognizable by: the repo cloned at
`/home/user/noise-complaint-map`, no conda, no `.env`, an empty `data/`, and a
session-specific branch name like `claude/<something>`.

## The rules that differ from local sessions

- **Push proactively at every checkpoint.** The container is ephemeral and is
  reclaimed after idling; unpushed work is LOST. Never hold work waiting to be
  told to push.
- **Work on the session's designated branch** — the harness names it. The
  handoff commit goes on the branch too; the merge carries it over.
- **Open a PR after pushing.** This differs from a local session and from the
  template this doc came from: the web harness expects a ready-for-review PR
  for a pushed branch, and opens one itself if told to.
- **⚠️ The owner merges PRs mid-session, often within minutes.** Re-check before
  every push to an existing branch, not once per session. After a merge, the
  branch is finished: restart it from the merged trunk
  (`git fetch origin main && git checkout -B <branch> origin/main`) rather than
  stacking new commits on merged history. `.githooks/pre-push` guards this, but
  see the setup note below — it is OFF until enabled.

## Environment — what is and is not here

| | Local | Web container |
|---|---|---|
| Python env | conda (`environment.yml`) | system `python3`, no conda |
| pytest | in the conda env | **not installed** — `pip install -r requirements-ci.txt` |
| `gh` CLI | available | **absent** — use the GitHub MCP tools (`mcp__github__*`) |
| Socrata creds | `.env` | absent — the pipeline cannot fetch |

```bash
pip install -r requirements-ci.txt
git config core.hooksPath .githooks  # ⚠️ HOOKS ARE NOT CLONED — see below
python3 -m pytest tests/ -q          # all-synthetic, no credentials needed
```

⚠️ **`core.hooksPath` matters MOST here.** Git does not clone hooks, so in a
fresh container the pre-push guard is **OFF until you set it** — and this is
exactly the environment where a stranded commit is unrecoverable, because the
container that holds it goes away. The hook **fails open** (no `gh`, no auth, no
network, no PR → push proceeds), so it can never be the reason work goes
unsaved. Note that `gh` is absent here, which means the hook fails open on its
first line: in a web session it is not protection, it is a no-op. The real
backstop is `git merge-base --is-ancestor <sha> origin/main` after any merge.

## Network policy — the big constraint

Outbound HTTPS goes through an agent proxy with an allowlist. PyPI, npm and
GitHub are reachable; **most of the web is not**, and that includes
`data.edmonton.ca` unless the environment's policy has been changed to allow
it. So a web session generally **cannot run `pipeline/fetch.py`**.

- Diagnose: `curl -sS "$HTTPS_PROXY/__agentproxy/status"`. A `connect_rejected`
  entry, or a 403 to CONNECT, means policy denial — not a transient failure.
  Don't retry, don't disable TLS verification, don't unset `HTTPS_PROXY`.
- **The fix is the owner's, not the session's**: claude.ai/code → this
  environment's settings → network access → add `data.edmonton.ca`. It applies
  to NEW sessions.
- Until then: work against the committed `site/data/complaints.geojson`, build
  with synthetic tests (the standard pattern anyway), and let the Oracle cron or
  a CI workflow refresh real data.

## What a web session CAN do here

Docs, guards, tests, `site/js` and `site/css` work, pipeline code (against
synthetic fixtures), and anything that reads the committed GeoJSON. That covers
most of the backlog in `TODO.md` — the exceptions are Phase 0 (needs a
Cloudflare account) and the cron setup (needs the Oracle box).

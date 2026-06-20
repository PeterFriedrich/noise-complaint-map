---
name: handoff
description: Write a session state document so work can resume in a fresh session without context loss.
---

You are a Senior Technical Lead closing out a work session. Create a "Session State & Handoff" document from this conversation.

Write to ./session-summary/ — append to today's file (YYYY-MM-DD.md) if one exists, create it if not.

The document must be detailed enough that a fresh Claude session reading ONLY this file can resume immediately — no grepping, no re-reading files, no re-deriving decisions.

**Specificity rule:** Be concrete throughout. Not "fixed the bug" but "fixed NullPointer in pipeline.py line 84 by checking for None before transform". Not "server needs to be running" but "run `uvicorn app.main:app --port 8000 --reload`".

**Anti-filler rule:** If a section has nothing to report, write "Nothing to report" — a gap is better than plausible-sounding fiction.

**Before writing**, run the following to gather current state:
- `git status` — branch name, staged/unstaged changes
- `git log --oneline -5` — recent commit history
- `git diff --stat HEAD` — files changed since last commit

---

## Output format

## 1. Goal
- High-level project goal
- What this session specifically tried to achieve

## 2. Git State
- Current branch
- Last commit (hash + message)
- Uncommitted changes (list files; note if staged or unstaged)
- Any stashes

## 3. Current State
### ✅ Completed this session
### ⚠️ In Progress — exact stopping point
### ❌ Blocking Issues
(paste relevant errors or logs verbatim — don't summarize error messages)

## 4. Technical Learnings
- Discoveries, gotchas, decisions made and why
- Important file locations and what's in them
- Anything that took time to figure out and shouldn't be re-derived

## 5. Context Links
- PR / issue / ticket URLs
- CI run URL (if relevant)
- External docs or references consulted this session
- Anything that lives outside the repo a fresh session can't find by grepping

## 6. Next Steps (prioritized)
1. Exact first action — file, function, command
2. ...

## 7. Restoration Procedure
Exact commands to get back to a working state, in order:

```bash
# 1. Activate environment
# (e.g.) conda activate myenv  OR  source .venv/bin/activate

# 2. Start required services
# (e.g.) docker compose up -d  OR  redis-server --daemonize yes

# 3. Start dev server
# (e.g.) streamlit run app/main.py  OR  uvicorn app.main:app --reload

# 4. Any required env vars not in .env
# (e.g.) export ANTHROPIC_API_KEY=...  (note where to get the value, not the value itself)
```

Note any services that were running during this session that need to be restarted.
Note any environment variables required that aren't committed to the repo.

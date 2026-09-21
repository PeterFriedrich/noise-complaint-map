# TODO

The source of truth for what's left. Read first every session; update in place.
Session summaries narrate *what happened*; this file owns *what's left*.

**Format contract** (`tools/todo_archive.py` depends on it): top-level items are
`- [ ]` / `- [x]` lines directly under `## Open work`; `###` sub-headings may
group them; closed items are moved to `docs/TODO_archive.md` by the tool, which
leaves a one-line stub under `## Done`. An open item can be stale — reproduce the
symptom and re-measure the stated cause before acting on it.

## Open work

### Pipeline correctness

- [ ] **`fetch.py` has no download-completeness guard.** It pages until a short
      batch and trusts the result: no check that the row count it got matches
      what the server says it holds. A Socrata query that caps or pages
      truncates *silently* — it returns rows with no error — so a partial fetch
      would publish a thinner map with every test still green. Add a count
      check against the live total (`$select=count(*)` with the same `$where`)
      and fail hard on a mismatch. Done when a deliberately truncated fetch
      fails the run instead of committing.
- [ ] **No vintage recorded per fetch.** `meta.json` carries a build timestamp
      and a record count; it does not carry the dataset's own last-updated
      stamp. If Socrata stalls, the site keeps saying "last updated today"
      because the *build* ran. Record the publisher's stamp and surface the
      older of the two. Guard must measure the data (max `date_created` in the
      file), never a metadata string.

### Phase 0 — basemap (blocks Phase 1 completion)

- [ ] **Cloudflare R2 + Protomaps basemap.** Full steps in `docs/PHASES.md`
      Phase 0. Create bucket, enable CORS, `pmtiles extract` the Edmonton bbox,
      upload, then re-add MapLibre GL + pmtiles.js to `site/index.html`,
      restore `buildStyle()` in `site/js/map.js` (removed in `2bbabf3`), and set
      `BASEMAP_URL` in `site/js/config.js`. Done when the basemap renders under
      the hexagons in a local browser test.

### Operations

- [ ] **Cron on the Oracle Ampere box.** Run `bash pipeline/run.sh` nightly.
      Needs SSH access, git credentials on the server, and the conda env
      created there. Done when one unattended run has pushed updated data.
- [ ] **Delete the merged `pipeline` branch:** `git push origin --delete pipeline`.
- [ ] **Enable the pre-push hook in every working clone:**
      `git config core.hooksPath .githooks`. Git does not clone hooks, so this
      is off by default in a fresh checkout and in every web session container.

### Data exploration

- [ ] Time-of-day distribution (morning / afternoon / evening / night).
- [ ] Geographic clustering — which neighbourhoods or hex cells concentrate
      complaints.
- [ ] Whether the weekday spike is driven by specific complaint types or times
      of day. See also the corridor-sound cross-check in `docs/FINDINGS.md`.

### Outstanding, not ours to fix

- [ ] **Tell the operator of `sethdear.ca` about the unauthenticated feed.** It
      serves internal fleet addressing alongside public measurements. Row is in
      `docs/DATA_ISSUES.md` with status **NOT SENT** — the status is the point
      of that file; a finding that never leaves the repo is the failure mode.

## Done

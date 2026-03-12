---
description: Log local work done on GMS project and post to Jira
---
# Work Logging and Posting

**When to log:** After completing any task that is **GMS project development work** (Confluence pages, WP files, GMS code).
**When NOT to log:** Tooling/codespace work (`confluence_sync.py`, `log_work.py`, `CLAUDE.md` updates, etc.)

## 1. Log a task locally
```sh
python3 scripts/logging/log_work.py log \
  --task "<short description of what was done>" \
  --score <1-10> \
  --files "<path/to/files>" \
  [--ticket <PBL26-XXX>]
```
- `--score`: effort weight 1-10 (default 5). Higher score = more time allocated when posting worklogs.
- `--ticket`: auto-detected from the WP number in task/files. If unable to match, it exits with code 2.

## 2. Post worklogs to Jira
Reads all log entries in the date range, divides hours proportionally by score, and POSTs a worklog to each entry's `pbl26_ticket`. Duplicate-safe: skips entries whose task description already exists as a worklog comment on that ticket.

```sh
python3 scripts/logging/log_work.py worklog \
  --from <YYYY-MM-DD> \
  [--to <YYYY-MM-DD>] \
  [--hours <number, default 6>]
```

## 3. Log work directly to Jira (no local file)
Use for work done outside of Claude (manually, on another device, etc.).

```sh
python3 scripts/logging/log_work.py log-direct \
  --ticket <WP_NUMBER or PBL26-XXX> \
  --task "<description>" \
  --hours <number> \
  [--date <YYYY-MM-DD>]
```
- `--ticket`: accepts WP number (e.g. `5.4`) or full key (e.g. `PBL26-563`).
- `--hours`: decimals supported (e.g. `1.5` = 1h 30m), rounded to nearest 5 min.
- `--date`: defaults to today.

## 4. Log workshop day attendance (report-log)
Posts two fixed worklogs to `PBL26-1362` (the class tracking ticket) for a workshop day.

```sh
python3 scripts/logging/log_work.py report-log \
  [--date <YYYY-MM-DD>] \
  [--task "<desc1>" "<desc2>"]
```
- Always posts: `15:15` (1h 30m) and `19:00` (1h 30m).
- Descriptions default to generic workshop text if `--task` is omitted.
- `--date` defaults to today.

## 5. Weekly standup report
Fetches all worklogs from every PBL26 ticket in the date range and prints a standup-style summary.

```sh
python3 scripts/logging/log_work.py report \
  --from <YYYY-MM-DD> \
  [--to <YYYY-MM-DD>]
```
- Shows what was done, total hours, and which WP to work on next (first WP with no worklogs).
- `--to` defaults to now.

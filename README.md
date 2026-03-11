# Greenhouse Management System (GMS)

PBL IoT course project — Technical University of Moldova (UTM)

**Team:** Alexei Maxim, Vremere Adrian, Cojocaru Daniel, Rațeeva Daria, Mutruc Victoria

---

## Repository Structure

```
documentation/
  confluence/
    confluence_pages.json   ← page ID map + config
    cloud/                  ← auto-synced .gcm files fetched from Confluence
    wip/                    ← files currently being actively worked on
    resources/              ← local reference/learning materials (not synced)
  jira/
    board.html              ← local interactive Jira board shell
scripts/
  confluence/
    confluence_sync.py      ← fetch Confluence → local .gcm files
    confluence_push.py      ← push local .gcm edits back to Confluence
    gcm_from_html.py        ← converter: Confluence storage HTML → GCM
    gcm_to_html.py          ← converter: GCM → Confluence storage HTML
    gcm_spec.py             ← shared GCM constants and utilities
    GCM_SPEC.md             ← GCM format specification
  jira/
    jira_board_server.py    ← local interactive Jira board API/server + Jira automation commands
.env                        ← credentials (never commit)
```

---

## Setup

Copy `.env.example` to `.env` and fill in your credentials:

```
CONFLUENCE_URL=http://confluence.microlab.club
CONFLUENCE_USER=your_username
CONFLUENCE_PASS=your_password

# Optional — defaults to jira.microlab.club and falls back to CONFLUENCE_USER/PASS
JIRA_URL=http://jira.microlab.club
JIRA_USER=your_username
JIRA_PASS=your_password
```

---

## Jira Workflow

Start the live local board server:

```sh
python3 scripts/jira/jira_board_server.py
```

Then open `documentation/jira/board.html` in VS Code Live Preview.

Jira-specific files live only in `documentation/jira/` and `scripts/jira/`.

The board pulls live data from Jira and supports local edits for summary, description, due date, assignee, and status transitions. Jira ticket references in Confluence pages (for example `[CDR-53](../../jira/board.html#cdr-53)`) resolve to the local board, while push back to Confluence still restores proper Jira macros linked to the online Jira instance.

The same script also exposes direct CLI commands for faster agentic operations:

```sh
python3 scripts/jira/jira_board_server.py users --query "Adrian Vremere"
python3 scripts/jira/jira_board_server.py assign --assignee adrian.vremere GMS-16 GMS-17
python3 scripts/jira/jira_board_server.py move --column proposed GMS-35
python3 scripts/jira/jira_board_server.py bulk-move --column proposed GMS-35 GMS-36
python3 scripts/jira/jira_board_server.py update --key GMS-35 --summary "New summary"
python3 scripts/jira/jira_board_server.py bulk-update --assignee adrian.vremere GMS-35 GMS-36
python3 scripts/jira/jira_board_server.py comment --key GMS-35 --text "Reviewed"
python3 scripts/jira/jira_board_server.py bulk-comment --text "Reviewed" GMS-35 GMS-36
python3 scripts/jira/jira_board_server.py create --issue-type Task --summary "New task"
```

---

## Confluence Workflow

Confluence-specific files live only in `documentation/confluence/` and `scripts/confluence/`.

### GCM — GMS Confluence Markup

Local copies of Confluence pages are stored in **GCM format** (`.gcm` files), a custom
line-oriented markup designed for lossless round-tripping of Confluence storage HTML.
See `scripts/confluence/GCM_SPEC.md` for the full format specification.

Key syntax:
- Headings: `= H1`, `== H2`, `=== H3`
- Bold/italic: `**bold**`, `*italic*`
- Links: `[text](url)`, `{link page="Page Title"}text{/link}`
- Jira issues: `{jira:GMS-10}`
- Tables: `{table}…{/table}` with full `rowspan`/`colspan` support
- Images: `{image file="diagram.png" height=400}`
- Raw passthrough: `{raw}…{/raw}` for any unrecognized Confluence XML

### Syncing

Fetch pages from Confluence up to a given work package:

```sh
python3 scripts/confluence/confluence_sync.py --up-to 5.4
python3 scripts/confluence/confluence_sync.py --up-to 5.4 --dry-run
python3 scripts/confluence/confluence_sync.py --up-to 5.4 --force
```

Pages are fetched in ascending WP order, converted from Confluence storage HTML to GCM,
and written to `documentation/confluence/cloud/*.gcm`. Version caching enables incremental sync.

### Pushing Changes

```sh
python3 scripts/confluence/confluence_push.py --file WP4.2_Analyze_Stakeholder_Requirements.gcm
python3 scripts/confluence/confluence_push.py --file WP4.2_Analyze_Stakeholder_Requirements.gcm --dry-run
```

- Only pushes if local file differs from last sync (hash-based detection)
- Detects Confluence version conflicts
- Use `--dry-run` to preview the converted XHTML without pushing
- Use `--no-confirm` to skip the confirmation prompt

### Editing Workflow

1. Edit the `.gcm` file in `documentation/confluence/cloud/`
2. Push back to Confluence using `scripts/confluence/confluence_push.py`

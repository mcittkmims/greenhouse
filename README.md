# Greenhouse Management System (GMS)

PBL IoT course project — Technical University of Moldova (UTM)

**Team:** Alexei Maxim, Vremere Adrian, Cojocaru Daniel, Rațeeva Daria, Mutruc Victoria

---

## Repository Structure

```
documentation/
  confluence_pages.json     ← page ID map + config
  cloud/                    ← auto-synced copies fetched from Confluence (do not manually edit)
  wip/                      ← files currently being actively worked on
  resources/                ← local reference/learning materials (not synced to Confluence)
scripts/
  confluence_sync.py        ← fetch pages from Confluence
  confluence_push.py        ← push local edits back to Confluence
.env                        ← credentials (never commit)
```

---

## Setup

Copy `.env.example` to `.env` and fill in your credentials:

```
CONFLUENCE_URL=http://confluence.microlab.club
CONFLUENCE_USER=your_username
CONFLUENCE_PASS=your_password
```

---

## Syncing Documentation

Fetch pages from Confluence up to a given work package:

```sh
python3 scripts/confluence_sync.py --up-to 5.4
```

Pages are fetched in ascending WP order: 1.1 → 2.1 → 3.1 → 3.2 → 3.3 → 3.4 → 4.1 → 4.2 → 4.3 → 5.1 → 5.2 → 5.3 → 5.4 → ...

---

## Pushing Changes to Confluence

```sh
python3 scripts/confluence_push.py --file WP4.2_Analyze_Stakeholder_Requirements.md
```

- Shows a diff against the cached cloud copy before pushing
- Use `--dry-run` to preview without pushing
- Use `--no-confirm` to skip the confirmation prompt

---

## Editing Workflow

1. Move the target file from `documentation/cloud/` to `documentation/wip/`
2. Edit the file
3. Push back to Confluence using `confluence_push.py`
4. Move the file back to `documentation/cloud/`

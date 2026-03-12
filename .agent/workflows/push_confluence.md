---
description: Push local GCM changes back to Confluence
---
# Pushing Documentation to Confluence

Only pushes if local file hash differs from last sync. Converts GCM → Confluence storage XHTML automatically.
Detects version conflicts (warns if Confluence was modified since last sync).

**Command:**
```sh
python3 scripts/confluence/confluence_push.py --file <FILE_NAME.gcm>
```

- Converts GCM → Confluence storage XHTML automatically
- Use `--dry-run` to preview the converted XHTML without pushing
- Use `--no-confirm` to skip the confirmation prompt

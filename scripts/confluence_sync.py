#!/usr/bin/env python3
"""
confluence_sync.py — Fetch GMS Confluence pages and update local markdown files.

Usage:
    python3 scripts/confluence_sync.py --up-to 4.2
    python3 scripts/confluence_sync.py --up-to 3.3 --dry-run

Options:
    --up-to X.Y     Fetch all pages with WP number <= X.Y (in ascending order)
    --dry-run       Print what would be fetched without writing files
    --force         Re-fetch even if the page hasn't changed (based on version)

Credentials are read from .env in the workspace root:
    CONFLUENCE_USER=...
    CONFLUENCE_PASS=...
    CONFLUENCE_URL=http://confluence.microlab.club

Pages config: documentation/confluence_pages.json
Output dir:   documentation/cloud/
"""

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: 'requests' not installed. Run: pip3 install requests")
    sys.exit(1)


ROOT = Path(__file__).parent.parent


# ---------------------------------------------------------------------------
# HTML → Markdown converter
# ---------------------------------------------------------------------------

class ConfluenceHTMLParser(HTMLParser):
    """Converts Confluence storage-format HTML to clean Markdown."""

    def __init__(self):
        super().__init__()
        self.output = []
        self._in_table = False
        self._table_rows = []
        self._current_row = []
        self._current_cell = []
        self._col_index = 0
        # pending_rowspans: {col_index: (remaining_rows, cell_text)}
        self._pending_rowspans = {}
        self._skip_tags = {"style", "script"}
        self._skip_depth = 0
        self._list_depth = 0
        self._in_heading = 0
        self._heading_text = []

    # -- helpers --

    def _clean(self, text):
        text = re.sub(r"\s+", " ", text)
        for e, r in [("&nbsp;", " "), ("&lt;", "<"), ("&gt;", ">"),
                     ("&amp;", "&"), ("&quot;", '"'), ("&#39;", "'")]:
            text = text.replace(e, r)
        return text.strip()

    def _flush_table(self):
        if not self._table_rows:
            return
        max_cols = max(len(r) for r in self._table_rows)
        rows = [r + [""] * (max_cols - len(r)) for r in self._table_rows]
        lines = []
        for i, row in enumerate(rows):
            line = "| " + " | ".join(cell.replace("|", "\\|") for cell in row) + " |"
            lines.append(line)
            if i == 0:
                lines.append("|" + "|".join(" --- " for _ in row) + "|")
        self.output.append("\n" + "\n".join(lines) + "\n")
        self._table_rows = []
        self._pending_rowspans = {}

    def _inject_pending_rowspans(self):
        """Inject any rowspan-carried cells at the current col_index position."""
        while self._col_index in self._pending_rowspans:
            remaining, text = self._pending_rowspans[self._col_index]
            self._current_row.append(text)
            if remaining <= 1:
                del self._pending_rowspans[self._col_index]
            else:
                self._pending_rowspans[self._col_index] = (remaining - 1, text)
            self._col_index += 1

    # -- tag handlers --

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs_dict = dict(attrs)

        if tag in self._skip_tags:
            self._skip_depth += 1
            return
        if self._skip_depth:
            return

        if tag == "table":
            self._in_table = True
            self._table_rows = []
            self._pending_rowspans = {}
        elif tag == "tr":
            self._current_row = []
            self._col_index = 0
        elif tag in ("td", "th"):
            self._current_cell = []
            # Inject carried rowspan cells before this new cell
            self._inject_pending_rowspans()
            # Note rowspan for this cell (text filled in on endtag)
            rowspan = int(attrs_dict.get("rowspan", 1))
            if rowspan > 1:
                self._pending_rowspans[self._col_index] = (rowspan - 1, "")
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._in_heading = int(tag[1])
            self._heading_text = []
        elif tag in ("ul", "ol"):
            self._list_depth += 1
        elif tag == "li":
            self.output.append("\n" + "  " * (self._list_depth - 1) + "- ")
        elif tag == "br":
            if self._in_table:
                self._current_cell.append(" ")
            else:
                self.output.append("\n")
        elif tag == "p":
            if not self._in_table:
                self.output.append("\n")
        elif tag in ("strong", "b"):
            if self._in_table:
                self._current_cell.append("**")
            else:
                self.output.append("**")
        elif tag in ("em", "i"):
            if self._in_table:
                self._current_cell.append("*")
            else:
                self.output.append("*")

    def handle_endtag(self, tag):
        tag = tag.lower()

        if tag in self._skip_tags:
            self._skip_depth = max(0, self._skip_depth - 1)
            return
        if self._skip_depth:
            return

        if tag == "table":
            self._flush_table()
            self._in_table = False
        elif tag == "tr":
            # Inject any remaining pending rowspans at the tail of the row
            if self._pending_rowspans:
                max_col = max(self._pending_rowspans.keys())
                while self._col_index <= max_col:
                    self._inject_pending_rowspans()
                    self._col_index += 1  # safety advance if no pending at this index
            self._table_rows.append(self._current_row)
            self._current_row = []
        elif tag in ("td", "th"):
            text = self._clean("".join(self._current_cell))
            self._current_row.append(text)
            # Update the pending rowspan entry with the actual cell text
            if self._col_index in self._pending_rowspans:
                remaining = self._pending_rowspans[self._col_index][0]
                self._pending_rowspans[self._col_index] = (remaining, text)
            self._col_index += 1
            self._current_cell = []
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = self._in_heading
            text = self._clean(" ".join(self._heading_text))
            self.output.append(f"\n\n{'#' * level} {text}\n\n")
            self._in_heading = 0
            self._heading_text = []
        elif tag in ("ul", "ol"):
            self._list_depth = max(0, self._list_depth - 1)
            if self._list_depth == 0:
                self.output.append("\n")
        elif tag in ("strong", "b"):
            if self._in_table:
                self._current_cell.append("**")
            else:
                self.output.append("**")
        elif tag in ("em", "i"):
            if self._in_table:
                self._current_cell.append("*")
            else:
                self.output.append("*")

    def handle_data(self, data):
        if self._skip_depth:
            return
        if self._in_heading:
            self._heading_text.append(data)
        elif self._in_table:
            self._current_cell.append(data)
        else:
            self.output.append(data)

    def get_markdown(self):
        text = "".join(self.output)
        for e, r in [("&nbsp;", " "), ("&lt;", "<"), ("&gt;", ">"),
                     ("&amp;", "&"), ("&quot;", '"')]:
            text = text.replace(e, r)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()


def html_to_markdown(html):
    parser = ConfluenceHTMLParser()
    parser.feed(html)
    return parser.get_markdown()


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def load_env():
    env_path = ROOT / ".env"
    if not env_path.exists():
        print(f"ERROR: .env not found at {env_path}")
        sys.exit(1)
    env = {}
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


def load_config():
    config_path = ROOT / "documentation" / "confluence_pages.json"
    if not config_path.exists():
        print(f"ERROR: Config not found at {config_path}")
        sys.exit(1)
    return json.loads(config_path.read_text())


def wp_sort_key(wp_str):
    """Convert '3.2' -> (3, 2) for sorting."""
    return tuple(int(p) for p in wp_str.split("."))


def fetch_page(page_id, base_url, auth):
    url = f"{base_url}/rest/api/content/{page_id}?expand=body.storage,version"
    resp = requests.get(url, auth=auth, timeout=15)
    resp.raise_for_status()
    return resp.json()


def pages_up_to(config, up_to_str):
    limit = wp_sort_key(up_to_str)
    result = []
    for page in config["pages"]:
        if wp_sort_key(page["wp"]) <= limit:
            result.append(page)
    result.sort(key=lambda p: wp_sort_key(p["wp"]))
    return result


def main():
    parser = argparse.ArgumentParser(description="Sync GMS Confluence pages to local markdown.")
    parser.add_argument("--up-to", required=True, metavar="X.Y", help="Fetch pages with WP number up to X.Y")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be done without writing")
    parser.add_argument("--force", action="store_true", help="Re-fetch even if version hasn't changed")
    args = parser.parse_args()

    env = load_env()
    config = load_config()
    auth = (env["CONFLUENCE_USER"], env["CONFLUENCE_PASS"])
    base_url = env.get("CONFLUENCE_URL", config["base_url"])
    out_dir = ROOT / "documentation" / "cloud"
    cache_dir = out_dir / ".cache"
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    pages = pages_up_to(config, args.up_to)
    if not pages:
        print(f"No pages found with WP <= {args.up_to}")
        sys.exit(0)

    print(f"Pages to sync (up to WP {args.up_to}):")
    for p in pages:
        skip = p.get("skip_fetch", False)
        note = f"  [SKIP — {p['note']}]" if skip else ""
        print(f"  WP{p['wp']} — {p['local_file']}{note}")

    if args.dry_run:
        print("\n[dry-run] No files written.")
        return

    print()
    for page in pages:
        if page.get("skip_fetch"):
            print(f"  SKIP   WP{page['wp']} ({page.get('note', '')})")
            continue

        local_path = out_dir / page["local_file"]

        # Check cached version
        version_cache_path = cache_dir / f"{page['local_file']}.version"
        cached_version = None
        if version_cache_path.exists():
            cached_version = version_cache_path.read_text().strip()

        try:
            data = fetch_page(page["id"], base_url, auth)
        except Exception as e:
            print(f"  ERROR  WP{page['wp']} — {e}")
            continue

        current_version = str(data.get("version", {}).get("number", ""))
        title = data.get("title", f"WP{page['wp']}")
        html = data["body"]["storage"]["value"]

        if not args.force and cached_version == current_version and local_path.exists():
            print(f"  UP-TO-DATE  WP{page['wp']} (version {current_version})")
            continue

        content = html_to_markdown(html)
        markdown = f"# {title}\n\n> Source: {base_url}/rest/api/content/{page['id']} | Version: {current_version}\n\n{content}\n"

        local_path.write_text(markdown, encoding="utf-8")
        version_cache_path.write_text(current_version, encoding="utf-8")
        print(f"  UPDATED WP{page['wp']} — {page['local_file']} (version {current_version})")

    print("\nSync complete.")


if __name__ == "__main__":
    main()

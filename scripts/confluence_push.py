#!/usr/bin/env python3
"""
confluence_push.py — Push a local markdown file back to Confluence.

Compares the local file against the last-synced cloud/ copy to show what
changed, then converts the local Markdown to Confluence storage format
and updates the page via the REST API.

Usage:
    python3 scripts/confluence_push.py --file WP4.2_Analyze_Stakeholder_Requirements.md
    python3 scripts/confluence_push.py --file WP4.2_Analyze_Stakeholder_Requirements.md --dry-run

Options:
    --file FILE     Filename to push (looks in documentation/cloud/ and documentation/wip/)
    --dry-run       Show diff and converted content without pushing
    --no-confirm    Skip confirmation prompt (auto-confirm push)

Credentials are read from .env in the workspace root.
Page IDs are read from documentation/confluence_pages.json.
"""

import argparse
import json
import re
import sys
import tempfile
from difflib import unified_diff
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: 'requests' not installed. Run: pip3 install requests")
    sys.exit(1)

ROOT = Path(__file__).parent.parent

# Import html_to_markdown from the sync script
sys.path.insert(0, str(Path(__file__).parent))
from confluence_sync import html_to_markdown


# ---------------------------------------------------------------------------
# Markdown → Confluence storage format (XHTML) converter
# ---------------------------------------------------------------------------

def _escape_xhtml(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _inline_markup(text):
    """Convert inline Markdown (bold, italic, inline code) to XHTML."""
    # Extract markup spans before escaping so < > inside plain text are escaped
    # but markers like ** and * are handled first.
    # Bold+italic: ***text***
    text = re.sub(r"\*\*\*(.+?)\*\*\*", lambda m: f"<strong><em>{_escape_xhtml(m.group(1))}</em></strong>", text)
    # Bold: **text**
    text = re.sub(r"\*\*(.+?)\*\*", lambda m: f"<strong>{_escape_xhtml(m.group(1))}</strong>", text)
    # Italic: *text* or _text_  (not preceded/followed by another * or _)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", lambda m: f"<em>{_escape_xhtml(m.group(1))}</em>", text)
    text = re.sub(r"(?<!_)_(?!_)(.+?)(?<!_)_(?!_)", lambda m: f"<em>{_escape_xhtml(m.group(1))}</em>", text)
    # Inline code: `code`
    text = re.sub(r"`(.+?)`", lambda m: f"<code>{_escape_xhtml(m.group(1))}</code>", text)
    # Escape remaining plain text (not inside tags)
    def escape_outside_tags(s):
        result = []
        i = 0
        while i < len(s):
            if s[i] == '<':
                end = s.find('>', i)
                if end != -1:
                    result.append(s[i:end+1])
                    i = end + 1
                    continue
            result.append(s[i])
            i += 1
        return ''.join(result)
    return text


def _table_row_to_xhtml(line, is_header=False):
    """Convert a Markdown table row to Confluence XHTML <tr>."""
    tag = "th" if is_header else "td"
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    cells_xhtml = "".join(f"<{tag}><p>{_inline_markup(c)}</p></{tag}>" for c in cells)
    return f"<tr>{cells_xhtml}</tr>"


def markdown_to_confluence(md_text):
    """Convert Markdown text to Confluence storage format XHTML."""
    lines = md_text.splitlines()
    output = []
    i = 0

    # Strip auto-generated metadata lines (# Title, > Source: ..., blank lines after)
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith("# ") or stripped.startswith("> Source:") or stripped == "":
            i += 1
        else:
            break

    in_code_block = False
    in_table = False
    table_lines = []
    list_stack = []  # stack of 'ul' or 'ol'
    paragraph_lines = []

    def flush_paragraph():
        if paragraph_lines:
            text = " ".join(paragraph_lines).strip()
            if text:
                output.append(f"<p>{_inline_markup(text)}</p>")
            paragraph_lines.clear()

    def flush_table():
        if not table_lines:
            return
        output.append("<table><tbody>")
        for j, tline in enumerate(table_lines):
            if re.match(r"^\s*\|[\s\-:|]+\|\s*$", tline):
                continue  # separator row
            is_header = j == 0
            output.append(_table_row_to_xhtml(tline, is_header))
        output.append("</tbody></table>")
        table_lines.clear()

    def close_lists():
        while list_stack:
            output.append(f"</{list_stack.pop()}>")

    while i < len(lines):
        line = lines[i]

        # ---- Code block ----
        if line.startswith("```"):
            if not in_code_block:
                flush_paragraph()
                close_lists()
                lang = line[3:].strip()
                output.append(f'<ac:structured-macro ac:name="code"><ac:plain-text-body><![CDATA[')
                in_code_block = True
            else:
                output.append("]]></ac:plain-text-body></ac:structured-macro>")
                in_code_block = False
            i += 1
            continue

        if in_code_block:
            output.append(line)
            i += 1
            continue

        # ---- Table ----
        if line.strip().startswith("|"):
            flush_paragraph()
            close_lists()
            table_lines.append(line)
            in_table = True
            i += 1
            continue
        elif in_table:
            flush_table()
            in_table = False
            continue

        # ---- Heading ----
        m = re.match(r"^(#{1,6})\s+(.+)", line)
        if m:
            flush_paragraph()
            close_lists()
            level = len(m.group(1))
            text = _inline_markup(_escape_xhtml(m.group(2).strip()))
            output.append(f"<h{level}>{text}</h{level}>")
            i += 1
            continue

        # ---- Unordered list ----
        m = re.match(r"^(\s*)[-*+]\s+(.+)", line)
        if m:
            flush_paragraph()
            indent = len(m.group(1)) // 2
            text = _inline_markup(m.group(2))
            # Open/close list tags based on indent depth
            while len(list_stack) > indent + 1:
                output.append(f"</{list_stack.pop()}>")
            if len(list_stack) <= indent:
                output.append("<ul>")
                list_stack.append("ul")
            output.append(f"<li>{text}</li>")
            i += 1
            continue

        # ---- Ordered list ----
        m = re.match(r"^(\s*)\d+\.\s+(.+)", line)
        if m:
            flush_paragraph()
            indent = len(m.group(1)) // 2
            text = _inline_markup(m.group(2))
            while len(list_stack) > indent + 1:
                output.append(f"</{list_stack.pop()}>")
            if len(list_stack) <= indent:
                output.append("<ol>")
                list_stack.append("ol")
            output.append(f"<li>{text}</li>")
            i += 1
            continue

        # ---- Horizontal rule ----
        if re.match(r"^[-*_]{3,}\s*$", line):
            flush_paragraph()
            close_lists()
            output.append("<hr/>")
            i += 1
            continue

        # ---- Blank line ----
        if not line.strip():
            flush_paragraph()
            close_lists()
            i += 1
            continue

        # ---- Regular paragraph text ----
        close_lists()
        paragraph_lines.append(line.strip())
        i += 1

    flush_paragraph()
    if in_table:
        flush_table()
    close_lists()

    return "\n".join(output)


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


def find_page_entry(config, filename):
    """Find a page config entry by filename (basename, no path needed)."""
    basename = Path(filename).name
    for page in config["pages"]:
        if page["local_file"] == basename:
            return page
    return None


def find_local_file(filename):
    """Locate the file in cloud/ only."""
    basename = Path(filename).name
    p = ROOT / "documentation" / "cloud" / basename
    return p if p.exists() else None


def fetch_page(page_id, base_url, auth):
    url = f"{base_url}/rest/api/content/{page_id}?expand=body.storage,version,title"
    resp = requests.get(url, auth=auth, timeout=15)
    resp.raise_for_status()
    return resp.json()


def push_page(page_id, title, version_number, storage_xhtml, base_url, auth):
    url = f"{base_url}/rest/api/content/{page_id}"
    payload = {
        "id": page_id,
        "type": "page",
        "title": title,
        "version": {"number": version_number, "minorEdit": True},
        "body": {
            "storage": {
                "value": storage_xhtml,
                "representation": "storage"
            }
        }
    }
    resp = requests.put(url, json=payload, auth=auth, timeout=30)
    resp.raise_for_status()
    return resp.json()


def show_diff(cloud_path, local_path):
    """Print a unified diff between cloud and local versions. Returns True if different."""
    if cloud_path and cloud_path.exists():
        cloud_lines = cloud_path.read_text(encoding="utf-8").splitlines(keepends=True)
    else:
        cloud_lines = []
    local_lines = local_path.read_text(encoding="utf-8").splitlines(keepends=True)

    diff = list(unified_diff(
        cloud_lines, local_lines,
        fromfile=f"cloud/{local_path.name}",
        tofile=f"local/{local_path.name}",
        lineterm=""
    ))

    if not diff:
        return False

    added = sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))
    removed = sum(1 for l in diff if l.startswith("-") and not l.startswith("---"))
    print(f"\n--- Diff: {added} lines added, {removed} lines removed ---\n")
    for line in diff:
        print(line)
    print()
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Push a local markdown file to Confluence.")
    parser.add_argument("--file", required=True, metavar="FILE",
                        help="Filename to push (e.g. WP4.2_Analyze_Stakeholder_Requirements.md)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show diff and converted XHTML without pushing")
    parser.add_argument("--no-confirm", action="store_true",
                        help="Skip confirmation prompt")
    args = parser.parse_args()

    env = load_env()
    config = load_config()
    auth = (env["CONFLUENCE_USER"], env["CONFLUENCE_PASS"])
    base_url = env.get("CONFLUENCE_URL", config["base_url"])

    # Locate local file
    local_path = find_local_file(args.file)
    if not local_path:
        print(f"ERROR: File not found in documentation/cloud/: {Path(args.file).name}")
        print("Only files in documentation/cloud/ can be pushed to Confluence.")
        sys.exit(1)

    print(f"Local file:  {local_path}")

    # Find config entry
    page_entry = find_page_entry(config, args.file)
    if not page_entry:
        print(f"ERROR: No page entry found for '{Path(args.file).name}' in confluence_pages.json")
        sys.exit(1)

    page_id = page_entry["id"]
    print(f"Page ID:     {page_id}  (WP{page_entry['wp']})")

    # Fetch live content from Confluence to diff against
    print("Fetching current Confluence content...")
    try:
        data = fetch_page(page_id, base_url, auth)
    except Exception as e:
        print(f"ERROR: Failed to fetch page: {e}")
        sys.exit(1)

    current_version = data["version"]["number"]
    title = data["title"]
    live_html = data["body"]["storage"]["value"]
    live_md = f"# {title}\n\n> Source: {base_url}/rest/api/content/{page_id} | Version: {current_version}\n\n{html_to_markdown(live_html)}\n"

    print(f"Confluence version: {current_version}  |  Title: {title}")

    # Conflict detection: check if Confluence was modified since last local sync
    cache_dir = ROOT / "documentation" / "cloud" / ".cache"
    version_cache_path = cache_dir / f"{page_entry['local_file']}.version"
    if version_cache_path.exists():
        cached_version = version_cache_path.read_text().strip()
        if str(current_version) != cached_version:
            print(f"\nCONFLICT: Confluence page was modified since your last sync.")
            print(f"  Your cached version : {cached_version}")
            print(f"  Current live version: {current_version}")
            print(f"\nRun the sync script first to review the remote changes:")
            print(f"  python3 scripts/confluence_sync.py --up-to {page_entry['wp']} --force")
            sys.exit(1)
    else:
        print("Warning: No local version cache found — skipping conflict check.")
        print("         Run the sync script to establish a baseline before pushing.")

    # Diff live Confluence markdown vs local file
    local_md = local_path.read_text(encoding="utf-8")

    # Write live content to a temp path for diffing
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as tmp:
        tmp.write(live_md)
        tmp_path = Path(tmp.name)

    try:
        has_changes = show_diff(tmp_path, local_path)
    finally:
        tmp_path.unlink(missing_ok=True)

    if not has_changes:
        print("No changes detected vs live Confluence content. Nothing to push.")
        sys.exit(0)

    # Convert local markdown → Confluence storage XHTML
    storage_xhtml = markdown_to_confluence(local_md)

    if args.dry_run:
        print("--- Confluence storage XHTML (dry-run) ---\n")
        print(storage_xhtml[:3000])
        if len(storage_xhtml) > 3000:
            print(f"\n... ({len(storage_xhtml) - 3000} more chars)")
        print("\n[dry-run] Nothing pushed.")
        return

    new_version = current_version + 1
    print(f"New version: {new_version}")

    # Confirm
    if not args.no_confirm:
        answer = input(f"\nPush to Confluence? [y/N] ").strip().lower()
        if answer != "y":
            print("Aborted.")
            sys.exit(0)

    # Push
    print("Pushing...")
    try:
        result = push_page(page_id, title, new_version, storage_xhtml, base_url, auth)
    except requests.HTTPError as e:
        print(f"ERROR: Push failed: {e}")
        if e.response is not None:
            print(e.response.text[:1000])
        sys.exit(1)

    pushed_version = result.get("version", {}).get("number", new_version)
    print(f"\nSUCCESS: WP{page_entry['wp']} pushed to Confluence (version {pushed_version})")

    # Update local version cache
    cache_dir = ROOT / "documentation" / "cloud" / ".cache"
    cache_dir.mkdir(exist_ok=True)
    (cache_dir / f"{page_entry['local_file']}.version").write_text(str(pushed_version))
    print(f"Updated version cache: version {pushed_version}")


if __name__ == "__main__":
    main()

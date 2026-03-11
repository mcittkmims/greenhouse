"""
gcm_spec.py — GCM (GMS Confluence Markup) shared constants and utilities.

Provides attribute parsing, escaping, and tag-name helpers used by both
the HTML→GCM converter and the GCM→HTML converter.
"""

import re

# ---------------------------------------------------------------------------
# File extension
# ---------------------------------------------------------------------------
GCM_EXT = ".gcm"

# ---------------------------------------------------------------------------
# Front-matter
# ---------------------------------------------------------------------------

def format_frontmatter(title, page_id, version, source_url=""):
    lines = ["--- gcm ---"]
    lines.append(f"title: {title}")
    lines.append(f"page_id: {page_id}")
    lines.append(f"version: {version}")
    if source_url:
        lines.append(f"source: {source_url}")
    lines.append("---")
    return "\n".join(lines)


def parse_frontmatter(text):
    """Parse GCM front-matter. Returns (metadata_dict, body_text)."""
    m = re.match(r'^--- gcm ---\n(.*?)\n---\n?', text, re.DOTALL)
    if not m:
        return {}, text
    meta_block = m.group(1)
    body = text[m.end():]
    meta = {}
    for line in meta_block.splitlines():
        line = line.strip()
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, body


# ---------------------------------------------------------------------------
# Tag attribute parsing / formatting
# ---------------------------------------------------------------------------

def parse_tag_attrs(attr_str):
    """Parse 'key=value key2="val with spaces"' into dict.
    
    Supports:
      key=value          (unquoted, no spaces)
      key="value"        (double-quoted)
      key='value'        (single-quoted)
    """
    attrs = {}
    for m in re.finditer(
        r"""([a-zA-Z_][\w:.-]*)\s*=\s*(?:"([^"]*)"|'([^']*)'|(\S+))""",
        attr_str
    ):
        key = m.group(1)
        val = m.group(2) if m.group(2) is not None else (
              m.group(3) if m.group(3) is not None else m.group(4))
        attrs[key] = val
    return attrs


def format_tag_attrs(attrs):
    """Format a dict into 'key=value key2="val ue"' string."""
    parts = []
    for k, v in attrs.items():
        if v is None or v == "":
            continue
        if " " in v or '"' in v or "'" in v or "=" in v:
            v_esc = v.replace('"', '\\"')
            parts.append(f'{k}="{v_esc}"')
        else:
            parts.append(f"{k}={v}")
    return " ".join(parts)


# ---------------------------------------------------------------------------
# Inline escaping
# ---------------------------------------------------------------------------

_INLINE_SPECIAL = re.compile(r'([{}*\[\]~`\\])')

def escape_inline(text):
    """Escape GCM special characters in plain text."""
    return _INLINE_SPECIAL.sub(r'\\\1', text)


def unescape_inline(text):
    """Remove GCM backslash escapes."""
    return re.sub(r'\\([{}*\[\]~`\\])', r'\1', text)


# ---------------------------------------------------------------------------
# XHTML escaping (for the push direction)
# ---------------------------------------------------------------------------

def escape_xhtml(text):
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;"))


def unescape_xhtml(text):
    return (text.replace("&quot;", '"')
                .replace("&gt;", ">")
                .replace("&lt;", "<")
                .replace("&amp;", "&"))

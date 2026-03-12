"""
gcm_preview.py — Convert a .gcm file to a self-contained HTML page for preview.

Usage:
    python3 scripts/confluence/gcm_preview.py <file.gcm>

Outputs the full HTML page to stdout.
"""

import re
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from gcm_spec import parse_frontmatter, parse_tag_attrs

# ── Config ──────────────────────────────────────────────────────────────────

JIRA_URL = os.environ.get("JIRA_URL", "http://jira.microlab.club").rstrip("/")
CONFLUENCE_URL = os.environ.get("CONFLUENCE_URL", "http://confluence.microlab.club").rstrip("/")

STATUS_COLORS = {
    "yellow":  ("#FFF0B3", "#534300"),
    "green":   ("#E3FCEF", "#006644"),
    "red":     ("#FFEBE6", "#BF2600"),
    "blue":    ("#DEEBFF", "#0747A6"),
    "grey":    ("#DFE1E6", "#42526E"),
    "gray":    ("#DFE1E6", "#42526E"),
    "purple":  ("#EAE6FF", "#403294"),
    "teal":    ("#E6FCFF", "#006470"),
}

PANEL_STYLES = {
    "info":    ("ℹ️",  "#DEEBFF", "#0052CC", "#B3D4FF"),
    "note":    ("📝",  "#FFFAE6", "#974F0C", "#FFE380"),
    "warning": ("⚠️",  "#FFEBE6", "#BF2600", "#FF8F73"),
    "tip":     ("💡",  "#E3FCEF", "#006644", "#79F2C0"),
}

# ── HTML escaping ────────────────────────────────────────────────────────────

def _esc(text):
    return (str(text)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))

# ── Inline renderer ──────────────────────────────────────────────────────────

def _render_inline(text):
    """Convert GCM inline markup to displayable HTML."""
    phs = []

    def _ph(html):
        idx = len(phs)
        phs.append(html)
        return f"\x00PH{idx}\x00"

    # {jira:KEY} or {jira:KEY|param=value|...}
    def _jira(m):
        key = m.group(1)
        href = f"{JIRA_URL}/browse/{key}"
        return _ph(f'<a class="jira-issue" href="{href}" target="_blank">{_esc(key)}</a>')
    text = re.sub(r'\{jira:([A-Z][A-Z0-9]*-\d+)((?:\|[^}]+)*)\}', _jira, text)

    # {br}
    text = re.sub(r'\{br\}', lambda m: _ph('<br>'), text)

    # {raw}...{/raw} inline passthrough — show verbatim
    text = re.sub(r'\{raw\}(.*?)\{/raw\}', lambda m: _ph(m.group(1)), text)

    # {anchor:name}
    text = re.sub(
        r'\{anchor:([^}]+)\}',
        lambda m: _ph(f'<a id="{_esc(m.group(1))}" class="anchor"></a>'),
        text
    )

    # {status:Title|color=X|subtle}
    def _status(m):
        parts = m.group(1).split("|")
        title = parts[0] if parts else ""
        color_key = ""
        for p in parts[1:]:
            if p.startswith("color="):
                color_key = p[6:].lower()
        bg, fg = STATUS_COLORS.get(color_key, ("#DFE1E6", "#42526E"))
        return _ph(f'<span class="status-badge" style="background:{bg};color:{fg}">{_esc(title)}</span>')
    text = re.sub(r'\{status:([^}]+)\}', _status, text)

    # {user:key}
    text = re.sub(
        r'\{user:([^}]+)\}',
        lambda m: _ph('<span class="user-badge">@user</span>'),
        text
    )

    # {link page="Title"}text{/link}  or  {link anchor=name}text{/link}
    def _link(m):
        attrs = parse_tag_attrs(m.group(1))
        link_text = m.group(2)
        if "anchor" in attrs:
            return _ph(f'<a href="#{_esc(attrs["anchor"])}">{_esc(link_text)}</a>')
        elif "page" in attrs:
            page = attrs["page"]
            return _ph(f'<a class="confluence-page" title="{_esc(page)}" href="#">{_esc(link_text)}</a>')
        return m.group(0)
    text = re.sub(r'\{link ([^}]+)\}(.*?)\{/link\}', _link, text)

    # {image file="x.png" ...} or {image url="..."}
    def _image(m):
        attrs = parse_tag_attrs(m.group(1))
        style_parts = []
        if "height" in attrs:
            style_parts.append(f'height:{_esc(attrs["height"])}px')
        if "width" in attrs:
            style_parts.append(f'width:{_esc(attrs["width"])}px')
        style_attr = f' style="{";".join(style_parts)}"' if style_parts else ""
        if "url" in attrs:
            return _ph(f'<img src="{_esc(attrs["url"])}" alt="image"{style_attr}>')
        elif "file" in attrs:
            return _ph(f'<span class="image-placeholder" title="{_esc(attrs["file"])}">📎 {_esc(attrs["file"])}</span>')
        return m.group(0)
    text = re.sub(r'\{image ([^}]+)\}', _image, text)

    # {sub}x{/sub}, {sup}x{/sup}, {u}x{/u}
    text = re.sub(r'\{sub\}(.*?)\{/sub\}', lambda m: _ph(f'<sub>{_esc(m.group(1))}</sub>'), text)
    text = re.sub(r'\{sup\}(.*?)\{/sup\}', lambda m: _ph(f'<sup>{_esc(m.group(1))}</sup>'), text)
    text = re.sub(r'\{u\}(.*?)\{/u\}', lambda m: _ph(f'<u>{_esc(m.group(1))}</u>'), text)

    # [text](url) external links
    text = re.sub(
        r'\[([^\[\]]*(?:\[[^\]]*\][^\[\]]*)*)\]\(([^)]+)\)',
        lambda m: _ph(f'<a href="{_esc(m.group(2))}" target="_blank">{_esc(m.group(1))}</a>'),
        text
    )

    ESC_STAR = "\x01STAR\x01"
    text = text.replace("\\*", ESC_STAR)

    text = re.sub(r'\*\*\*(.+?)\*\*\*',
                  lambda m: _ph(f'<strong><em>{_esc(m.group(1).replace(ESC_STAR, "*"))}</em></strong>'), text)
    text = re.sub(r'\*\*(.+?)\*\*',
                  lambda m: _ph(f'<strong>{_esc(m.group(1).replace(ESC_STAR, "*"))}</strong>'), text)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)',
                  lambda m: _ph(f'<em>{_esc(m.group(1).replace(ESC_STAR, "*"))}</em>'), text)
    text = re.sub(r'~~(.+?)~~', lambda m: _ph(f'<del>{_esc(m.group(1))}</del>'), text)
    text = re.sub(r'`(.+?)`', lambda m: _ph(f'<code>{_esc(m.group(1))}</code>'), text)

    # Escape remaining plain text
    parts = re.split(r'(\x00PH\d+\x00)', text)
    result = []
    for part in parts:
        if part.startswith("\x00PH"):
            result.append(part)
        else:
            result.append(_esc(part.replace(ESC_STAR, "*")))
    text = "".join(result)

    changed = True
    while changed:
        changed = False
        for i, html in enumerate(phs):
            marker = f"\x00PH{i}\x00"
            if marker in text:
                text = text.replace(marker, html)
                changed = True

    return text


# ── Block renderer ───────────────────────────────────────────────────────────

def _render_cell_content(cell_text):
    """Render multi-line table cell content."""
    cell_lines = cell_text.strip().split("\n")
    parts = []
    in_list_block = False
    para_buf = []

    def flush_para():
        if para_buf:
            parts.append(f'<p>{"</p><p>".join(para_buf)}</p>')
            para_buf.clear()

    j = 0
    while j < len(cell_lines):
        cl = cell_lines[j]
        stripped = cl.strip()

        # {raw}...{/raw} block inside a cell
        if stripped == "{raw}":
            flush_para()
            j += 1
            raw_parts = []
            while j < len(cell_lines) and cell_lines[j].strip() != "{/raw}":
                raw_parts.append(cell_lines[j])
                j += 1
            raw_content = chr(10).join(raw_parts)
            if "<ac:task-list>" in raw_content or "<ac:task-list" in raw_content:
                tasks_html = []
                for task_m in re.finditer(
                    r'<ac:task>.*?<ac:task-status>(.*?)</ac:task-status>.*?<ac:task-body>(.*?)</ac:task-body>.*?</ac:task>',
                    raw_content, re.DOTALL
                ):
                    status = task_m.group(1).strip()
                    body = re.sub(r'<[^>]+>', '', task_m.group(2)).strip()
                    checked = ' checked' if status == 'complete' else ''
                    tasks_html.append(f'<li class="task-item"><input type="checkbox" disabled{checked}> {_esc(body)}</li>')
                if tasks_html:
                    parts.append(f'<ul class="task-list">{"".join(tasks_html)}</ul>')
            else:
                parts.append(raw_content)
            j += 1
            continue

        if not stripped:
            if not in_list_block:
                flush_para()
            j += 1
            continue
        if stripped in ("{ul}", "{ol}"):
            flush_para()
            lt = stripped[1:-1]
            parts.append(f"<{lt}>")
            in_list_block = True
            j += 1
            continue
        if stripped in ("{/ul}", "{/ol}"):
            lt = stripped[2:-1]
            parts.append(f"</{lt}>")
            in_list_block = False
            j += 1
            continue
        if in_list_block:
            lm = re.match(r'^[-*+]\s+(.+)', stripped)
            if lm:
                parts.append(f"<li>{_render_inline(lm.group(1))}</li>")
                j += 1
                continue
        hm = re.match(r'^(={1,6})\s+(.+)$', stripped)
        if hm:
            flush_para()
            hlev = len(hm.group(1))
            parts.append(f"<h{hlev}>{_render_inline(hm.group(2).strip())}</h{hlev}>")
            j += 1
            continue
        para_buf.append(_render_inline(stripped))
        j += 1

    flush_para()
    return "".join(parts)


def _render_blocks(lines):
    """Render a list of GCM lines to an HTML string."""
    output = []
    i = 0
    paragraph_lines = []
    list_stack = []
    in_blockquote = False
    bq_lines = []

    def flush_paragraph():
        if paragraph_lines:
            text = " ".join(paragraph_lines).strip()
            if text:
                output.append(f"<p>{_render_inline(text)}</p>")
            paragraph_lines.clear()

    def flush_blockquote():
        nonlocal in_blockquote
        if bq_lines:
            inner = " ".join(bq_lines).strip()
            if inner:
                output.append(f"<blockquote><p>{_render_inline(inner)}</p></blockquote>")
            bq_lines.clear()
        in_blockquote = False

    def close_lists():
        while list_stack:
            output.append(f"</{list_stack.pop()}>")

    def collect_until(close_tag):
        """Collect lines until close_tag is found. Returns (inner_lines, new_i)."""
        nonlocal i
        inner = []
        i += 1
        while i < len(lines) and lines[i].strip() != close_tag:
            inner.append(lines[i])
            i += 1
        return inner

    while i < len(lines):
        line = lines[i]

        # {raw}...{/raw}
        if line.strip() == "{raw}":
            flush_paragraph(); flush_blockquote(); close_lists()
            raw_lines = collect_until("{/raw}")
            raw_content = chr(10).join(raw_lines)
            # Render ac:task-list as HTML checkboxes
            if "<ac:task-list>" in raw_content or "<ac:task-list" in raw_content:
                tasks_html = []
                for task_m in re.finditer(
                    r'<ac:task>.*?<ac:task-status>(.*?)</ac:task-status>.*?<ac:task-body>(.*?)</ac:task-body>.*?</ac:task>',
                    raw_content, re.DOTALL
                ):
                    status = task_m.group(1).strip()
                    body = re.sub(r'<[^>]+>', '', task_m.group(2)).strip()
                    checked = ' checked' if status == 'complete' else ''
                    tasks_html.append(f'<li class="task-item"><input type="checkbox" disabled{checked}> {_esc(body)}</li>')
                if tasks_html:
                    output.append(f'<ul class="task-list">{"".join(tasks_html)}</ul>')
            else:
                # Inject other raw HTML directly (browser ignores unknown tags)
                output.append(raw_content)
            i += 1
            continue

        # {code ...}...{/code}
        m = re.match(r'^\{code\b([^}]*)\}$', line.strip())
        if m:
            flush_paragraph(); flush_blockquote(); close_lists()
            attrs = parse_tag_attrs(m.group(1))
            lang = attrs.get("lang", attrs.get("language", ""))
            title = attrs.get("title", "")
            code_lines = collect_until("{/code}")
            header = ""
            if lang or title:
                parts = []
                if lang:
                    parts.append(f'<span class="code-lang">{_esc(lang)}</span>')
                if title:
                    parts.append(f'<span class="code-title">{_esc(title)}</span>')
                header = f'<div class="code-header">{"".join(parts)}</div>'
            output.append(
                f'<div class="code-block">{header}'
                f'<pre><code>{_esc(chr(10).join(code_lines))}</code></pre></div>'
            )
            i += 1
            continue

        # {expand title="..."}...{/expand}
        m = re.match(r'^\{expand\b([^}]*)\}$', line.strip())
        if m:
            flush_paragraph(); flush_blockquote(); close_lists()
            attrs = parse_tag_attrs(m.group(1))
            exp_title = attrs.get("title", "Click to expand")
            inner_lines = collect_until("{/expand}")
            inner_html = _render_blocks(inner_lines)
            output.append(
                f'<details class="expand-block">'
                f'<summary>{_esc(exp_title)}</summary>'
                f'<div class="expand-content">{inner_html}</div>'
                f'</details>'
            )
            i += 1
            continue

        # {info/note/warning/tip ...}...{/info/note/warning/tip}
        m = re.match(r'^\{(info|note|warning|tip)\b([^}]*)\}$', line.strip())
        if m:
            flush_paragraph(); flush_blockquote(); close_lists()
            panel_type = m.group(1)
            attrs = parse_tag_attrs(m.group(2))
            panel_title = attrs.get("title", panel_type.capitalize())
            icon, bg, fg, border = PANEL_STYLES[panel_type]
            inner_lines = collect_until(f"{{/{panel_type}}}")
            inner_html = _render_blocks(inner_lines)
            output.append(
                f'<div class="panel panel-{panel_type}" '
                f'style="background:{bg};border-left:4px solid {border}">'
                f'<div class="panel-header" style="color:{fg}">'
                f'{icon} <strong>{_esc(panel_title)}</strong></div>'
                f'<div class="panel-body">{inner_html}</div>'
                f'</div>'
            )
            i += 1
            continue

        # {table ...}...{/table}
        if re.match(r'^\{table\b', line.strip()):
            flush_paragraph(); flush_blockquote(); close_lists()
            m = re.match(r'^\{table\s*(.*)\}$', line.strip())
            tbl_attrs = parse_tag_attrs(m.group(1) if m else "")
            style = f'width:{tbl_attrs["width"]}' if "width" in tbl_attrs else ""
            style_attr = f' style="{style}"' if style else ""
            output.append(f"<table{style_attr}>")
            i += 1

            while i < len(lines) and lines[i].strip() != "{/table}":
                tl = lines[i].strip()
                simple_map = {
                    "{thead}": "<thead>", "{/thead}": "</thead>",
                    "{tbody}": "<tbody>", "{/tbody}": "</tbody>",
                    "{tfoot}": "<tfoot>", "{/tfoot}": "</tfoot>",
                    "{tr}": "<tr>", "{/tr}": "</tr>",
                    "{colgroup}": "<colgroup>", "{/colgroup}": "</colgroup>",
                }
                if tl in simple_map:
                    output.append(simple_map[tl])
                elif re.match(r'^\{col\b', tl):
                    cm = re.match(r'^\{col\s*(.*)\}$', tl)
                    col_attrs = parse_tag_attrs(cm.group(1)) if cm else {}
                    ca = " ".join(f'{k}="{_esc(v)}"' for k, v in col_attrs.items())
                    output.append(f'<col {ca}/>' if ca else '<col/>')
                elif re.match(r'^\{(td|th)\b', tl):
                    cm = re.match(r'^\{(td|th)\s*([^}]*)\}(.*)$', tl)
                    if cm:
                        cell_tag = cm.group(1)
                        cell_attr_str = cm.group(2)
                        cell_rest = cm.group(3)
                        close_pat = f"{{/{cell_tag}}}"
                        if close_pat in cell_rest:
                            cell_content = cell_rest[:cell_rest.index(close_pat)]
                        else:
                            cell_parts = [cell_rest]
                            i += 1
                            while i < len(lines) and close_pat not in lines[i]:
                                cell_parts.append(lines[i])
                                i += 1
                            if i < len(lines):
                                last = lines[i]
                                cell_parts.append(last[:last.index(close_pat)])
                            cell_content = "\n".join(cell_parts)
                        ca = parse_tag_attrs(cell_attr_str)
                        ca_html = " ".join(f'{k}="{_esc(v)}"' for k, v in ca.items())
                        ca_attr = (" " + ca_html) if ca_html else ""
                        inner = _render_cell_content(cell_content)
                        output.append(f"<{cell_tag}{ca_attr}>{inner}</{cell_tag}>")
                i += 1

            output.append("</table>")
            i += 1
            continue

        # {layout}...{/layout}, {layout-section}...{/layout-section}, {layout-cell}...{/layout-cell}
        m = re.match(r'^\{(layout(?:-section|-cell)?)\b([^}]*)\}$', line.strip())
        if m:
            flush_paragraph(); flush_blockquote(); close_lists()
            tag = m.group(1)
            attrs = parse_tag_attrs(m.group(2))
            cls_extra = f' layout-type-{_esc(attrs["type"])}' if "type" in attrs else ""
            output.append(f'<div class="gcm-{tag}{cls_extra}">')
            i += 1
            continue

        m = re.match(r'^\{/(layout(?:-section|-cell)?)\}$', line.strip())
        if m:
            flush_paragraph(); close_lists()
            output.append("</div>")
            i += 1
            continue

        # {div ...}...{/div}
        m = re.match(r'^\{div\b([^}]*)\}$', line.strip())
        if m:
            flush_paragraph(); flush_blockquote(); close_lists()
            attrs = parse_tag_attrs(m.group(1))
            cls = _esc(attrs.get("class", ""))
            cls_attr = f' class="gcm-div {cls}"' if cls else ' class="gcm-div"'
            output.append(f"<div{cls_attr}>")
            i += 1
            continue

        if line.strip() == "{/div}":
            flush_paragraph(); close_lists()
            output.append("</div>")
            i += 1
            continue

        # Heading
        m = re.match(r'^(={1,6})\s+(.*)$', line)
        if m:
            flush_paragraph(); flush_blockquote(); close_lists()
            level = len(m.group(1))
            htext = _render_inline(m.group(2).strip())
            output.append(f"<h{level}>{htext}</h{level}>")
            i += 1
            continue

        # Horizontal rule
        if re.match(r'^-{4,}\s*$', line):
            flush_paragraph(); flush_blockquote(); close_lists()
            output.append("<hr>")
            i += 1
            continue

        # Blockquote
        if line.startswith("> "):
            flush_paragraph(); close_lists()
            in_blockquote = True
            bq_lines.append(line[2:].strip())
            i += 1
            continue
        elif in_blockquote:
            flush_blockquote()

        # Escaped list-like pattern
        if re.match(r'^\\(-\s|\d+\.\s)', line):
            close_lists()
            paragraph_lines.append(line[1:])
            i += 1
            continue

        # Unordered list
        m = re.match(r'^(\s*)-\s+(.+)', line)
        if m:
            flush_paragraph(); flush_blockquote()
            indent = len(m.group(1)) // 2
            text = _render_inline(m.group(2))
            while len(list_stack) > indent + 1:
                output.append(f"</{list_stack.pop()}>")
            if len(list_stack) <= indent:
                output.append("<ul>")
                list_stack.append("ul")
            output.append(f"<li>{text}</li>")
            i += 1
            continue

        # Ordered list
        m = re.match(r'^(\s*)\d+\.\s+(.+)', line)
        if m:
            flush_paragraph(); flush_blockquote()
            indent = len(m.group(1)) // 2
            text = _render_inline(m.group(2))
            while len(list_stack) > indent + 1:
                output.append(f"</{list_stack.pop()}>")
            if len(list_stack) <= indent:
                output.append("<ol>")
                list_stack.append("ol")
            output.append(f"<li>{text}</li>")
            i += 1
            continue

        # Blank line
        if not line.strip():
            flush_paragraph(); flush_blockquote(); close_lists()
            i += 1
            continue

        # Regular paragraph text
        close_lists()
        paragraph_lines.append(line.strip())
        i += 1

    flush_paragraph()
    flush_blockquote()
    close_lists()

    return "\n".join(output)


# ── Full page generator ──────────────────────────────────────────────────────

CSS = """
*, *::before, *::after { box-sizing: border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: 14px;
  line-height: 1.6;
  color: #172B4D;
  background: #ffffff;
  margin: 0;
  padding: 0;
}

.page-wrapper {
  padding: 24px 24px 48px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #172B4D;
  margin: 0 0 4px;
  padding-bottom: 16px;
  border-bottom: 2px solid #DFE1E6;
}

.page-meta {
  font-size: 12px;
  color: #6B778C;
  margin-bottom: 24px;
}
.page-meta a { color: #0052CC; }

h1, h2, h3, h4, h5, h6 {
  font-weight: 600;
  color: #172B4D;
  margin: 28px 0 8px;
  line-height: 1.3;
}
h1 { font-size: 20px; }
h2 { font-size: 17px; border-bottom: 1px solid #EBECF0; padding-bottom: 6px; }
h3 { font-size: 15px; }
h4 { font-size: 13px; }
h5, h6 { font-size: 12px; }

p { margin: 8px 0; }

a { color: #0052CC; text-decoration: none; }
a:hover { text-decoration: underline; }

strong { font-weight: 600; }
em { font-style: italic; }
del { color: #6B778C; }

code {
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
  font-size: 12px;
  background: #F4F5F7;
  color: #172B4D;
  padding: 1px 4px;
  border-radius: 3px;
}

pre {
  background: #F4F5F7;
  border-radius: 4px;
  padding: 12px 16px;
  overflow-x: auto;
  margin: 12px 0;
}
pre code { background: none; padding: 0; font-size: 12px; }

.code-block { margin: 12px 0; }
.code-header {
  display: flex;
  gap: 8px;
  align-items: center;
  background: #DFE1E6;
  padding: 4px 12px;
  border-radius: 4px 4px 0 0;
  font-size: 11px;
}
.code-lang {
  font-family: monospace;
  color: #42526E;
  font-weight: 600;
}
.code-title { color: #6B778C; }
.code-block pre { border-radius: 0 0 4px 4px; margin: 0; }
.code-block .code-header + pre { border-radius: 0 4px 4px 4px; }

.raw-block {
  background: #FFFAE6;
  border-left: 3px solid #FFD700;
  border-radius: 0 4px 4px 0;
  color: #6B778C;
  font-size: 11px;
  margin: 8px 0;
}

blockquote {
  border-left: 3px solid #DFE1E6;
  margin: 8px 0;
  padding: 4px 16px;
  color: #505F79;
}

ul, ol { margin: 8px 0; padding-left: 24px; }
li { margin: 3px 0; }

table {
  border-collapse: collapse;
  width: 100%;
  margin: 12px 0;
  font-size: 13px;
}
th, td {
  border: 1px solid #DFE1E6;
  padding: 8px 12px;
  vertical-align: top;
  text-align: left;
}
th { background: #F4F5F7; font-weight: 600; }
tr:nth-child(even) td { background: #FAFBFC; }

hr { border: none; border-top: 1px solid #DFE1E6; margin: 24px 0; }

.jira-issue {
  display: inline-block;
  font-family: "SFMono-Regular", Consolas, monospace;
  font-size: 11px;
  background: #DEEBFF;
  color: #0747A6;
  padding: 1px 6px;
  border-radius: 3px;
  text-decoration: none;
  border: 1px solid #B3D4FF;
  vertical-align: middle;
  line-height: 1.6;
}
.jira-issue:hover { background: #B3D4FF; text-decoration: none; }

.status-badge {
  display: inline-block;
  font-size: 11px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 3px;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.confluence-page { color: #0052CC; }
.user-badge {
  display: inline-block;
  font-size: 11px;
  background: #EAE6FF;
  color: #403294;
  padding: 1px 6px;
  border-radius: 10px;
}
.image-placeholder {
  display: inline-block;
  font-size: 12px;
  background: #F4F5F7;
  color: #6B778C;
  border: 1px dashed #C1C7D0;
  padding: 2px 8px;
  border-radius: 3px;
}
.anchor { display: block; height: 0; visibility: hidden; }

.panel {
  border-radius: 4px;
  margin: 12px 0;
  overflow: hidden;
}
.panel-header {
  padding: 6px 12px;
  font-size: 13px;
}
.panel-body {
  padding: 4px 12px 8px;
}
.panel-body p:first-child { margin-top: 4px; }

details.expand-block {
  border: 1px solid #DFE1E6;
  border-radius: 4px;
  margin: 12px 0;
}
details.expand-block summary {
  cursor: pointer;
  padding: 8px 12px;
  background: #F4F5F7;
  font-weight: 500;
  user-select: none;
}
details.expand-block summary:hover { background: #EBECF0; }
.expand-content { padding: 8px 12px; }

.task-list { list-style: none; padding-left: 4px; margin: 8px 0; }
.task-item { margin: 4px 0; }
.task-item input[type="checkbox"] { margin-right: 6px; vertical-align: middle; }

.gcm-layout { display: flex; gap: 16px; margin: 12px 0; flex-wrap: wrap; }
.gcm-layout-section { display: flex; gap: 16px; flex: 1; flex-wrap: wrap; }
.gcm-layout-cell { flex: 1; min-width: 200px; }
.gcm-div {}
"""


def gcm_to_preview(gcm_text):
    """Convert GCM to a full displayable HTML page."""
    meta, body = parse_frontmatter(gcm_text)
    title = meta.get("title", "Preview")
    page_id = meta.get("page_id", "")
    version = meta.get("version", "")

    inner_html = _render_blocks(body.splitlines())

    meta_line = ""
    if page_id:
        conf_url = f"{CONFLUENCE_URL}/pages/viewpage.action?pageId={page_id}"
        meta_line = (
            f'<div class="page-meta">'
            f'Page ID: <a href="{conf_url}" target="_blank">{page_id}</a>'
            + (f' &nbsp;·&nbsp; Version {_esc(str(version))}' if version else '')
            + '</div>'
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_esc(title)}</title>
<style>{CSS}</style>
</head>
<body>
<div class="page-wrapper">
  <h1 class="page-title">{_esc(title)}</h1>
  {meta_line}
  <div class="page-content">{inner_html}</div>
</div>
</body>
</html>"""


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: gcm_preview.py <file.gcm>", file=sys.stderr)
        sys.exit(1)
    file_path = sys.argv[1]
    with open(file_path, encoding="utf-8") as f:
        gcm_text = f.read()
    print(gcm_to_preview(gcm_text))

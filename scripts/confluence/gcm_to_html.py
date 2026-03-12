"""
gcm_to_html.py — Convert GCM markup back to Confluence storage-format HTML.

Usage:
    from gcm_to_html import gcm_to_html
    storage_html = gcm_to_html(gcm_text, jira_server="", jira_server_id="")
"""

import re

from gcm_spec import parse_frontmatter, escape_xhtml, parse_tag_attrs


# ── Jira macro generation ───────────────────────────────────────────────────

def _jira_macro(key, server="", server_id="", extra_params=None):
    parts = []
    if server:
        parts.append(f'<ac:parameter ac:name="server">{escape_xhtml(server)}</ac:parameter>')
    if server_id:
        parts.append(f'<ac:parameter ac:name="serverId">{server_id}</ac:parameter>')
    parts.append(f'<ac:parameter ac:name="key">{escape_xhtml(key)}</ac:parameter>')
    for k, v in (extra_params or {}).items():
        parts.append(f'<ac:parameter ac:name="{escape_xhtml(k)}">{escape_xhtml(v)}</ac:parameter>')
    return f'<ac:structured-macro ac:name="jira" ac:schema-version="1">{"".join(parts)}</ac:structured-macro>'


# ── Inline conversion ───────────────────────────────────────────────────────

def _convert_inline(text, server="", server_id=""):
    """Convert GCM inline markup to XHTML. Returns an XHTML string."""
    # Use placeholders to protect already-converted spans from re-escaping
    phs = []

    def _ph(xhtml):
        idx = len(phs)
        phs.append(xhtml)
        return f"\x00PH{idx}\x00"

    # {jira:KEY} or {jira:KEY|param=value|...}
    def _parse_jira(m):
        key = m.group(1)
        extras_str = m.group(2) or ""
        extra_params = {}
        for part in extras_str.split("|"):
            if "=" in part:
                k, _, v = part.partition("=")
                extra_params[k.strip()] = v.strip()
        return _ph(_jira_macro(key, server, server_id, extra_params))
    text = re.sub(
        r'\{jira:([A-Z][A-Z0-9]*-\d+)((?:\|[^}]+)*)\}',
        _parse_jira,
        text
    )

    # {br} → <br/>
    text = re.sub(r'\{br\}', lambda m: _ph('<br/>'), text)

    # {raw}...{/raw} inline passthrough
    text = re.sub(r'\{raw\}(.*?)\{/raw\}', lambda m: _ph(m.group(1)), text)

    # {anchor:name}
    text = re.sub(
        r'\{anchor:([^}]+)\}',
        lambda m: _ph(f'<ac:structured-macro ac:name="anchor" ac:schema-version="1">'
                       f'<ac:parameter ac:name="">{escape_xhtml(m.group(1))}</ac:parameter>'
                       f'</ac:structured-macro>'),
        text
    )

    # {status:Title|color=X|subtle}
    def _status_repl(m):
        body = m.group(1)
        parts_list = body.split("|")
        title = parts_list[0] if parts_list else ""
        color = ""
        subtle = ""
        for p in parts_list[1:]:
            if p.startswith("color="):
                color = p[6:]
            elif p == "subtle":
                subtle = "true"
        params = []
        if title:
            params.append(f'<ac:parameter ac:name="title">{escape_xhtml(title)}</ac:parameter>')
        if color:
            params.append(f'<ac:parameter ac:name="colour">{escape_xhtml(color)}</ac:parameter>')
        if subtle:
            params.append(f'<ac:parameter ac:name="subtle">true</ac:parameter>')
        return _ph(f'<ac:structured-macro ac:name="status" ac:schema-version="1">{"".join(params)}</ac:structured-macro>')

    text = re.sub(r'\{status:([^}]+)\}', _status_repl, text)

    # {user:key}
    text = re.sub(
        r'\{user:([^}]+)\}',
        lambda m: _ph(f'<ac:link><ri:user ri:userkey="{escape_xhtml(m.group(1))}"/></ac:link>'),
        text
    )

    # {link page="Title"}text{/link}  or  {link anchor=name}text{/link}
    def _link_repl(m):
        attr_str = m.group(1)
        link_text = m.group(2)
        attrs = parse_tag_attrs(attr_str)
        if "anchor" in attrs:
            anchor = attrs["anchor"]
            return _ph(
                f'<ac:link ac:anchor="{escape_xhtml(anchor)}">'
                f'<ac:plain-text-link-body><![CDATA[{link_text}]]></ac:plain-text-link-body>'
                f'</ac:link>'
            )
        elif "page" in attrs:
            page = attrs["page"]
            return _ph(
                f'<ac:link>'
                f'<ri:page ri:content-title="{escape_xhtml(page)}"/>'
                f'<ac:plain-text-link-body><![CDATA[{link_text}]]></ac:plain-text-link-body>'
                f'</ac:link>'
            )
        return m.group(0)  # leave as-is if unknown

    text = re.sub(r'\{link ([^}]+)\}(.*?)\{/link\}', _link_repl, text)

    # {image file="x.png" height=400}
    def _image_repl(m):
        attr_str = m.group(1)
        attrs = parse_tag_attrs(attr_str)
        ac_attrs = []
        for k in ("height", "width", "align", "class", "thumbnail"):
            v = attrs.get(k, "")
            if v:
                ac_attrs.append(f'ac:{k}="{escape_xhtml(v)}"')
        ac_str = " ".join(ac_attrs)
        if ac_str:
            ac_str = " " + ac_str

        if "file" in attrs:
            inner = f'<ri:attachment ri:filename="{escape_xhtml(attrs["file"])}"/>'
        elif "url" in attrs:
            inner = f'<ri:url ri:value="{escape_xhtml(attrs["url"])}"/>'
        else:
            inner = ""
        return _ph(f'<ac:image{ac_str}>{inner}</ac:image>')

    text = re.sub(r'\{image ([^}]+)\}', _image_repl, text)

    # {sub}x{/sub}, {sup}x{/sup}, {u}x{/u}
    text = re.sub(r'\{sub\}(.*?)\{/sub\}', lambda m: _ph(f'<sub>{escape_xhtml(m.group(1))}</sub>'), text)
    text = re.sub(r'\{sup\}(.*?)\{/sup\}', lambda m: _ph(f'<sup>{escape_xhtml(m.group(1))}</sup>'), text)
    text = re.sub(r'\{u\}(.*?)\{/u\}', lambda m: _ph(f'<u>{escape_xhtml(m.group(1))}</u>'), text)

    # [text](url) → <a href>
    # Pattern allows brackets in link text (e.g. [[1]](url)) but prevents
    # matching across separate [...] groups (e.g. [1] ... [text](url))
    text = re.sub(
        r'\[([^\[\]]*(?:\[[^\]]*\][^\[\]]*)*)\]\(([^)]+)\)',
        lambda m: _ph(f'<a href="{escape_xhtml(m.group(2))}">{escape_xhtml(m.group(1))}</a>'),
        text
    )

    # Protect escaped asterisks from being treated as formatting
    ESC_STAR = "\x01STAR\x01"
    text = text.replace("\\*", ESC_STAR)

    # ***bold italic***
    text = re.sub(r'\*\*\*(.+?)\*\*\*',
                  lambda m: _ph(f'<strong><em>{escape_xhtml(m.group(1).replace(ESC_STAR, "*"))}</em></strong>'), text)
    # **bold**
    text = re.sub(r'\*\*(.+?)\*\*',
                  lambda m: _ph(f'<strong>{escape_xhtml(m.group(1).replace(ESC_STAR, "*"))}</strong>'), text)
    # *italic*
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)',
                  lambda m: _ph(f'<em>{escape_xhtml(m.group(1).replace(ESC_STAR, "*"))}</em>'), text)
    # ~~strikethrough~~
    text = re.sub(r'~~(.+?)~~',
                  lambda m: _ph(f'<del>{escape_xhtml(m.group(1))}</del>'), text)
    # `code`
    text = re.sub(r'`(.+?)`',
                  lambda m: _ph(f'<code>{escape_xhtml(m.group(1))}</code>'), text)

    # Escape remaining plain text
    parts = re.split(r'(\x00PH\d+\x00)', text)
    result = []
    for part in parts:
        if part.startswith("\x00PH"):
            result.append(part)
        else:
            result.append(escape_xhtml(part.replace(ESC_STAR, "*")))
    text = "".join(result)

    # Restore placeholders — iterate until all nested placeholders are resolved
    changed = True
    while changed:
        changed = False
        for i, xhtml in enumerate(phs):
            marker = f"\x00PH{i}\x00"
            if marker in text:
                text = text.replace(marker, xhtml)
                changed = True

    return text


# ── Block-level conversion ──────────────────────────────────────────────────

def gcm_to_html(gcm_text, jira_server="", jira_server_id=""):
    """Convert GCM markup to Confluence storage-format XHTML.
    
    Returns (storage_html, metadata_dict).
    """
    meta, body = parse_frontmatter(gcm_text)
    lines = body.splitlines()
    output = []
    i = 0

    server = jira_server
    server_id = jira_server_id

    # State
    paragraph_lines = []
    list_stack = []  # stack of 'ul'/'ol'
    in_blockquote = False
    bq_lines = []

    def flush_paragraph():
        if paragraph_lines:
            text = " ".join(paragraph_lines).strip()
            if text:
                output.append(f"<p>{_convert_inline(text, server, server_id)}</p>")
            paragraph_lines.clear()

    def flush_blockquote():
        nonlocal in_blockquote
        if bq_lines:
            inner = " ".join(bq_lines).strip()
            if inner:
                output.append(f"<blockquote><p>{_convert_inline(inner, server, server_id)}</p></blockquote>")
            bq_lines.clear()
        in_blockquote = False

    def close_lists():
        while list_stack:
            output.append(f"</{list_stack.pop()}>")

    while i < len(lines):
        line = lines[i]

        # ── {raw}...{/raw} — verbatim passthrough ──
        if line.strip() == "{raw}":
            flush_paragraph()
            flush_blockquote()
            close_lists()
            raw_lines = []
            i += 1
            while i < len(lines) and lines[i].strip() != "{/raw}":
                raw_lines.append(lines[i])
                i += 1
            output.append("\n".join(raw_lines))
            i += 1  # skip {/raw}
            continue

        # ── {table ...} ──
        if re.match(r'^\{table\b', line.strip()):
            flush_paragraph()
            flush_blockquote()
            close_lists()
            # Parse table attributes
            m = re.match(r'^\{table\s*(.*)\}$', line.strip())
            tbl_attr_str = m.group(1) if m else ""
            tbl_attrs = parse_tag_attrs(tbl_attr_str)
            html_attrs = []
            if "width" in tbl_attrs:
                html_attrs.append(f'style="width: {tbl_attrs["width"]};"')
            if "class" in tbl_attrs:
                html_attrs.append(f'class="{escape_xhtml(tbl_attrs["class"])}"')
            attr_html = " " + " ".join(html_attrs) if html_attrs else ""
            output.append(f"<table{attr_html}>")
            i += 1

            # Parse table contents until {/table}
            while i < len(lines) and lines[i].strip() != "{/table}":
                tl = lines[i].strip()

                if tl == "{thead}":
                    output.append("<thead>")
                elif tl == "{/thead}":
                    output.append("</thead>")
                elif tl == "{tfoot}":
                    output.append("<tfoot>")
                elif tl == "{/tfoot}":
                    output.append("</tfoot>")
                elif tl == "{tbody}":
                    output.append("<tbody>")
                elif tl == "{/tbody}":
                    output.append("</tbody>")
                elif tl == "{tr}":
                    output.append("<tr>")
                elif tl == "{/tr}":
                    output.append("</tr>")
                elif tl == "{colgroup}":
                    output.append("<colgroup>")
                elif tl == "{/colgroup}":
                    output.append("</colgroup>")
                elif re.match(r'^\{col\b', tl):
                    cm = re.match(r'^\{col\s*(.*)\}$', tl)
                    col_attrs = parse_tag_attrs(cm.group(1)) if cm else {}
                    col_html = []
                    for ck, cv in col_attrs.items():
                        col_html.append(f'{ck}="{escape_xhtml(cv)}"')
                    col_attr_html = " " + " ".join(col_html) if col_html else ""
                    output.append(f"<col{col_attr_html}/>")

                elif re.match(r'^\{(td|th)\b', tl):
                    # Cell: {td rowspan=3}content{/td} — may span multiple lines
                    cm = re.match(r'^\{(td|th)\s*([^}]*)\}(.*)$', tl)
                    if cm:
                        cell_tag = cm.group(1)
                        cell_attr_str = cm.group(2)
                        cell_rest = cm.group(3)

                        # Collect cell content (may span lines if {/td} not on same line)
                        close_pattern = f"{{/{cell_tag}}}"
                        if close_pattern in cell_rest:
                            cell_content = cell_rest[:cell_rest.index(close_pattern)]
                        else:
                            cell_parts = [cell_rest]
                            i += 1
                            while i < len(lines) and close_pattern not in lines[i]:
                                cell_parts.append(lines[i])
                                i += 1
                            if i < len(lines):
                                last = lines[i]
                                cell_parts.append(last[:last.index(close_pattern)])
                            cell_content = "\n".join(cell_parts)

                        # Build cell HTML
                        cell_attrs = parse_tag_attrs(cell_attr_str)
                        ca_parts = []
                        for ck, cv in cell_attrs.items():
                            ca_parts.append(f'{ck}="{escape_xhtml(cv)}"')
                        ca_html = " " + " ".join(ca_parts) if ca_parts else ""

                        # Convert cell content — handle headings, {ul}/{ol} lists, and paragraphs
                        cell_lines = cell_content.strip().split("\n")
                        cell_parts = []
                        cur_list = None  # None, 'ul', or 'ol'
                        in_list_block = False  # inside {ul}...{/ul} or {ol}...{/ol}
                        para_buf = []

                        def flush_cell_para():
                            if para_buf:
                                ptxt = "</p><p>".join(para_buf)
                                cell_parts.append(f"<p>{ptxt}</p>")
                                para_buf.clear()

                        for cl in cell_lines:
                            stripped = cl.strip()
                            if not stripped:
                                if not in_list_block:
                                    flush_cell_para()
                                continue

                            # List block markers
                            if stripped in ("{ul}", "{ol}"):
                                flush_cell_para()
                                list_type = stripped[1:-1]  # 'ul' or 'ol'
                                cell_parts.append(f"<{list_type}>")
                                cur_list = list_type
                                in_list_block = True
                                continue
                            if stripped in ("{/ul}", "{/ol}"):
                                list_type = stripped[2:-1]
                                cell_parts.append(f"</{list_type}>")
                                cur_list = None
                                in_list_block = False
                                continue

                            # List item inside {ul}/{ol} block
                            if in_list_block:
                                lm = re.match(r'^[-*+]\s+(.+)', stripped)
                                if lm:
                                    ltxt = _convert_inline(lm.group(1), server, server_id)
                                    cell_parts.append(f"<li>{ltxt}</li>")
                                    continue

                            # Heading inside cell
                            hm = re.match(r'^(={1,6})\s+(.+)$', stripped)
                            if hm:
                                flush_cell_para()
                                hlev = len(hm.group(1))
                                htxt = _convert_inline(hm.group(2).strip(), server, server_id)
                                cell_parts.append(f"<h{hlev}>{htxt}</h{hlev}>")
                                continue

                            # Regular paragraph text
                            para_buf.append(_convert_inline(stripped, server, server_id))

                        flush_cell_para()
                        cell_html = "".join(cell_parts)

                        output.append(f"<{cell_tag}{ca_html}>{cell_html}</{cell_tag}>")

                i += 1

            # Close table
            output.append("</table>")
            i += 1  # skip {/table}
            continue

        # ── Heading ──
        m = re.match(r'^(={1,6})\s+(.*)$', line)
        if m:
            flush_paragraph()
            flush_blockquote()
            close_lists()
            level = len(m.group(1))
            htext = m.group(2).strip()
            text = _convert_inline(htext, server, server_id) if htext else ""
            output.append(f"<h{level}>{text}</h{level}>")
            i += 1
            continue

        # ── Horizontal rule ──
        if re.match(r'^-{4,}\s*$', line):
            flush_paragraph()
            flush_blockquote()
            close_lists()
            output.append("<hr/>")
            i += 1
            continue

        # ── Blockquote ──
        if line.startswith("> "):
            flush_paragraph()
            close_lists()
            in_blockquote = True
            bq_lines.append(line[2:].strip())
            i += 1
            continue
        elif in_blockquote:
            flush_blockquote()

        # ── Escaped list-like pattern (paragraph text starting with - or 1.) ──
        if re.match(r'^\\(-\s|\d+\.\s)', line):
            close_lists()
            paragraph_lines.append(line[1:])  # unescape, treat as paragraph
            i += 1
            continue

        # ── Unordered list (only '-' to avoid ambiguity with italic *) ──
        m = re.match(r'^(\s*)-\s+(.+)', line)
        if m:
            flush_paragraph()
            flush_blockquote()
            indent = len(m.group(1)) // 2
            text = _convert_inline(m.group(2), server, server_id)
            while len(list_stack) > indent + 1:
                output.append(f"</{list_stack.pop()}>")
            if len(list_stack) <= indent:
                output.append("<ul>")
                list_stack.append("ul")
            output.append(f"<li><p>{text}</p></li>")
            i += 1
            continue

        # ── Ordered list ──
        m = re.match(r'^(\s*)\d+\.\s+(.+)', line)
        if m:
            flush_paragraph()
            flush_blockquote()
            indent = len(m.group(1)) // 2
            text = _convert_inline(m.group(2), server, server_id)
            while len(list_stack) > indent + 1:
                output.append(f"</{list_stack.pop()}>")
            if len(list_stack) <= indent:
                output.append("<ol>")
                list_stack.append("ol")
            output.append(f"<li><p>{text}</p></li>")
            i += 1
            continue

        # ── Blank line ──
        if not line.strip():
            flush_paragraph()
            flush_blockquote()
            close_lists()
            i += 1
            continue

        # ── Regular paragraph text ──
        close_lists()
        paragraph_lines.append(line.strip())
        i += 1

    flush_paragraph()
    flush_blockquote()
    close_lists()

    return "\n".join(output), meta

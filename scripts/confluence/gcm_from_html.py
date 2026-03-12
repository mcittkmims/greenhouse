"""
gcm_from_html.py — Convert Confluence storage-format HTML to GCM markup.

Usage:
    from gcm_from_html import html_to_gcm
    gcm_text = html_to_gcm(storage_html)
"""

import re
from html.parser import HTMLParser

from gcm_spec import escape_inline, escape_xhtml


# ── Tag classification ──────────────────────────────────────────────────────

# Tags whose content we render natively as GCM
_BLOCK_TAGS = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote",
               "ul", "ol", "li", "hr", "br", "div", "pre"}

_TABLE_STRUCT = {"table", "thead", "tbody", "tfoot", "tr", "td", "th",
                 "colgroup", "col", "caption"}

_INLINE_TAGS = {"strong", "b", "em", "i", "del", "s", "code",
                "sub", "sup", "span", "u"}

# Confluence namespace tags with dedicated GCM syntax
_AC_DEDICATED = {"jira", "anchor", "status"}

# ac:* tags whose open/close just passes text through (no structural meaning)
_AC_TRANSPARENT = {"ac:inline-comment-marker", "ac:plain-text-link-body",
                   "ac:rich-text-body", "ac:task-body"}

# Tags to silently skip (and their content)
_SKIP_TAGS = {"style", "script"}


# ── Parser ──────────────────────────────────────────────────────────────────

class _GCMBuilder(HTMLParser):
    """SAX-style HTML→GCM converter."""

    def __init__(self):
        super().__init__()
        self.out = []            # output line fragments
        self._skip = 0           # depth inside skip tags

        # Raw capture: verbatim Confluence XML for unknown constructs
        self._raw_depth = 0
        self._raw_buf = []

        # Table state
        self._in_table = False
        self._table_attrs = {}
        self._table_section = ""  # "thead" | "tbody" | ""
        self._cell_tag = ""       # "td" or "th"
        self._cell_buf = []       # collects inline content inside a cell
        self._cell_attrs = {}

        # Inline state
        self._list_depth = 0
        self._heading = 0
        self._heading_buf = []
        self._in_blockquote = False
        self._in_link = False
        self._link_href = ""
        self._link_text = []
        self._in_pre = False

        # ac:structured-macro state
        self._macro_name = ""
        self._macro_id = ""
        self._macro_params = {}
        self._in_macro_param = None   # None = not inside a param; "" = inside unnamed param
        self._macro_depth = 0
        self._macro_raw_buf = []

        # ac:link state
        self._in_ac_link = False
        self._ac_link_depth = 0
        self._ac_link_buf = []
        self._ac_link_attrs = {}
        self._ac_link_text = []

        # ac:image state
        self._in_ac_image = False
        self._ac_image_depth = 0
        self._ac_image_buf = []
        self._ac_image_attrs = {}
        self._ac_image_file = ""
        self._ac_image_url = ""

        # ac:task-list state
        self._in_task_list = False
        self._task_depth = 0
        self._task_buf = []

        # Inline formatting stack (for cells): tracks open inline markers
        # Each entry is the GCM close-marker string, e.g. "**", "*", "~~", "`"
        self._inline_stack = []

        # Inline formatting depth (prevent doubled markers for nested <strong><strong>)
        self._strong_depth = 0
        self._em_depth = 0

    # ── Helpers ──────────────────────────────────────────────────────────

    def _close_inline_markers(self):
        """Close any open inline formatting markers (reverse order) and clear stack."""
        for marker in reversed(self._inline_stack):
            self._cell_buf.append(marker)
        self._inline_stack.clear()

    def _emit(self, text):
        """Add text to current output context.  Inner contexts (links) take
        priority over outer containers (cell, heading)."""
        if self._in_link:
            self._link_text.append(text)
        elif self._in_ac_link:
            self._ac_link_text.append(text)
        elif self._cell_tag:
            self._cell_buf.append(text)
        elif self._heading:
            self._heading_buf.append(text)
        else:
            self.out.append(text)

    def _attrs_str(self, attrs_list):
        """Convert [(k,v), ...] to 'k="v" k2="v2"' XML attribute string."""
        parts = []
        for k, v in attrs_list:
            v_esc = (v or "").replace("&", "&amp;").replace("<", "&lt;"
                        ).replace(">", "&gt;").replace('"', "&quot;")
            parts.append(f'{k}="{v_esc}"')
        return " ".join(parts)

    def _gcm_tag_attrs(self, keep_attrs, attrs_list):
        """Build GCM tag attribute string from HTML attrs, keeping only listed keys."""
        parts = []
        for k, v in attrs_list:
            if k in keep_attrs and v:
                if " " in v or '"' in v or "=" in v:
                    v_esc = v.replace('"', '\\"')
                    parts.append(f'{k}="{v_esc}"')
                else:
                    parts.append(f"{k}={v}")
        return " ".join(parts)

    # ── Raw capture helpers ──────────────────────────────────────────────

    def _raw_open(self, tag, attrs_list):
        a = self._attrs_str(attrs_list)
        self._raw_buf.append(f"<{tag}{' ' + a if a else ''}>")
        self._raw_depth += 1

    def _raw_selfclose(self, tag, attrs_list):
        a = self._attrs_str(attrs_list)
        self._raw_buf.append(f"<{tag}{' ' + a if a else ''}/>")

    def _raw_close(self, tag):
        self._raw_buf.append(f"</{tag}>")
        self._raw_depth -= 1
        if self._raw_depth == 0:
            raw = "".join(self._raw_buf)
            self._raw_buf = []
            self._emit(f"\n{{raw}}\n{raw}\n{{/raw}}\n")

    def _raw_data(self, data):
        self._raw_buf.append(escape_xhtml(data))

    # ── Macro helpers ────────────────────────────────────────────────────

    def _macro_open(self, tag, attrs_list):
        a = self._attrs_str(attrs_list)
        self._macro_raw_buf.append(f"<{tag}{' ' + a if a else ''}>")
        self._macro_depth += 1

    def _macro_selfclose(self, tag, attrs_list):
        a = self._attrs_str(attrs_list)
        self._macro_raw_buf.append(f"<{tag}{' ' + a if a else ''}/>")

    def _macro_close(self, tag):
        self._macro_raw_buf.append(f"</{tag}>")
        self._macro_depth -= 1

    def _macro_data(self, data):
        self._macro_raw_buf.append(escape_xhtml(data))

    def _flush_macro(self):
        """Emit the completed macro as GCM."""
        name = self._macro_name
        params = self._macro_params

        if name == "jira":
            key = params.get("key", "UNKNOWN-0")
            # Preserve all params except server/serverId (re-added from config at push time)
            extras = "".join(
                f"|{k}={v}"
                for k, v in params.items()
                if k not in ("key", "server", "serverId") and v
            )
            self._emit(f"{{jira:{key}{extras}}}")
        elif name == "anchor":
            aname = params.get("", params.get("name", ""))
            # anchor macro: the default (unnamed) parameter is the anchor name
            if not aname:
                # try first param
                for v in params.values():
                    if v:
                        aname = v
                        break
            self._emit(f"{{anchor:{aname}}}")
        elif name == "status":
            title = params.get("title", "")
            color = params.get("colour", params.get("color", ""))
            subtle = params.get("subtle", "")
            extra = ""
            if color:
                extra += f"|color={color}"
            if subtle and subtle.lower() == "true":
                extra += "|subtle"
            self._emit(f"{{status:{title}{extra}}}")
        else:
            # Unknown macro → raw passthrough of full XML
            raw = "".join(self._macro_raw_buf)
            self._emit(f"\n{{raw}}\n{raw}\n{{/raw}}\n")

        self._macro_name = ""
        self._macro_id = ""
        self._macro_params = {}
        self._in_macro_param = None
        self._macro_depth = 0
        self._macro_raw_buf = []

    # ── ac:link helpers ──────────────────────────────────────────────────

    def _flush_ac_link(self):
        attrs = self._ac_link_attrs
        text = "".join(self._ac_link_text).strip()
        raw_buf = list(self._ac_link_buf)   # save before reset

        anchor = attrs.get("ac:anchor", "")
        page_title = attrs.get("ri:content-title", "")

        # Reset state BEFORE emitting so _emit routes correctly
        self._in_ac_link = False
        self._ac_link_depth = 0
        self._ac_link_buf = []
        self._ac_link_attrs = {}
        self._ac_link_text = []

        if anchor:
            attr_str = f"anchor={anchor}"
            if not text:
                text = anchor
            self._emit(f"{{link {attr_str}}}{text}{{/link}}")
        elif page_title:
            if " " in page_title or '"' in page_title:
                pt_esc = page_title.replace('"', '\\"')
                attr_str = f'page="{pt_esc}"'
            else:
                attr_str = f"page={page_title}"
            if not text:
                text = page_title
            self._emit(f"{{link {attr_str}}}{text}{{/link}}")
        elif attrs.get("ri:userkey"):
            # ac:link wrapping ri:user → {user:key}
            self._emit(f"{{user:{attrs['ri:userkey']}}}")
        else:
            # Fallback: raw passthrough of the full ac:link XML
            raw = "".join(raw_buf)
            self._emit(f"\n{{raw}}\n{raw}\n{{/raw}}\n")

    # ── ac:image helpers ─────────────────────────────────────────────────

    def _flush_ac_image(self):
        attrs = self._ac_image_attrs
        file = self._ac_image_file
        url = self._ac_image_url
        parts = []
        if file:
            parts.append(f'file="{file}"')
        elif url:
            parts.append(f'url="{url}"')
        for k in ("ac:height", "ac:width", "ac:align", "ac:class", "ac:thumbnail"):
            v = attrs.get(k, "")
            if v:
                short = k.split(":")[-1]  # height, width, etc.
                parts.append(f"{short}={v}")
        self._emit("{image " + " ".join(parts) + "}")

        self._in_ac_image = False
        self._ac_image_depth = 0
        self._ac_image_buf = []
        self._ac_image_attrs = {}
        self._ac_image_file = ""
        self._ac_image_url = ""

    # ── Tag handlers ─────────────────────────────────────────────────────

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs_dict = dict(attrs)

        # ── Inside raw capture ──
        if self._raw_depth > 0:
            self._raw_open(tag, attrs)
            return

        # ── Inside macro capture ──
        if self._macro_depth > 0:
            self._macro_open(tag, attrs)
            # Capture inner ri:* and ac:parameter data
            if tag == "ac:parameter":
                self._in_macro_param = attrs_dict.get("ac:name", "")
            return

        # ── Inside ac:link capture ──
        if self._in_ac_link:
            a = self._attrs_str(attrs)
            self._ac_link_buf.append(f"<{tag}{' ' + a if a else ''}>")
            self._ac_link_depth += 1
            # Capture ri:page attrs
            if tag == "ri:page":
                for k, v in attrs:
                    self._ac_link_attrs[k] = v
            # Capture ri:user inside ac:link
            elif tag == "ri:user":
                userkey = attrs_dict.get("ri:userkey", "")
                if userkey:
                    self._ac_link_attrs["ri:userkey"] = userkey
            return

        # ── Inside ac:image capture ──
        if self._in_ac_image:
            a = self._attrs_str(attrs)
            self._ac_image_buf.append(f"<{tag}{' ' + a if a else ''}>")
            self._ac_image_depth += 1
            if tag == "ri:attachment":
                self._ac_image_file = attrs_dict.get("ri:filename", "")
            elif tag == "ri:url":
                self._ac_image_url = attrs_dict.get("ri:value", "")
            return

        # ── Inside task-list capture ──
        if self._in_task_list:
            a = self._attrs_str(attrs)
            self._task_buf.append(f"<{tag}{' ' + a if a else ''}>")
            self._task_depth += 1
            return

        # ── Skip tags ──
        if tag in _SKIP_TAGS:
            self._skip += 1
            return
        if self._skip:
            return

        # ── Confluence structured macros ──
        if tag == "ac:structured-macro":
            self._macro_name = attrs_dict.get("ac:name", "")
            self._macro_id = attrs_dict.get("ac:macro-id", "")
            self._macro_params = {}
            self._in_macro_param = None
            self._macro_depth = 1
            self._macro_raw_buf = [f"<{tag}{' ' + self._attrs_str(attrs) if attrs else ''}>"]
            return

        # ── ac:link ──
        if tag == "ac:link":
            self._in_ac_link = True
            self._ac_link_depth = 1
            self._ac_link_buf = [f"<ac:link{' ' + self._attrs_str(attrs) if attrs else ''}>"]
            self._ac_link_attrs = dict(attrs)
            self._ac_link_text = []
            return

        # ── ac:image ──
        if tag == "ac:image":
            self._in_ac_image = True
            self._ac_image_depth = 1
            self._ac_image_buf = [f"<ac:image{' ' + self._attrs_str(attrs) if attrs else ''}>"]
            self._ac_image_attrs = dict(attrs)
            self._ac_image_file = ""
            self._ac_image_url = ""
            return

        # ── ac:task-list ──
        if tag == "ac:task-list":
            self._in_task_list = True
            self._task_depth = 1
            self._task_buf = [f"<ac:task-list{' ' + self._attrs_str(attrs) if attrs else ''}>"]
            return

        # ── Any other ac:* → raw capture ──
        if tag.startswith("ac:") and tag not in _AC_TRANSPARENT:
            self._raw_open(tag, attrs)
            return

        # ── <a> links ──
        if tag == "a":
            self._in_link = True
            self._link_href = attrs_dict.get("href", "")
            self._link_text = []
            return

        # ── Table structure ──
        if tag == "table":
            self._in_table = True
            table_a = self._gcm_tag_attrs({"class", "style"}, attrs)
            # translate style width
            style = attrs_dict.get("style", "")
            wm = re.search(r'width:\s*([\d.]+%)', style)
            width_attr = f" width={wm.group(1)}" if wm else ""
            cls = attrs_dict.get("class", "")
            cls_attr = f' class="{cls}"' if cls else ""
            self._emit(f"\n{{table{width_attr}{cls_attr}}}\n")
            return

        if tag == "thead":
            self._table_section = "thead"
            self._emit("{thead}\n")
            return
        if tag == "tbody":
            self._table_section = "tbody"
            return
        if tag == "tfoot":
            self._table_section = "tfoot"
            self._emit("{tfoot}\n")
            return
        if tag == "tr":
            self._emit("{tr}\n")
            return

        if tag in ("td", "th"):
            self._cell_tag = tag
            self._cell_buf = []
            self._cell_attrs = dict(attrs)
            self._inline_stack.clear()
            return

        if tag == "colgroup":
            self._emit("{colgroup}\n")
            return
        if tag == "col":
            col_a = self._gcm_tag_attrs({"style", "class"}, attrs)
            self._emit(f"{{col {col_a}}}\n")
            return
        if tag == "caption":
            # Swallow caption open; text flows into output naturally
            return

        # ── Block elements ──
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag[1])
            if self._cell_tag:
                # Heading inside a cell — emit marker directly into cell buf
                self._cell_buf.append(f"\n{'=' * level} ")
            else:
                self._heading = level
                self._heading_buf = []
            return

        if tag == "p":
            if not self._cell_tag:
                if self._list_depth > 0:
                    pass  # <p> inside <li> — <li> already emits newline+marker
                elif self._in_blockquote:
                    self._emit("\n> ")
                else:
                    self._emit("\n")
            return

        if tag == "blockquote":
            self._in_blockquote = True
            return

        if tag in ("ul", "ol"):
            if self._cell_tag:
                self._close_inline_markers()
                list_tag = "ul" if tag == "ul" else "ol"
                self._cell_buf.append(f"\n{{{list_tag}}}\n")
            self._list_depth += 1
            return

        if tag == "li":
            indent = "  " * (self._list_depth - 1)
            self._emit(f"\n{indent}- ")
            return

        if tag == "hr":
            self._emit("\n----\n")
            return

        if tag == "br":
            if self._cell_tag:
                self._close_inline_markers()
                self._cell_buf.append("\n")
            else:
                self._emit("{br}")
            return

        if tag == "pre":
            self._in_pre = True
            return

        # ── Inline formatting ──
        if tag in ("strong", "b"):
            self._strong_depth += 1
            if self._strong_depth == 1:
                self._emit("**")
                if self._cell_tag:
                    self._inline_stack.append("**")
            return
        if tag in ("em", "i"):
            self._em_depth += 1
            if self._em_depth == 1:
                self._emit("*")
                if self._cell_tag:
                    self._inline_stack.append("*")
            return
        if tag in ("del", "s"):
            self._emit("~~")
            if self._cell_tag:
                self._inline_stack.append("~~")
            return
        if tag == "code":
            self._emit("`")
            if self._cell_tag:
                self._inline_stack.append("`")
            return
        if tag == "sub":
            self._emit("{sub}")
            return
        if tag == "sup":
            self._emit("{sup}")
            return
        if tag == "u":
            self._emit("{u}")
            return

        # ── div / span — transparent or skip ──
        if tag == "div":
            return
        if tag == "span":
            return

        # ── ri:user (self-closing handled below but also appears with closing tag) ──
        if tag == "ri:user":
            key = attrs_dict.get("ri:userkey", "")
            self._emit(f"{{user:{key}}}")
            return

        # ── Fallback: unknown tag → raw ──
        if tag.startswith("ri:") or tag.startswith("ac:"):
            # Should already be handled above; safety fallback
            self._raw_open(tag, attrs)
            return

        # Normal HTML tag we don't care about — swallow open tag

    def handle_endtag(self, tag):
        tag = tag.lower()

        # ── Raw capture ──
        if self._raw_depth > 0:
            self._raw_close(tag)
            return

        # ── Macro capture ──
        if self._macro_depth > 0:
            self._macro_close(tag)
            if tag == "ac:parameter":
                self._in_macro_param = None
            if self._macro_depth == 0:
                self._flush_macro()
            return

        # ── ac:link capture ──
        if self._in_ac_link:
            self._ac_link_buf.append(f"</{tag}>")
            self._ac_link_depth -= 1
            if self._ac_link_depth == 0:
                self._flush_ac_link()
            return

        # ── ac:image capture ──
        if self._in_ac_image:
            self._ac_image_buf.append(f"</{tag}>")
            self._ac_image_depth -= 1
            if self._ac_image_depth == 0:
                self._flush_ac_image()
            return

        # ── task-list capture ──
        if self._in_task_list:
            self._task_buf.append(f"</{tag}>")
            self._task_depth -= 1
            if self._task_depth == 0:
                raw = "".join(self._task_buf)
                self._emit(f"\n{{raw}}\n{raw}\n{{/raw}}\n")
                self._in_task_list = False
                self._task_buf = []
            return

        # ── Skip tags ──
        if tag in _SKIP_TAGS:
            self._skip = max(0, self._skip - 1)
            return
        if self._skip:
            return

        # ── ac:* transparent ──
        if tag.lower() in _AC_TRANSPARENT or tag.lower().startswith("ac:"):
            return

        # ── </a> ──
        if tag == "a" and self._in_link:
            text = "".join(self._link_text).strip()
            href = self._link_href
            # Reset link state BEFORE emitting so _emit routes correctly
            self._in_link = False
            self._link_href = ""
            self._link_text = []
            if href and text:
                self._emit(f"[{text}]({href})")
            elif text:
                self._emit(text)
            return

        # ── Table structure ──
        if tag == "table":
            self._emit("{/table}\n")
            self._in_table = False
            return
        if tag == "thead":
            self._emit("{/thead}\n")
            self._table_section = ""
            return
        if tag == "tbody":
            self._table_section = ""
            return
        if tag == "tfoot":
            self._emit("{/tfoot}\n")
            self._table_section = ""
            return
        if tag == "tr":
            self._emit("{/tr}\n")
            return
        if tag in ("td", "th"):
            content = "".join(self._cell_buf).strip()
            # Normalize internal newlines (from <br>) to keep single-line if simple
            cell_a = self._cell_attrs
            attr_parts = []
            for k in ("rowspan", "colspan", "style", "scope"):
                v = cell_a.get(k, "")
                if v and not (k == "rowspan" and v == "1") and not (k == "colspan" and v == "1"):
                    if " " in v:
                        attr_parts.append(f'{k}="{v}"')
                    else:
                        attr_parts.append(f"{k}={v}")
            attr_str = " " + " ".join(attr_parts) if attr_parts else ""
            # Reset cell state BEFORE emitting so _emit routes to out, not cell_buf
            self._cell_tag = ""
            self._cell_buf = []
            self._cell_attrs = {}
            self._inline_stack.clear()
            self._emit(f"{{{tag}{attr_str}}}{content}{{/{tag}}}\n")
            return
        if tag == "colgroup":
            self._emit("{/colgroup}\n")
            return
        if tag == "col":
            return
        if tag == "caption":
            return

        # ── Block elements ──
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            if self._cell_tag:
                # Heading inside cell — marker was added at open, text went to cell_buf
                self._heading = 0
                self._heading_buf = []
            else:
                level = self._heading
                text = "".join(self._heading_buf).strip()
                # Reset state BEFORE emitting so _emit routes to out, not heading_buf
                self._heading = 0
                self._heading_buf = []
                self._emit(f"\n{'=' * level} {text}\n")
            return

        if tag == "p":
            if self._cell_tag:
                self._close_inline_markers()
                self._cell_buf.append("\n")
            elif self._list_depth > 0:
                pass  # </p> inside <li> — <li> already handles structure
            else:
                self._emit("\n")
            return

        if tag == "blockquote":
            self._in_blockquote = False
            self._emit("\n")
            return

        if tag in ("ul", "ol"):
            self._list_depth = max(0, self._list_depth - 1)
            if self._cell_tag and self._list_depth == 0:
                list_tag = "ul" if tag == "ul" else "ol"
                self._cell_buf.append(f"\n{{/{list_tag}}}\n")
            elif self._list_depth == 0:
                self._emit("\n")
            return
        if tag == "li":
            return

        if tag == "pre":
            self._in_pre = False
            return

        # ── Inline ──
        if tag in ("strong", "b"):
            self._strong_depth = max(0, self._strong_depth - 1)
            if self._strong_depth == 0:
                if self._cell_tag and "**" in self._inline_stack:
                    self._inline_stack.remove("**")
                elif self._cell_tag:
                    return  # already force-closed by line break
                self._emit("**")
            return
        if tag in ("em", "i"):
            self._em_depth = max(0, self._em_depth - 1)
            if self._em_depth == 0:
                if self._cell_tag and "*" in self._inline_stack:
                    self._inline_stack.remove("*")
                elif self._cell_tag:
                    return  # already force-closed by line break
                self._emit("*")
            return
        if tag in ("del", "s"):
            if self._cell_tag and "~~" in self._inline_stack:
                self._inline_stack.remove("~~")
            elif self._cell_tag:
                return
            self._emit("~~")
            return
        if tag == "code":
            if self._cell_tag and "`" in self._inline_stack:
                self._inline_stack.remove("`")
            elif self._cell_tag:
                return
            self._emit("`")
            return
        if tag == "sub":
            self._emit("{/sub}")
            return
        if tag == "sup":
            self._emit("{/sup}")
            return
        if tag == "u":
            self._emit("{/u}")
            return

        # div, span, etc. — swallow

    def handle_startendtag(self, tag, attrs):
        """Self-closing tags like <br/>, <hr/>, <ri:attachment ... />."""
        tag = tag.lower()
        attrs_dict = dict(attrs)

        if self._raw_depth > 0:
            self._raw_selfclose(tag, attrs)
            return
        if self._macro_depth > 0:
            self._macro_selfclose(tag, attrs)
            return
        if self._in_ac_link:
            a = self._attrs_str(attrs)
            self._ac_link_buf.append(f"<{tag}{' ' + a if a else ''}/>")
            # Capture ri:page attributes
            if tag == "ri:page":
                for k, v in attrs:
                    self._ac_link_attrs[k] = v
            # Capture ri:user inside ac:link
            elif tag == "ri:user":
                userkey = attrs_dict.get("ri:userkey", "")
                if userkey:
                    self._ac_link_attrs["ri:userkey"] = userkey
            return
        if self._in_ac_image:
            a = self._attrs_str(attrs)
            self._ac_image_buf.append(f"<{tag}{' ' + a if a else ''}/>")
            if tag == "ri:attachment":
                self._ac_image_file = attrs_dict.get("ri:filename", "")
            elif tag == "ri:url":
                self._ac_image_url = attrs_dict.get("ri:value", "")
            return
        if self._in_task_list:
            a = self._attrs_str(attrs)
            self._task_buf.append(f"<{tag}{' ' + a if a else ''}/>")
            return

        # Self-closing ac:structured-macro (e.g. toc, children-display)
        if tag == "ac:structured-macro":
            a = self._attrs_str(attrs)
            macro_xml = f"<{tag}{' ' + a if a else ''}/>"
            if self._heading:
                # Keep macro inside heading as inline {raw}
                self._heading_buf.append(f"{{raw}}{macro_xml}{{/raw}}")
            else:
                self._emit(f"\n{{raw}}\n{macro_xml}\n{{/raw}}\n")
            return

        if tag == "br":
            if self._cell_tag:
                self._close_inline_markers()
                self._cell_buf.append("\n")
            else:
                self._emit("{br}")
            return
        if tag == "hr":
            self._emit("\n----\n")
            return
        if tag == "col":
            col_a = self._gcm_tag_attrs({"style", "class"}, attrs)
            self._emit(f"{{col {col_a}}}\n")
            return
        if tag == "ri:user":
            key = attrs_dict.get("ri:userkey", "")
            self._emit(f"{{user:{key}}}")
            return

        # Other self-closing ac:*/ri:* — swallow (emoticons, etc.)
        # They'll be inside a macro/link capture context normally

    def handle_data(self, data):
        if self._skip:
            return
        if self._raw_depth > 0:
            self._raw_data(data)
            return
        if self._macro_depth > 0:
            if self._in_macro_param is not None:
                self._macro_params[self._in_macro_param] = (
                    self._macro_params.get(self._in_macro_param, "") + data)
            self._macro_data(data)
            return
        if self._in_ac_link:
            self._ac_link_text.append(data)
            self._ac_link_buf.append(escape_xhtml(data))
            return
        if self._in_ac_image:
            self._ac_image_buf.append(escape_xhtml(data))
            return
        if self._in_task_list:
            self._task_buf.append(escape_xhtml(data))
            return
        # Normalize newlines in flowing text — HTML source newlines should not
        # become structural line breaks in GCM (would create false list items).
        # Only normalize when in flowing context (not in pre, raw, macro, etc.)
        if not self._in_pre and not self._cell_tag:
            data = data.replace("\n", " ")
        # Escape literal asterisks in text content to prevent confusion with
        # GCM bold/italic markers when adjacent to ** or * formatting.
        if not self._in_pre and not self._cell_tag:
            data = data.replace("*", "\\*")
        # Escape list-like patterns in non-list paragraph text to prevent
        # gcm_to_html from interpreting them as list items.
        if (self._list_depth == 0 and not self._cell_tag and not self._heading
                and self.out and self.out[-1].endswith('\n')
                and (re.match(r'^-\s', data) or re.match(r'^\d+\.\s', data))):
            data = '\\' + data
        self._emit(data)

    def handle_entityref(self, name):
        """Handle &name; entities."""
        entity_map = {"amp": "&", "lt": "<", "gt": ">",
                      "quot": '"', "nbsp": " ", "apos": "'"}
        char = entity_map.get(name, f"&{name};")
        if self._raw_depth > 0:
            self._raw_buf.append(f"&{name};")
        elif self._macro_depth > 0:
            self._macro_raw_buf.append(f"&{name};")
            if self._in_macro_param is not None:
                self._macro_params[self._in_macro_param] = (
                    self._macro_params.get(self._in_macro_param, "") + char)
        elif self._in_ac_link:
            self._ac_link_buf.append(f"&{name};")
            self._ac_link_text.append(char)
        elif self._in_ac_image:
            self._ac_image_buf.append(f"&{name};")
        elif self._in_task_list:
            self._task_buf.append(f"&{name};")
        else:
            self._emit(char)

    def handle_charref(self, name):
        """Handle &#nn; or &#xNN; entities."""
        if name.startswith('x'):
            char = chr(int(name[1:], 16))
        else:
            char = chr(int(name))
        if self._raw_depth > 0:
            self._raw_buf.append(f"&#{name};")
        elif self._macro_depth > 0:
            self._macro_raw_buf.append(f"&#{name};")
        elif self._in_ac_link:
            self._ac_link_buf.append(f"&#{name};")
        elif self._in_task_list:
            self._task_buf.append(f"&#{name};")
        else:
            self._emit(char)

    def get_gcm(self):
        text = "".join(self.out)
        # Normalize excessive blank lines
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()


# ── Public API ───────────────────────────────────────────────────────────────

def html_to_gcm(html, title="", page_id="", version="", source_url=""):
    """Convert Confluence storage HTML to GCM markup text.
    
    If title/page_id/version are given, a front-matter block is prepended.
    """
    parser = _GCMBuilder()
    parser.feed(html)
    body = parser.get_gcm()

    if title or page_id or version:
        from gcm_spec import format_frontmatter
        fm = format_frontmatter(title, page_id, version, source_url)
        return fm + "\n\n" + body + "\n"
    return body + "\n"

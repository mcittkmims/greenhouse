# GCM — GMS Confluence Markup

## Complete Reference Documentation

---

## 1. Overview

GCM (GMS Confluence Markup) is a custom, human-readable, line-oriented markup format designed for **lossless round-tripping** of Confluence storage-format HTML. It serves as the local representation of Confluence pages in the GMS (Greenhouse Management System) project.

### Purpose

- **Edit Confluence pages locally** using any text editor
- **Version-control documentation** in Git alongside code
- **Preserve every structural detail** of Confluence pages — headings, tables, macros, images, links, formatting — through round-trip conversion
- **Human-readable**: common elements look natural; exotic elements use tag-style syntax

### File Extension

`.gcm`

### Architecture

```
Confluence Storage HTML ──► gcm_from_html.py ──► .gcm file
                                                    │
                                                    ▼
                                              (edit locally)
                                                    │
                                                    ▼
.gcm file ──► gcm_to_html.py ──► Confluence Storage HTML ──► Confluence API
```

| Module | Purpose |
| --- | --- |
| `gcm_from_html.py` | Confluence storage HTML → GCM conversion |
| `gcm_to_html.py` | GCM → Confluence storage HTML conversion |
| `gcm_spec.py` | Shared constants, attribute parsing, escaping utilities |

### Design Principles

1. **One-to-one mapping** — every Confluence construct maps to exactly one GCM construct, and vice versa
2. **Lossless round-trip** — `HTML → GCM → HTML` produces semantically identical output (validated against 202 pages with 100% acceptance)
3. **Human-editable** — headings, paragraphs, bold, links, Jira issues look natural
4. **Diff-friendly** — line-oriented, deterministic formatting, no trailing whitespace
5. **`{raw}` safety net** — anything unrecognized (code blocks, layout sections, expand macros, info/note/warning/tip panels, and any unknown Confluence macro) is captured verbatim

---

## 2. Document Envelope

### Front-Matter

Every `.gcm` file begins with a YAML-ish front-matter block:

```
--- gcm ---
title: 04 - GMS - WP4.3 Import Stakeholder requirements in Jira
page_id: 42634112
version: 65
source: http://confluence.microlab.club/pages/viewpage.action?pageId=42634112
---
```

| Field | Type | Description |
| --- | --- | --- |
| `title` | string | Page title (as stored in Confluence) |
| `page_id` | string | Confluence page ID (numeric) |
| `version` | string | Confluence page version number |
| `source` | string | (Optional) Source URL for reference |

The body content follows after a blank line.

### Parsing

```python
from gcm_spec import parse_frontmatter

metadata, body = parse_frontmatter(gcm_text)
# metadata = {"title": "...", "page_id": "42634112", "version": "65"}
# body = "remaining text..."
```

---

## 3. Block Elements

### 3.1 Headings

Headings use `=` prefix markers. The number of `=` signs determines the level (1–6):

```
= Heading 1
== Heading 2
=== Heading 3
==== Heading 4
===== Heading 5
====== Heading 6
```

**Rules:**
- One space required between `=` markers and heading text
- Empty headings are allowed: `== ` (renders as `<h2></h2>`)
- Headings may contain inline formatting: `== **Bold Heading**`
- Headings may contain inline `{raw}...{/raw}` for macros embedded in headings (e.g., anchors, self-closing TOC macros)

**HTML mapping:**

| GCM | HTML |
| --- | --- |
| `= Title` | `<h1>Title</h1>` |
| `== Section` | `<h2>Section</h2>` |
| `=== Sub` | `<h3>Sub</h3>` |

### 3.2 Paragraphs

Plain text lines form paragraphs. A blank line separates paragraphs:

```
This is the first paragraph with some text.

This is a second paragraph.
```

**HTML mapping:** Each paragraph → `<p>text</p>`

### 3.3 Horizontal Rule

Four or more dashes on a line by themselves:

```
----
```

**HTML mapping:** `<hr/>`

### 3.4 Blockquotes

Lines prefixed with `> `:

```
> This is a quoted paragraph.
> This continues the same quote.
```

**HTML mapping:** `<blockquote><p>text</p></blockquote>`

### 3.5 Lists

#### Unordered Lists

Use `-` prefix (GCM only recognizes `-` as the unordered list marker at the block level, not `*` or `+`, to avoid ambiguity with italic markers):

```
- First item
- Second item
  - Nested item (2-space indent per level)
    - Deeply nested
```

**HTML mapping:**
```html
<ul>
  <li><p>First item</p></li>
  <li><p>Second item</p></li>
</ul>
```

#### Ordered Lists

Use `N.` prefix:

```
1. First item
2. Second item
  1. Nested ordered item
```

**HTML mapping:**
```html
<ol>
  <li><p>First item</p></li>
  <li><p>Second item</p></li>
</ol>
```

**Nesting:** 2-space indent per level. Unordered and ordered lists can be mixed.

**Escaping:** If paragraph text naturally starts with `- ` or `1. `, it's escaped with a leading backslash to prevent false list detection:

```
\- This is not a list item, just text starting with a dash
\1. This is not a list item either
```

### 3.6 Tables

Tables use tag-style syntax with full support for merged cells, headers, footers, and column groups:

```
{table width=54.0761%}
{colgroup}
{col style="width: 50.0%"}
{col style="width: 50.0%"}
{/colgroup}
{thead}
{tr}
{th}Header 1{/th}
{th}Header 2{/th}
{/tr}
{/thead}
{tr}
{td}Normal cell{/td}
{td}Normal cell{/td}
{/tr}
{tr}
{td rowspan=3}Spans 3 rows{/td}
{td colspan=2}Spans 2 columns{/td}
{/tr}
{/table}
```

#### Table Tags

| Tag | Description | Supported Attributes |
| --- | --- | --- |
| `{table ...}...{/table}` | Table container | `width`, `class` |
| `{thead}...{/thead}` | Table header section | — |
| `{tbody}...{/tbody}` | Table body section (optional; never emitted by converter, but parsed if present) | — |
| `{tfoot}...{/tfoot}` | Table footer section | — |
| `{colgroup}...{/colgroup}` | Column group | — |
| `{col ...}` | Column definition (self-closing) | `style`, `class` |
| `{tr}...{/tr}` | Table row | — |
| `{td ...}content{/td}` | Table cell | `rowspan`, `colspan`, `style`, `scope` |
| `{th ...}content{/th}` | Table header cell | `rowspan`, `colspan`, `style`, `scope` |

#### Cell Content

Cell content supports inline formatting (bold, italic, links, etc.) and can span multiple lines using literal newlines within the cell:

```
{td}**Bold text** and *italic*{/td}
{td}Line one
Line two
Line three{/td}
```

Multi-line cells use literal newlines. Each line within a cell becomes a `<br/>`-separated block or a `<p>` tag, depending on original structure.

#### Headings Inside Cells

Standard GCM heading markers can appear inside cells:

```
{td}=== Cell Heading
Some paragraph text{/td}
```

#### Lists Inside Cells

Lists inside cells are explicitly wrapped with `{ul}...{/ul}` or `{ol}...{/ol}` markers to prevent ambiguity with paragraph text starting with `-`:

```
{td}{ul}
- First item
- Second item
{/ul}{/td}
```

```
{td}{ol}
1. First
2. Second
{/ol}{/td}
```

#### Raw Passthrough Inside Cells

`{raw}...{/raw}` blocks are supported inside cell content for verbatim Confluence XML.

### 3.7 Aligned Paragraphs

Paragraphs with a text-align style use the `{p align=X}` tag:

```
{p align=center}This text is centered.{/p}

{p align=right}This text is right-aligned.{/p}
```

**Supported alignment values:** `left`, `center`, `right`, `justify`

**HTML mapping:** `<p style="text-align: center;">text</p>`

**Note:** This construct is generated from HTML whenever a `<p>` element carries a `text-align` style. It can also be written manually in GCM.

---

## 4. Inline Elements

### 4.1 Bold / Italic / Bold-Italic

```
**bold text**
*italic text*
***bold and italic***
```

**HTML mapping:**

| GCM | HTML |
| --- | --- |
| `**text**` | `<strong>text</strong>` |
| `*text*` | `<em>text</em>` |
| `***text***` | `<strong><em>text</em></strong>` |

**Depth tracking:** Nested `<strong><strong>...</strong></strong>` in HTML produces a single `**...**` in GCM (inner nesting is suppressed). Adjacent `</strong><strong>` produces `****` which may be collapsed during post-processing.

**Literal asterisks:** Literal `*` characters in text are escaped as `\*` to prevent confusion with formatting markers.

### 4.2 Strikethrough

```
~~deleted text~~
```

**HTML mapping:** `<del>deleted text</del>`

### 4.3 Inline Code

```
`code here`
```

**HTML mapping:** `<code>code here</code>`

### 4.4 Underline

```
{u}underlined text{/u}
```

**HTML mapping:** `<u>underlined text</u>`

### 4.5 Links

#### External Links

```
[display text](http://example.com)
```

**HTML mapping:** `<a href="http://example.com">display text</a>`

**Note:** Link text may contain brackets for bibliography references like `[1]`:
```
[See reference [1]](http://example.com)
```

#### Confluence Internal Page Links

```
{link page="WP1.1 Problem Definition"}display text{/link}
```

**HTML mapping:** `<ac:link><ri:page ri:content-title="WP1.1 Problem Definition"/><ac:plain-text-link-body>display text</ac:plain-text-link-body></ac:link>`

#### Confluence Anchor Links

```
{link anchor=ref4}display text{/link}
```

#### Confluence User Links

User mentions inside ac:link structures are handled as `{user:...}` (see below).

### 4.6 Images

#### Attached Images

```
{image file="diagram.png" height=400 align=center}
```

**Supported attributes:** `file`, `height`, `width`, `align`, `class`, `thumbnail`

**HTML mapping:** `<ac:image ...><ri:attachment ri:filename="diagram.png"/></ac:image>`

#### External URL Images

```
{image url="https://example.com/img.png" height=150}
```

**HTML mapping:** `<ac:image ...><ri:url ri:value="https://example.com/img.png"/></ac:image>`

### 4.7 Jira Issue

```
{jira:GMS-10}
{jira:GMS-10|showSummary=false}
{jira:GMS-10|showSummary=false|columns=key,summary,status}
```

This is the most common inline element in the GMS project. The key is always the first segment. Any additional Jira macro parameters (e.g. `showSummary`, `columns`, `maximumIssues`, `jqlQuery`) are preserved as `|name=value` pairs after the key.

`server` and `serverId` are **not** stored in GCM — they are re-added at push time from the `jira` config in `confluence_pages.json`.

Can appear both inline (within paragraphs, table cells) and as a standalone block.

### 4.8 Status Badge

```
{status:Draft|color=Yellow}
{status:Approved|color=Green|subtle}
```

**Parameters:**
- Title (first segment, before `|`)
- `color=` — badge color (`Red`, `Yellow`, `Green`, `Blue`, `Grey`)
- `subtle` — flag for subtle (outlined) style

**HTML mapping:** `<ac:structured-macro ac:name="status">` with `<ac:parameter>` children

### 4.9 Anchor

```
{anchor:ref4}
```

Creates a named anchor point for cross-referencing.

**HTML mapping:** `<ac:structured-macro ac:name="anchor"><ac:parameter ac:name="">ref4</ac:parameter></ac:structured-macro>`

### 4.10 User Mention

```
{user:ff8081819b134c58019c0a81410c0005}
```

References a Confluence user by their userkey.

**HTML mapping:** `<ri:user ri:userkey="ff8081819b134c58019c0a81410c0005"/>`

### 4.11 Subscript / Superscript

```
H{sub}2{/sub}O
x{sup}2{/sup}
```

**HTML mapping:** `<sub>2</sub>` / `<sup>2</sup>`

### 4.12 Inline Line Break

```
{br}
```

Represents `<br/>` within flowing text (outside table cells). Inside table cells, line breaks are represented as literal newlines in the cell content.

### 4.13 Inline Raw Passthrough

```
{raw}<ac:structured-macro ac:name="toc"/>{/raw}
```

For macros or other Confluence XML that appears inline within text (e.g., inside a heading). The content is passed through without modification.

---

## 5. Raw Passthrough Blocks

### Block-Level Raw

```
{raw}
<ac:structured-macro ac:name="children" ac:schema-version="2">
  <ac:parameter ac:name="all">true</ac:parameter>
</ac:structured-macro>
{/raw}
```

Used for any Confluence construct that doesn't have a dedicated GCM representation. The XML content is preserved verbatim — never parsed, never modified. It is pushed back byte-for-byte to Confluence.

### Raw-Wrapped Elements

All Confluence structured macros that do not have a dedicated GCM syntax are captured as `{raw}...{/raw}` blocks by the HTML→GCM converter. This includes:

| Confluence Element | Description |
| --- | --- |
| `ac:task-list` | Task lists with checkboxes |
| `code` macro | Syntax-highlighted code blocks |
| `expand` macro | Collapsible expand/collapse sections |
| `info` / `note` / `warning` / `tip` macros | Styled info panels |
| `layout` / `layout-section` / `layout-cell` | Multi-column layout sections |
| `children` macro | Displays child pages |
| `pagetree` macro | Page tree navigation |
| `toc` macro | Table of contents |
| `excerpt` macro | Page excerpt |
| Any other plugin macro | Any unrecognized `ac:structured-macro` |

**Note:** `<div>` and `<span>` elements in Confluence HTML are transparent in GCM — their content flows through without any special markers and their attributes are discarded.

---

## 6. Escaping

GCM uses backslash escaping for characters that have special meaning in the format:

| Escape | Literal Character | Context |
| --- | --- | --- |
| `\*` | `*` | Prevents interpretation as bold/italic marker |
| `\{` | `{` | Prevents interpretation as tag opener |
| `\}` | `}` | Prevents interpretation as tag closer |
| `\[` | `[` | Prevents interpretation as link opener |
| `\]` | `]` | Prevents interpretation as link closer |
| `\~` | `~` | Prevents interpretation as strikethrough marker |
| `` \` `` | `` ` `` | Prevents interpretation as code marker |
| `\\` | `\` | Literal backslash |

### Automatic Escaping

The converter automatically escapes:

1. **Literal asterisks** in text content → `\*` (prevents confusion with bold/italic markers)
2. **List-like paragraph starts** → `\- ` or `\1. ` (when paragraph text happens to start with what looks like a list marker but is not actually a list)

---

## 7. Attribute Syntax

Tag attributes use `key=value` or `key="value with spaces"` syntax:

```
{table width=54.0761% class=my-table}
{td rowspan=3 style="background-color: #f0f0f0"}
{image file="photo.jpg" height=400 align=center}
```

### Rules

- Unquoted values: no spaces allowed (`key=value`)
- Quoted values: double quotes (`key="value"`) or single quotes (`key='value'`)
- Multiple attributes separated by spaces
- Boolean-like attributes: `key=true` (not standalone keywords)

### Parsing API

```python
from gcm_spec import parse_tag_attrs, format_tag_attrs

attrs = parse_tag_attrs('width=50% class="my class"')
# {"width": "50%", "class": "my class"}

text = format_tag_attrs({"width": "50%", "class": "my class"})
# 'width=50% class="my class"'
```

---

## 8. Conversion API

### HTML → GCM

```python
from gcm_from_html import html_to_gcm

gcm_text = html_to_gcm(
    html,                    # Confluence storage-format HTML string
    title="Page Title",      # Optional: included in front-matter
    page_id="42634112",      # Optional: included in front-matter
    version="65",            # Optional: included in front-matter
    source_url=""            # Optional: source URL
)
```

### GCM → HTML

```python
from gcm_to_html import gcm_to_html

storage_html, metadata = gcm_to_html(
    gcm_text,                # GCM markup string (with or without front-matter)
    jira_server="",          # Jira server name (for {jira:KEY} expansion — from confluence_pages.json)
    jira_server_id=""        # Jira server ID (for {jira:KEY} expansion — from confluence_pages.json)
)
# storage_html: Confluence storage-format XHTML string
# metadata: dict from front-matter (title, page_id, version, etc.)
```

---

## 9. Sync and Push Workflow

### Syncing from Confluence

```bash
python3 scripts/confluence/confluence_sync.py --up-to 5.4
```

Fetches pages via REST API, converts HTML → GCM, writes `.gcm` files to `documentation/confluence/cloud/`.

**Options:**
- `--up-to X.Y` — fetch pages up to work package limit
- `--dry-run` — preview without writing
- `--force` — re-fetch even if cached version matches

### Pushing to Confluence

```bash
python3 scripts/confluence/confluence_push.py --file WP4.2_Analyze_Stakeholder_Requirements.gcm
```

Converts GCM → HTML, pushes via REST API with conflict detection.

**Options:**
- `--dry-run` — preview converted XHTML without pushing
- `--no-confirm` — skip confirmation prompt

### Version and Hash Cache

The sync system maintains version + hash caches in `documentation/confluence/cloud/.cache/` to enable:

- **Incremental sync** — only fetches pages that changed on the server
- **Conflict detection** — warns if local file was edited since last sync
- **Push safety** — prevents overwriting concurrent server changes

---

## 10. Special Handling Notes

### Adjacent Bold/Italic Tags

Confluence WYSIWYG editors often produce redundant adjacent tags like:

```html
<strong>Part 1</strong><strong>Part 2</strong>
```

GCM represents this as `**Part 1****Part 2**` where `****` is the close-open boundary. On round-trip, this produces a single `<strong>Part 1Part 2</strong>` which is semantically identical. The tag count may differ, but the visual rendering is the same.

### Nested Inline Formatting with Depth Tracking

HTML may contain nested identical tags: `<strong><strong>text</strong></strong>`. GCM tracks depth and only emits one pair of `**` markers, producing `**text**` — semantically equivalent.

### `<span>` and `<div>` Transparency

`<span>` and `<div>` elements are treated as transparent containers — their content flows through without any GCM markers. Style attributes are not preserved (they're typically Confluence editor artifacts). `<div>` does not have a GCM equivalent.

### Newline Normalization

Source HTML newlines within flowing text are normalized to spaces. This prevents HTML source formatting (which has no semantic meaning) from creating false paragraph or list boundaries in GCM.

### Table Cell Inline Formatting

When inline formatting (bold, italic, etc.) spans a line break within a table cell, GCM automatically closes the formatting markers before the newline and (in the HTML direction) the formatting context is re-established on the next line. This prevents cross-line formatting issues.

### `{tbody}` is Optional

The `{tbody}` tag is recognized and correctly converted to `<tbody>` by `gcm_to_html.py`, but `gcm_from_html.py` never emits it (Confluence HTML's implicit tbody is discarded). Manually adding `{tbody}...{/tbody}` to a GCM file is valid and will round-trip correctly.

### Unknown Macros → Raw

Any `ac:structured-macro` whose `ac:name` is not `jira`, `anchor`, or `status` is captured verbatim as a `{raw}...{/raw}` block. Self-closing macros (`<ac:structured-macro ... />`) that appear inside a heading become inline `{raw}...{/raw}`. This ensures 100% lossless round-tripping regardless of which Confluence plugins are in use.

---

## 11. Complete Example

### GCM Source

```
--- gcm ---
title: Example GCM Page
page_id: 12345678
version: 3
---

= Project Overview

This project implements an IoT-based **greenhouse management system** for the
Technical University of Moldova.

== Key Features

- Real-time temperature monitoring with {jira:GMS-10}
- Automated irrigation control
- Cloud-based data analytics dashboard

== Status

{status:In Progress|color=Yellow}

== Requirements Traceability

{table width=100%}
{thead}
{tr}
{th}Requirement{/th}
{th}Status{/th}
{th}Jira Issue{/th}
{/tr}
{/thead}
{tr}
{td}Temperature monitoring{/td}
{td}{status:Approved|color=Green}{/td}
{td}{jira:GMS-10}{/td}
{/tr}
{tr}
{td}Humidity sensor integration{/td}
{td}{status:Draft|color=Yellow}{/td}
{td}{jira:GMS-15}{/td}
{/tr}
{/table}

== Architecture Diagram

{image file="system-architecture.png" height=500 align=center}

== References

{anchor:ref1}

[1] FAO, *The future of food and agriculture*, Rome: FAO, 2017.
[See full report](https://www.fao.org/publications/card/en/c/I6583E)

----

*Last updated: 2025*
```

### Conversion Result (HTML)

The above GCM, when converted with `gcm_to_html()`, produces valid Confluence storage-format XHTML with proper `<h1>`, `<h2>`, `<ul><li>`, `<table>`, `<ac:structured-macro>` (for Jira, status, anchor), `<ac:image>`, and `<a href>` elements — ready for direct upload via the Confluence REST API.

---

## 12. File Organization

```
scripts/confluence/
├── gcm_from_html.py    # HTML → GCM converter (~952 lines)
├── gcm_to_html.py      # GCM → HTML converter (~490 lines)
├── gcm_spec.py         # Shared utilities (~115 lines)
├── GCM_SPEC.md         # Quick-reference specification
├── confluence_sync.py  # Sync: Confluence → local .gcm files
└── confluence_push.py  # Push: local .gcm → Confluence

documentation/confluence/
├── confluence_pages.json   # Page ID map + configuration
├── cloud/                  # Auto-synced .gcm files
├── wip/                    # Files being actively edited
└── resources/              # Learning materials (Markdown, not synced)
```

---

## 13. Validation

The GCM round-trip conversion has been validated against **202 Confluence pages** from the PBL26 space (across all projects: GMS, AFB, AGC, CDR, PDD, SPM) with a **100% acceptance ratio**:

- **Exact match**: structural elements (headings, tables, rows, cells, lists, macros, links, images) preserved with identical counts
- **Tolerated cosmetic differences**: paragraph `<p>` count (structural wrapping differences), `<br/>` normalization, and strong/em count changes from adjacent tag collapse (semantically equivalent)
- **Zero errors**: no conversion failures across all 202 pages

Test infrastructure:
- Full server test: `/tmp/test_gcm_comprehensive.py` (fetches all pages live)
- Cached test: `/tmp/test_cached.py` (49 cached pages, no network needed)

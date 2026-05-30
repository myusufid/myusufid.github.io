#!/usr/bin/env python3
"""Build standalone HTML pages for cpns/materi notes.

Run: python3 build.py    (from cpns/)

Reads body fragments from cpns/materi-content/, injects them into
cpns/materi/template.html, and writes full standalone pages to cpns/materi/
mirroring the source directory tree. Also generates cpns/materi/index.html
as a listing page.
"""

import html as html_lib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONTENT = HERE / "materi-content"
OUT = HERE / "materi"
TEMPLATE = OUT / "template.html"

GROUPS = {
    "": "Pengantar",
    "02-pancasila": "Pancasila",
    "03-uud-1945": "UUD 1945",
    "04-twk": "CPNS TWK",
    "05-tiu": "TIU",
    "pembahasan": "Pembahasan",
}
GROUP_ORDER = ["", "02-pancasila", "03-uud-1945", "04-twk", "05-tiu", "pembahasan"]

H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.DOTALL | re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]+>")
TABLE_RE = re.compile(r"(<table[\s>].*?</table>)", re.DOTALL | re.IGNORECASE)


def wrap_tables(html: str) -> str:
    return TABLE_RE.sub(r'<div class="table-wrap">\1</div>', html)


WS_RE = re.compile(r"\s+")


def to_plain_text(html: str) -> str:
    """Strip tags, decode entities, collapse whitespace."""
    text = TAG_RE.sub(" ", html)
    text = html_lib.unescape(text)
    text = WS_RE.sub(" ", text).strip()
    return text


def extract_title(html: str, fallback: str) -> str:
    m = H1_RE.search(html)
    if not m:
        return fallback
    return TAG_RE.sub("", m.group(1)).strip()


def collect():
    """Return list of dicts: {src, out_rel, group_key, title}, sorted."""
    items = []
    for src in sorted(CONTENT.rglob("*.html")):
        rel = src.relative_to(CONTENT)
        group_key = rel.parent.as_posix() if rel.parent != Path(".") else ""
        if group_key not in GROUPS:
            print(f"WARN: unknown group '{group_key}' for {rel}", file=sys.stderr)
            continue
        html = src.read_text(encoding="utf-8")
        title = extract_title(html, rel.stem)
        items.append(
            {
                "src": src,
                "rel": rel,
                "out": OUT / rel,
                "group_key": group_key,
                "title": title,
                "url": "/cpns/materi/" + rel.as_posix(),
            }
        )
    items.sort(key=lambda x: (GROUP_ORDER.index(x["group_key"]), x["rel"].name))
    return items


def build_sidebar(items) -> str:
    html_parts = [
        '<a href="/cpns/materi/index.html" class="sidebar-link">📚 Daftar Materi</a>'
    ]
    by_group = {}
    for it in items:
        by_group.setdefault(it["group_key"], []).append(it)
    for key in GROUP_ORDER:
        if key not in by_group:
            continue
        html_parts.append(f'<div class="group-label">{GROUPS[key]}</div>')
        for it in by_group[key]:
            html_parts.append(
                f'<a href="{it["url"]}" class="sidebar-link">{it["title"]}</a>'
            )
    return "\n".join(html_parts)


def render(template: str, title: str, sidebar: str, content: str) -> str:
    out = template.replace("<!-- TITLE -->", title)
    out = out.replace("<!-- SIDEBAR -->", sidebar)
    out = out.replace("<!-- CONTENT -->", content)
    return out


def build_listing(items, sidebar: str, template: str) -> str:
    by_group = {}
    for it in items:
        by_group.setdefault(it["group_key"], []).append(it)

    body = ['<h1>Daftar Materi CPNS</h1>',
            '<p>Catatan belajar untuk TWK, TIU, dan pembahasan soal.</p>']
    for key in GROUP_ORDER:
        if key not in by_group:
            continue
        body.append(f"<h2>{GROUPS[key]}</h2>")
        body.append("<ul>")
        for it in by_group[key]:
            body.append(f'<li><a href="{it["url"]}">{it["title"]}</a></li>')
        body.append("</ul>")
    return render(template, "Daftar Materi", sidebar, "\n".join(body))


def main():
    if not TEMPLATE.exists():
        print(f"Missing {TEMPLATE}", file=sys.stderr)
        sys.exit(1)
    if not CONTENT.exists():
        print(f"Missing {CONTENT}", file=sys.stderr)
        sys.exit(1)

    template = TEMPLATE.read_text(encoding="utf-8")
    items = collect()
    sidebar = build_sidebar(items)

    for it in items:
        body = it["src"].read_text(encoding="utf-8")
        body = wrap_tables(body)
        page = render(template, it["title"], sidebar, body)
        it["out"].parent.mkdir(parents=True, exist_ok=True)
        it["out"].write_text(page, encoding="utf-8")
        print(f"  {it['rel']} → {it['out'].relative_to(OUT)}")

    listing = build_listing(items, sidebar, template)
    (OUT / "index.html").write_text(listing, encoding="utf-8")
    print("  → index.html")

    index_entries = []
    for it in items:
        raw = it["src"].read_text(encoding="utf-8")
        index_entries.append(
            {
                "title": it["title"],
                "url": it["url"],
                "group": GROUPS[it["group_key"]],
                "content": to_plain_text(raw)[:8000],
            }
        )
    (OUT / "search-index.json").write_text(
        json.dumps(index_entries, ensure_ascii=False), encoding="utf-8"
    )
    print("  → search-index.json")

    print(f"\nBuilt {len(items)} pages + index + search.")


if __name__ == "__main__":
    main()

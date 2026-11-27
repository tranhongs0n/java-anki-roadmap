# -*- coding: utf-8 -*-
"""Effective Java 3e -> per-item briefs (TOC driven, one brief per Item)."""
import json, os, re, sys
import pymupdf

PDF = r"C:\Users\OF1VNHAN\Downloads\Effective Java (2017, Addison-Wesley).pdf"
OUT = os.path.dirname(os.path.abspath(__file__))
HEADER = re.compile(r"^\s*(ITEM \d+:|[A-Z][A-Z &,\-]{8,})\s*$")
FOLIO = re.compile(r"^\s*\d{1,3}\s*$")


def items(doc):
    toc = [(lvl, t, pg) for lvl, t, pg in doc.get_toc()]
    out = []
    for i, (lvl, title, pg) in enumerate(toc):
        if not lvl == 2 or not title.startswith("Item "):
            continue
        nxt = next((p for l2, t2, p in toc[i + 1:] if l2 == 2 and t2.startswith("Item ")), doc.page_count)
        n = int(re.match(r"Item (\d+)", title).group(1))
        out.append({"n": n, "title": title.split(": ", 1)[1], "start": pg, "end": nxt - 1})
    return out


def text_of(doc, start, end):
    lines = []
    for i in range(start - 1, min(end, doc.page_count)):
        for ln in doc[i].get_text("text").splitlines():
            t = re.sub(r"\s+", " ", ln).strip()
            if not t or FOLIO.match(t) or HEADER.match(t):
                continue
            lines.append(t)
    return " ".join(lines)


def main(nums=None):
    doc = pymupdf.open(PDF)
    all_items = items(doc)
    json.dump(all_items, open(os.path.join(OUT, "items.json"), "w", encoding="utf-8"), indent=1)
    for it in all_items:
        if nums and it["n"] not in nums:
            continue
        body = text_of(doc, it["start"], it["end"])
        path = os.path.join(OUT, f"item{it['n']:02d}.md")
        open(path, "w", encoding="utf-8").write(f"# Item {it['n']}: {it['title']}\n\npages {it['start']}-{it['end']}\n\n{body}")
        print(f"item {it['n']:>2} p{it['start']}-{it['end']} {len(body):>6}c  {it['title'][:60]}")


if __name__ == "__main__":
    main([int(x) for x in sys.argv[1:]] or None)

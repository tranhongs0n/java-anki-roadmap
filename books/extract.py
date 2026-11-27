# -*- coding: utf-8 -*-
"""Extract Head First Java chapters into reviewable briefs.

Drops the page furniture (running head, folio), the exercise pages (Code Magnets,
Pool Puzzle, Be the Compiler, crosswords, Who Am I) and the arrow labels that
describe a diagram, keeping prose paragraphs, headings and code blocks.
"""
import json, os, re, sys
import pymupdf

PDF = r"C:\Users\OF1VNHAN\Downloads\Head First Java.pdf"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hfj3e")
FURNITURE = re.compile(r"^(you are here.*|chapter \d+|dive in.*|[ivx]+|\d{1,3})$", re.I)
EXERCISE = re.compile(r"(sharpen your pencil|code magnets|pool puzzle|be the compiler|mixed messages|"
                      r"who am i|crossword|magnets|exercise|fireside chat|there are no dumb questions|"
                      r"bullet points|make it stick|watch it!|test drive|your job)", re.I)
HEADING_MIN_SIZE = 15.0


def clean_line(t):
    t = t.replace("\u0017", "").strip()
    return re.sub(r"\s+", " ", t)


def chapter_blocks(doc, start, end):
    out = []
    for pno in range(start, end + 1):
        page = doc[pno - 1]
        for blk in page.get_text("dict")["blocks"]:
            lines = []
            for ln in blk.get("lines", []):
                spans = [s for s in ln["spans"] if s["text"].strip()]
                if not spans:
                    continue
                txt = clean_line("".join(s["text"] for s in spans))
                if not txt or FURNITURE.match(txt):
                    continue
                mono = all(re.search(r"(courier|consol|mono)", s["font"], re.I) for s in spans)
                size = max(s["size"] for s in spans)
                lines.append({"t": txt, "mono": mono, "size": size})
            if lines:
                out.append({"page": pno, "lines": lines})
    return out


def to_brief(blocks, toc_titles=()):
    """Merge lines into paragraphs / code runs, dropping diagram labels and exercises."""
    items, buf, code = [], [], []
    toc_norm = {re.sub(r"[^a-z0-9 ]", "", t.lower()).strip(): (t, pg) for t, pg in toc_titles}
    for b in blocks:
        mode = "code" if sum(1 for l in b["lines"] if l["mono"]) > len(b["lines"]) * 0.6 else "prose"
        text = " ".join(l["t"] for l in b["lines"])
        if mode == "prose" and EXERCISE.search(text[:120]) and len(b["lines"]) < 6:
            continue
        if mode == "code":
            code.extend(l["t"] for l in b["lines"] if l["mono"])
            continue
        if code:
            items.append(("code", code)); code = []
        for l in b["lines"]:
            probe = re.sub(r"[^a-z0-9 ]", "", l["t"].lower()).strip()
            if probe in toc_norm and len(l["t"]) < 90:
                canon, page = toc_norm[probe]
                l["t"] = f"{canon}\u200b{page}"
                if buf: items.append(("p", " ".join(buf))); buf = []
                items.append(("h", l["t"]))
            elif len(l["t"]) >= 90:
                buf.append(l["t"])
            elif buf:
                buf.append(l["t"])
        if buf and len(" ".join(buf)) > 400:
            items.append(("p", " ".join(buf))); buf = []
    if code: items.append(("code", code))
    if buf: items.append(("p", " ".join(buf)))
    return items


def main(only=None):
    doc = pymupdf.open(PDF)
    toc = [(t, pg) for lvl, t, pg in doc.get_toc() if lvl == 1]
    chapters = []
    for i, (title, start) in enumerate(toc):
        end = toc[i + 1][1] - 1 if i + 1 < len(toc) else doc.page_count
        m = re.match(r"Chapter (\d+)", title)
        if not m:
            continue
        n = int(m.group(1))
        if only and n not in only:
            continue
        chapters.append((n, title, start, end))
    os.makedirs(OUT, exist_ok=True)
    stats = []
    for n, title, start, end in chapters:
        titles = [(t, pg) for lvl, t, pg in doc.get_toc() if lvl == 2 and start <= pg <= end]
        items = to_brief(chapter_blocks(doc, start, end), titles)
        text = []
        seen_heading = None
        for kind, val in items:
            if kind == "h":
                h_title, page = val.rsplit("\u200b", 1)
                h_title = h_title.strip()
                if h_title.lower() == seen_heading:
                    continue
                seen_heading = h_title.lower()
                text.append(f"\n## {h_title} <!--p{page}-->")
            elif kind == "p":
                text.append(f"\n{val}")
            else:
                text.append("\n```java\n" + "\n".join(val) + "\n```")
        body = "\n".join(text)
        open(os.path.join(OUT, f"ch{n:02d}_brief.md"), "w", encoding="utf-8").write(
            f"# Chapter {n}: {title}\n\npages {start}-{end}\n" + body)
        stats.append((n, title, end - start + 1, body.count("\n## "), len(body),
                      sum(1 for k, _ in items if k == "code")))
        print(f"ch{n:02d} p{start}-{end} ({end-start+1}p) headings={stats[-1][3]:>2} brief={len(body):>6}c codeblocks={stats[-1][5]}")
    json.dump([{"ch": s[0], "title": s[1], "pages": s[2], "headings": s[3], "chars": s[4], "codeblocks": s[5]} for s in stats],
              open(os.path.join(OUT, "chapters.json"), "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main([int(x) for x in sys.argv[1:]] or None)

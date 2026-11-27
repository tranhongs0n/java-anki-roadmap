# -*- coding: utf-8 -*-
"""Thinking in Java 4e -> per-chapter briefs (printed page + 22 = pdf page)."""
import json, os, re, sys
import pymupdf

PDF = r"C:\Users\OF1VNHAN\Downloads\Thinking_in_Java_4th_Edition.pdf"
OUT = os.path.dirname(os.path.abspath(__file__))
OFFSET = 22
CHAPTERS = [
 ("1","Introduction to Objects",15,41),("2","Everything Is an Object",41,63),
 ("3","Operators",63,93),("4","Controlling Execution",93,107),
 ("5","Initialization & Cleanup",107,145),("6","Access Control",145,165),
 ("7","Reusing Classes",165,193),("8","Polymorphism",193,219),
 ("9","Interfaces",219,243),("10","Inner Classes",243,275),
 ("11","Holding Your Objects",275,313),("12","Error Handling with Exceptions",313,355),
 ("13","Strings",355,393),("14","Type Information",393,439),
 ("15","Generics",439,535),("16","Arrays",535,567),
 ("17","Containers in Depth",567,647),("18","I/O",647,725),
 ("19","Enumerated Types",725,761),("20","Annotations",761,797),
 ("21","Concurrency",797,933),("22","Graphical User Interfaces",933,1035),
]
FURNITURE = re.compile(r"^\s*(\d{1,4}|Thinking in Java|Bruce Eckel)\s*$", re.I)


def pages_of(doc, start_pdf, end_pdf):
    out = []
    for i in range(start_pdf - 1, min(end_pdf - 1, doc.page_count)):
        lines = []
        for blk in doc[i].get_text("dict")["blocks"]:
            for ln in blk.get("lines", []):
                spans = [s for s in ln["spans"] if s["text"].strip()]
                if not spans:
                    continue
                t = re.sub(r"\s+", " ", "".join(s["text"] for s in spans)).strip()
                if not t or FURNITURE.match(t):
                    continue
                mono = sum(1 for s in spans if re.search(r"(courier|consol|mono|code)", s["font"], re.I)) >= len(spans) / 2
                size = max(s["size"] for s in spans)
                lines.append({"t": t, "mono": mono, "size": size, "bold": any("bold" in s["font"].lower() for s in spans)})
        out.append({"page": i + 1, "lines": lines})
    return out


def brief(pages):
    """Prose paragraphs + headings + code blocks, page-anchored."""
    body, code, para = [], [], []

    def flush_code():
        if code:
            body.append("```java\n" + "\n".join(code) + "\n```")
            code.clear()

    def flush_para():
        if para:
            body.append(" ".join(para))
            para.clear()

    for pg in pages:
        if not pg["lines"]:
            continue
        body.append(f"\n<!--p{pg['page']}-->")
        for l in pg["lines"]:
            t = l["t"]
            if l["mono"]:
                flush_para()
                code.append(t)
                continue
            flush_code()
            if l["bold"] and l["size"] >= 13 and len(t) < 70 and not t.startswith(("\u201c", '"', "\u2018")):
                flush_para()
                body.append(f"## {t}")
            else:
                para.append(t)
    flush_code(); flush_para()
    return "\n".join(body)


def main(only=None):
    doc = pymupdf.open(PDF)
    os.makedirs(OUT, exist_ok=True)
    stats = []
    for num, title, printed_start, printed_end in CHAPTERS:
        if only and num not in only:
            continue
        s, e = printed_start + OFFSET, printed_end + OFFSET
        txt = brief(pages_of(doc, s, e))
        path = os.path.join(OUT, f"ch{int(num):02d}_brief.md")
        open(path, "w", encoding="utf-8").write(f"# {num}. {title} (printed p{printed_start}-{printed_end-1})\n\n" + txt)
        stats.append((num, title, len(txt), txt.count("\n## ")))
        print(f"ch{num:>2} printed {printed_start}-{printed_end-1} -> brief {len(txt):>6}c headings {stats[-1][3]:>2}  {title}")
    json.dump([{"ch": s[0], "title": s[1], "chars": s[2], "headings": s[3]} for s in stats],
              open(os.path.join(OUT, "chapters.json"), "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main([x for x in sys.argv[1:]] or None)

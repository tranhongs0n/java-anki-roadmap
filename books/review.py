# -*- coding: utf-8 -*-
"""Feedback loop for a book chapter: coverage, duplicates, lint, card shape."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import anki
from lint import lint_cards

KINDS = {"basic", "cloze", "visual"}


def norm(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\{\{c\d+::|\}\}", " ", s)
    s = re.sub(r"&[a-z]+;", " ", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def main(chapter):
    deck_prefix = "20 Head First Java"
    notes = []
    own = [d for d in anki.deck_names() if d.startswith(deck_prefix) and d.split("::")[-1].startswith(f"{chapter:02d} ")]
    for d in anki.deck_names():
        if d.startswith(deck_prefix) and "::" in d and d not in own:
            notes.extend(anki.notes_info(anki.find_notes(f'deck:"{d}"')))
    fronts = {norm(n["fields"].get("Front", {}).get("value", "") or n["fields"].get("Text", {}).get("value", "")): n for n in notes}
    brief = open(f"books/hfj3e/ch{chapter:02d}_brief.md", encoding="utf-8").read()
    raw = [(t.strip(), int(pg)) for t, pg in re.findall(r"^## (.+?) <!--p(\d+)-->$", brief, re.M)]
    seen, headings = set(), []
    for t, pg in sorted(raw, key=lambda x: x[1]):
        if (t, pg) in seen:
            continue
        seen.add((t, pg)); headings.append((t, pg))

    payload = json.load(open(f"cards/book-hfj3e-ch{chapter:02d}.json", encoding="utf-8"))
    cards = payload["cards"]
    problems = lint_cards(f"ch{chapter:02d}", payload)

    print(f"== ch{chapter}: {len(cards)} cards, {len(headings)} sections in brief")

    def page_of(card):
        m = re.search(r"p\.?\s*(\d+)\s*$", card.get("source", ""))
        return int(m.group(1)) if m else None

    # coverage: every TOC section should own at least one card by page
    for i, (h, pg) in enumerate(headings):
        end = headings[i + 1][1] if i + 1 < len(headings) else 10 ** 6
        got = [c for c in cards if page_of(c) is not None and (pg - 1) <= page_of(c) < end]
        print(f"   {'ok ' if got else 'GAP'}  p{pg:<4} {h[:62]}  ({len(got)})")
    # 2. duplicates against every note already in the book tree
    for c in cards:
        k = norm(c.get("front", ""))
        if k in fronts:
            print(f"   DUP  {c['front'][:70]}")
    # 3. card shape
    for c in cards:
        back = re.sub(r"<[^>]+>", "", c.get("back", ""))
        if len(back) > 120: print(f"   LONG back ({len(back)}): {c['front'][:60]}")
        if re.search(r",\s*and\s|\band\b.*\band\b", back) and len(back) > 80:
            print(f"   LIST-Y back: {c['front'][:60]}")
        if len(c.get("extra", "")) < 80: print(f"   THIN extra: {c['front'][:60]}")
    if problems:
        print("   lint:", *problems, sep="\n     ")
    print("done")


if __name__ == "__main__":
    main(int(sys.argv[1]))

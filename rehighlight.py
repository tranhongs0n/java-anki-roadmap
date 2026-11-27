# -*- coding: utf-8 -*-
"""Re-apply Java syntax highlighting to notes already in Anki.

Needed when notes were pushed by a path that did not run highlight_fields():
the card CSS has the token colours, but the fields carry no <span class="kw"> markup,
so code renders monochrome.

    python rehighlight.py --dry-run          # count what would change
    python rehighlight.py --deck "01 Foundations"   # limit to a deck
    python rehighlight.py                    # rewrite every note in the tree

Idempotent: highlight_fields() strips existing spans inside <code>/<pre> before
re-tokenising, so a second run changes nothing.
"""
import argparse
import re
import sys

import anki
from highlight import highlight_fields

FIELDS = ("Front", "Back", "Extra", "Text", "Question")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--deck", default="00 Java Roadmap")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    decks = [d for d in anki.deck_names() if args.deck.lower() in d.lower()]
    if not decks:
        sys.exit(f"no deck matches {args.deck!r}")
    ids = []
    for d in decks:
        ids.extend(anki.find_notes(f'deck:"{d}"'))
    if args.limit:
        ids = ids[: args.limit]
    print(f"{len(ids)} notes across {len(decks)} deck(s) matching {args.deck!r}")

    changed = scanned = 0
    batch = []
    for i in range(0, len(ids), 200):
        for note in anki.notes_info(ids[i:i + 200]):
            scanned += 1
            cur = {k: v["value"] for k, v in note["fields"].items()}
            new = {}
            for name in FIELDS:
                if name in cur:
                    hl = highlight_fields(cur[name])
                    if hl != cur[name]:
                        new[name] = hl
            if new:
                changed += 1
                batch.append((note["noteId"], new))

        if not args.dry_run and batch:
            for nid, fields in batch:
                anki.update_note_fields(nid, fields)
            batch = []

    print(f"scanned {scanned}, {'would update' if args.dry_run else 'updated'} {changed}")


if __name__ == "__main__":
    try:
        main()
    except anki.AnkiError as e:
        sys.exit(str(e))

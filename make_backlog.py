# -*- coding: utf-8 -*-
"""Rebuild out/examples-backlog.json: every repo card that still has no Example field.

    python make_backlog.py

The file is a JSON list, sorted by deck then CardKey, with the note id so a later push can be
verified against the collection. Run it after each fill_examples.py push.
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import anki  # noqa: E402
from keys import card_key  # noqa: E402

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "out", "examples-backlog.json")


def plain(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html or "")).strip()


def main():
    ids = list(set(anki.find_notes('deck:"00 Java Roadmap"')))
    notes = []
    for i in range(0, len(ids), 400):
        notes += anki.notes_info(ids[i:i + 400])
    note_of, has_example = {}, set()
    for note in notes:
        fields = {k: v["value"] for k, v in note["fields"].items()}
        key = plain(fields.get("CardKey", ""))
        if not key:
            continue
        note_of[key] = note["noteId"]
        if plain(fields.get("Example", "")):
            has_example.add(key)

    backlog = []
    for path in sorted(glob.glob(os.path.join(BASE, "cards", "*.json"))):
        data = json.load(open(path, encoding="utf-8"))
        for batch in data.get("batches") or [data]:
            for card in batch["cards"]:
                kind = card.get("type", "basic")
                kind = kind if kind in ("basic", "cloze", "visual") else "basic"
                key = card_key(batch["deck"], kind, card)
                if key in has_example or key not in note_of:
                    continue
                backlog.append({
                    "key": key,
                    "note": note_of[key],
                    "deck": batch["deck"],
                    "file": os.path.basename(path),
                    "front": plain(card.get("front") or card.get("text") or card.get("question")),
                    "back": plain(card.get("back")),
                    "kind": kind,
                    "src": card.get("source") or batch.get("source", ""),
                })
    backlog.sort(key=lambda r: (r["deck"], r["key"]))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(backlog, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"backlog: {len(backlog)} card(s) without an Example")
    if backlog:
        print("next up:", backlog[0]["deck"], "|", backlog[0]["front"][:60])


if __name__ == "__main__":
    main()

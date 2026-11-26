# -*- coding: utf-8 -*-
"""Offline fallback: cards/*.json + media/ -> out/Java-Roadmap.apkg (genanki).

The default push path is push.py (AnkiConnect). This exists for when Anki is not
running or the deck must travel as a single file.
"""
import glob
import json
import os
import sys

import genanki

from highlight import highlight_fields
from keys import card_key
from lint import lint_all
from models import CSS, SPECS, genanki_models

BASE = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE, "media")
CARDS_DIR = os.path.join(BASE, "cards")
OUT = os.path.join(BASE, "out", "Java-Roadmap.apkg")

MODELS = {m.name: m for m in genanki_models()}
MODEL_OF = {"basic": "JV Basic", "cloze": "JV Cloze", "visual": "JV Visual"}


def deck_id(name):
    import hashlib
    h = int(hashlib.sha1(name.encode("utf-8")).hexdigest()[:8], 16)
    return h & 0x7FFFFFFF


def main():
    problems = lint_all(CARDS_DIR)
    if problems:
        print(f"LINT: {len(problems)} problem(s)")
        print("\n".join(problems))
        if "--strict" in sys.argv:
            sys.exit(1)

    decks, media, total = {}, set(), 0
    for path in sorted(glob.glob(os.path.join(CARDS_DIR, "*.json"))):
        payload = json.load(open(path, encoding="utf-8"))
        deck_name = payload["deck"]
        deck = decks.setdefault(deck_name, genanki.Deck(deck_id(deck_name), deck_name))
        for c in payload["cards"]:
            kind = c.get("type", "basic")
            key = card_key(deck_name, kind, c)
            tags = c.get("tags", []) + payload.get("tags", [])
            src = c.get("source", "")
            if kind == "basic":
                fields = [highlight_fields(c["front"]), highlight_fields(c["back"]),
                          highlight_fields(c.get("extra", "")), src, key]
            elif kind == "cloze":
                fields = [highlight_fields(c["text"]), highlight_fields(c.get("extra", "")),
                          src, key]
            elif kind == "visual":
                media.add(os.path.join(MEDIA_DIR, c["image"]))
                fields = [f'<img src="{c["image"]}">',
                          highlight_fields(c.get("question", "What does this show?")),
                          highlight_fields(c["back"]),
                          highlight_fields(c.get("extra", "")), src, key]
            else:
                sys.exit(f"unknown card type {kind!r} in {path}")
            deck.add_note(genanki.Note(model=MODELS[MODEL_OF[kind]], fields=fields,
                                       tags=tags,
                                       guid=genanki.guid_for(key)))
            total += 1

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    pkg = genanki.Package(list(decks.values()))
    pkg.media_files = sorted(media)
    pkg.write_to_file(OUT)
    print(f"{total} notes, {len(decks)} decks, {len(media)} media files -> {OUT}")


if __name__ == "__main__":
    main()

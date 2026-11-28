# -*- coding: utf-8 -*-
"""Push cards/*.json into the running Anki through AnkiConnect.

    python push.py                 # add new, update changed, skip identical
    python push.py --dry-run       # print what would happen, write nothing
    python push.py --strict        # lint failures are fatal
    python push.py --only basic    # only decks whose path matches
    python push.py --browse        # open the pushed decks in the browser

Identity: every note carries a hidden CardKey field, hashed from the deck and the
fact (not from the answer text), so re-pushing updates in place and never duplicates.
"""
import argparse
import base64
import glob
import hashlib
import json
import os
import re
import sys

import anki
from highlight import highlight_fields
from keys import card_key
from lint import batches_of, lint_all, lint_examples
from models import CSS, SPECS

BASE = os.path.dirname(os.path.abspath(__file__))
CARDS_DIR = os.path.join(BASE, "cards")
MEDIA_DIR = os.path.join(BASE, "media")
LEDGER = os.path.join(BASE, "out", "pushed.json")

KINDS = {"basic", "cloze", "visual"}   # anything else (compare, rule, table…) is a basic card
TEMPLATE_OF = {"basic": "JV Basic", "cloze": "JV Cloze", "visual": "JV Visual"}


def note_fields(kind, card, key, image_tag=None, batch_src=""):
    if kind == "basic":
        return {"Front": highlight_fields(card["front"]),
                "Back": highlight_fields(card["back"]),
                "Extra": highlight_fields(card.get("extra", "")),
                "Example": highlight_fields(card.get("example", "")),
                "Example": highlight_fields(card.get("example", "")),
                "Source": card.get("source") or batch_src, "CardKey": key}
    if kind == "cloze":
        return {"Text": highlight_fields(card["text"]),
                "Extra": highlight_fields(card.get("extra", "")),
                "Example": highlight_fields(card.get("example", "")),
                "Source": card.get("source") or batch_src, "CardKey": key}
    if kind == "visual":
        return {"Image": image_tag,
                "Question": highlight_fields(card.get("question", "What does this show?")),
                "Back": highlight_fields(card["back"]),
                "Extra": highlight_fields(card.get("extra", "")),
                "Example": highlight_fields(card.get("example", "")),
                "Source": card.get("source") or batch_src, "CardKey": key}
    raise SystemExit(f"unknown card type: {kind}")


def ensure_models(dry):
    existing = set(anki.model_names())
    for name, spec in SPECS.items():
        if name not in existing:
            print(f"  model {name}: create")
            if not dry:
                anki.create_model(name, spec["fields"], spec["templates"],
                                  CSS, spec["isCloze"])
            continue
        have = anki.model_fields(name)
        for f in spec["fields"]:
            if f not in have:
                print(f"  model {name}: add field {f}")
                if not dry:
                    anki.add_field(name, f)
        print(f"  model {name}: styling + templates")
        if not dry:
            anki.update_styling(name, CSS)
            anki.update_templates(name, spec["templates"])


def ensure_decks(deck_paths, dry):
    existing = set(anki.deck_names())
    for path in sorted(deck_paths):
        parts = path.split("::")
        for i in range(1, len(parts) + 1):
            name = "::".join(parts[:i])
            if name not in existing:
                print(f"  deck {name}: create")
                if not dry:
                    anki.create_deck(name)
                existing.add(name)


def ensure_media(paths, dry):
    if not paths:
        return
    have = set(anki.media_names()) if not dry else set()
    for p in sorted(paths):
        name = os.path.basename(p)
        if name in have:
            continue
        print(f"  media {name}: upload ({os.path.getsize(p) // 1024} KB)")
        if not dry:
            with open(p, "rb") as fh:
                anki.store_media(name, base64.b64encode(fh.read()).decode("ascii"))


def load_batches(only=None, file_glob=None):
    pattern = file_glob or "*.json"
    for path in sorted(glob.glob(os.path.join(CARDS_DIR, pattern))):
        payload = json.load(open(path, encoding="utf-8"))
        for batch in batches_of(payload):
            if only and only.lower() not in batch["deck"].lower():
                continue
            yield path, batch


def run(args):
    anki.version()  # fail fast with a readable message

    batches = list(load_batches(args.only, args.file))
    if not batches:
        sys.exit("no matching card batches")

    decks = {c.get("merge_into") or p.get("merge_into") or p["deck"] for _, p in batches for c in p["cards"]}
    print("Anki reachable. Preparing models and decks.")
    ensure_models(args.dry_run)
    ensure_decks(decks, args.dry_run)

    media = set()
    for _, payload in batches:
        for c in payload["cards"]:
            if c.get("image"):
                media.add(os.path.join(MEDIA_DIR, c["image"]))
    missing = [m for m in media if not os.path.exists(m)]
    if missing:
        sys.exit(f"missing image files: {missing}")
    ensure_media(media, args.dry_run)

    ledger = {}
    if os.path.exists(LEDGER):
        ledger = json.load(open(LEDGER, encoding="utf-8"))

    totals = {"new": 0, "updated": 0, "same": 0, "rejected": 0}
    pushed_decks = []

    no_example = 0
    for _, payload in batches:
        for batch in batches_of(payload):
            no_example += sum(1 for c in batch.get("cards", []) if not (c.get("example") or "").strip())

    for path, payload in batches:
        deck = payload["deck"]                       # identity (stable CardKey)
        place = payload.get("merge_into") or deck     # where the note actually lives
        new_notes, updates, same, rejected = [], [], 0, []
        for c in payload["cards"]:
            kind = c.get("type", "basic")
            if kind not in KINDS:
                kind = "basic"
            key = card_key(deck, kind, c)
            target = c.get("merge_into") or place
            img = (f'<img src="{c["image"]}">' if kind == "visual" else None)
            fields = note_fields(kind, c, key, img, payload.get("source", ""))
            tags = c.get("tags", []) + payload.get("tags", [])

            if args.limit and totals["new"] + totals["updated"] >= args.limit:
                continue

            hits = [] if args.dry_run else anki.find_notes(f'CardKey:"{key}"')
            if not hits:
                new_notes.append({"deckName": target, "modelName": TEMPLATE_OF[kind],
                                  "fields": fields, "tags": tags,
                                  "options": {"allowDuplicate": False,
                                              "duplicateScope": "deck"}})
                if args.dry_run:
                    print(f"  + {key} {deck} :: {(c.get('front') or c.get('text') or '')[:60]}")
            elif len(hits) > 1:
                rejected.append((key, f"{len(hits)} notes share this key"))
            else:
                nid = hits[0]
                current = anki.notes_info([nid])[0]["fields"]
                same_now = all((current.get(k, {}).get("value", "").strip()
                                == v.strip()) for k, v in fields.items())
                if same_now:
                    same += 1
                else:
                    updates.append((nid, fields, key))

        for nid, fields, key in updates:
            print(f"  ~ {key} update {target}")
            if not args.dry_run:
                anki.update_note_fields(nid, fields)

        if new_notes and not args.dry_run:
            ids = anki.add_notes(new_notes)
            added = 0
            for spec, nid in zip(new_notes, ids):
                if nid is None:
                    rejected.append((spec["fields"]["CardKey"], "rejected by Anki"))
                else:
                    added += 1
                    ledger[spec["fields"]["CardKey"]] = nid
            totals["new"] += added
        elif new_notes:
            totals["new"] += len(new_notes)

        totals["updated"] += len(updates)
        totals["same"] += same
        totals["rejected"] += len(rejected)
        if reserved := (new_notes or updates):
            pushed_decks.append(deck)

        print(f"{deck}: +{len(new_notes)} new, ~{len(updates)} updated, "
              f"={same} unchanged" + (f", !{len(rejected)} rejected" if rejected else ""))
        for key, why in rejected:
            print(f"    ! {key}: {why}")

    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    if not args.dry_run:
        json.dump(ledger, open(LEDGER, "w", encoding="utf-8"), indent=1)

    print(f"\ntotal: {totals['new']} new, {totals['updated']} updated, "
          f"{totals['same']} unchanged, {totals['rejected']} rejected")

    if no_example:
        print(f"note: {no_example} card(s) in this batch still have no Example")

    if args.browse and pushed_decks and not args.dry_run:
        for d in pushed_decks:
            anki.gui_browse(f'deck:"{d}"')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--only", default=None)
    ap.add_argument("--browse", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--file", default=None, help="only this cards/*.json (glob)")
    args = ap.parse_args()

    problems = lint_all(CARDS_DIR)
    if problems:
        print(f"lint: {len(problems)} problem(s)")
        print("\n".join(problems))
        if args.strict:
            sys.exit(1)

    try:
        run(args)
    except anki.AnkiError as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()

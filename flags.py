# -*- coding: utf-8 -*-
"""Flag workflow: what the user marked with Ctrl+1 (explain) and Ctrl+2 (audit).

    python flags.py list            # everything pending, grouped by deck
    python flags.py list --flag 2   # audit queue only
    python flags.py show <cardId>   # full fields of one card
    python flags.py done --cards 1 2 3 --note <vault path>   # clear flag, tag explain::done

Flag 1 = the card needs an explanation: write a note in the Obsidian vault, add atomic
cards to cards/*.json, push, then run `done` so the same card is never processed twice.
Flag 2 = the card is suspect (duplicate or violates the card standard): no cards are
added, the verdict goes to the vault audit log instead.

Card state is the source of truth; the ledger in out/flags.json is bookkeeping only.
"""
import argparse
import json
import os
import re
import sys

import anki

BASE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(BASE, "out", "flags.json")
VAULT = os.path.join(BASE, "vault")

TEXT_FIELDS = ("Front", "Text", "Word", "Question", "Expression")


def strip(html_text):
    text = re.sub(r"<[^>]+>", "", html_text or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def headline(fields):
    for name in TEXT_FIELDS:
        if fields.get(name):
            return strip(fields[name])
    for name, value in fields.items():
        if value and value.strip():
            return strip(value)
    return ""


def pending(flag):
    cards = anki.find_cards(f"flag:{flag}")
    rows = []
    for i in range(0, len(cards), 250):
        chunk = cards[i:i + 250]
        infos = anki.cards_info(chunk)
        note_ids = []
        for card in infos:
            note_ids.append(card.get("note") or (anki.cards_to_notes([card["cardId"]]) or [0])[0])
        notes = {n["noteId"]: n for n in anki.notes_info(note_ids)} if note_ids else {}
        for card in infos:
            fields = {k: v["value"] for k, v in card["fields"].items()}
            back = ""
            for name in ("Back", "Definition", "Meaning", "Answer"):
                if fields.get(name):
                    back = strip(fields[name])
                    break
            note = notes.get(card.get("note"), {})
            rows.append({
                "cardId": card["cardId"],
                "noteId": card.get("note"),
                "cardKey": strip(fields.get("CardKey", "")),
                "deck": card["deckName"],
                "model": card["modelName"],
                "front": headline(fields),
                "back": back,
                "tags": note.get("tags", []),
            })
    return rows


def load_ledger():
    if os.path.exists(LEDGER):
        return json.load(open(LEDGER, encoding="utf-8"))
    return {}


def save_ledger(ledger):
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    json.dump(ledger, open(LEDGER, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def slug(text, limit=48):
    text = re.sub(r"[^\w\s-]", "", strip(text).lower())
    return re.sub(r"[\s_-]+", "-", text).strip("-")[:limit]


def note_path(row):
    section = row["deck"].replace("00 Java Roadmap::", "").replace("::", " - ")
    folder = os.path.join(VAULT, "10 Explanations", section)
    if not os.path.isdir(folder):
        folder = os.path.join(VAULT, "10 Explanations")
    return os.path.join(folder, f"{row.get('cardKey') or row['cardId']} {slug(row['front'])}.md")


def cmd_list(args):
    rows = pending(args.flag)
    ledger = load_ledger()
    if not rows:
        print(f"no cards flagged {args.flag}")
        return
    by_deck = {}
    for row in rows:
        by_deck.setdefault(row["deck"], []).append(row)
    seen = 0
    for deck, items in sorted(by_deck.items()):
        print(f"\n{deck}  ({len(items)})")
        for row in items:
            done = "ledger" if str(row["cardId"]) in ledger else ""
            print(f"  {row['cardId']}  {row['model']:<12} {row['front'][:78]} {done}")
            seen += 1
    print(f"\ntotal: {seen}")


def cmd_show(args):
    for card in anki.cards_info([args.card_id]):
        print(card["deckName"], "|", card["modelName"], "| flags", card["flags"])
        for name, value in card["fields"].items():
            print(f"--- {name} ---")
            print(value["value"])


def cmd_done(args):
    ledger = load_ledger()
    rows = {str(r["cardId"]): r for r in pending(1) + pending(2) + pending(3) + pending(4)}
    for card_id in args.cards:
        row = rows.get(str(card_id)) or {}
        notes = anki.cards_to_notes([card_id])
        if not notes:
            print(f"  ! {card_id}: no such card")
            continue
        anki.set_flag([card_id], 0)
        if args.tag:
            anki.add_tags([notes[0]], [args.tag])
        ledger[str(card_id)] = {"note": args.note or "", "tag": args.tag or "",
                                "deck": row.get("deck", ""), "front": row.get("front", "")}
        print(f"  ok {card_id}: flag cleared" + (f", tagged {args.tag}" if args.tag else ""))
    save_ledger(ledger)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("list")
    p.add_argument("--flag", type=int, default=1)
    p.set_defaults(func=cmd_list)
    p = sub.add_parser("show")
    p.add_argument("card_id", type=int)
    p.set_defaults(func=cmd_show)
    p = sub.add_parser("done")
    p.add_argument("--cards", type=int, nargs="+", required=True)
    p.add_argument("--tag", default="explain::done")
    p.add_argument("--note", default="", help="vault note that explains this card")
    p.set_defaults(func=cmd_done)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

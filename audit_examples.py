# -*- coding: utf-8 -*-
"""Feedback loop for the Example field: check every example in the collection and repair the
mechanical defects, so a bad example cannot survive more than one cycle.

    python audit_examples.py            # report only
    python audit_examples.py --fix      # clean what is mechanically fixable
    python audit_examples.py --sample 12  # print a few finished examples for eyeballing

Checks:
  * the value is a bare <pre>…</pre> block (no <pre><code> nesting, which the highlighter escapes)
  * no HTML tags other than spans inside the block
  * no escaped tags (&lt;b&gt; …) left over from an older push
  * non-trivial length (>= 20 chars of code) and a sane upper bound
  * the card actually renders the block (class="ex" in its answer)
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import anki  # noqa: E402
from highlight import highlight_fields  # noqa: E402

BASE = os.path.dirname(os.path.abspath(__file__))
PRE = re.compile(r"^<pre>(.*)</pre>$", re.S)
BAD_TAG = re.compile(r"</?(?:code|b|i|strong|em|u|s|mark|font|div|br)\b[^>]*>", re.I)
ESCAPED = re.compile(r"&lt;/?(?:code|b|i|strong|em|pre)&gt;", re.I)


def plain(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html or "")).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix", action="store_true")
    ap.add_argument("--sample", type=int, default=0)
    args = ap.parse_args()

    notes = []
    ids = list(set(anki.find_notes('deck:"00 Java Roadmap"')))
    for i in range(0, len(ids), 400):
        notes += anki.notes_info(ids[i:i + 400])

    have, problems = [], []
    for note in notes:
        fields = {k: v["value"] for k, v in note["fields"].items()}
        example = fields.get("Example", "")
        if not plain(example):
            continue
        have.append((note["noteId"], fields, example))

        text = example.strip()
        m = PRE.match(text)
        if not m:
            problems.append((note["noteId"], "not a bare <pre> block", text[:60]))
            continue
        body = m.group(1)
        if BAD_TAG.search(body) or ESCAPED.search(body):
            problems.append((note["noteId"], "markup inside the block", body[:60]))
        code = plain(body)
        if len(code) < 20:
            problems.append((note["noteId"], f"too short ({len(code)} chars)", code))
        elif len(code) > 900:
            problems.append((note["noteId"], f"too long ({len(code)} chars)", code[:60]))

    render_bad = 0
    cards = [anki.find_cards(f'nid:{nid}') for nid, _, _ in have[:400]]
    for (nid, fields, example), card_ids in zip(have[:400], cards):
        if not card_ids:
            continue
        info = anki.cards_info([card_ids[0]])[0]
        if 'class="ex"' not in info["answer"]:
            render_bad += 1

    print(f"examples in the tree: {len(have)}")
    print(f"render failures (first 400 checked): {render_bad}")
    print(f"defects: {len(problems)}")
    for nid, why, detail in problems[:25]:
        print(f"  {nid}  {why}: {detail}")

    if args.fix and problems:
        fixed = 0
        for nid, why, _ in problems:
            note = anki.notes_info([nid])[0]
            fields = {k: v["value"] for k, v in note["fields"].items()}
            value = fields.get("Example", "")
            body = PRE.match(value.strip())
            body = body.group(1) if body else value
            body = ESCAPED.sub("", body)
            body = BAD_TAG.sub("", body)
            body = body.replace("<code>", "").replace("</code>", "")
            cleaned = "<pre>" + body.strip() + "</pre>"
            if cleaned != value:
                anki.update_note_fields(nid, {"Example": highlight_fields(cleaned)})
                fixed += 1
        print(f"repaired: {fixed}")

    if args.sample:
        step = max(1, len(have) // args.sample)
        for nid, fields, example in have[::step][:args.sample]:
            question = plain(fields.get("Front") or fields.get("Text") or "")
            print(f"\n--- {nid} | {question[:80]}")
            print(plain(example)[:220])


if __name__ == "__main__":
    main()

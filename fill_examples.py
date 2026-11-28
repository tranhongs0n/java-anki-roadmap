# -*- coding: utf-8 -*-
"""Apply Example fields to cards in cards/*.json, validate them with javac, then push.

    python fill_examples.py out/examples/map.json            # apply + javac check, no push
    python fill_examples.py out/examples/map.json --push     # also push every touched live file

The map is {"jv-0001-xxxxxxxx": "<pre>code</pre>", ...} or
{"jv-0001-xxxxxxxx": {"example": "<pre>...</pre>", "extra": "..."}}

Rules enforced here:
  * the payload must be a bare <pre> block (a nested <code> gets escaped by the highlighter);
  * every snippet is wrapped in `class Ex { static void m() { ... } }` and compiled with javac,
    so an example that does not compile fails the run instead of reaching the collection;
  * a file whose deck string is no longer live is never pushed (that would fork the tree); its
    cards are still updated in the repo and reported.
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from keys import card_key  # noqa: E402

BASE = os.path.dirname(os.path.abspath(__file__))
CARDS = os.path.join(BASE, "cards")

PRE = re.compile(r"<pre>.*?</pre>", re.S)
TAGS = re.compile(r"</?[a-zA-Z][^<>]*>")


def strip_pre(html):
    text = TAGS.sub("", html)
    for a, b in (("&lt;", "<"), ("&gt;", ">"), ("&amp;", "&"), ("&quot;", '"'), ("&#39;", "'")):
        text = text.replace(a, b)
    return text


def check(code):
    """Compile one snippet in isolation. Returns None on success, else the first error line."""
    snippet = strip_pre(code)
    if re.search(r"^\s*(public\s+)?(class|enum|interface|record)\s", snippet, re.M):
        src = snippet                      # already a compilation unit
    else:
        src = "class Ex { static void m() {\n" + snippet + "\n} }"
    with tempfile.TemporaryDirectory() as tmp:
        f = os.path.join(tmp, "Ex.java")
        open(f, "w", encoding="utf-8").write(src)
        r = subprocess.run(["javac", "-d", tmp, f], capture_output=True, text=True)
        if r.returncode == 0:
            return None
        lines = [l.strip() for l in r.stderr.splitlines() if "error:" in l]
        return lines[0] if lines else r.stderr.strip().splitlines()[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("map")
    ap.add_argument("--push", action="store_true")
    ap.add_argument("--skip-javac", action="store_true")
    args = ap.parse_args()

    mapping = json.load(open(args.map, encoding="utf-8"))
    bad = []
    for key, payload in mapping.items():
        example = payload["example"] if isinstance(payload, dict) else payload
        if "<pre><code>" in example:
            bad.append((key, "nested <code> inside <pre>"))
            continue
        if not PRE.search(example):
            bad.append((key, "not a <pre> block"))
            continue
        if isinstance(payload, dict) and payload.get("skip_javac"):
            continue          # shell commands, framework config, snippets needing a jar
        if not args.skip_javac:
            err = check(example)
            if err:
                bad.append((key, err))
    if bad:
        for key, why in bad:
            print(f"  ! {key}: {why}")
        sys.exit(f"{len(bad)} example(s) rejected; nothing written")

    live = None
    touched = {}
    applied = 0
    for path in sorted(glob.glob(os.path.join(CARDS, "*.json"))):
        data = json.load(open(path, encoding="utf-8"))
        changed = 0
        for batch in data.get("batches") or [data]:
            for card in batch["cards"]:
                kind = card.get("type", "basic")
                kind = kind if kind in ("basic", "cloze", "visual") else "basic"
                key = card_key(batch["deck"], kind, card)
                if key not in mapping:
                    continue
                payload = mapping[key]
                if isinstance(payload, dict):
                    if "example" in payload:
                        card["example"] = payload["example"]
                    if "extra" in payload:
                        card["extra"] = payload["extra"]
                else:
                    card["example"] = payload
                changed += 1
                applied += 1
        if changed:
            json.dump(data, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
            touched[os.path.basename(path)] = changed
    print(f"applied {applied} example(s) across {len(touched)} file(s): {touched}")

    if not args.push:
        return
    import anki
    live = set(anki.deck_names())
    skip = []
    for name in touched:
        data = json.load(open(os.path.join(CARDS, name), encoding="utf-8"))
        decks = {b["deck"] for b in (data.get("batches") or [data])}
        merges = {c.get("merge_into") for b in (data.get("batches") or [data]) for c in b["cards"]}
        ok = all(d in live or any(merge in live for merge in merges) for d in decks)
        if not ok:
            skip.append(name)
    if skip:
        print(f"  not pushing (deck string no longer live): {skip}")
    pushable = sorted(set(touched) - set(skip))
    if pushable:
        # push.py takes ONE --file glob, so each touched file needs its own run;
        # passing several --file flags silently keeps only the last one.
        print("  pushing:", pushable)
        rc = 0
        for name in pushable:
            r = subprocess.run([sys.executable, os.path.join(BASE, "push.py"), "--strict", "--file", name],
                               cwd=BASE, capture_output=True, text=True)
            tail = [l for l in r.stdout.splitlines() if l.startswith("total:")]
            print(f"    {name}: {tail[-1] if tail else r.stdout.strip()[-120:] or r.stderr.strip()[-120:]}")
            rc = rc or r.returncode
        sys.exit(rc)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Re-render the deck tree inside BLUEPRINT.md from decks.json.

Idempotent: replaces the fenced block that starts with "00 Java Roadmap".
"""
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(BASE, "BLUEPRINT.md")


def render(tree):
    lines = ["```", tree["deck"]]
    secs = tree["sections"]
    for i, sec in enumerate(secs):
        last = i == len(secs) - 1
        topics = sec.get("topics", [])
        if not topics:
            label = f"   ({sec.get('cards', 0)} cards)"
        else:
            res = sum(t.get("n_resources", 0) for t in topics)
            label = f"   ({len(topics)} decks · {res} resources)"
        lines.append(("└─ " if last else "├─ ") + sec["deck"] + label)
        pre = "   " if last else "│  "
        for j, topic in enumerate(topics):
            lastt = j == len(topics) - 1
            tag = "[overview]" if topic.get("synthetic") else f"[{topic.get('n_resources', 0)} res]"
            lines.append(pre + ("└─ " if lastt else "├─ ") + topic["deck"] + "   " + tag)
    lines.append("```")
    return "\n".join(lines)


def main():
    tree = json.load(open(os.path.join(BASE, "decks.json"), encoding="utf-8"))
    doc = open(DOC, encoding="utf-8").read()
    new = render(tree)
    patched, n = re.subn(r"```\n" + re.escape(tree["deck"]) + r"\n.*?\n```", new, doc, flags=re.S)
    if not n:
        raise SystemExit("tree block not found in BLUEPRINT.md")
    open(DOC, "w", encoding="utf-8").write(patched)
    decks = sum(len(s.get("topics", [])) for s in tree["sections"])
    print(f"tree re-rendered: {len(tree['sections'])} sections, {decks} decks")


if __name__ == "__main__":
    main()

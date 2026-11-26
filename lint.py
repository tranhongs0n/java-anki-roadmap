# -*- coding: utf-8 -*-
"""Card-batch lint. A warning nobody reads is not a gate."""
import os

MIN_EXTRA = 60
POINTER = ("see the article", "read the article", "visit the", "see source", "read more")
ROOT_SOURCES = {"https://roadmap.sh/java", "https://roadmap.sh/java/", "https://roadmap.sh/"}


def lint_cards(path, payload, min_extra=MIN_EXTRA):
    problems = []
    for i, c in enumerate(payload["cards"], start=1):
        extra = (c.get("extra") or "").strip()
        label = (c.get("front") or c.get("question") or c.get("text") or "")[:60]
        if not extra:
            problems.append(f"  {path}#{i} missing extra: {label}")
        elif len(extra) < min_extra:
            problems.append(f"  {path}#{i} extra too short ({len(extra)}): {label}")
        elif any(p in extra.lower() for p in POINTER):
            problems.append(f"  {path}#{i} extra points at a resource: {label}")
        src = (c.get("source") or "").strip()
        if not src:
            problems.append(f"  {path}#{i} missing source: {label}")
        elif src.rstrip("/") in {u.rstrip("/") for u in ROOT_SOURCES} and "scope::map" not in c.get("tags", []):
            problems.append(f"  {path}#{i} source is the roadmap root, not the page: {label}")
        if not any(t.startswith("type::") for t in c.get("tags", [])):
            problems.append(f"  {path}#{i} missing type:: tag: {label}")
    return problems


def lint_all(cards_dir):
    import glob, json
    problems = []
    for p in sorted(glob.glob(os.path.join(cards_dir, "*.json"))):
        payload = json.load(open(p, encoding="utf-8"))
        problems += lint_cards(os.path.basename(p), payload)
    return problems

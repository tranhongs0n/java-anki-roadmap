# -*- coding: utf-8 -*-
"""Card-batch lint. A warning nobody reads is not a gate."""
import os

MIN_EXTRA = 60
POINTER = ("see the article", "read the article", "visit the", "see source", "read more")
ROOT_SOURCES = {"https://roadmap.sh/java", "https://roadmap.sh/java/", "https://roadmap.sh/"}


def batches_of(payload):
    """Accept {"deck","cards"} and {"batches":[...]}, with a file-level source."""
    root_src = payload.get("source", "") if isinstance(payload, dict) else ""
    batches = payload["batches"] if isinstance(payload, dict) and "batches" in payload else [payload]
    out = []
    for b in batches:
        if root_src and not b.get("source"):
            b = dict(b, source=root_src)
        out.append(b)
    return out


def lint_cards(path, payload, min_extra=MIN_EXTRA):
    problems = []
    # a card may inherit its source from the batch wrapper
    cards = [(i, c, b.get("source", "")) for b in batches_of(payload)
             for i, c in enumerate(b.get("cards", []), start=1)]
    for i, c, batch_src in cards:
        extra = (c.get("extra") or "").strip()
        label = (c.get("front") or c.get("question") or c.get("text") or "")[:60]
        if not extra:
            problems.append(f"  {path}#{i} missing extra: {label}")
        elif len(extra) < min_extra:
            problems.append(f"  {path}#{i} extra too short ({len(extra)}): {label}")
        elif any(p in extra.lower() for p in POINTER):
            problems.append(f"  {path}#{i} extra points at a resource: {label}")
        src = (c.get("source") or batch_src or "").strip()
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

def lint_examples(cards_dir):
    """Every card is expected to carry an Example. Returns {card_label: path} for the ones that do not."""
    import glob, json, os
    missing = []
    for path in sorted(glob.glob(os.path.join(cards_dir, "*.json"))):
        payload = json.load(open(path, encoding="utf-8"))
        for batch in batches_of(payload):
            for card in batch.get("cards", []):
                if not (card.get("example") or "").strip():
                    label = (card.get("front") or card.get("text") or "")[:60]
                    missing.append((os.path.basename(path), label))
    return missing

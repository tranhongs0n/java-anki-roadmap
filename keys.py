# -*- coding: utf-8 -*-
"""Note identity: stable, deterministic, shared by both push paths."""
import hashlib
import re


def card_key(deck, kind, card):
    ident = card.get("front") or card.get("text") or card.get("question") or ""
    ident = re.sub(r"\s+", " ", ident).strip()
    h = hashlib.sha1(f"{deck}|{kind}|{ident}".encode("utf-8")).hexdigest()[:10]
    secs = re.findall(r"^(\d{2})", deck.replace("::", "\n"), re.M)
    prefix = "".join(secs[:2]) or "00"
    return f"jv-{prefix}-{h}"

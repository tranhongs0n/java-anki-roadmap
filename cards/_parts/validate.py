import json, os, re, collections

parts = os.path.dirname(os.path.abspath(__file__))
out_dir = os.path.dirname(parts)
out_path = os.path.join(out_dir, "devjava-CHUNK-1.json")

KINDS = {"definition", "gotcha", "syntax", "rule", "convention", "mental-model", "compare"}
TYPES = {"basic", "cloze", "compare", "rule", "table"}

batches = []
for f in ("p1.json", "p2.json", "p3.json", "p4.json", "p5.json"):
    with open(os.path.join(parts, f), encoding="utf-8") as fh:
        batches.extend(json.load(fh)["batches"])

# table-shaped cards keep type=table but must carry one of the seven kind tags
for bt in batches:
    for c in bt["cards"]:
        if c["type"] == "table" and (not c["tags"] or c["tags"][0] not in {"type::" + k for k in KINDS}):
            c["tags"] = ["type::" + ("syntax" if len(c["back"]) < 45 else "definition")]

result = {"batches": batches}
with open(out_path, "w", encoding="utf-8") as fh:
    json.dump(result, fh, ensure_ascii=False, indent=1)

errs = []
seen = set()
for bi, bt in enumerate(batches, 1):
    if set(bt) != {"deck", "source", "tags", "cards"}:
        errs.append(f"batch {bi} keys {set(bt)}")
    if not re.match(r"https://dev\.java/(learn|organizing)/", bt["source"]):
        errs.append(f"batch {bi} bad source {bt['source']}")
    for t in ("roadmap::java", "devjava"):
        if t not in bt["tags"]:
            errs.append(f"batch {bi} missing tag {t}")
    for ci, c in enumerate(bt["cards"], 1):
        loc = f"{bi}.{ci}"
        if c["type"] not in TYPES:
            errs.append(f"{loc} bad type {c['type']}")
        tt = [t for t in c["tags"] if t.startswith("type::")]
        if len(tt) != 1 or tt[0][6:] not in KINDS:
            errs.append(f"{loc} type tags {tt}")
        if not (60 <= len(c["extra"]) <= 260):
            errs.append(f"{loc} extra len {len(c['extra'])}")
        low = c["extra"].lower()
        for bad in ("see the article", "read more", "shown above", "as above", "the example above", "this article", "this page"):
            if bad in low:
                errs.append(f"{loc} pointer phrase '{bad}'")
        if c["type"] == "cloze":
            if "{{c1::" not in c["text"]:
                errs.append(f"{loc} cloze without c1")
            if len(re.sub(r"\{\{c\d+::(.*?)\}\}", r"\1", c["text"])) > 200:
                errs.append(f"{loc} cloze text too long")
            key = re.sub(r"\s+", " ", c["text"]).strip()
        else:
            if len(c["back"]) > 110:
                errs.append(f"{loc} back len {len(c['back'])}: {c['back'][:60]}")
            if len(c["front"]) > 150:
                errs.append(f"{loc} front len {len(c['front'])}")
            key = re.sub(r"\s+", " ", c["front"]).strip()
        if key in seen:
            errs.append(f"{loc} duplicate: {key[:60]}")
        seen.add(key)
        for field in ("front", "back", "extra"):
            v = c.get(field)
            if not v:
                continue
            for tag in ("b", "code", "i"):
                if v.count(f"<{tag}>") != v.count(f"</{tag}>"):
                    errs.append(f"{loc} unbalanced <{tag}> in {field}")
            if re.search(r"</?(span|td|tr|table)>", v):
                errs.append(f"{loc} stray table/span markup in {field}")

print("batches:", len(batches))
print("cards:", sum(len(b["cards"]) for b in batches))
for b in batches:
    print(f"  {len(b['cards']):>3}  {b['source'].split('dev.java')[1]:<72} -> {b['deck'].split('::')[-1].strip()}")
print("\ncards per deck:")
for d, n in sorted(collections.Counter(b["deck"] for b in batches for _ in b["cards"]).items()):
    print(f"  {n:>3}  {d}")
print("\ncard types:", dict(collections.Counter(c["type"] for b in batches for c in b["cards"])))
print("kinds:", dict(collections.Counter(c["tags"][0] for b in batches for c in b["cards"])))
print("\nerrors:", len(errs))
for e in errs:
    print("  ", e)

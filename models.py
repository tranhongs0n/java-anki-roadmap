# -*- coding: utf-8 -*-
"""Note-type definitions shared by both push paths.

The CardKey field is the identity of a note: deterministic, hidden from the card,
and searchable from AnkiConnect. It is derived from the fact, not from the wording
of the answer, so editing an explanation updates in place.
"""

CSS = """
.card { font-family: -apple-system, "Segoe UI", Roboto, sans-serif; font-size: 20px;
        text-align: left; color: #1a1a1a; background: #fdfdfd; line-height: 1.45; }
.nightMode.card, .night_mode .card { color: #e8e8e8; background: #1f1f1f; }
.q { font-weight: 600; font-size: 22px; margin-bottom: 12px; }
.a { border-top: 1px solid #d0d0d0; padding-top: 10px; }
code, pre { font-family: "Cascadia Code", Consolas, monospace; font-size: 17px;
            background: #f0f0f0; border-radius: 4px; padding: 1px 4px; }
pre { padding: 10px; overflow-x: auto; white-space: pre-wrap; }
.nightMode code, .night_mode code, .nightMode pre, .night_mode pre { background: #2b2b2b; }
img { max-width: 100%; border-radius: 6px; display: block; margin: 10px 0; }
.extra { font-size: 16px; color: #555; margin-top: 12px; }
.nightMode .extra, .night_mode .extra { color: #aaa; }
.src { font-size: 12px; color: #888; margin-top: 14px; word-break: break-all; }
.cloze { font-weight: 700; color: #1565c0; }

/* --- Java code colour scheme (light: IntelliJ, dark: VS Code) --- */
.kw, .lit { color: #0033b3; font-weight: 600; }
.type     { color: #267f99; }
.fn       { color: #00627a; }
.str, .chr{ color: #067d17; }
.num      { color: #1750eb; }
.cmt      { color: #8c8c8c; font-style: italic; }
.ann      { color: #9e880d; }
.nightMode .kw, .night_mode .kw, .nightMode .lit, .night_mode .lit { color: #569cd6; }
.nightMode .type, .night_mode .type { color: #4ec9b0; }
.nightMode .fn, .night_mode .fn { color: #dcdcaa; }
.nightMode .str, .night_mode .str, .nightMode .chr, .night_mode .chr { color: #ce9178; }
.nightMode .num, .night_mode .num { color: #b5cea8; }
.nightMode .cmt, .night_mode .cmt { color: #6a9955; }
.nightMode .ann, .night_mode .ann { color: #dcdcaa; }
pre { background: #f6f8fa; border-left: 3px solid #d0d7de; border-radius: 6px; }
.nightMode pre, .night_mode pre { background: #252526; border-left-color: #3c3c3c; }
"""

BASIC_AFMT = ('<div class="q">{{Front}}</div><div class="a">{{Back}}</div>'
              '{{#Extra}}<div class="extra">{{Extra}}</div>{{/Extra}}'
              '{{#Source}}<div class="src">{{Source}}</div>{{/Source}}')

SPECS = {
    "JV Basic": {
        "id": 1749200001,
        "isCloze": False,
        "fields": ["Front", "Back", "Extra", "Source", "CardKey"],
        "templates": [{
            "Name": "Card 1",
            "Front": '<div class="q">{{Front}}</div>',
            "Back": BASIC_AFMT,
        }],
    },
    "JV Cloze": {
        "id": 1749200002,
        "isCloze": True,
        "fields": ["Text", "Extra", "Source", "CardKey"],
        "templates": [{
            "Name": "Cloze",
            "Front": '<div class="q">{{cloze:Text}}</div>',
            "Back": ('<div class="q">{{cloze:Text}}</div>'
                     '{{#Extra}}<div class="extra">{{Extra}}</div>{{/Extra}}'
                     '{{#Source}}<div class="src">{{Source}}</div>{{/Source}}'),
        }],
    },
    "JV Visual": {
        "id": 1749200003,
        "isCloze": False,
        "fields": ["Image", "Question", "Back", "Extra", "Source", "CardKey"],
        "templates": [{
            "Name": "Image front",
            "Front": '<div class="q">{{Question}}</div><div>{{Image}}</div>',
            "Back": ('<div class="q">{{Question}}</div><div>{{Image}}</div>'
                     '<div class="a">{{Back}}</div>'
                     '{{#Extra}}<div class="extra">{{Extra}}</div>{{/Extra}}'
                     '{{#Source}}<div class="src">{{Source}}</div>{{/Source}}'),
        }],
    },
}


def genanki_models():
    """Offline fallback: the same three note types as genanki models."""
    import genanki
    out = []
    for name, spec in SPECS.items():
        fields = [{"name": f} for f in spec["fields"]]
        templates = [{"name": t["Name"], "qfmt": t["Front"], "afmt": t["Back"]}
                     for t in spec["templates"]]
        kwargs = dict(model_id=spec["id"], name=name, fields=fields,
                      templates=templates, css=CSS)
        if spec["isCloze"]:
            kwargs["model_type"] = genanki.Model.CLOZE
        out.append(genanki.Model(**kwargs))
    return out

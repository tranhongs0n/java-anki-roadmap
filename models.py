# -*- coding: utf-8 -*-
"""Note-type definitions shared by both push paths.

The CardKey field is the identity of a note: deterministic, hidden from the card,
and searchable from AnkiConnect. It is derived from the fact, not from the wording
of the answer, so editing an explanation updates in place.
"""

CSS = """
/* ---------- palette ---------- */
.card {
  --text: #1f2328; --muted: #57606a; --faint: #8b949e;
  --rule: #d8dee4; --panel: #f6f8fa; --paper: #ffffff;
  --accent: #1f6feb; --accent-soft: #b6d4fe;
  --code-bg: #eef1f5;
  --code-in-panel: #ffffff;
  --kw: #0b58b8; --type: #0e7490; --str: #0a7d32; --num: #6f42c1;
  --cmt: #8b949e; --ann: #8250df; --fn: #0a5c78;
}
.card.nightMode, .night_mode .card {
  --text: #e6edf3; --muted: #9aa4af; --faint: #6e7681;
  --rule: #30363d; --panel: #1c2128; --paper: #0d1117;
  --accent: #79c0ff; --accent-soft: #1f4b86;
  --code-bg: #1b232d;
  --code-in-panel: rgba(255,255,255,.10);
  --kw: #79c0ff; --type: #56d4dd; --str: #a5d6ff; --num: #d2a8ff;
  --cmt: #8b949e; --ann: #d2a8ff; --fn: #d2a8ff;
}

/* ---------- base ---------- */
.card {
  font-family: ui-sans-serif, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial,
               "Noto Sans", sans-serif;
  font-size: 20px;
  line-height: 1.65;
  color: var(--text);
  background: transparent;
  text-align: left;
  max-width: 46rem;
  margin: 0 auto;
  padding: 6px 4px 4px;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}

/* ---------- question ---------- */
.q {
  font-size: 1.14em;
  font-weight: 600;
  letter-spacing: -0.011em;
  line-height: 1.45;
  color: var(--text);
}
.q p { margin: 0 0 .6em; }

/* ---------- answer ---------- */
.a {
  margin-top: 1.05em;
  padding-top: 1.05em;
  border-top: 1px solid var(--rule);
  font-size: 1.02em;
}
.a b, .a strong { color: var(--accent); font-weight: 650; }
.a ul, .extra ul { margin: .45em 0 .15em 1.15em; padding: 0; }
.a li, .extra li { margin: .22em 0; padding-left: .12em; }
.a li::marker, .extra li::marker { color: var(--accent); font-weight: 700; }

/* ---------- context panel ---------- */
.extra {
  margin-top: 1.1em;
  padding: .8em 1em .85em;
  background: var(--panel);
  border-left: 3px solid var(--accent-soft);
  border-radius: 0 10px 10px 0;
  font-size: .84em;
  line-height: 1.6;
  color: var(--muted);
}
.extra b, .extra strong { color: var(--text); }

/* ---------- footer ---------- */
.src {
  margin-top: 1.35em;
  padding-top: .7em;
  border-top: 1px dashed var(--rule);
  font-size: .66em;
  letter-spacing: .01em;
  color: var(--faint);
  word-break: break-word;
}
.src a { color: var(--faint); text-decoration: none; border-bottom: 1px dotted var(--rule); }

/* ---------- code ---------- */
code, pre {
  font-family: ui-monospace, "Cascadia Code", "SF Mono", Consolas, "Liberation Mono", monospace;
  font-size: .84em;
  font-variant-ligatures: none;
}
code {
  background: var(--code-bg);
  padding: .08em .34em;
  border-radius: 4px;
  border: 0;
  white-space: normal;
  overflow-wrap: anywhere;
}
pre {
  background: var(--code-bg);
  border: 1px solid var(--rule);
  border-radius: 10px;
  padding: .9em 1em;
  margin: .9em 0 0;
  overflow-x: auto;
  line-height: 1.5;
  white-space: pre;
}
pre code { background: none; border: 0; padding: 0; white-space: pre; }
.extra code, .src code { background: var(--code-in-panel); }

/* ---------- syntax tokens ---------- */
.kw, .lit { color: var(--kw); font-weight: 600; }
.type     { color: var(--type); }
.fn       { color: var(--fn); }
.str, .chr{ color: var(--str); }
.num      { color: var(--num); }
.cmt      { color: var(--cmt); font-style: italic; }
.ann      { color: var(--ann); }

/* ---------- cloze ---------- */
.cloze {
  font-weight: 700;
  color: var(--accent);
  border-bottom: 2px solid var(--accent-soft);
  padding-bottom: 1px;
}

/* ---------- images ---------- */
img {
  display: block;
  max-width: 100%;
  height: auto;
  margin: 1em auto .4em;
  border-radius: 10px;
  border: 1px solid var(--rule);
  background: var(--paper);
}

/* ---------- tables (rare, but the book cards have a few) ---------- */
table { border-collapse: collapse; margin: .8em 0; font-size: .9em; }
th, td { border: 1px solid var(--rule); padding: .35em .6em; text-align: left; }
th { background: var(--panel); font-weight: 600; }

/* ---------- small screens ---------- */
@media (max-width: 480px) {
  .card { font-size: 18px; padding: 2px; }
  .q { font-size: 1.1em; }
  code, pre { font-size: .8em; }
}
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

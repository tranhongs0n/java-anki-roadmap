# Java Anki roadmap deck

A numbered, nested Anki deck built from [roadmap.sh/java](https://roadmap.sh/java),
plus the pipeline that generates it, the blueprint behind it, and the Hermes skill that
documents the workflow.

Cards are pushed straight into a running Anki through **AnkiConnect** — no `.apkg`
import step. `build.py` remains as an offline fallback.

## Layout

    BLUEPRINT.md        the whole design: deck numbering, card standard, ingestion,
                        image policy, push mechanics, rollout
    make_outline.py     roadmap content → decks.json (1 map deck + 12 sections + 100 decks)
    make_tree.py        re-renders the tree section of BLUEPRINT.md
    make_images.py      draws the diagrams in media/
    cards/*.json        one file per deck (source of truth for the cards)
    media/*.png         images referenced by cards
    push.py             cards + media → Anki (AnkiConnect)
    anki.py             AnkiConnect client (protocol v6)
    models.py           the three note types + shared CSS (Java syntax colours)
    lint.py             hard gate: mandatory self-contained Extra, real source, type tag
    highlight.py        Java tokeniser → span classes, cloze-safe
    build.py            offline fallback → out/Java-Roadmap.apkg
    decks.json          generated deck tree with per-topic resource URLs
    docs.json           scraped roadmap content (titles, summaries, 181 resources)
    probe_all.json      measured extraction results for the 160 article links
    probe_figures.json  measured figure harvest (28/160 pages, 66 usable figures)
    skills/anki-deck-building/   the Hermes skill (see below)

## On the other machine

```bash
git clone https://github.com/tranhongs0n/java-anki-roadmap.git
cd java-anki-roadmap
cp -r skills/anki-deck-building ~/AppData/Local/hermes/skills/productivity/   # Windows
# cp -r skills/anki-deck-building ~/.hermes/skills/productivity/               # macOS/Linux
```

Then continue with the setup below.

## Run it

```bash
python -m pip install genanki pillow httpx trafilatura youtube-transcript-api
```

Anki 2.1.49+ with the **AnkiConnect** add-on (`2055492159`), Anki left running.

```bash
python make_outline.py     # rebuild decks.json from docs.json
python make_images.py      # redraw the diagrams
python push.py --strict    # lint, then add/update notes in Anki
python push.py --dry-run   # show what would change, write nothing
```

`push.py` is idempotent: every note carries a hidden `CardKey` hashed from
`deck|type|prompt`, so re-running updates changed notes in place and never duplicates.
Decks are created automatically, images go through `storeMediaFile`, and CSS changes are
re-applied with `updateModelStyling` on every run.

## Import the skill into Hermes

The skill lives at `skills/anki-deck-building/`. Copy it into the Hermes profile on the
target machine:

    Windows  C:\Users\<you>\AppData\Local\hermes\skills\productivity\anki-deck-building
    macOS    ~/.hermes/skills/productivity/anki-deck-building

It needs `SKILL.md` plus `references/` (course-to-deck mapping, card patterns, pushing to
Anki) and `scripts/java_highlight.py`. Then `skill_view(name='anki-deck-building')` in a
Hermes session picks it up.

## Status

| Level | Deck | Cards |
|---|---|---|
| 0 map | `00 Java Roadmap::00 Big Picture` | 20 |
| 2 detail | `00 Java Roadmap::01-Foundations::02 Basic Syntax` | 11 |

31 notes total, 3 note types, 3 diagrams, pushed and verified in Anki. Next: the ingester
(§4 of the blueprint), then section 01 Foundations.

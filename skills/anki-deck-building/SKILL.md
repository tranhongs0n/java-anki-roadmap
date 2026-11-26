---
name: anki-deck-building
description: Use when turning a roadmap or course into an Anki deck.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [anki, flashcards, spaced-repetition, curriculum, genanki, ankiconnect]
    related_skills: [obsidian, document-to-action-items]
---

# Building Anki decks from a source curriculum

## When to Use

- The user wants flashcards, a deck, or "cards" from a course, roadmap, book chapter or
docs set ("turn roadmap.sh/X into Anki decks", "make me cards for this module").
- An existing deck needs restructuring, re-numbering, new cards, or images.
- Someone is studying with spaced repetition and asks for a study plan keyed to a syllabus.

Not for: note-taking in Obsidian (use `obsidian`), or extracting action items from a
document (use `document-to-action-items`).

The deliverable is a numbered deck tree living in the user's Anki plus the JSON that
regenerates it. Not a pile of cards: a tree, a card standard, a lint gate, a push script.

## Procedure

1. **Pin four decisions before writing a card.** Source (URL / repo), deck depth, card
   language, push path. Default push path is AnkiConnect — the user has said they do not
   want `.apkg` imports. `.apkg` via genanki is the offline fallback only.
2. **Scrape the curriculum into one row per topic** — title, summary, source URL,
   resource links. Never work from memory of a roadmap; the node list changes.
   Recipe: `references/course-to-deck-mapping.md`.
3. **Generate the deck tree programmatically** into `decks.json` (path + topic + sources).
   Hand-typed deck names drift and renumber themselves.
4. **Write top-down**: level-0 map deck → per-section `00 Overview` → topic decks.
5. **Write cards** to the standard in §3, one JSON batch per deck.
6. **Lint, push, read back** (§5) before saying it is done.

## 1. Deck names: numbered, nested, stable

    "00 Java Roadmap::01-Foundations::02 Basic Syntax"

- Anki sorts decks by the full name string, so every level carries a zero-padded
  2-digit prefix; the prefix doubles as study order.
- `::` is the separator and may never appear inside a name. No `/ \ : * ? " < > |`.
  ASCII only — non-ASCII names drift out of numeric order.
- Never renumber. To insert, append `13`, `14`, … Rename only through the Anki browser.
- Three levels is the working maximum (root → section → topic). A 4th only for a topic
  with ≥3 clear subtopics and ≥30 cards; deeper and you stop reviewing a deck and start
  reviewing fragments.
- One leaf deck = one 15–20 min sitting. When a leaf outgrows a sitting (~30 new / ~150
  total), split it into `NN-a` / `NN-b` — split the deck, never drop facts to hit a size.
- Deck options: one preset on the root, `new cards/day = 0` on every parent, unlock only
  the leaf being studied. Otherwise N decks × 20 new cards arrives at once.

## 2. Top-down order (user preference)

| Level | Deck | Cards | Content |
|---|---|---|---|
| 0 map | `00 Big Picture` | 15–20 | what the field is made of, what each area is for, what runs where |
| 1 skeleton | `NN-Section::00 Overview` | 3–5 | what this section covers, what it assumes, what it unlocks |
| 2 detail | `NN-Section::NN Topic` | as many as the topic's facts justify | the facts of one topic |

Map cards are the handles that detailed facts hang on; a fact attached to nothing is
forgotten in a week. Write level 1 the day a section opens, never all 100 decks up front —
a section is "open" only while it is being studied.

## 3. Card standard (non-negotiable)

A card must pass all six gates: **atomic** (one fact, no "and", no comma list),
**unambiguous** (a stranger knows what is asked), **retrievable** (<5 s), **canonical**
(one accepted answer), **contextual** (version/scope pinned), **testable** (checkable
out loud).

Anatomy — exactly these parts:

1. **Prompt** — smallest question that isolates the fact, ≤120 chars.
2. **Answer** — one line; code in `<code>`, ≤2 lines.
3. **Extra** — **mandatory and self-contained**: 1–4 sentences explaining the fact from
   the fetched resource, plus a tiny example or consequence. The user must never need to
   reopen the article. Reject an extra that is empty, under ~60 chars, or that points at a
   source ("see the article", "read more") — that is what `source` is for.
4. **Source** — URL of the roadmap page or the specific article it came from.
5. **Image** — only when the fact is structural (§4).

**Volume is an output, not a target.** A topic gets one card per independent testable
fact in its resources — 4 for a thin topic, 40 for Map or Threads. Never pad to reach a
range and never drop a distinct fact to stay under a cap; both corrupt the deck. The
fixed things are the *unit* (one card = one fact) and the *container* (one deck = one
sitting). A 90-card deck is fine; a 90-card deck you never review is not. Never state a
fixed card range as a requirement — the user rejects it.

**Tags earn their place only if they change study behaviour.** Push `roadmap::`, `sec::`,
`topic::` — they drive filtered decks and per-section stats. Keep the classification
(`type::gotcha`, `type::trace`, …) in the card JSON as build metadata and out of Anki's
tags by default: Anki's scheduler ignores tags, so a type tag costs a decision per card
and buys nothing at review time. Push it only when the user wants practice filtered by
card shape.

Extras never introduce a second testable fact: if it deserves testing, it deserves its
own card. Rewrite patterns, card taxonomy, tag scheme and code-card colouring:
`references/card-patterns.md`.

## 4. Images

Structural facts only (containment, hierarchy, state, layout), target ~25–30 % of cards.
Priority: script-drawn diagram (PIL / Graphviz / Mermaid → PNG) → official docs figure →
screenshot of real output → redrawn article figure, cited. Never stock photos, never a
republished article graphic.

- `media/<topic-slug>-<nn>-<what>.png`, lowercase ASCII; Anki media is global, so the
  prefix prevents collisions.
- 900–1400 px wide, background `#fdfdfd` so it reads in light and dark themes.
- One image per card, parts labelled, referenced by bare filename
  (`<img src="…png">`) — never an absolute path.

## 5. Lint, push, verify

Lint every batch before pushing: missing/short `extra`, pointer phrasing, missing
`source`, missing `type::` tag, answers containing lists. Make it a hard gate (`--strict`
exits non-zero); a warning nobody reads is not a gate.

Push: AnkiConnect by default (`references/pushing-to-anki.md`). Read back counts with
`findNotes` / `notesInfo` before claiming success.

Push verification: run the push twice. The second run must report `0 new, 0 updated` and
every note unchanged — anything else means the identity key or the rendered fields are
unstable. Then read back with `findNotes('deck:"…"')` and `notesInfo` to confirm note
counts, field names and media. Editing one card's text and re-pushing must yield exactly
`1 updated`.

If a `.apkg` is produced anyway, verify by unzipping: `collection.anki2` must open in
sqlite3, `notes`/`cards` counts must match, media map must list every image, and the deck
names must show the full `::` path.

**Colour and layout claims must be measured, not eyeballed.** Render the card HTML in a
browser and read `getComputedStyle(el).color` per token class. A screenshot description
will confidently call green text "orange".

## 6. Ingestion is where it breaks

Fetching the source is the failure-prone step, not card writing. Measured on
roadmap.sh/java (160 article links): 81 % extract cleanly with one generic fetch,
16 % come back thin, 3 % empty, 6 % return 403/429. Failures are mechanisms, not
layouts: expired TLS (jenkov.com — set `verify=False`), bot walls (Stack Overflow,
dzone), JS shells (dev.java index, simplilearn), landing pages mistaken for articles
(spring.io, cucumber.io). Use four tiers — plain fetch + trafilatura → external
renderer → headless browser → give up and fall back to a sibling resource — and keep
per-domain overrides in config, never in code.

Keep text **and** `<pre>` code blocks **and** figure URLs; trafilatura alone flattens
code, which is usually the fact being tested. Filter images hard: inside main content,
≥400 px, has alt/figcaption, ≤3 per page, dedupe by hash.

Video (12 % of roadmap resources): captions via `youtube-transcript-api` return
timestamped segments; join on >2 s pauses and cite `?t=<seconds>` in Extra. Pulling
frames is mostly junk — draw the diagram instead.

Cache raw HTML + extracted text + fetch metadata per topic; that is the evidence you
re-check when a card looks wrong later.

## 7. Reference implementation

The whole pipeline (outline generator, card JSON, lint, Java highlighter, push) lives at
`github.com/tranhongs0n/java-anki-roadmap`, with `BLUEPRINT.md` and this skill. Clone it
when starting from nothing; read `BLUEPRINT.md` before re-deciding the deck scheme, and
treat `cards/*.json` as the source of truth, never the live collection.

Rollout order, measured on that project: level 0 (20 cards) -> one `00 Overview` per
section as that section opens -> leaf decks. 31 notes shipped from 2 leaves before the
ingester existed; the ingester is not a prerequisite for the first decks.

## 8. Pitfalls that cost time

- `genanki.Deck(id, name)` needs an **int** id; `genanki.guid_for()` returns a base91
  string and raises `TypeError: Deck .deck_id must be an integer`. Use
  `sha1(name) & 0x7fffffff` so rebuilds never duplicate decks.
- Note GUID `= guid_for(deck, type, front)` gives the behaviour you want: editing an
  answer updates in place, rewording the prompt forks a new card.
- Cloze cards produce several cards from one note — count notes and cards separately
  when verifying.
- `roadmap.sh` topic pages are not addressable and nodes are SVG; scrape content from
  the GitHub repo instead of the rendered roadmap.
- Code cards: highlight at push time and pass `{{c1::…}}` markers through the tokeniser
  untouched, or Anki shows the braces.
- `pip install genanki pillow` into the interpreter that will run the builder; a stripped
  venv python may have no `pip` at all, so check before writing code against it.
- An AnkiConnect add-on copied into `addons21/<id>/` is **not** loaded by an Anki that is
  already running, and the HTTP server binds 8765 only after a profile window opens.
  Restart Anki, wait for the deck browser, then probe
  `curl -s http://127.0.0.1:8765 -d '{"action":"version","version":6}'` before debugging
  the client.

## Files

    references/course-to-deck-mapping.md   scraping a roadmap/course into decks.json
    references/card-patterns.md            card taxonomy, rewrite patterns, code colouring
    references/pushing-to-anki.md          AnkiConnect + genanki, identity, failure modes
    templates/card-batch.json              deck payload schema (basic / cloze / visual)
    scripts/java_highlight.py              Java tokeniser -> span classes for Anki fields

Sibling skills: a leaf deck that outgrows a review sitting goes through `anki-card-dedupe`;
CSS/template/add-on work goes through `anki-card-styling`; images through
`anki-image-backfill`. Do not re-solve those here.

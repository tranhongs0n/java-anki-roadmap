# Anki blueprint — roadmap.sh/java

A repeatable system for turning roadmap.sh/java into a numbered, nested Anki deck
with one fact per card and a real image on every card that needs one.

Source of truth: the roadmap content files in
https://github.com/nilbuild/developer-roadmap/tree/master/roadmaps/java/content
(88 topic pages, 181 free resources: 138 articles, 21 videos, 19 official docs,
1 course, 1 repo, 1 roadmap). Each `.md` file = one topic = one leaf deck.
Its "Visit the following resources to learn more" list = the Free Resources you fetch
before writing cards.

Everything below is implemented in this folder; see "Files" at the end.

---

## 1. Deck numbering and naming

Anki sorts decks by the full name string, so every level carries a zero-padded
2-digit prefix. The prefix also encodes study order — the tree reads top to bottom
as a curriculum.

    "00 Java Roadmap::01-Foundations::02 Basic Syntax"

Rules (all enforced by make_outline.py):

1. Two digits per level, starting at 01. Order is the roadmap order, not alphabetical.
2. Number and name are joined by a hyphen for the parent levels; leaf names keep a
   space after the number ("02 Basic Syntax"). Pick one style and never mix.
3. `::` is the separator — it may never appear inside a name.
4. ASCII only. No `/ \ : * ? " < > |`, no Vietnamese diacritics, no emoji.
   Anki sorts by byte value; non-ASCII names drift out of numeric order.
5. Names are stable. Never renumber; to insert, append at the end (13, 14, ...).
   Rename only through the Anki browser so cards and review history follow.
6. Leaf names ≤ 35 characters.
7. Three levels is the working maximum: root → section → topic. A 4th level only
   for a topic with ≥3 clear subtopics and ≥30 cards (Collections::Map is the
   realistic candidate). Deeper than that and you stop reviewing "a deck" and
   start reviewing fragments.
8. One leaf deck = one sitting. Card count follows the topic's fact count, but when a
   leaf no longer fits a session (~30 new / ~150 total), split it into `NN-a` / `NN-b`
   — split the deck, do not cut the facts.

Deck options: put all leaves under one preset on the root, then set
`new cards/day = 0` on every section deck and unlock only the leaf you are
currently studying. Otherwise Anki starts feeding you 20 new cards from every
deck at once.

---

## 2. Three levels: map → section skeleton → topic detail

Build and study in this order; never open a detail deck before its two parents exist.

| Level | Deck | Cards | Question it answers |
|---|---|---|---|
| 0 — map | `00 Big Picture` | 15–20 | What is Java made of, where does each area fit, what runs where |
| 1 — skeleton | `NN-Section::00 Overview` | 3–5 | What is inside this section, what does it assume, what does it unlock |
| 2 — detail | `NN-Section::NN Topic` | every fact the topic supports | the facts of one roadmap topic |

Level 0 is written once and reviewed for the whole project. Level 1 is written the
day you start a section — it is the "you are here" note. Level 2 is the actual
studying and the only level that keeps growing.

Why this order works: the map cards are the handles you hang detail on. A fact
attached to "concurrency = shared heap + per-thread stack" survives; the same fact
attached to nothing is forgotten in a week. It also means every session starts by
re-reading the map (2 minutes) and ends one level deeper.

Level 0 content, concretely — 19 cards in `cards/00-00-big-picture.json`:

- platform: JVM vs JDK vs JRE, what makes bytecode portable
- memory: stack vs heap, references, when an object becomes collectable
- landscape: the four bands, and which band each area belongs to
- navigation: which area owns `new`, HashSet, `volatile`, Maven/Spring, logging facades

Level 1 content, rule of thumb: 3–5 cards answering *what this section is for*,
*what it requires first*, *what breaks if you skip it*. Not a table of contents —
navigation cards ("which topic covers X") belong at level 0.

---

## 3. The tree (generated from the real roadmap, not from memory)

```
00 Java Roadmap
├─ 00 Big Picture   (19 cards)
├─ 01 Foundations   (12 decks · 24 resources)
│  ├─ 00 Overview   [overview]
│  ├─ 01 Java Basics   [4 res]
│  ├─ 02 Basic Syntax   [3 res]
│  ├─ 03 Data Types   [2 res]
│  ├─ 04 Conditionals   [3 res]
│  ├─ 05 Arrays   [2 res]
│  ├─ 06 Loops   [1 res]
│  ├─ 07 Variables and Scopes   [2 res]
│  ├─ 08 Type Casting   [2 res]
│  ├─ 09 Strings and Methods   [1 res]
│  ├─ 10 Math Operations   [1 res]
│  └─ 11 Lifecycle of a Program   [3 res]
├─ 02 Object Model   (21 decks · 36 resources)
│  ├─ 00 Overview   [overview]
│  ├─ 01 Classes and Objects   [2 res]
│  ├─ 02 Attributes and Methods   [3 res]
│  ├─ 03 Access Specifiers   [1 res]
│  ├─ 04 Static Keyword   [3 res]
│  ├─ 05 Nested Classes   [2 res]
│  ├─ 06 Basics of OOP   [1 res]
│  ├─ 07 Object Lifecycle   [0 res]
│  ├─ 08 Method Chaining   [1 res]
│  ├─ 09 Enums   [2 res]
│  ├─ 10 Final Keyword   [2 res]
│  ├─ 11 Abstraction   [2 res]
│  ├─ 12 Inheritance   [2 res]
│  ├─ 13 Method Overloading and Overriding   [2 res]
│  ├─ 14 Static vs Dynamic Binding   [2 res]
│  ├─ 15 Interfaces   [2 res]
│  ├─ 16 Encapsulation   [1 res]
│  ├─ 17 Record   [2 res]
│  ├─ 18 Packages   [1 res]
│  ├─ 19 Initializer Block   [3 res]
│  └─ 20 Pass by Value vs Pass by Reference   [2 res]
├─ 03 Language Features   (5 decks · 6 resources)
│  ├─ 00 Overview   [overview]
│  ├─ 01 Exception Handling   [2 res]
│  ├─ 02 Annotations   [1 res]
│  ├─ 03 Lambda Expressions   [1 res]
│  └─ 04 Modules   [2 res]
├─ 04 Collections   (10 decks · 19 resources)
│  ├─ 00 Overview   [overview]
│  ├─ 01 Array vs ArrayList   [2 res]
│  ├─ 02 Set   [2 res]
│  ├─ 03 Map   [4 res]
│  ├─ 04 Queue   [1 res]
│  ├─ 05 Stack   [2 res]
│  ├─ 06 Dequeue   [2 res]
│  ├─ 07 Iterator   [2 res]
│  ├─ 08 Generics   [2 res]
│  └─ 09 Optionals   [2 res]
├─ 05 Functional Programming   (5 decks · 8 resources)
│  ├─ 00 Overview   [overview]
│  ├─ 01 Functional Interfaces   [2 res]
│  ├─ 02 High Order Functions   [1 res]
│  ├─ 03 Functional Composition   [2 res]
│  └─ 04 Streams   [3 res]
├─ 06 Concurrency   (6 decks · 10 resources)
│  ├─ 00 Overview   [overview]
│  ├─ 01 Concurrency   [2 res]
│  ├─ 02 Threads   [2 res]
│  ├─ 03 Virtual Threads   [3 res]
│  ├─ 04 Java Memory Model   [1 res]
│  └─ 05 Volatile Keyword   [2 res]
├─ 07 IO, Network, Data Formats   (7 decks · 14 resources)
│  ├─ 00 Overview   [overview]
│  ├─ 01 I-O Operations   [1 res]
│  ├─ 02 File Operations   [4 res]
│  ├─ 03 Networking in Java   [3 res]
│  ├─ 04 Cryptography   [2 res]
│  ├─ 05 Date and Time   [3 res]
│  └─ 06 Regular Expressions   [1 res]
├─ 08 Persistence   (6 decks · 12 resources)
│  ├─ 00 Overview   [overview]
│  ├─ 01 Database Access   [2 res]
│  ├─ 02 Java JDBC   [1 res]
│  ├─ 03 Spring data jpa   [4 res]
│  ├─ 04 Hibernate   [2 res]
│  └─ 05 Ebean   [3 res]
├─ 09 Build and Frameworks   (11 decks · 22 resources)
│  ├─ 00 Overview   [overview]
│  ├─ 01 Build Tools   [0 res]
│  ├─ 02 Maven   [2 res]
│  ├─ 03 Gradle   [4 res]
│  ├─ 04 Bazel   [3 res]
│  ├─ 05 Dependency Injection   [2 res]
│  ├─ 06 Web Frameworks   [0 res]
│  ├─ 07 Spring Boot   [4 res]
│  ├─ 08 Quarkus   [1 res]
│  ├─ 09 Play Framework   [4 res]
│  └─ 10 Javalin   [2 res]
├─ 10 Testing   (8 decks · 17 resources)
│  ├─ 00 Overview   [overview]
│  ├─ 01 Testing   [2 res]
│  ├─ 02 JUnit   [4 res]
│  ├─ 03 Testng   [2 res]
│  ├─ 04 Rest assured   [3 res]
│  ├─ 05 JMeter   [1 res]
│  ├─ 06 Cucumber JVM   [4 res]
│  └─ 07 Mockito   [1 res]
├─ 11 Logging   (6 decks · 9 resources)
│  ├─ 00 Overview   [overview]
│  ├─ 01 Logging Frameworks   [3 res]
│  ├─ 02 Logback   [1 res]
│  ├─ 03 Log4j2   [2 res]
│  ├─ 04 Slf4j   [1 res]
│  └─ 05 TinyLog   [2 res]
└─ 12 Documentation   (3 decks · 4 resources)
   ├─ 00 Overview   [overview]
   ├─ 01 Documentation   [0 res]
   └─ 02 Javadoc   [4 res]
```

---

## 4. Ingestion — the hard part, measured

Every card rests on a fetched page, and the fetching is where this breaks. I probed all
160 non-video resources in this roadmap (`probe_all.json`, 8 threads, 31 s):

| Result | Count | Share |
|---|---|---|
| clean article text (≥1500 chars) | 130 | 81 % |
| thin (0–1500 chars: hub page, consent wall, JS shell) | 25 | 16 % |
| nothing at all | 5 | 3 % |
| HTTP 403 / 429 on first pass | 10 | 6 % |

Per domain, the failures are not random:

| Source | n | What actually happens |
|---|---|---|
| jenkov.com | 46 | **expired TLS certificate** — every request fails until `verify=False`. After that, 46/46 clean, ~10 k chars each |
| baeldung.com | 30 | fine on article pages; category pages return ~800 chars |
| stackoverflow.com | 4 | **403 to any non-browser client** |
| digitalocean.com | 5 | every URL returns the same 945 chars = a consent/JS shell |
| dev.java (index) | 1 | JS app, 342 bytes; **its subpages are static and fine** |
| cucumber.io, spring.io, slf4j.org, hibernate.org, ebean.io | 6 | landing pages, 300–1600 chars — not teaching content |
| docs.oracle.com, junit.org | 5 | fine but huge (136 k chars for one page) → needs section slicing |
| youtube.com / youtu.be | 21 | no HTML at all — see video below |

So "write a scraper per site" is the wrong instinct: 14 domains cover 80 % of the
resources, and the failures are four specific mechanisms (TLS, bot wall, JS shell,
hub page), not arbitrary layout differences.

### The four tiers

    T0  status/HEAD, robots, content-type
    T1  httpx (verify=False, follow_redirects, browser UA, gzip/br) + trafilatura
    T2  external renderer (web_extract / r.jina.ai) for 403, 429, JS
    T3  headless browser (browser_exec): wait for network idle, then read
        document.querySelector('main, article, .content').innerText
    T4  give up → cache the failure, fall back to a sibling resource or the
        topic's roadmap .md, and record the topic as "source unavailable"

T1 alone gets 81 % and costs milliseconds per page. T2 recovers Stack Overflow, dev.java
and simplilearn (verified: full question + answers, full index, full article). T3 is the
last resort — it needs a real browser session, so it is slow and should be reserved for
pages T2 also loses.

Per-domain overrides are configuration, not code: a small table in `sources.yaml` with
`insecure_tls: [jenkov.com]`, `render: [digitalocean.com, stackoverflow.com]`, and
`hub_only: [cucumber.io, spring.io, slf4j.org]`.

### What to keep from each page

Plain text is not enough — cards about code and diagrams need structure, so extraction
returns three things, not one:

    {"text": "...", "code": [{"lang": "java", "body": "..."}], "figures": [...]}

- **Code**: trafilatura flattens `<pre>`. 111 of 160 pages contain `<pre>` blocks, and the
  code is usually the fact being tested — pull `pre/code` separately from the raw HTML,
  keep language hints from `class="language-java"`.
- **Figures**: 141 of 160 pages contain `<img>`, but most are logos, avatars and ads.
  Keep an image only if it is inside the main content, ≥400 px wide, and has `alt` or a
  `<figcaption>`; cap 3 per article and dedupe by hash. Expect ~10–15 % of images to
  survive, which is exactly the budget §6 wants.
- **Headings**: keep the `h2/h3` outline. It becomes the candidate fact list without an
  extra model call, and it is how you notice a page that has no facts at all.

### Video (21 links, 12 % of resources)

There is no text to extract, but YouTube captions are machine-readable and were working
in both samples (`youtube-transcript-api`, 190 segments / 5.6 k chars and 1 632 segments
/ 47.6 k chars). Pipeline:

1. Parse the id from `watch?v=` or `youtu.be/` — both forms appear in the roadmap.
2. Fetch the transcript in `en`, `en-US`, `en-GB`; fail loudly rather than silently
   inventing content if only auto-translated tracks exist.
3. Join segments into paragraphs on >2 s pauses, keep `start` per paragraph.
4. Facts from video cite `https://youtu.be/<id>?t=<seconds>` so the Extra can say
   "watch from 12:31" — a deep link is the only navigation a flashcard can offer.
5. Slides/screenshots: a frame every N seconds is 95 % junk out of context. Only pull a
   frame when the transcript says "as you can see here" *and* the topic needs a diagram,
   then draw our own instead (§6).

### Cache and reproducibility

    cache/raw/<slug>.html        what the site actually served
    cache/text/<slug>.md         extracted text + code + figure list
    cache/meta/<slug>.json       tier used, status, chars, counts, fetched_at

Re-runs read the cache; refetch only if `fetched_at` is older than 30 days or `--refresh`
is passed. This matters beyond speed: when a card looks wrong six weeks later, the
evidence is on disk, and a re-extract shows whether the site changed or the card did.

**Source URL rule.** A card's `source` is the page the fact was read from — the article
or video URL from the topic's resource list, or the topic's own roadmap `.md` when the
fact comes from the roadmap summary. The bare `https://roadmap.sh/java` is only valid for
map-level cards (which area owns what), because that page is the thing being asked about.
Lint rejects the roadmap root on content cards.

---

## 5. What counts as a good card

A card is good when it forces exactly one retrieval and the answer is either right
or wrong with no room for "kind of". Concretely, it must pass all six gates:

| Gate | Test | Fail example |
|---|---|---|
| Atomic | Back contains one fact, no "and", no comma list | "What are the 4 access modifiers?" |
| Unambiguous | A stranger reading only the front knows what is being asked | "What does this do?" |
| Retrievable | Answerable in < 5 s without scrolling | "Explain the JMM" |
| Canonical | One accepted answer; synonyms are in the extra field | "What's the JVM?" |
| Contextual | Enough scope to pin the meaning (Java version, class, situation) | "What is a record?" |
| Testable | You can say it out loud and check yourself | "Why is Java good?" |

**The card anatomy — exactly these five parts:**

1. **Prompt** — the smallest question that isolates the fact. 1 sentence, ≤ 120 chars.
2. **Answer** — the fact itself. 1 line. Code answers in `<code>`, ≤ 2 lines.
3. **Extra** — optional "why / when / gotcha" or a 1–3 line example. Never new facts
   that belong on their own card; if you need a second fact, make a second card.
4. **Source** — the roadmap topic URL (or the specific article you took it from).
   Lets you re-check and re-generate later.
5. **Image** — only when the fact *is* spatial or structural (see §5). Never decorative.

**What must never be inside a card:** paragraphs copied from an article, "list all X",
two questions joined by "and", version-dependent claims without the version,
personal anecdotes, links the reader must open before answering.

**Rewrite patterns:**

- Enumeration → one card per item, plus one *ordering* card only if order matters.
  Bad: "Name all primitive types." Good: "Which primitive holds a 64-bit integer?"
  and "How many primitive types exist in Java? → 8" (separate cards).
- Comparison → ask for the discriminator, not both definitions.
  Bad: "Difference between ArrayList and LinkedList?" Good: "Which List gives O(1)
  random access but O(n) insert at the head? → ArrayList".
- Definition → ask for the role. Bad: "Define polymorphism." Good: "What lets
  `animal.speak()` run Dog's version when the variable is declared `Animal`? →
  dynamic dispatch (virtual method invocation)".
- Process → one step per card, in `NN` order, never the whole pipeline.
- Gotcha → make the *failure* the answer. "What happens when you modify a List while
  iterating it with a for-each? → ConcurrentModificationException (fail-fast iterator)".

**Card types in this deck** (tag `type::`):

- `definition` — what is X, what is it for
- `syntax` — how is X written (cloze)
- `convention` — naming, style, idiom
- `gotcha` — what breaks and why
- `compare` — pick the right one for a scenario
- `trace` — what does this snippet print / return
- `visual` — image on the front, name the structure it shows (`JV Visual`)
- `mental-model` — why the language is built this way

Target mix per topic: ~40 % definition/syntax, ~25 % gotcha/trace, ~15 % compare,
~10 % mental-model, ~10 % visual.

**Volume is an output, not a target.** A topic gets exactly as many cards as it has
independent testable facts in its resources — a thin topic (Object Lifecycle) may
support 4, a rich one (Collections::Map, Concurrency::Threads) 40. Write until the
facts run out, then stop. Never pad to hit a range and never drop a distinct fact to
stay under a cap; both corrupt the deck's meaning.

What is fixed is the *unit*, not the count: one card = one fact, and one deck = one
sitting. When a topic's facts no longer fit a session (~30 new cards, ~150 total),
split the deck into subtopics (`02a Statements`, `02b Naming`, `02c Literals`) rather
than cramming or trimming. A 90-card deck is fine; a 90-card deck you never review
is not.

---

## 6. Image policy

Cards need images when the fact is spatial — containment, hierarchy, state, layout,
before/after. Target ~25–30 % of cards, i.e. roughly 250 images for the full roadmap.

**Measured first.** I ran a harvester over all 160 article pages (`probe_figures.json`):
trafilatura's main-content pass, then reject `screenshot|icon|logo|avatar|banner|announce|thumb|-small`,
download the rest, reject anything under 400×150, dedupe by sha1.

    160 pages → 28 pages with any usable figure → 66 figures total

That is 0.4 figures per article, and half of those 66 are author photos, hero
illustrations and output screenshots. The Java text tutorials teach with code, not
diagrams: baeldung, tutorialspoint, digitalocean and programiz return zero usable
figures; jenkov returns real ones only in the concurrency series (JMM, thread stacks,
visibility). So harvesting supplies ~6 % of the cards at best, not 25 %.

**Therefore: draw by default, harvest by exception.**

| Case | Action |
|---|---|
| Structure I can draw (JDK layers, collection hierarchy, thread states, stream pipeline, JPA states, GC roots) | script it in `make_images.py` (PIL/Graphviz) — consistent style, no licence question, regenerable |
| A page already has the canonical depiction (jenkov's JMM hardware diagram, programiz deque, bazel's dependency graph) | crop it, annotate what the card asks about, cite the article |
| Real output (stack trace, `jstack`, build log, heap histogram) | screenshot it, crop, keep the exact text |
| Anything else | none — a decorative image makes the card slower, not better |

Harvested figures are evidence, not decoration: crop to the region the card asks about,
label the parts, and keep the source URL in `source`. Never hotlink (the card must work
offline) and never republish a full article figure — redraw when the redraw is cheap.

**Film/video:** no frames. A frame every N seconds is 95 % junk; pull one only when the
transcript says "as you can see here" *and* the topic needs a structure, then draw it.

**Technical rules**

- `media/<topic-slug>-<nn>-<what>.png`, lowercase ASCII; Anki media is global, so the
  prefix prevents collisions.
- PNG, 900–1400 px wide, background `#fdfdfd` so it reads in both themes. Rasterise SVG.
- One image per card: on the front when the image *is* the question (`JV Visual`), in
  `Extra` when it illustrates the answer.
- Dedupe by content hash; the same diagram used by three cards is stored once, but each
  card still shows it only if the fact needs it.

---

## 7. Production loop — one topic at a time

For every leaf deck, in roadmap order:

1. **Fetch the topic page** (`docs.json` already holds all 88 with their resource
   URLs). Read the description paragraph — that's the roadmap's own summary.
2. **Fetch the free resources** (2–3 per topic on average). Read them; do not
   summarise them. Four topics have no resources (Java Basics hub, Build Tools,
   Documentation, Object Lifecycle) — use their child topics or the official docs.
3. **Extract facts into a list**, one line each, no prose: "char literal = single
   quotes", "javac emits bytecode", "8 primitives". If a line has two facts, split it.
4. **Convert each fact into one card** using the §5 gates. Name the type.
5. **Add the image** if the fact is structural (§6); otherwise `extra` only.
6. **Write the JSON file** `cards/<sec>-<topic>-<slug>.json` with `deck` set to the
   exact deck path from `decks.json`.
7. **Push**: `python push.py` → creates the deck, uploads images, adds/updates notes
   through AnkiConnect. Nothing to import, no file to move.
8. **Study it once in Anki**, then rewrite anything that felt slow. Slowness on a card
   is usually two facts, not a hard fact.

Budget: ~20–30 minutes per topic, 3–4 topics per session. 88 topics ≈ 25–30 hours
spread over 8–10 weeks — which is also the study schedule, so never build more than
2 weeks ahead of what you are actually reviewing.

**Per-topic checklist before moving on**

- [ ] every card traceable to a sentence in a fetched resource; no padding, no dropped facts
- [ ] no card with "and"/comma-list in the answer
- [ ] every front answerable in < 5 s
- [ ] ≥ 1 image if the topic is structural
- [ ] `source` filled, `type::` tag on every card
- [ ] deck path matches `decks.json` exactly

---

## 8. Push mechanics — AnkiConnect, no .apkg

Anki must be running with the AnkiConnect add-on (`2055492159`); the client talks to
`POST http://127.0.0.1:8765`, protocol v6. `python push.py` does everything: creates
decks and note types, uploads images, adds new notes, updates changed ones, honours a
lint gate. There is no import step and no file to move between machines.

**Note types** (defined once in `models.py`, shared with the offline fallback)

| Model | Fields | Used for |
|---|---|---|
| `JV Basic` | Front, Back, Extra, Source, **CardKey** | definition, syntax, gotcha, compare, trace |
| `JV Cloze` | Text, Extra, Source, **CardKey** | syntax facts inside a sentence |
| `JV Visual` | Image, Question, Back, Extra, Source, **CardKey** | diagram → name the structure |

`CardKey` is hidden from every template: it exists so a push can find its own notes.

**Identity.** `CardKey = "jv-" + section digits + sha1(deck | type | prompt)[:10]`.
The hash is over the prompt and deck, not the answer, so editing an explanation
updates in place while rewording a question legitimately forks a new card. Lookup is
`findNotes('CardKey:"…"')`: 0 hits → `addNotes`, 1 hit → compare fields →
`updateNoteFields` only if something differs, 2+ hits → report and refuse. No local
state is required; `out/pushed.json` is only a cache.

**Media.** `storeMediaFile` with base64 data, skipped when `getMediaFilesNames`
already has the name. Names are global in Anki, so they carry the topic prefix.

**Styling.** `updateModelStyling` runs on every push — that is how a CSS change (the
Java colour scheme) reaches notes that already exist. Card *templates* are only
touched with `updateModelTemplates`, which is destructive on customised cards, so it
is opt-in (`--templates`) rather than automatic.

**Flags.** `--dry-run` prints deck, keys and media without writing; `--strict` makes
lint fatal; `--only <substr>` limits the run; `--limit N` caps new cards per run;
`--browse` opens the pushed decks in the Anki browser.

**Tags** (hierarchical, filterable, come from the payload)

    roadmap::java  sec::01-foundations  topic::basic-syntax  type::syntax

**What the push never does:** delete decks or notes, rename anything, or touch
scheduling. Idempotency means "the same JSON yields the same collection", not
"the collection is wiped and rebuilt".

Offline fallback (Anki closed, or a laptop you want to carry the deck on):
`python build.py` writes `out/Java-Roadmap.apkg` with the same three models. Verify it
by unzipping — `collection.anki2` in sqlite3, notes/cards counts, media map, full deck
paths — rather than trusting the writer.

---

## 9. QA and rollout

Top-down, so every session starts from the map and ends one level deeper.

| Phase | What you write | Decks | Cards | Gate |
|---|---|---|---|---|
| 0 — map (done) | `00 Big Picture` | 1 | 20 | explain the four bands and stack vs heap without notes |
| 1 — skeleton + detail | 01 Foundations: `00 Overview` + 10 topic decks | 12 | as many as the facts justify (pilot: 11) | 85 % correct on first review of the section |
| 2 | 02 Object Model: overview + 20 topics | 21 | | as above |
| 3 | 03 Language Features + 04 Collections | 15 | | |
| 4 | 05 Functional + 06 Concurrency | 11 | | |
| 5 | 07 IO and Network + 08 Persistence | 13 | | |
| 6 | 09 Build and Frameworks | 11 | | |
| 7 | 10 Testing + 11 Logging + 12 Documentation | 16 | | |

No card target per phase. The gate is comprehension, not volume: a section is done when
you can answer its overview cards cold and its topic cards sit at >85 % on first review.
Sections with little factual content (12 Documentation) stay small; dense ones
(02 Object Model, 04 Collections) will run to several hundred cards, and that is correct.

Rule: a section is "open" only while you are studying it. Finish (or consciously
park) a section before opening the next — 100 decks in flight at once is how decks die.

Within a section, same order: write `00 Overview` first, study it, then topics
01…N in roadmap order, building 2 weeks ahead of your reviews at most.

Quality metrics to watch: cards answered "Again" more than 3× in a row (leech →
rewrite or delete), median answer time > 8 s (split), and any deck where you
suspend more than 10 % (the generation prompt was wrong, fix the source, not the card).

---

## 10. Files

    C:\Users\OF1VNHAN\Desktop\anki-java\
      BLUEPRINT.md            this document
      make_outline.py         roadmap mapping → decks.json (1 map + 12 sections + 100 decks)
      make_tree.py            re-renders the tree in §3 from decks.json
      make_images.py          draws media/jdk-jre-jvm.png, java-landscape.png, stack-heap.png
      push.py                 cards/*.json + media/ → Anki via AnkiConnect (default path)
      anki.py                 AnkiConnect client (protocol v6, readable errors)
      models.py               the three note types + shared CSS (both push paths)
      lint.py                 card gate: mandatory self-contained extra, source, type tag
      highlight.py            Java tokeniser → span classes, cloze-safe
      build.py                offline fallback: cards/*.json → out/Java-Roadmap.apkg
      decks.json              the full numbered tree with per-topic resource URLs
      docs.json               scraped roadmap content (title, summary, 181 resources)
      probe_all.json          measured extraction results for all 160 article links
      probe_figures.json      measured figure harvest: 28/160 pages, 66 usable images
      cards/*.json            one file per deck written so far (2 of 101)
      media/*.png             images referenced by the cards
      out/pushed.json         key → note id cache (not required, safe to delete)
      cache/                  raw + extracted text per topic (to be added with the ingester)
      sources.yaml            per-domain overrides: insecure_tls, render, hub_only

Rebuild everything:

    python make_outline.py && python make_images.py && python push.py --strict

(Python that has `genanki` and `pillow`:
`C:\Users\OF1VNHAN\AppData\Local\hermes\tools\python-3.14.9+20261021-win32-x64\python`)

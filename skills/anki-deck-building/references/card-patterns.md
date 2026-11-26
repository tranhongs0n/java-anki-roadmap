# Card patterns, taxonomy and code styling

## Rewrite patterns

| Bad | Why | Rewrite |
|---|---|---|
| "Name the 4 access modifiers" | one card, four facts | one card per modifier + a separate ordering card if order matters |
| "Difference between ArrayList and LinkedList?" | two definitions, no discriminator | "Which List gives O(1) random access but O(n) insert at the head? → ArrayList" |
| "Define polymorphism" | recalls prose, not a model | "What lets `animal.speak()` run Dog's version when the variable is `Animal`? → dynamic dispatch" |
| "Explain the JVM" | unanswerable in 5 s | "Which component does `javac` target: CPU or JVM?" |
| "What happens with try/catch/finally/close?" | pipeline as one fact | one card per stage, `NN`-prefixed in the extra |

Gotcha cards make the **failure** the answer: "What happens when you modify a List while
iterating it with for-each? → ConcurrentModificationException, fail-fast iterator".

## Taxonomy (tag `type::`)

definition · syntax · convention · gotcha · compare · trace · visual · mental-model ·
navigation (level 0 only: "which area owns X").

Target mix per topic: ~40 % definition/syntax, ~25 % gotcha/trace, ~15 % compare,
~10 % mental-model, ~10 % visual.

## Tags

    roadmap::<name>  sec::01-foundations  topic::basic-syntax  type::gotcha

One hierarchical tag per axis; `type::` is per card, the rest come from the deck payload
so `findNotes 'tag:sec::01-foundations'` can build a filtered deck across leaves.

## Cloze rules

- 1–2 blanks per note, never 3+ on unrelated points.
- Blank the keyword, keep the context: `A {{c1::char}} literal uses single quotes`.
- Never blank a value the extra field also has to explain.

## Extra-writing rules

- Written from the fetched resource, not from memory; if the article does not say it,
the claim does not go in.
- Structure: what it is → why / when it bites → one tiny example.
- No second testable fact; no "see the docs"; no version-less claims ("since 21" is fine).

## Code cards: Java colour scheme

Highlight at push time (`scripts/java_highlight.py`), style with CSS classes on spans:

| class | light (IntelliJ) | dark (VS Code) |
|---|---|---|
| `.kw`, `.lit` | `#0033b3` bold | `#569cd6` |
| `.type` | `#267f99` | `#4ec9b0` |
| `.fn` | `#00627a` | `#dcdcaa` |
| `.str`, `.chr` | `#067d17` | `#ce9178` |
| `.num` | `#1750eb` | `#b5cea8` |
| `.cmt` | `#8c8c8c` italic | `#6a9955` |
| `.ann` | `#9e880d` | `#dcdcaa` |

Rules: `pre` gets `background:#f6f8fa; border-left:3px solid #d0d7de` (dark:
`#252526` / `#3c3c3c`); duplicate every rule under `.nightMode` **and** `.night_mode`
(Anki desktop and mobile use different class names); a capitalised identifier is a type
only when something binding follows it (identifier, `<`, `[`, `(`, `.`), otherwise a short
answer like `Bea` turns into a fake class name.

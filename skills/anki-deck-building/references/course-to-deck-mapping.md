# Scraping a curriculum into a numbered deck tree

Works for any roadmap.sh-style site and any course whose syllabus is a list of pages.
roadmap.sh is the worked case.

## 1. Find the machine-readable source

Do not scrape the rendered roadmap: on the 2026 site the topic nodes are `<g>` elements
inside dozens of lazily-rendered `<svg>` blocks, they expose `data-node-id` and
`data-title` but **not** a URL, and `/java/<slug>` returns 404. Content lives in the repo:

    https://api.github.com/repos/<owner>/developer-roadmap/contents/roadmaps/<topic>/content

Each file is `<slug>@<nodeId>.md` with three useful parts:

    # Title

    One-paragraph description (the site's own summary).

    Visit the following resources to learn more:

    - [@article@Label](https://…)
    - [@video@Label](https://www.youtube.com/…)

Resource kinds seen: `article`, `video`, `official`, `course`, `opensource`, `roadmap`.
Parse with `^- \[@(\w+)@([^\]]+)\]\(([^)]+)\)` per line.

Download with Python `urllib` and the `download_url` from the API listing. `xargs curl`
breaks on these URLs; do one file at a time and skip files already on disk.

## 2. Build the tree, do not hand-write it

Keep a `SECTIONS = [(name, description, [slugs…])]` mapping in the generator script and
emit `decks.json`:

    { deck, deck_path, sections: [ { n, deck, deck_path, desc, topics: [
        { n, deck, deck_path, title, slug, source_md, resources[], n_resources, summary } ] } ] }

Rules:

- Section order = the order the learner meets them, not the repo's file order.
- Number with `enumerate(..., 1)` and `f"{i:02d}"`; leaf name `f"{i:02d} {title}"`.
- Sanitise titles once, in the generator: `" / " -> " vs "`, strip ``\ / : * ? " < > |``.
  Skipping this is how `Pass by Value / Pass by Reference` becomes an illegal deck name.
- Assert the mapping covers every scraped doc and every synthetic deck:
  `set(by_slug) - used` must be empty, and hub pages that are really section headers
  (e.g. an intro page with no subtopics) go in as topic `01`, not as a section.
- Add the level-0 map deck and one `00 Overview` per section as synthetic entries so the
  tree in the plan matches what will exist in Anki.

## 3. Coverage check before writing cards

Report per topic: `n_resources`. Zero-resource topics are usually hub pages or deep
concepts (object lifecycle, build tools) — source them from child topics or official
javadoc instead of inventing content. Median ~2 resources per topic is normal; the
resource list is an input to card writing, never itself a card.

## 4. Volume estimate

`topics × 11` cards for a first pass (6–15 per topic). A 88-topic roadmap ≈ 950 cards ≈
25–30 h of authoring spread over the same weeks as the studying — deliberately never
build more than 2 weeks ahead of what is being reviewed.

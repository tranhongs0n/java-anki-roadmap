# Pushing decks into Anki

Two paths. AnkiConnect is the default for this user; genanki `.apkg` is the offline
fallback (and the only option when Anki is not running).

## AnkiConnect

Prereqs: Anki 2.1.49+, add-on `2055492159`, Anki left running. Endpoint
`POST http://127.0.0.1:8765`, body `{"action": …, "version": 6, "params": {…}}`.
No CORS setup needed from Python.

| action | use |
|---|---|
| `createDeck` | `"A::B::C"` also creates every parent |
| `createModel` | fields, `qfmt`/`afmt`, `css` |
| `modelFieldAdd` | add a field later (e.g. `CardKey`) |
| `updateModelStyling` | push CSS changes; idempotent, run every push |
| `updateModelTemplates` | change card layout (destructive on customised cards) |
| `storeMediaFile` | `filename` + base64 `data` (or `url`/`path`) |
| `addNotes` | batch; returns note ids, `null` where a note was rejected |
| `updateNoteFields` | edit fields by note id, keeps scheduling |
| `findNotes` | query string, e.g. `deck:"…" CardKey:abc` |
| `notesInfo`, `guiBrowse`, `sync` | read back / show user / push to AnkiWeb |

## Note identity is the design decision

`addNotes` takes **no guid** — unlike `.apkg`, nothing survives a rebuild. Options:

1. **Local ledger** (JSON map key → note id). Simple, but lose the file or push from a
   second machine and you get duplicates.
2. **Duplicate detection** (`options: {allowDuplicate: false, duplicateScope: "deck"}`).
   No state, but it keys on the rendered front: reword a prompt and you silently get a
   second card.
3. **Deterministic `CardKey` field** (`topic::slug::n`, hashed from the fact, not the
   wording) + `findNotes` → 0 hits add, 1 hit update, 2+ hits report and stop.

Prefer 3 and add the field before there are notes worth migrating; keep the ledger as an
optional cache. A `type::`-style tag works as a cheap key too, but fields survive
regeneration better than tags.

## Push loop

    for each cards/*.json:
        createDeck(path)                       # no-op when it exists
        ensure models + styling
        for each card:
            highlight code, lint
            storeMediaFile once per image checksum
            findNotes(CardKey) -> addNotes | updateNoteFields
    report added / updated / skipped / rejected(reason)
    optional guiBrowse(changed deck)

Design constraints:

- Fail with "start Anki" on `ConnectionRefused`, not a stack trace.
- `addNotes` returns per-note errors (duplicate, empty first field) — surface them, keep
  the batch going.
- Media names are global in Anki: hash-prefix them, and never delete media blindly.
- Never auto-delete decks or notes; that is not the idempotency anyone wants.
- Offer `--dry-run` that prints deck, note count, media list and keys, and writes nothing.
- Keep `sync` a separate explicit call so an AnkiWeb round-trip cannot hide push errors.

## genanki fallback (.apkg)

- `Deck(id, name)` needs an **int** id. `guid_for()` returns base91 text and raises
  `TypeError: Deck .deck_id must be an integer` — use `int(sha1(name).hexdigest()[:8],16) & 0x7fffffff`.
- Note guid `guid_for(deck, kind, front)` → edits update, rewordings fork.
- `Package(decks).media_files = [paths]`; fields reference the bare filename.
- Modern genanki still writes the legacy v11 collection; Anki imports it fine.

Verify the artifact rather than trusting the writer:

    unzip apkg -> collection.anki2 (sqlite3)
    select count(*) from notes, cards
    select models, decks from col      # JSON blobs: field names, css, full deck paths
    media map JSON must list every image

Cloze notes create several cards per note, so compare notes vs cards instead of asserting
one number.

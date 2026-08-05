---
name: book-atomizer
description: Turn a PDF book into atomic concept notes under docs/booknotes/ — split by the PDF's embedded chapter outline, one chapter per pass, every note born UNTESTED. Never writes docs/wiki/ or FINDINGS.md. Use for a PDF book specifically; for ingesting an already-markdown source into an existing wiki, use karpathy-llm-wiki. Triggers, /book-atomizer, "atomize this book", "extract knowledge from this PDF", "book to notes".
---

# book-atomizer

Turns a PDF book into atomic concept notes. Chapters come from the PDF's own embedded
outline, not from guessing at font sizes.

## The script

Lives beside this file, outside the target repo. `~` does not expand in PowerShell — define
the path once:

```powershell
$BA = "$env:USERPROFILE\.claude\skills\book-atomizer\booknotes.py"   # PowerShell
```

```bash
BA="$HOME/.claude/skills/book-atomizer/booknotes.py"                 # POSIX
```

```
python $BA probe <book.pdf>
python $BA split <book.pdf> [--out DIR] [--split-regex RX] [--force]
python $BA index <vault-dir>
python $BA lint  <vault-dir>
python $BA --demo
```

Requires PyMuPDF. On ImportError it prints `PyMuPDF is required: pip install pymupdf`.

Source of truth is `scripts/book-atomizer/booknotes.py` in the Backtesting repo; this is a
deployed copy. Re-copy after editing there.

## Why the outline and not font sizes

Measured on two real books: Ernie Chan's section headings sit at **1.33×** body size, so the
obvious `1.4` threshold rejects every one of them, while Irene Aldridge's candidate count
barely moves across 1.15–1.5. **No single font-scale default serves both books.** Both PDFs
carry an embedded outline giving chapter titles and page numbers directly, so the heuristic
is unnecessary — it survives only as the no-outline fallback.

The same measurement killed three other guesses: drop caps (19 in Chan, 21 in Aldridge)
would each have become a chapter titled `T`; chapter titles are set across multiple lines and
need joining; and the last chapter absorbs the back matter unless clamped.

## Layout

Paths are relative to the target repo's root (the invocation cwd).

```
docs/booknotes/<book-slug>/
    raw/        chNN-<slug>.md      script output, read-only once written
    notes/      <concept>.md        you write these; RELAY + UNTESTED at birth
    index.md                        written by `index`, never typed
    manifest.json                   chapters, source identity, probe measurements
    plan.md                         the candidate table with its gate cells
    log.md                          append-only
    collision-candidates.md         nominations only
```

Never write `docs/wiki/**` or `FINDINGS.md`. Those are human-gated.

## The adapter

If the target repo has `docs/wiki/CLAUDE.md`, read it, adopt its tag axes, and say in chat
which shape you adopted **before writing the first note**. If that schema puts its tags as
per-claim inline markers, the note carries the page-level default in frontmatter AND every
claim carries its own inline marker — a six-claim note must not end up with one tag.
Otherwise use the template below.

The gate's knowledge-layer globs come from the same schema doc. With no schema, grep the
project's docs root.

## Workflow — six steps, stop between chapters

1. **Probe + split** — `python $BA probe <pdf>`, **eyeball the printed chapter table** (a
   table of contents is the phantom-chapter risk), then `python $BA split <pdf>`.
2. **Plan** — write `plan.md`: a markdown table, one row per candidate,
   `| note-slug | chapter | gate |`. See the gate below.
3. **Atomize** — one chapter per pass. Write `notes/*.md`. Append to `log.md`. Stop.
4. **Index** — `python $BA index <vault>`.
5. **Nominate** — write `collision-candidates.md`: `book claim | note | FINDINGS.md line |
   why it may collide`. Nominations only; promotion into the wiki is a human act.
6. **Lint** — `python $BA lint <vault>` must exit 0. The run is not complete until it does.

`log.md` entries: `## [YYYY-MM-DD] probe|split|atomize|index|lint — <chapter>`

### The gate (step 2)

A candidate becomes a note only if, and the gate cell records which:

- **(a)** it names a term already in the project's knowledge layer. A hit is a
  case-insensitive match of a **two-or-more-word phrase**, or a single term appearing in the
  project's indicator/terminology index or on a status-tagged ledger line. A bare common word
  is not a hit — `grep -i risk` matching a trading book is not evidence of anything. Write it
  as `(a) path/to/file.md:123`. **The path resolves from the directory you run lint in**,
  which is the repo root.
- **(b)** the owner asked for it by name. Write it as `(b) owner YYYY-MM-DD`.

Everything else stays a row in `plan.md` and is written on demand. Lint rule 3 enforces this.

## Note template

Frontmatter keys `provenance`, `verification`, `book`, `chapter` are all required.

```markdown
---
type: concept
title: <Concept>
book: <Book Title>
chapter: <NN — Chapter Title>
provenance: RELAY
verification: UNTESTED
tags: [...]
---

# <Concept>

## What the author says
<Reformulated explanation. Source terminology preserved verbatim; non-English terms
keep the original in parentheses on first use. Quote exactly where the wording is
load-bearing. Numbers quoted from the book go in a blockquote.>

## So what
> [!important]
> <One sentence. Why this matters here.>

## Related
- [[other-note]] — <why this link exists>
```

⚠ **Wikilinks in notes are written bare, never in backticks.** `lint` rule 2 ignores code
spans and fenced blocks (it has to — otherwise it fails on its own documentation), so a
wikilink inside backticks is invisible to the checker and can rot silently. This template
block is safe because `SKILL.md` is never linted.

`provenance: RELAY` is fixed, not a four-way pick: `raw/chNN-*.md` is an artifact we hold and
read, so a note summarising it is a summary of an artifact we could re-open. If the source
PDF goes missing, lint rule 6 fails and **you** rewrite every note to `ORPHAN` — nothing does
that automatically.

`verification: UNTESTED` is written at birth. Only a run on our own data may change it, and
that requires an artifact path.

No date in the template. The pass stamps `log.md`.

## Rules

Lint enforces 2, 3, 4, 5. The rest are yours to keep.

1. Reformulate the *explanation*; never paraphrase away source terminology.
2. Every note carries `book` + `chapter`. Never a line number — line cites drift.
3. Every note has a gate row in `plan.md`.
4. No hand-typed counts **of our own material**. Numbers from the book are quoted, in a
   blockquote, with the chapter cite.
5. Every wikilink resolves and says **why** it exists.
6. Disagreements go to `collision-candidates.md`, one home. Never restated per-note.
7. No running ordinals — every insertion invalidates the rest.
8. Use the code callout **only** when `manifest.has_code` is true.
9. One chapter per pass, stop between. A whole book does not fit in context — Chan's chapter
   1 alone is 93,367 characters.
10. Never write `FINDINGS.md` or `docs/wiki/**`, and never mark a note CONFIRMED.

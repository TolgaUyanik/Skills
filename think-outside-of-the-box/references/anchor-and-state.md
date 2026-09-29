# Anchor, docs, slug, state

## Why this is not automatic

An earlier design resolved the project boundary by walking ancestors for a `docs/` dir
containing `reviews/`. It failed on this machine in four separate ways, and the fixes for
those failures failed too. The reasons are worth keeping, because they are what make the
ask below necessary rather than lazy:

- **`reviews/` is not a project marker.** It is a side-effect of `brutally-honest-review`,
  which hardcodes `docs/reviews/`. Every hit is a scar from a previous review.
- **A git repo is not a project.** `D:/AwakenAnalytics/Skills/` — where this skill's own
  source lives — is a separate git repo with its own GitHub remote and no `CLAUDE.md`, no
  `TODO.md`, no `docs/`, no memory store. There are 28 distinct `.git` roots under
  `D:/AwakenAnalytics`, most of them vendored third-party clones in `AlternativeRepos/`.
  Anchoring to "nearest `.git`" points research at a vendored dependency.
- **"Exactly one `docs/` below the anchor" is false.** `D:/AwakenAnalytics` at depth ≤2 has
  four (`docs`, `Career/docs`, `PandasTa/docs`, `SkillOpt/docs`). `CanariaMarketing` has
  five, three of them at depth 3 and invisible to a depth-2 scan.
- **Recording the answer inside `<docs>` is circular.** If the record of which `docs/` to
  use lives in that `docs/`, a later run cannot find it without already knowing.

So: **ask once, remember globally.**

## Resolution

1. **Look up the recorded answer.** State file:
   `~/.claude/think-outside-of-the-box/state.json`. Match the longest recorded `cwd_prefix`
   that is a prefix of the current cwd. Hit → use its `anchor` and `docs`, print them, done.

2. **No hit → propose and ask.** Gather candidates and show them:
   - anchor candidates: cwd and each ancestor that contains any of `.git`, `CLAUDE.md`,
     `TODO.md` or `docs/`, nearest first, each annotated with which markers it has
   - docs candidates: `docs/` directories at depth ≤3 below the proposed anchor
   Ask one `AskUserQuestion` with up to 4 anchor candidates (plus Other for a typed path).
   Then, if the chosen anchor has more than one `docs/` candidate, ask a second.

3. **Record it** in the state file, keyed by the chosen anchor as `cwd_prefix`, so every
   later run from anywhere inside that tree resolves without asking.

4. `--anchor <path>` overrides and updates the record.

State file shape:

```json
{
  "anchors": [
    { "cwd_prefix": "<project root as the owner named it>",
      "anchor":     "<same, unless --anchor overrode it>",
      "docs":       "<the chosen docs dir — may be nested well below the anchor>",
      "todo":       "<the chosen task file, or null if none>",
      "memory":     "<the matched ~/.claude/projects/<slug>/memory, or null>",
      "recorded":   "<YYYY-MM-DD>" }
  ]
}
```

`todo` and `memory` are recorded here too, for the same reason — both are ambiguous on
this machine (seven `TODO.md` under this tree; four memory stores whose names share the
`d--AwakenAnalytics` prefix) and neither should be re-asked every run.

**A recorded answer is never silently reused across a mismatch.** Print the resolved
anchor and docs on every run. If the owner sees the wrong one, `--anchor` fixes it and
rewrites the record.

## Output tree

```
<docs>/DeepResearch/
  INDEX.md
  prompts/<slug>-prompt.md
  prompts/<slug>-context.md
  prompts/<slug>-coverage.md      # only when the project has no coverage doc of its own
  results/<slug>-result.md
  results/<slug>-critique.md
  results/<slug>-task-drafts.md
```

No dates in filenames — dates live in `INDEX.md`, so a follow-up months later finds its
predecessor without guessing.

## Slug

`lowercase → non-alphanumeric to "-" → collapse repeats → trim → cap 40 chars`.

Then: if the resulting slug already exists in `INDEX.md` **and** its recorded topic text
differs, append `-2`, `-3`. (The 40-char cap does manufacture collisions between long
topics sharing a prefix; this is what catches them.)

Two differently-phrased runs of the same topic ("pairs trading on BIST" / "BIST pairs
trading") produce two different slugs and two separate rows. That is not prevented by the
slug rule and cannot be. It is handled at the other end: **before writing a new row, grep
`INDEX.md`'s topic column for overlapping words and, on a hit, show the existing row and
ask whether this is a follow-up.**

Always echo the slug in the handoff block — `--result --slug S` asks for a string the
owner has seen.

## `INDEX.md`

```
schema: 1

| slug | topic | status | created | updated |
|------|-------|--------|---------|---------|
```

- **slug is the key.** Never the topic.
- topic text escapes `|` as `\|` on write; a reader splits on unescaped `|` only. Topics
  are free text and `|` in one would otherwise mis-column every field after it.
- `status`: `prompt-written` · `result-filed` · `closed-<class>` (a triage refusal is
  recorded too — it is a result).
- Anchor and docs are **not** columns. They live in the global state file, one level up
  from the thing they locate.
- Write by reading the whole file, replacing the one row whose slug matches, and writing
  the whole file back. Leave other rows byte-identical so a git merge conflicts only on a
  genuine same-slug collision.
- If a row does not parse (hand-edited, wrong column count), **stop and show it** rather
  than rewriting the file around it.
- `schema: 1` is read on load. A higher number than this skill knows → stop and say so.
  There is no migration path yet; there is one version.

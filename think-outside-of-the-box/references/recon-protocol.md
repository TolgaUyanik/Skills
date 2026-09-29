# Recon protocol

Four sources, the cold audit, then the owner. Nothing here is hardcoded to a project —
everything resolves from the anchor, and **every failure prints**.

## The four sources

| Source | Resolution | On failure |
|---|---|---|
| project instructions | `<anchor>/CLAUDE.md`, plus any `CLAUDE.md` in ancestors up to the drive root (these nest by design — this is the one source that deliberately reads above the anchor, and it says so) | print "no CLAUDE.md found", continue |
| task file | the `todo` path in the state file; if unset, `<anchor>/TODO.md`, else `find <anchor> -maxdepth 2 -iname 'TODO.md'`; >1 hit → ask once and record it | print "no task file", continue |
| memory | the `memory` path in the state file; if unset, mangle the anchor (`D:\A\B` → `d--A-B`) and match `~/.claude/projects/*` **exactly, case-insensitively** — not as a prefix. On this machine a prefix match for `d--AwakenAnalytics` hits four stores (`-Backtesting`, `-Career`, `-CompanyWebsite`). >1 exact hit or 0 → ask once and record | print "no memory store for `<anchor>`" |
| knowledge graph | `/graphify query "<question>"`, if `<anchor>/graphify-out/graph.json` exists | print "no graph at `<anchor>`, skipped" |

**Never skip silently.** A source that is absent is a line the owner reads, because the
alternative is a run that quietly researched half a project.

> ⚠ **Unproven:** whether one skill can invoke another skill's slash command mid-workflow
> has never been verified here. `/graphify query` is used on that assumption. If it does not
> run, print that it did not — do not fall back to an invented script path. (An earlier
> draft cited `python scripts/utils/graph_query.py`, which does not exist anywhere on this
> disk and would have failed silently forever.)

## The cold audit

Dispatch one fresh read-only `Agent` (`subagent_type: "Explore"`). Isolation is the
delivery mechanism, not the standard — an isolated agent with no rubric opens `CLAUDE.md`,
finds a belief stated as fact, and hands it back as a finding. Ship the rubric.

### Rubric — paste this into the subagent prompt

> A belief written in `CLAUDE.md`, `TODO.md` or a memory file is a **claim, not evidence.**
> Your job is to find what backs it.
>
> Tier every belief you report:
>
> - `MEASURED` — a result file, number or test behind it, cited by file:line
> - `SINGLE-CONFIG` — measured once, at one parameter set
> - `STALE` — measured, but the measurement predates a fix or event the project itself says
>   invalidates it (look for phrases like "suspect until", "re-run required", "superseded")
> - `ASSERTED` — written down, nothing behind it
> - `INHERITED` — carried from an older doc, origin unknown
>
> Cite file:line for every row. No citation found → `ASSERTED`, and say where you looked.
>
> Then list **what the project is NOT doing, and for each one, the reason it is not** —
> quoted from the source, with file:line. If no reason is written anywhere, say
> "no reason recorded" rather than inferring one.

`STALE` exists because a project can carry measured numbers that its own memory declares
suspect — here, every pre-2026-07-06 backtest figure until a re-run. Without that tier a
cold agent files them `MEASURED`, the one tier the owner is told to trust.

> ⚠ **Unproven:** whether one pass is enough. The "unproven / single-config" half requires
> cross-referencing result files, which is far more work than reading stated beliefs. If the
> audit comes back with a long `ASSERTED` list and a thin `SINGLE-CONFIG` list, suspect the
> pass, not the project — and say so in the triage output's `confidence` field.

## The owner interview

Ask in **plain chat text**, not through a picker:

- What do you believe about this, and what is that belief resting on?
- What are you least sure of?
- What would change your mind?
- What constraints do I not know about?

`AskUserQuestion` needs 2-4 pre-written options per question, which would mean guessing the
owner's beliefs in order to ask what they are. Use it only for genuinely closed choices —
anchor selection, docs selection, a yes/no override.

## Constraints — derived, not recited

The pack needs two lists, and neither can be hardcoded into a global skill. Work through
these questions against the anchor's own artifacts, and ask the owner what recon cannot
answer:

**Cost / mechanical** — what does a round trip cost? where does data come from and what are
its limits (history depth, granularity, known contamination)? what currency? what universe?

**Executability** — the ones that silently kill imported findings:
- Can the project take the other side (short, hedge, reverse)?
- What is the finest execution granularity actually available?
- What is frozen, paused or otherwise off-limits right now?
- What data horizon exists for the timeframe being researched?
- What is known to be broken or under re-validation?

Record file:line where a constraint is written down; where it came from the owner, say so.
**Do not invent a trail for something nobody wrote down** — "owner, this session" is an
honest provenance.

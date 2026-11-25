# Auto-run folder templates (Modes B and C)

Run folder: `docs/reviews/auto-YYYY-MM-DD-<runid>/`

## 00-pregate.md (Mode B only, written before any item runs)

```markdown
# Pre-gate — <plan path>

**Date:** <YYYY-MM-DD>
**Outcome:** PROCEED | HALT | ESCALATE (zero LOAD-BEARING rows — extractor
failure)

## Ledger

| id | assumption | tag | status | attack | evidence / check |
|----|------------|-----|--------|--------|------------------|

Joined by `id`: `assumption`/`tag` come from the extractor, `status`/`attack`/
`evidence` from the attacker. Lists every extracted row, incidental rows
included — a row never attacked carries an empty `status`.

## Halting / escalation rows
- **A1** (BROKEN) — <assumption>
  - Attack: <scenario> · Evidence: <file:line>
- **A3** (UNVERIFIED) — <assumption>
  - Settling check: <the one check>
- **A5** (REJECTED or NOT RETURNED, counted UNVERIFIED) — <assumption> · Settling check: re-attack A5
- ESCALATE — zero LOAD-BEARING rows extracted; ledger above holds only
  incidental rows, if any
- (or: none — proceeded)

## Rejected rows
- <id> — <why invalid>
- (or: none)
```

Mode B halts on any LOAD-BEARING row that is BROKEN **or** UNVERIFIED — stricter
than a standalone `--refute`, which only REVISEs on BROKEN. The pre-gate never
enters the REVISE loop.

## 00-manifest.md

```markdown
# Auto run <runid> — <date>

## Tasks
| # | Task id | Source | One-line scope |
|---|---------|--------|----------------|
| 1 | KB-6 | TODO.md:88 | Fill docs/knowledgebase/06-data-quality.md to draft |

## Clarifications (asked ONCE, before execution)
- Q: <question> → A: <user answer>
- (or: none needed)

## Execution map
| Task | Lane | Why |
|------|------|-----|
| KB-6 | parallel subagent (worktree) | doc-only, no scope overlap |
| STAT-1 | main thread | depends on KB-6 verdict |
```

## NN-<task-id>.md (one per task, appended live)

```markdown
# <task-id> — <title>

Task text (verbatim from source) + clarifications that apply.

## Execution log
- <timestamp-ish step>: <what was done, files touched>
- ASSUMPTION: <any mid-run ambiguity + the conservative reading taken>

## Review round 1
<full reviewer output, verbatim — the whole SKILL.md contract>
Open list after step 5: <location — round raised> | none

### Fix log
- Applied: <finding → what was changed, all instances; or `already removed by <what removed it>, <file:line>`>
- Adjusted: <finding → narrower change and why the cite did not hold, or a missed copy edited + the grep used>
- Declined: <finding → why>
- Deferred: <MINOR/NIT not applied in this round>

## Review round 2 ... (up to the round cap)

## Outcome
PASS (round N) | ESCALATED (outstanding findings listed)
```

## 99-summary.md

```markdown
# Run summary — <runid>

| Task | Status | Rounds | Files touched | Follow-ups |
|------|--------|--------|---------------|------------|
| KB-6 | PASS | 2 | docs/knowledgebase/06-data-quality.md | none |
| STAT-1 | ESCALATED | 3 | indicator_engine.py | 2 MAJOR outstanding, see 02-STAT-1.md |

Task-file write-back: <done per convention | skipped (no convention)>
```

Rules: reviewer verdicts always verbatim, never paraphrased. Log lines written
as they happen, not reconstructed. Every ESCALATED row names its blocking
findings file.

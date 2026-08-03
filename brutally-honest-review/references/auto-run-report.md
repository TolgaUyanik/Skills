# Mode C run-folder templates

Run folder: `docs/reviews/auto-YYYY-MM-DD-<runid>/`

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
<full reviewer output, verbatim — VERDICT / FINDINGS / SUMMARY>

### Fixes applied
- <finding → what was changed>

## Review round 2 ... (up to 3)

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

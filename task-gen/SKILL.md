---
name: task-gen
description: Use when the user wants a loose idea, request, brainstorm output, or post-mortem thought turned into a properly-shaped task in the project's task file ("create a task for this", "add this to TODO", /task-gen). Detects the project's task conventions (TODO.md Jira-shape, board tags, plain checklists), interviews the user if the idea is underspecified, auto-wires related-task ties, and writes the task following local discipline. Generator only — never marks tasks done, never deletes.
---

# task-gen

Turn a loose idea into a properly-shaped task in the project's task file, enforcing the local discipline automatically. Works in ANY project.

## What You Must Do When Invoked

### Step 1 — Detect the project's task convention

Look, in order:
1. Project `CLAUDE.md` (and parent CLAUDE.md) for a task-discipline section (e.g. Backtesting's "TODO.md discipline" — that section IS the spec; follow it exactly: `## TAG` heading + `<!--board: ...-->` tag, `> **Goal (user):**` blockquote, `- [ ] **TAG-N — <imperative> (SEVERITY).**` sub-tasks with file:line + acceptance criteria, `⚠` ties line, band placement, unique `pri`, regen command).
2. Else an existing `TODO.md` / `TASKS.md` / `BACKLOG.md` — mirror its dominant shape (heading style, checkbox style, tag prefixes).
3. Else: plain markdown checklist appended to `TODO.md` (create it), one `## <TAG>` heading + `- [ ]` items with acceptance criteria.

Never invent a richer format than the project uses; never write a poorer one than its spec demands.

### Step 2 — Interview if underspecified (grill-lite)

If ANY of these are missing from the user's ask, ask 2-4 sharp questions in ONE AskUserQuestion round BEFORE writing:
- Goal in the user's framing (the WHY — becomes the Goal blockquote verbatim, not paraphrased into assistant-speak)
- Acceptance criterion ("done" looks like what — a number, a file, a passing check?)
- Dependencies / ordering (blocked by what? blocks what?)
- Severity/priority if the convention requires one

If the idea is already complete (goal + done + scope inferable), skip the interview — do not ask ceremonial questions.

### Step 3 — Auto-wire context (anti-duplicate)

Before writing, search the project for related work:
- Grep task file(s) + `FINDINGS.md` + `CompletedTasks.md` (if present) for overlapping keywords/tags.
- If a related or duplicate initiative exists: say so, propose extending it (new TAG-N sub-item under the existing heading) instead of a new section. A duplicate initiative is a bug — this step exists because merges are painful later.
- Wire what you find into the task's `⚠` ties line: related tags, `docs/` pointers, `[[memory-links]]`, honesty gates that apply (e.g. data-integrity checklists, review-gate requirements).

### Step 4 — Write the task

- New initiative → new `## TAG` section in the correct band (ACTIVE only if genuinely next-up; else BACKLOG), with every element the convention demands.
- Extension → new `- [ ] **TAG-N**` sub-item under the existing section.
- Complex build (multi-file, design ambiguity) → first sub-task is `TAG-0 Brainstorm + design FIRST` per the convention.
- Tag choice: short, stable, ALL-CAPS, not colliding with existing tags (grep first).
- Run the project's post-write hooks if the convention names them (e.g. `python scripts/utils/gen_board.py --selfcheck` then regen).

### Step 5 — Report

Print: the task block as written (verbatim), where it landed (file:line, band), what ties were wired, and any related tasks found. If hooks ran, show their output.

## Hard rules

- **Generator only.** Never mark anything done, never move bands, never delete or edit existing tasks (except appending sub-items to a section the user agreed to extend).
- Goal blockquote stays in the USER's words — quote their framing, don't launder it.
- Every sub-task carries an acceptance criterion. No bare one-liners.
- If the convention can't be satisfied (e.g. selfcheck fails on pri collision), fix the collision per the convention's rules and say so — don't leave the file broken.

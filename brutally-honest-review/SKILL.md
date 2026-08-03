---
name: brutally-honest-review
description: Use when the user wants a brutally honest, independent review of Claude's work (code, specs, or analysis), types /brutally-honest-review, wants hands-off "mindless" plan execution gated by a relentless reviewer, or wants a SET of TODO tasks executed hands-off with review gating (--auto with task tags). Dispatches a fresh read-only subagent (the "third eye") with a Terence Fletcher persona that returns a PASS/REVISE verdict plus concrete fixes. Three modes: standalone reviewer, auto/mindless plan loop, and batch task execution. No external LLM.
---

# Brutally Honest Review

An independent reviewer that holds Claude's work to a brutal standard. The
reviewer is the demanding instructor Terence Fletcher: no praise, no
participation trophies — but every barb is bolted to a concrete fix. The point
is always "make this better".

## Why a subagent (the third eye)

Every review runs in a FRESH `Agent` subagent (read-only), never in the main
conversation. A separate context is the whole point: Claude reviewing its own
work in-context rubber-stamps it. An isolated subagent with no attachment to
the work reviews honestly. This is why NO external LLM is needed — the context
isolation IS the objectivity.

## Mode routing

Parse the invocation:

- Contains `--auto` and the argument is a plan/spec file path → **Mode B: Mindless mode**.
- Contains `--auto` and the argument is one or more TASK references (TODO tags
  like `KB-6 STAT-1`, a free-form task list, or `top-N` from a board) → **Mode C:
  Batch task execution**.
- `--auto` with an ambiguous argument → ask ONE question: "plan file or task set?"
- Otherwise → **Mode A: Standalone reviewer**.

Flags:
- `--fletcher` → load `references/fletcher-persona.md` and use full theatrics.
  (Mode B turns this on automatically.)

## The reviewer contract

Every dispatched reviewer MUST return exactly this shape (see
`references/rubric.md` for the rubric and report template):

```
VERDICT: PASS | REVISE
FINDINGS:
  - severity: CRITICAL | MAJOR | MINOR | NIT
    location: <file:line or section>
    problem:  <what is wrong>
    fix:      <concrete, actionable correction>
SUMMARY: <one-paragraph brutal verdict>
```

Gate rule: any CRITICAL or MAJOR finding → REVISE. Clean, or only MINOR/NIT → PASS.

## Mode A: Standalone reviewer

Invocation: `/brutally-honest-review [target] [--fletcher]`

1. **Resolve the target.**
   - If an argument is given, the target is that file / directory / spec.
   - If no argument, the target is the files Claude touched this session
     (recent edits and outputs). List them explicitly before reviewing.
2. **Detect the target type** (code / design / text) per `references/rubric.md`.
3. **Build the reviewer prompt.** Concatenate:
   - The persona block: brutal-but-clean by default; if `--fletcher`, prepend
     the full contents of `references/fletcher-persona.md`.
   - The matching rubric dimensions + severity definitions + gate rule from
     `references/rubric.md`.
   - The strict output contract (VERDICT / FINDINGS / SUMMARY).
   - An explicit instruction: "You ONLY review. Do NOT edit or fix anything.
     Read the target and return the contract."
   - The target: file paths to read (the subagent reads them itself).
4. **Dispatch the reviewer** with the `Agent` tool, `subagent_type: "Explore"`
   (read-only). The subagent reads the target and returns the contract text.
5. **Parse the VERDICT line.**
6. **Output:**
   - Print inline: the VERDICT and the SUMMARY, plus a one-line count of
     findings by severity.
   - Write the full report to `docs/reviews/YYYY-MM-DD-<topic>-review.md`
     (cwd-relative; create `docs/reviews/` if missing) using the report
     template in `references/rubric.md`. Point to the file path in chat.
7. **Do not auto-fix.** Mode A is advisory; the user decides what to act on.

## Mode B: Mindless mode

Invocation: `/brutally-honest-review --auto [plan-path]`

Fire-and-forget. After the user has a spec + plan, this drives the whole plan
to completion, gating every item with the Fletcher reviewer. `--fletcher`
theatrics are ON automatically.

**Setup:** Read the spec + plan (the "first guidance"). Build a todo list with
one entry per plan item/phase. This rides on top of `executing-plans` — use its
rhythm for doing the work.

**Per item, loop:**

1. **Implement** the item on the main thread (normal execution per the plan).
2. **Gate:** dispatch a Fletcher reviewer subagent (same dispatch as Mode A,
   Steps 3-5) against the item's output. `--fletcher` ON.
3. **Branch on VERDICT:**
   - **PASS** → write the item's report to `docs/reviews/`, mark the todo done,
     advance to the next item.
   - **REVISE** → apply every finding's `fix:` on the main thread, increment the
     item's round counter, re-dispatch the reviewer. Repeat.
4. **Round cap:** at most **3** REVISE rounds per item. The round count is
   tracked in the todo list (in-context) — no state file.
5. **Escalate:** if still REVISE after round 3 → STOP the loop. Write the report
   with all outstanding findings, then ping the user with the item name, the
   blocking findings, and what was tried. Do not proceed to later items until
   the user responds.

**On completion:** when every item PASSes, report the run summary (items, total
rounds, where the reports live).

## Mode C: Batch task execution

Invocation: `/brutally-honest-review --auto <task refs>`
(e.g. `--auto KB-6 STAT-1`, `--auto "fix the loader, update the docs"`, `--auto top-3`)

Executes a SET of tasks hands-off, each gated by the Fletcher reviewer.
`--fletcher` ON automatically. The run is reconstructable from its report
folder alone — someone who never saw the chat must be able to follow it.

### Phase 1 — Select

1. Resolve task refs. Tags (`KB-6`) → look up the matching task block in the
   project's `TODO.md` (or equivalent task file); `top-N` → take the N
   highest-priority actionable items from the project board/task file;
   free-form list → take as given.
2. Print the resolved task list (id, one-line scope, source line) and the
   run folder path that will be used.

### Phase 2 — Clarify (ONCE, batched)

3. For each task, check: is the goal, scope, and "done" criterion actionable
   as written? Collect ALL gaps across ALL tasks.
4. If any gaps: ask them in ONE batched AskUserQuestion round (small, concrete
   questions only). **This is the only point questions are allowed.** After
   answers, execution is hands-off — a mid-run ambiguity is resolved by the
   most conservative reading and logged as an ASSUMPTION in the task log,
   never by asking. Tiebreak for "conservative": the reading with the SMALLER
   scope/blast radius wins.
5. Record questions + answers (or "none needed") in `00-manifest.md`.

### Phase 3 — Plan execution (parallel map)

6. Classify each task's file scope. Tasks with NON-overlapping scopes and no
   ordering dependency → eligible for parallel subagents (use worktree
   isolation when two parallel tasks both edit files). Overlapping scope,
   sequential dependency, or work needing main-context judgment → main thread,
   in dependency order.
7. Write the execution map (task → parallel-subagent | main-thread, and why)
   into `00-manifest.md` before starting.

### Phase 4 — Execute + gate (per task)

8. **Implement** — on the assigned lane. Subagent lanes get a self-contained
   prompt (task text, clarifications, file scope, done criterion) and return
   a summary of what they changed.
9. **Gate** — dispatch a Fletcher reviewer (same dispatch as Mode A steps 3-5)
   against the task's output. The gate is NEVER skipped in Mode C — hands-off
   only works because the third eye is always on. Parallel-lane outputs are
   reviewed the same as main-thread outputs.
10. **Branch on VERDICT:** PASS → log + mark done. REVISE → apply every fix,
    re-dispatch. Cap: 3 REVISE rounds.
11. **On cap:** mark the task ESCALATED with its outstanding findings and
    **continue with the remaining tasks** (unlike Mode B's halt — a batch
    should not die on one member). All escalations surface in the final
    summary.
12. Append each step (implementation summary, every review verdict verbatim,
    fixes applied, assumptions made) to the task's log file as it happens —
    not reconstructed at the end.

### Phase 5 — Report + write-back

13. Run folder: `docs/reviews/auto-YYYY-MM-DD-<runid>/` (cwd-relative; runid =
    short slug). Contents per `references/auto-run-report.md`:
    `00-manifest.md` (tasks, clarifications, execution map),
    `NN-<task-id>.md` per task (log + review rounds), `99-summary.md`
    (table: task | status PASS/ESCALATED | rounds | files touched | follow-ups).
14. If the project's task file has a status convention (e.g. `- [x]` +
    inline OUTCOME), write completed tasks back following THAT convention;
    escalated tasks: partially done → `- [~]` + pointer to the run folder;
    untouched (stopped before any work) → leave the checkbox as-is, only add
    the pointer. No convention detectable → leave the task file alone and say
    so in the summary.
15. Print inline: the summary table + run folder path.

### Hard limits (all modes' rules apply, plus)

- **Destructive/irreversible actions are out of auto scope.** A task step that
  requires force-push, deleting data, deploying, or publishing externally →
  STOP that task, mark ESCALATED("needs user"), continue the rest. No
  exceptions, including "the task explicitly says to". A task MIXING safe and
  destructive steps: the safe steps may run, but stop at the FIRST destructive
  step (never reorder to squeeze more in) — log exactly where it stopped.
  Phase 2 questions may ask the user to pre-authorize a specific named
  destructive step; without an explicit yes recorded in the manifest, it stays
  out of scope.
- No new questions after Phase 2. No skipping the gate "because the change is
  trivial". No summarizing reviewer verdicts — quote them.

---
name: brutally-honest-review
description: Use when the user wants a brutally honest, independent review of Claude's work (code, specs, or analysis), types /brutally-honest-review, wants a plan, spec, or argument attacked for a solid evidenced reason it will fail (--refute), wants hands-off "mindless" plan execution gated by a relentless reviewer, or wants a SET of TODO tasks executed hands-off with review gating (--auto with task tags). Dispatches fresh read-only subagents (the "third eye") with a Terence Fletcher persona that return a PASS/REVISE verdict plus concrete fixes. Four modes: standalone review, refutation by assumption-attack, auto/mindless plan loop, and batch task execution. No external LLM.
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

- Contains `--refute` WITHOUT `--auto` → **Mode D: Refutation**, standalone, on
  the given target.
- Contains `--refute` WITH `--auto` → no special behaviour. In Mode B the
  pre-gate is unconditional, so the flag is redundant there: accept it silently
  rather than erroring, and do NOT run refutation twice. In Mode C there is no
  pre-gate at all, so the flag has no effect — say so once, in one line, so a
  user who explicitly asked for refutation is told they did not get it.
- Contains `--auto` and the argument is a plan/spec file path → **Mode B: Mindless mode**.
- Contains `--auto` and the argument is one or more TASK references (TODO tags
  like `KB-6 STAT-1`, a free-form task list, or `top-N` from a board) → **Mode C:
  Batch task execution**.
- `--auto` with an ambiguous argument → ask ONE question: "plan file or task set?"
- Otherwise → **Mode A: Standalone reviewer**.

Flags:
- `--fletcher` → load `references/fletcher-persona.md` and use full theatrics.
  (Mode B turns this on automatically.)
- `--refute` → Mode D. See `references/refutation.md`. Fletcher theatrics are ON
  automatically, and are confined to `attack:` prose and SUMMARY.

## The reviewer contract

Every reviewer dispatched by Modes A, B, and C MUST return exactly this shape.
Mode D's agents return the ledger shapes in `references/refutation.md` instead.
(See `references/rubric.md` for the rubric and report template.)

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
   - **The original user ask, verbatim**, and **an explicit list of file paths**.
     On a no-argument invocation, resolve "files touched this session" in step 1
     and pass that list. The reviewer is never told to work out its own target.
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

**Step 0 — pre-gate the plan (UNCONDITIONAL).** Every Mode B run pre-gates; no
flag required. Before any code is written, run **Mode D steps 1-4** against the
plan itself — extract, zero-check, attack, validate — then apply the rule
below to the VALIDATED ledger. Validation is Mode D step 4, not a phase: skip
it and an unevidenced BROKEN row halts a whole unattended run.

- Zero LOAD-BEARING rows → ESCALATE to the user (Mode D step 2). Do not proceed
  and do not emit a verdict. Zero rows is an extractor failure, NOT "all HOLDS".
- Any LOAD-BEARING row returning **BROKEN or UNVERIFIED** → HALT. Ping the user
  with the assumption, the attack, the `evidence:` behind a BROKEN row, and
  (for UNVERIFIED) the settling check.
- All HOLDS → proceed to the per-item loop.

The pre-gate **does not enter the 3-round REVISE loop.** A broken premise in the
plan is not something the executor can fix by editing its own output — the plan
itself is wrong, and only the user can decide what replaces it. Halt, report,
wait.

Write the pre-gate ledger to
`docs/reviews/auto-YYYY-MM-DD-<runid>/00-pregate.md` — runid = a short slug of
the plan filename — using the `00-pregate.md` template in
`references/auto-run-report.md`, before halting or proceeding, so the decision
is on disk either way. That directory is Mode B's run folder: the per-item
reports written in the loop below go there too.

**Per item, loop:**

1. **Implement** the item on the main thread (normal execution per the plan).
2. **Gate:** dispatch a Fletcher reviewer subagent (same dispatch as
   Mode A, Steps 3-5) against the item's output. `--fletcher` ON. The report
   goes to this run's folder (`docs/reviews/auto-YYYY-MM-DD-<runid>/`),
   never Mode A's flat `docs/reviews/YYYY-MM-DD-<topic>-review.md` path.
3. **Branch on VERDICT:**
   - **PASS** → write the item's report to the step-0 run folder
     (`docs/reviews/auto-YYYY-MM-DD-<runid>/`), mark the todo done, advance to
     the next item.
   - **REVISE** → apply every finding's `fix:` on the main thread, increment the
     item's round counter, then re-dispatch the reviewer. Repeat.
4. **Round cap:** at most **3** REVISE rounds per item. The round count is
   tracked in the todo list (in-context) — no state file.
5. **Escalate:** if still REVISE after round 3 → STOP the loop. Write the
   report to the step-0 run folder (`docs/reviews/auto-YYYY-MM-DD-<runid>/`)
   with all outstanding findings, then ping the user with the item name, the
   blocking findings, and what was tried. Do not proceed to later items
   until the user responds.

**On completion:** when every item PASSes, report the run summary (items, total
rounds, where the reports live).

## Mode C: Batch task execution

Invocation: `/brutally-honest-review --auto <task refs>`
(e.g. `--auto KB-6 STAT-1`, `--auto "fix the loader, update the docs"`, `--auto top-3`)

Executes a SET of tasks hands-off, each gated by the Fletcher reviewer.
`--fletcher` ON automatically. The run is reconstructable from its report
folder alone — someone who never saw the chat must be able to follow it.
**No pre-gate in Mode C.** Mode C resolves TODO references, which are tasks, not
plans carrying load-bearing reasoning. The absence is deliberate, not an
oversight.

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

8. **Implement** — on the assigned lane. Subagent lanes get a
   self-contained prompt (task text, clarifications, file scope, done
   criterion) and return a summary of what they changed.
9. **Gate** — dispatch a Fletcher reviewer subagent (same dispatch as
   Mode A steps 3-5) against the task's output. The gate is NEVER skipped
   in Mode C — hands-off only works because the third eye is always on.
   Parallel-lane outputs are reviewed the same as main-thread outputs.
   The report goes into this task's `NN-<task-id>.md` in the run folder
   (Phase 5), not Mode A's flat path.
10. **Branch on VERDICT:** PASS → log + mark done. REVISE → apply every fix,
    then re-dispatch. Cap: 3 REVISE rounds.
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

## Mode D: Refutation

Invocation: `/brutally-honest-review --refute [target]`

Finds a solid reason the target FAILS, by locating the failure rather than
asserting it. Reuses the PASS/REVISE verdict vocabulary, so nothing downstream
needs a new verdict type — except the zero-LOAD-BEARING path (step 2), which
escalates and emits no verdict at all. Full rules, prompts, and the report
template live in `references/refutation.md`.

**Target:** any target; resolve it as in Mode A step 1 (the given argument, or
the files Claude touched this session, listed explicitly). Against a plan or
spec, the assumptions are the premises the plan rests on. Against code, they
are what the code assumes about its inputs, environment, invariants, and
callers. Same ledger, same solidity bar, no target-type routing.

**Persona:** Fletcher theatrics ON, always. They live in `attack:` prose and
SUMMARY only — `status:` is structure and is immune to voice.

1. **Phase 1 — extract.** Dispatch ONE extractor subagent (`Explore`) with the
   Phase 1 prompt from `references/refutation.md`, the target paths, and the
   original user ask verbatim. It returns the ASSUMPTIONS ledger, each row
   tagged LOAD-BEARING or incidental.
2. **Zero LOAD-BEARING rows → ESCALATE.** This is not a PASS. A target with no
   load-bearing assumptions does not exist, so zero means the extractor failed.
   Stop, tell the user, do not emit a verdict.
3. **Phase 2 — attack.** Split the LOAD-BEARING rows: `ceil(n / 3)` per
   attacker, max 3 attackers, min 1. Dispatch them ALL IN ONE MESSAGE
   (`Explore`), each built from the Phase 2 "Prompt contents" list in
   `references/refutation.md`: the persona, the target paths and the original
   user ask, ONLY its own rows, the solidity bar, and the evidence bound —
   target, files the target references, ONE repo grep sweep. Attackers may NOT
   invent assumptions.
4. **Validate the returned rows.** A row whose `id` was not in the set handed
   to that attacker → reject. BROKEN whose `evidence:` is missing, does not
   resolve, or does not support the `attack:` → downgrade to UNVERIFIED.
   UNVERIFIED without `check:` → reject the row and record it under "Rejected
   rows". The main thread applies the solidity bar; it never re-writes an
   `attack:`.
5. **Verdict.** Any LOAD-BEARING BROKEN → REVISE. Otherwise PASS — including
   when LOAD-BEARING rows are UNVERIFIED, which are reported but do not block a
   standalone run. (Mode B's pre-gate applies a stricter rule; see Mode B
   step 0.)
6. **Output.** Print the verdict, the count by status, and every BROKEN row
   inline. Write the full ledger to
   `docs/reviews/YYYY-MM-DD-<topic>-refutation.md` using the report template in
   `references/refutation.md`.
7. **Do not auto-fix.** Like Mode A, standalone Mode D is advisory.

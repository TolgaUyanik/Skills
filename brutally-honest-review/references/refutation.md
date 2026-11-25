# Refutation Mode (Mode D) — the assumption ledger

Mode D finds a solid reason the target fails by LOCATING the failure, not by
asserting it. Two phases, both dispatched as read-only `Explore` subagents.

## Phase 1 — extractor (exactly 1 agent)

Prompt contents:
- The Fletcher persona (always on in Mode D).
- The target file paths, and the original user ask verbatim.
- This instruction:

  "List every assumption this target rests on. An assumption is something that
  must be TRUE for the target to work, but which the target does not itself
  prove. Tag each row LOAD-BEARING (the target FAILS if this is false) or
  incidental (the target merely degrades or is inelegant if this is false).
  Do NOT attack them. Do NOT propose fixes. Extract only."

Round N ≥ 2 (SKILL.md Mode D step 7): the extractor gets the diff since round N-1 and the existing ledger, extracts only assumptions the changed lines add, and numbers them from the next free id.

Output shape:

```
ASSUMPTIONS:
  - id: A1
    tag: LOAD-BEARING | incidental
    assumption: <what must be true>
    rests_on: <the section or line of the target that needs it>
```

**Zero LOAD-BEARING rows in round 1 is NOT a pass.** A target with no load-bearing assumptions does not exist, so zero in round 1 means the extractor failed. ESCALATE to the user; do not proceed to Phase 2 and do not emit a verdict. In round N ≥ 2 the extractor extracts only from the diff, so zero new rows is expected: proceed to Phase 2 with the rows SKILL.md Mode D step 7 re-attacks. A reply with no `ASSUMPTIONS:` block is not zero rows: re-dispatch once; if still missing, ESCALATE as in round 1.

## Phase 2 — attackers (parallel, LOAD-BEARING rows only)

Split: `ceil(n / 3)` assumptions per attacker, at most 3 attackers, at least 1.
For n <= 3, one assumption per agent. Dispatch all attackers in ONE message.

Prompt contents (one prompt per attacker):
- The Fletcher persona (always on in Mode D). The attackers write the `attack:`
  prose, so this is where the theatrics live.
- The target file paths, and the original user ask verbatim. An attacker is
  never told to work out its own target.
- ONLY this attacker's assigned rows (id, tag, assumption, rests_on).
- Round N ≥ 2: each row's previous `attack:` and `evidence:`/`check:`, and the diff since round N-1. The attack re-tests the previous scenario first.
- The solidity bar and the evidence bound below.
- The output shape below, and the instruction to return that and nothing else.

**The attacker may NOT invent assumptions.** It attacks only the rows it was
handed. This is what stops the mode degenerating into a pile of what-ifs.

**Evidence search is bounded:** the target, the files the target references, and
ONE grep sweep of the repo — a single pattern set run once, not an iterative
hunt that refines patterns against what the last one returned. An attacker that
wanders is slower than the serial reviewer it replaced.

Output shape:

```
LEDGER:
  - id: A1
    status: BROKEN | UNVERIFIED | HOLDS
    attack:   <the scenario in which the assumption is false>
    evidence: <file:line or command output — REQUIRED for BROKEN>
    check:    <the one check that would settle it — REQUIRED for UNVERIFIED>
```

## Solidity bar

| Status | Requires |
|---|---|
| **BROKEN** | a concrete scenario where the assumption is false, PLUS evidence from the target or the repo. Speculation is not BROKEN. |
| **UNVERIFIED** | a plausible attack with no evidence behind it. Must name the ONE check that would settle it. |
| **HOLDS** | attacked, and survived. |

Before the two passes, the main thread checks provenance: any returned row
whose `id` is not in the set handed to that attacker is **rejected** and logged
under "Rejected rows". This is what enforces "may NOT invent assumptions".

Validation, applied by the main thread on return, as an ordered TWO-PASS
pipeline. Pass 2 reads the status pass 1 produced, not the attacker's original
status:

1. A `BROKEN` row with no `evidence:` value is invalid — **downgrade it to
   UNVERIFIED**. The main thread opens each `evidence:` citation. A citation
   that does not resolve, or that does not support the `attack:`, fails pass 1
   and the row is downgraded to UNVERIFIED. `n/a`, `none`, and bare prose are
   not evidence.
2. Any row whose status is `UNVERIFIED` — including one just downgraded by
   pass 1 — with no `check:` value is invalid: **reject the row** and note the
   rejection in the report.

So a row arriving `BROKEN` with neither `evidence:` nor `check:` is downgraded,
then rejected, and appears under "Rejected rows". It is never silently kept.

An attacker that returns nothing, or skips a row it was handed, is re-dispatched once for those rows. A LOAD-BEARING row that is rejected here, or still not returned, counts as UNVERIFIED for the verdict, with the settling check 're-attack <id>'. It is still listed under Rejected rows. Round N ≥ 2: a row that was BROKEN in round N-1 and is rejected or still not returned stays BROKEN, with its previous `evidence:`.

## Persona guard

Fletcher theatrics are ALWAYS ON in Mode D. They live in `attack:` prose and in
SUMMARY — never anywhere else. The `status` column is STRUCTURE and is immune to
voice: a loudly written row is not thereby a BROKEN row. Status is set by the
solidity bar alone. Without this guard, rhetoric passes for evidence, which is
the exact failure this mode exists to catch.

## Verdict

| Condition | Standalone `--refute` | Mode B pre-gate |
|---|---|---|
| any LOAD-BEARING BROKEN | REVISE | HALT + ping user |
| any LOAD-BEARING UNVERIFIED | PASS (reported, not blocking) | HALT + ping user, quoting the settling check |
| all HOLDS | PASS | proceed |

The asymmetry is deliberate. Before spending hours executing a plan, verifying a
load-bearing assumption is cheap. A standalone document review that blocked on
every unverified premise would never PASS, and would be ignored.

Mode B's pre-gate reads THIS LEDGER, not the verdict line.

## Report template

Standalone report path: `docs/reviews/YYYY-MM-DD-<topic>-refutation-r<N>.md` (N = round, 1 on a single run). The
suffix differs from Mode A's `-review-r<N>.md` because the artifact is a ledger, not a
findings list.

```markdown
# Refutation — <topic>

**Date:** <YYYY-MM-DD>
**Target:** <file/dir/spec>
**Verdict:** PASS | REVISE

## Ledger

| id | assumption | tag | status | attack | evidence / check |
|----|------------|-----|--------|--------|------------------|
| A1 | ... | LOAD-BEARING | BROKEN | ... | app/x.py:42 |

## Broken load-bearing assumptions

- **A1** — <assumption>
  - Attack: <scenario in which it is false>
  - Evidence: <file:line or command output>

## Unverified load-bearing assumptions

- **A3** — <assumption>
  - Settling check: <the one check that resolves it>

## Rejected rows

- <id> — <why the row was invalid>
- (or: none)

## Summary

<one-paragraph brutal verdict>
```

The Ledger table joins the two phases **by `id`**: `assumption` and `tag` come
from the Phase 1 extractor, `status`, `attack`, `evidence` and `check` from the
attacker that was handed that row. It lists EVERY extracted row, incidental
rows included; a row that was never attacked carries an empty `status`.

If a section is empty, omit it — except **Rejected rows**, which always states
"none" when empty, so a silently dropped row is visible.

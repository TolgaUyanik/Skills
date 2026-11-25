# Review Rubric & Report Template

## Detecting target type

- **Code / implementation** — source files (`.py`, `.js`, `.ts`, `.sh`, etc.).
- **Design / spec** — files under `specs/`, `docs/`, or named `*-design.md`, `*-plan.md`, `*.spec.md`.
- **Text / analysis** — reports, research, written deliverables, results docs.

The prompt states the type (SKILL.md Mode A step 3); grade by it. If the content is mixed, the main thread picks the dominant content at step 2.

## Dimensions per type

### Code / implementation
- Correctness / bugs — does it actually work; edge cases, off-by-one, null/empty.
- Spec-adherence — does it match what was asked.
- Completeness — did it do ALL of the item, not just the easy 80%.
- Slop / over-engineering — unnecessary abstraction, dead flexibility, copy-paste.
- Tests / verification — present, meaningful, and passing.

### Design / spec
- Placeholders / TBD / incomplete sections.
- Internal contradictions.
- Ambiguity — a requirement readable two ways.
- Missing edge cases.
- Scope creep.
- Scope of claims — the Scope bullet under Text / analysis decides whether a LEDGER row is OVER-SCOPED; the design anchors below set its severity.

### Text / analysis
- Claims backed by evidence.
- Scope: every quantifier (all, every, each, one per, never, always) and every
  number's population, period and sample is no wider than its source (a
  narrower or hedged statement is not a scope defect). A conditional or
  sampled fact stated as universal is CRITICAL. Applies to `fix:` text too.
- Correctness.
- Completeness vs the original question.
- Hand-waving / unsupported assertions.

**Round 1 is exhaustive.** Text targets: round 1 lists every factual sentence and number in `LEDGER:`. Design targets: the LEDGER holds only claims about something outside the target that a rule needs to be true to work (a file or path, a number, another skill, a tool's or system's behaviour); rules, requirements and rationale (why a rule exists, even when it describes a system's behaviour) are counted in COVERAGE. A claim about the harness itself (a tool, subagent type or flag) is backed by the tool's presence in the reviewer's own session or in a transcript; cite `observed: <tool>` or the transcript file:line. Anything in the target left unchecked goes in `not_checked`. `not_checked` lists only items in the target; context or evidence the reviewer did not verify goes in SUMMARY and never blocks. Each later round checks the `not_checked` items in (d) first and adds them to the LEDGER or COVERAGE; in a round whose prompt carries inputs (a)-(e), `not_checked` lists only items that round had to check (the first diff of (e), the items in (d), the class sweep) and did not. A round whose prompt has no input (e) is reviewed like round 1.

## Severity definitions

- **CRITICAL** — wrong, broken, or unsafe; ships a bug or a false claim.
- **MAJOR** — misses a requirement, large gap, or significant quality failure.
- **MINOR** — real but small; should fix, won't block.
- **NIT** — style/polish.

Text and design targets are graded by their anchors below, in place of these definitions; code targets use these definitions.

Anchors for text targets (use these, not tone):
- **CRITICAL** — contradicted by a cited source, over-scoped against it, or
  breaks a stated hard rule.
- **MAJOR** — unbacked claim, or a required element missing.
- **MINOR** — backed and scoped, but weak or redundant.
- **NIT** — wording.

Anchors for design targets (rules, protocols, plans, specs). The outcome is what following the target produces: for a review protocol, a verdict, a gate or which file is written; for a plan or spec, what gets built or run.
- **CRITICAL** — followed as written, the target lets a known defect through (past a gate, or into what is built or run), or breaks a stated hard rule.
- **MAJOR** — a contradiction, a rule readable two ways, a missing step, input or branch, or an UNBACKED or OVER-SCOPED LEDGER row, where it can change the outcome.
- **MINOR** — the same kinds of gap where the outcome does not change (noise, an extra listed item, a stale cross-reference, an incidental outside reference).
- **NIT** — wording.

Regrading an item raised or written in an earlier round needs
`regrade: <old> → <new> because <evidence>` in its `problem:`.

## Gate rule

Any CRITICAL or MAJOR → **REVISE**. Round 2+, each CRITICAL/MAJOR in (a) is also **REVISE** unless its PRIOR line is CLOSED and its latest entry in the fix logs (c) holds in full is Applied or Adjusted, WITHDRAWN and that latest entry is a Declined entry giving file:line evidence that the finding was wrong, or OPEN or REGRESSED and FINDINGS repeats it with `origin: prior` and a `regrade:` to MINOR or NIT. Otherwise **PASS**, except that a text or design target with a non-empty `not_checked` is REVISE. Every finding names a concrete `fix:`; a vague fix does not void the finding.

- A PRIOR line marked OPEN or REGRESSED is repeated in FINDINGS at its old
  severity (or with `regrade:`) and `origin: prior`, so it gates and carries
  forward (a `regrade:` to MINOR or NIT ends this: it is then a MINOR/NIT). WITHDRAWN only when the fix log's Declined entry cites file:line
  evidence that the finding was wrong and the reviewer agrees. A finding declined because its fix text would break a cited line, or because it had no applicable fix, stays OPEN while its defect is present, and the repeated finding gives a new `fix:` that avoids that break and can be applied as written. If its defect is gone, its PRIOR line is CLOSED; under the Gate rule it still gates until the fixer logs it under Applied as already removed (SKILL.md, Re-review rounds).
- Text/design targets: VERDICT is PASS only when `not_checked` is `none`. A
  claim whose source the reviewer cannot find is UNBACKED (graded by the
  severity anchors), never not_checked.

Fix text is held to the finding bar. A `fix:` that adds or rewrites a factual
claim must cite file:line for every claim it introduces and is held to the Scope bullet under Text / analysis. Prefer deleting or narrowing
over writing new claims. A fix that introduces an uncited or wider-than-source
claim is a defective fix, not a void finding: the finding still stands and
still gates, and the fixer applies the narrowest deletion or hedge instead
(SKILL.md, Re-review rounds). A `fix:` that adds, moves or rewrites a rule names every other line that states, references or governs the same case (grep its key terms) and gives the edit for each; a fix that leaves a dangling reference or a second, differing copy is incomplete. The fixer completes such a fix (SKILL.md, Re-review rounds) and the reviewer checks that edit as a changed line.

A CRITICAL/MAJOR lists every instance of its `class:` in `instances:`. A fix
that covers fewer than all listed instances is incomplete. If a class recurs in
a later round, the finding names the upstream source (fact file, template,
sibling target) and the fix either changes it or files a BLOCKED item for it.

## Blocked items

Actions only someone other than the fixer can take (an owner decision, a data
team answer, a capture nobody can make now) go in `BLOCKED:` as
`<owner> | <action> | <evidence>`. They never go in FINDINGS and never gate.
A sentence in the target that is false or unbacked today is always a FINDING
(hedge or delete it now), even when the real fix is BLOCKED. Re-reviews list a
BLOCKED item again only when its status changed.

## Re-review rounds (reviewer, round 2+)

1. Fills `PRIOR:` for every CRITICAL/MAJOR in (a).
2. Reviews every line in the first diff of (e) and every item in (d) at full rigor; text targets add one LEDGER row per factual claim in them, design targets one row per claim the Round 1 rule puts in the LEDGER.
3. Sweeps the whole target for every class in (b).
4. Still reports any other defect it sees, with `origin:` `prior` (a repeated OPEN or REGRESSED PRIOR line), `fix-text` (text inside the cumulative diff in (e)), `missed-r1` (text outside it) or `context-change` (caused by a rule or fact file changed mid-loop). Every origin blocks like any other.
5. Does not re-list a MINOR/NIT already logged as Deferred unless its lines
   changed.

## Report template

Mode A: write the full report to `docs/reviews/YYYY-MM-DD-<topic>-review-r<N>.md`
(N = round, 1 on a single run). Modes B/C: see `auto-run-report.md`.

```markdown
# Brutally Honest Review — <topic> (round <N>)

**Date:** <YYYY-MM-DD>
**Target:** <file/dir/spec reviewed>
**Type:** code | design | text
**Context read:** <each rule / fact file the reviewer read, with mtime or git hash>
**Verdict:** PASS | REVISE
**Coverage:** checked <n>; not_checked: <list | none>
**Open list:** <location — round raised> | none

## Prior findings (round 2+)
- <prior location> — CLOSED | OPEN | REGRESSED | WITHDRAWN

## Findings

### CRITICAL
- **<location>** (class: <class>; instances: <locations>; origin: <round 2+>) — <problem>
  - Fix: <concrete fix>

### MAJOR
- ...

### MINOR / NIT
- ...

## Blocked
- <owner> | <action> | <evidence>

## Ledger
- <location> → <source file:line | observed: <tool>> | UNBACKED | OVER-SCOPED

## Summary

<one-paragraph brutal verdict>
```

If there are no findings in a severity band, omit that band. Omit Prior,
Blocked or Ledger when empty or not applicable.

Fix log (when the review is looped): `...-review-r<N>-fix.md` with Applied /
Adjusted (why) / Declined (why) / Deferred.

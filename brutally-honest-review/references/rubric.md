# Review Rubric & Report Template

## Detecting target type

- **Code / implementation** — source files (`.py`, `.js`, `.ts`, `.sh`, etc.).
- **Design / spec** — files under `specs/`, `docs/`, or named `*-design.md`, `*-plan.md`, `*.spec.md`.
- **Text / analysis** — reports, research, written deliverables, results docs.

If ambiguous, pick the dominant content and state the assumption in the SUMMARY.

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

### Text / analysis
- Claims backed by evidence.
- Correctness.
- Completeness vs the original question.
- Hand-waving / unsupported assertions.

## Severity definitions

- **CRITICAL** — wrong, broken, or unsafe; ships a bug or a false claim.
- **MAJOR** — misses a requirement, large gap, or significant quality failure.
- **MINOR** — real but small; should fix, won't block.
- **NIT** — style/polish.

## Gate rule

Any CRITICAL or MAJOR → **REVISE**. Clean, or only MINOR/NIT → **PASS**.
Findings without a concrete `fix:` are invalid — every finding names the fix.

## Report template

Write the full report to `docs/reviews/YYYY-MM-DD-<topic>-review.md`:

```markdown
# Brutally Honest Review — <topic>

**Date:** <YYYY-MM-DD>
**Target:** <file/dir/spec reviewed>
**Type:** code | design | text
**Verdict:** PASS | REVISE

## Findings

### CRITICAL
- **<location>** — <problem>
  - Fix: <concrete fix>

### MAJOR
- ...

### MINOR / NIT
- ...

## Summary

<one-paragraph brutal verdict>
```

If there are no findings in a severity band, omit that band.

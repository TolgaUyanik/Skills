# Gap triage

**Run this before writing any prompt.** Most gaps are not knowledge gaps, and Deep Research
only moves knowledge gaps. Aiming it at the other four kinds burns the run and returns
advice the project cannot use.

## The five classes

| Class | Test (all evidence internal) | What it actually needs |
|---|---|---|
| **KNOWLEDGE** | No artifact in the project answers it, **and** no artifact shows it was tried | → write the prompt |
| **EXECUTION** | The method exists or is nearly built; what is missing is a run nobody has done | the run. Name it. |
| **BLOCKED** | Depends on a capability the project does not have — data, fills, a short leg, an unbuilt feature | the blocker cleared. Name it and what clears it. |
| **CLOSED** | It was tried and answered. The empty cell is a result, not a gap | nothing. Cite the evidence that closed it. |
| **DECISION** | Nobody lacks knowledge, nothing is blocked, no run is outstanding — it is a priority or values call | the owner. Not research. |

### Why the tests are internal-only

An earlier version's KNOWLEDGE test read "nobody here knows how **and the answer plausibly
exists outside**." The second clause is a claim about the external world, and every recon
source is inside the project. It made the test undecidable while looking decidable. The
test above asks only what the project's own artifacts show. Whether the answer exists
outside is what the Deep Research run is *for* — it is the question, not the entry
criterion.

### Overlap

Signals overlap constantly. **Most-restrictive wins:**

```
CLOSED  >  BLOCKED  >  EXECUTION  >  KNOWLEDGE
```

One exception, and it needs a test rather than a feeling: a KNOWLEDGE gap whose blocker is
expected to clear within the horizon of the research itself is written as KNOWLEDGE, with
the blocker stated in the prompt's CONSTRAINTS block so the report does not return advice
that cannot be acted on. If the blocker has no owner, no date and no task, it is BLOCKED.

DECISION is checked first in practice, because it is the one class where more information
does not help. If the owner already knows both options and is choosing between them, say so
and stop.

## Worked examples

### Any project — the shapes to recognise

| Situation | Class | Tell |
|---|---|---|
| "We should look at using a queue here" — never tried, nothing written | KNOWLEDGE | no artifact answers it, no artifact shows it was tried |
| A benchmark harness exists with passing tests, never pointed at real data | EXECUTION | the method is built; a run is missing |
| "Add SSO" but the identity provider contract is unsigned | BLOCKED | depends on a capability the project does not have |
| A migration was benchmarked twice, both times slower, and the doc says "not pursuing" | CLOSED | it was tried and answered |
| "Postgres or DynamoDB for v2" — both understood, trade-offs known | DECISION | more information does not help; the owner chooses |

### A calibrated set — one project's three empty cells

The rows below come from a BIST-100 trading repo. They are here because they are *hard*
cases with documented evidence, not because this is a trading skill. A triage that gets
these wrong is broken.

| Cell | Evidence | Class | Why not KNOWLEDGE |
|---|---|---|---|
| **Trend-Following** | 0 Gate-C across h3-5 × 5-6% with dip features blacklisted; docs say "leave empty deliberately — a finding, not a gap" | **CLOSED** | It was tried. Repeatedly. The empty cell is the answer. |
| **Range / Support-Bounce** | needs `dist_to_pivot` / `dist_from_high_N`; MLF-1 backlog, unbuilt | **BLOCKED** | The features do not exist. No amount of reading builds them. |
| **Relative-Value / Pairs** | `rel_*` built (MLF-6); edge provisional-negative **at one config** | **EXECUTION** | The method is built and was run once. The blocker is a multi-config backtest, and the deciding number — two legs × 0.315% ≈ 0.63% round-trip — is internal and unreachable by any source on the web. |

Note that the third one was an earlier draft's flagship example for what the skill should
research. It is the clearest case of an execution gap wearing a knowledge gap's coat.

## Reading the reason, not the emptiness

The input is the cold audit's **"not doing + why"** list, plus the project's own coverage
docs where it has them. The "why" is what classifies; the emptiness classifies nothing.

Two warnings about the input, both of which must be passed to the owner with the verdict:

- **In a project with no coverage doc**, the "why" comes from `outside-box-tactics.md`
  building one in a single pass. That is a judgement, not a measurement — nothing like the
  backtest-and-live-P&L trail behind a real coverage map. Say so when it is the basis.
- **One cold pass may not be enough.** Whether it is has never been tested. A missed or
  wrong "why" produces a confident wrong classification.

## Output

Report, every time, including when the answer is "no prompt":

```
GAP TRIAGE — <topic>
  class:      EXECUTION
  because:    <the why, quoted>
  evidence:   <file:line>
  confidence: coverage-doc | audit-only | built-this-run
  needs:      <the run / the blocker / the decision — named concretely>
```

Then stop, unless the owner overrides in one word. **The refusal is the deliverable** in
four cases out of five, and it is recorded in `INDEX.md` as `closed-<class>` — a triage
that says "do not research this, run the backtest instead" has done its job.

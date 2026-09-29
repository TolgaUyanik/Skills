# Context pack and disclosure

## The pack

`<slug>-context.md`, uploaded alongside the prompt. Sections:

1. **What this project does** — two paragraphs, no more
2. **Current approach** — what it actually does today, from live code and config
3. **What was tried and failed, and at what configuration** — the config matters more than
   the failure; "tested once at one parameter set" and "tested across a grid" are different
   facts and Deep Research will treat them the same unless told
4. **Cost / mechanical constraints** — derived per `recon-protocol.md`
5. **Executability constraints** — derived per `recon-protocol.md`
6. **What we believe, tiered** — MEASURED / SINGLE-CONFIG / STALE / ASSERTED / INHERITED
7. **Explicit non-goals** — what a useful answer must *not* be

Carry file:line for anything written down. For anything that came from the owner this
session, write "owner, <date>". Do not manufacture a citation for a judgement — where a
coverage doc was built this run, mark it `built-this-run`.

## The conflict, stated

The pack exists to stop Deep Research re-answering what the project already knows. Doing
that requires saying what it knows **precisely** — the thresholds, the rules, the numbers.
Those specifics are frequently the thing that must not leave the building.

Strip them and what remains is generic enough to return the shallow landscape the pack was
supposed to prevent. Falsification sharpens the same edge: a belief must be specific to be
falsifiable, and the specific version is the IP.

**There is no setting where both are fully satisfied.** A manifest does not resolve that —
it makes the trade visible and hands the owner the dial. What follows is the dial, not a
solution.

## Pack tiers — the owner picks one

| Tier | Contains | Costs |
|---|---|---|
| **Full** | exact rules, thresholds, numbers | maximum disclosure |
| **Shaped** | the *structure* without the values — "a four-condition conjunction on an oscillator and a volatility measure, tuned per-symbol" | the report cannot tell you your thresholds are wrong |
| **Generic** | domain, market, cost, universe only | little better than no pack; expect a landscape answer |

Default to **Shaped** and show what Full would add. Say plainly which questions become
unanswerable at the chosen tier — that sentence is the deliverable, not the tier.

## The manifest

After writing the pack, scan it and print:

```
DISCLOSURE MANIFEST — <slug>-context.md   [tier: shaped]
  [rule logic]          pack:L12, L31      ← src CLAUDE.md:181, MEMORY.md:44
  [thresholds]          pack:L12, L33-L35  ← src MEMORY.md:44-45
  [live P&L]            pack:L48           ← src CLAUDE.md:158
  [personal/financial]  pack:L9            ← src MEMORY.md:4
  [identifying]         (none found)
  [other sensitive]     pack:L52           ← flagged by heuristic, unclassified
Delete any line before sending. Categories are a floor, not a closure — read the pack.
```

### Detection rubric

Category names alone are not a detector. Flag a pack line when it matches:

| Category | Flag when the line contains |
|---|---|
| **rule logic** | a comparison chain (`>`, `<=`, `AND`, `OR`) over named features; a strategy identifier; an entry/exit condition in any notation |
| **thresholds** | a bare numeric constant attached to a feature name, an exit parameter (stop, trailing, max hold), a percentage tied to a decision |
| **live P&L** | currency amounts, returns, win rates, Sharpe/PF figures attributed to *live* or *paper* trading rather than to a backtest |
| **personal/financial** | earnings, income, capital, account size, a person's returns — **whether or not** it is framed as a project fact |
| **identifying** | names, employers, brokers, account identifiers, URLs to private systems |
| **other sensitive** | a line the owner would not post publicly that matched none of the above — flag it unclassified rather than dropping it |

The last row exists because the previous category set was three names and one counterexample
broke it: a directive reading "owner earns ~20%/month on 100k TL manually" is not rule
logic, not a threshold and not live P&L, and the falsification block *requires* putting it
in the prompt. `personal/financial` was added for it and `other sensitive` for whatever
breaks the list next. **Five named categories are a floor. Say so in the printed manifest**
so the owner reads the pack rather than trusting the count.

Cite both ends: the pack line the owner must delete, and the source line it came from.

## Hard rules

- **Never redact automatically.** Classify, list, hand over. The owner deletes.
- **Never send.** This skill writes files; the owner pastes and uploads.
- Print the manifest **before** the handoff block, not after — it is the last thing read
  before the owner acts.
- If the manifest is empty, say "nothing flagged — this does not mean the pack is safe,
  it means nothing matched."

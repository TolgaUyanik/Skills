# Results protocol

`--result <path> [--slug S]`

## 1. Store

Copy the report verbatim to `results/<slug>-result.md`. Never edit it. If `--slug` is
omitted, show the `INDEX.md` rows and ask which one this answers.

## 2. Contract check

Compare the report's top-level headings against the ten output sections the prompt asked
for. Report what is missing or merged:

```
CONTRACT CHECK — <slug>
  present: 1,2,3,4,5,7,9,10
  missing: 6 (source audit)
  merged:  8 (what's missing) folded into 7 (practical implications)
```

**This is a structural check and nothing more.** Headings are cheap to produce; a file with
the right ten headings and empty or invented content passes it. It tells you whether the
report engaged the contract, not whether the content is real. Do not use it as an
authenticity test — that was an earlier design's mistake.

> ⚠ **Unproven:** whether Deep Research honours a ten-section contract at all, or collapses
> it into its own report template. First real run settles it. If sections come back merged,
> the contract is advisory and the prompt needs its output block tightened.

## 3. Skeptic pass

Fresh read-only `Agent` (`subagent_type: "Explore"`). Hand it the report **and both
constraint lists from the pack** — cost and executability. Ask for:

```
For each conclusion in this report:
  - does it survive the COST constraints?
  - does it survive the EXECUTABILITY constraints? (check the other side of the trade, the
    execution granularity, anything frozen, the data horizon)
  - what setting was the underlying evidence drawn from, and does that setting match ours?
    (liquid US equities / crypto / an academic dataset / a different regime)
  - what would have to be true here for it to transfer?
Return SURVIVES / CONDITIONAL / DOES-NOT-TRANSFER with the reason and the citation.
```

Write `results/<slug>-critique.md`.

The executability list does the heavy lifting. A pass holding only cost constraints
green-lights strategies the project structurally cannot run — no short leg, no intraday
fills, a standing freeze — because none of those are prices.

## 4. Task drafts

**The main thread writes these.** The skeptic subagent is read-only; its findings come back
as text and the main thread turns them into drafts. Do not ask the subagent to write.

`results/<slug>-task-drafts.md`, one block per SURVIVES / CONDITIONAL item:

```
### DRAFT — <short name>
what:       <the concrete thing to build or test>
why:        <the finding, cited to the report section>
transfers:  SURVIVES | CONDITIONAL — <the condition>
done looks like: <a number, a file, or a passing check>
blocked by: <anything, or none>
```

Then tell the owner: **run `/task-gen` and point it at this file.**

This skill does not invoke `task-gen` programmatically, for a mechanical reason rather than
a stylistic one: `task-gen` interviews the user whenever goal, acceptance criterion,
dependencies or severity are missing, and its hard rule is that the goal blockquote stays
in the *user's* words. A list of findings carved out of a machine-written report has
neither. Run by a human, the interview has someone to interview and the goal gets the
owner's framing. Run programmatically, it either stalls on every item or attributes a
model's prose to the owner.

## 5. Record

Update the `INDEX.md` row: `status: result-filed`, `updated: <date>`.

## Did the prompt earn its cost?

The only honest test is an A/B, and it is **owner-run and has never been run**:

1. Same topic, two Deep Research jobs. Arm A: a one-line naive prompt. Arm B: this skill's
   prompt.
2. **Give both arms the same context pack.** Otherwise the skeptic pass grades arm A
   against constraints it was never told, and arm B wins by construction rather than by
   prompt quality.
3. Score both:
   - novel claims — anything not already in the project? (this needs the cold audit's
     output to check against, not a from-memory judgement)
   - are claims evidence-labelled and traced to primary sources?
   - does it engage the real constraints, or generic ones?
   - does it surface disagreement, or one smooth narrative?
   - what fraction survives the skeptic pass?
4. Repeat at least twice per arm before believing the result. Deep Research has run-to-run
   variance in which sources surface; a single pair can flip on chance.

Until that has been run, **this skill's advantage over a well-written one-line prompt is
unmeasured.** Say so when asked. Do not claim the delta on the strength of the design.

# Prompt anatomy

**One prompt. Full contract. No stages.**

An earlier design split the contract across five stages, then discovered that the tail
sections it mandated on every stage (evidence tiers, conflicting evidence) *were* stages 2
and 3 — stage 1 already shipped them — while an owner who stopped at stage 1, which the
same design said most topics should, received none of the evidence standards the skill was
sold on. A follow-up here is a new run with the prior report attached, not a stage.

## Blocks, in order

### 1. OBJECTIVE
From the framing the owner picked. An objective, not a question — it names what the
research is *for*, not just what to look up.

```
I want to investigate <X> in order to <ultimate goal>.
The result should let me <decide / build / test / abandon> <thing>.
```

### 2. USE MY DOCUMENTS AS THE STARTING CONTEXT  ← never omit
```
The attached context pack describes what I already know, what I have already tried, and
the constraints I work under. Use it as the starting context, not as one source among
many. Identify what I already understand, what assumptions I am making, and where the
gaps are. Do not spend the report re-establishing what the pack already states.
```

Without this block the pack is one attachment competing with forty web citations and the
report comes back as the generic landscape the pack existed to prevent. It is the cheapest
high-value line in the prompt, and an earlier draft left it out.

### 3. CONTEXT
Compressed from the pack: what the project does, what has been tried and at what
configuration, what must not be re-answered. Then, verbatim:

```
Do not assume my existing beliefs are correct. Treat them as hypotheses to investigate.
```

### 4. WHAT WE BELIEVE — TRY TO KILL IT
The falsification block from `outside-box-tactics.md`, with the belief's evidence tier
attached.

### 5. DECOMPOSITION
Eight to twelve sub-questions, drafted here rather than delegated — the project's own
structure should shape them. Two are mandatory:

- the **cross-domain** sub-question from `outside-box-tactics.md`
- "What has been tried here and failed, and under what conditions did it fail? Distinguish
  failures of the idea from failures of the test."

### 6. CONSTRAINTS
Both lists from the pack, inline. Then:

```
An answer I cannot execute under these constraints is not useful to me. Where a finding
depends on a capability I do not have, say so explicitly rather than omitting it.
```

This is the line that stops a report full of long/short convergence strategies arriving at
a project with no short leg.

### 7. SOURCE STRATEGY
Search broadly first, then prioritise: systematic reviews and meta-analyses · peer-reviewed
primary research · academic books and established researchers · universities and research
institutions · government and professional bodies · high-quality industry research ·
reputable journalism · blogs and forums as leads only.

```
When an important secondary source makes a claim, trace it to the original.
Do not treat popularity as evidence.
```

### 8. EVIDENCE STANDARD
```
Label every significant conclusion: STRONG (multiple high-quality sources converge) /
MODERATE / PRELIMINARY / EXPERT INTERPRETATION / POPULAR-BUT-UNSUPPORTED.
Distinguish evidence from interpretation, primary from secondary, correlation from cause.
Define any overloaded term before comparing sources that use it.
Actively search for evidence that would falsify your own strongest conclusions.
```

### 9. OUTPUT
```
1. Executive summary — the conclusions, in a two-minute read
2. Key findings, with evidence labels
3. Comparison table(s) wherever a comparison is being made
4. Detailed analysis, organised by sub-question
5. Conflicting evidence — where credible sources disagree, and WHY they disagree
   (different methods? populations? definitions? measurements?)
6. Source audit — for each major conclusion: supporting sources, their quality, primary
   or secondary, conflicts, and which conclusions rest on weak evidence
7. Practical implications under MY constraints specifically
8. What's missing — what remains uncertain, what this did not investigate, and what
   evidence would change the conclusions
9. The five highest-value follow-up research questions, and what each would resolve
10. Sources

Compare alternatives on their trade-offs. Do not pick a winner — I will decide what matters.
Optimise for truth, evidence quality and usefulness, not for a confident narrative.
```

### 10. SELF-AUDIT
```
Before finalising: which claim is least supported? Which conclusion could most easily be
wrong? Did you lean on secondary sources? Did you miss credible contradictory evidence?
Did you treat popularity as evidence? Revise accordingly.
```

## Length

**Print the character count. Do not silently move or drop anything.**

No cap is asserted here. An earlier draft invented an 8,000-character limit with no
measurement behind it, then handled overflow by moving blocks into the context pack — the
one place the S10 block above exists precisely because content gets ignored there.

If the prompt exceeds **~12,000 characters**, say so and offer two honest choices: trim the
decomposition (it is the longest block and the most compressible), or paste as-is and
report whether it was accepted whole. The real limit is unknown until someone pastes one.

## Follow-ups

A follow-up run is a normal run with two additions: the prior report attached to the pack,
and an objective that names what the prior report left open. Same contract, same blocks.
Use the prior report's own section 9 to pick the objective — that is what it is for.

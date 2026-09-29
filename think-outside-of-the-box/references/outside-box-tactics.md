# Outside-box tactics

Four tactics. They are not four ways to write the objective — that was the mistake in an
earlier draft, where coverage-gap pre-committed the objective, rival framings refused to
pre-commit it, and falsification pointed at the opposite cell. They operate on four
different parts of the run.

| Layer | Tactic | Writes | Never writes |
|---|---|---|---|
| 1 territory | **Coverage gap** | the candidate set, before any objective exists. Feeds triage. | the objective |
| 2 objective | **Rival framings** | the OBJECTIVE. The only tactic that does. | anything else |
| 3 prompt block | **Falsification** | the `WHAT WE BELIEVE — TRY TO KILL IT` block | the objective |
| 4 sub-question | **Cross-domain transplant** | one mandated sub-question in the decomposition | the objective |

## Precedence — all four layers

```
triage  >  territory  >  objective  >  blocks (falsification, cross-domain)
```

- **Triage** can veto the whole run. Nothing overrides it but the owner.
- **Territory** narrows what the framings may range over. Framings cannot re-open a cell
  triage closed.
- **Objective** is fixed by the owner's pick and is not revised by layers 3 and 4.
- **Blocks** are written *about* the chosen objective. When falsification's house belief
  and the objective concern different territory — the usual case, since the belief lives in
  the occupied cell and the objective usually aims elsewhere — that is not a conflict, and
  the prompt says plainly which is which: the objective is what to investigate, the belief
  is what to attack while investigating it.

If the territory that survives triage contains only occupied cells, falsification and the
objective land on the same cell. That is allowed. Say so in the prompt in one line, so the
report does not read as two briefs stapled together.

## 1. Coverage gap — territory

Map the project's work onto the space it varies along, then look at the cells nobody
occupies — **and read why each one is empty before aiming at it** (that reading is triage's
input, `gap-triage.md`).

**When the project already has a coverage doc**, use it, and use it as written. Do not
restate its headline without checking its table: a headline like "1 of 8 styles carrying the
entire book" is a statement about where the *weight* sits, and the table under it may show
five occupied cells and three empty ones. An earlier draft aimed this skill at seven empty
cells that did not exist.

**When it does not**, build a minimal one during recon and write it to
`<slug>-coverage.md`:

- name the dimension the project's work varies along, in one sentence
- list the cells — as many as the dimension has. Do not pad to a target count and do not
  truncate to one; if the honest answer is three cells, it is three
- mark each occupied or empty
- for each empty cell, the **reason**, quoted with file:line, or the words "no reason
  recorded"

Show it to the owner before triage. If they reject the dimension, **drop this layer** and
run the other three — but then triage has only the audit's "not doing + why" list, so set
`confidence: audit-only` in the triage output. This is a real degradation, not a graceful
one, and the report should say which projects it applies to: any project without a coverage
doc, which is most of them.

> A built-this-run coverage doc is a judgement made in one pass. A project's real coverage
> map is built from live code, backtests and P&L over months. They carry the same shape and
> very different weight. Never present the first as the second.

## 2. Rival framings — objective

Draft as many genuinely different objectives as the territory supports — three, four, six.
Present them as **plain text**, numbered, each with one line on what it would and would not
answer. The owner picks.

Do not route this through `AskUserQuestion`. That tool caps at four options, and a cap
imported from a widget is not a finding about how many framings a topic deserves. If the
owner wants a picker after seeing the list, offer one for the top four.

Framings are drafted **after** territory and **after** triage, over the surviving space
only.

## 3. Falsification — a prompt block

The prompt carries the house belief and asks Deep Research to attack it:

```
# WHAT WE BELIEVE — TRY TO KILL IT
We currently believe: <the belief, stated specifically enough to be falsifiable>
It rests on: <the evidence, with its tier from the audit rubric>
Actively search for evidence that this is false, mis-measured, or true only under
conditions we have not stated. Report what would have to be true for it to be wrong.
```

Two things this requires, both of which have costs the owner must see:

- **The belief must be specific to be falsifiable.** A vague belief cannot be killed. The
  specific version is frequently the project's IP — `disclosure.md` handles that, and does
  not pretend the tension away.
- **The project's governing assumptions are beliefs too.** If a project's top-level
  directive says an edge exists, that directive is a hypothesis with evidence behind it, and
  it belongs in this block like any other. Flag it in the manifest under
  `personal/financial` if it names money or a person.

## 4. Cross-domain transplant — a sub-question

One mandated item in the decomposition:

```
Which other fields face a problem with this SHAPE — <the shape, in structural terms:
e.g. "rare positive events, costly false positives, non-stationary base rate"> — and what
have they built for it? Report the mechanism, not the vocabulary, and say what would have
to hold for it to transfer here.
```

State the shape structurally, not in the project's own domain terms. The point is to reach
past the field's own literature, which the other three tactics already cover.

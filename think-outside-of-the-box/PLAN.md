# Skill: `think-outside-of-the-box`

> ## ⛔ SUPERSEDED — the skill is BUILT. Read `SKILL.md`, not this file.
>
> Rev 2 was refuted a second time: **51 of 65 load-bearing assumptions broke**
> (`docs/reviews/2026-09-20-think-outside-of-the-box-rev2-refutation.md`), a *higher* rate
> than rev 1's 30/41. Seven of those breaks were the document contradicting itself within a
> few paragraphs. A third prose pass was not going to converge, so the skill was built
> instead, with the design changed where the ledger showed the design was wrong.
>
> **What shipped differs from rev 2 below:**
>
> | Rev 2 said | Shipped | Kills |
> |---|---|---|
> | 5-stage pipeline | **one prompt, full contract**; a follow-up is a new run with the prior report attached | B32-B34, B39-B41, B47, B54-B56, B62 |
> | 3 triage classes | **5** — KNOWLEDGE · EXECUTION · BLOCKED · CLOSED · DECISION, most-restrictive-wins | B1, B4, B5 |
> | KNOWLEDGE test includes "exists outside" | internal-only test; what exists outside is the research question, not the entry criterion | B2 |
> | anchor = nearest `.git` → `CLAUDE.md` → cwd, docs searched within | **ask once, record in `~/.claude/think-outside-of-the-box/state.json`** (global, outside docs) | B7, B9, B11-B14, B16 |
> | 4 audit tiers | **5** — adds `STALE` for measured-but-invalidated | B51 |
> | rival framings capped at 4 | plain-text list, uncapped | B20 |
> | 8,000-char cap, overflow into the pack | no cap; print the count, warn at ~12k, never move content silently | B36-B38, B63 |
> | 5 disclosure category names | detection rubric with match patterns + an `other sensitive` catch-all, declared a floor | B26, B27 |
> | manifest resolves the IP conflict | conflict stated; owner picks a **pack tier** (Full / Shaped / Generic) and is told what each costs | B29 |
> | executability constraints listed for this repo | derived via a question checklist; "owner, <date>" is valid provenance | B30, B31 |
> | advisory gate + heading-only compliance detector as authenticity test | contract check kept, explicitly labelled structural-only, not an authenticity test | B40 |
> | A/B where only one arm gets the pack | **both arms get the same pack**, ≥2 runs per arm, labelled never-run | B42, B45, B46 |
> | Verification 9 via `skill-creator` eval | dropped — that eval's `run_eval.py:108` uses `select.select()` on a pipe, which throws on Windows | B71 |
>
> **Confirmed at install:** the skill appears in the live session roster — it is not caught
> by whatever gate hides `domain-modeling`.
>
> **Still unproven, flagged at the point of use inside the skill rather than buried:** one
> cold pass sufficiency (`recon-protocol.md`), skill→skill `/graphify query` invocation
> (`recon-protocol.md`), whether Deep Research honours the section contract
> (`results-protocol.md`), and whether the prompt beats a naive one (`results-protocol.md`).
> None can be settled by planning.

---

**Rev 2** — rewritten 2026-09-20 after `/brutally-honest-review --refute` broke 30 of 41
load-bearing assumptions. Ledger: `docs/reviews/2026-09-20-think-outside-of-the-box-plan-refutation.md`.
Sections carry the `Axx` rows they answer.

## Context

A **global** skill that turns "we should look into X" into a ChatGPT Deep Research prompt
worth the run — per `DeepResearchGuideline.md` (objective-not-question, decomposition,
evidence standards, falsification, source audit).

### What rev 1 got wrong, and what replaces it

Rev 1's premise was a misquote. It read `StrategyCoverageMap.md`'s headline
("1 of 8 styles carrying the entire book") as a coverage count and aimed the pipeline at
"the seven empty cells." The map's own Section B says otherwise: **five styles have live
strategies** (Mean-Reversion ~20+28, Swing 2, Gap-Reversal 2, Breakout ~3, Scalp 28) and
**three cells are empty**. "1 of 8" is a statement about where the book's *weight* sits —
concentration, not coverage. `[A34]`

And the three empty cells are not three opportunities:

| Empty cell | Why empty | Does research help? |
|---|---|---|
| Trend-Following | 0 Gate-C across h3-5 x 5-6%; docs say "leave empty deliberately — a finding, not a gap" | **No.** Closed by evidence. |
| Range / Support-Bounce | blocked upstream on MLF-1 level-distance features | **No.** Blocked, not unknown. |
| Relative-Value / Pairs | `rel_*` features already built (MLF-6); edge provisional-negative **at one config** | **No.** Needs a multi-config backtest, not a paper. |

So the plan's own flagship example was an **execution** gap wearing a knowledge gap's coat —
and its deciding number (two legs x 0.315% ~ 0.63% round-trip) is repo-internal and
unreachable by any web source. `[A24] [A35]`

**The replacement premise:** an empty cell is not a research target. The skill's first real
job is **gap triage** — is this a KNOWLEDGE gap (research moves it), an EXECUTION gap (a test
moves it), or a STRUCTURAL gap (neither, until a blocker clears)? **Only KNOWLEDGE gaps get a
Deep Research prompt.** For the other two the skill says so and names what the gap actually
needs. A skill that refuses to write a prompt is doing its job.

Decisions carried over from rev 1 (owner, 2026-09-20): global skill · staged pipeline ·
all four recon sources · store+critique+tasks results loop · **no auto-redaction** ·
all four outside-box tactics · context-pack companion file · `INDEX.md` state.

---

## Deliverables

### A. Skill source

Source of truth: `D:/AwakenAnalytics/Skills/think-outside-of-the-box/`
Install target: `C:/Users/Tolga/.claude/skills/think-outside-of-the-box/`

```
think-outside-of-the-box/
  SKILL.md                     # frontmatter + router + workflow (loads references lazily)
  DeepResearchGuideline.md     # owner's source doc, kept as-is
  references/
    anchor-and-state.md        # anchor, docs, slug, INDEX schema      [A12 A13 A15 A16 A29 A30 A46 A47]
    recon-protocol.md          # 4 sources + the cold-audit rubric     [A7 A8 A31 A37 A54]
    gap-triage.md              # KNOWLEDGE / EXECUTION / STRUCTURAL    [A24 A34 A35]
    outside-box-tactics.md     # 4 tactics + the layer precedence rule [A36 A42]
    prompt-anatomy.md          # per-stage blocks, S10, length budget  [A18 A20 A21 A22]
    disclosure.md              # the disclosure manifest               [A27 A28]
    results-protocol.md        # compliance -> skeptic -> task drafts  [A9 A10 A25 A52]
    prompt-rubric.md           # the actual quality gate               [A49 A50]
    fixtures/sample-result.md  # pinned results-loop fixture           [A52]
```

Lazy loading is proven: BHR runs on a 16.2 KB `SKILL.md` + 12.9 KB of references pulled per
mode. `DeepResearchGuideline.md` (23 KB) is never loaded whole — `prompt-anatomy.md` carries
the extracted blocks. `[A41 holds]`

**Install is not "drop a directory."** Of 15 dirs in `~/.claude/skills/`, only about half
appear in a session roster; `grill-me` is gated by `disable-model-invocation: true`, and
`domain-modeling` has clean frontmatter and is *still* absent. So: copy the dir, then
**verify invocability** in a fresh session before calling install done — frontmatter carries
`name` + `description` only, no `disable-model-invocation`. If it does not appear, that is a
blocker, not a footnote. `[A1]`

**Description drafting:** BHR's "one sentence" is ~70 words of explicit trigger enumeration.
Match that density. Contested surface forms: "deep research prompt" and "research prompt for
ChatGPT" (vs `anthropic-skills:deep-research`), "what are we not trying" (vs `graphify`).
Settle with `skill-creator`'s description eval — 5/5 on the listed forms with deep-research,
graphify, task-gen and BHR all loaded. `[A4 — unverified; this is the check]`

### B. Output tree

```
<docs>/DeepResearch/
  INDEX.md
  prompts/<slug>-s<N>-<stage>.md
  prompts/<slug>-context.md
  prompts/<slug>-coverage.md        # only when the project has no coverage doc of its own
  results/<slug>-s<N>-result.md
  results/<slug>-s<N>-critique.md
  results/<slug>-s<N>-task-drafts.md
```

Dates live in `INDEX.md`, not in filenames — a stage-3 run in October must find its stage-1
predecessor without guessing a date. `[A17]`

---

## Anchor, docs, slug, state  (`references/anchor-and-state.md`)

Rev 1's `<docs>` ladder walked *upward* for a dir containing `reviews/`. Three things wrong:
`reviews/` is a BHR side-effect, not a project marker (BHR hardcodes that path, so every hit
in this repo and in CanariaMarketing is a BHR scar); the walk had no upward boundary, so from
`Backtesting/paper-trading/` it escapes the git repo entirely; and "project root" was
undefined at `D:/AwakenAnalytics`, which has no `.git`. `[A12]`

**Anchor resolution** — nearest ancestor of cwd, inclusive:
1. a directory containing `.git`
2. else a directory containing `CLAUDE.md`
3. else cwd

**Never search above the anchor.** `--anchor <path>` overrides. Print the resolved anchor.

Verified on this machine:

| cwd | anchor | why |
|---|---|---|
| `D:/AwakenAnalytics/Backtesting/paper-trading` | `…/Backtesting` | `.git` |
| `D:/AwakenAnalytics` | `D:/AwakenAnalytics` | no `.git`, has `CLAUDE.md` |
| `D:/DeCanaria/CanariaMarketing` | itself | confirm at build time |

**`<docs>` resolution — search *within* the anchor, never above it.** An ancestor ladder
cannot work here: `D:/AwakenAnalytics/Backtesting/` has **no `docs/`** — the real one is a
level *deeper*, at `Backtesting/Backtesting/docs/`, which no upward walk reaches. That
misreading is also what made rev 1's verification 1 assert a result that could never
happen. `[A46]`

1. `docs/` directories at depth <= 2 below the anchor. Exactly one → use it.
2. More than one → ask once, record the choice in `INDEX.md`, never ask again for that anchor.
3. None → create `<anchor>/docs/`.

**Topic != cwd.** cwd says where the terminal was opened. A BIST topic launched from
`D:/AwakenAnalytics` must not write to root `docs/` while reading `Backtesting/Backtesting/docs/`.
So the resolved anchor is **printed and confirmable**, `--anchor` overrides, and the choice is
stored per-slug in `INDEX.md` so a resume never re-resolves. `[A13]`

**Slug derivation** (rev 1 used `<slug>` as filename, primary key and CLI argument and never
defined it): lowercase → non-alphanumeric to `-` → collapse repeats → trim → cap 40 chars.
On collision with an existing row whose topic text differs, append `-2`, `-3`. **The handoff
line always echoes the slug**, so `--resume <slug>` asks for a string the owner has seen. `[A16]`

**`INDEX.md` schema.** A pipe-delimited table whose primary key is free text is a parser bug
waiting for the topic `"mean-reversion | pairs"` — which mis-columns `stage` and `status`, the
exact fields the gate reads. So: **slug is the key, never the topic**; the topic column escapes
`|` as `\|`; one row per slug; a `schema: 1` line above the table. The skill read-modify-writes
only its own slug's row and leaves the rest byte-identical, so a git merge conflicts only on a
genuine same-slug collision. `[A15]`

Columns: `slug | topic | anchor | docs | stage | status | started | updated`

---

## Run flow

`/think-outside-of-the-box <topic> [--stage N] [--resume <slug>] [--result <path>] [--anchor <path>]`

Flags on a plain `~/.claude/skills/` skill are proven — this plan was refuted by
`/brutally-honest-review --refute <path>`, same mechanism, same machine. `[A5 holds]`

### 0. Orient
Resolve anchor → `<docs>` → slug. Read/create `DeepResearch/INDEX.md`. Print anchor, docs and
slug in one line. `--result` short-circuits to step 7.

### 1. Recon  (`references/recon-protocol.md`)

**Every source is discovered from the anchor. Nothing is hardcoded.** Rev 1 hardcoded three
paths and all three failed: `D:/AwakenAnalytics/TODO.md` does not exist (seven `TODO.md` and
seven `CLAUDE.md` under this tree, none at root); the memory slug was written as `<proj>` and
never derived, on a disk where drive-letter case is *not* normalised (`D--DeCanaria-mk6-mk6`
beside `d--AwakenAnalytics`) and where both `d--AwakenAnalytics/` and
`d--AwakenAnalytics-Backtesting/` exist; and `python scripts/utils/graph_query.py` **does not
exist anywhere on the disk** — cited with a confident relative path and a "skip silently if
absent" branch that guaranteed nobody would find out. `[A29 A30 A31]`

| Source | Resolution | On failure |
|---|---|---|
| `CLAUDE.md` | `<anchor>/CLAUDE.md`, then each parent to the drive root (project instructions nest) | note absent, continue |
| `TODO.md` | `<anchor>/TODO.md`; else `find <anchor> -maxdepth 2 -iname 'TODO.md'`; >1 hit → **ask, record in INDEX** | note absent, continue |
| memory | mangle anchor path (`D:\A\B` → `d--A-B`), then case-insensitive glob of `~/.claude/projects/*`; **verify the dir exists** | **print** "no memory store found for `<anchor>`" |
| graph | `/graphify query "<question>"` — the documented interface (`graphify/SKILL.md:33`), *not* a script. Precondition: `<anchor>/graphify-out/graph.json` | **print** "no graph at `<anchor>`, skipped" |

No source is ever skipped silently. A missing source is a printed line. `[A31]`

**Cold audit subagent — with a standard shipped into it.** Rev 1 asserted "isolated context is
the point — main-thread self-audit rubber-stamps." Isolation removes *attachment*; it does not
supply *skepticism*. A cold agent opens `CLAUDE.md`, finds the GOVERNING PRINCIPLE stated as
fact, and returns it under "what this project believes, evidence: CLAUDE.md" — it has laundered
an assertion into a finding. Rev 1's own model refutes it: BHR ships `fletcher-persona.md` +
`rubric.md` + `refutation.md` into every subagent. Isolation is the delivery mechanism; the
rubric is the standard. `[A8]`

`recon-protocol.md` therefore ships an **audit rubric** into the subagent:
- A belief stated in `CLAUDE.md`/`MEMORY.md` is a **claim, not evidence**. Cite what backs it.
- Tier every belief: `MEASURED` (a result file or number behind it) · `SINGLE-CONFIG`
  (measured once, one parameter set) · `ASSERTED` (written down, nothing behind it) ·
  `INHERITED` (carried from an older doc, origin unknown).
- file:line for each. No citation → `ASSERTED`.
- Return what the project is **not** doing and, for each, the reason it is not.

That last field feeds gap triage. `[A7 — whether one pass suffices is open; Verification 2]`

**Interview the owner — in chat, not through a picker.** Rev 1 routed four open-ended questions
("what do you believe, what are you uncertain about, what would change your mind") through
`AskUserQuestion`, a closed-form tool needing 2-4 pre-written options — which means guessing the
owner's beliefs in order to ask what they are. Open questions are plain text. `AskUserQuestion`
is used only where the choice is genuinely closed and <= 4 options — which also caps rival
framings at **4, not 3-5**, since the tool cannot present a fifth. `[A11]`

**Stage >= 2 runs a recon delta.** Rev 1 froze the pack at stage 1. Its own step 6 writes tasks
into `TODO.md`, the owner executes them, and `TODO.md`/`CLAUDE.md` are recon sources — so by
stage 3 the pack describes a project the earlier stages already changed, and that stale pack is
uploaded as ground truth. The delta is cheap: re-read the four sources, diff against the pack's
recorded state, regenerate and say so if anything material moved. `[A54]`

### 2. Gap triage — the gate before any prompt exists  (`references/gap-triage.md`)

| Class | Test | Action |
|---|---|---|
| **KNOWLEDGE** | nobody here knows how; the answer plausibly exists outside | → write the prompt |
| **EXECUTION** | we know how; it is built or nearly built; the blocker is a run we have not done | → **no prompt.** Name the run. Offer `/task-gen` |
| **STRUCTURAL** | blocked on a capability we lack (data, fills, a short leg, a feature) | → **no prompt.** Name the blocker and what clears it |

Inputs: the cold audit's "not doing + why" list, and where the project has one, its own coverage
docs. **Read the reason a cell is empty before aiming at it.** Worked example, the rev-1
flagship: Relative-Value/Pairs → features built, tested once, provisional-negative →
**EXECUTION**. `[A24 A35]`

A KNOWLEDGE gap that is *partly* execution-blocked is still written, with the blocker stated in
the prompt's CONSTRAINTS block so Deep Research does not return advice we cannot act on.

### 3. Outside-box pass — four tactics, four layers  (`references/outside-box-tactics.md`)

Rev 1 said "apply all four" and two of them fought over the same field. Coverage-gap
pre-commits the OBJECTIVE to the empty cell; rival-framings explicitly refuses to pre-commit it
("never lock the first framing"); falsification points at the *occupied* cell — the house
belief — which is the opposite of the empty one. One OBJECTIVE, three referents, no precedence
rule. `[A42]`

They are not four ways to write the objective. They are four layers:

| Layer | Tactic | Writes |
|---|---|---|
| 1 — territory | **Coverage gap** | narrows the *candidate set*, before any objective exists. Feeds triage. |
| 2 — objective | **Rival framings** | the OBJECTIVE. <= 4 drafts over the surviving territory, owner picks. The only tactic that writes it. |
| 3 — prompt block | **Falsification** | a `# WHAT WE BELIEVE — TRY TO KILL IT` block. Never the objective. |
| 4 — sub-question | **Cross-domain transplant** | one mandated sub-question: fields sharing the problem's *shape*. Never the objective. |

Precedence when they disagree: **triage > territory > framing.** Triage can veto the run;
territory narrows the framings; framings can never re-open a cell triage closed.

**Generalization.** `StrategyCoverageMap.md` and `TradingStyleTaxonomy.md` exist in exactly one
directory on this machine, and the plan's own portability target has no taxonomy and nothing
shaped like one. Rev 1 wrote "(here: …)" and supplied no procedure for the case that is every
other project — the hard part, and the whole value. So: **when no coverage doc exists, the skill
builds a minimal one** during recon (6-10 cells: what dimension does this project's work vary
along, which cells are occupied, which empty, why), writes `<slug>-coverage.md`, and shows it
before triage. If the owner rejects the dimension, the coverage-gap layer drops for this run and
the other three still apply. `[A36]`

### 4. Context pack + disclosure manifest  (`references/disclosure.md`)

Pack contents are **derived, not hardcoded**. Rev 1 hardcoded five constraints into a *global*
skill: they describe one of three markets this repo trades (US is 0.05%, planned crypto is CCXT
at ~0.2%, not yfinance), they name the wrong universe (mining runs BIST_FULL filtered to ~155 by
turnover, not BIST_100), and they omit the one that actually bites — every pre-2026-07-06
backtest number is suspect until DI-3 re-runs. `[A37]`

Pack sections, each sourced from recon with a file:line trail:
- what the project does · current approach · **what was tried and failed, and at what config**
- **Cost/mechanical constraints** — commissions, data source and its limits, universe, currency
- **Executability constraints** — the ones rev 1 omitted, which silently kill imported findings:
  *can we short?* (this repo's Style 7 is defined long-only because there is no short leg),
  *do we have intraday fills?* (no — scalping blocked on LT/Matriks), *what is frozen?* (citing
  recent live P&L as evidence is under a standing freeze), *what data horizon exists?* (~60d of
  30-minute bars on yfinance). A skeptic pass holding only the cost list green-lights an
  unexecutable strategy. `[A25]`
- owner beliefs, tiered by the audit rubric · explicit non-goals

**The IP conflict is real, and stated rather than deferred.** The pack's job is to stop Deep
Research re-answering what we know, which requires saying what we know precisely. Strip the rule
strings and thresholds and what survives — "we buy dips on BIST-100, commission 0.315%" — is
generic enough to return exactly the shallow landscape this skill exists to prevent.
Falsification sharpens the conflict: a belief must be stated specifically to be falsifiable, and
the specific version *is* the IP. There is no setting where both are fully satisfied. `[A28]`

Owner's call stands: **no auto-redaction.** Replacing rev 1's one-line warning is a **disclosure
manifest** — printed and itemised before anything is sent:

```
DISCLOSURE MANIFEST — <slug>-context.md
  [rule logic]          N items — file:line each, plus the pack line number
  [thresholds]          N items — …
  [live P&L]            N items — …
  [personal/financial]  N items — e.g. "owner earns ~20%/month on 100k TL manually" (MEMORY.md:4)
  [identifying]         N items — names, accounts, brokers
Each item is listed with its line in the pack. Delete any line before sending.
```

The `personal/financial` category exists because rev 1's three categories did not cover it — and
the falsification tactic *mandates* putting that exact claim into the prompt. The owner was going
to be warned about rule strings and not about his own income. `[A27]`

A manifest, not a redaction engine: the skill classifies and lists, the owner deletes.

### 5. Emit the stage prompt  (`references/prompt-anatomy.md`)

**Per-stage tail sections, not a universal one.** Rev 1 mandated S8 evidence tiers and S14
conflicting-evidence on *every* stage — stage 2's evidence matrix and stage 3's falsifiers
shipped inside stage 1. Stage 1 already returned stages 2 and 3, and the owner then waited days
to pay for the same artifacts under different headers. `[A18]`

| Stage | Prompt carries |
|---|---|
| 1 Exploration | S10 · S3 objective/context/scope · S14 what's missing · S23 next questions · cross-domain sub-question |
| 2 Evidence | + S8 evidence tiers · S22 research matrix · S15 source audit · S19 primary sources |
| 3 Challenge | + S7 search-for-disagreement · falsification block foregrounded |
| 4 Synthesis | + S16 no winner-picking · S17 three output layers |
| 5 Implementation | + constraints block foregrounded · experiment spec |

**S10 is mandatory on every stage and was missing from rev 1's list.** Without "Use my documents
as the starting context — identify what I already understand, what assumptions I am making, where
gaps exist," the uploaded pack is one attachment among forty citations and stage 1 returns the
generic landscape the whole skill exists to prevent. Cheapest fix in the rewrite. `[A20]`

**Length budget.** S24's meta-prompt alone is ~170 lines; rev 1 budgeted nothing, and truncation
eats the *tail* — exactly where S14/S15/S23 live. Cap the emitted prompt at **8,000 characters**;
over that, S24 blocks move into the context pack (a file upload, not length-bound) and the prompt
references them. Print the character count on emit. `[A22]`

Guideline section numbering was attacked hardest and held — all eleven cited numbers resolve.
Citing by section number is safe. `[A39 holds]`

### 6. Hand off
Print: anchor · docs · slug · files written · prompt char count · the disclosure manifest ·
"upload the pack, paste the prompt, and review Deep Research's plan before it runs" (S11).
Update `INDEX.md`.

### 7. `--result`  (`references/results-protocol.md`)

1. **Store** raw under `results/`.
2. **Structural compliance check** — do the returned headings match the sections this stage's
   prompt mandated? A collapsed report (S15 source audit folded into "Recommendations") is
   reported as a finding, not silently accepted. Rev 1 had no detector for this anywhere.
   `[A21 — also its settling check]`
3. **Skeptic pass** (fresh read-only subagent) — does each conclusion survive **both** constraint
   lists from step 4, cost *and* executability?
4. **Task drafts, not a task write.** Write `results/<slug>-s<N>-task-drafts.md` and tell the
   owner to run `/task-gen`. The skill does **not** call `task-gen` programmatically: its Step 2
   interviews whenever goal / acceptance criterion / dependencies / severity are missing — a list
   of surviving findings has none of the four, so it would interview on every item and stall
   exactly where rev 1 promised automation. And its hard rule is *"Goal blockquote stays in the
   USER's words — quote their framing, don't launder it"*; these are ChatGPT's words paraphrased
   by a subagent, so feeding them in either violates that rule or attributes a model's prose to
   the owner under `> **Goal (user):**`. Rev 1's "task-gen knows the local discipline" was
   backwards — the local discipline is what rejects this input. `[A10]`
   Separately, the skeptic pass is read-only and rev 1 never handed back to the main thread,
   orphaning the writer step in a context definitionally forbidden from writing. Drafts are
   written by the main thread. `[A9]`
5. Update `INDEX.md`.

---

## The 5 stages, and the gate

| # | Stage | Question | Output |
|---|-------|----------|--------|
| 1 | Exploration | What exists here that we have never touched? | landscape, terminology, schools |
| 2 | Evidence | What actually works, and how strong is the proof? | evidence matrix |
| 3 | Challenge | Why would this fail *for us*? | contradictions, falsifiers |
| 4 | Synthesis | Which principles survive? | framework |
| 5 | Implementation | What do we build or test first? | experiment spec → task drafts |

**Stage 1 stands alone by design.** Most topics should stop there. Stages 2-5 are opt-in and each
must be *asked for* — the pipeline is not a commitment made at stage 1. This repo has a documented
base rate for work that shipped and then died on one manual step: the RD-BT harness (53 green
tests, one command, never run), PM-CAP (never run), the trading-freeze resume gate (neither item
ever registered as a TODO). Those loops are cheaper than six manual acts per stage x five stages.
A pipeline that only pays off at stage 5 will not pay off. `[A26]`

**The gate is advisory, and validated.** Rev 1 made it a hard block — then shipped the bypass as
an acceptance test (verification 4 fed "a short fake ChatGPT report" and passed). The documented
way to unblock stage N+1 was to hand the skill a fabricated file. `[A19]` Instead: stage N+1 runs
the structural compliance check (7.2) against stage N's stored result and **prints what it
found** — "stage 2 result has no S15 source audit and no citations; proceeding on a result that
may not be a Deep Research report." No refusal, no fake-file incentive, and the owner sees the
quality of what he is building on.

**Staging is a claim, not a law.** The guideline's S12 (six stages) and S26 (five) are unsourced
assertion, and rev 1 silently collapsed six into five. Verification 1 decides whether staging
earns its cost. `[A18]`

---

## Verification

Rev 1's six checks were all plumbing — every one passes on a skill that emits *"Research
everything about X"*, the exact anti-pattern the guideline's closing rule names. The delta
between a naive prompt and this skill's prompt **is the product**, and nothing in the suite
touched it. `[A50]`

**1. The A/B — the only check that tests the product.** One topic, a genuine KNOWLEDGE gap (not
Relative-Value, which triage classifies EXECUTION). Run two Deep Research jobs: a naive one-line
prompt, and the skill's stage-1 prompt + pack. Score both with `references/prompt-rubric.md`:
- novel claims — anything not already in the repo?
- are claims evidence-tiered and traceable to primary sources?
- does it engage our actual constraints, or generic ones?
- does it surface disagreement, or one smooth narrative?
- what fraction survives the skeptic pass?

If the skill's report does not beat naive on novel-claims **and** survival rate, the skill does
not justify its cost — say so and cut back to a single better prompt. Then, and only then: is
stage 2 worth its cost against a stage 1 that already ran?

**2. Cold-audit sufficiency.** Run the audit brief once against this repo. Diff its
`SINGLE-CONFIG` list against memory files that already name single-config results
(`bist-trend-following-no-edge`, `daily-live-set-overfit-losers`,
`combination-search-breadth-artifact`, `regime-gate-redundant-on-hybrid`). Misses items already
written down → one pass is insufficient; split the audit. `[A7]`

**3. Triage correctness.** Feed the three empty cells from `StrategyCoverageMap.md`. Required:
Trend-Following → STRUCTURAL (closed by evidence), Range → STRUCTURAL (MLF-1), Relative-Value →
EXECUTION. Any classified KNOWLEDGE → triage is broken and the skill will burn a Deep Research
run on a closed cell. `[A24 A35]`

**4. Anchor + docs resolution, four cwds.** `Backtesting/paper-trading` → anchor `Backtesting`
(`.git`), docs `Backtesting/Backtesting/docs`. Repo root → anchor `D:/AwakenAnalytics`
(`CLAUDE.md`), docs `D:/AwakenAnalytics/docs`. CanariaMarketing → its own docs. A scratch dir
with neither `.git` nor `CLAUDE.md` → anchor = cwd, creates `docs/`. `[A12 A13 A46]`

**5. Source discovery, including the failures.** From each cwd above, confirm every recon source
either resolves or **prints** its absence. Specifically: no `TODO.md` at `D:/AwakenAnalytics` →
asks or reports, never guesses among the seven; the memory glob finds `d--AwakenAnalytics` and
says which; graph precondition absent → prints "no graph, skipped". Confirm nothing anywhere
invokes `graph_query.py`. `[A29 A30 A31]`

**6. Portability, honestly.** CanariaMarketing is **not** a negative control — it has
`docs/reviews/` with 13 BHR reports, so under rev 1's ladder rule 1 fired on the first try and
tested nothing. Under the anchor rule it is a plain positive. The real portability test is the
**no-coverage-doc** path: confirm the skill builds a minimal coverage doc there, shows it, and
degrades to three tactics if the owner rejects the dimension. Confirm graphify skips with a
printed line. `[A36 A47]`

**7. State round-trip.** Topic `"mean-reversion | pairs trading"` → the `|` is escaped, the row
parses back, `stage`/`status` read correctly. Two near-identical topics → two distinct slugs, no
silent merge. The handoff line echoes the slug. `[A15 A16]`

**8. Results loop, pinned fixture.** `references/fixtures/sample-result.md` must carry what a real
report carries: S8 evidence tiers, an S15 source audit with real-shaped citations, S17 layers.
Rev 1 said "a short fake report" and left contents unspecified — a bare-conclusions fake gives the
skeptic pass nothing to grade, so it marks everything survived and hands fabricated survivors
onward, and the test passes while proving only that two files were created. Also run a
deliberately **non-compliant** fixture and confirm 7.2 reports the gap. `[A52 A21]`

**9. Install + invocability.** Copy to `~/.claude/skills/`, open a fresh session, confirm the
skill appears in the roster and fires on all five surface forms. `skill-creator` eval: 5/5.
`[A1 A4]`

**10. Disclosure manifest.** Generate a pack for a BIST topic. Confirm the manifest lists the
GOVERNING PRINCIPLE under `personal/financial` with its `MEMORY.md` line — the item rev 1's three
categories missed. `[A27]`

**Not a quality gate:** `/brutally-honest-review` on the prompt. Its Design/spec rubric measures
placeholders, contradictions, ambiguity, missing edge cases and scope creep — not one dimension
asks whether a prompt is a good *research instrument*, so a consistent, unambiguous, tightly-scoped
and utterly generic prompt scores clean and PASSes. Run it for hygiene if you like;
`prompt-rubric.md` + check 1 are the quality signal. `[A49]`

## Out of scope

- No auto-redaction engine — manifest only (owner's decision; the conflict is stated in step 4,
  not hidden).
- No browser automation; the owner pastes.
- No programmatic `task-gen` invocation — drafts plus a prompt to run it. `[A10]`
- No changes to `brutally-honest-review` or `task-gen`.

## Known-open (unverified, tracked)

| id | Open question | Settling check |
|---|---|---|
| A4 | description triggers without collision | Verification 9 |
| A7 | one cold pass suffices | Verification 2 |
| A9 | main-thread draft-writing after a read-only skeptic pass | Verification 8 |
| A21 | Deep Research honors the section contract | Verification 8 + first real run |
| A22 | 8,000-char cap is enough and is accepted whole | first real paste |
| A52 | fixture is representative | Verification 8 |

Rev 1's Step 0 ("copy this plan into the work folder") is **deleted** — the file exists, and the
step named its own path as both source and destination, so executing it was either a no-op or a
clobber of the reviewed copy, indistinguishable from each other. `[A44]`

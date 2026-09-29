---
name: think-outside-of-the-box
description: >-
  Use when the user wants a ChatGPT Deep Research prompt built from a real project instead of from memory, types /think-outside-of-the-box, asks for a "deep research prompt" or a "research prompt for ChatGPT" about their own codebase or work, wants to know what they are NOT trying, wants a research objective aimed at the space their current approach does not cover, or wants an existing belief attacked rather than confirmed. Audits the project cold, classifies the gap (research it / test it / it is blocked / it is already closed / it is your call), and emits ONE self-contained prompt plus an uploadable context pack and a disclosure manifest. Refuses to write a prompt when research is the wrong tool.
---

# Think Outside Of The Box

Turns "we should look into X" into a Deep Research prompt worth the run.

Two things make it different from writing the prompt by hand:

1. **It audits the project cold before writing.** ChatGPT cannot read the repo, so the
   prompt ships with a context pack built from what is actually on disk — not from memory.
2. **It refuses when research is the wrong tool.** Most "gaps" are not knowledge gaps.
   A cell is empty because it was tested and closed, or because a capability is missing,
   or because nobody has run the test yet. Aiming Deep Research at those wastes the run.
   Triage happens before a single line of prompt is written.

## Invocation

```
/think-outside-of-the-box <topic>
/think-outside-of-the-box <topic> --anchor <path>     # override the project boundary
/think-outside-of-the-box --result <path> [--slug S]  # file a returned report
/think-outside-of-the-box --list                      # show recorded topics
```

## Workflow

Run these in order. Each step names the reference to load; do not load them all up front.

### 0. Resolve where we are — `references/anchor-and-state.md`

Resolve the **anchor** (the project boundary) and `<docs>`. First time at a given cwd,
propose and ask; after that, read the recorded answer. State the resolved pair in one line
before writing anything.

### 1. Recon — `references/recon-protocol.md`

Four sources, all discovered from the anchor, none hardcoded: project instructions, the
task file, the memory store, the knowledge graph. **A source that does not resolve is a
printed line, never a silent skip.**

Then dispatch the **cold audit** subagent with the rubric in that file. The rubric is the
point — an isolated agent without one launders stated beliefs into findings.

Then ask the owner the open questions in plain chat text. `AskUserQuestion` is for closed
choices only.

### 2. Triage the gap — `references/gap-triage.md`

Classify: **KNOWLEDGE · EXECUTION · BLOCKED · CLOSED · DECISION.**

Only KNOWLEDGE gets a prompt. For the other four, say which, say what the gap actually
needs, and stop. Report the classification and its evidence — the owner can override with
one word, but the default is to stop.

### 3. Outside-box pass — `references/outside-box-tactics.md`

Four tactics on four layers, with a precedence rule that covers all four. Coverage-gap
narrows the territory; rival framings write the objective; falsification and cross-domain
are prompt blocks, never the objective.

### 4. Context pack + disclosure — `references/disclosure.md`

Write `<slug>-context.md`. Then print the **disclosure manifest**: every line of the pack
that falls in a sensitive category, with its pack line number. The owner deletes before
sending. The skill never redacts on its own.

### 5. Emit the prompt — `references/prompt-anatomy.md`

**One prompt, full contract.** It carries the objective, the context hook, the
decomposition, evidence tiering, the source audit, falsification, cross-domain, what's
missing, and next research questions. There are no stages — a follow-up is a new run with
the prior result attached.

Print the character count. Do not silently move content anywhere.

### 6. Hand off

One block: anchor · docs · slug · files written · character count · the manifest · then
"upload the pack, paste the prompt, and review Deep Research's plan before it runs."

### 7. `--result` — `references/results-protocol.md`

Store the report, check it against what the prompt asked for, run the skeptic pass against
the project's real constraints, and write task **drafts**. The owner runs `/task-gen`; this
skill never calls it.

## What this skill will not do

- **It will not redact.** It classifies and lists; the owner deletes. Deleting costs
  usefulness — `references/disclosure.md` says how much and lets the owner choose.
- **It will not drive a browser.** The owner pastes.
- **It will not write tasks.** Drafts only.
- **It will not write a prompt for a non-KNOWLEDGE gap** unless the owner overrides.

## Honest status

Never run end to end. The following are unproven and are flagged at the point of use, not
buried here: whether one cold pass is enough to audit a project (`recon-protocol.md`),
whether `/graphify query` is callable from inside a skill (`recon-protocol.md`), and
whether a Deep Research report actually honours the section contract
(`results-protocol.md`). None of them can be settled by more planning.

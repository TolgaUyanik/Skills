---
name: karpathy-llm-wiki
description: Build and maintain a persistent LLM-maintained wiki (Karpathy's "LLM Wiki" pattern) — a structured, interlinked markdown knowledge base that compounds over time instead of RAG-style re-retrieval. Use when the user wants to set up a personal/project knowledge base, ingest a new source into an existing wiki, query the wiki, or lint/health-check it. Triggers: /karpathy-llm-wiki, "llm wiki", "ingest this into the wiki", "add to knowledge base", "wiki lint". For a PDF book specifically, use book-atomizer.
---

# karpathy-llm-wiki

Pattern for building personal knowledge bases with an LLM as the maintainer. Source: Andrej Karpathy's "LLM Wiki" idea file.

## Core idea

Not RAG. Instead of retrieving raw chunks per query, the LLM **incrementally builds and maintains a persistent wiki** — interlinked markdown pages between the user and raw sources. Each new source is read once, integrated everywhere it matters (entity pages, topic summaries, contradictions flagged), and the synthesis stays current. **The wiki is a persistent, compounding artifact.** The user curates sources and asks questions; the LLM does ALL writing, cross-referencing, filing, and bookkeeping.

Applies to: personal tracking, long-running research, book companions, team wikis, competitive analysis, course notes, hobby deep-dives.

## Architecture (three layers)

1. **Raw sources** — `raw/` directory of immutable source documents (articles, papers, images, data). Read-only for the LLM. Source of truth.
2. **The wiki** — directory of LLM-generated markdown: summaries, entity pages, concept pages, comparisons, overview, synthesis. LLM owns this layer entirely.
3. **The schema** — a CLAUDE.md (or equivalent) in the wiki root defining structure, conventions, and workflows for ingest/query/lint. Co-evolved with the user. This is what makes the LLM a disciplined maintainer, not a chatbot.

## Setup (first invocation on a new project)

If no wiki exists yet, collaborate with the user to instantiate one:
1. Ask: domain, source types, where sources live, output formats they care about.
2. Create the directory layout (`raw/`, `wiki/`, `index.md`, `log.md`) and write the schema doc encoding the agreed conventions.
3. Keep it minimal — everything below is optional/modular; pick what fits the domain.

## Operations

**Ingest.** User drops a source into raw collection → LLM reads it, discusses key takeaways, writes a summary page, updates `index.md`, updates every relevant entity/concept page (a single source may touch 10–15 pages), notes contradictions with existing claims, appends to `log.md`. Default: one source at a time with the user in the loop; batch mode only if the user asks.

**Query.** Read `index.md` first to find relevant pages, drill into them, synthesize an answer with citations. Answers can be markdown pages, comparison tables, Marp slide decks, matplotlib charts. **Good answers get filed back into the wiki as new pages** — explorations compound like sources do.

**Lint.** On request, health-check the wiki: contradictions between pages, stale claims superseded by newer sources, orphan pages (no inbound links), important concepts lacking a page, missing cross-references, data gaps fillable via web search. Suggest next questions and sources.

## Index and log

- **index.md** — content catalog: every page with link + one-line summary + optional metadata, organized by category. Updated on every ingest. Read it first when answering queries; works fine to ~100 sources / hundreds of pages without search infra.
- **log.md** — append-only chronological record of ingests/queries/lints. Consistent entry prefix `## [YYYY-MM-DD] ingest | Title` so `grep "^## \[" log.md | tail -5` works.

## Optional tooling

- Search at scale: [qmd](https://github.com/tobi/qmd) — local hybrid BM25/vector search over markdown, CLI + MCP. Or vibe-code a naive search script when the index stops being enough.
- Obsidian as the browsing IDE: Web Clipper for sources, graph view for wiki shape, Marp plugin for decks, Dataview over YAML frontmatter.
- Local images: Obsidian "Download attachments for current file" hotkey; LLM reads text first, then views referenced images separately.
- Wiki is just a git repo of markdown — version history for free.

## Why it works

Wiki maintenance burden (cross-references, currency, consistency) is what kills human wikis; for an LLM it's near-free. Human: curate sources, direct analysis, ask questions. LLM: everything else. (Spirit of Vannevar Bush's Memex — the LLM solves the maintenance problem Bush couldn't.)

## Note

This is a pattern, not an implementation. Directory structure, page formats, and tooling depend on the domain. Everything above is modular — instantiate with the user what fits their needs.

# Opportunity Discovery Agent

**Pipeline position:** Stage 0 of the AI Editorial Operating System — runs before the Opportunity Research Agent (ORA)
**Status:** Draft — designed, not yet implemented

---

## What it does

The Opportunity Discovery Agent takes a **content pillar** as input — not a keyword — and explores it using the same intelligence sources ORA already relies on. It surfaces candidate publishing opportunities, filters out anything already published or in progress, scores what survives, and produces a single standardized output: the **Opportunity Queue**.

It does not research any single keyword in depth, and it does not decide what gets written. It decides what's worth researching next.

---

## Where it fits

```
[YOU] → Content Pillar
           ↓
  0. Opportunity Discovery Agent   ← YOU ARE HERE
           ↓
     Opportunity Queue
           ↓
     (operator selects a top-ranked, unclaimed candidate)
           ↓
     Candidate keyword/topic
           ↓
  1. Opportunity Research Agent    (existing — unchanged)
           ↓
     Opportunity Brief
           ↓
  2. Research Compiler             ← placeholder
           ↓
     Research Brief
           ↓
  3. Editorial Builder             ← placeholder (Builder V1 will migrate here)
           ↓
     Built Astro page
           ↓
  4. Editorial QA                  ← placeholder
           ↓
     QA-approved page
           ↓
  5. Publisher                     ← placeholder
           ↓
     Published page
```

Everything from stage 1 onward is the existing production pipeline. This agent only changes what feeds stage 1 — a queued, evidence-backed candidate instead of a manually typed keyword.

---

## Inputs

**Required:**
- `pillar` — one of the pillars defined in `docs/CONTENT-REGISTRY.md` (`OLSP Ecosystem`, `Affiliate Traffic & List Building`, `Lead Generation`, `Online Income for Beginners`), or `all` to run every pillar in sequence.

**Optional:**
- `seed_topics` — operator-supplied starting points within the pillar. If omitted, the agent derives seeds from the pillar's existing coverage in `CONTENT-REGISTRY.md`.
- `max_candidates` — cap on new candidates queued per pillar per run (default 15).

---

## Output

A single **Opportunity Queue**, updated (not replaced) on every run:

```
agents/opportunity-discovery-agent/OPPORTUNITY-QUEUE.md
```

Each queued candidate carries: a topic/summary, a candidate keyword (the exact string to hand to ORA if promoted), supporting evidence from every source that surfaced or confirmed it, a Discovery Score with sub-score rationale, the result of its content-coverage check, and a status (`unclaimed` / `promoted` / `rejected` / `stale`).

See `OUTPUT-TEMPLATE.md` for the full structure.

---

## Documents in this folder

| File | Purpose |
|---|---|
| `README.md` | This file — overview and quick reference |
| `SPEC.md` | Full specification: mission, workflow, capability reuse, scoring, schema |
| `PROMPT.md` | The agent system prompt and user prompt template |
| `OUTPUT-TEMPLATE.md` | The blank Opportunity Queue structure the agent fills in |
| `OPPORTUNITY-QUEUE.md` | Output — the live, ranked backlog (created on first run) |

---

## Available tools (reused from ORA — no new integrations)

| Tool | Purpose here |
|---|---|
| `dataforseo-keyword-research` skill | Search demand signal per seed topic (bulk keyword-ideas mode, not single-keyword lookup) |
| `reddit-public-fetch` skill | Community intelligence — primary source, same fallback chain ORA uses |
| `mcp__claude_ai_G_Trends__*` | Trend direction and rising related topics per seed |
| `mcp__claude_ai_G_News__*` | Community intelligence fallback (same position in the cascade as in ORA) |
| `WebSearch` / `WebFetch` | Competitor gap confirmation; community fallback (Quora, Discussions, YouTube) |
| `Grep` / `Read` | Content-coverage check against the registry, drafted pages, briefs, research briefs, and the queue itself |

Every source here is one ORA already uses. This agent adds no new provider — only a bulk/exploratory invocation mode and one new internal capability (`CONTENT_COVERAGE`, detailed in `SPEC.md`).

---

## What this agent does NOT do

- Produce an Opportunity Brief (ORA's job, unchanged)
- Run ORA's six-stage deep-research workflow on any candidate
- Write articles, outlines, or Astro pages
- Make the final "write this now" call — it prioritizes; ORA and the operator still decide
- Automatically invoke ORA (queue write is the last step of this agent's run)
- Modify any file outside `agents/opportunity-discovery-agent/OPPORTUNITY-QUEUE.md`
- Modify anything in `agents/opportunity-research-agent/`

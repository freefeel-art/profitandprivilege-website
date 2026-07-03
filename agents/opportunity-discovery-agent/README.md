# Opportunity Discovery Agent

**Pipeline position:** Stage 0 of the AI Editorial Operating System — runs before the Opportunity Research Agent (ORA)
**Status:** Implemented — dry-run validated; DataForSEO is optional, never required (see below)

---

## What it does

The Opportunity Discovery Agent takes a **content pillar** as input — not a keyword — and explores it using the same intelligence sources ORA already relies on. It surfaces candidate publishing opportunities, filters out anything already published or in progress, scores what survives on two separate dimensions, and produces a single standardized output: the **Opportunity Queue**.

It does not research any single keyword in depth, and it does not decide what gets written. It decides what's worth researching next — and, separately, what's worth researching *now* versus later, given the rest of the site's portfolio.

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
- `language` — passed through to Google Trends calls, and to DataForSEO if it happens to be configured (default `EN`; Nordic languages auto-route to Sweden/SV per the underlying skill's existing behavior).
- `region` — passed through to Google Trends regional interest, and to DataForSEO's location parameter if configured (default `United States`).
- `audience_hint` — optional operator note narrowing exploration, advisory only (same spirit as ORA's `intent_hint`).
- `strategic_priorities` — optional Product-Owner-defined priorities for this run (e.g. "favor OLSP Ecosystem hub content this quarter"). Feeds the Priority Score's Strategic Fit sub-score; absence is treated as neutral, never as a penalty.
- `max_candidates` — cap on new candidates queued per pillar per run (default 15).

---

## Output

A single **Opportunity Queue**, updated (not replaced) on every run:

```
agents/opportunity-discovery-agent/OPPORTUNITY-QUEUE.md
```

Each queued candidate carries: a topic/summary, a candidate keyword (the exact string to hand to ORA if promoted), supporting evidence from every source that surfaced or confirmed it, and **two separate scores** — an **Opportunity Score (preliminary)** measuring the candidate's quality in isolation (Trend/Community/Gap — DataForSEO/Demand is never part of this score; see below), and a **Priority Score** measuring whether it should be produced now relative to the rest of the portfolio (Opportunity Quality/Pillar Coverage & Balance/Authority Cluster & Internal-Linking Fit/Strategic Priority Fit) — plus the result of its content-coverage check and a status (`unclaimed` / `promoted` / `rejected` / `stale`). The two scores are never averaged or collapsed into one number.

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

**Mandatory** — a run cannot meaningfully proceed without these, though individual failures are handled per-source (see `SPEC.md` § 4):

| Tool | Purpose here |
|---|---|
| `reddit-public-fetch` skill | Community intelligence — primary source, same fallback chain ORA uses |
| `mcp__claude_ai_G_Trends__*` | Trend direction and rising related topics per seed |
| `mcp__claude_ai_G_News__*` | Community intelligence fallback (same position in the cascade as in ORA) |
| `WebSearch` / `WebFetch` | Competitor gap confirmation; community fallback (Quora, Discussions, YouTube) |
| `Grep` / `Read` | Content-coverage check (registry, drafted pages, briefs, research briefs, the queue itself) and portfolio context (pillar balance, internal-linking gaps, both read from `CONTENT-REGISTRY.md`) |

**Optional enrichment** — never required; a run is fully valid with this absent, disabled, or failing:

| Tool | Purpose here |
|---|---|
| `dataforseo-keyword-research` skill | Search demand signal per seed topic, if configured. Never blocks a run; never enters the Opportunity Score. When available, shown as a labeled evidence line only. |

Every source here is one ORA already uses. This agent adds no new provider — only a bulk/exploratory invocation mode and two new internal capabilities (`CONTENT_COVERAGE` and `PORTFOLIO_CONTEXT`, detailed in `SPEC.md`). Google Search Console is documented in `SPEC.md` § 3 as a future source, not yet wired to any provider.

---

## What this agent does NOT do

- Produce an Opportunity Brief (ORA's job, unchanged)
- Run ORA's six-stage deep-research workflow on any candidate
- Write articles, outlines, or Astro pages
- Make the final "write this now" call — Priority Score informs; ORA and the operator still decide
- Collapse Opportunity Score and Priority Score into a single number
- Treat an unstated `strategic_priorities` input as a penalty
- Require DataForSEO credentials, or treat their absence/failure as a run failure
- Score Demand as a weighted dimension, even when DataForSEO happens to be available
- Automatically invoke ORA (queue write is the last step of this agent's run)
- Modify any file outside `agents/opportunity-discovery-agent/OPPORTUNITY-QUEUE.md`
- Modify anything in `agents/opportunity-research-agent/`

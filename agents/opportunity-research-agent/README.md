# Opportunity Research Agent

**Pipeline position:** Stage 1 of the AI Editorial Operating System  
**Status:** Architecture approved — implementing

---

## What it does

The Opportunity Research Agent takes a keyword as input and determines whether it represents a worthwhile publishing opportunity for Profit and Privilege. It produces a single, standardized output: the **Opportunity Brief**.

It does nothing else.

---

## Where it fits

```
[YOU] → Keyword
           ↓
  1. Opportunity Research Agent   ← YOU ARE HERE
           ↓
     Opportunity Brief
           ↓
  2. Research Compiler            ← placeholder
           ↓
     Research Brief
           ↓
  3. Editorial Builder            ← placeholder (Builder V1 will migrate here)
           ↓
     Built Astro page
           ↓
  4. Editorial QA                 ← placeholder
           ↓
     QA-approved page
           ↓
  5. Publisher                    ← placeholder
           ↓
     Published page
```

---

## Inputs

**Required:** a single keyword or keyword phrase, supplied as plain text. This becomes the brief's Primary SEO Target.

Examples:
- `best affiliate marketing training`
- `how to make money online with no experience`
- `leadsminer pro review`

**Optional:** an `opportunity_name` — an internal identifier for the opportunity (e.g. a candidate_id promoted from `agents/opportunity-discovery-agent/OPPORTUNITY-QUEUE.md`). If omitted, the agent derives one from its own research. See `PROMPT.md` for the full input list (`intent_hint`, `affiliate_product`, `opportunity_name`).

---

## Output

A single **Opportunity Brief** — a structured markdown document saved to:

```
agents/opportunity-research-agent/briefs/[slug].md
```

The slug is derived from the brief's **Opportunity Name** (an internal identifier describing the opportunity), not from the keyword researched — the brief keeps those two deliberately separate. The keyword becomes the brief's **Primary SEO Target**.

The brief contains (schema v1.3): an Evidence Summary panel (why the opportunity exists, at a glance), keyword intelligence, trend data, community insights, SERP analysis, opportunity scoring, **Business Value** (commercial value assessed independently of search opportunity), **Strategic Fit** (target pillar, authority cluster, internal-linking and portfolio impact), an editorial recommendation, data confidence, and an Executive Summary sized for a 30-second decision by the Editorial Commander.

See `OUTPUT-TEMPLATE.md` for the full schema.

---

## Documents in this folder

| File | Purpose |
|---|---|
| `README.md` | This file — overview and quick reference |
| `SPEC.md` | Full specification: mission, workflow, data sources, failure handling, schema |
| `PROMPT.md` | The agent system prompt and user prompt template |
| `OUTPUT-TEMPLATE.md` | The Opportunity Brief schema the agent fills in |
| `briefs/` | Output directory — one `.md` file per opportunity researched |

---

## Available tools (at implementation time)

| Tool | Purpose |
|---|---|
| `dataforseo-keyword-research` skill | Search volume, CPC, difficulty, related keywords |
| `mcp__claude_ai_G_Trends__*` | Interest over time, related topics, regional data |
| `reddit-public-fetch` skill | Community intelligence — primary source |
| `WebSearch` | SERP intelligence; fallback community research |
| `WebFetch` | Fetch specific pages for deeper SERP analysis |
| `mcp__claude_ai_G_News__*` | Trending news and topical relevance signals |

---

## What this agent does NOT do

- Write articles
- Create Research Briefs
- Generate Astro pages
- Modify any file outside `agents/opportunity-research-agent/briefs/`
- Make publishing decisions (it recommends; humans decide)
- Blend Business Value into the Opportunity Score, or vice versa — they answer different questions and are never collapsed into one number
- Re-rank this candidate against other candidates on the site — Strategic Fit is context for one opportunity; portfolio-wide ranking remains the Opportunity Discovery Agent's job

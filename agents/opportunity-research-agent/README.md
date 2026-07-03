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

A single keyword or keyword phrase, supplied as plain text.

Examples:
- `best affiliate marketing training`
- `how to make money online with no experience`
- `leadsminer pro review`

---

## Output

A single **Opportunity Brief** — a structured markdown document saved to:

```
agents/opportunity-research-agent/briefs/[slug].md
```

The brief contains: keyword intelligence, trend data, community insights, SERP analysis, opportunity scoring, and an editorial recommendation.

See `OUTPUT-TEMPLATE.md` for the full schema.

---

## Documents in this folder

| File | Purpose |
|---|---|
| `README.md` | This file — overview and quick reference |
| `SPEC.md` | Full specification: mission, workflow, data sources, failure handling, schema |
| `PROMPT.md` | The agent system prompt and user prompt template |
| `OUTPUT-TEMPLATE.md` | The Opportunity Brief schema the agent fills in |
| `briefs/` | Output directory — one `.md` file per keyword researched |

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

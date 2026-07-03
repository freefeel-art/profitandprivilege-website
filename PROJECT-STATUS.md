# OLSP.ProfitAndPrivilege.com

## Project Status

This document provides a high-level overview of the current project status, priorities, completed milestones, and future roadmap.

_Last updated: 2026-07-03_

---

## Site Overview

- **Platform:** Astro static site, fully self-contained `.astro` pages (`prerender = true`, no shared layouts)
- **Monetization:** Affiliate — primary product is OLSP Academy ($7 entry, $5 commission), driven through the OLSP Megalink funnel
- **Production standard:** Gold Master V1 — see `docs/GOLD-MASTER-SPEC.md`. Canonical review reference: `src/pages/reviews/olsp-academy.astro`. Approved blog reference: `src/pages/blog/part-time-jobs-near-me-no-experience.astro`
- **Content registry:** Single source of truth for published pages is `docs/CONTENT-REGISTRY.md`

## Published Content

| Metric | Count |
|---|---|
| Total published pages | 23 |
| Reviews | 8 |
| Blog articles | 12 |
| Roundups | 1 |
| Infrastructure (home, author) | 2 |
| Gold Master V1 compliant | 21 of 21 editorial pages |

Content spans 4 pillars: OLSP Ecosystem, Affiliate Traffic & List Building, Lead Generation, and Online Income for Beginners. See `docs/CONTENT-REGISTRY.md` for the full page-by-page breakdown and internal link map.

## AI Editorial Operating System

A 5-agent pipeline is planned for content production. Current status:

| Stage | Agent | Status |
|---|---|---|
| 1 | Opportunity Research Agent (ORA) | **Operational** — v1.1, see `agents/opportunity-research-agent/` |
| 2 | Research Compiler | Placeholder — `agents/research-compiler/PLACEHOLDER.md` |
| 3 | Editorial Builder | Placeholder — `agents/editorial-builder/PLACEHOLDER.md` |
| 4 | Editorial QA | Placeholder — `agents/editorial-qa/PLACEHOLDER.md` |
| 5 | Publisher | Placeholder — requires operator approval, `agents/publisher/PLACEHOLDER.md` |

Article generation currently runs manually against `docs/PRODUCTION-MASTER-PROMPT.md` (reviews), `docs/ROUNDUP-MASTER-PROMPT.md` (roundups), and `docs/BLOG-MASTER-PROMPT.md` (blog articles), using ORA briefs as the research input where available.

## Pipeline Queue

- ORA briefs are saved to `agents/opportunity-research-agent/briefs/`
- Current brief: `make-money-online-for-beginners` — scored 70, WRITE NOW — already produced as a published blog article

## Known Gaps

- Research Compiler, Editorial Builder, Editorial QA, and Publisher agents are unimplemented placeholders; the pipeline from brief to published page is manual
- Review cluster is isolated — no lateral internal links between review pages
- LeadsMiner Pro and TD Pages Magick Link reviews are fully orphaned (0 inbound links)
- No OLSP Ecosystem hub/pillar page exists yet

## Documentation Map

| Document | Purpose |
|---|---|
| `docs/GOLD-MASTER-SPEC.md` | Authoritative structural/CSS/link standard for reviews (with blog/roundup exceptions noted) |
| `docs/PRODUCTION-MASTER-PROMPT.md` | Builder prompt for review articles |
| `docs/ROUNDUP-GOLD-MASTER-SPEC.md` / `docs/ROUNDUP-MASTER-PROMPT.md` | Standard and builder prompt for roundup articles |
| `docs/BLOG-MASTER-SPEC.md` / `docs/BLOG-MASTER-PROMPT.md` | Standard and builder prompt for blog/informational articles |
| `docs/CONTENT-REGISTRY.md` | Published page inventory and internal link map |
| `agents/opportunity-research-agent/` | ORA spec, prompt design, and briefs |

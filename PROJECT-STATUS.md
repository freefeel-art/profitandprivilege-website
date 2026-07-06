# OLSP.ProfitAndPrivilege.com

## Project Status

This document provides a high-level overview of the current project status, priorities, completed milestones, and future roadmap.

_Last updated: 2026-07-06_

---

## Site Overview

- **Platform:** Astro static site, hybrid architecture: review articles use the Gold Master shared component system (`src/components/olsp-standard/`); blog/roundup articles remain fully self-contained `.astro` files
- **Monetization:** Affiliate — primary product is OLSP Academy ($7 entry, $5 commission), driven through the OLSP Megalink funnel
- **Production standard:** Gold Master V1 (OLSP Standard V1) — see `docs/GOLD-MASTER-SPEC.md`. Validated review references: `src/pages/reviews/olsp-mineeme.astro`, `src/pages/reviews/seo-writing-ai-review.astro`. Approved blog reference: `src/pages/blog/part-time-jobs-near-me-no-experience.astro`
- **Content registry:** Single source of truth for published pages is `docs/CONTENT-REGISTRY.md`

## Published Content

| Metric | Count |
|---|---|
| Total published pages | 23 |
| Reviews | 14 |
| Blog articles | 12 |
| Roundups | 1 |
| Infrastructure (home, author) | 2 |
| Gold Master V1 compliant | 14 of 14 review pages |

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

Article generation currently runs manually against `docs/PRODUCTION-MASTER-PROMPT.md` (reviews), `docs/ROUNDUP-MASTER-PROMPT.md` (roundups), and `docs/BLOG-MASTER-PROMPT.md` (blog articles), using a Research Brief as the research package input where available.

**Two distinct brief types — do not conflate them:**

| Type | Produced by | Canonical location | Content |
|---|---|---|---|
| **Opportunity Brief** | Opportunity Research Agent (stage 1, operational) | `agents/opportunity-research-agent/briefs/` | Keyword scoring + editorial decision (WRITE NOW / WAIT / DO NOT WRITE) — decides *whether* to write |
| **Research Brief** | Research Compiler (stage 2, placeholder — currently produced manually) | `docs/research/` | Compiled product research: primary sources, mechanics, competitive analysis — the "research package" input the builder prompts consume |

ORA's own spec explicitly excludes creating Research Briefs and forbids it from touching files outside its own `briefs/` directory (`agents/opportunity-research-agent/SPEC.md`, `README.md`). Keep these two artifact types and locations separate.

## Pipeline Queue

- Opportunity Briefs are saved to `agents/opportunity-research-agent/briefs/`
- Current brief: `make-money-online-for-beginners` — scored 70, WRITE NOW — already produced as a published blog article

## Completed Milestones

| Milestone | Date | Description |
|---|---|---|
| Gold Master V1 Spec | 2026-06-XX | Initial shared-component architecture spec for review articles |
| OLSP Standard V1 Validated | 2026-07-XX | Architecture validated via olsp-mineeme.astro and seo-writing-ai-review.astro |
| TD Pages Migration | 2026-07-03 | All old self-contained reviews migrated to Gold Master components |
| External Link Validation | 2026-07-06 | Audited all external link targets and attributes across every review page |
| Production Readiness Audit V1 | 2026-07-06 | Comprehensive audit: P0 SEO fix (shared OG/Twitter/Schema in OlspLayout), P1+ recommendations documented |
| Shared SEO Layer Implementation | 2026-07-06 | OG tags, Twitter Cards, and JSON-LD structured data added to OlspLayout; zero article templates modified |
| OLSP Standard V1 Production Ready | 2026-07-06 | Documentation updated, dead code removed, milestone committed |

## Known Gaps

- Research Compiler, Editorial Builder, Editorial QA, and Publisher agents are unimplemented placeholders; the pipeline from brief to published page is manual
- Review cluster is partially isolated — no systematic lateral internal linking between review pages
- No OLSP Ecosystem hub/pillar page exists yet
- Old self-contained blog and roundup articles (12 blog, 1 roundup) remain outside the shared component system — not in scope for OLSP Standard
- P1+ recommendations from Production Readiness Audit (image alt text, comparison table semantics, FAQ schema for reviews) are documented but not yet implemented

## Documentation Map

| Document | Purpose |
|---|---|
| `docs/GOLD-MASTER-SPEC.md` | Authoritative structural/CSS/SEO/link standard for review articles using the shared component system |
| `docs/PRODUCTION-MASTER-PROMPT.md` | Builder prompt for review articles |
| `docs/ROUNDUP-GOLD-MASTER-SPEC.md` / `docs/ROUNDUP-MASTER-PROMPT.md` | Standard and builder prompt for roundup articles |
| `docs/BLOG-MASTER-SPEC.md` / `docs/BLOG-MASTER-PROMPT.md` | Standard and builder prompt for blog/informational articles |
| `docs/CONTENT-REGISTRY.md` | Published page inventory and internal link map |
| `docs/research/` | Canonical location for Research Briefs (compiled product research; Research Compiler's output) |
| `agents/opportunity-research-agent/` | ORA spec, prompt design, and Opportunity Briefs (`briefs/`) |
| `PROJECT-STATUS.md` | High-level project status, milestones, known gaps, and documentation map |

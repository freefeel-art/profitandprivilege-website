# Engineering Assessment

**Date:** 2026-07-12
**Assessor:** Inherited codebase audit
**Method:** Verify everything against the actual repository

---

## Executive Summary

This repository contains a well-architected content production system that has never fully operated as designed. The individual components work, but the automated pipeline that connects them has never run end-to-end. Articles were produced through manual/assisted AI sessions, not through the automated orchestrator. The system is over-documented relative to its operational reality.

---

## What Is Working

### 1. Content Output (Strong)

42+ published `.astro` articles exist with real editorial content:
- 15 review articles using Gold Master V1 component system
- 26 blog articles using Gold Master blog components
- 1 roundup article
- All articles pass `astro build` and serve HTTP 200
- SEO metadata, OG tags, JSON-LD structured data present
- Internal linking between articles

### 2. Component System (Strong)

13 shared components in `src/components/olsp-standard/`:
- `OlspLayout` provides CSS tokens, TOC, scroll-spy, responsive grid
- Components are used consistently across articles
- Gold Master spec exists and is followed

### 3. Agent Specifications (Strong)

10 agents with complete documentation:
- Each has PROMPT.md, SPEC.md, README.md, and OUTPUT-TEMPLATE/SCHEMA
- Agent contracts define clear boundaries
- Prompt quality is high — specific, actionable, with checklists

### 4. Python Research Pipeline (Functional, Limited)

26 Python files implementing an 8-stage data pipeline:
- Discovery → CI → EI → Briefs → Research → Content Outline → QA → Publishing Package
- Has been executed for 1 pillar (`affiliate_marketing`)
- Produces real data (820 KB discovery package, 976 KB CI findings)
- **Limitation:** Produces structured metadata only — no article text or HTML

### 5. Publishing Engine (Structurally Complete)

`publishing/publish.cjs` (496 lines) implements a 7-stage publish workflow:
- QA validation → Git operations → Build → Deploy → Post-deploy validation → Sitemap ping → Report generation
- Has been executed for at least 3 articles (evidence: publication reports + git commits)

### 6. Mission Control Dashboard (Working)

Real-time dashboard showing:
- Pipeline stage status (inferred from filesystem)
- Production metrics (real file counts)
- Activity feed (real git log)
- Quick access links to all artifacts
- "Produce" button (simulated — see below)

---

## What Is Incomplete

### 1. Pipeline Orchestrator — NOT IMPLEMENTED

`pipeline/PROMPT.md` defines a 5-stage orchestrator. `pipeline/run.sh` invokes it. But:
- `pipeline/state.json` has `lastRun: null` — the pipeline has never run
- The orchestrator has never been executed end-to-end
- No evidence of a successful orchestrator run in git history

### 2. Automated Article Generation — NOT WORKING

The Editorial Builder prompt exists but:
- The "Produce" button in Mission Control runs `simulatePipeline()` — a client-side timer simulation
- `simulatePipeline()` uses `setTimeout` delays and hardcoded event strings
- It produces no artifacts — just updates a UI state store
- The `verifyAssets()` function does real HTTP checks but against fabricated URLs

### 3. Content Registry — STALE

`docs/CONTENT-REGISTRY.md` was last updated 2026-07-06:
- Claims 14 reviews, 14 blog articles
- Actual: 15 reviews, 26 blog articles
- Missing 3+ articles created on 2026-07-12
- Orphan status claims are outdated

### 4. Python Pipeline → Article Gap

The Python pipeline produces structured metadata (JSON outlines, briefs, research packages) but:
- The content production stage explicitly states it does NOT produce article text
- No code connects the Python pipeline output to the Editorial Builder
- The gap between "structured outline" and "published .astro article" is manual

### 5. Post-Deploy Validation — INCOMPLETE

`publish.cjs` Stage 5 hardcodes `https://profitandprivilege-website.netlify.app` while articles reference `https://olsp.profitandprivilege.com`. Stage 6 prepares a Google ping URL but never sends it.

### 6. Legacy Content — ORPHANED

`src/content/reviews/` contains 2 legacy HTML files that are not referenced by any Astro component. Pre-Astro artifacts that should be removed.

---

## What Is Over-Engineered

### 1. Documentation Volume

233 markdown files for 42 articles and 10 agents. The docs-to-code ratio is approximately 5:1. Many documents describe systems that were never built (orchestration spec, implementation docs, workbench analyses).

### 2. Python Research Pipeline

26 Python files implementing an 8-stage pipeline that produces structured metadata but no content. The pipeline is architecturally complete but practically unused — only 1 of 4 pillars has been run, and the output feeds into nothing.

### 3. Agent Documentation Bloat

Each agent has PROMPT.md, SPEC.md, README.md, and OUTPUT-TEMPLATE/SCHEMA — 4 files per agent. The README files are redundant with the SPEC files. The output templates are often superseded by the actual component system.

### 4. Workbench Analysis Documents

13 files in `docs/workbench/` that analyze architecture decisions, validate MVPs, and review designs. These are historical artifacts from the design phase, not active documentation.

### 5. Implementation Documents

12 files in `docs/implementation/` that describe how each pipeline stage was implemented. These are stale — they describe an architecture that was superseded by the OlspLayout migration.

---

## What Is Missing

### 1. CI/CD Pipeline

No `.github/workflows/`, no automated tests, no build validation on push. Deployment is manual `git push` triggering Netlify auto-deploy.

### 2. Automated Testing

No unit tests, no integration tests, no component tests. The only validation is `astro build` (compilation) and manual QA.

### 3. Pipeline State Management

`pipeline/state.json` is never updated. The pipeline has no persistent state tracking. No run history, no stage completion records, no error logs.

### 4. Real-Time Pipeline Execution

The Mission Control "Produce" button runs a simulation. There is no way to trigger a real pipeline run from the dashboard. The real pipeline requires running `pipeline/run.sh` manually in a terminal.

### 5. Article Generation from Briefs

No code connects a research brief to an Editorial Builder output. The gap between "brief exists" and "article published" is entirely manual.

### 6. Monitoring and Observability

No error tracking, no build notifications, no deploy status indicators beyond the dashboard's filesystem-based inference.

### 7. Content Freshness Tracking

No mechanism to detect stale content, broken links, or outdated information in published articles.

---

## What Prevents End-to-End Production

### Blocker 1: The Pipeline Orchestrator Has Never Run

`pipeline/state.json` shows `lastRun: null`. The orchestrator script (`run.sh`) exists but has never been executed successfully. There is no evidence of a single end-to-end pipeline run in the repository's history.

### Blocker 2: No Automated Article Generation

The Editorial Builder prompt exists, but there is no code that:
1. Reads a research brief
2. Passes it to the Editorial Builder
3. Receives a generated .astro file
4. Writes it to `src/pages/`
5. Runs QA
6. Publishes

The entire flow from brief to published article is manual.

### Blocker 3: The Simulation Is Not the Pipeline

The Mission Control "Produce" button calls `simulatePipeline()` which:
- Uses `setTimeout` to fake delays
- Displays hardcoded event strings
- Produces no files
- Updates a client-side state store

This is a UI demo, not a production pipeline.

### Blocker 4: Pipeline State Is Never Persisted

`pipeline/state.json` is never written to. The pipeline has no memory of what it has done. Every run would start from scratch.

### Blocker 5: No Connection Between Python Pipeline and Articles

The Python research pipeline produces JSON metadata. The Editorial Builder produces .astro files. There is no code that connects these two systems.

---

## What Are the Next Five Implementation Milestones

### Milestone 1: Fix the Pipeline Orchestrator

**Objective:** Make `pipeline/run.sh` actually execute end-to-end.

**Work:**
- Implement pipeline state persistence (write to `state.json` after each stage)
- Add error handling and retry logic
- Validate that each stage produces its expected artifact
- Test with a single seed keyword
- Verify all 5 stages complete

**Exit criteria:** `pipeline/run.sh "test keyword"` produces: opportunity brief → research brief → article → QA report → publication report, with `state.json` updated after each stage.

### Milestone 2: Connect Editorial Builder to Briefs

**Objective:** Enable the Editorial Builder to generate articles from research briefs.

**Work:**
- Implement a script that reads a research brief and invokes the Editorial Builder
- The builder generates an .astro file using OlspLayout and components
- Write the output to `src/pages/blog/{slug}.astro`
- Validate against Gold Master spec
- Run `astro build` to verify

**Exit criteria:** Given a research brief path, the system produces a Gold Master compliant .astro article.

### Milestone 3: Implement Real Pipeline in Mission Control

**Objective:** Replace the simulation with actual pipeline execution.

**Work:**
- Replace `simulatePipeline()` with a real pipeline trigger
- Connect the "Produce" button to `pipeline/run.sh` (or equivalent)
- Show real pipeline progress (stage-by-stage)
- Display actual generated artifacts in the Results panel

**Exit criteria:** Clicking "Produce" on a problem triggers a real pipeline run that produces real articles.

### Milestone 4: Update Content Registry

**Objective:** Make the content registry accurate and auto-updating.

**Work:**
- Audit all 42+ existing articles against the registry
- Add missing articles
- Fix page counts and orphan status claims
- Implement auto-update on publish (or periodic rebuild)

**Exit criteria:** `docs/CONTENT-REGISTRY.md` accurately lists all published articles with correct metadata.

### Milestone 5: Add CI/CD and Automated Testing

**Objective:** Ensure every build is validated and every deploy is verified.

**Work:**
- Add GitHub Actions workflow for build validation
- Add link checker (verify all internal/external links)
- Add Gold Master compliance check (automated component validation)
- Add post-deploy verification (HTTP 200, canonical URL, SEO metadata)

**Exit criteria:** Every push triggers automated validation. Every deploy is verified within 5 minutes.

---

## Appendix: Component Status Matrix

| Component | Real Code | Tested | Connected | Operational |
|---|---|---|---|---|
| Astro pages (42+) | ✓ | ✓ (build) | ✓ | ✓ |
| Gold Master components (13) | ✓ | ✓ (build) | ✓ | ✓ |
| Agent prompts (10) | ✓ | ✗ (never run as pipeline) | ✗ | ✗ |
| Pipeline orchestrator | ✓ | ✗ (never executed) | ✗ | ✗ |
| Python research pipeline | ✓ | ✓ (1 pillar) | ✗ | Partial |
| Publishing engine | ✓ | ✓ (3 articles) | ✓ | ✓ |
| Mission Control dashboard | ✓ | ✓ | ✓ | ✓ (simulation only) |
| Pipeline runner (JS) | ✓ | ✓ (simulation) | ✓ | ✗ (simulated) |
| Content registry | ✓ | ✗ (stale) | ✓ | ✗ (outdated) |
| CI/CD | ✗ | N/A | N/A | ✗ |
| Automated tests | ✗ | N/A | N/A | ✗ |

---

## Appendix: Risk Assessment

| Risk | Severity | Mitigation |
|---|---|---|
| Pipeline has never run end-to-end | High | Implement Milestone 1 |
| No automated article generation | High | Implement Milestone 2 |
| Simulation mistaken for production | Medium | Implement Milestone 3 |
| Content registry is stale | Medium | Implement Milestone 4 |
| No CI/CD or automated testing | Medium | Implement Milestone 5 |
| Python pipeline output unused | Low | Connect to Editorial Builder |
| Legacy HTML files orphaned | Low | Remove `src/content/reviews/` |
| Documentation volume excessive | Low | Execute documentation migration plan |

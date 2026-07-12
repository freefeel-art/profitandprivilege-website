# Architecture Consolidation Report

## Executive Summary

The repository has two architectures living side by side: a **production architecture** that actually works, and a **documented future architecture** that was never built.

**Production architecture:** A human manually copies a prompt (`docs/PRODUCTION-MASTER-PROMPT.md`, `docs/BLOG-MASTER-PROMPT.md`, or `docs/ROUNDUP-MASTER-PROMPT.md`) into an LLM, feeds in research, and commits the generated self-contained `.astro` file. All 30 published pages were produced this way. The authoritative standard is `docs/GOLD-MASTER-SPEC.md`, which mandates fully self-contained files with zero imports, inline CSS, and inline JavaScript.

**Intended future architecture:** A 5-stage automated pipeline (Discovery → Research → Writer → QA → Publish) with agent folders for each stage. The Editorial Builder (Stage 3) placeholder states the manual Builder "will migrate here." This direction was introduced in commit `de1d240` and formalized in `4dacee8`, but implementation stopped at documentation.

**Where they agree:** Both architectures define the same output format — a complete Gold Master-compliant `.astro` file. The committed PLACEHOLDER.md and the production specs all agree on this.

**Where they diverge:** An untracked draft of the Editorial Builder prompt (`agents/editorial-builder/PROMPT.md` v2.1) describes a component-based architecture (`OlspLayout` + shared imports) that contradicts the Gold Master standard. This draft was never committed, never approved, and references components that don't exist in the codebase. It is the sole source of architectural conflict in the repository.

---

## Architecture Layers

### Layer 1: Production Content System
**Status: Production**

The system that produces every published page. Self-contained `.astro` files, manual prompt workflow, Gold Master spec enforcement.

Includes:
- `docs/GOLD-MASTER-SPEC.md` — production standard
- `docs/BLOG-MASTER-SPEC.md` — blog production standard
- `docs/ROUNDUP-GOLD-MASTER-SPEC.md` — roundup production standard
- `docs/PRODUCTION-MASTER-PROMPT.md` — manual builder prompt (reviews)
- `docs/BLOG-MASTER-PROMPT.md` — manual builder prompt (blog)
- `docs/ROUNDUP-MASTER-PROMPT.md` — manual builder prompt (roundups)
- All `.astro` files in `src/pages/reviews/`, `src/pages/blog/`, `src/pages/roundups/`

**Fully operational. No changes needed for continued content production.**

---

### Layer 2: Editorial Operating System (Documentation)
**Status: Migration / Future**

The documented 5-stage automated pipeline that was intended to replace Layer 1. Exists as specifications and placeholders only.

Includes:
- `docs/PIPELINE-ARCHITECTURE.md` — pipeline design
- `docs/PIPELINE-HANDOFF-STANDARD.md` — stage handoff contract
- `docs/HEAVY-ASSET-LIBRARY.md` — Knowledge Asset registry
- `agents/opportunity-discovery-agent/` — Stage 0 (full spec)
- `agents/opportunity-research-agent/` — Stage 1L (full spec, manually usable)
- `agents/research-compiler/` — Stage 2H (full spec, never run)
- `agents/editorial-builder/` — Stage 3 (placeholder + untracked draft)
- `agents/editorial-qa/` — Stage 4 (placeholder)
- `agents/publisher/` — Stage 5 (placeholder)

**Pipeline stages 0–2 are documented and could theoretically be run manually. Stages 3–5 are not implemented.**

---

### Layer 3: Production Prompts (Bridge)
**Status: Production — intended to be replaced**

The manual workflow prompts (`docs/PRODUCTION-MASTER-PROMPT.md` etc.) that are the bridge between Layers 1 and 2. They were intended to "migrate into" the Editorial Builder agent but remain the only production tools.

**Stable, well-tested across 30 pages. The migration target for the Editorial Builder agent.**

---

### Layer 4: Abandoned Experiments
**Status: Obsolete**

Architecture explorations that were attempted, reverted, or never completed:
- `src/components/ArticleNavigation.astro` — shared component, deployed to production, reverted within 1 hour
- `src/data/olsp-reviews.ts` — data file created for the ArticleNavigation component, unused since the revert
- `src/layouts/Layout.astro` — generic layout, used only by infrastructure pages, never by article pages
- `agents/editorial-builder/PROMPT.md` (untracked) — component-based draft, never committed

**These files exist in the repository but have no production impact.**

---

## Migration Status

| Subsystem | Status | Detail |
|---|---|---|
| **Gold Master** | **Complete** | Standard defined, all 30 published pages compliant. The canonical reference (`src/pages/reviews/olsp-academy.astro`) is locked. |
| **Production Builder** | **Production (will be replaced)** | Manual prompt workflow. Works reliably. Three prompt variants (review, blog, roundup). Intended migration target for Editorial Builder agent. |
| **Opportunity Discovery** | **Documented (never run)** | Full spec exists in `agents/opportunity-discovery-agent/`. SPEC.md v0.6, PROMPT.md, OUTPUT-TEMPLATE.md, README.md all present. Never invoked as a standalone agent. `OPPORTUNITY-QUEUE.md` was populated once manually. |
| **Opportunity Research** | **Documented / Manually usable** | Full spec in `agents/opportunity-research-agent/`. SPEC.md v1.4, PROMPT.md, OUTPUT-TEMPLATE.md, README.md. 14 Opportunity Briefs exist in `briefs/`. Briefs are produced manually by copying the prompt into an LLM. Not automated. |
| **Research Compiler** | **Documented (never run)** | Full spec in `agents/research-compiler/`. SPEC.md v1.0, PROMPT.md, OUTPUT-TEMPLATE.md, README.md. 3 existing Research Briefs in `docs/research/` were produced manually before the spec existed. Never run as a standalone agent. |
| **Editorial Builder** | **Not started** | Committed state: PLACEHOLDER.md only. Untracked draft: PROMPT.md v2.1 (architecturally divergent). No implementation exists. |
| **Editorial QA** | **Not started** | PLACEHOLDER.md only. No spec, no prompt, no checklist beyond what's embedded in the production prompts. |
| **Publisher** | **Not started** | PLACEHOLDER.md only. Publication is entirely manual (git add, commit, push). |
| **Pipeline Orchestrator** | **Not started** | No orchestration layer exists. The pipeline is a conceptual design, not a runnable system. Each stage exists as documentation, not automation. |
| **Asset Library** | **Seeded** | `docs/HEAVY-ASSET-LIBRARY.md` created with 3 seed entries. 2 known gaps documented (LeadsMiner Pro, Wayne Crowe). Never consulted by any automated process. |

---

## Architectural Conflicts

### Conflict 1: Editorial Builder PROMPT.md vs Gold Master Spec

| Detail | Value |
|---|---|
| **Cause** | Untracked `agents/editorial-builder/PROMPT.md` v2.1 describes a component-based architecture (`OlspLayout` + shared components). The Gold Master spec (`docs/GOLD-MASTER-SPEC.md` § 1) mandates self-contained files with "no shared layout imports, no component imports, and no framework components." |
| **Impact** | If the Editorial Builder were invoked using the untracked PROMPT.md, it would produce output that cannot render — none of the referenced components exist. The prompt is unusable today. |
| **Resolution** | Either (a) revise the PROMPT.md to match the Gold Master self-contained architecture, or (b) update the Gold Master spec to a component architecture and build all required components. The committed evidence favors (a). |

### Conflict 2: Editorial Builder PROMPT.md vs Editorial Builder PLACEHOLDER.md

| Detail | Value |
|---|---|
| **Cause** | The committed `PLACEHOLDER.md` says the agent produces "a complete, Gold Master-compliant Astro page." The untracked `PROMPT.md` says the agent produces "body content only" — a fragment. |
| **Impact** | Two incompatible definitions of the same stage's output exist. The committed version is authoritative; the untracked draft contradicts it. |
| **Resolution** | Reconcile the PROMPT.md with the PLACEHOLDER.md. If the output is a complete Gold Master file, the PROMPT.md must describe producing one, not a content block. |

### Conflict 3: Documented Pipeline vs Actual Production

| Detail | Value |
|---|---|
| **Cause** | `docs/PIPELINE-ARCHITECTURE.md` describes an automated 5-stage pipeline with production-ready stages. In reality, only Stage 0 (Discovery) and Stage 1L (ORA) are documented enough to be run manually. Stages 3–5 are unimplemented. |
| **Impact** | A new contributor reading the pipeline docs would believe the automated system exists. The docs describe a future state as if it were current. |
| **Resolution** | Either mark the pipeline documentation as "Future — not yet implemented" or begin implementation. The current state is misleading. |

### Conflict 4: Blog CTA Inconsistency Across Published Pages

| Detail | Value |
|---|---|
| **Cause** | 13 blog pages use the old `.cta-card` pattern (3 identical sales CTAs). 9 blog pages use the new `quote-banner` + `standard-cta` pattern. Both patterns are described as current in different documents. |
| **Impact** | Blog articles are visually inconsistent. Readers see different CTA patterns depending on which generation of blog article they land on. |
| **Resolution** | A content normalization sprint could standardize all 13 older blog pages to the QuoteBanner + Standard CTA pattern. This is optional — both patterns build and work correctly. |

### Conflict 5: Blog Frontmatter Inconsistency

| Detail | Value |
|---|---|
| **Cause** | 3 blog pages still use the legacy `const pageTitle`/`const pageDescription` frontmatter pattern. The BLOG-MASTER-SPEC.md § 1 says frontmatter should contain "only `export const prerender = true;` — no other variables." |
| **Impact** | Minor inconsistency. The variables are declared but never used (actual `<title>` is hardcoded). Does not affect builds or rendering. |
| **Resolution** | Remove the unused variables from the 3 legacy blog pages. Low priority. |

### Conflict 6: PROJECT-STATUS.md Lag

| Detail | Value |
|---|---|
| **Cause** | `PROJECT-STATUS.md` was last updated 2026-07-03 and reports 23 published pages and 4 pillars. Actual count is 30 pages and 5 pillars (Pillar 5: AI Tools was added after). |
| **Impact** | Stale reference document. Agents reading it will get incorrect page counts and miss the AI Tools pillar. |
| **Resolution** | Update `PROJECT-STATUS.md` to reflect current state. |

---

## Required Architecture Decisions

### Decision A: What should the Editorial Builder agent produce?

| Detail | Value |
|---|---|
| **Why needed** | The untracked PROMPT.md v2.1 and the committed PLACEHOLDER.md/Gold Master spec describe incompatible outputs. Before the Editorial Builder can be implemented, this must be resolved. |
| **Option 1: Self-contained Gold Master file** | The Editorial Builder produces a complete, self-contained `.astro` file matching `docs/GOLD-MASTER-SPEC.md`. Same output format as the manual Builder. No new components needed. **Matches committed architecture.** |
| **Option 2: Component-based content block** | The Editorial Builder produces an Astro content block using `OlspLayout` and shared components. Requires building a new layout system, 12+ components, and rewriting the Gold Master spec. **Matches untracked draft, contradicts committed specs.** |
| **Recommendation** | Option 1. It matches the committed PLACEHOLDER.md, the Gold Master spec, the production pages, and the ArticleNavigation reversion experience (which demonstrated that shared components cause issues). |

### Decision B: Should the Agent Pipeline documentation be marked as "future design" or kept as-is?

| Detail | Value |
|---|---|
| **Why needed** | `docs/PIPELINE-ARCHITECTURE.md` presents a future state as current reality. This misleads contributors. |
| **Option 1: Add explicit "Future Design" header** | Minimal change. A single `**Status:** Future design — not yet implemented` line at the top of PIPELINE-ARCHITECTURE.md clarifies the state without changing architecture. |
| **Option 2: Leave as-is** | The documentation continues to imply a pipeline that doesn't exist. Higher risk of confusion. |
| **Recommendation** | Option 1. Reduces ambiguity with zero architectural impact. |

### Decision C: Should the 13 older blog pages be standardized to QuoteBanner + Standard CTA?

| Detail | Value |
|---|---|
| **Why needed** | Blog articles are visually inconsistent. 13 use old `.cta-card`, 9 use new `quote-banner` + `standard-cta`. |
| **Option 1: Standardize all** | Update the 13 older blog pages to match the current BLOG-MASTER-SPEC.md. Consistent reader experience. |
| **Option 2: Leave as-is** | Both patterns build and work correctly. The spec describes both as acceptable (old pages are "not retroactively rewritten"). |
| **Recommendation** | Defer. This is a content normalization task, not an architectural decision. It does not block any other work. |

### Decision D: Should the legacy `src/components/ArticleNavigation.astro` be removed or retained?

| Detail | Value |
|---|---|
| **Why needed** | Orphaned component. No page uses it. Files in `src/components/` and `src/data/` exist solely for a reverted feature. |
| **Option 1: Remove** | Delete the unused files. Cleaner repository. |
| **Option 2: Retain** | Keep as reference for future shared-component experiments. |
| **Recommendation** | Defer. The files are small and cause no harm. Removing them has no architectural significance. |

### Decision E: Should the untracked Editorial Builder PROMPT.md be committed, revised, or deleted?

| Detail | Value |
|---|---|
| **Why needed** | The untracked file represents a silent architecture direction change. It must be resolved. |
| **Option 1: Revise to match committed architecture, then commit** | Rewrite PROMPT.md v2.1 to describe producing self-contained Gold Master files. Then commit it as the official Editorial Builder prompt. |
| **Option 2: Discard the draft** | Delete the untracked file. The PLACEHOLDER.md remains the sole definition of Stage 3. |
| **Option 3: Commit as-is, then build the component architecture** | Accept the component-based direction. Build `OlspLayout`, all 12+ shared components, and rewrite the Gold Master spec. High effort. |
| **Recommendation** | Option 1. It aligns with the committed architecture, requires no new components, and resolves the conflict. |

---

## Immediate Safe Work

The following work can proceed immediately without waiting for any architectural decision:

1. **Content production.** The manual prompt workflow works. New review, blog, or roundup articles can be produced today using the existing `docs/*-MASTER-PROMPT.md` files. None of the architectural decisions above affect this capability.

2. **Content Registry maintenance.** Updating `docs/CONTENT-REGISTRY.md` and `PROJECT-STATUS.md` page counts and status does not depend on any architectural decision. These are documentation tasks.

3. **Update PROJECT-STATUS.md to current state.** The file reports 23 pages and 4 pillars; reality is 30 pages and 5 pillars. This can be fixed independently.

4. **Run Opportunity Discovery Agent manually.** The agent is fully specified. An operator could invoke it against a pillar to produce new Opportunity Briefs. No architectural decision blocks this.

5. **Run the Research Compiler manually to fill known gaps.** The 2 known gaps (LeadsMiner Pro Research Brief, Wayne Crowe founder brief) could be produced today using the existing Research Compiler spec and process.

These tasks are safe because they use existing, working systems and produce artifacts that are consumed by humans (not by any automated pipeline that might change).

---

## Deferred Work

The following work should NOT continue until the architecture decisions have been made:

### Deferred: Editorial Builder agent implementation

| Detail | Value |
|---|---|
| **Why** | The Editorial Builder has two incompatible architectural definitions. Implementing either one without resolving the conflict commits to an architecture direction that may be reversed. |
| **Dependencies** | Decision A (output format: self-contained file vs component block) and Decision E (PROMPT.md disposition). |

### Deferred: Editorial QA agent design

| Detail | Value |
|---|---|
| **Why** | QA can only validate output whose format is known. If the Editorial Builder produces content blocks, QA must validate different things than if it produces self-contained files. |
| **Dependencies** | Decision A. Editorial QA follows Editorial Builder in the pipeline. |

### Deferred: Publisher agent design

| Detail | Value |
|---|---|
| **Why** | Publisher follows QA. Publication mechanics may differ depending on whether the output is a single file or involves multiple artifacts. |
| **Dependencies** | Decision A, Editorial QA design. |

### Deferred: Shared component development (OlspLayout, QuoteBanner, etc.)

| Detail | Value |
|---|---|
| **Why** | If Decision A selects Option 1 (self-contained files), these components should not exist. Building them would be wasted effort. |
| **Dependencies** | Decision A. |

### Deferred: Blog CTA standardization (13 older blog pages)

| Detail | Value |
|---|---|
| **Why** | The QuoteBanner + Standard CTA pattern may change as the Editorial Builder architecture is resolved. Standardizing now risks rework. |
| **Dependencies** | Decision A, Decision C. |

---

## Repository Cleanup Candidates

The following items are identified as cleanup candidates. Do not remove them — they are listed here for awareness.

### Obsolete documents
- `PROJECT-STATUS.md` — page counts and pillar counts are stale. Still contains useful pipeline status information.
- `docs/ROUNDUP-PRODUCTION-WORKFLOW.md` — predates the Gold Master spec; possibly superseded by `docs/ROUNDUP-GOLD-MASTER-SPEC.md` and `docs/ROUNDUP-MASTER-PROMPT.md`.

### Duplicated documents
- The prompt instructions for content rules (epistemic labelling, source fidelity, tone) are duplicated across `PRODUCTION-MASTER-PROMPT.md` (Section "Content and Editorial Rules"), `BLOG-MASTER-PROMPT.md` (references the production prompt), and `agents/editorial-builder/PROMPT.md` (also has its own copy). Three copies of the same rules.
- CTA placement rules exist in `GOLD-MASTER-SPEC.md` § 8.13 (for reviews), `BLOG-MASTER-SPEC.md` § 3a/3b (for blog), `ROUNDUP-GOLD-MASTER-SPEC.md` (for roundups), `PRODUCTION-MASTER-PROMPT.md` (Component Rules > CTA cards), `BLOG-MASTER-PROMPT.md` (QuoteBanner + Standard CTA), `ROUNDUP-MASTER-PROMPT.md` (CTA cards), and `agents/editorial-builder/PROMPT.md` (CTA placements). The same information is maintained in 7 places.

### Superseded drafts
- `agents/editorial-builder/PROMPT.md` (untracked) — drafted but never committed. Supersedes `PLACEHOLDER.md` in intent but contradicts it in architecture.

### Temporary files
- None identified.

### Orphaned architecture
- `src/components/ArticleNavigation.astro` — created for a shared-component experiment that was reverted. No page imports it.
- `src/data/olsp-reviews.ts` — data file for ArticleNavigation. Unused.
- `src/layouts/Layout.astro` — generic layout, used only by `index.astro` and `authors/jarmo-halonen.astro`. Article pages bypass it entirely.

---

## Recommended Next Sprint

**One sprint: Reconcile the Editorial Builder PROMPT.md with the committed Gold Master architecture.**

### Sprint goal
Eliminate the single largest architectural conflict in the repository: the incompatible Editorial Builder PROMPT.md v2.1.

### Sprint tasks
1. Read the committed Gold Master spec (`docs/GOLD-MASTER-SPEC.md`), BLOG-MASTER-SPEC.md, and ROUNDUP-GOLD-MASTER-SPEC.md to establish the production architecture.
2. Read the committed Editorial Builder PLACEHOLDER.md to establish the intended agent output format.
3. Rewrite the untracked `agents/editorial-builder/PROMPT.md` so it describes producing **complete self-contained `.astro` files** matching the Gold Master spec — the architecture that actually exists.
4. Commit the revised PROMPT.md, replacing the PLACEHOLDER.md or supplementing it.
5. Verify: read the revised PROMPT.md and confirm every component reference, import path, and architectural assumption matches an existing codebase element.

### Why this sprint
- **Reduces architectural uncertainty.** The conflicting PROMPT.md is the only source of architectural conflict in the repository. Resolving it unblocks every deferred task.
- **Avoids unnecessary redesign.** The Gold Master self-contained architecture is proven across 30 pages. The revised prompt would describe what already works.
- **Preserves the Architecture Freeze.** No production code is modified. No spec is rewritten. Only the untracked draft is reconciled with committed reality.
- **Moves closer to production readiness.** With a committed, correct Editorial Builder prompt, the next step (implementation) has a clear target.

### Sprint output
A single committed file: `agents/editorial-builder/PROMPT.md` (revised), with the placeholder updated to reference it, and a brief summary of what changed and why.

---

Architecture Consolidation Complete

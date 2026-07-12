# ADR-001: Editorial Builder Output Architecture

## Status

Proposed

---

## Context

### Production architecture

The repository currently produces all article pages through a manual workflow. A human operator copies a production prompt (`docs/PRODUCTION-MASTER-PROMPT.md`, `docs/BLOG-MASTER-PROMPT.md`, or `docs/ROUNDUP-MASTER-PROMPT.md`) into an LLM, feeds in a research package, and commits the generated output. All 30 published pages (14 reviews, 22 blog, 1 roundup, 2 infrastructure) were produced this way.

Every published article page is a fully self-contained `.astro` file with:
- Zero `import` statements
- Inline `<style>` block with the full CSS design token set
- Inline `<script is:inline>` block with scroll-spy and mobile TOC JavaScript
- Complete `<html>`, `<head>`, `<body>` document structure
- No shared layouts, no component imports, no framework components

This architecture is defined and enforced by `docs/GOLD-MASTER-SPEC.md` Section 1:

> "Every article is a **standalone `.astro` file** placed in the appropriate subdirectory of `src/pages/`. There are no shared layout imports, no component imports, and no framework components. The file is entirely self-contained: CSS, HTML, and JavaScript all live in the same file."

And Section 18, Rule 1:

> "One file, self-contained. Every article is a single `.astro` file in the appropriate `src/pages/{type}/` directory. No layout imports, no component imports, no shared CSS files."

The `docs/BLOG-MASTER-SPEC.md` Section 1 follows the same rule.

### Intended migration

Commit `de1d240` (2026-07-03) introduced an "AI Editorial Operating System" — a 5-stage automated pipeline intended to replace the manual workflow. The Editorial Builder agent (Stage 3) was created as a placeholder with the explicit note:

> "The current manual Builder workflow (documented in `docs/PRODUCTION-MASTER-PROMPT.md` and `docs/GOLD-MASTER-SPEC.md`) will be migrated into this agent when the upstream pipeline stages are stable."

The committed `agents/editorial-builder/PLACEHOLDER.md` defines the agent's role:

> "Takes an approved Research Brief as input and produces a complete, Gold Master-compliant Astro page ready for QA."

And its output:

> "A fully built `.astro` file placed in the correct `src/pages/` subdirectory, matching the Gold Master specification exactly."

The migration was started but halted after documentation. Only the Opportunity Research Agent (Stage 1L) was implemented. Stages 3–5 remain placeholders. Commit `4dacee8` (2026-07-04) formalized the pipeline split into Heavy and Light tracks but did not advance implementation.

### Conflicting untracked Builder prompt

After the last committed changes, a draft `agents/editorial-builder/PROMPT.md` v2.1 was created (untracked, never committed). This draft describes a fundamentally different architecture:

- Output is "the **body content only**" — a fragment, not a complete file
- Output is wrapped in `<OlspLayout>`, a shared layout component
- Content uses imported shared components: `QuoteBanner`, `StandardCta`, `AuthorBox`, `ScoreBars`, `Quiz`, `ComparisonTable`, `ProsCons`, `SvgDiagram`, `VideoEmbed`
- Presentation is "owned by the OLSP Standard v2.1 layout system"

None of these components exist. The `src/layouts/` directory contains only a generic `Layout.astro` (used by infrastructure pages, never by articles). The `src/components/` directory contains one orphaned component (`ArticleNavigation.astro`) that was created during a shared-component experiment, deployed to production, and reverted within one hour.

### Investigation results

Three inspections were conducted:

1. **Production Pipeline Audit** (`docs/workbench/production-pipeline-audit.md`): Confirmed every published page is self-contained with zero imports. Confirmed the production prompts are human-copy-paste instructions, not agent prompts. Confirmed the agent pipeline was documented after all pages were published.

2. **Architecture Intent Investigation** (`docs/workbench/architecture-intent-audit.md`): Confirmed the committed intent was to migrate the manual Builder into an agent that produces the same Gold Master self-contained files. Confirmed the untracked PROMPT.md v2.1 is a divergent exploration that was never committed or approved.

3. **Architecture Consolidation Report** (`docs/workbench/ARCHITECTURE-CONSOLIDATION-REPORT.md`): Identified the conflicting PROMPT.md as the single architectural conflict in the repository. Recommended reconciling the prompt with the committed architecture before any implementation.

### Historical precedent

A shared-component experiment was conducted on 2026-06-26:
- `683fe8b`: `ArticleNavigation.astro` component created
- `8c5ae16`: Component imported into all 7 OLSP review pages
- `4b54edd` (~1 hour later): **Reverted** — all pages restored to pre-import state

This is the only production deployment of shared components in the repository's history. It was rolled back within hours, indicating a deliberate architectural decision against the shared-component approach.

---

## Decision

### The Editorial Builder SHALL produce complete, self-contained `.astro` files matching the Gold Master specification.

This means:

**Output format:** A single `.astro` file containing the complete HTML document (`<!DOCTYPE html>` through `</html>`), with all CSS in an inline `<style>` block and all JavaScript in an inline `<script is:inline>` block. Zero imports. No shared layouts. No component dependencies.

**Relationship to Gold Master:** The output must match the architecture defined in `docs/GOLD-MASTER-SPEC.md` Section 1 and Section 18 Rule 1. The structural template is `src/pages/reviews/olsp-academy.astro` (for reviews), the blog reference articles (for blog posts), and the roundup reference (for roundups). No new layout system or component library is introduced.

**Relationship to manual Builder:** The manual Builder prompts (`docs/PRODUCTION-MASTER-PROMPT.md`, `docs/BLOG-MASTER-PROMPT.md`, `docs/ROUNDUP-MASTER-PROMPT.md`) define the correct output format. The Editorial Builder agent automates what the manual prompts already do. The agent prompt should describe producing the same output the manual prompts produce.

**Migration strategy:** The Editorial Builder agent is implemented by formalizing the existing manual workflow into an automated prompt. No production files are restructured. No Gold Master spec is rewritten. The existing 30 published pages remain untouched. The migration is operational — the process changes, the output format does not.

### The Editorial Builder SHALL NOT:

- Produce content fragments or body-only output intended for insertion into a separate layout
- Reference `OlspLayout` or any shared layout component that wraps its output
- Depend on imported shared components (`QuoteBanner`, `StandardCta`, `AuthorBox`, `ScoreBars`, `Quiz`, `ComparisonTable`, `ProsCons`, `SvgDiagram`, `VideoEmbed`, `CtaCard`, `RankingTable`, `ProductCard`)
- Generate partial files that require manual assembly with a separate layout system
- Introduce a new presentation layer or layout system

---

## Consequences

### Positive

- **No new components required.** The Gold Master architecture already exists and is proven across 30 pages. The Editorial Builder simply automates what is already done manually.
- **No production disruption.** Existing pages continue to work unchanged. The agent produces output in the same format.
- **No spec rewrite.** The Gold Master spec, blog spec, and roundup spec remain authoritative. The Editorial Builder prompt references them as-is.
- **No dependency risk.** Self-contained files have zero external dependencies. A change to one page never breaks another.
- **Historical precedent respected.** The reverted ArticleNavigation experiment confirms the project's experience with shared components.
- **Fastest path to production.** The agent automates an existing working process. No parallel development of a component system is needed.

### Negative

- **CSS duplication.** Every self-contained file carries the full CSS token set (~80 lines). Changes to the design system require updating every page individually.
- **JavaScript duplication.** Every self-contained file carries the full scroll-spy and mobile TOC script (~40 lines). Same maintenance cost as CSS.
- **No component reuse.** Patterns like FAQ, score bars, and comparison tables are duplicated as HTML in every file rather than shared as components.

### Trade-offs

The primary trade-off is **maintenance cost** (duplicated CSS/JS across 30+ files) versus **architectural simplicity** (zero dependencies, zero build-time assembly). The repository has operated under the self-contained model since inception and has managed updates across all 30 pages successfully (commits `bac24d0`, `a667de6`, `2442aee` applied site-wide changes). The duplicated CSS/JS is approximately 120 lines per file — a known and accepted cost of the self-contained architecture.

---

## Alternatives Considered

### Alternative 1: Component-based architecture (rejected)

The untracked `agents/editorial-builder/PROMPT.md` v2.1 describes outputting body content only, wrapped in an `<OlspLayout>` layout component, with every visual element implemented as an imported component.

**Why considered:** This is the pattern used by most Astro projects. Components are the idiomatic Astro approach. It would eliminate CSS/JS duplication.

**Why rejected:**
1. It contradicts the committed Gold Master spec, which is the production standard
2. It contradicts the committed Editorial Builder PLACEHOLDER.md, which defines the output as a complete Gold Master file
3. It requires building 12+ components (`OlspLayout`, `QuoteBanner`, `StandardCta`, `AuthorBox`, `ScoreBars`, `Quiz`, `ComparisonTable`, `ProsCons`, `SvgDiagram`, `VideoEmbed`, `CtaCard`, `RankingTable`, `ProductCard`) — none of which exist
4. It requires building a new layout system (`src/layouts/OlspLayout.astro`) that does not exist
5. It requires rewriting the Gold Master spec, which explicitly prohibits shared layouts
6. A production experiment with shared components (`ArticleNavigation`) was deployed and reverted within one hour, indicating real-world problems with this approach
7. The draft prompt was never committed, never approved, and has no implementation plan

### Alternative 2: Self-contained architecture (selected)

The Editorial Builder produces complete self-contained `.astro` files matching the existing Gold Master spec.

**Why considered:** This matches every committed specification, every production page, and the historical architecture decision (the ArticleNavigation revert).

**Why selected:**
1. It is the architecture defined by the committed production standard (`docs/GOLD-MASTER-SPEC.md`)
2. It is the architecture described by the committed Editorial Builder PLACEHOLDER.md
3. It is the architecture proven across 30 published pages
4. It is the architecture the manual Builder prompts already define
5. It requires zero new components, zero new layout files, and zero spec rewrites
6. The migration from manual to automated is a process change, not a file format change

---

## Repository Impact

This ADR does not modify any files. The following documents will eventually require updates to align with this decision when implementation begins:

| Document | Required change |
|---|---|
| `agents/editorial-builder/PROMPT.md` (untracked) | Rewrite to describe producing complete self-contained Gold Master files instead of component-based content blocks. Commit the revised version. |
| `agents/editorial-builder/PLACEHOLDER.md` | Update to reference the committed PROMPT.md as the authoritative prompt. |
| `docs/PIPELINE-ARCHITECTURE.md` | Status for Stage 3 (Editorial Builder) can be updated from "Placeholder" once the prompt is committed. |
| `PROJECT-STATUS.md` | Update page counts and pipeline status to reflect current state. |

The following documents are NOT affected by this decision and require no changes:

- `docs/GOLD-MASTER-SPEC.md` — already defines the correct architecture
- `docs/BLOG-MASTER-SPEC.md` — already defines the correct architecture
- `docs/ROUNDUP-GOLD-MASTER-SPEC.md` — already defines the correct architecture
- `docs/PRODUCTION-MASTER-PROMPT.md` — already produces the correct output format
- `docs/BLOG-MASTER-PROMPT.md` — already produces the correct output format
- `docs/ROUNDUP-MASTER-PROMPT.md` — already produces the correct output format
- All files in `src/pages/` — no changes needed
- All files in `src/layouts/` — no changes needed
- All files in `src/components/` — no changes needed
- `agents/opportunity-*/` — no changes needed
- `agents/research-compiler/` — no changes needed
- `agents/editorial-qa/` — no changes needed
- `agents/publisher/` — no changes needed

---

## Future Work

This ADR enables the following implementation work:

1. **Rewrite and commit `agents/editorial-builder/PROMPT.md`** to describe producing complete self-contained Gold Master files. Update or replace `PLACEHOLDER.md` to reference the committed prompt.

2. **Implement the Editorial Builder agent** using the committed prompt. The agent reads a research package (Opportunity Brief or Knowledge Asset) and writes a complete `.astro` file to the correct `src/pages/` directory.

3. **Design Editorial QA (Stage 4)** with the knowledge that QA validates complete self-contained files against the Gold Master spec — not content blocks against a component contract.

4. **Design Publisher (Stage 5)** with standard git commit/push mechanics.

5. **Update PROJECT-STATUS.md** to reflect current page counts and pipeline status.

6. **Optionally standardize 13 older blog pages** to the QuoteBanner + Standard CTA pattern (content normalization, not architecture).

---

Pending Product Owner Approval

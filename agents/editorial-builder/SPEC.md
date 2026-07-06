# Editorial Builder Agent — Specification

## 1. Purpose

This document specifies the operational requirements for the Editorial Builder Agent V1. It defines inputs, outputs, workflow, constraints, and quality standards.

The agent operates as Stage 3 of the two-track pipeline (PIPELINE-ARCHITECTURE.md) and Stage 7 of the AI Editorial Operating System (Content Production). Its sole function is to transform an approved Research Brief (Heavy pipeline) or Opportunity Brief (Light pipeline) into a complete, publication-ready article file.

It does not conduct research, validate facts, or make editorial decisions.

---

## 2. Authority

```
docs/WHY.md
docs/AI-EDITORIAL-OPERATING-SYSTEM.md
docs/AGENT-CONTRACT.md
docs/EDITORIAL-OBJECT-MODEL.md
    ↓
docs/GOLD-MASTER-SPEC.md           (all article types — layout, CSS tokens, JS, components)
docs/ROUNDUP-GOLD-MASTER-SPEC.md    (for roundup-type articles)
docs/BLOG-MASTER-SPEC.md            (for informational/blog articles)
    ↓
agents/editorial-builder/SPEC.md   ← this document
    ↓
agents/editorial-builder/PROMPT.md
    ↓
Runtime execution
```

If any conflict arises, the higher document wins.

---

## 3. Inputs

The Editorial Builder Agent may receive input from two possible upstream paths:

### Light Pipeline — Opportunity Brief

| Input | Format | Required | Description |
|-------|--------|----------|-------------|
| Opportunity Brief | Markdown document | Yes | Keyword scoring, editorial decision, section structure from ORA |
| Seed keyword | String | Yes | Original keyword that generated this opportunity |
| Content type | Enum | Yes | informational, how-to, guide, listicle, comparison |

### Heavy Pipeline — Knowledge Asset Citation

| Input | Format | Required | Description |
|-------|--------|----------|-------------|
| Research Brief | Markdown document | Yes | Complete research package from Research Compiler |
| Knowledge Asset entry | Registry reference | Yes | Entry from `docs/HEAVY-ASSET-LIBRARY.md` |
| Content type | Enum | Yes | review, roundup, pillar, comparison |

### Common Inputs

| Input | Format | Required | Description |
|-------|--------|----------|-------------|
| Gold Master Spec | GOLD-MASTER-SPEC.md | Required | Layout, CSS tokens, JS, components |
| Reference Article | `.astro` file | Required | `src/pages/reviews/olsp-academy.astro` for CSS/JS verbatim copy |

---

## 4. Output

| Output | Format | Location | Description |
|--------|--------|----------|-------------|
| Complete article file | `.astro` | `src/pages/{section}/{slug}.astro` | Standalone, publication-ready page |

### File location by content type

| Content Type | Location |
|---|---|
| Review | `src/pages/reviews/{slug}.astro` |
| Blog / informational | `src/pages/blog/{slug}.astro` |
| Roundup | `src/pages/roundups/{slug}.astro` |
| Investigation | `src/pages/{slug}.astro` |

---

## 5. Workflow

### Step 1: Validate inputs
Verify required inputs are present. If not, stop and report.

### Step 2: Determine article structure
- Reviews: fixed section order from GOLD-MASTER-SPEC.md
- Blog/informational: section structure from template or brief
- Roundups: section order from ROUNDUP-GOLD-MASTER-SPEC.md

### Step 3: Map evidence to sections
Identify which claims from the brief are relevant to each section.

### Step 4: Write each section
Use only evidence from the brief. No invention. Label claims by reliability.

### Step 5: Assemble complete file
- Add Astro frontmatter with `export const prerender = true`
- Copy CSS verbatim from Gold Master reference article
- Copy JS verbatim from Gold Master reference article
- Include all required Gold Master components
- No layout imports, no component imports, no shared CSS

### Step 6: Self-review
Verify every factual claim traces to the brief. Verify knowledge gaps treated per instructions.

---

## 6. Gold Master Compliance (all article types)

| Element | Requirement |
|---|---|
| Astro frontmatter | `export const prerender = true`, `pageTitle`, `pageDescription` |
| CSS | Copy entire `<style>` block verbatim from `src/pages/reviews/olsp-academy.astro` |
| JS | Copy entire `<script is:inline>` tag verbatim from reference article |
| Canonical URL | Absolute with trailing slash |
| External links | Non-affiliate: `target="_blank" rel="noopener noreferrer"`. Affiliate/sponsored: `rel="noopener noreferrer sponsored"`. Internal: no target/rel |
| Sources | `<ul class="pill-list">` with pill-shaped source links |

---

## 7. Constraints

1. Never conduct additional research. The brief is the sole source of facts.
2. Never invent facts, statistics, quotes, or data.
3. Never fill a knowledge gap with an assumption.
4. Never modify the brief.
5. Never perform Editorial QA — produce a draft, not an approved article.
6. Respect the section structure from the brief or template.

---

## 8. Next Stage

**Stage:** Editorial QA (Stage 4)

**Handoff includes:**
- Complete article file
- Brief (for QA cross-reference)
- Any open questions for QA

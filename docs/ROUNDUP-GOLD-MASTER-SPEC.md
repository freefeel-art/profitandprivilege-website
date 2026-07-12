# Roundup Content Specification

**Layout / CSS / JavaScript:** The universal Gold Master standard defined in `docs/GOLD-MASTER-SPEC.md`. The OLSP Academy review (`src/pages/reviews/olsp-academy.astro`) is the canonical reference for layout, CSS token set, responsive breakpoint, and `<script is:inline>` behavior. Copy the `<style>` block and `<script is:inline>` block verbatim from the most recent published roundup (which inherits from the Gold Master).

This document describes only the **content structure** specific to roundup articles.

---

## Purpose

A roundup article compares multiple products, tools, services, or platforms to help readers choose the most appropriate option for their needs.

Unlike a review article, a roundup provides editorial comparisons rather than a deep analysis of a single product.

The primary purpose is to educate readers while naturally directing them to detailed individual reviews where appropriate.

---

# Editorial Principles

Every roundup must:

- distinguish verified facts from vendor claims
- clearly separate editorial analysis from sourced information
- avoid invented testing or personal experience
- avoid fabricated testimonials or case studies
- remain objective and evidence-based
- link to primary sources whenever practical
- solve the reader's problem first; introduce the OLSP ecosystem naturally as the logical next step
- never become a sales page

---

# Content Structure

## 1. Introduction

- Who the guide is for
- What products are covered
- How products were selected

---

## 2. Quick Comparison Table

Include:

- Product
- Best For
- Pricing
- Key Strength
- Overall Verdict

---

## 3. Individual Product Sections

Each product includes:

- Overview
- Best for
- Key features
- Pricing
- Advantages
- Limitations
- Editorial analysis
- Link to full review (if available)

---

## 4. Comparison Section

Compare products using practical criteria such as:

- Ease of use
- Pricing
- Features
- Scalability
- Beginner friendliness
- Value

---

## 5. Best Choice By Scenario

Examples:

- Best Overall
- Best for Beginners
- Best Budget Choice
- Best for Advanced Users
- Best Long-Term Value

---

## 6. Alternatives

Mention additional products that may suit specific situations.

---

## 7. Decision Guide

Provide a simple decision flow or quiz helping readers select the most suitable option.

---

## 8. FAQ

Minimum four questions.

---

## 8a. Author Box

Include an Author Box immediately before the Sources section.

Use `src/pages/authors/jarmo-halonen.astro` as the single source of truth. Do not invent or rewrite author information.

The Author Box must include:

- Author photo (`/assets/authors/jarmo-halonen-author.png`)
- Author name
- Role / title
- Short biography (2–4 sentences drawn from the author profile)
- Link to `/authors/jarmo-halonen/`

Use the `.author-box` CSS component (defined in the roundup `<style>` block). The author profile page remains the canonical source for all future articles.

---

## 9. Sources

Sources must be formatted as a `<ul class="pill-list">` (see Gold Master Spec Section 8.12). Each source is a pill-shaped link. Prefer:

- Official documentation
- Vendor documentation
- Independent sources
- Community discussions

Include the `.pill-list` CSS in the article's `<style>` block. The disclaimer paragraph follows the pill-list.

---

## 10. Call To Action

Include two identical `.cta-card` components (see Gold Master Spec Section 8.13) placed at:
1. CTA #1: After the introduction section — in the upper visible part of the article
2. CTA #2: Near the conclusion before the Sources section

The CTA card promotes the recommended product from the roundup with a heading, body copy, button link (`target="_blank" rel="noopener noreferrer sponsored"` pointing to `https://olspacademy.com/megalive/1006001`), and affiliate disclosure. Both cards are identical. Include the `.cta-card` and `.cta-btn` CSS in the article's `<style>` block.

---

# SEO Rules

Every roundup must:

- include the primary keyword naturally
- use descriptive H2 headings
- contain internal links to related reviews
- include relevant supporting articles
- avoid keyword stuffing

---

# Content Rules

Do NOT:

- invent testing
- invent screenshots
- invent testimonials
- invent benchmarks
- exaggerate conclusions

Always:

- distinguish verified facts
- distinguish vendor claims
- distinguish independent opinions

---

# Build Requirements

Every generated roundup must:

- build successfully
- preserve the Gold Master architecture
- pass QA before publication

---

# Architecture Notes

## File location

Roundup pages live at:

```
src/pages/roundups/[slug].astro
```

## Layout / CSS / JS

The Gold Master standard from `docs/GOLD-MASTER-SPEC.md` applies. Use the two-column grid, CSS token set, responsive breakpoint, sticky TOC, scroll-spy, and `<script is:inline>` block exactly as defined by the Gold Master.

## Quiz logic

The roundup quiz uses per-question matching, not a cumulative score threshold:

- One question per platform being compared (value `2` = yes, `0` = no)
- Results show which platforms match the reader's stated goals
- Three outcomes: no match → Alternatives section; one match → named platform; multiple matches → compare free tiers

---

# QA Checklist

- Complete comparison table
- Individual sections for every platform covered
- Author Box present before Sources section (sourced from `src/pages/authors/jarmo-halonen.astro`)
- Two `.cta-card` components present: CTA #1 post-intro, CTA #2 before Sources — both identical
- CTA card uses `.cta-btn` with `target="_blank" rel="noopener noreferrer sponsored"` pointing to `https://olspacademy.com/megalive/1006001` and affiliate disclosure
- Sources section uses `<ul class="pill-list">` with pill-shaped source links
- Site footer (`<footer class="site-footer">`) present inside `<main>` after Sources
- `.cta-card`, `.cta-btn`, `.pill-list`, `.site-footer` CSS included in `<style>` block
- Internal links verified — at least one contextual link to an OLSP pillar article
- FAQ included (minimum four questions)
- Sources section uses Trustpilot links for competing platforms plus any supplied affiliate/official links
- All external links include `target="_blank"`; affiliate links use `target="_blank" rel="noopener noreferrer sponsored"`; non-affiliate external links use `target="_blank" rel="noopener noreferrer"`
- Editorial neutrality maintained — article solves reader's problem first, OLSP introduced naturally
- `<script is:inline>` directive present
- Build successful (`npm run build`)
- Ready for Playwright QA

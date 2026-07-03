# Roundup Master Prompt

## How to Use This Document

Generate a production-ready Astro roundup article. The layout, CSS, and JavaScript follow the **universal Gold Master standard** defined in `docs/GOLD-MASTER-SPEC.md` and `docs/PRODUCTION-MASTER-PROMPT.md`. The editorial content pattern (CTA cards, pill-list sources, site footer) follows the approved production reference article at `src/pages/blog/part-time-jobs-near-me-no-experience.astro`. This document describes only the roundup-specific content structure.

Generate roundups using the universal builder (`docs/PRODUCTION-MASTER-PROMPT.md`) with Article Type set to `roundups`. Use this document as the content-structure guide within the research package.

Do not redesign the architecture.

---

# Task

Generate a complete production-ready roundup article comparing multiple products, tools, services, or platforms.

The objective is to help readers choose the best option based on their specific needs while maintaining editorial neutrality.

---

# Required Inputs

You will receive:

- Research Brief (see `docs/research/` — the canonical location for Research Briefs)
- Target keyword
- Canonical URL
- Author
- Publication date

---

# Generation Instructions

## Step 1 — Read before writing

Read:

- ROUNDUP-GOLD-MASTER-SPEC.md
- Research Brief

Do not begin writing until both documents have been analyzed.

---

## Step 2 — Plan the article

Produce the article using the following structure:

1. Introduction
2. Quick Comparison Table
3. Individual Product Reviews
4. Feature Comparison
5. Best For Scenarios
6. Alternatives
7. Decision Guide / Quiz
8. FAQ
9. Sources
10. Call To Action

---

## Step 3 — Editorial Standards

Always distinguish:

- Verified Facts
- Vendor Claims
- Independent Opinions
- Editorial Analysis

Never invent:

- Testing
- Personal experience
- Screenshots
- Testimonials
- Benchmarks

Whenever practical, verify information using original sources.

---

## Step 4 — Internal Linking

Whenever detailed reviews exist:

Link naturally to the corresponding review pages.

Whenever supporting informational articles exist:

Link naturally where relevant.

---

## Step 5 — Output

Produce a production-ready Astro page.

Preserve the Gold Master structure. Include:
- Three identical `.cta-card` components (post-intro, mid-article, before Sources) — see Gold Master Spec Section 8.13
- Sources section as `<ul class="pill-list">` — see Gold Master Spec Section 8.12
- `<footer class="site-footer">` inside `<main>` after Sources — see Gold Master Spec Section 8.14
- `.cta-card`, `.cta-btn`, `.pill-list`, `.site-footer` CSS in the `<style>` block

---

# SEO Rules

The article must:

- satisfy search intent
- include the primary keyword naturally
- use descriptive headings
- include internal links
- avoid keyword stuffing

---

# Pre-Delivery Checklist

Before completion confirm:

- Gold Master architecture preserved
- Three `.cta-card` components present (post-intro, mid-article, before Sources) — all identical
- Sources section uses `<ul class="pill-list">`
- Author Box present immediately before Sources section (sourced from `src/pages/authors/jarmo-halonen.astro`)
- `<footer class="site-footer">` present inside `<main>` after Sources
- `.cta-card`, `.cta-btn`, `.pill-list`, `.site-footer`, `.author-box` CSS included in `<style>` block
- All external links include `target="_blank"`
- Affiliate links use `target="_blank" rel="noopener noreferrer sponsored"`
- Non-affiliate external links use `target="_blank" rel="noopener noreferrer"`
- External link audit completed (every outbound link checked against the standard above)
- Editorial rules followed
- Internal links verified
- Sources verified
- FAQ completed
- Quiz completed
- Build ready
- Ready for Playwright QA

If any requirement cannot be satisfied, explain why instead of inventing content.

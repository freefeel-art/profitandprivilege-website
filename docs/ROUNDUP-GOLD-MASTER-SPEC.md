# ROUNDUP GOLD MASTER SPECIFICATION

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

Prefer:

- Official documentation
- Vendor documentation
- Independent sources
- Community discussions

---

## 10. Call To Action

Provide a neutral recommendation based on the reader's situation.

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

## Styling

Copy the `<style>` block verbatim from the most recent published roundup. The CSS token set is shared with the review pipeline. Do not change token names or values.

## Scripting

Use `<script is:inline>` — never bare `<script>`. Without `is:inline`, Astro bundles the script as an ES module, removing `evaluateQuiz` from global scope and breaking the quiz button's `onclick` handler.

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
- Internal links verified
- FAQ included (minimum four questions)
- Sources section uses Trustpilot links for competing platforms plus any supplied affiliate/official links
- Affiliate links use `rel="noopener sponsored"`
- Editorial neutrality maintained
- `<script is:inline>` directive present
- Build successful (`npm run build`)
- Ready for Playwright QA

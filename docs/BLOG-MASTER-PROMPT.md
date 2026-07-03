# Blog Master Prompt — Blog/Informational Article Generator

**Version:** 1.0
**Applies to:** `src/pages/blog/[slug].astro`
**Structural reference:** `src/pages/blog/part-time-jobs-near-me-no-experience.astro`
**Metadata reference (OG + JSON-LD):** `src/pages/blog/make-money-online-for-beginners.astro`
**Specification:** `docs/BLOG-MASTER-SPEC.md`

---

## How to Use This Document

Copy everything inside the horizontal rule below (from "## Task" to the end of the checklist) into a new conversation with Claude. Supply all required inputs listed in the Inputs section before asking for output. Do not modify this prompt between articles — if the standard needs to change, update `docs/BLOG-MASTER-SPEC.md` first, then revise this document.

---

---

## Task

You are generating a production-ready Astro blog article page for the website **Profit & Privilege** (`olsp.profitandprivilege.com`). This site publishes independent, research-based reviews, blog posts, and roundups about online business, affiliate marketing, and digital education products. Blog articles are informational — they answer a question or explain a topic, rather than reviewing a single product.

Your output is exactly one complete file:

```
src/pages/blog/[slug].astro
```

**The Gold Master layout is mandatory.** Copy the layout architecture, CSS token set, two-column grid, sticky TOC, scroll-spy JS, and `<script is:inline>` block from `src/pages/reviews/olsp-academy.astro` (via the blog structural reference below). Only the section content and section IDs change per article. For the exact blog content pattern (CTA cards, verdict box, FAQ, author box, pill-list sources, site footer), follow `src/pages/blog/part-time-jobs-near-me-no-experience.astro`. For the metadata block (Open Graph, Twitter Card, JSON-LD), follow `src/pages/blog/make-money-online-for-beginners.astro`.

The file must be ready to build and deploy without any manual structural edits. It must pass `astro build` on first attempt.

---

## Required Inputs

The following inputs must be supplied before you begin. Do not start generating until all of them are present. If any are missing, list what is absent and wait.

| Input | Format | Notes |
|---|---|---|
| **Blog structural reference** | Full file contents of `src/pages/blog/part-time-jobs-near-me-no-experience.astro` | Layout, CSS, JS, and content-pattern template. |
| **Blog Master Specification** | Full contents of `docs/BLOG-MASTER-SPEC.md` | The authoritative rule set. Read it before generating. |
| **Research package** | Freeform text, notes, or pasted source material | Your primary content source. Everything you write must be grounded in this. |
| **Target keyword** | Plain text, e.g. `how to [do thing]` | Used in `<title>`, `<h1>`, and `<meta name="description">`. |
| **Canonical URL** | Full absolute URL with trailing slash, e.g. `https://olsp.profitandprivilege.com/blog/[slug]/` | Hardcoded into `<link rel="canonical">` and the OG/JSON-LD `url` fields. |
| **Publish date** | `YYYY-MM-DD` | Used in `.hero-tag` and JSON-LD `datePublished`/`dateModified`. |
| **Internal links** | List of anchor text + URL pairs, or "none" | Links to other pages on olsp.profitandprivilege.com to weave naturally into the content. Should include at least one link to a review. |
| **Affiliate links** | List of anchor text + URL pairs with tracking parameters, or "none" | Used in the three CTA cards. |

---

## Generation Instructions

### Step 1 — Read before writing

Before producing any output, read the blog structural reference and `docs/BLOG-MASTER-SPEC.md` in full. Confirm you understand:

- Which elements are structural (must be copied verbatim from the Gold Master CSS/JS)
- Which components blog articles use vs. omit (no Methodology Block, Score Bars, Quiz, SVG Diagram, or Video Embed)
- The required OG + JSON-LD metadata block
- The three-CTA-card placement rule

### Step 2 — Plan the content sections

Using the research package, plan 3–7 numbered body sections that answer the target keyword's search intent, plus:

- The verdict box's "Best for" / "Not ideal for" framing
- Whether a data table or pros/cons grid is warranted by the content (both optional — use only if the research supports it)
- 6–8 FAQ questions drawn from the research
- At least one internal link to a review and, where relevant, to sibling blog articles

### Step 3 — Generate the file

Generate the complete `.astro` file from top to bottom, in document order. Do not skip sections. Do not summarise or placeholder any section — every section must contain finished, publishable content.

---

## Structural Rules

These rules are non-negotiable. Violating any of them produces a file that fails the production standard.

**Architecture**
- One self-contained `.astro` file. No imports. No shared layouts. No framework components.
- Frontmatter contains only `export const prerender = true;` — no other consts. Hardcode `<title>` and `<meta name="description">` directly in `<head>`.
- Copy the entire `<style>` block verbatim from the blog structural reference. Do not change any CSS token value, class name, or selector, even for components this article does not use.
- Copy the entire `<script is:inline>` block verbatim, **including the `is:inline` directive**. It powers the mobile TOC toggle and scroll-spy.

**Layout and IDs**
- The `.layout` grid, `<aside>`, `<main>`, and the mobile TOC `<button>` must be present with identical attributes and IDs to the structural reference.
- The `<aside>` must have `id="tocWrap"`. The `<nav>` inside it must have `id="tocNav"`. The `<button>` must have `id="tocToggle"` and the exact label text `☰ Table of Contents`.

**Sections**
- Order: `intro → [3–7 numbered body sections] → faq → author → sources`, per `docs/BLOG-MASTER-SPEC.md` Section 3.
- `intro` must not contain an `<h2>` (it contains the `<h1>` instead). Every other section must open with an `<h2>`.
- Section `id` values may be descriptive-slug or generic (`section-N`) — pick one style and use it consistently. The TOC `<nav>` must list every section with an `href` matching its `id` exactly.

**Components to omit**
- Do not add a Methodology Block, Score Bars, Self-Check Quiz, SVG Diagram, or Video Embed. These are review-only components (`docs/BLOG-MASTER-SPEC.md` Section 4).

**SEO and metadata**
- `<title>` and `<meta name="description">` are hardcoded, not interpolated. Both must contain the target keyword.
- `<link rel="canonical">` must be the exact canonical URL supplied in the inputs — absolute, trailing slash.
- Include the full OG + Twitter Card + JSON-LD block per `docs/BLOG-MASTER-SPEC.md` Section 5. OG/Twitter title and description must exactly match `<title>` and `<meta name="description">`. JSON-LD `FAQPage.mainEntity` must contain every FAQ question, in order, matching the `#faq` section text.
- Do not add a `<header>` or site navigation.

**Links**
- Every external link (any `href` not starting with `/`) must include `target="_blank" rel="noopener noreferrer"`.
- Affiliate or CTA links must use `target="_blank" rel="noopener noreferrer sponsored"`.
- Internal links (href starting with `/`) must NOT have a `target` or `rel` attribute.
- The active CTA destination is `https://olspacademy.com/megalive/1006001`.

---

## Content and Editorial Rules

Same source-fidelity, epistemic-labelling, income-claims, no-first-hand-testing, and tone rules as `docs/PRODUCTION-MASTER-PROMPT.md` ("Content and Editorial Rules" section) apply unchanged to blog articles. In summary:

- The research package is the primary and only source. Do not invent facts, figures, or names not present in it.
- Label every factual claim as verified, vendor claim, third-party reported, unverifiable, or self-reported, as appropriate.
- Any income or earnings figure must be labelled self-reported/unverified and never presented as typical or guaranteed. Use `.callout.warn` when surfacing these prominently.
- Do not write as though the editorial team personally tested anything unless the research package documents it.
- Tone: measured, direct, consumer-protective. No hype, no superlatives.

---

## Component Rules

**Hero tag:** A short descriptive label + `· Updated [Month Year]` using the supplied publish date.

**Verdict box:** "Best for" and "Not ideal for" must be grounded in the research and specific to the topic, not generic.

**Tables (optional):** Use when the research supports structured comparison data (pay ranges, feature comparisons, etc.). Wrap in `.table-scroll`.

**Pros & cons grid (optional):** Use `.two-col` / `.pc-card` only when the content genuinely compares options or methods.

**FAQ:** 6–8 questions minimum four, drawn directly from the research — real questions people ask about this topic. Every question here must also appear in the JSON-LD `FAQPage.mainEntity` array, verbatim.

**Author Box:** Use the same markup and source as `docs/ROUNDUP-GOLD-MASTER-SPEC.md` Section 8a — sourced from `src/pages/authors/jarmo-halonen.astro`, includes photo, name, role, bio, and profile link.

**CTA cards:** Insert three identical `.cta-card` components:
1. Immediately after the `intro` section.
2. Mid-article, roughly at the midpoint of the numbered body sections.
3. After the FAQ section, immediately before the Author Box.
All three must be identical in content. Include `.cta-card` and `.cta-btn` CSS in the article's `<style>` block (already present if copied verbatim from the structural reference).

**Pill-list sources:** Format Sources & References as `<ul class="pill-list">`, each source a pill-shaped `<li><a>`. End with the disclaimer paragraph in small print, referencing the current month/year.

**Site footer:** End every article with `<footer class="site-footer">` inside `<main>`, after Sources. Left span reads "Profit and Privilege — independent research since 2025". Right link points to `https://olsp.profitandprivilege.com`.

**Internal links:** Weave supplied internal links naturally into body copy. Include at least one link to a review page. Do not create a separate "related articles" block.

---

## Output Specification

Produce exactly one output: the complete, finished content of the file `src/pages/blog/[slug].astro`.

- Output the raw file content only.
- Do not add explanatory prose, section commentary, or notes before or after the file.
- Do not use a code fence unless the user's interface requires it. If you do use a code fence, use ` ```astro ` as the language identifier.
- The file must be complete from the opening `---` frontmatter fence to the closing `</html>` tag.
- Do not truncate any section. Do not use placeholder text such as `<!-- TODO -->` or `[INSERT CONTENT HERE]`.

---

## Pre-Delivery Checklist

Before outputting the file, verify each item in `docs/BLOG-MASTER-SPEC.md` Section 9. If any item fails, fix it before delivering.

## Research Source Policy

- Secondary sources (blogs, reviews, and AI-generated summaries) may be used to discover topics, claims, and original references.
- Whenever practical, verify information using the original source before publication.
- Prefer citing official documentation, reputable third-party sources, and primary sources instead of another blog or review article.
- Do not cite another blog/review when the same information is available from an original or official source.

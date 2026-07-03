# Production Master Prompt — Article Generator

**Version:** 2.0  
**Applies to:** `src/pages/{type}/[slug].astro` — where `{type}` is `reviews`, `blog`, or `roundups`  
**Gold Master (structural template):** `src/pages/reviews/olsp-academy.astro`  
**Approved production reference article:** `src/pages/blog/part-time-jobs-near-me-no-experience.astro`  
**Specification:** `docs/GOLD-MASTER-SPEC.md`

---

## How to Use This Document

Copy everything inside the horizontal rule below (from "## Task" to the end of the checklist) into a new conversation with Claude. Supply all required inputs listed in the Inputs section before asking for output. Do not modify this prompt between articles — if the standard needs to change, update `docs/GOLD-MASTER-SPEC.md` first, then revise this document.

---

---

## Task

You are generating a production-ready Astro article page for the website **Profit & Privilege** (`olsp.profitandprivilege.com`). This site publishes independent, research-based reviews, blog posts, and roundups about online business, affiliate marketing, and digital education products.

Your output is exactly one complete file:

```
src/pages/{type}/[slug].astro
```

Where `{type}` is `reviews`, `blog`, or `roundups` depending on the article type specified in the inputs.

**The Gold Master layout is mandatory for every article type.** Copy the layout architecture, CSS token set, two-column grid, sticky TOC, scroll-spy JS, and `<script is:inline>` block from `src/pages/reviews/olsp-academy.astro`. Only the section content and section IDs change per article type. The visual identity (typography, spacing, tokens, breakpoint) must remain identical to the Gold Master. For the editorial content pattern (CTA cards, pill-list sources, site footer), follow the approved production reference article at `src/pages/blog/part-time-jobs-near-me-no-experience.astro`.

The file must be ready to build and deploy without any manual structural edits. It must pass `astro build` on first attempt.

---

## Required Inputs

The following inputs must be supplied before you begin. Do not start generating until all of them are present. If any are missing, list what is absent and wait.

| Input | Format | Notes |
|---|---|---|
| **Article type** | `reviews`, `blog`, or `roundups` | Determines the output directory and section structure. |
| **Gold Master file** | Full file contents of `src/pages/reviews/olsp-academy.astro` | The structural template. Copy its layout, CSS, and JS exactly. |
| **Gold Master Specification** | Full contents of `docs/GOLD-MASTER-SPEC.md` | The authoritative rule set. Read it before generating. |
| **Research package** | Freeform text, notes, or pasted source material | Your primary content source. Everything you write must be grounded in this. |
| **Target keyword** | Plain text, e.g. `what is [product name]` | Used in `<title>`, `<h1>`, and `<meta name="description">`. |
| **Canonical URL** | Full absolute URL with trailing slash, e.g. `https://olsp.profitandprivilege.com/{type}/[slug]/` | Hardcoded into `<link rel="canonical">`. |
| **Internal links** | List of anchor text + URL pairs, or "none" | Links to other pages on olsp.profitandprivilege.com to weave naturally into the content. |
| **Author bio** | 1–3 sentences describing the editorial team or author | Used in the methodology block. |
| **Affiliate links** | List of anchor text + URL pairs with tracking parameters, or "none" | Placed only in the Sources section with `rel="noopener sponsored"`. |

---

## Generation Instructions

### Step 1 — Read before writing

Before producing any output, read the Gold Master file and the Gold Master Specification in full. Confirm you understand:

- Which elements are structural (must be copied verbatim)
- Which elements are per-article content (must be rewritten for the specific topic)
- The complete section order and fixed `id` values
- The JavaScript dependencies on specific `id` attributes

### Step 2 — Plan the content sections

Using the research package, plan the specific content for each of the 12 sections before generating HTML. Identify:

- The product's core mechanic (for the SVG diagram)
- The pricing structure (for the Overview table)
- The 2–4 competitors for the Comparison table
- 4 pros and 4 cons grounded in the research
- 4 scoring categories appropriate to this product
- 3 quiz questions that reflect this product's real decision factors
- 4 FAQ questions drawn from the research
- The third-party YouTube video URL (or note its absence)
- All source URLs and their affiliate status

### Step 3 — Generate the file

Generate the complete `.astro` file from top to bottom, in document order. Do not skip sections. Do not summarise or placeholder any section — every section must contain finished, publishable content.

---

## Structural Rules

These rules are non-negotiable. Violating any of them produces a file that fails the production standard.

**Architecture**
- One self-contained `.astro` file. No imports. No shared layouts. No framework components.
- First line of frontmatter: `export const prerender = true;`
- Declare `const pageTitle` and `const pageDescription` in frontmatter, but hardcode the actual `<title>` and `<meta name="description">` in `<head>`.
- Copy the entire `<style>` block verbatim from the Gold Master. Do not change any CSS token value, any class name, or any selector. Only the HTML content changes.
- Copy the entire `<script is:inline>` block verbatim from the Gold Master, **including the `is:inline` directive**. The JS is structural. Do not modify it and do not drop `is:inline`. Without it, Astro bundles the script as an ES module, removing `evaluateQuiz` from global scope and silently breaking the quiz button's `onclick` handler.

**Layout and IDs**
- The `.layout` grid, `<aside>`, `<main>`, and the mobile TOC `<button>` must be present with identical attributes and IDs to the Gold Master.
- The `<aside>` must have `id="tocWrap"`. The `<nav>` inside it must have `id="tocNav"`. The `<button>` must have `id="tocToggle"` and the exact label text `☰ Table of Contents`.
- The quiz result container must have `id="quiz-result"`. The quiz wrapper must have `id="quizBox"`.

**Sections**
- Sections must appear in this order: `intro → overview → design → performance → ux → comparison → proscons → history → recommend → buy → verdict → faq → sources`
- Each `<section>` must have its fixed `id` attribute. Do not rename any section id.
- The `intro` section must not contain an `<h2>`. Every other section must open with an `<h2>`.
- The TOC `<nav>` must list every section with an `href` that matches the section `id`.

**Score bars**
- Percentage widths must match the displayed fraction exactly: 5/5 = 100%, 4/5 = 80%, 3/5 = 60%, 2/5 = 40%, 1.5/5 = 30%, 1/5 = 20%.

**Quiz**
- Exactly three questions, using radio groups named `q1`, `q2`, `q3`.
- Answer values: `2` for the aligned answer, `0` for the misaligned answer.
- Outcome thresholds: score `≥ 5` = good fit, `≥ 3` = mixed fit, `< 3` = poor fit.

**SEO**
- `<title>` and `<h1>` must be different strings. Both must contain the target keyword.
- `<link rel="canonical">` must be the exact canonical URL supplied in the inputs — absolute, with trailing slash.
- Do not add JSON-LD, Open Graph tags, or Twitter Card tags. They are not part of the Gold Master standard.
- Do not add a `<header>` or site navigation. A `<footer class="site-footer">` is required on every production article (see CTA card, pill-list sources, and site footer instructions below).
- The `<footer class="site-footer">` must be placed inside `<main>`, **after** the `sources` section and **before** `</main>`.

**Links**
- Every external link (any `href` not starting with `/`) must include `target="_blank"`.
- Affiliate or tracking links must use `target="_blank" rel="noopener noreferrer sponsored"`.
- External non-affiliate links must use `target="_blank" rel="noopener noreferrer"`.
- Internal links (href starting with `/`) must NOT have a `target` or `rel` attribute.
- The active CTA destination is `https://olspacademy.com/megalive/1006001`.

---

## Content and Editorial Rules

These rules govern the writing inside the structural shell.

**Source fidelity**
- The research package is your primary and only source. Do not supplement it with facts from your training data unless you explicitly label them as general background knowledge that could not be confirmed from the research.
- Do not invent product details, pricing figures, feature descriptions, or the name of any person associated with the product unless they appear in the research package.

**Epistemic labelling**
Every factual claim must carry one of the following labels, either explicitly in the prose or clearly implied by the sentence structure:

| Category | How to signal it |
|---|---|
| Verified independently | State it plainly as fact, with the source noted |
| Vendor claim / marketing copy | "According to the official site…", "The product is marketed as…", "The company claims…" |
| Third-party reported | "Independent reviewers describe…", "Multiple sources report…", "One third-party review cited…" |
| Could not be verified | "We could not independently confirm…", "This could not be verified at the time of writing…" |
| Self-reported / unaudited | "Self-reported by individual members…", "Not independently audited…" |

Do not state anything as verified fact if it comes only from the vendor's own marketing copy or from a source with a financial incentive to promote sign-ups.

**Income and earnings claims**
Any income figure, earnings example, or result claim found in the research package must be explicitly labelled as self-reported and unverified. Use `.callout.warn` when surfacing these claims prominently. Never present an income figure as a typical or guaranteed result.

**No first-hand testing**
Do not write as though you or the editorial team personally used, purchased, or tested the product unless the research package explicitly includes a first-hand account to draw from. The methodology block must accurately describe how the research was conducted.

**Tone**
The site's editorial voice is measured, direct, and consumer-protective. It acknowledges what is unknown. It does not hype, condemn, or use superlatives. It treats the reader as an intelligent adult who will make their own decision.

---

## Component Rules

Apply these rules when populating each component.

**Hero tag:** `Independent Review · Updated [Month Year]` — use the current month and year.

**Verdict box:** "Best for" and "Not ideal for" must be grounded in the research, not generic. They must reflect the specific product's audience and model.

**Methodology block:** Use the supplied author bio. The "How this review was built" paragraph must accurately describe the research method used — desk research, supplied materials, or otherwise. Do not claim first-hand access unless the research package documents it.

**Pricing table:** Mark all pricing as reported/unconfirmed if the research package does not include a screenshot or direct purchase confirmation. Use `.callout.warn` above the table.

**Comparison table:** Include the product being reviewed in the first row. Include two or three genuine alternatives. The alternatives must be real, named products or platforms — not generic placeholders.

**Pros & cons:** Four items on each side minimum. Each item must be a specific observation, not a generic marketing sentence. Cons must be genuine cautions, not softened to the point of being meaningless.

**SVG diagram:** Create an original diagram that illustrates the product's core mechanic or earning structure. It must not be a copy of the OLSP diagram. It must have `role="img"` and `aria-label`. The `<figcaption>` must state it is an original illustration, not a screenshot.

**Score bars:** Choose 4–5 scoring categories that are meaningful for this specific product type. Name them appropriately. Do not copy the OLSP category names if they do not fit.

**Quiz:** Three questions must reflect the actual decision factors for this product — not generic questions about affiliate marketing. Each question must have a clear "aligned" and "misaligned" answer.

**FAQ:** Four questions minimum. Questions must come from the research — things real people ask about this product. Do not invent questions that the research does not address.

**Video embed:** Use the YouTube URL from the research package. If none is supplied, omit the video embed and the "Video Content" subsection heading, but retain the sources `<ul>` and disclaimer paragraph.

**Sources section:** Every external link cited in the body copy must appear in the sources list. Affiliate links go in this section with `target="_blank" rel="noopener noreferrer sponsored"`. Non-affiliate source links use `target="_blank" rel="noopener noreferrer"`. The disclaimer paragraph must reference the current month and year and note that information may not be current.

**Internal links:** If internal links are supplied in the inputs, weave them naturally into relevant body copy sections. Do not create a separate "related articles" block.

**CTA cards:** Insert three identical `.cta-card` components (see Gold Master Spec Section 8.13) in the article:
1. Immediately after the `intro` section, before the first content section.
2. Mid-article, after approximately the fifth content section (before comparison/pros-cons).
3. Immediately before the Sources section.
All three cards must be identical in content. Customise the heading, body paragraphs, link, and disclosure for the product being promoted. Include the `.cta-card` and `.cta-btn` CSS in the article's `<style>` block (see approved reference article).

**Pill-list sources:** Format the Sources & References section as a `<ul class="pill-list">` with each source as a pill-shaped `<li><a>` tag. Include the `.pill-list` CSS in the article's `<style>` block. Follow the approved reference article for structure and styling.

**Site footer:** End every article with `<footer class="site-footer">` inside `<main>`, after the Sources section. Include the `.site-footer` CSS in the article's `<style>` block. The left span reads "Profit and Privilege — independent research since 2025". The right link points to `https://olsp.profitandprivilege.com`.

---

## Output Specification

Produce exactly one output: the complete, finished content of the file `src/pages/{type}/[slug].astro`.

- Output the raw file content only.
- Do not add explanatory prose, section commentary, or notes before or after the file.
- Do not use a code fence unless the user's interface requires it. If you do use a code fence, use ` ```astro ` as the language identifier.
- The file must be complete from the opening `---` frontmatter fence to the closing `</html>` tag.
- Do not truncate any section. Do not use placeholder text such as `<!-- TODO -->` or `[INSERT CONTENT HERE]`.

---

## Pre-Delivery Checklist

Before outputting the file, verify each item. If any item fails, fix it before delivering.

**Architecture**
- [ ] `export const prerender = true;` is the first frontmatter statement
- [ ] `pageTitle` and `pageDescription` are declared in frontmatter
- [ ] `<title>` and `<meta name="description">` are hardcoded strings in `<head>`, not interpolated
- [ ] No imports of any kind appear in the frontmatter
- [ ] The `<style>` block is copied verbatim from the Gold Master
- [ ] The `<script is:inline>` block is copied verbatim from the Gold Master, with the `is:inline` directive present

**Structure**
- [ ] All 13 sections are present in the correct order
- [ ] All section `id` values match the fixed names in the specification
- [ ] `intro` has no `<h2>`; all other sections open with `<h2>`
- [ ] `#tocWrap`, `#tocNav`, `#tocToggle`, `#quizBox`, `#quiz-result` are all present
- [ ] TOC has a link for every section

**Content**
- [ ] `<title>` ≠ `<h1>` (they are different strings)
- [ ] Both `<title>` and `<h1>` contain the target keyword
- [ ] `<link rel="canonical">` matches the supplied canonical URL exactly
- [ ] `.hero-tag` contains the current month and year
- [ ] `.methodology` block is present in `#intro`
- [ ] `.verdict-box` is present in `#intro` after the opening paragraph
- [ ] Pricing table is preceded by a `.callout.warn` if pricing is unconfirmed
- [ ] Pros and cons have at least four items each
- [ ] Score bar percentages match their displayed fractions
- [ ] Quiz has exactly three fieldsets using `q1`, `q2`, `q3`
- [ ] FAQ has at least four `<details>` items
- [ ] SVG diagram has `role="img"` and `aria-label`
- [ ] SVG `<figcaption>` states it is an original illustration
- [ ] `<iframe>` has a `title` attribute
- [ ] All external links include `target="_blank"`
- [ ] Affiliate links use `target="_blank" rel="noopener noreferrer sponsored"`
- [ ] Non-affiliate external links use `target="_blank" rel="noopener noreferrer"`
- [ ] Sources section ends with the disclaimer paragraph in small print
- [ ] No income or earnings figures are presented as verified or typical results
- [ ] No first-hand testing is claimed unless the research package documents it
- [ ] No Open Graph tags, JSON-LD, `<header>`, or site navigation are present (per Gold Master standard)
- [ ] `<footer class="site-footer">` is present inside `<main>`, after `#sources`, with brand tagline and domain link
- [ ] Three `.cta-card` components are present: after `#intro`, mid-article, and before `#sources` — all identical
- [ ] `.cta-card` includes heading, body copy, `.cta-btn` link pointing to `https://olspacademy.com/megalive/1006001` with `target="_blank" rel="noopener noreferrer sponsored"`, and affiliate disclosure paragraph
- [ ] Sources section uses `<ul class="pill-list">` with pill-shaped source links
- [ ] `.cta-card`, `.cta-btn`, `.pill-list`, and `.site-footer` CSS are included in the `<style>` block

## Research Source Policy

- Secondary sources (blogs, reviews, and AI-generated summaries) may be used to discover products, claims, and original references.
- Whenever practical, verify information using the original source before publication.
- Prefer citing official documentation, reputable third-party sources, and primary sources instead of another review article.
- Do not cite another review when the same information is available from an original or official source.

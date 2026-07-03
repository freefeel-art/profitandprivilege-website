# Gold Master Specification

**Source file (structural template):** `src/pages/reviews/olsp-academy.astro`
**Approved production reference article:** `src/pages/blog/part-time-jobs-near-me-no-experience.astro`
**Purpose:** This document defines the production standard for every future article on this site — reviews, blog posts, and roundups. Treat the approved production reference article as the canonical reference implementation for editorial content, CTAs, sources formatting, and the site footer. The OLSP Academy review remains the structural template for layout, CSS tokens, and JavaScript. Do not modify either file.

---

## 1. Page Architecture

Every article is a **standalone `.astro` file** placed in the appropriate subdirectory of `src/pages/`. There are no shared layout imports, no component imports, and no framework components. The file is entirely self-contained: CSS, HTML, and JavaScript all live in the same file. The Gold Master layout, CSS token set, and JavaScript behavior apply identically to all article types.

```
src/pages/reviews/
  olsp-academy.astro   ← Gold Master (canonical reference)
  [slug].astro         ← copies this structure

src/pages/blog/
  [slug].astro          ← copies this structure

src/pages/roundups/
  [slug].astro          ← copies this structure
```

The Astro frontmatter contains exactly two variables:

```astro
export const prerender = true;

const pageTitle = "...";
const pageDescription = "...";
```

`prerender = true` ensures Astro generates a static HTML file at build time. The `pageTitle` and `pageDescription` variables are declared in frontmatter for documentation purposes, but the actual `<title>` and `<meta name="description">` tags are written directly in the `<head>` with their final strings — they are not interpolated from these variables.

---

## 2. HTML Document Structure

The file renders a complete HTML5 document:

```
<!DOCTYPE html>
<html lang="en">
  <head>      — meta, canonical, inline <style>
  <body>
    <div class="layout">
      <button class="mobile-toc-btn">  — mobile TOC toggle
      <aside class="toc-wrap">         — sticky Table of Contents
      <main>                           — all article content in <section> blocks
    </div>
    <script>                           — inline vanilla JS
```

A `<footer class="site-footer">` is present at the bottom of `<main>`, after the `sources` section. No `<header>` or site-wide navigation is present. Each article is a standalone editorial document that also functions as a page within the website.

---

## 3. Layout & Grid

The two-column grid is defined on `.layout`:

```css
.layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  max-width: 1280px;
  margin: 0 auto;
}
```

- **Left column (280px):** sticky Table of Contents (`<aside class="toc-wrap">`)
- **Right column (1fr):** `<main>` content area, capped at `max-width: 880px`, padded `2.5rem 3rem 5rem`

At `≤ 900px`, the grid collapses to a single column and the TOC becomes a collapsible drawer.

---

## 4. CSS Design Tokens

All colour and shape values are defined as custom properties on `:root`. These must not change between reviews.

| Token | Value | Purpose |
|---|---|---|
| `--ink` | `#1e293b` | Primary text |
| `--ink-light` | `#475569` | Secondary/muted text |
| `--bg` | `#ffffff` | Page background |
| `--bg-soft` | `#f8fafc` | Subtle panel backgrounds |
| `--line` | `#e2e8f0` | Borders and dividers |
| `--accent` | `#2563eb` | Primary blue (links, TOC active state, score bars, buttons) |
| `--accent-soft` | `#eff6ff` | Light blue tint (h2 border, callout backgrounds) |
| `--warn` | `#92400e` | Warning text |
| `--warn-bg` | `#fef3c7` | Warning callout background |
| `--warn-border` | `#fcd34d` | Warning callout border |
| `--good` | `#166534` | Pros card heading |
| `--good-bg` | `#f0fdf4` | Pros card background |
| `--bad` | `#991b1b` | Cons card heading |
| `--bad-bg` | `#fef2f2` | Cons card background |
| `--radius` | `10px` | Standard border radius |

---

## 5. Typography

| Element | Size | Notes |
|---|---|---|
| `body` | 17px | System font stack; `line-height: 1.65` |
| `h1` | 1.9rem | `line-height: 1.25` |
| `h2` | 1.5rem | Bottom border: `3px solid var(--accent-soft)` |
| `h3` | 1.15rem | Colour: `var(--accent)` |

Font stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`

---

## 6. Sticky Table of Contents

### Desktop behaviour
The `<aside class="toc-wrap">` is `position: sticky; top: 0; height: 100vh; overflow-y: auto`. It stays fixed to the viewport left edge as the user scrolls through the article.

### Mobile behaviour (`≤ 900px`)
- The aside collapses: `max-height: 0; overflow: hidden`
- A full-width `<button class="mobile-toc-btn">` appears above it, styled `background: var(--ink); color: #fff`
- Clicking the button toggles `.open` on the aside, expanding it to `max-height: 70vh`
- Clicking any TOC link inside the drawer removes `.open`, closing the drawer

### TOC link structure
```html
<aside class="toc-wrap" id="tocWrap">
  <h4>On This Page</h4>
  <nav id="tocNav">
    <a href="#section-id">N. Section Title</a>
    ...
  </nav>
</aside>
```

Each link maps to a `<section id="...">` in `<main>`. Non-numbered entries (FAQ, Sources) appear at the end without a number prefix.

### Scroll-spy active state
An `IntersectionObserver` watches all `<section>` elements in `<main>`. When a section enters the viewport (rootMargin: `'-20% 0px -70% 0px'`), its corresponding TOC link receives `.active` (white text on `--accent` background). All other links lose `.active`.

---

## 7. Section Structure

`<main>` contains a sequence of `<section>` elements, each with a unique `id` and `scroll-margin-top: 1rem`. The standard section order is:

| # | `id` | Heading |
|---|---|---|
| 1 | `intro` | First Impressions *(contains h1, hero-tag, verdict-box, methodology)* |
| 2 | `overview` | Overview & Pricing |
| 3 | `design` | Platform & Build Quality |
| 4 | `performance` | Performance Analysis |
| 5 | `ux` | User Experience |
| 6 | `comparison` | How It Compares |
| 7 | `proscons` | Pros & Cons |
| 8 | `history` | History & Updates |
| 9 | `recommend` | Who Should Join |
| 10 | `buy` | Where to Sign Up & Pricing |
| 11 | `verdict` | Final Verdict *(contains score bars and quiz)* |
| — | `faq` | Frequently Asked Questions |
| 12 | `sources` | Evidence & Sources *(contains video embed and sources list)* |

The `intro` section never has an `<h2>` — it opens directly with the `.hero-tag` span and the `<h1>`. Every other section opens with an `<h2>`.

---

## 8. Component Inventory

### 8.1 Hero Tag
```html
<span class="hero-tag">Independent Review · Updated [Month Year]</span>
```
Pill-shaped label (`border-radius: 99px`). Colour: `--accent` on `--accent-soft`. Placed immediately before `<h1>`.

### 8.2 Verdict Box
```html
<div class="verdict-box">
  <p><strong>Best for:</strong> ...</p>
  <p><strong>Not ideal for:</strong> ...</p>
</div>
```
`border-left: 5px solid var(--accent)`. Placed in the `intro` section, after the opening paragraph and before the first `<h3>`.

### 8.3 Methodology Block
```html
<div class="methodology">
  <p><strong>Who wrote this:</strong> ...</p>
  <p><strong>How this review was built:</strong> ...</p>
</div>
```
Dashed border (`border: 1px dashed #94a3b8`), `--bg` background, `font-size: .95rem`. Placed at the end of the `intro` section.

### 8.4 Callouts
Two variants:
```html
<div class="callout warn">...</div>   <!-- amber -->
<div class="callout info">...</div>   <!-- blue -->
```
Used inline within sections to surface cautions and tips. `warn` uses `--warn-bg`/`--warn-border`. `info` uses `--accent-soft`/`#bfdbfe`.

### 8.5 Tables
All tables are wrapped in `.table-scroll` for horizontal scroll on mobile:
```html
<div class="table-scroll">
  <table>...</table>
</div>
```
`<th>` cells: small-caps, uppercase, `--ink-light`, `--bg-soft` background.

### 8.6 Pros & Cons Grid
```html
<div class="two-col">
  <div class="pc-card good"><h3>...</h3><ul>...</ul></div>
  <div class="pc-card bad"><h3>...</h3><ul>...</ul></div>
</div>
```
Two-column `1fr 1fr` grid, collapses to single column at `≤ 900px`. `.good` uses green tokens, `.bad` uses red tokens.

### 8.7 Score Bars
```html
<div class="score-row">
  <div class="score-label">Category Name</div>
  <div class="score-track"><div class="score-fill" style="width:80%"></div></div>
  <div class="score-num">4/5</div>
</div>
```
The `width` percentage and the display label must match (e.g. 4/5 = 80%, 3/5 = 60%, 1.5/5 = 30%). A small italic disclaimer follows the score block.

### 8.8 Self-Check Quiz
```html
<div class="quiz-box" id="quizBox">
  <h3 style="margin-top:0;">...</h3>
  <p style="font-size:.85rem;color:var(--ink-light);">...</p>
  <fieldset>
    <legend>Question text</legend>
    <label><input type="radio" name="qN" value="2"> Yes answer</label>
    <label><input type="radio" name="qN" value="0"> No answer</label>
  </fieldset>
  ...
  <button type="button" onclick="evaluateQuiz()">See My Result</button>
  <div id="quiz-result"></div>
</div>
```
Exactly three questions. Values are `2` (yes/aligned) or `0` (no/misaligned). Score thresholds: `≥ 5` = good fit, `≥ 3` = mixed fit, `< 3` = poor fit.

### 8.9 SVG Diagram
Original inline SVG diagrams are used to illustrate mechanics. They must:
- Have `role="img"` and `aria-label`
- Carry a `<figcaption>` explicitly stating the diagram is an original illustration, not a screenshot
- Use `viewBox` and `width:100%; max-width:640px`

### 8.10 Video Embed
```html
<div class="video-frame">
  <iframe src="..." title="..." allowfullscreen></iframe>
</div>
<p class="video-caption">...</p>
```
The `.video-frame` wrapper uses `padding-top: 56.25%` to create a responsive 16:9 container. The `title` attribute is required for accessibility. The caption must clarify that the video is third-party content, not an official company channel or the author's own production.

### 8.11 FAQ Accordion
```html
<details>
  <summary>Question text</summary>
  <p>Answer text</p>
</details>
```
Native `<details>`/`<summary>` — no JavaScript required. Each question is a `<summary>`, each answer is one `<p>` inside the element.

### 8.12 Sources Section (Pill-List Format)
The `<section id="sources">` contains:

1. **(Optional) Video Content** — introduces the video embed with a third-party disclosure paragraph, if a video is included.
2. **Sources heading** — `<h2>Sources &amp; References</h2>`.
3. **Pill-list** — a `<ul class="pill-list">` containing source links as individual `<li><a>` items. Each source link is rendered as a pill-shaped tag using the `.pill-list` CSS class.
4. **Disclaimer paragraph** — a small-print paragraph (`font-size:.82rem; color:var(--ink-light)`) disclosing the financial interests of cited sources and the information cutoff date.

**Pill-list HTML:**
```html
<section id="sources">
  <h2>Sources &amp; References</h2>
  <ul class="pill-list">
    <li><a href="..." target="_blank" rel="noopener noreferrer">Source Name</a></li>
    ...
  </ul>
  <p style="font-size:.82rem;color:var(--ink-light);">Disclaimer text.</p>
</section>
```

**Pill-list CSS (embedded in the article `<style>` block):**
```css
.pill-list{display:flex; flex-wrap:wrap; gap:.45rem; margin:0 0 1rem; padding:0; list-style:none;}
.pill-list li{margin:0;}
.pill-list a{
  display:inline-block;
  font-size:.78rem;
  background:var(--bg-soft);
  color:var(--ink-light);
  border:1px solid var(--line);
  border-radius:99px;
  padding:.25rem .7rem;
  white-space:nowrap;
}
.pill-list a:hover{background:var(--accent-soft); color:var(--accent); border-color:var(--accent); text-decoration:none;}
```

Every external link (any `href` that does not begin with `/`) must include `target="_blank"`. Affiliate or sponsored links must use `target="_blank" rel="noopener noreferrer sponsored"`. Non-affiliate external links must use `target="_blank" rel="noopener noreferrer"`. Internal links (href starting with `/`) must NOT carry a `target` or `rel` attribute.

### 8.13 CTA Card Component
A call-to-action card is placed three times in every production article:
1. **After the `intro` section** (immediately before the first content section)
2. **Mid-article** (after approximately the fifth content section, before the comparison/pros-cons area)
3. **Before the Sources section** (final CTA before the reader leaves the article)

**CTA Card HTML:**
```html
<div class="cta-card">
  <h3>New to online income? Start with the $7 Megalink</h3>
  <p>If you're curious about earning online but don't know where to begin, the <strong>$7 OLSP Megalink</strong> is one of the most <strong>beginner-friendly</strong> ways to get started. It walks you through <strong>affiliate marketing step by step</strong>—from generating traffic and leads to earning commissions—so you understand how the business works <strong>before investing in expensive tools or ads</strong>. As an added bonus, <strong>every Starter Training you refer earns you a $5 commission</strong>, making it possible to learn while earning. <strong>No experience required.</strong></p>
  <a href="https://olspacademy.com/megalive/1006001" class="cta-btn" target="_blank" rel="noopener noreferrer sponsored">Start the $7 Megalink →</a>
</div>
```

**CTA Card CSS:**
```css
.cta-card{
  border-radius:var(--radius);
  padding:1.1rem 1.3rem;
  border:1px solid var(--line);
  background:var(--accent-soft);
  border-left:4px solid var(--accent);
  margin:3rem 0;
}
.cta-card h3{font-size:1.05rem; margin:0 0 .3rem; color:var(--ink);}
.cta-card p{font-size:.92rem; margin:0 0 .8rem; color:var(--ink-light); line-height:1.55;}
.cta-card .cta-btn{font-size:.88rem; padding:.45rem 1.1rem;}
.cta-card .cta-btn::after{content:" →";}

.cta-btn{
  display:inline-block;
  background:var(--accent);
  color:#fff;
  font-weight:600;
  border-radius:8px;
}
.cta-btn:hover{background:#1d4ed8; text-decoration:none; color:#fff;}
```

**Per-article variables:**
- `h3` heading text (product name, price)
- Body copy paragraphs (what the product offers, value proposition)
- `href` on the `.cta-btn` link
- Button label text
- Affiliate disclosure paragraph

All three CTA cards on the page are **identical** — same heading, same body, same link, same disclosure. The component appears three times for placement convenience, not with different content.

---

### 8.14 Site Footer Component
Every production article ends with `<footer class="site-footer">` inside `<main>`, **after** the `sources` section and **before** `</main>`.

**Site Footer HTML:**
```html
<footer class="site-footer">
  <span>Profit and Privilege — independent research since 2025</span>
  <span><a href="https://olsp.profitandprivilege.com">olsp.profitandprivilege.com</a></span>
</footer>
```

**Site Footer CSS:**
```css
.site-footer{
  border-top:1px solid var(--line);
  padding:1.2rem 0 0;
  margin-top:2rem;
  font-size:.8rem;
  color:var(--ink-light);
  display:flex;
  justify-content:space-between;
  align-items:center;
  flex-wrap:wrap;
  gap:.4rem;
}
.site-footer a{color:var(--ink-light);}
.site-footer a:hover{color:var(--accent); text-decoration:underline;}
```

**Per-article variables:**
- The left-hand `<span>` text (brand tagline — may stay constant across articles)
- The right-hand `<a>` link text and `href` (normally points to the main domain)

---

## 9. Responsive Behaviour

| Breakpoint | Change |
|---|---|
| `> 900px` | Two-column grid; full sidebar TOC; `main` padded `2.5rem 3rem 5rem` |
| `≤ 900px` | Single column; TOC becomes collapsible drawer; mobile TOC button shown; `main` padded `1.5rem 1.2rem 3rem`; `.two-col` collapses to single column; `.score-label` shrinks to `130px` width |

The mobile TOC button (`#tocToggle`) is hidden at desktop widths via `display: none` and shown via `display: block` inside the media query.

---

## 10. JavaScript Functionality

All JavaScript is inline in a single `<script is:inline>` tag at the bottom of `<body>`. It is vanilla JS with no dependencies.

> **Why `is:inline` is required:** Astro processes `<script>` tags as ES modules by default, scoping all declarations to the module rather than the global `window` object. The quiz button uses `onclick="evaluateQuiz()"`, which requires `evaluateQuiz` to be accessible as a global function. Without `is:inline`, Astro bundles the script as a module and the `onclick` handler throws `evaluateQuiz is not defined` at runtime. The `is:inline` directive instructs Astro to emit the script exactly as written, preserving global scope. Do not remove it.

### Three behaviours:

**1. Mobile TOC toggle**
Attaches a `click` listener to `#tocToggle`. Toggles `.open` on `#tocWrap`.

**2. Scroll-spy**
Builds a `linkMap` dictionary keyed by section `id`. An `IntersectionObserver` watches all `main section` elements with `rootMargin: '-20% 0px -70% 0px'`. On intersection, removes `.active` from all TOC links and adds it to the matching link.

**3. Close TOC on link click (mobile)**
Each TOC `<a>` has a listener that removes `.open` from `#tocWrap` when `window.innerWidth <= 900`.

**4. Quiz evaluation (`evaluateQuiz`)**
Global function called by the quiz button's `onclick`. Reads three radio groups (`q1`, `q2`, `q3`). If any is unanswered, shows a prompt. Otherwise sums the values and renders one of three outcome messages into `#quiz-result`.

---

## 11. SEO Structure

### `<title>` vs `<h1>`
These are intentionally different. The `<title>` is optimised for search result snippets and can include the product creator's name or longer descriptive terms. The `<h1>` is the human-facing article title. Both must target the same primary keyword.

### `<meta name="description">`
Should match `pageDescription` in frontmatter (even though currently not interpolated). One sentence, under ~160 characters, summarising the review's scope and independent stance.

### Canonical URL
```html
<link rel="canonical" href="https://olsp.profitandprivilege.com/reviews/{slug}/" />
```
Always absolute URL. Always trailing slash. Always the production domain.

### `prerender = true`
Every article page must declare this. It ensures static generation and maximum crawlability.

### No structured data (as of Gold Master)
The Gold Master does not include `FAQPage`, `Article`, or `Review` JSON-LD schema. Future reviews may add it, but it is not currently part of the standard and should not be added without deliberate intent.

---

## 12. Open Graph / Metadata

The Gold Master contains **no Open Graph tags** (`og:title`, `og:description`, `og:image`, etc.) and **no Twitter Card tags**. This is the current production state. Future reviews should match this unless OG tags are deliberately added as a feature across all reviews at once.

---

## 13. Canonical URL Strategy

- Pattern: `https://olsp.profitandprivilege.com/{type}/{slug}/` where `{type}` is `reviews`, `blog`, or `roundups`
- The slug matches the `.astro` filename (e.g. `olsp-academy.astro` → `/reviews/olsp-academy/`)
- Trailing slash is present on the canonical but the slug itself is lowercase-kebab-case
- The canonical is hardcoded, not generated from a variable

---

## 14. Internal Linking Strategy

The Gold Master contains **no site navigation and no header**. Each article includes a `<footer class="site-footer">` (see Section 8.14) as part of its editorial page structure. The TOC links only scroll within the current page.

Internal links to other articles on the site **are permitted** within body copy where contextually relevant (e.g. linking from a blog post to a related review, or from a roundup to individual reviews). These must not include `rel="sponsored"` and should be woven naturally into the prose. Do not create a separate "related articles" block.

---

## 15. Accessibility Considerations

| Element | Requirement |
|---|---|
| `<html>` | Must have `lang="en"` |
| `<aside>` | Used for the TOC — correct semantic landmark |
| `<main>` | Single `<main>` per page |
| `<nav>` | Wraps TOC links inside `<aside>` |
| `<figure>` / `<figcaption>` | Wraps all SVG diagrams |
| SVG | Must have `role="img"` and a descriptive `aria-label` |
| `<iframe>` | Must have a `title` attribute describing the content |
| `<details>` / `<summary>` | Native accessible accordion — no ARIA overrides needed |
| Colour contrast | `--ink` on `--bg` and `--bg-soft` must pass WCAG AA; do not change token values |
| `scroll-behavior: smooth` | Set globally on `html`; respects OS reduced-motion preference at the browser level |

---

## 16. What Changes Between Articles

The following elements are **per-article variables** — everything else is structural and must remain consistent:

| Element | Notes |
|---|---|
| `pageTitle` / `pageDescription` | Frontmatter declarations |
| `<title>` tag | SEO-optimised; includes product and creator name |
| `<meta name="description">` | Article-specific summary |
| `<link rel="canonical">` | New slug |
| `.hero-tag` text | Product category label + updated date |
| `<h1>` text | Human-facing article title |
| All body copy | Every section rewrites entirely for the product |
| Pricing table rows | Product-specific tiers, costs, what's included |
| Comparison table rows | Products being compared change; OLSP row is removed |
| Pros/cons list items | Product-specific findings |
| Score bar widths and labels | Per-category scores for the specific product |
| Score category names | Can be renamed to fit the product |
| Quiz questions, values, and outcome messages | Must be logical for the specific product's decision factors |
| FAQ questions and answers | Product-specific questions |
| SVG diagram content | Illustrates the specific product's mechanics |
| Video embed URL | Third-party video discussing the specific product |
| Video caption | Reflects the actual video content |
| Sources list `<li>` items | Links and anchor text for the specific product |
| Sources disclaimer paragraph | Date reference and affiliate disclosure updated |
| Section headings | `<h2>` text customised to the product (e.g. "OLSP Academy Overview" → "[Product] Overview") |
| Callout body text | Warn/info callout messages are product-specific |
| CTA card heading, body, link, and disclosure | Per-article product name, price, value proposition, affiliate link, and disclosure text |
| Pill-list source items | Links and anchor text specific to the article's research sources |
| Site footer right-side link | Text and `href` (normally points to the main domain) |

---

## 17. What Must Not Change Between Articles

| Element | Why |
|---|---|
| CSS custom properties (all `--*` tokens) | Shared visual identity |
| `.layout` grid dimensions (280px / 1fr / 1280px max) | Consistent layout |
| `main` max-width (880px) and padding values | Reading width and rhythm |
| The 900px breakpoint | Single responsive breakpoint for the entire system |
| TOC `id` values: `tocWrap`, `tocNav`, `tocToggle` | JS relies on these |
| `quiz-result` div id | JS relies on this |
| Section `id` names (`intro`, `overview`, `design`, `performance`, `ux`, `comparison`, `proscons`, `history`, `recommend`, `buy`, `verdict`, `faq`, `sources`) | TOC href anchors must match |
| Section order | Consistent reader expectation across all reviews |
| `.hero-tag` placement (before `<h1>`, inside `#intro`) | Visual pattern |
| `.verdict-box` placement (after intro paragraph, before first `<h3>`) | Editorial structure |
| `.methodology` block in `#intro` | Credibility signal; required on every article |
| `.video-frame` aspect-ratio padding (56.25%) | Responsive 16:9 |
| `target="_blank" rel="noopener noreferrer sponsored"` on affiliate/CTA links | Compliance + security; opens in new tab |
| `target="_blank" rel="noopener noreferrer"` on non-affiliate external links | Security; opens in new tab |
| Sources disclaimer paragraph at end of `#sources` | Transparency requirement |
| `.cta-card` structure and CSS (Section 8.13) | Consistent CTA placement and visual identity across articles |
| Three CTA card placements (post-intro, mid-article, before Sources) | Content marketing pattern; all three cards must be identical |
| `.pill-list` structure and CSS (Section 8.12) | Consistent sources formatting across articles |
| `.site-footer` structure and CSS (Section 8.14) | Global brand presence on every production page |
| `prerender = true` | Static generation |

---

## 18. Production Rules

1. **One file, self-contained.** Every article is a single `.astro` file in the appropriate `src/pages/{type}/` directory. No layout imports, no component imports, no shared CSS files.

2. **`prerender = true` is mandatory.** Every article page must be statically generated.

3. **Do not change the CSS token values.** Copy the entire `<style>` block verbatim. Customise only the content inside sections.

   Also copy the `<script is:inline>` tag verbatim — including the `is:inline` directive. Omitting `is:inline` breaks the quiz: Astro will bundle the script as an ES module, removing `evaluateQuiz` from global scope and silently breaking the `onclick` handler. See Section 10 for the full explanation.

4. **The section order is fixed for reviews.** Reviews must follow: `intro → overview → design → performance → ux → comparison → proscons → history → recommend → buy → verdict → faq → sources`. Do not reorder, skip, or rename these sections. Other article types (roundups, blog posts) define their own section order and `id` values, but must use the same layout grid, CSS tokens, and `<script is:inline>` block.

5. **Section `id` values are fixed for each article type.** The TOC, scroll-spy JS, and `<link>` anchors all depend on them. Do not rename them within the same article type.

6. **The `intro` section must contain four elements in order:** `.hero-tag` pill, `<h1>`, opening paragraph, `.verdict-box`, then the first `<h3>`, then `.methodology`.

7. **The `<title>` and `<h1>` must be different.** `<title>` is for search engines; `<h1>` is for readers. Both must target the same primary keyword.

8. **The canonical URL must be absolute, with a trailing slash,** using the production domain: `https://olsp.profitandprivilege.com/{type}/{slug}/`.

9. **All external links must include `target="_blank"`** so they open in a new browser tab. Affiliate and sponsored links must use `target="_blank" rel="noopener noreferrer sponsored"`. Non-affiliate external links must use `target="_blank" rel="noopener noreferrer"`. The active CTA destination is `https://olspacademy.com/megalive/1006001`.

10. **The sources section must end with a disclaimer paragraph** in small print (`font-size:.82rem; color:var(--ink-light)`) disclosing the financial interests of cited sources and the date the information was gathered.

11. **The methodology block is not optional.** Every article must include a `<div class="methodology">` in the `intro` section disclosing who wrote it and how the research was conducted.

12. **Income claims and self-reported figures must be labelled as unverified.** Use `.callout.warn` or explicit inline language ("self-reported," "could not be independently verified") whenever citing any earnings figure.

13. **SVG diagrams must carry `role="img"` and `aria-label`.** Captions must state the diagram is an original illustration, not a screenshot.

14. **The `<iframe>` must have a `title` attribute.** The caption must disclose that the video is third-party content.

15. **The quiz must have exactly three questions.** Answers score `2` (aligned) or `0` (misaligned). Outcomes map to score ranges: `≥ 5` (good fit), `≥ 3` (mixed), `< 3` (poor fit).

16. **Score bar percentages must match the displayed fraction.** 5/5 = 100%, 4/5 = 80%, 3/5 = 60%, 2/5 = 40%, 1.5/5 = 30%, 1/5 = 20%.

17. **No site navigation or header.** Do not add a `<header>` or `<nav>` unless a deliberate site-wide navigation upgrade is applied to all pages simultaneously. A `<footer class="site-footer">` (as specified in Section 8.14) is required on every production article.

18. **No Open Graph tags** unless added to all articles as a deliberate upgrade. Do not add OG tags to individual articles only.

19. **The mobile TOC button label must be `☰ Table of Contents`** to maintain a consistent affordance.

20. **Do not modify `src/pages/reviews/olsp-academy.astro`.** It is the canonical reference. Future changes to the standard are made by updating this spec, then applying the change to all article pages together.

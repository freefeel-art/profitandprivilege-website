# Gold Master Specification — OLSP Standard

**Version:** 2.1 — Production Ready  
**Validated by:** `src/pages/reviews/olsp-mineeme.astro`, `src/pages/reviews/seo-writing-ai-review.astro`  
**Components directory:** `src/components/olsp-standard/` (12 shared components + OlspLayout)  
**Purpose:** This document defines the production standard for every OLSP review article on this site. The Gold Master is a reusable component system — not a single file to copy. Structure, CSS tokens, JS behavior, SEO metadata, and CTA architecture are shared across all articles through OlspLayout and 10 Gold Master components. Editorial content, product metadata (CTA props, sources, pricing tables), and section body text vary per article.

---

## 1. Architecture Overview

Every review article is an `.astro` file that imports OlspLayout and 13 Gold Master components. The layout, CSS tokens, TOC, and JavaScript live in OlspLayout, not in the article file. The article file contains only frontmatter metadata and editorial content wrapped in `<OlspLayout>` tags.

```
src/pages/reviews/
  olsp-mineeme.astro                 ← Validated reference article (MineeMe)
  seo-writing-ai-review.astro        ← Validated reference article (SEO Writing AI)
  [slug].astro                       ← future articles copy this pattern

src/components/olsp-standard/
  OlspLayout.astro                   ← layout, CSS tokens, TOC, JS
  HeroTag.astro                      ← pill-shaped category label
  VerdictBox.astro                   ← best-for / not-ideal-for box
  Methodology.astro                  ← research methodology disclosure
  Callout.astro                      ← warn/info callout blocks
  ProductCta.astro                   ← product-specific CTA (props-driven)
  GoldMasterQuote.astro              ← fixed editorial trust quote
  FaqItem.astro                      ← accordion FAQ item
  PillList.astro                     ← source link pills
  AuthorBox.astro                   ← author bio
  SiteFooter.astro                   ← brand footer
  ScoreBar.astro                     ← individual score row with fill bar
  QuizBox.astro                      ← self-check quiz wrapper with heading + button
```

The same component system renders every review article. Only editorial content and product metadata change between articles.

---

## 2. Article File Structure

Every review article follows this pattern:

```astro
---
export const prerender = true;

import OlspLayout from "../../components/olsp-standard/OlspLayout.astro";
import HeroTag from "../../components/olsp-standard/HeroTag.astro";
import VerdictBox from "../../components/olsp-standard/VerdictBox.astro";
import Methodology from "../../components/olsp-standard/Methodology.astro";
import Callout from "../../components/olsp-standard/Callout.astro";
import ProductCta from "../../components/olsp-standard/ProductCta.astro";
import GoldMasterQuote from "../../components/olsp-standard/GoldMasterQuote.astro";
import FaqItem from "../../components/olsp-standard/FaqItem.astro";
import PillList from "../../components/olsp-standard/PillList.astro";
import AuthorBox from "../../components/olsp-standard/AuthorBox.astro";
import SiteFooter from "../../components/olsp-standard/SiteFooter.astro";
import ScoreBar from "../../components/olsp-standard/ScoreBar.astro";
import QuizBox from "../../components/olsp-standard/QuizBox.astro";

const pageTitle = "...";
const pageDescription = "...";

const tocLinks = [
  { href: "#intro", label: "1. First Impressions" },
  // ... all section links
];
---

<OlspLayout title={pageTitle} description={pageDescription} canonical="https://olsp.profitandprivilege.com/reviews/{slug}/" tocLinks={tocLinks}>

  <section id="intro">
    <HeroTag text="..." />
    <h1>...</h1>
    <p>...</p>
    <VerdictBox>...</VerdictBox>
    <h3>...</h3>
    <Methodology>...</Methodology>
  </section>

  <GoldMasterQuote />

  <ProductCta title="..." description="..." buttonText="..." href="..." />

  <!-- Score bars (final verdict section): ScoreBar components -->
  <ScoreBar label="Category Name" score={4} />

  <!-- Body sections: overview, design, performance, ux, comparison, proscons, history, recommend, buy, verdict -->

  <ProductCta title="..." buttonText="..." href="..." />

  <QuizBox heading="Quick Self-Check: Is This Worth Exploring for You?">
    <!-- Exactly three fieldset elements with radio inputs named q1, q2, q3 -->
  </QuizBox>

  <section id="faq">
    <h2>Frequently Asked Questions</h2>
    <FaqItem question="..." answer="..." />
  </section>

  <section id="author">
    <h2>About the Author</h2>
    <AuthorBox />
  </section>

  <GoldMasterQuote />

  <section id="sources">
    <h2>Sources &amp; References</h2>
    <PillList items={[...]} />
    <p class="disclaimer">...</p>
    <SiteFooter />
  </section>

</OlspLayout>
```

---

## 3. Frontmatter

The Astro frontmatter contains:

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `prerender` | `true` | Always | Ensures static HTML generation at build time |
| `pageTitle` | string | Always | Used in `<title>` tag via OlspLayout |
| `pageDescription` | string | Always | Used in `<meta name="description">` via OlspLayout |
| `tocLinks` | `{href, label}[]` | Always | Array of section links rendered by OlspLayout's TOC |
| `ogImage` | string | No | Full URL to OG image asset; enables `og:image` and `twitter:image` |
| `datePublished` | string | No | ISO date string; enables `datePublished` in schema |
| `dateModified` | string | No | ISO date string; falls back to `datePublished` if set; enables `dateModified` in schema |
| `articleType` | `"Article" \| "Review" \| "BlogPosting"` | No | Controls JSON-LD schema type; defaults to `"Article"` |
| `productName` | string | No | Required when `articleType: "Review"`; populates `itemReviewed.name` in Review schema |

---

## 4. OlspLayout — Responsibilities

`OlspLayout.astro` provides everything that does not change between articles:

### 4.1 Document Shell
- `<!DOCTYPE html>` and `<html lang="en">`
- `<head>` with charset, viewport, `<title>`, `<meta name="description">`, canonical link
- `<meta name="robots" content="index, follow">`
- Favicon links for SVG and ICO formats
- Open Graph tags: `og:title`, `og:description`, `og:url`, `og:type`, `og:site_name`; `og:image` conditionally when `ogImage` prop provided
- Twitter Card tags: `twitter:card` (summary_large_image), `twitter:title`, `twitter:description`; `twitter:image` conditionally when `ogImage` prop provided
- JSON-LD structured data via `<script type="application/ld+json">` — generates Article, Review, or BlogPosting schema depending on `articleType` prop, plus Organization node
- Inline `<style>` block with all CSS tokens and classes
- `<body>` with the two-column layout grid
- Inline `<script is:inline>` with mobile TOC toggle, scroll-spy, and quiz evaluation

### 4.2 CSS Design Tokens
All colour and shape values are defined as custom properties on `:root`. These must not change.

| Token | Value | Purpose |
|-------|-------|---------|
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

### 4.3 Layout Grid
Two-column grid on `.layout`:
- Left column (280px): sticky Table of Contents (`<aside class="toc-wrap">`)
- Right column (1fr): `<main>` content area, capped at `max-width: 880px`

At `≤ 900px` the grid collapses to a single column and the TOC becomes a collapsible drawer.

### 4.4 Typography
| Element | Size | Notes |
|---------|------|-------|
| `body` | 17px | System font stack; `line-height: 1.65` |
| `h1` | 1.9rem | `line-height: 1.25` |
| `h2` | 1.5rem | Bottom border: `3px solid var(--accent-soft)` |
| `h3` | 1.15rem | Colour: `var(--accent)` |

Font stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`

### 4.5 JavaScript
All JavaScript is inline in a single `<script is:inline>` tag. Functions:
1. **Mobile TOC toggle** — toggles `.open` on `#tocWrap`
2. **Scroll-spy** — `IntersectionObserver` watches `<section>` elements, highlights active TOC link
3. **Close TOC on link click** — closes mobile drawer after navigation
4. **Quiz evaluation** — `evaluateQuiz()` reads three radio groups and renders outcome

### 4.6 TOC Rendering
The TOC is rendered from the `tocLinks` prop using `.map()`. Each link maps to a `<section id="...">` in `<main>`. Non-numbered entries appear at the end without a number prefix.

---

## 5. Gold Master Components

### 5.1 HeroTag
```astro
<HeroTag text="Independent Review · Updated July 2026" />
```
Pill-shaped label. Colour: `--accent` on `--accent-soft`. Placed immediately before `<h1>`.

### 5.2 VerdictBox
```astro
<VerdictBox>
  <p><strong>Best for:</strong> ...</p>
  <p><strong>Not ideal for:</strong> ...</p>
</VerdictBox>
```
`border-left: 5px solid var(--accent)`. Placed in the `intro` section, after the opening paragraph and before the first `<h3>`.

### 5.3 Methodology
```astro
<Methodology>
  <p><strong>Who wrote this:</strong> ...</p>
  <p><strong>How this review was built:</strong> ...</p>
</Methodology>
```
Dashed border, `--bg` background. Placed at the end of the `intro` section.

### 5.4 Callout
```astro
<Callout type="warn">...</Callout>
<Callout type="info">...</Callout>
```
Used inline within sections. `warn` uses amber tokens. `info` uses blue tokens.

### 5.5 ProductCta (Props-Driven)
```astro
<ProductCta title="..." description="..." buttonText="..." href="..." />
```
**Props:**

| Prop | Type | Required | Default |
|------|------|----------|---------|
| `title` | string | Yes | — |
| `description` | string | No | "Visit the official product page to see current pricing, features, updates, and purchase options." |
| `buttonText` | string | Yes | — |
| `href` | string | Yes | — |

The component renders an editorial CTA card with heading, description, button, and affiliate disclosure. The button uses `target="_blank" rel="noopener noreferrer sponsored"`. The affiliate disclosure paragraph is hardcoded in the component — article pages do not add it.

### 5.11 ScoreBar
```astro
<ScoreBar label="Category Name" score={4} />
<ScoreBar label="Category Name" score={3.5} width={70} />
```
**Props:**

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `label` | string | Yes | — | Category label displayed in the score row |
| `score` | number | Yes | — | Numerator of the score fraction (e.g. 4 for 4/5) |
| `max` | number | No | `5` | Denominator of the score fraction |
| `width` | number | No | calculated from `(score/max)*100` | Explicit width percentage override if calculated value does not match the existing visual output |

Renders a single score row with label, fill track, and fraction. Width percentage and fraction must match per § 11 rules. Use `width` prop only when preserving an existing visual that diverges from the standard calculation.

### 5.12 QuizBox
```astro
<QuizBox heading="Quick Self-Check: Is This Worth Exploring for You?">
  <fieldset>...</fieldset>
  <fieldset>...</fieldset>
  <fieldset>...</fieldset>
</QuizBox>
```
**Props:**

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `heading` | string | Yes | — | Heading for the quiz box (product-specific) |

Wraps the three radio-group fieldsets with the standard quiz box container, disclaimer text, submit button, and result div. The `evaluateQuiz()` function lives in OlspLayout. Exactly three fieldsets with `q1`, `q2`, `q3` radio inputs must be provided as slot content.

**Placement rules:**
- **First placement:** After the intro section, after the first `GoldMasterQuote`
- **Second placement (long-form reviews):** Near the Final Verdict, before the FAQ section
- The second placement may omit `description` to use the default editorial line

### 5.6 GoldMasterQuote (Fixed)
```astro
<GoldMasterQuote />
```
A lightweight editorial pull-quote with fixed text and URL across all articles. No props. Renders a hyperlinked quote with no card, no button, no sales copy. Uses `target="_blank" rel="noopener noreferrer"`.

**Placement rules (exactly 3, same order every article):**
1. After the intro section, before the first ProductCta
2. After the UX section, before the comparison section
3. After the author section, before the sources section

### 5.7 FaqItem
```astro
<FaqItem question="..." answer="..." />
```
Native `<details>`/`<summary>` accordion — no JavaScript required.

### 5.8 PillList
```astro
<PillList items={[
  { label: "Source Name", url: "https://...", sponsored: true },
  { label: "Source Name", url: "https://..." },
]} />
```
Each item is rendered as a pill-shaped `<a>` tag. When `sponsored: true`, the link uses `target="_blank" rel="noopener noreferrer sponsored"`. Non-sponsored external links use `target="_blank" rel="noopener noreferrer"`. Internal links (href starting with `/`) get no target/rel.

### 5.9 AuthorBox
```astro
<AuthorBox />
```
Renders the author bio with photo, name, role, and profile link.

### 5.10 SiteFooter
```astro
<SiteFooter />
```
Renders the brand footer with "Profit and Privilege — independent research since 2025" and the site domain link.

---

## 6. Section Structure

`<main>` contains a sequence of `<section>` elements in this fixed order:

| Position | `id` | Heading | Notes |
|----------|------|---------|-------|
| 1 | `intro` | *(no h2)* | Contains HeroTag, h1, opening paragraph, VerdictBox, h3, Methodology |
| — | *(GoldMasterQuote)* | — | First trust quote placement |
| — | *(ProductCta)* | — | First product CTA placement |
| 2 | `overview` | Overview & Pricing | Pricing tables, feature lists, Callout blocks |
| 3 | `design` | Platform & Build Quality | Technology architecture, data flow |
| 4 | `performance` | Features & Performance | SVG diagram, key features, hands-on validation notes |
| 5 | `ux` | User Experience | Setup, daily usage, learning curve |
| — | *(GoldMasterQuote)* | — | Second trust quote placement |
| 6 | `comparison` | How It Compares | Comparison table with 4-6 rows |
| 7 | `proscons` | Pros & Cons | Two-column grid with good/bad cards |
| 8 | `history` | History & Updates | Company background, market presence |
| 9 | `recommend` | Who Should Use It | Best For / Skip If / Alternatives |
| 10 | `buy` | Where to Get It | Sign-up links, pricing verification |
| 11 | `verdict` | Final Assessment | Score bars, editorial summary |
| — | *(ProductCta)* | — | Second product CTA placement (may omit description) |
| — | `faq` | Frequently Asked Questions | FaqItem accordions |
| — | `author` | About the Author | AuthorBox |
| — | *(GoldMasterQuote)* | — | Third trust quote placement |
| 12 | `sources` | Sources & References | PillList, disclaimer, SiteFooter |

The `intro` section never has an `<h2>` — it opens directly with `<HeroTag>` and the `<h1>`. Every other section opens with an `<h2>`.

---

## 7. What Changes Between Articles (Product Metadata)

| Element | Where | How |
|---------|-------|-----|
| `pageTitle`, `pageDescription` | Frontmatter | String values |
| `tocLinks` | Frontmatter | Section label array (section numbers may differ slightly) |
| `canonical` | OlspLayout prop | URL with new slug |
| `HeroTag` text | Component prop | Product category + date |
| `<h1>` | In section | Human-facing title |
| All body copy | Inside sections | Every section rewrites entirely |
| Pricing tables | `#overview` | Product-specific tiers and costs |
| Comparison table | `#comparison` | Products being compared change |
| Pros/cons lists | `#proscons` | Product-specific findings |
| Score bar widths/labels | `#verdict` | Per-category scores |
| Quiz questions | `#verdict` | Product-specific decision factors |
| FAQ items | `#faq` | Product-specific questions |
| SVG diagram | `#performance` | Illustrates the specific product's mechanics |
| Video embed | (optional) | Third-party video |
| `ProductCta props` | Component | `title`, `description`, `buttonText`, `href` — product-specific |
| `PillList items` | `#sources` | Product-specific source links |

---

## 8. What Must Not Change Between Articles

| Element | Why |
|---------|-----|
| CSS custom properties (all `--*` tokens) | Shared visual identity |
| `.layout` grid dimensions (280px / 1fr / 1280px max) | Consistent layout |
| `main` max-width (880px) and padding values | Reading width and rhythm |
| The 900px breakpoint | Single responsive breakpoint |
| TOC `id` values: `tocWrap`, `tocNav`, `tocToggle` | JS relies on these |
| `quiz-result` div id | JS relies on this |
| Section `id` names | TOC href anchors must match |
| Section order | Consistent reader expectation |
| `HeroTag` placement (before `<h1>`, inside `#intro`) | Visual pattern |
| `VerdictBox` placement (after intro paragraph, before first `<h3>`) | Editorial structure |
| `Methodology` block in `#intro` | Credibility signal |
| Three `GoldMasterQuote` placements | Brand signature pattern; same component, same position |
| First `ProductCta` placement (after intro, after first GoldMasterQuote) | Product conversion point |
| Second `ProductCta` placement (near verdict, before FAQ) | Second conversion point |
| `GoldMasterQuote` fixed text and URL | Fixed — never customized per article |
| `ProductCta` uses `sponsored` rel | Compliance |
| `GoldMasterQuote` uses plain `noopener noreferrer` | Editorial — not sponsored |
| Component imports (all 11) | Every article uses the same component set |
| `SiteFooter` at end of `#sources` | Brand presence on every page |
| `prerender = true` | Static generation |

---

## 9. SEO Layer

SEO metadata is generated by OlspLayout — no article page should add its own `<meta>`, OG, or schema tags.

| Element | Source | Notes |
|---------|--------|-------|
| `<title>` | `pageTitle` prop | Optimised for search result snippets; must differ from `<h1>` |
| `<meta name="description">` | `pageDescription` prop | Summarises the review's scope and independent stance |
| `<link rel="canonical">` | `canonical` prop | Absolute URL with trailing slash, production domain |
| `<meta name="robots">` | Hardcoded in OlspLayout | `index, follow` — always present |
| Favicon links | Hardcoded in OlspLayout | SVG + ICO fallback |
| Open Graph tags | Generated from props | `og:title`, `og:description`, `og:url`, `og:type` (article), `og:site_name`; `og:image` conditional on `ogImage` prop |
| Twitter Card tags | Generated from props | `summary_large_image`, `twitter:title`, `twitter:description`; `twitter:image` conditional on `ogImage` prop |
| JSON-LD Schema | Generated from props | Article, Review, or BlogPosting type (controlled by `articleType` prop); always includes Organization node in `@graph` |

### 9.1 Schema Variants

**Default (Article or BlogPosting):**
```json
{
  "@type": "Article",
  "headline": "<pageTitle>",
  "description": "<pageDescription>",
  "url": "<canonical>",
  "author": { "@type": "Person", "name": "Jarmo Halonen" },
  "publisher": { "@type": "Organization", "name": "Profit and Privilege" },
  "mainEntityOfPage": { "@type": "WebPage", "@id": "<canonical>" }
}
```

**Review (when `articleType: "Review"` + `productName` set):**
```json
{
  "@type": "Review",
  "itemReviewed": { "@type": "Product", "name": "<productName>" },
  "author": { "@type": "Person", "name": "Jarmo Halonen" },
  "url": "<canonical>"
}
```

Both wrappers include an Organization node and optional `datePublished` / `dateModified` if those props are provided.

---

## 10. Link Rules

| Link type | Attributes |
|-----------|------------|
| Affiliate / sponsored | `target="_blank" rel="noopener noreferrer sponsored"` |
| Non-affiliate external | `target="_blank" rel="noopener noreferrer"` |
| Internal (starts with `/`) | No target or rel attributes |

---

## 11. Score Bars

Score bars must use the `<ScoreBar>` component:

```astro
<ScoreBar label="Category Name" score={4} />
```

Width percentage (calculated from `score/max`) and display fraction must match: 5/5 = 100%, 4/5 = 80%, 3/5 = 60%, 2/5 = 40%, 1.5/5 = 30%, 1/5 = 20%. Use the `width` prop only when preserving existing visual output that diverges from the standard calculation.

---

## 12. Self-Check Quiz

The quiz must use the `<QuizBox>` component:

```astro
<QuizBox heading="Quick Self-Check: Is This Product Right for You?">
  <fieldset>
    <legend>Question 1...</legend>
    <label><input type="radio" name="q1" value="2"> Yes...</label>
    <label><input type="radio" name="q1" value="0"> No...</label>
  </fieldset>
  <fieldset>
    <legend>Question 2...</legend>
    <label><input type="radio" name="q2" value="2"> Yes...</label>
    <label><input type="radio" name="q2" value="0"> No...</label>
  </fieldset>
  <fieldset>
    <legend>Question 3...</legend>
    <label><input type="radio" name="q3" value="2"> Yes...</label>
    <label><input type="radio" name="q3" value="0"> No...</label>
  </fieldset>
</QuizBox>
```

Exactly three questions using radio groups `q1`, `q2`, `q3`. Values: `2` (aligned) or `0` (misaligned). Score thresholds: `≥ 5` = good fit, `≥ 3` = mixed fit, `< 3` = poor fit. The `evaluateQuiz()` function lives in OlspLayout.

---

## 13. SVG Diagrams

Inline SVG diagrams must:
- Have `role="img"` and `aria-label`
- Carry a `<figcaption>` stating it is an original illustration, not a screenshot
- Use `viewBox` and `width:100%; max-width:640px`

---

## 14. Video Embeds

```html
<div class="video-frame">
  <iframe src="..." title="..." allowfullscreen></iframe>
</div>
<p class="video-caption">...</p>
```
The `.video-frame` wrapper uses `padding-top: 56.25%` for 16:9 responsive container. The `title` attribute is required for accessibility. The caption must clarify that the video is third-party content.

---

## 15. Responsive Behaviour

| Breakpoint | Change |
|------------|--------|
| `> 900px` | Two-column grid; full sidebar TOC; `main` padded `2.5rem 3rem 5rem` |
| `≤ 900px` | Single column; TOC becomes collapsible drawer; `main` padded `1.5rem 1.2rem 3rem`; `.two-col` collapses; `.score-label` shrinks |

---

## 16. Production Rules

1. **Component imports are mandatory.** Every article must import all 13 Gold Standard components. Do not omit imports.

2. **`prerender = true` is mandatory.** Every article page must be statically generated.

3. **Do not modify the components in `src/components/olsp-standard/`.** They are shared across all articles. Changes to a component affect every article simultaneously.

4. **Do not modify `src/components/olsp-standard/OlspLayout.astro`.** It is the canonical layout. CSS tokens, grid, TOC, and JS live here.

5. **The section order is fixed.** Reviews must follow: `intro → overview → design → performance → ux → comparison → proscons → history → recommend → buy → verdict → faq → author → sources`. Do not reorder, skip, or rename these sections.

6. **Section `id` values are fixed.** The TOC, scroll-spy JS, and link anchors depend on them.

7. **The `intro` section must contain in order:** `<HeroTag>`, `<h1>`, opening paragraph, `<VerdictBox>`, first `<h3>`, `<Methodology>`.

8. **Three `GoldMasterQuote` placements are fixed.** Post-intro (before first ProductCta), mid-article (after UX, before comparison), and near-end (after author, before sources). The component has no props — fixed text and URL.

9. **ProductCta appears 1–2 times.** First after the first GoldMasterQuote (post-intro), second near Final Verdict before FAQ. The second may omit `description` to use the default.

10. **The `<title>` and `<h1>` must be different.** `<title>` is for search engines; `<h1>` is for readers.

11. **The canonical URL must be absolute, with a trailing slash,** using the production domain.

12. **All external links must include `target="_blank"`.** Affiliate links use `sponsored`. Non-affiliate external links use `noopener noreferrer`. Internal links (starting with `/`) get no target or rel.

13. **The sources section must end with a disclaimer paragraph** disclosing financial interests and information cutoff date.

14. **The methodology block is not optional.** Every article must include `<Methodology>` in the `intro` section.

15. **Income claims and self-reported figures must be labelled as unverified.** Use `<Callout type="warn">` or explicit inline language.

16. **The quiz must have exactly three questions.** Answers score `2` (aligned) or `0` (misaligned). Outcomes map to score ranges.

17. **Score bar percentages must match the displayed fraction.**

18. **No site navigation or header.** Do not add a `<header>` or site-wide `<nav>`. A `<SiteFooter />` is required on every article.

19. **SEO metadata is generated by OlspLayout, not article pages.** Do not add `<meta>`, OG, Twitter, or schema tags to individual article files. All such tags live in OlspLayout and are controlled via its props.

20. **Do not modify the validated reference articles** (`olsp-mineeme.astro`, `seo-writing-ai-review.astro`). They are canonical references for the component-based architecture.

---

## 17. Component Directory Reference

| File | Path | Purpose |
|------|------|---------|
| OlspLayout | `src/components/olsp-standard/OlspLayout.astro` | Layout, CSS tokens, OG/Twitter/Schema, TOC, JS |
| HeroTag | `src/components/olsp-standard/HeroTag.astro` | Category pill label |
| VerdictBox | `src/components/olsp-standard/VerdictBox.astro` | Best-for / not-ideal-for |
| Methodology | `src/components/olsp-standard/Methodology.astro` | Research disclosure |
| Callout | `src/components/olsp-standard/Callout.astro` | Warn/info blocks |
| ProductCta | `src/components/olsp-standard/ProductCta.astro` | Product CTA (props-driven) |
| GoldMasterQuote | `src/components/olsp-standard/GoldMasterQuote.astro` | Fixed trust quote |
| FaqItem | `src/components/olsp-standard/FaqItem.astro` | FAQ accordion |
| PillList | `src/components/olsp-standard/PillList.astro` | Source link pills |
| AuthorBox | `src/components/olsp-standard/AuthorBox.astro` | Author bio |
| SiteFooter | `src/components/olsp-standard/SiteFooter.astro` | Brand footer |
| ScoreBar | `src/components/olsp-standard/ScoreBar.astro` | Individual score row with fill bar |
| QuizBox | `src/components/olsp-standard/QuizBox.astro` | Self-check quiz wrapper |

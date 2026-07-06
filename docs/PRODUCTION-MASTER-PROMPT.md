# Production Master Prompt — OLSP Review Article Generator

**Version:** 3.0  
**Applies to:** `src/pages/reviews/[slug].astro`  
**Gold Master specification:** `docs/GOLD-MASTER-SPEC.md`  
**Validated reference articles:** `src/pages/reviews/olsp-mineeme.astro`, `src/pages/reviews/seo-writing-ai-review.astro`  
**Components directory:** `src/components/olsp-standard/`

---

## How to Use This Document

Copy everything inside the horizontal rule below (from "## Task" to the end of the checklist) into a new conversation with the writer. Supply all required inputs listed in the Inputs section before asking for output. Do not modify this prompt between articles — if the standard needs to change, update `docs/GOLD-MASTER-SPEC.md` first, then revise this document.

---

## Task

You are generating a production-ready Astro review article for the website **Profit & Privilege** (`olsp.profitandprivilege.com`). This site publishes independent, research-based reviews of online business, affiliate marketing, and digital education products.

Your output is exactly one complete file:

```
src/pages/reviews/[slug].astro
```

**The Gold Master is a component-based architecture.** Every article imports OlspLayout and 11 Gold Master components from `src/components/olsp-standard/`. Layout, CSS tokens, TOC, and JavaScript are provided by OlspLayout — do not write them in the article. The article file contains only frontmatter metadata, editorial content, and component usage within `<OlspLayout>` tags.

For the editorial content pattern (section structure, CTA placements, component usage), follow the validated reference article at `src/pages/reviews/olsp-mineeme.astro`.

The file must be ready to build and deploy without any manual structural edits. It must pass `astro build` on first attempt.

---

## Required Inputs

The following inputs must be supplied before you begin. Do not start generating until all of them are present. If any are missing, list what is absent and wait.

| Input | Format | Notes |
|-------|--------|-------|
| **Gold Master Specification** | Full contents of `docs/GOLD-MASTER-SPEC.md` | The authoritative rule set. Read it before generating. |
| **Validated reference article** | Full contents of `src/pages/reviews/olsp-mineeme.astro` | The canonical editorial pattern. Copy component usage and section structure exactly. |
| **Research package** | Freeform text, notes, or pasted source material — typically a Research Brief from `docs/research/` | Your primary content source. Everything you write must be grounded in this. |
| **Target keyword** | Plain text, e.g. `[product name] review` | Used in `<title>`, `<h1>`, and `<meta name="description">`. |
| **Canonical URL** | Full absolute URL with trailing slash, e.g. `https://olsp.profitandprivilege.com/reviews/[slug]/` | Hardcoded into OlspLayout's `canonical` prop. |
| **Product metadata** | Product CTA title, description, buttonText, href | Used in ProductCta component props. |
| **Internal links** | List of anchor text + URL pairs, or "none" | Links to other pages on olsp.profitandprivilege.com to weave naturally into the content. |
| **Author bio** | 1–3 sentences describing the editorial team or author | Used in Methodology block. |
| **Affiliate links** | List of anchor text + URL pairs with tracking parameters, or "none" | Placed only in the Sources section via PillList `sponsored: true`. |

---

## Generation Instructions

### Step 1 — Read before writing

Before producing any output, read the Gold Master Specification and the validated reference article in full. Confirm you understand:

- The component import block (all 11 components)
- The OlspLayout props and how `<slot />` renders content
- The fixed section order and `id` values
- The three GoldMasterQuote placements
- The two ProductCta placements (first with custom description, second may omit it)
- The frontmatter metadata structure

### Step 2 — Plan the content sections

Using the research package, plan the specific content for each section before generating HTML. Identify:

- The product's core mechanic (for the SVG diagram)
- The pricing structure (for the Overview table)
- 4–6 competitors for the Comparison table
- 4+ pros and 4+ cons grounded in the research
- 5–6 scoring categories appropriate to this product
- 3 quiz questions that reflect this product's real decision factors
- 4–8 FAQ questions drawn from the research
- The third-party YouTube video URL (or note its absence)
- All source URLs and their affiliate status

### Step 3 — Generate the file

Generate the complete `.astro` file from top to bottom, in document order. Do not skip sections. Do not summarise or placeholder any section — every section must contain finished, publishable content.

---

## Structural Rules

These rules are non-negotiable. Violating any of them produces a file that fails the production standard.

**Architecture**
- Import OlspLayout and all 11 Gold Master components from `src/components/olsp-standard/`.
- First line of frontmatter: `export const prerender = true;`
- Declare `const pageTitle`, `const pageDescription`, and `const tocLinks` in frontmatter.
- Wrap all content in `<OlspLayout title={pageTitle} description={pageDescription} canonical="..." tocLinks={tocLinks}>`.
- Do NOT add a `<style>` block — all CSS is in OlspLayout.
- Do NOT add a `<script>` block — all JS is in OlspLayout.
- Do NOT add a `<head>` or `<body>` — the document shell is in OlspLayout.

**Components**
- HeroTag: text prop with product category and date.
- VerdictBox: two `<p>` tags — "Best for" and "Not ideal for".
- Methodology: two `<p>` tags — "Who wrote this" and "How this review was built".
- Callout: `type="warn"` or `type="info"` with inner content.
- ProductCta: `title`, `description` (optional on second instance), `buttonText`, `href`.
- GoldMasterQuote: no props, no customization. Three fixed placements.
- FaqItem: `question` and `answer` props.
- PillList: `items` array with `{label, url, sponsored?}` objects.
- AuthorBox: no props — renders from component internals.
- SiteFooter: no props — renders from component internals.

**Sections**
- Sections must appear in this order: `intro → overview → design → performance → ux → comparison → proscons → history → recommend → buy → verdict → faq → author → sources`
- Each `<section>` must have its fixed `id` attribute. Do not rename any section id.
- The `intro` section must not contain an `<h2>`. Every other section must open with an `<h2>`.
- GoldMasterQuote and ProductCta are placed between sections at the fixed positions.

**Score bars**
- Percentage widths must match the displayed fraction exactly: 5/5 = 100%, 4/5 = 80%, 3/5 = 60%, 2/5 = 40%, 1.5/5 = 30%, 1/5 = 20%.

**Quiz**
- Exactly three questions, using radio groups named `q1`, `q2`, `q3`.
- Answer values: `2` for the aligned answer, `0` for the misaligned answer.
- Outcome thresholds: score `≥ 5` = good fit, `≥ 3` = mixed fit, `< 3` = poor fit.

**SEO**
- `<title>` and `<h1>` must be different strings. Both must contain the target keyword.
- JSON-LD, Open Graph tags, and Twitter Card tags are generated by OlspLayout from its props — do not add any of these in the article file.
- Optionally pass `ogImage`, `datePublished`, `dateModified`, `articleType`, and `productName` props to OlspLayout when the research package provides them.
- Do not add a `<header>` or site navigation. `<SiteFooter />` is placed at the end of `#sources`.

**Links**
- Affiliate or tracking links in PillList must use `sponsored: true`.
- Non-affiliate external links use `sponsored: false` or omit the field.
- Internal links (href starting with `/`) must NOT have a `target` or `rel` attribute.

---

## Content and Editorial Rules

**Source fidelity**
- The research package is your primary and only source. Do not supplement it with facts from your training data unless you explicitly label them as general background knowledge that could not be confirmed from the research.
- Do not invent product details, pricing figures, feature descriptions, or the name of any person associated with the product unless they appear in the research package.

**Epistemic labelling**
Every factual claim must carry one of the following labels:

| Category | How to signal it |
|----------|------------------|
| Verified independently | State it plainly as fact, with the source noted |
| Vendor claim / marketing copy | "According to the official site…", "The product is marketed as…" |
| Third-party reported | "Independent reviewers describe…", "Multiple sources report…" |
| Could not be verified | "We could not independently confirm…", "This could not be verified…" |
| Self-reported / unaudited | "Self-reported by individual members…", "Not independently audited…" |

**Income and earnings claims**
Any income figure must be explicitly labelled as self-reported and unverified. Use `<Callout type="warn">` when surfacing these claims prominently.

**No first-hand testing**
Do not write as though you or the editorial team personally used, purchased, or tested the product unless the research package explicitly includes a first-hand account.

**Tone**
The site's editorial voice is measured, direct, and consumer-protective. It acknowledges what is unknown. It does not hype, condemn, or use superlatives.

---

## Component Rules

**HeroTag:** `Independent Review · Updated [Month Year]` — use the current month and year.

**VerdictBox:** "Best for" and "Not ideal for" must be grounded in the research, not generic.

**Methodology:** Use the supplied author bio. The "How this review was built" paragraph must accurately describe the research method used.

**Pricing table:** Mark all pricing as reported/unconfirmed if the research package does not include a screenshot or direct purchase confirmation.

**Comparison table:** Include the product being reviewed in the first row. Include 3–5 genuine alternatives.

**Pros & cons:** Four items on each side minimum. Each item must be a specific observation.

**SVG diagram:** Create an original diagram illustrating the product's core mechanic. Must have `role="img"` and `aria-label`.

**Score bars:** Choose 5–6 scoring categories meaningful for this specific product type.

**Quiz:** Three questions reflecting the actual decision factors for this product.

**FAQ:** Four questions minimum. Questions must come from the research.

**Video embed:** Use the YouTube URL from the research package. If none supplied, omit the video embed entirely.

**GoldMasterQuote (3 placements):**
1. Immediately after `</section> <!-- intro -->`, before the first ProductCta
2. After the UX section, before the comparison section
3. After the author section, before the sources section
No props. No customization. Exact same component at all three placements.

**ProductCta (1–2 placements):**
1. After the first GoldMasterQuote (post-intro) — include `description` prop
2. Near Final Verdict, before FAQ — `description` is optional (component uses default)
The `href` prop uses the product's affiliate URL. `buttonText` should be action-oriented.

**PillList:** Format sources as a list of `{label, url, sponsored?}` objects. Affiliate links use `sponsored: true`.

**SiteFooter:** One instance at the end of `#sources`, after the PillList and disclaimer paragraph.

---

## Output Specification

Produce exactly one output: the complete, finished content of the file `src/pages/reviews/[slug].astro`.

- Output the raw file content only.
- Do not add explanatory prose, section commentary, or notes before or after the file.
- Do not truncate any section. Do not use placeholder text.
- The file must be complete from the opening `---` frontmatter fence to the closing `</OlspLayout>` tag.

---

## Pre-Delivery Checklist

Before outputting the file, verify each item:

**Architecture**
- [ ] All 11 component imports are present from `src/components/olsp-standard/`
- [ ] `export const prerender = true;` is the first frontmatter statement
- [ ] `pageTitle`, `pageDescription`, and `tocLinks` are declared in frontmatter
- [ ] All content is wrapped in `<OlspLayout>` with required props
- [ ] No `<style>`, `<script>`, `<head>`, or `<body>` tags present in article file
- [ ] No duplicate HTML structure — OlspLayout provides the document shell

**Structure**
- [ ] All sections are present in the correct order (including `#author`)
- [ ] All section `id` values match the fixed names
- [ ] `intro` has no `<h2>`; all other sections open with `<h2>`
- [ ] Three GoldMasterQuote components at fixed positions
- [ ] Two ProductCta components at fixed positions (second one may omit description)
- [ ] SiteFooter at end of `#sources`

**Content**
- [ ] `<title>` ≠ `<h1>`
- [ ] Both `<title>` and `<h1>` contain the target keyword
- [ ] `<link rel="canonical">` matches the supplied canonical URL exactly
- [ ] `.hero-tag` contains the current month and year
- [ ] Methodology block present in `#intro`
- [ ] VerdictBox present in `#intro` after the opening paragraph
- [ ] Pros and cons have at least four items each
- [ ] Score bar percentages match their displayed fractions
- [ ] Quiz has exactly three fieldsets using `q1`, `q2`, `q3`
- [ ] FAQ has at least four `<FaqItem>` entries
- [ ] SVG diagram has `role="img"` and `aria-label`
- [ ] SVG `<figcaption>` states it is an original illustration
- [ ] All external links include `target="_blank"`
- [ ] Affiliate links use `sponsored: true` in PillList items
- [ ] Sources section ends with the disclaimer paragraph
- [ ] No income or earnings figures presented as verified or typical results
- [ ] No first-hand testing claimed unless the research package documents it
- [ ] No `<header>` or site navigation in article file
- [ ] GoldMasterQuote appears exactly 3 times with no props
- [ ] ProductCta first instance includes description prop; second may omit it
- [ ] ProductCta `href` uses product's affiliate URL with `sponsored` rel

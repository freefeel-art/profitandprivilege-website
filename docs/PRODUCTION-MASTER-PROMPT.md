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

Before producing any output, read the Gold Master Specification (`docs/GOLD-MASTER-SPEC.md`) and the validated reference article in full. **The Gold Master Specification is the authoritative rule set for all structural, component, and editorial rules** — architecture, section order, component usage, score bars, quiz, SEO, link rules, GoldMasterQuote frequency, CTA placement, internal linking, and editorial principles are all defined there. Do not duplicate rules in the generated file; follow the spec exactly.

Confirm you understand:

- The component import block (all 11 components)
- The OlspLayout props and how `<slot />` renders content
- The fixed section order and `id` values
- The GoldMasterQuote frequency (§5.6) — short articles 2–3, long-form 4–5
- The two ProductCta placements (§5.5, §16 rule 9) — CTA #1 post-intro, CTA #2 near conclusion
- The frontmatter metadata structure (§3)

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
- At least one natural internal link to an existing OLSP pillar article (e.g. `/reviews/olsp-academy/`)

### Step 3 — Generate the file

Generate the complete `.astro` file from top to bottom, in document order. Do not skip sections. Do not summarise or placeholder any section — every section must contain finished, publishable content.

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

**Internal linking**
Every article must include at least one natural contextual link to a relevant existing OLSP pillar article (e.g. `/reviews/olsp-academy/`). Links must be editorially relevant — never forced. If no natural connection exists, do not add a link.

**Editorial principle**
The article always solves the reader's problem first. The OLSP ecosystem is introduced naturally as the logical next step. Articles must never become sales pages.

---

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
- [ ] GoldMasterQuote appears 2–3× (short article) or 4–5× (long-form) — distributed naturally, never grouped
- [ ] Two ProductCta components present: CTA #1 post-intro, CTA #2 near conclusion
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
- [ ] ProductCta first instance includes description prop; second may omit it
- [ ] ProductCta `href` uses product's affiliate URL with `sponsored` rel
- [ ] At least one contextual internal link to an OLSP pillar article present (§10.1 of GOLD-MASTER-SPEC.md)
- [ ] Article solves reader's problem first; OLSP introduced naturally as logical next step (§16 rule 22)
- [ ] Article does not read as a sales page

# Blog / Informational Article — Master Specification

**Status:** Production
**Scope:** Article type `blog` only. Reviews and roundups have their own specs — see `docs/GOLD-MASTER-SPEC.md` and `docs/ROUNDUP-GOLD-MASTER-SPEC.md`.

This document codifies the standard already established across the 12 published blog articles. It is descriptive of current production practice, not a new design — no existing blog article needs to change as a result of this spec.

**Canonical reference (structure/CSS/JS):** `src/pages/blog/part-time-jobs-near-me-no-experience.astro`
**Canonical reference (metadata: OG tags + JSON-LD):** `src/pages/blog/make-money-online-for-beginners.astro`

No single existing file demonstrates every rule below at once — the structure/CSS/JS reference predates the OG+JSON-LD standard being applied consistently. New blog articles must combine both: the layout from the structure reference, the metadata block from the metadata reference.

---

## 1. Page Architecture

Same as Gold Master: a single, fully self-contained `.astro` file. Frontmatter contains **only** `export const prerender = true;` — no other variables, no imports. `<title>` and `<meta name="description">` are hardcoded strings in `<head>`, not interpolated from frontmatter constants.

(Three early blog articles — `b2b-lead-generation.astro`, `part-time-jobs-near-me-no-experience.astro`, `sales-lead-generation.astro` — declare `pageTitle` / `pageDescription` consts in frontmatter. This is a legacy pattern from before the no-interpolation rule was applied to blog articles. Do not carry it forward into new articles.)

The file must be ready to build and deploy without manual structural edits, and must pass `astro build` on first attempt.

---

## 2. HTML Document Structure & Layout

Identical to Gold Master: `<!DOCTYPE html>`, sticky two-column grid (`.layout` → `.toc-wrap` + `main`), CSS design tokens, typography, sticky TOC with scroll-spy, mobile TOC toggle. Copy the `<style>` block and `<script is:inline>` block verbatim from the canonical structure reference. See `docs/GOLD-MASTER-SPEC.md` Sections 2–6 and 10 — they apply unchanged to blog articles.

---

## 3. Section Structure

Blog articles use a free-form section count and naming — unlike reviews, there is no fixed 13-section list. Observed pattern across all 12 published articles:

1. `#intro` — no `<h2>` (contains the `<h1>` instead), opens with a hero tag and lead paragraph(s), a `.verdict-box` summarizing who the content is/isn't for
2. A CTA card (`.cta-card`) immediately after `#intro`
3. Numbered body sections (3–7 typically), each opening with `<h2>`. Section `id` values are either descriptive-slug (`#types`, `#earnings`) or generic (`#section-1`, `#section-2`) — either is acceptable, but must be consistent within one article and must match the TOC anchors exactly
4. A second CTA card roughly at the midpoint of the body sections
5. `#faq` — 6–8 `<details>` FAQ items (minimum 4, per Gold Master Section 8.11)
6. A third CTA card after FAQ, before the author box
7. `#author` — Author Box
8. `#sources` — Sources & References, `<ul class="pill-list">`
9. `<footer class="site-footer">`

**Exactly three `.cta-card` components per article**, identical in content, placed post-intro / mid-article / pre-author. This matches the CTA card rule in `docs/GOLD-MASTER-SPEC.md` Section 8.13 and `docs/ROUNDUP-MASTER-PROMPT.md`.

---

## 4. Components Used

Blog articles use a **subset** of the Gold Master component inventory (Section 8). The CSS block is copied verbatim from the structure reference regardless of which components a given article actually uses — do not trim unused CSS.

**Used in every article:**
- Hero Tag (8.1)
- Verdict Box (8.2)
- Callouts (8.4)
- CTA Card (8.13) — exactly three
- FAQ Accordion (8.11)
- Author Box (author box CSS class `.author-box`, same markup pattern as Section 8a of `docs/ROUNDUP-GOLD-MASTER-SPEC.md`)
- Sources Section / Pill-List (8.12)
- Site Footer (8.14)

**Used when the content calls for it (optional):**
- Tables (8.5) — for pay ranges, comparisons, data tables
- Pros & Cons Grid / `.two-col` `.pc-card` (8.6) — used in roughly half of published articles, when comparing methods or options

**Not used in blog articles:**
- Methodology Block (8.3)
- Score Bars (8.7)
- Self-Check Quiz (8.8)
- SVG Diagram (8.9)
- Video Embed (8.10)

These five components are review-specific. Do not add them to blog articles. (A handful of early blog articles carry unused CSS or vestigial markup for these — this is legacy noise, not a pattern to replicate.)

---

## 5. SEO & Metadata — Blog-Specific Exception to Gold Master

`docs/GOLD-MASTER-SPEC.md` Sections 11–12 state that reviews have **no** JSON-LD and **no** Open Graph/Twitter Card tags. **Blog articles are the deliberate exception** — this has been the consistent, established standard across published blog articles and must continue.

### Required `<head>` block for every blog article

```html
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{Exact title string}</title>
<meta name="description" content="{~155 char summary}" />
<link rel="canonical" href="https://olsp.profitandprivilege.com/blog/{slug}/" />
<meta property="og:title" content="{same as <title>}" />
<meta property="og:description" content="{same as meta description}" />
<meta property="og:url" content="{same as canonical}" />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="Profit and Privilege" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{same as <title>}" />
<meta name="twitter:description" content="{same as meta description}" />
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Article",
      "headline": "{article headline}",
      "description": "{meta description}",
      "datePublished": "{YYYY-MM-DD}",
      "dateModified": "{YYYY-MM-DD}",
      "url": "{canonical URL}",
      "author": { "@type": "Person", "name": "Jarmo Halonen", "url": "https://olsp.profitandprivilege.com/authors/jarmo-halonen" },
      "publisher": { "@type": "Organization", "name": "Profit and Privilege", "url": "https://olsp.profitandprivilege.com" },
      "mainEntityOfPage": { "@type": "WebPage", "@id": "{canonical URL}" }
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        { "@type": "Question", "name": "{question text}", "acceptedAnswer": { "@type": "Answer", "text": "{answer text}" } }
      ]
    }
  ]
}
</script>
```

Rules:
- The `FAQPage` `mainEntity` array must contain every FAQ question in the `#faq` section, in the same order, with matching question text.
- OG/Twitter title and description must exactly match `<title>` and `<meta name="description">` — no divergent copy.
- `datePublished` / `dateModified` use the actual publish/last-modified date, not a placeholder.
- `<title>` ≠ `<h1>` is not required for blog articles the way it is for reviews, but both must contain the target keyword.
- Canonical URL pattern: `https://olsp.profitandprivilege.com/blog/{slug}/` — absolute, trailing slash, production domain.
- `prerender = true` is still required (Section 1).

This exception is now also recorded in `docs/GOLD-MASTER-SPEC.md` Sections 11, 12, and 18 (rule 18) so a reader of the review spec is not misled into stripping OG/JSON-LD from blog articles.

---

## 6. Author Box

Same requirement and markup pattern as `docs/ROUNDUP-GOLD-MASTER-SPEC.md` Section 8a: sourced from `src/pages/authors/jarmo-halonen.astro`, includes photo, name, role, 2–4 sentence bio, and a link to `/authors/jarmo-halonen/`. Placed in its own `#author` section, immediately before `#sources`.

---

## 7. Internal Linking

Blog articles are the primary internal-linking hub type on the site (see `docs/CONTENT-REGISTRY.md`). Weave links to related reviews and other blog articles naturally into body content — do not restrict links to the sources section. Every blog article should link to at least one review (typically `/reviews/olsp-academy/`) and, where topically relevant, to sibling blog articles in the same content pillar.

---

## 8. External Links

Same standard as the rest of the site: every external link uses `target="_blank" rel="noopener noreferrer"`; affiliate/CTA links use `target="_blank" rel="noopener noreferrer sponsored"`. Internal links (`/...`) get no target/rel changes.

---

## 9. Pre-Delivery Checklist

Before delivering a blog article, verify:

- [ ] Frontmatter contains only `export const prerender = true;` — no other consts, no imports
- [ ] `<title>` and `<meta name="description">` are hardcoded, both contain the target keyword
- [ ] `<link rel="canonical">` matches the absolute production URL with trailing slash
- [ ] OG tags (`og:title`, `og:description`, `og:url`, `og:type`, `og:site_name`) present and matching `<title>`/description
- [ ] Twitter Card tags (`twitter:card`, `twitter:title`, `twitter:description`) present
- [ ] JSON-LD `@graph` present with `Article` + `FAQPage` types; `FAQPage` questions match the `#faq` section exactly
- [ ] Exactly three identical `.cta-card` components, placed post-intro / mid-article / pre-author
- [ ] `.verdict-box` present in `#intro`
- [ ] FAQ has at least four `<details>` items (typically 6–8)
- [ ] Author Box present in `#author`, sourced from the author profile page
- [ ] Sources section uses `<ul class="pill-list">` with the disclaimer paragraph
- [ ] `<footer class="site-footer">` present inside `<main>` after Sources
- [ ] No Methodology Block, Score Bars, Quiz, SVG Diagram, or Video Embed (review-only components)
- [ ] All external links use `target="_blank" rel="noopener noreferrer"` (or `...sponsored` for affiliate/CTA links)
- [ ] TOC has a link for every section, anchors match section `id`s exactly
- [ ] `astro build` passes on first attempt

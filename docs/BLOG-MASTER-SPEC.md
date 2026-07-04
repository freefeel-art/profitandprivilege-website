# Blog / Informational Article — Master Specification

**Status:** Production
**Scope:** Article type `blog` only (the Light Pipeline's output — see `docs/PIPELINE-ARCHITECTURE.md`). Reviews and roundups have their own specs — see `docs/GOLD-MASTER-SPEC.md` and `docs/ROUNDUP-GOLD-MASTER-SPEC.md`; their CTA card standard is unchanged by this document.

This document codifies the standard already established across the published blog articles, with two exceptions noted below, both dated 2026-07-04: blog articles use the **QuoteBanner** component (§ 3a) instead of `.cta-card` for three brand-signature touchpoints through the body, plus a single **Standard CTA** (§ 3b) — one real call-to-action, near the end of the article. These are deliberate, current changes to the standard, not a description of legacy practice. Existing published blog articles built before this date used `.cta-card` three times and are not retroactively rewritten by this spec change. (The QuoteBanner styling itself was also revised same-day, from a bordered/boxed treatment to a borderless brand-signature line — see § 3a.)

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

Blog articles use a free-form section count and naming — unlike reviews, there is no fixed 13-section list. Current pattern (as of 2026-07-04):

1. `#intro` — no `<h2>` (contains the `<h1>` instead), opens with a hero tag and lead paragraph(s), a `.verdict-box` summarizing who the content is/isn't for
2. A **QuoteBanner** (`.quote-banner`, see § 3a) immediately after `#intro`
3. Numbered body sections (3–7 typically), each opening with `<h2>`. Section `id` values are either descriptive-slug (`#types`, `#earnings`) or generic (`#section-1`, `#section-2`) — either is acceptable, but must be consistent within one article and must match the TOC anchors exactly
4. A second QuoteBanner roughly at the midpoint of the body sections
5. A third QuoteBanner immediately before `#faq` (not after it — this differs from the pre-2026-07-04 CTA card pattern, which placed the third promotional element after FAQ)
6. `#faq` — 6–8 `<details>` FAQ items (minimum 4, per Gold Master Section 8.11)
7. A single **Standard CTA** (`.standard-cta`, see § 3b) immediately after `#faq`, before the Author section
8. `#author` — Author Box
9. `#sources` — Sources & References, `<ul class="pill-list">`
10. `<footer class="site-footer">`

**Exactly three QuoteBanner components per article**, identical in content, placed post-intro / mid-article / pre-FAQ — plus **exactly one Standard CTA**, post-FAQ / pre-author. Blog articles no longer use `.cta-card` in its original three-times, sales-copy form (see § 3a/§ 3b for why). This is a blog-specific change — `docs/GOLD-MASTER-SPEC.md` Section 8.13 and `docs/ROUNDUP-MASTER-PROMPT.md`'s CTA card rule for reviews and roundups are unaffected.

---

## 3a. QuoteBanner Component (brand signature, revised 2026-07-04)

**Why:** QuoteBanner is a **brand signature, not an information box or a CTA** — a quiet, recurring editorial line that appears three times per article, carrying no button and no sales copy. It was first introduced as a bordered/boxed element on 2026-07-04, then revised same-day to remove the box entirely once it was clear the boxed treatment still read as "a CTA in disguise." The current version has no border, no background, no padding-box — just centered, bold-italic brand-blue text with generous vertical whitespace, functioning like a pull-quote rather than a callout.

**Fixed content — identical in every blog article, never rewritten per article:**

```html
<a href="https://olspacademy.com/c/profitandprivilege" class="quote-banner" target="_blank" rel="noopener noreferrer sponsored">
  <p>&ldquo;Discover the tools and training that can open the next chapter in your online marketing journey.&rdquo;</p>
</a>
```

- The link target (`https://olspacademy.com/c/profitandprivilege`) and quote text are both fixed and universal — unlike `.cta-card`, there is nothing to customize per article.
- `target="_blank" rel="noopener noreferrer sponsored"` — this is an external, monetized (affiliate-tracked) link, so it keeps `sponsored` per the site's external-links standard even though it is editorially framed, not a sales CTA.
- No button element, no border, no background box. The `<a>` wraps the entire banner — the whole thing is one clickable link.
- CSS (add to the article's `<style>` block, alongside the still-present but now-unused-in-blog `.cta-card`/`.cta-btn` rules, reused by § 3b — per § 4, unused CSS is never trimmed):

```css
.quote-banner{
  display:block;
  text-align:center;
  margin:4rem 0;
  text-decoration:none;
}
.quote-banner p{
  font-size:1.2rem;
  font-weight:700;
  font-style:italic;
  line-height:1.6;
  margin:0;
  color:var(--accent);
}
.quote-banner:hover p{color:#1d4ed8; text-decoration:none;}
```

`var(--accent)` is the site's primary brand blue (`#2563eb`), already defined as a design token in every article's `:root`. `4rem` top/bottom margin (no padding, no border) is the "generous whitespace" — the banner floats in open space rather than sitting in a box.

---

## 3b. Standard CTA Component (added 2026-07-04)

**Why:** With QuoteBanner now carrying no button and appearing three times as a brand signature, articles need exactly one real, unambiguous call-to-action — placed once, near the end, after the reader has finished the content and the FAQ. This is intentionally short: a heading and a button, nothing else. No sales paragraph.

**Fixed content — identical in every blog article, never rewritten per article:**

```html
<div class="cta-card standard-cta">
  <h3>Ready to Build More Than Just an Email List?</h3>
  <a href="https://olspacademy.com/megalive/1006001" class="cta-btn" target="_blank" rel="noopener noreferrer sponsored">Start with the $7 Megalink &rarr;</a>
</div>
```

- Reuses the existing `.cta-card` / `.cta-btn` CSS (already present in every article's `<style>` block per § 3a) — no new CSS class needed beyond the `.standard-cta` modifier below, which only removes the bottom margin so it sits flush before the Author section.
- No `<p>` sales paragraph. Heading + button only.
- Placement: immediately after `#faq`, immediately before `#author`. Exactly one per article — this is not repeated like QuoteBanner.
- `target="_blank" rel="noopener noreferrer sponsored"` — external, monetized link.

```css
.standard-cta{margin-bottom:0;}
```

**Important — this heading and button text are placeholders reflecting the site's current example, not literally fixed for every topic the way QuoteBanner's text is.** Unlike QuoteBanner (whose text never changes), the Standard CTA's heading should read naturally as "the logical next step after reading *this* article" — keep it just as short (one heading line, one button), but adapt the heading's wording to the article's topic rather than reusing "Ready to Build More Than Just an Email List?" verbatim on unrelated topics. The button text and destination URL (`https://olspacademy.com/megalive/1006001`, the standard Megalink CTA link) stay fixed across articles.

---

## 4. Components Used

Blog articles use a **subset** of the Gold Master component inventory (Section 8). The CSS block is copied verbatim from the structure reference regardless of which components a given article actually uses — do not trim unused CSS.

**Used in every article:**
- Hero Tag (8.1)
- Verdict Box (8.2)
- Callouts (8.4)
- QuoteBanner (§ 3a) — exactly three, replaces CTA Card (8.13) in blog articles as of 2026-07-04
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
- [ ] Exactly three identical `.quote-banner` QuoteBanner components (§ 3a) — borderless, centered, bold italic, brand blue — placed post-intro / mid-article / pre-FAQ
- [ ] Exactly one Standard CTA (§ 3b), post-FAQ / pre-author — heading + button only, no sales paragraph
- [ ] `.verdict-box` present in `#intro`
- [ ] FAQ has at least four `<details>` items (typically 6–8)
- [ ] Author Box present in `#author`, sourced from the author profile page
- [ ] Sources section uses `<ul class="pill-list">` with the disclaimer paragraph
- [ ] `<footer class="site-footer">` present inside `<main>` after Sources
- [ ] No Methodology Block, Score Bars, Quiz, SVG Diagram, or Video Embed (review-only components)
- [ ] All external links use `target="_blank" rel="noopener noreferrer"` (or `...sponsored` for affiliate/CTA links)
- [ ] TOC has a link for every section, anchors match section `id`s exactly
- [ ] `astro build` passes on first attempt

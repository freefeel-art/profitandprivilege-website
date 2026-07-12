# Editorial Builder — Output Specification

## File Format

```
---
export const prerender = true;
---
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{article title}</title>
  <meta name="description" content="{meta description}" />
  <link rel="canonical" href="https://olsp.profitandprivilege.com/{type}/{slug}/" />
  <!-- per-type head additions (OG tags, JSON-LD) -->
</head>
<body>
  <!-- article content -->
  <style is:inline>/* full CSS block */</style>
  <script is:inline>/* full JS block */</script>
</body>
</html>
```

`export const prerender = true;` is the **only** frontmatter entry. No imports, no other exports, no additional constants.

## Component Inventory

All components are defined in `docs/GOLD-MASTER-SPEC.md` sections 8.1–8.14 (and `docs/BLOG-MASTER-SPEC.md` sections 3a–3b for blog-specific components).

| # | Component | Review | Blog | Roundup |
|---|---|---|---|---|
| 8.1 | Hero Tag | ✅ | ✅ | ✅ |
| 8.2 | Verdict Box | ✅ | ✅ | ✅ |
| 8.3 | Methodology Block | ✅ | ❌ | ❌ |
| 8.4 | Callouts | ✅ | ✅ | ✅ |
| 8.5 | Tables | ✅ | optional | ✅ |
| 8.6 | Pros & Cons Grid | ✅ | optional | ✅ |
| 8.7 | Score Bars | ✅ | ❌ | ❌ |
| 8.8 | Self-Check Quiz | ✅ | ❌ | ❌ |
| 8.9 | SVG Diagram | ✅ | ❌ | ❌ |
| 8.10 | Video Embed | ✅ | ❌ | ❌ |
| 8.11 | FAQ Accordion | ✅ | ✅ | ✅ |
| 8.12 | Sources / Pill-List | ✅ | ✅ | ✅ |
| 8.13 | CTA Card (×3) | ✅ | ❌ | ✅ |
| 8.14 | Site Footer | ✅ | ✅ | ✅ |
| § 3a | QuoteBanner (×3) | ❌ | ✅ | ❌ |
| § 3b | Standard CTA (×1) | ❌ | ✅ | ❌ |
| — | Author Box | ❌ | ✅ | ✅ |

## CSS Block

The `<style is:inline>` block must contain the CSS for **every** component listed in `docs/GOLD-MASTER-SPEC.md` sections 8.1–8.14, copied verbatim — regardless of which components the article actually uses. Do not trim unused CSS.

For blog articles, additionally include the `.quote-banner` and `.standard-cta` CSS from `docs/BLOG-MASTER-SPEC.md` sections 3a–3b.

## JavaScript Block

The `<script is:inline>` block must contain:

1. Mobile TOC toggle (`#tocToggle` click → toggle `.open` on `#tocWrap`)
2. Scroll-spy (`IntersectionObserver` watching `main section` elements, `rootMargin: '-20% 0px -70% 0px'`)
3. TOC link-close on mobile (each TOC `<a>` removes `.open` from `#tocWrap` at `width <= 900`)
4. Quiz evaluation (`evaluateQuiz` global function) — included conditionally:
   - **Reviews:** always included (quiz is a required component)
   - **Blogs:** included only if the blog spec adds quiz logic (currently unused, include stub or omit)
   - **Roundups:** included with per-question matching logic (not cumulative threshold)

The `is:inline` directive is required — do not use a bare `<script>` tag.

## Head Section Per Type

### Review
```
<title>{title}</title>
<meta name="description" content="{~155 char summary}" />
<link rel="canonical" href="https://olsp.profitandprivilege.com/reviews/{slug}/" />
```
No OG tags, no Twitter Card tags, no JSON-LD.

### Blog
```
<title>{title}</title>
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
{/* Article + FAQPage */}</script>
```
OG and Twitter tags must exactly match `<title>` and `<meta name="description">`. JSON-LD `FAQPage` `mainEntity` must match FAQ questions exactly.

### Roundup
```
<title>{title}</title>
<meta name="description" content="{~155 char summary}" />
<link rel="canonical" href="https://olsp.profitandprivilege.com/roundups/{slug}/" />
```
No OG tags, no Twitter Card tags, no JSON-LD (same as reviews).

## External Links Standard

| Link Type | `target` | `rel` |
|---|---|---|
| Internal (`/...`) | (none) | (none) |
| External, non-affiliate | `_blank` | `noopener noreferrer` |
| External, affiliate/CTA/sponsored | `_blank` | `noopener noreferrer sponsored` |

Applied to every `<a>` tag in the article body, navigation, and footer.

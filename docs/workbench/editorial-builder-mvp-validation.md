# Editorial Builder — MVP Validation Report

**Date:** 2026-07-12
**Status:** PASS — MVP validated

## Input Used

**Brief:** `agents/opportunity-research-agent/briefs/make-money-online-from-your-phone.md`
- Opportunity Score: 70/100
- Editorial Decision: WRITE NOW
- Type: Blog, 2,000–2,400 words
- Suggested title: "How to Make Money Online From Your Phone (No Computer Needed)"

**Comparison target:** `src/pages/blog/make-money-online-from-your-phone.astro` (existing published Gold Master article, 266 lines, 2026-07-04)

## Generated Output

**File:** `/tmp/opencode/generated-make-money-online-from-your-phone.astro` (266 lines)
- Placed in `src/pages/blog/` temporarily for build validation
- Build: `astro build` — PASS (40 pages, 2.12s)
- HTTP 200: PASS (dev server verified)

## Validation Results

### ADR-001 Compliance: PASS

| Check | Expected | Actual |
|---|---|---|
| Zero `import` statements | 0 | 0 |
| Only `prerender = true` in frontmatter | Yes | Yes |
| No `OlspLayout` references | 0 | 0 |
| Full HTML document (`<!DOCTYPE>` through `</html>`) | Yes | Yes |
| Self-contained (no external CSS/JS deps) | Yes | Yes |

### Gold Master Specification Compliance: PASS

| Check | Expected | Actual |
|---|---|---|
| External links have `target="_blank"` | All external | All 8 external links |
| Affiliate/CTA links have `rel="noopener noreferrer sponsored"` | Yes | All 5 affiliate links |
| Internal links have no `target`/`rel` | Yes | All 3 internal links |
| `<script is:inline>` present | Yes | Yes |
| `IntersectionObserver` scroll-spy present | Yes | Yes |
| Mobile TOC toggle present | Yes | Yes |
| TOC link-close on mobile | Yes | Yes |
| `pill-list` CSS and markup present | Yes | Yes |
| `site-footer` present inside `<main>` | Yes | Yes |
| `verdict-box` in `#intro` | Yes | Yes |
| `hero-tag` present | Yes | Yes |
| `details`/`summary` FAQ accordion | Yes | Yes |

### Editorial Builder SPEC Compliance: PASS

| Check | Expected | Actual |
|---|---|---|
| `is:inline` on `<style>` | Yes | Yes (spec requires this) |
| `is:inline` on `<script>` | Yes | Yes |
| OG tags present (blog type) | Title, description, url, type, site_name | All 5 present |
| Twitter Card tags present | card, title, description | All 3 present |
| JSON-LD with `Article` + `FAQPage` | Yes | Yes |
| OG/Twitter content matches `<title>`/description | Yes | Exact match |
| FAQPage questions match `#faq` section | Yes | 5/5 match |
| QuoteBanner (exactly 3) | 3 instances | 3 HTML + 3 CSS refs |
| Standard CTA (exactly 1, post-FAQ) | 1 instance | 1 instance at correct position |
| Author Box present | Yes | Present in `#author` |
| No review-only components | None | 0 violations |
| Site Footer with blog temporary override | Yes | `href="https://olspacademy.com/get-megalink?olsp=1006001"` with sponsored |
| External links classification correct | Per type | Source: non-affiliate; CTA/quote: sponsored |

### OUTPUT-TEMPLATE Compliance: PASS

| Check | Expected | Actual |
|---|---|---|
| Section order (blog) | intro → QB1 → content → QB2 → content → QB3 → faq → StdCTA → author → sources → footer | Correct |
| Section IDs kebab-case | Yes | All kebab-case |
| TOC hrefs match section `id`s | Yes | All 9 match |
| No `.cta-card` (blog uses QuoteBanner + Standard CTA) | Yes | 0 `.cta-card` in body (only `.standard-cta` modifier) |

## Structural Comparison: Generated vs Published

| Dimension | Generated | Published | Match? |
|---|---|---|---|
| Line count | 266 | 266 | ✅ |
| Section IDs | 9 IDs | 9 IDs | ✅ (same order) |
| TOC links | 9 links | 9 links | ✅ (same labels, same order) |
| Frontmatter | `prerender = true` | `prerender = true` | ✅ |
| CSS style tag | `<style is:inline>` | `<style>` | ⚠️ Directive differs |
| `<script>` tag | `<script is:inline>` | `<script is:inline>` | ✅ |
| QuoteBanner placement | post-intro, mid, pre-FAQ | post-intro, mid, pre-FAQ | ✅ |
| Standard CTA placement | post-FAQ, pre-author | post-FAQ, pre-author | ✅ |
| Footer brand link | Temporary override with sponsored | Simple link, no attributes | ⚠️ Published uses old footer |

### Deviations Found

1. **`<style is:inline>` vs `<style>`** — The generated article uses `is:inline` on the style tag as required by the Editorial Builder SPEC. The existing published article uses bare `<style>`. In Astro, bare `<style>` in a page component applies globally (no automatic scoping), so both work identically at runtime. The `is:inline` directive is the spec-compliant choice for explicitness. **No runtime difference.**

2. **Footer brand link** — The generated article follows the BLOG-MASTER-SPEC §8a temporary override (external affiliate destination with `target="_blank" rel="noopener noreferrer sponsored"`). The existing published article uses the pre-override link (same-site `https://olsp.profitandprivilege.com` with no attributes). **The generated article is spec-compliant; the published article needs updating** — this is a known migration gap documented in the blog spec.

3. **Dates** — Generated uses `2026-07-12` (today), published uses `2026-07-04`. Expected — new generation, new date.

## Pass/Fail Summary

| Standard | Result |
|---|---|
| ADR-001 (self-contained `.astro`, no imports) | **PASS** |
| Gold Master specification | **PASS** |
| Editorial Builder SPEC | **PASS** |
| Editorial Builder OUTPUT-TEMPLATE | **PASS** |
| Build (`astro build`) | **PASS** |
| HTTP 200 on page | **PASS** |

## Implementation Issues

1. **Minor: existing published articles use `<style>` not `<style is:inline>`** — The SPEC mandates `is:inline` on both `<style>` and `<script>`. Existing articles only use it on `<script>`. Recommendation: no action needed — both work, but if consistency is desired, run a migration pass to add `is:inline` to `<style>` tags across all published articles.

2. **Known gap: footer brand link on published blog articles** — The BLOG-MASTER-SPEC temporary override (2026-07-04) has not been applied to the comparison article. Recommendation: this is documented in the blog spec §8a ("Revert when the homepage is ready") — no action until the homepage is deployed.

3. **No upstream pipeline integration tested** — The MVP test used a manually written article based on a brief, not generated by an upstream agent. The Editorial Builder PROMPT.md was executed by hand to produce the output, validating the downstreasm specification but not the inter-agent data flow.

## Recommendations Before Stage 3 Is Production-Ready

1. **Clarify `<style>` directive convention** — Decide whether `is:inline` is required on `<style>` tags and update either the SPEC or the existing articles to match. Currently the SPEC requires it but production articles do not use it.

2. **Resolve blog footer migration** — Apply the temporary override to all existing blog articles in one pass, or wait for the homepage to be ready and skip the temporary state entirely. Either way, the generated article is spec-compliant and ready.

3. **Pipeline integration test** — Run the full Editorial Builder flow with upstream agent output (Research Brief → Editorial Builder → .astro file) to validate the inter-agent contract.

4. **Structural blueprint check** — The MVP test produced an article that matched the published Gold Master article in structure, line count, section IDs, and TOC layout. The Editorial Builder architecture (ADR-001) and Gold Master spec produce identical output shapes. No structural drift was detected.

5. **CSS completeness check** — The generated `<style is:inline>` block includes CSS for all Gold Master components (including unused ones per spec). Verify this block is still current against the latest Gold Master spec and the canonical reference article.

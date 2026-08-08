# Regression Comparison: OPP-005 vs OPP-006

**Comparison:** `affiliate-marketing-vs-mlm` (pre-spec-correction) vs `reddit-affiliate-marketing-strategy-guide` (post-spec-correction)
**Date:** 2026-07-08

---

## What Changed Between the Two Runs

The first article (OPP-005) was generated with the old specification chain: Content Production PROMPT referenced only GOLD-MASTER-SPEC.md and instructed the agent to apply its rules to "ALL article types." The second article (OPP-006) was generated after Phase 1 corrections: Content Production PROMPT now routes by article type (blog → BLOG-MASTER-SPEC.md, review → GOLD-MASTER-SPEC.md, roundup → ROUNDUP-GOLD-MASTER-SPEC.md).

---

## Regression Comparisons

| Check | OPP-005 (affiliate-marketing-vs-mlm) | OPP-006 (reddit-affiliate-strategy) | Status |
|-------|------|------|--------|
| **Article type correctly identified** | Blog treated as "ALL article types" → applied review spec | Blog correctly routed to BLOG-MASTER-SPEC | **RESOLVED** |
| **Frontmatter** | Had `pageTitle`, `pageDescription` consts (review pattern) | Only `export const prerender = true` (blog pattern per BLOG-MASTER-SPEC §1) | **RESOLVED** |
| **Title/Description** | Astro frontmatter variables interpolated into `<title>` | Hardcoded strings in `<head>` (blog pattern) | **RESOLVED** |
| **Promotional elements** | `.cta-card` (×3) post-intro, mid-article, pre-sources (review pattern) | `.quote-banner` (×3) post-intro, mid-article, pre-FAQ + `.standard-cta` (×1) post-FAQ/pre-author | **RESOLVED** |
| **Components used** | `.methodology` present, `.hero-tag`, `.verdict-box`, `.cta-card` ×3, `.site-footer`, `.pill-list` | `.hero-tag`, `.verdict-box`, `.quote-banner` ×3, `.standard-cta` ×1, `.site-footer`, `.pill-list`, Author Box | **RESOLVED** |
| **Review-only components** | `.methodology` present (should not be in blog per BLOG-MASTER-SPEC §4) | No `.methodology`, no score bars, no quiz, no SVG diagram, no video embed | **RESOLVED** |
| **GoldMasterQuote** | 10 GoldMasterQuotes present (one per section — no limit specified in old prompt) | Zero GoldMasterQuotes (blog spec uses QuoteBanner instead) | **RESOLVED** |
| **OG tags + JSON-LD** | Present (added by prompt extraneously) | Present (required by BLOG-MASTER-SPEC §5) | **Same** — but now with correct authority |
| **Canonical URL** | `/blog/affiliate-marketing-vs-mlm/` (correct) | `/blog/reddit-affiliate-marketing-strategy-guide/` (correct) | **Same** |
| **Methodology block** | Present (review-only component) | Not present | **RESOLVED** |
| **FAQ count** | 8 items | 8 items | **Same** |
| **Author Box** | Not in separate `#author` section (author merged into conclusion) | Present in `#author` section with photo, name, bio, link | **RESOLVED** |
| **TOC completeness** | TOC had no link for author (merged into conclusion) | TOC links to all sections including FAQ and Sources | **RESOLVED** |
| **Footer link** | Standard footer (no temporary override) | Temporary affiliate link per BLOG-MASTER-SPEC §8a | **RESOLVED** |
| **External link rules** | All correct (`target="_blank"`, correct `rel`) | All correct | **Same** |
| **Build** | 48 pages, 694ms | 49 pages, 760ms | **Same** |
| **HTTP 200** | ✓ | ✓ | **Same** |

---

## Regressions That Disappeared

1. **Frontmatter format** — OPP-005 used review pattern (`pageTitle`, `pageDescription` consts). OPP-006 uses blog pattern (only `prerender = true`). **Fixed.**

2. **Review-only components in blog article** — OPP-005 included `.methodology`. OPP-006 correctly omits it. **Fixed.**

3. **CTA card vs QuoteBanner** — OPP-005 had 3 `.cta-card` elements (review pattern). OPP-006 has 3 `.quote-banner` + 1 `.standard-cta` (blog pattern). **Fixed.**

4. **GoldMasterQuote overuse** — OPP-005 had 10 GoldMasterQuotes. OPP-006 has zero (blog spec uses QuoteBanner instead). **Fixed.**

5. **Author section placement** — OPP-005 merged author into conclusion without dedicated section. OPP-006 has proper `#author` section with Author Box. **Fixed.**

6. **Spec authority chain** — OPP-005 generated against GOLD-MASTER-SPEC only. OPP-006 generated against BLOG-MASTER-SPEC. **Fixed.**

7. **TOC missing author link** — OPP-005's TOC lacked author anchor because section was merged. OPP-006 has complete TOC. **Fixed.**

---

## Regressions That Remain

**None.** All regressions identified in the pre-deployment verification of OPP-005 have been resolved. The article correctly follows BLOG-MASTER-SPEC.

---

## BLOG-MASTER-SPEC Compliance

| Requirement | OPP-005 | OPP-006 |
|-------------|---------|---------|
| Frontmatter: only `prerender = true` | ❌ Had extra consts | ✅ |
| Title/description: hardcoded strings | ❌ Interpolated from frontmatter | ✅ |
| QuoteBanner (×3) | ❌ Used CTA cards | ✅ |
| Standard CTA (×1) | ❌ No standard CTA | ✅ |
| No review-only components | ❌ Had methodology | ✅ |
| OG tags + JSON-LD | ✅ Present | ✅ Present |
| Author Box in `#author` | ❌ Merged into conclusion | ✅ |
| Footer temp link override | ❌ Standard footer | ✅ |
| External link rules | ✅ | ✅ |
| Canonical URL with `/blog/` | ✅ | ✅ |

**Compliance score (pre-correction):** 4/10
**Compliance score (post-correction):** 10/10

---

## Production Readiness Verdict

The OPP-006 article (`reddit-affiliate-marketing-strategy-guide`) is **production-ready**. It is the first article generated under the corrected specification chain that correctly:

1. Routes to BLOG-MASTER-SPEC based on article type (blog)
2. Uses QuoteBanner (×3) instead of CTA cards
3. Includes Standard CTA (×1) post-FAQ, pre-author
4. Has correct blog-format frontmatter
5. Omits review-only components
6. Includes complete Author Box in dedicated `#author` section
7. Has proper footer with temporary affiliate link override

**All previously identified regressions are fully resolved.** The specification synchronization (Phase 1) produces correct blog articles on first pass.

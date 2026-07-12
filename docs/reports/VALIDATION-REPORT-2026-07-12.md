# Production Validation Report

**Date:** 2026-07-12
**Topic:** How much money do real affiliates actually make after their first year?
**Article:** how-much-can-beginners-realistically-earn-online.astro
**Validator:** Automated inspection + Gold Master spec comparison

---

## 1. Generated Assets

| Asset | Exists | Path | Size | Created |
|-------|--------|------|------|---------|
| Opportunity Brief | ✓ | agents/opportunity-discovery-agent/OPPORTUNITY-QUEUE.md | 23,029 B | 2026-07-12 11:54 |
| Research Brief | ✓ | agents/opportunity-research-agent/briefs/how-much-can-beginners-realistically-earn-online.md | 6,095 B | 2026-07-04 07:00 |
| Generated Article | ✓ | src/pages/blog/how-much-can-beginners-realistically-earn-online.astro | 12,342 B | 2026-07-12 08:55 |
| QA Report | ✗ | NOT FOUND for this article | — | — |
| Publication Report | ✗ | NOT FOUND for this article | — | — |

---

## 2. Article Validation

| Check | Status | Detail |
|-------|--------|--------|
| Generated file exists | ✓ | 12,342 bytes |
| Astro page exists | ✓ | dist/client/blog/how-much-can-beginners-realistically-earn-online/index.html |
| Uses Gold Master layout | ✓ | OlspLayout imported |
| Word count | 1,469 | Below typical 2,000+ target |
| Heading structure | ✓ | h1 → h3 → 6× h2 → h2 FAQ → h2 Author → h2 Sources |
| Required sections | ✓ | 10 sections with correct IDs |
| Internal links | ⚠ | Only 1 internal link (/blog/make-money-online-for-beginners/) |
| CTA blocks | ✗ | Uses inline .cta-card, not Standard CTA component |
| FAQ section | ✓ | 7 FaqItem components |
| Schema | ✓ | JSON-LD present |
| SEO metadata | ✓ | title, description, canonical all present |

---

## 3. Gold Master Compliance (Blog Spec)

### ✓ Passing

- Gold Master layout (OlspLayout)
- Hero tag (inline span.hero-tag)
- Introduction section (#intro)
- VerdictBox (inline div.verdict-box)
- 6 numbered body sections
- FAQ section (7 items)
- Author section (AuthorBox)
- SiteFooter
- prerender = true
- Canonical URL
- SEO metadata
- JSON-LD schema
- 3× QuoteBanner (within 2-3 range for short articles)

### ✗ Failing

| Requirement | Status | Detail |
|-------------|--------|--------|
| Standard CTA #1 | ✗ MISSING | Should be after intro + QuoteBanner |
| Standard CTA #2 | ✗ MISSING | Should be after FAQ, before Author |
| Standard CTA format | ✗ WRONG | Uses .cta-card with sales copy instead of heading+button only |
| Sources PillList | ✗ MISSING | Uses inline <ul class="pill-list"> instead of PillList component |
| Editorial Builder compliance | ✗ VIOLATION | Article has 6 imports; PROMPT.md requires "zero imports" |

---

## 4. Production Timing

| Stage | Timestamp | Duration |
|-------|-----------|----------|
| Queue discovery | 2026-07-12 11:54 | — |
| Research brief | 2026-07-04 07:00 | — (created earlier) |
| Article generation | 2026-07-12 08:55 | — |
| QA report | NOT FOUND | — |
| Publication report | NOT FOUND | — |

Note: The brief was created 8 days before the article. The article was generated but QA and publication were never completed for this specific article.

---

## 5. Writer Audit

| Item | Value |
|------|-------|
| Writer implementation | Editorial Builder (agents/editorial-builder/) |
| Prompt used | agents/editorial-builder/PROMPT.md |
| Layout/template | OlspLayout (src/components/olsp-standard/OlspLayout.astro) |
| Spec followed | docs/BLOG-MASTER-SPEC.md |
| Source files | OPPORTUNITY-QUEUE.md → brief → article |

**Critical finding:** The Editorial Builder PROMPT.md states: "Every article you produce must be a single self-contained .astro file with zero imports." The generated article has 6 imports. This is a direct violation of the writer's own architecture constraint.

---

## 6. Final Verdict

### FAIL

The pipeline did not generate a production-ready Gold Master article.

**Reasons:**

1. **Missing Standard CTAs** — Blog spec requires exactly 2 Standard CTA components (heading + button). The article uses an inline .cta-card with sales copy instead, and is missing CTA #2 entirely.

2. **Missing PillList component** — Sources section uses inline HTML instead of the PillList component.

3. **Architecture violation** — The Editorial Builder PROMPT requires "zero imports" but the article has 6 imports. This suggests the article was written by a different process (likely the OlspLayout migration in commit 025deec) rather than the Editorial Builder pipeline.

4. **No QA or Publication reports** — The pipeline never completed Stages 3-4 for this article.

5. **No evidence of pipeline execution** — The article was created during a bulk migration commit, not through the Editorial Builder → QA → Publisher pipeline.

**Root cause:** The article was generated outside the pipeline (during the OlspLayout migration) and does not conform to the current Editorial Builder or Blog Master specifications. The pipeline has never successfully produced a complete Gold Master article from seed keyword to published output.

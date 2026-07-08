# Content Production — Implementation

**Date:** 2026-07-08
**Status:** Implemented

Transforms Research Reports into structured editorial content. Only generates structured content data — presentation (HTML, Astro) remains outside this stage.

**Input:** `research/output/research-reports/{pillar}-research-report.json`
**Output:** `research/output/content/{pillar}-content.json`

## Format Templates

| Format | Sections |
|--------|----------|
| Guide | introduction, what_is_this, why_it_matters, step_by_step_guide, common_mistakes, tips, faq, conclusion |
| Comparison | introduction, overview, detailed_comparison, pros_and_cons, which_is_best, faq, conclusion |
| Myth-busting | introduction, myth_1-5, the_truth, conclusion |
| Evidence-based | introduction, landscape, key_findings, evidence_analysis, applications, limitations, conclusion |

## Usage

```bash
python -m research.content_production.producer
```

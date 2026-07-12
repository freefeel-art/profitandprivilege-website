# Editorial QA — Implementation

**Date:** 2026-07-12
**Status:** Implemented (v2)

Validates produced content against editorial rules before packaging.

**Input:** `research/output/content/{pillar}-content.json` + Research Report
**Output:** `research/output/qa-reports/{pillar}-qa-report.json`

## Checks performed

| Check | Type | Description |
|-------|------|-------------|
| Gold Master structure | PASS/FAIL | All required sections present for format |
| Evidence support | PASS/WARN | Evidence references available per section |
| Internal consistency | PASS/FAIL | No duplicate section IDs |
| Citations available | PASS/WARN | At least one citation exists |
| Knowledge gaps | PASS | Gaps documented (info only) |
| Word count viability | PASS/WARN | Minimum 500 words |
| Internal linking | PASS/FAIL | At least one contextual link to an OLSP pillar article exists (reviews, blogs, roundups) |
| Quote sentence distribution | PASS/FAIL | GoldMasterQuote (reviews) or QuoteBanner (blogs) distributed appropriately for article length — 2–3 short, 4–5 long-form; never grouped |
| CTA placement | PASS/FAIL | CTA #1 in upper visible part of article (post-intro); CTA #2 near conclusion before final closing section |
| Editorial principle | PASS/FAIL | Article solves reader's problem first; OLSP introduced naturally as logical next step; not a sales page |

## Usage

```bash
python -m research.editorial_qa.validator
```

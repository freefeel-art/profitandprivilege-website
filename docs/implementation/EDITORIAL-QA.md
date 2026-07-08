# Editorial QA — Implementation

**Date:** 2026-07-08
**Status:** Implemented

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

## Usage

```bash
python -m research.editorial_qa.validator
```

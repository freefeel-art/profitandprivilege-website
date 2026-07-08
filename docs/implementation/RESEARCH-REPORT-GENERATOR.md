# Research Report Generator — Implementation

**Date:** 2026-07-08
**Status:** Implemented

Transforms Research Packages into the canonical Research Report. Organises evidence into clear sections for Content Production.

**Input:** `research/output/research-packages/{pillar}-research-package.json`
**Output:** `research/output/research-reports/{pillar}-research-report.json`

## Structure

- research_summary (total evidence, high/medium confidence, sources, facts, gaps)
- key_findings (top high-confidence findings)
- evidence_breakdown (by category)
- fact_summary (verified claims with reliability notes)
- knowledge_gaps
- recommended_citations (sources for the writer)

## Usage

```bash
python -m research.research_report.generator
```

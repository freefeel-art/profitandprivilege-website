# Research Factory — Implementation

**Date:** 2026-07-08
**Status:** Implemented

Builds the factual foundation from Opportunity Briefs. Collects evidence from Discovery Packages and organises into Evidence Library, Source List, Fact Summary, and Knowledge Gap Log.

**Input:** `research/output/opportunity-briefs/{pillar}-opportunity-brief.json` + Discovery Package
**Output:** `research/output/research-packages/{pillar}-research-package.json`

## Components

- **Evidence Library** — all relevant CI findings matched to each brief
- **Source List** — deduplicated community sources with reliability labels
- **Fact Summary** — top claims with verified answers and confidence
- **Knowledge Gap Log** — topics with insufficient evidence

## Usage

```bash
python -m research.research_factory.factory
```

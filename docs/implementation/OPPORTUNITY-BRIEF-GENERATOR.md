# Opportunity Brief Generator — Implementation

**Date:** 2026-07-08
**Status:** Implemented

Transforms Editorial Intelligence into canonical Opportunity Briefs. No article generation. Only structured editorial planning.

**Input:** `research/output/editorial-intelligence/{pillar}-editorial-intelligence-report.json`
**Output:** `research/output/opportunity-briefs/{pillar}-opportunity-brief.json`

## Structure per brief

- brief_id, working_title, primary_question, root_problem
- target_audience, recommended_format, pipeline_type (Heavy/Light)
- priority_score, signal_strength, confidence_score, intensity
- estimated_effort, source_cluster
- related_questions, candidate_affiliate_products, internal_linking_candidates
- narrative_context (beliefs, fears, desires from community)

## Usage

```bash
python -m research.opportunity_brief.generator
```

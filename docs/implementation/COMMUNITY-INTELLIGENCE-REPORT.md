# Community Intelligence Report — Implementation

**Date:** 2026-07-08
**Status:** Implemented, awaiting architectural review
**Architecture freeze:** Active

---

## Purpose

The Community Intelligence Report Generator transforms structured Community Intelligence findings (from the [CI Processor](COMMUNITY-INTELLIGENCE-PROCESSOR.md)) into the **canonical Community Intelligence Report** — a clean, organised summary of all community signals organised by section.

This is the final output of the **Community Intelligence** stage. Editorial Intelligence consumes this report to begin strategic analysis.

---

## Inputs

| Input | Location | Description |
|---|---|---|
| CI Package | `research/output/community-intelligence/{pillar}-community-intelligence.json` | Structured findings with 12 categories |
| Discovery Package (optional) | `research/output/discovery/{pillar}-discovery.json` | Raw posts — used only for Emerging Topics timestamp analysis |

---

## Outputs

| Output | Location | Description |
|---|---|---|
| CI Report | `research/output/community-intelligence-reports/{pillar}-community-intelligence-report.json` | Canonical report with all evidence organised by section |

---

## Report Structure

```
report_metadata
├── pillar_name
├── pillar_slug
├── generated_at
├── report_version
└── source_ci

executive_summary
├── pillar_name / pillar_slug
├── posts_analyzed
├── communities_analyzed
├── coverage_percent
├── collection_date
├── generated_at
├── total_finding_categories
├── total_finding_entries
├── unique_source_posts
├── source_discovery_package
├── provider
├── total_queries_executed
└── unique_posts_collected

sections
├── most_frequent_questions            (from CI: recurring_questions)
├── most_frequent_pain_points          (from CI: pain_points)
├── most_frequent_frustrations         (from CI: frustrations)
├── most_common_misconceptions         (from CI: misconceptions)
├── frequently_mentioned_tools         (from CI: frequently_mentioned_tools)
├── frequently_mentioned_competitors   (from CI: frequently_mentioned_competitors)
├── desired_outcomes                   (from CI: desired_outcomes)
├── common_beginner_mistakes           (from CI: common_beginner_mistakes)
├── positive_signals                   (from CI: positive_signals)
├── negative_signals                   (from CI: negative_signals)
├── representative_quotes              (from CI: representative_quotes)
├── supporting_evidence                (from CI: supporting_evidence)
└── emerging_topics                    (computed from recency analysis)
```

### Section Structure (standard)

```json
{
  "total_findings": 25,
  "high_confidence": 11,
  "medium_confidence": 9,
  "low_confidence": 5,
  "unique_contributing_posts": 83,
  "findings": [
    {
      "finding": "Users report: struggle",
      "frequency": 7,
      "confidence": "high",
      "supporting_source_count": 7,
      "source_posts": [
        {
          "post_id": "1r2w1oz",
          "title": "Is affiliate marketing still worth starting in 2026?",
          "subreddit": "AffiliateMarket",
          "url": "https://www.reddit.com/r/AffiliateMarket/comments/...",
          "timestamp": 1770909297,
          "snippet": "Is affiliate marketing still a good opportunity for beginners?..."
        }
      ]
    }
  ]
}
```

### Emerging Topics Section

Emerging topics are identified mechanically: for each finding, the median timestamp of its source posts is computed. If the median is above the global median timestamp (i.e. more recent than average), the finding is flagged as emerging. No interpretation is applied.

```json
{
  "method": "Median post timestamp above global median — mechanical, no interpretation",
  "global_median_timestamp": 1775000000,
  "total_emerging": 437,
  "unique_posts_contributing": 141,
  "emerging_topics": [
    {
      "finding": "A Crucial Update For Email Open Rate Tracking",
      "category": "recurring_questions",
      "frequency": 1,
      "confidence": "low",
      "supporting_source_count": 1,
      "median_timestamp": 1781453920,
      "recency_delta_seconds": 6451920,
      "source_posts": [...]
    }
  ]
}
```

---

## Processing Workflow

```
CI Package (12 categories × findings)
        │
        ▼
Report Generator
        │
        ├── 1. Build Executive Summary (metadata + derived stats)
        ├── 2-13. Build each section (findings sorted by frequency)
        │         - All findings preserved, no truncation
        │         - Confidence counts computed
        │         - Unique contributing post IDs tracked
        │
        └── 14. Compute Emerging Topics
                  - Load discovery package for timestamps
                  - Compute global median timestamp
                  - Flag findings with above-median recency
                  - Sort by recency delta descending
        │
        ▼
Community Intelligence Report
```

---

## Traceability Model

Every finding in the report is traceable to its source post(s):

| Field | Purpose |
|---|---|
| `finding` | The identified signal text |
| `frequency` | How many posts exhibited this signal |
| `confidence` | high (≥5), medium (2-4), low (1) |
| `supporting_source_count` | Number of unique post references |
| `source_posts[].post_id` | Reddit post ID — links back to raw post data |
| `source_posts[].url` | Direct link to the Reddit thread |
| `source_posts[].subreddit` | Community of origin |
| `source_posts[].timestamp` | UTC epoch for temporal analysis |
| `source_posts[].snippet` | Excerpt of the relevant post content |

---

## How Editorial Intelligence Will Consume This Report

Editorial Intelligence (the next stage) will:

1. Load the report JSON from `research/output/community-intelligence-reports/`
2. Read the **Executive Summary** for high-level context (posts, communities, coverage)
3. Scan each section for **high-confidence findings** (highest potential for content)
4. Cross-reference **pain points** with **competitor mentions** to identify positioning opportunities
5. Use **emerging topics** to prioritise timely content
6. Use **representative quotes** and **supporting evidence** for social proof in content

The report is designed to be consumed programmatically. Every field is structured, typed, and documented. No parsing of free-text descriptions is required.

---

## File Layout

```
research/community_intelligence/
├── __init__.py
├── processor.py                  # CI Processor
└── report_generator.py           # CI Report Generator (this component)

research/output/community-intelligence-reports/
└── {pillar}-community-intelligence-report.json

docs/implementation/
└── COMMUNITY-INTELLIGENCE-REPORT.md   # This file
```

---

## Usage

```bash
# Auto-detect: uses the first CI file found
python -m research.community_intelligence.report_generator

# Explicit CI file path
python -m research.community_intelligence.report_generator \
    research/output/community-intelligence/affiliate_marketing-community-intelligence.json
```

The generator automatically derives the Discovery Package path from the CI filename.

---

## Design Decisions

1. **All findings preserved.** No truncation or filtering. The report includes every finding from the CI Processor, sorted by frequency within each section.

2. **Emerging topics are mechanical.** Timestamp-based recency analysis uses median post timestamp vs. global median. No trend scoring, no prediction. Pure arithmetic.

3. **Report is a transformation, not analysis.** The report generator reorganises existing CI data into a cleaner structure. It does not add new data, interpret signals, or draw conclusions.

4. **Section order is fixed.** The 12 standard sections follow a logical sequence: questions → pain points → frustrations → misconceptions → tools → competitors → outcomes → mistakes → positive → negative → quotes → evidence. Emerging topics is always last.

5. **Source count tracks unique posts.** `supporting_source_count` reflects unique post IDs, not total refs (a post appearing across multiple keywords within a finding is counted once).

---

## Verification

Run the report generator against the Affiliate Marketing CI:

```bash
python -m research.community_intelligence.report_generator
```

Expected results (verified 2026-07-08):

| Section | Findings | High | Unique Posts |
|---|---|---|---|
| Most Frequent Questions | 651 | 0 | 175 |
| Most Frequent Pain Points | 25 | 11 | 83 |
| Most Frequent Frustrations | 17 | 5 | 35 |
| Most Common Misconceptions | 12 | 1 | 22 |
| Frequently Mentioned Tools | 29 | 6 | 33 |
| Frequently Mentioned Competitors | 3 | 1 | 12 |
| Desired Outcomes | 12 | 7 | 68 |
| Common Beginner Mistakes | 10 | 3 | 38 |
| Positive Signals | 16 | 4 | 45 |
| Negative Signals | 12 | 6 | 44 |
| Representative Quotes | 30 | 7 | 30 |
| Supporting Evidence | 137 | 17 | 83 |
| Emerging Topics | 437 | — | 141 |

- All 13 sections present
- No editorial recommendations, Opportunity Briefs, or article content
- Every finding traceable to source posts with post_id
- Executive summary includes all required fields

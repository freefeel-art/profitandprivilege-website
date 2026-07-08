# Community Intelligence Processor — Implementation

**Date:** 2026-07-08
**Status:** Implemented, awaiting architectural review
**Architecture freeze:** Active

---

## Purpose

The Community Intelligence (CI) Processor transforms raw Discovery Packages (from the [Discovery Runner](DISCOVERY-RUNNER.md)) into structured, traceable Community Intelligence. It identifies recurring signals across community posts — questions, pain points, frustrations, tools, competitors, and evidence — without making editorial recommendations or generating Opportunity Briefs.

This component is the **boundary** between Discovery (raw signal collection) and Editorial Intelligence (strategic analysis). CI ends when evidence has been structured. Editorial Intelligence begins after this component.

---

## Inputs

| Input | Location | Description |
|---|---|---|
| Discovery Package | `research/output/discovery/{pillar}-discovery.json` | Raw posts with `_discovery` metadata tags |

---

## Outputs

| Output | Location | Description |
|---|---|---|
| Community Intelligence | `research/output/community-intelligence/{pillar}-community-intelligence.json` | Structured findings with full traceability |

---

## Processing Workflow

```
Discovery Package (raw posts)
        │
        ▼
For each of 12 extractors:
        │
        ├── 1. Recurring Questions      (question marks, question starters)
        ├── 2. Pain Points              (struggle, difficult, can't, no money...)
        ├── 3. Frustrations             (frustrating, give up, nothing works...)
        ├── 4. Misconceptions           (myth, saturated, too late...)
        ├── 5. Frequently Mentioned Tools    (brand/pattern matching)
        ├── 6. Frequently Mentioned Competitors (brand/pattern matching)
        ├── 7. Desired Outcomes         (goal, full time, passive income...)
        ├── 8. Common Beginner Mistakes (mistake, avoid, don't do...)
        ├── 9. Positive Signals         (success, made $, game changer...)
        ├── 10. Negative Signals        (scam, waste, avoid, didn't work...)
        ├── 11. Representative Quotes   (top 30 most substantive posts)
        └── 12. Supporting Evidence     (dollar amounts, %, time periods)
                │
                ▼
        FindingAccumulator
        │
        ├── Groups by normalized key
        ├── Counts frequency
        ├── Assigns confidence (high ≥ 5, medium 2-4, low 1)
        └── Tracks source posts with id, title, subreddit, url, timestamp, snippet
                │
                ▼
Community Intelligence Package
        │
        ├── ci_metadata     (pillar, source, timestamp)
        ├── findings        (12 categories × findings)
        └── summary         (totals, coverage, unique posts)
```

---

## Evidence Model

Each finding is a structured object:

```json
{
  "finding": "Users report: struggle",
  "frequency": 7,
  "confidence": "high",
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
```

### Confidence Levels

| Level | Threshold | Meaning |
|---|---|---|
| `high` | ≥ 5 occurrences | Strong signal, recurring across multiple posts |
| `medium` | 2-4 occurrences | Notable but not dominant |
| `low` | 1 occurrence | Single mention, trackable but isolated |

### Traceability

Every finding entry is traceable to its source post(s) via:
- `post_id` — Reddit post ID (links to raw post data)
- `url` — direct Reddit URL
- `subreddit` — community of origin
- `timestamp` — UTC epoch for temporal analysis

---

## The 12 Finding Categories

| # | Category | Method | Purpose |
|---|---|---|---|
| 1 | Recurring Questions | Regex on question marks + question-starter keywords | Identifies what users are actively asking — direct content opportunities |
| 2 | Pain Points | Keyword matching (struggle, difficult, no money, etc.) | Reveals problems users need solved |
| 3 | Frustrations | Strong-emotion keyword matching (frustrating, give up, etc.) | High-intensity signals for intervention content |
| 4 | Misconceptions | Skepticism/saturation keywords (myth, too late, legit?) | Identifies beliefs that block action — content to address |
| 5 | Frequently Mentioned Tools | Brand name matching against seed list | Shows what tools the community actually uses |
| 6 | Frequently Mentioned Competitors | Brand name matching against competitor seed list | Competitive landscape awareness |
| 7 | Desired Outcomes | Goal/aspiration keywords (full time, passive income, etc.) | What users ultimately want — positioning guidance |
| 8 | Common Beginner Mistakes | Mistake/regret keywords (mistake, avoid, don't do, etc.) | Educational content opportunities |
| 9 | Positive Signals | Success story keywords (made $, game changer, etc.) | Validates what's working — social proof |
| 10 | Negative Signals | Warning/scam keywords (scam, waste, avoid, etc.) | Identifies trust barriers and objections |
| 11 | Representative Quotes | Top 30 posts by length + engagement | Verbatim community voice for Editorial Intelligence |
| 12 | Supporting Evidence | Dollar amounts, percentages, time periods | Concrete data points for credibility |

---

## File Layout

```
research/community_intelligence/
├── __init__.py          # Package marker
└── processor.py         # Main processor (12 extractors + runner)

research/output/community-intelligence/
└── {pillar}-community-intelligence.json   # CI output

docs/implementation/
└── COMMUNITY-INTELLIGENCE-PROCESSOR.md    # This file
```

---

## Usage

```bash
# Auto-detect: uses the first discovery package found
python -m research.community_intelligence.processor

# Explicit path
python -m research.community_intelligence.processor research/output/discovery/affiliate_marketing-discovery.json
```

---

## Design Decisions

1. **Pattern-based, not AI.** All extractors use keyword/regex matching. No LLM, no web search, no AI summarization. The processor organizes evidence — it does not interpret it.

2. **No cross-boundary output.** The CI Package contains exactly 12 finding categories and their source references. No editorial recommendations, no Opportunity Briefs, no article content.

3. **Conservative grouping.** Findings are grouped by normalized keywords, not semantic similarity. "Struggle" and "struggling" are grouped; "struggle" and "difficult" are separate. Semantic grouping belongs in Editorial Intelligence.

4. **Deduplication within findings.** If the same post matches multiple keywords in the same category, its post reference is added only once to that finding group.

5. **Representative Quotes are scored.** Quotes are ranked by `len(selftext) + (score * 10) + (num_comments * 5)` to surface the most substantive discussions. Confidence is quartile-based.

---

## Current Limitations

1. **Keyword lists are static.** Tools, competitors, and keyword lists may need periodic updates.
2. **No semantic grouping.** "Make money" and "earn income" are treated as separate findings.
3. **English only.** All keyword lists are English.
4. **Flat structure.** No hierarchical clustering of related findings.
5. **Single-pillar input.** Each run processes one pillar. Cross-pillar pattern analysis is not implemented.

---

## Verification

Run against the Affiliate Marketing Discovery Package:

```bash
python -m research.community_intelligence.processor \
    research/output/discovery/affiliate_marketing-discovery.json
```

Expected results (verified 2026-07-08):

| Category | Findings | High | Medium | Low |
|---|---|---|---|---|
| Recurring Questions | 651 | 0 | 32 | 619 |
| Pain Points | 25 | 11 | 9 | 5 |
| Frustrations | 17 | 5 | 3 | 9 |
| Misconceptions | 12 | 1 | 4 | 7 |
| Frequently Mentioned Tools | 29 | 6 | 9 | 14 |
| Frequently Mentioned Competitors | 3 | 1 | 1 | 1 |
| Desired Outcomes | 12 | 7 | 2 | 3 |
| Common Beginner Mistakes | 10 | 3 | 2 | 5 |
| Positive Signals | 16 | 4 | 4 | 8 |
| Negative Signals | 12 | 6 | 3 | 3 |
| Representative Quotes | 30 | 7 | 7 | 16 |
| Supporting Evidence | 137 | 17 | 35 | 85 |

- **Total findings:** 954
- **Unique posts referenced:** 177 / 178 (99.4% coverage)
- **No editorial recommendations:** ✓
- **No Opportunity Brief:** ✓
- **Every finding traceable to source posts:** ✓

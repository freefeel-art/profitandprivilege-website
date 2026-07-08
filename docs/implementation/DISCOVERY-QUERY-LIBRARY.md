# Discovery Query Library — Implementation

**Date:** 2026-07-08
**Status:** Implemented, awaiting architectural review
**Architecture freeze:** Active

---

## Purpose

The Discovery Query Library provides **Community Intelligence** with structured search inputs organized by the opportunity-first hierarchy defined in the approved [Discovery Search Strategy](/docs/architecture/DISCOVERY-SEARCH-STRATEGY.md).

Instead of formulating ad-hoc brand-name queries, Community Intelligence consumes this library to search for **user problems** — the actual struggles, frustrations, and questions people discuss online, organized by content pillar and topic cluster.

---

## Data Structure

```
Pillar
├── name          — Human-readable name
├── slug          — Machine-readable key (used for lookup)
├── description   — One-sentence pillar definition
├── brands[]      — Optional product names (solution mapping only)
└── clusters[]
    ├── name          — Cluster name
    ├── description   — What this cluster covers
    └── problems[]
        ├── description      — The user problem / pain point
        ├── search_queries[] — Natural-language Reddit search phrases
        └── communities[]    — Target subreddits for this problem
```

All types are defined as Python dataclasses in `research/discovery/models.py`.

---

## File Layout

```
research/discovery/
├── __init__.py          # Package marker
├── models.py            # Dataclasses: Pillar, Cluster, Problem
├── registry.py          # Seed data for all approved pillars
├── loader.py            # DiscoveryLoader — the CI-consumable interface
└── test_discovery.py    # Standalone test script

docs/implementation/
└── DISCOVERY-QUERY-LIBRARY.md   # This file
```

---

## How Community Intelligence Will Use It

CI imports `DiscoveryLoader` and calls:

```python
from research.discovery.loader import DiscoveryLoader

loader = DiscoveryLoader()

# Get everything for a pillar
pillar = loader.get_pillar("affiliate_marketing")

# Flat list of search queries
queries = loader.search_queries_for_pillar("affiliate_marketing")

# Unique target communities
communities = loader.communities_for_pillar("affiliate_marketing")

# Full CI-ready input structure
ci_input = loader.search_inputs_for_ci("affiliate_marketing")
```

The `search_inputs_for_ci()` method returns the exact format proposed in the Discovery Search Strategy:

```yaml
pillar: "Affiliate Marketing"
slug: "affiliate_marketing"
description: "..."
search_queries: ["query 1", "query 2", ...]
communities: ["r/Subreddit1", "r/Subreddit2", ...]
brands: ["OLSP Academy", ...]
clusters:
  - name: "Beginner Affiliate Marketing"
    description: "..."
    problems:
      - description: "..."
        search_queries: [...]
        communities: [...]
```

---

## Seeded Pillars

| Pillar | Slug | Clusters | Problems | Queries |
|---|---|---|---|---|
| Affiliate Marketing | `affiliate_marketing` | 2 | 9 | 44 |
| Lead Generation | `lead_generation` | 3 | 8 | 41 |
| Online Income | `online_income` | 3 | 10 | 38 |
| AI Tools | `ai_tools` | 3 | 10 | 39 |

**Total:** 4 pillars, 11 clusters, 37 problems, 162 search queries.

---

## How to Add a Future Pillar

1. Open `research/discovery/registry.py`
2. Create a new `Pillar(...)` block at the bottom, before the registry list
3. Add it to `PILLAR_REGISTRY`

```python
MY_NEW_PILLAR = Pillar(
    name="My New Pillar",
    slug="my_new_pillar",
    description="What this pillar covers.",
    brands=["Brand A", "Brand B"],
    clusters=[
        Cluster(
            name="Cluster One",
            description="...",
            problems=[
                Problem(
                    description="User problem description",
                    search_queries=[
                        "natural language query",
                        "another query",
                    ],
                    communities=["r/Subreddit"],
                ),
            ],
        ),
    ],
)

PILLAR_REGISTRY = [
    # ... existing pillars ...
    MY_NEW_PILLAR,
]
```

No other code changes are required. `DiscoveryLoader` automatically picks up new pillars from `PILLAR_REGISTRY`.

---

## Design Decisions

1. **Data-driven, not code-driven.** Pillars are pure data (lists of dataclass instances), not logic. Adding a pillar is a data entry task, not a programming task.

2. **Community Intelligence does not import registry.py directly.** It uses `DiscoveryLoader` or the convenience functions `load_all()` / `load_pillar()`. This gives a stable API that can be refactored later without breaking consumers.

3. **Brands are optional metadata only.** They are stored on the pillar but never used for search. They exist solely for solution mapping after signals are collected, as mandated by the Discovery Search Strategy.

4. **Queries are natural-language Reddit search phrases.** They mirror the language real people use when describing their problems — not tool names, product names, or SEO keywords.

---

## Verification

Run the test script:

```bash
python -m research.discovery.test_discovery
```

This loads all pillars, prints the full hierarchy, and validates that every data access method returns the expected structure. No external dependencies or API keys required.

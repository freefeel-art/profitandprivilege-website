# Discovery Runner — Implementation

**Date:** 2026-07-08
**Status:** Implemented, awaiting architectural review
**Architecture freeze:** Active

---

## Purpose

The Discovery Runner bridges the [Discovery Query Library](DISCOVERY-QUERY-LIBRARY.md) with Discovery Providers (currently Scrape Creators). It executes all search queries for a given content pillar, collects raw results, deduplicates, and saves a single Discovery Package for Community Intelligence to consume later.

This component **only collects data**. It performs no scoring, clustering, or editorial analysis.

---

## Workflow

```
Discovery Query Library (research/discovery/registry.py)
        ↓
Loader.load_pillar("affiliate_marketing")
        ↓
For each Cluster → Problem → Search Query:
        ↓
Provider.search(query, limit=20)
        ↓
Tag each post with source metadata
        ↓
Collect all posts → Deduplicate by Reddit post ID
        ↓
Save Discovery Package (.json)
```

---

## Inputs

| Input | Source | Description |
|---|---|---|
| Config file | `research/discovery/config.json` | Provider, pillar slug, limit |
| Pillar data | `research/discovery/registry.py` | Clusters, problems, queries, communities |
| Provider | `research/discovery/providers/scrape_creators.py` | API call to Reddit search |
| API key | `.env` → `SCRAPECREATORS_API_KEY` | Loaded automatically at query time |

---

## Output: Discovery Package

A single JSON file saved to `research/output/discovery/{pillar_slug}-discovery.json`.

### Structure

```json
{
  "discovery_metadata": {
    "pillar_name": "Affiliate Marketing",
    "pillar_slug": "affiliate_marketing",
    "provider": "scrape_creators",
    "config_used": { ... },
    "timestamp": "2026-07-08T06:31:23Z"
  },
  "queries_executed": [
    {
      "query": "...",
      "cluster": "...",
      "problem": "...",
      "success": true,
      "status_code": 200,
      "response_time_seconds": 2.34,
      "posts_found": 7,
      "error": null
    }
  ],
  "summary": {
    "total_queries": 40,
    "queries_succeeded": 40,
    "queries_failed": 0,
    "total_raw_posts": 280,
    "unique_posts": 178,
    "duplicates_removed": 102,
    "subreddits_covered": 63,
    "providers_used": ["scrape_creators"]
  },
  "subreddits": ["AffiliateMarket", "Affiliatemarketing", ...],
  "posts": [
    {
      "id": "1uljqqg",
      "title": "...",
      "subreddit": "passive_income",
      "selftext": "...",
      "score": 28,
      "num_comments": 29,
      "url": "https://...",
      "created_utc": 1783002276,
      "_discovery": {
        "pillar_slug": "affiliate_marketing",
        "pillar_name": "Affiliate Marketing",
        "cluster": "Beginner Affiliate Marketing",
        "problem": "No audience or followers to promote to",
        "matched_query": "affiliate marketing without followers",
        "provider": "scrape_creators",
        "timestamp": "2026-07-08T06:25:33Z"
      }
    }
  ]
}
```

---

## Configuration

`research/discovery/config.json`:

```json
{
  "provider": "scrape_creators",
  "pillar_slug": "affiliate_marketing",
  "limit": 20,
  "output_dir": "research/output/discovery"
}
```

| Field | Description |
|---|---|
| `provider` | Provider module name. Currently only `scrape_creators`. |
| `pillar_slug` | Pillar slug from the Discovery Query Library. |
| `limit` | Approximate max posts requested per query (passed to the API). |
| `output_dir` | Relative path for output files. |

---

## Usage

```bash
# Default (reads config.json, pillar from config)
python -m research.discovery.runner

# Custom config
python -m research.discovery.runner path/to/config.json

# Override pillar via CLI
python -m research.discovery.runner config.json lead_generation
```

---

## Current Limitations

1. **Single provider only.** Only Scrape Creators is implemented. Adding providers requires a new module in `research/discovery/providers/`.
2. **Synchronous execution.** Queries run sequentially. For 40 queries at ~3s each, a full cycle takes ~2 minutes. A future version could parallelise.
3. **No rate limiting.** Scrape Creators has generous limits (996+ credits remaining in tests), but no built-in throttling.
4. **No incremental updates.** Every run re-fetches all queries. No cache or differential update layer.
5. **Posts are raw.** No sanitisation or normalisation of post content (HTML in selftext, etc.). The raw API response is preserved.

---

## Verification

Run the Affiliate Marketing discovery cycle:

```bash
python -m research.discovery.runner research/discovery/config.json
```

Expected output (verified 2026-07-08):
- 40/40 queries succeeded
- ~178 unique posts from ~280 raw (duplicates removed)
- 63 unique subreddits covered
- Output saved to `research/output/discovery/affiliate_marketing-discovery.json`
- Every post has a `_discovery` tag
- No analysis performed

# Scrape Creators — Proof of Concept Report

**Date:** 2026-07-08
**Status:** Experimental — no production changes
**Architecture freeze:** Active

---

## Overview

A minimal Proof of Concept to validate Scrape Creators as an optional Discovery provider for Community Intelligence. The PoC implemented a single endpoint (`GET /v1/reddit/search`) and ran three keyword queries with raw JSON output only — no summarization, scoring, or editorial analysis.

---

## Implementation

**Provider location:** `research/providers/scrape-creators/query.py`

**Output location:** `research/output/scrape-creators-test-{slug}.json`

**Endpoint tested:** `GET https://api.scrapecreators.com/v1/reddit/search`

**Parameters:**
- `query`: keyword
- `sort`: relevance
- `timeframe`: all
- `trim`: true

**Authentication:** `x-api-key` header, read from `.env` (`SCRAPECREATORS_API_KEY`)

---

## Test Results

### Test 1 — "OLSP Academy"

| Metric | Value |
|---|---|
| **Request succeeded?** | Yes (HTTP 200) |
| **Response time** | 6.92s |
| **Response size** | 12,697 bytes |
| **Posts returned** | 7 |
| **Comments returned** | 0 |
| **Media returned** | 0 |
| **Credits consumed** | 1 |
| **Subreddits** | Affiliate, Affiliatemarketing, Marikina, NEETard, AskLE, cybersecurity |

**Top results:**
1. `r/Affiliate` — "Is there anything like OLSP Academy - but better?" (score:1)
2. `r/Affiliatemarketing` — same post cross-posted (score:0)
3. `r/Marikina` — "everything about olopsc (its terrible)" (score:51) — **false positive** (Philippine school)
4. `r/NEETard` — "Oslsp" (score:1) — **false positive** (typo match)
5. `r/AskLE` — "OSHP Academy" (score:4) — **false positive** (police academy)

**Quality issues:** 3 of 7 results are false positives (keyword overlap with unrelated acronyms: OLOPSC, OSLSP, OSHP). The 2 relevant posts are cross-posts of the same question.

**Body text:** All 7 posts include selftext content.

---

### Test 2 — "Affiliate Marketing"

| Metric | Value |
|---|---|
| **Request succeeded?** | Yes (HTTP 200) |
| **Response time** | 11.17s |
| **Response size** | 13,655 bytes |
| **Posts returned** | 6 |
| **Comments returned** | 0 |
| **Media returned** | 0 |
| **Credits consumed** | 1 |
| **Subreddits** | passive_income, AffiliateMarket, answers, Affiliatemarketing |

**Top results:**
1. `r/passive_income` — "I made $1.5k in two weeks with affiliate content!!" (score:28)
2. `r/AffiliateMarket` — "Is affiliate marketing still worth starting in 2026?" (score:29)
3. `r/passive_income` — "Now I am making 100-200$/month doing affiliate marketing" (score:6)
4. `r/answers` — "New to affiliate marketing, what's the smartest way to start?" (score:10)
5. `r/Affiliatemarketing` — "What are the best (free) websites to find affiliate marketing opportunities?" (score:18)

**Quality issues:** None. All 6 results are on-topic. Good subreddit diversity (4 different communities).

---

### Test 3 — "Lead Generation"

| Metric | Value |
|---|---|
| **Request succeeded?** | Yes (HTTP 200) |
| **Response time** | 9.36s |
| **Response size** | 16,187 bytes |
| **Posts returned** | 7 |
| **Comments returned** | 0 |
| **Media returned** | 0 |
| **Credits consumed** | 1 |
| **Subreddits** | LeadGeneration, DigitalMarketing, AskMarketing, microsaas, LeadGenMarketplace, ClaudeAI, WholesaleRealestate |

**Top results:**
1. `r/LeadGeneration` — "Is Any Lead Generation Method Still Working in 2026?" (score:64)
2. `r/DigitalMarketing` — "What does everyone here use for lead generation?" (score:10)
3. `r/AskMarketing` — "Best AI Tool for B2B Lead Generation in 2026?" (score:18)
4. `r/microsaas` — "best lead generation tools for small businesses on a budget?" (score:6)
5. `r/LeadGenMarketplace` — "Hiring for Lead Generation" (score:9)

**Quality issues:** None. All 7 results are on-topic. Best subreddit diversity (7 different communities).

---

## Rate Limits

| Observation | Value |
|---|---|
| Credits consumed per request | 1 credit |
| Starting balance | 1,000 (free tier) |
| Credits remaining after 3 tests | 995 |
| Effective cost | 3 credits for 3 requests |
| No rate-limit errors encountered | Yes |
| No 429 errors | Yes |

The API returns `credits_remaining` in every response header and body. No request throttling or IP-based rate limiting was observed during testing.

---

## Response Quality Assessment

| Criterion | Assessment |
|---|---|
| **Data freshness** | Good — posts appear recent (timestamps in JSON) |
| **Subreddit diversity** | Excellent — each query returned 4–7 different subreddits |
| **Post body availability** | All posts include `selftext` — full discussion content available |
| **Engagement metrics** | Score (votes), comment count, subreddit subscriber count available |
| **False positive rate** | Low for generic terms (0/6, 0/7); moderate for branded/niche terms (3/7 for OLSP Academy) |
| **Comment data** | Not returned by the search endpoint with `trim=true` |
| **Pagination** | No cursor returned (response limited by default) |

---

## Platforms Returned

This PoC tested only the **Reddit** search endpoint. Scrape Creators also offers endpoints for:

- X/Twitter (profiles, tweets, communities)
- YouTube (search, comments, community posts)
- TikTok (search by keyword, comments, trending)
- Facebook (group posts, comments)
- LinkedIn (search posts, company posts)
- GitHub (trending repos)
- Plus 20+ more platforms

These were not tested in this PoC but are documented in the companion analysis at `docs/architecture/SCRAPE-CREATORS-DISCOVERY-ANALYSIS.md`.

---

## Errors Encountered

| Error | Count | Resolution |
|---|---|---|
| None | — | All 3 requests returned HTTP 200 |

No authentication errors, rate-limit errors, timeout errors, or malformed response errors were encountered.

---

## Overall Assessment

| Criterion | Verdict |
|---|---|
| **Can it provide Discovery signals?** | Yes — returns structured Reddit posts with engagement metrics |
| **Is it reliable enough?** | Yes — 3/3 requests succeeded within 7–12 seconds |
| **Is it cheap enough?** | Yes — 1 credit per request; free tier covers ~1,000 requests |
| **Does it enrich our current Reddit access?** | Yes — structured JSON with scores, timestamps, subreddit metadata is better than raw redditwarp scraping |
| **Is it a replacement for redditwarp?** | No — should be supplemental. redditwarp gives more control; SC gives convenience |
| **Should it be integrated?** | Tentative yes — as an **optional** Signal Layer provider within CI |

### What works well

- Structured JSON with engagement metrics (score, comment count, subreddit metadata)
- Broad subreddit coverage (4–7 communities per query)
- All posts include full body text (selftext)
- 1 credit per request — sustainable at our production volume
- No authentication friction (single API key, simple header)

### What needs improvement

- **No comments returned** — the `trim=true` parameter excludes the `comments` array. Without `trim=true`, the response includes comments from matching threads, which is valuable for mining recurring questions and problems.
- **False positives on short/ambiguous keywords** — "OLSP Academy" matched "OLOPSC" (school), "OSLSP" (typo), "OSHP Academy" (police). The `subreddit` field can be used to filter by known relevant communities.
- **No pagination cursor returned** — limited result set per query. For a systematic sweep, cursor-based pagination is needed.
- **Single-platform focus** — the PoC tested Reddit only. The real value comes from cross-platform queries (Reddit + X + YouTube + TikTok).
- **Slow response times** — 7–12 seconds per request. Acceptable for batch discovery, not for real-time use.

---

## Raw Output Files

- `research/output/scrape-creators-test-olsp-academy.json`
- `research/output/scrape-creators-test-affiliate-marketing.json`
- `research/output/scrape-creators-test-lead-generation.json`

Each file contains:
- `test`: metadata (keyword, endpoint, timing, status)
- `raw_response`: complete API response (posts array, credits remaining)

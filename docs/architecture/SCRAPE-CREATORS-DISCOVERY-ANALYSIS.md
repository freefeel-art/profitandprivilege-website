# Scrape Creators — Discovery Engine Integration Analysis

**Date:** 2026-07-08
**Status:** Architecture review only — no implementation approved
**Architecture Freeze:** Active

---

## Executive Summary

Scrape Creators is a third-party REST API that provides structured access to public data from 27+ social media platforms via 110+ endpoints. For the OLSP AI Editorial Operating System, its primary value is accelerating the **Community Intelligence** stage by providing API-based access to platforms that are currently either manually monitored, planned but not implemented, or completely absent from our data sources.

Scrape Creators should be treated as **an optional Discovery signal provider** — not a replacement for any existing source. It complements our current Reddit-first approach by adding structured access to X/Twitter, YouTube, TikTok, LinkedIn, Facebook, and other platforms with a single API integration.

The smallest architectural integration adds Scrape Creators as a **configurable data source** within the Community Intelligence stage's "Question Mining" and "Problem Mining" steps. No new pipeline stages, no architectural changes, and no disruption to existing discovery workflows.

Key finding: Scrape Creators' **MCP server** (`https://api.scrapecreators.com/mcp`) enables direct tool-based access from AI agents without building any integration code — this is the lowest-friction integration path available.

---

## API Capabilities

### Platforms and Endpoints

Scrape Creators exposes 110+ REST endpoints across 27+ platforms. The following platforms are relevant to our Discovery Engine, ranked by usefulness:

| Platform | Available Endpoints | Discovery Value | Current Status in Our CI |
|---|---|---|---|
| **Reddit** | Subreddit Details, Subreddit Posts, Subreddit Search, Post Comments, Post Transcript, Search | **High** — structured post/comment data with engagement metrics | Current (via redditwarp/manual) |
| **X/Twitter** | Profile, User Tweets, Tweet Details, Community, Community Tweets | **High** — real-time discussion monitoring | Planned in CI spec |
| **YouTube** | Channel Details, Channel Videos, Video Comments, Community Posts, Search, Transcript | **High** — comment mining for audience questions | Future in CI spec |
| **TikTok** | Search by Keyword, Search by Hashtag, Comments, Trending Feed, Popular Creators | **Medium-High** — emerging discussion trends | Not in current plan |
| **Facebook** | Group Posts, Profile Posts, Comments, Comment Replies | **Medium-High** — group discussions | Planned in CI spec |
| **LinkedIn** | Search Posts, Company Posts, Company Page | **Medium** — B2B/professional discussions | Not in current plan |
| **GitHub** | Trending Repositories, Trending Developers, User Activity | **Low** — not a primary discovery source for our niche | Not in current plan |
| **Google Search** | Search | **Low** — we already have web search | Already covered |
| **Threads** | Search by Keyword, Profile, Posts | **Low-Medium** — emerging but low signal for our niche | Not in current plan |
| **Bluesky** | Profile, Posts | **Low** — very low signal for affiliate marketing | Not in current plan |
| **Pinterest** | Search, Pin, User Boards | **Low** — visual discovery, low text signal | Not in current plan |

### Pricing Model

- **Credit-based:** 1 request = 1 credit (most endpoints)
- **Free tier:** 100 credits on signup (no credit card)
- **Solo Dev:** $10 (credit pack)
- **Freelance:** $47 (credit pack)
- **Business:** $497 (credit pack)
- Credits never expire
- Per the transcript: the "Last 30 Days" skill used Scrape Creators with the free 1,000-credit allocation (appears to be per-user, may vary)

### Integration Methods

Scrape Creators offers multiple integration paths, ranked by architectural fit:

1. **REST API** — standard `GET` requests with `x-api-key` header. Returns JSON. Most flexible.
2. **MCP Server** — `https://api.scrapecreators.com/mcp`. AI agents can call it as a tool directly via Model Context Protocol. No integration code needed.
3. **Agent Skill** — `npx skills add ScrapeCreators/social-media-research-skills`. Pre-built skill that teaches an AI agent how to use the API effectively.
4. **CLI** — `scrapecreators` CLI for terminal-based usage.
5. **Apify Actor** — available on Apify marketplace.

---

## Mapping to Discovery Engine

### Where Scrape Creators Fits in the Pipeline

Scrape Creators maps to **Community Intelligence (Stage 1)** — specifically the "Question Mining" and "Problem Mining" discovery steps. It does not map to any other stage.

Current CI data source status (from COMMUNITY-INTELLIGENCE-SPEC.md):

| Source | Current Status | Scrape Creators Coverage | Impact |
|---|---|---|---|
| Reddit | Current (redditwarp) | Full (6 endpoints) | Enrichment — structured API vs. library-based |
| Quora | Current | Not covered | No impact |
| Forums | Current | Not covered | No impact |
| Product communities | Current | Not covered | No impact |
| Facebook Groups | Planned | Full (Group Posts, Comments, Replies) | **Accelerates** — enables now vs. planned |
| YouTube comments | Future | Full (Comments, Replies, Community Posts) | **Accelerates** — enables now vs. future |
| X (Twitter) | Planned | Full (Tweets, Communities) | **Accelerates** — enables now vs. planned |
| LinkedIn | Not planned | Full (Search Posts, Company Posts) | **New capability** |
| TikTok | Not planned | Full (Search, Comments, Trending) | **New capability** |
| Discord | Future | Not covered | No impact |

### Endpoint-to-Discovery-Signal Mapping

| Discovery Signal (from CI spec §5.1) | Scrape Creators Endpoint(s) | Value |
|---|---|---|
| Recurring questions | Reddit Search, Reddit Subreddit Search, YouTube Comments, Twitter Community Tweets | Structured text with frequency analysis potential |
| Recurring frustrations | Reddit Post Comments, YouTube Video Comments, Facebook Group Posts | Comment bodies contain emotional language |
| Recurring misconceptions | Reddit Search (with topic queries), Twitter Tweet Details | Can search for specific myth patterns |
| Recurring buying objections | Reddit Search (affiliate/marketing subreddits), LinkedIn Search Posts | Professional and consumer objections |
| Recurring comparisons | Reddit Search ("vs", "or", "alternative"), YouTube Comments | Comparison language in discussions |
| Emerging discussions | TikTok Trending Feed, YouTube Trending Shorts, Reddit Subreddit Posts (new sort) | Real-time trend detection |
| Unsolved problems | Reddit Search (questions with few replies), YouTube Comments | Low-engagement questions = unmet needs |
| Self-reported failures | Reddit Search ("I tried", "didn't work"), Facebook Group Posts | First-person failure narratives |
| Conflicting advice | Reddit Search ("some say", "others say"), Twitter Communities | Opposing viewpoints |

---

## Potential Benefits

### 1. Accelerate Planned Sources

Three sources currently documented as "Planned" (Facebook Groups, X/Twitter) or "Future" (YouTube comments) in our CI spec could be activated immediately via Scrape Creators:
- **Facebook Groups** — `GET /v1/facebook/group/posts` gives structured access to group discussions
- **X/Twitter** — `GET /v1/twitter/community/tweets` surfaces discussion in topic-based communities
- **YouTube** — `GET /v1/youtube/video/comments` mines comment sections for audience questions

No custom scrapers to build. No API approval processes to navigate. One API key covers all three.

### 2. Structured Data Over Manual Collection

Our current Reddit mining uses redditwarp (Python library) via the supplement-reddit-research skill. Scrape Creators returns structured JSON with engagement metrics (votes, comment counts, subreddit metadata, user data) that our current approach requires additional processing to extract.

For X/Twitter and YouTube, we currently have no structured data source at all — these are monitored manually or not at all.

### 3. Cross-Platform Recency Scanning

The "Last 30 Days" pattern from the transcript — querying a topic across Reddit, X, YouTube, and TikTok simultaneously — is feasible with a single Scrape Creators integration. This directly addresses the "recency" pillar of Net Information Gain that the previous architectural review identified as a priority improvement.

### 4. Low Integration Friction

Scrape Creators offers an **MCP server** that works with Claude, Cursor, VS Code Copilot, and any MCP-compatible client. This means the Community Intelligence agent could call Scrape Creators as a tool without any Python code, API client library, or custom integration. The agent skill (`npx skills add ScrapeCreators/social-media-research-skills`) further reduces friction by teaching the agent which endpoints to use and how.

### 5. TikTok and LinkedIn Coverage

TikTok and LinkedIn are not currently in our CI source plan at all. TikTok's trending feed and keyword search surfaces emerging topics that our affiliate marketing and AI tools niches would benefit from. LinkedIn posts search surfaces professional B2B discussions relevant to our OLSP audience.

---

## Risks

| Risk | Severity | Likelihood | Mitigation |
|---|---|---|---|
| **Vendor lock-in** | Medium | Low | Never make Scrape Creators the sole provider for any source. Always maintain independent alternatives (redditwarp for Reddit, web search for cross-platform). |
| **API downtime** | Medium | Medium | Cache results. Treat SC as an enrichment layer — if it's down, existing discovery methods continue. |
| **Credit costs at scale** | Low-Medium | Low | Solo Dev ($10) or Freelance ($47) covers our current production volume (we are not high-frequency). Free 100 credits covers initial evaluation. |
| **Data quality variance** | Low | Low | SC is an unofficial API — data is best-effort. All findings must still pass our CI verification process (Finding → Verified state). |
| **Terms of service violation** | Low | Low | SC only accesses public data (same as what a browser sees). No authentication bypass. Our usage (community discussion mining) is standard. |
| **Scope creep** | Low | Medium | SC makes it easy to add sources. Must enforce the Editorial Decision gate — new sources enrich existing topics, they do not create new topics. |

---

## Recommended Integration

### Proposed Role: Optional Discovery Signal Provider

Scrape Creators should be treated as:

> **An optional, configurable data source within the Community Intelligence stage — one signal among many, not a primary or sole provider.**

This means:
- No existing source is replaced
- No existing discovery workflow is modified
- Scrape Creators provides additional signal that CI agents *may* consult
- CI reports must clearly label which findings came from which source

### Smallest Architectural Integration

The integration touches exactly one place in the existing architecture:

```
Community Intelligence (Stage 1)
  ├── Question Mining
  │     ├── Current: Reddit (redditwarp), Quora, Forums
  │     └── Optional: Scrape Creators (Reddit, X, YouTube, LinkedIn, TikTok)
  ├── Problem Mining
  │     ├── Current: Same sources as Question Mining
  │     └── Optional: Scrape Creators (same)
  └── Emerging Discussions
        ├── Current: Manual / periodic
        └── Optional: Scrape Creators (TikTok Trending, YouTube Trending)
```

**No changes to:**
- AI-EDITORIAL-OPERATING-SYSTEM.md (stage definitions unchanged)
- EDITORIAL-OBJECT-MODEL.md (no new objects)
- AGENT-CONTRACT.md (stage isolation unchanged)
- PIPELINE-ARCHITECTURE.md (no new pipeline tracks)
- WHY.md (philosophy unchanged)
- Any agent specification document

### Integration Methods (Recommended Order)

1. **MCP Server** (lowest friction) — Add Scrape Creators as an MCP tool in the project's OpenCode configuration. CI agents can call it directly without any code.

2. **Agent Skill** (next) — Install the Scrape Creators agent skill to teach CI agents best practices for endpoint selection.

3. **REST API** (if MCP is insufficient) — Direct HTTP calls from a lightweight wrapper if we need more control over request batching or caching.

### Which Endpoints to Use First

Priority order for initial integration (highest value, lowest effort):

| Priority | Endpoint | CI Signal | Why First |
|---|---|---|---|
| 1 | `GET /v1/reddit/search` | Recurring questions, problems | Accelerates existing Reddit mining with structured data |
| 2 | `GET /v1/twitter/community/tweets` | Emerging discussions | Activates planned X source immediately |
| 3 | `GET /v1/youtube/video/comments` | Audience questions, objections | Activates future YouTube source immediately |
| 4 | `GET /v1/facebook/group/posts` | Niche community discussions | Activates planned Facebook source |
| 5 | `GET /v1/tiktok/search/keyword` | Emerging trends | New source — TikTok trending topics |

### Sources That Should Remain Independent

The following sources should never depend on Scrape Creators:

| Source | Reason |
|---|---|
| **Reddit (current redditwarp method)** | Our primary discovery source. Must maintain independent access. SC should *supplement*, not replace. |
| **Quora** | Not covered by SC. Must remain independent or find alternative. |
| **Niche forums** | Not covered by SC. These are manually curated. |
| **Web search (Google, Bing)** | Our general research tool. SC's Google Search endpoint exists but our existing web search is sufficient. |
| **Community Intelligence Report (CI → EI handoff)** | The CI Report is an architectural object. Its format, structure, and required deliverables are defined in the spec and do not change regardless of data sources. |

---

## Final Recommendation

**Adopt Scrape Creators as an optional Discovery signal layer within Community Intelligence.**

### What it does for the system

1. Accelerates three "Planned/Future" sources (Facebook Groups, X/Twitter, YouTube comments) to active status
2. Adds two new sources (TikTok, LinkedIn) with no additional integration work
3. Provides structured JSON data with engagement metrics that enriches our existing text-based discovery
4. Enables the cross-platform recency scanning pattern from the "Last 30 Days" transcript concept
5. Integrates via MCP with zero code changes to the repository

### What it does NOT do

- Does not replace any existing Discovery source
- Does not change the architecture
- Does not add new pipeline stages or gates
- Does not create new canonical objects
- Does not change the Editorial Object Model
- Does not require changes to any spec document
- Does not bypass the problems-before-keywords philosophy (topics still originate from CI, not from SC)

### Architectural Classification

**Type:** Implementation improvement — specifically, a data source addition to Community Intelligence

**Scope:** Community Intelligence stage only — no cross-stage impact

**Architecture freeze impact:** None — no spec documents require modification

### Next Steps (if approved)

1. Register for free Scrape Creators account (100 free credits)
2. Add MCP server to project configuration (one-line config)
3. Verify CI agent can call Scrape Creators endpoints as tools
4. Update CI agent prompt to include Scrape Creators as an optional data source
5. Test on one topic sweep (e.g., cross-platform "affiliate marketing" query)
6. Evaluate credit consumption and decide on paid plan if needed

---

*End of analysis. Awaiting approval before any implementation.*

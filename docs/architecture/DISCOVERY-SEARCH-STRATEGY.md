# Discovery Search Strategy — From Brand-First to Opportunity-First

**Date:** 2026-07-08
**Status:** Strategy document only — no implementation
**Architecture freeze:** Active

---

## Executive Summary

The Scrape Creators PoC (Test 1: "OLSP Academy") revealed a fundamental architectural issue: **brand-first search produces narrow, noisy results** — 7 posts returned, 3 of which were false positives (unrelated acronym matches). In contrast, **problem-first search** (Test 2: "Affiliate Marketing", Test 3: "Lead Generation") returned high-quality, on-topic results across diverse communities.

This document proposes a shift in how the Discovery Engine formulates search queries. Instead of starting from product or brand names, discovery should begin from **content pillars → topic clusters → user problems → community discussions → signals**. Product/brand names enter only at the end of the flow, as potential solutions to problems already validated by community signal.

This is a **search strategy change only** — not an architectural change. Community Intelligence retains its existing pipeline position and deliverables. The change is in *how* signals are discovered, not *what* happens to them after discovery.

---

## Why Brand-First Discovery Fails

### Limited Surface Area

A brand name is a single keyword. Searching for "OLSP Academy" queries only discussions that mention that exact phrase. Most community discussions about the *problem* that OLSP Academy solves do not mention the brand by name. They discuss:

- "How do I start affiliate marketing with no audience?"
- "Is there a training program that actually works?"
- "I tried solo ads and made nothing — what am I doing wrong?"
- "What's the best way to generate leads as a beginner?"

These discussions never mention "OLSP Academy", yet they represent the exact editorial opportunities our system exists to discover.

### High False Positive Rate

Brand names are often short strings that overlap with unrelated acronyms:

| Searched term | False positive matches |
|---|---|
| "OLSP Academy" | OLOPSC (Philippine school), OSLSP (typo), OSHP Academy (police) |
| "LeadsMiner" | Low (unique name, but low volume — 0 meaningful results) |
| "MegaLink" | Philippine telecom company, unrelated software products |

### Zero Discovery for New Opportunities

Brand-first search can only find discussions about *existing* brands. It cannot discover:

- Emerging problems that no product yet addresses
- Competitor weaknesses that create positioning opportunities
- Adjacent problems the brand could expand into
- Underserved audience segments

### Violates the Editorial Philosophy

From `docs/WHY.md`:

> *"A keyword tool tells you how many people searched for a phrase. It does not tell you why they searched."*

Brand-first search is keyword-first search with a brand filter. It finds *mentions* but reveals *nothing* about the underlying human problem. This directly contradicts the problems-before-keywords philosophy.

---

## Opportunity-First Discovery

### The Correct Flow

```
Content Pillar
    ↓
Topic Cluster
    ↓
User Problems / Pain Points / Questions
    ↓
Community Discussions (where these problems surface)
    ↓
Signals (extracted recurring questions, frustrations, objections)
    ↓
Opportunity Brief
    ↓
Possible Products / Solutions (including brand names, if relevant)
```

Brand names enter only at the final step — after the problem is validated and the opportunity is defined. At that point, the question becomes: "Does OLSP Academy solve this problem?" not "What does the community say about OLSP Academy?"

### What This Changes

| Aspect | Brand-First | Opportunity-First |
|---|---|---|
| Starting point | Product name | User problem |
| Search queries | "OLSP Academy review" | "How to start affiliate marketing with no money" |
| Signal quality | Narrow, noisy | Broad, relevant |
| Discovery potential | Existing products only | New problems and gaps |
| Alignment with WHY.md | Violates | Enforces |
| Use for Scrape Creators | Limited (no results) | Rich (broad results) |

---

## Discovery Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTENT PILLAR                           │
│  The strategic domain we publish in                         │
│  Examples: Online Income, Lead Generation, AI Tools         │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     TOPIC CLUSTER                           │
│  A specific sub-domain within the pillar                    │
│  Examples: Beginner affiliate marketing, B2B lead gen       │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      USER PROBLEMS                          │
│  What people actually struggle with                         │
│  Examples: "I have no audience", "I can't generate leads"   │
└─────────────┬──────────────────────┬────────────────────────┘
              │                      │
              ▼                      ▼
┌─────────────────────────┐  ┌─────────────────────────┐
│    COMMUNITY SIGNALS    │  │    SEARCH SIGNALS        │
│  Reddit threads         │  │  Search phrases mined   │
│  YouTube comments       │  │  from keyword research   │
│  X/Twitter discussions  │  │  SERP gaps               │
│  Facebook groups        │  │  PAA questions           │
└─────────────┬───────────┘  └────────────┬────────────┘
              │                           │
              └──────────────┬────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                      SIGNALS                                │
│  Recurring questions, frustrations, misconceptions,         │
│  objections, comparisons, self-reported failures            │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   OPPORTUNITY BRIEF                         │
│  Validated editorial opportunity with working title,        │
│  primary question, target audience, recommended format      │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              POSSIBLE PRODUCTS / SOLUTIONS                  │
│  Brand names enter here — as answers to validated problems  │
└─────────────────────────────────────────────────────────────┘
```

---

## Search Strategy

### Design Principle

Search queries should mirror the language real people use when describing their problems — not the language products use in their marketing.

### Query Patterns by Intent

| Intent | Query pattern | Example |
|---|---|---|
| Beginner seeking guidance | "how to [verb] for beginners" | "how to start affiliate marketing for beginners" |
| Troubleshooting failure | "I tried X and it didn't work" | "I tried email marketing and no one opened" |
| Seeking comparison | "X vs Y", "best X for Y" | "solo ads vs Facebook ads for affiliate marketing" |
| Verification/trust | "Is X legitimate?", "Does X actually work?" | "Is affiliate marketing still profitable in 2026?" |
| Resource constraints | "X with no money", "X free" | "lead generation with no budget" |
| Emotional signal | "X frustrated", "X overwhelmed" | "affiliate marketing overwhelmed where to start" |

### Community Search Phrases

For Reddit (the primary discovery source), search queries should be formulated as natural-language questions:

| Topic cluster | Reddit search query |
|---|---|
| Beginner affiliate marketing | "how to start affiliate marketing no experience" |
| Beginner affiliate marketing | "affiliate marketing without website" |
| Beginner affiliate marketing | "affiliate marketing no money to start" |
| Beginner affiliate marketing | "affiliate marketing beginner mistakes" |
| Lead generation | "how to generate leads for free" |
| Lead generation | "best lead generation tools 2026" |
| Lead generation | "lead generation no budget" |
| Lead generation | "B2B lead generation strategies" |
| AI tools | "best AI writing tools for content" |
| AI tools | "AI video generation review" |
| Traffic | "how to drive traffic affiliate links" |
| Traffic | "solo ads review scam" |
| Traffic | "email list building no website" |
| Online income | "make money online realistic 2026" |
| Online income | "side hustle from home no experience" |
| Online income | "how much can I earn online 2026" |

---

## Community Discovery Strategy

### Primary Discovery Communities (by pillar)

**Pillar 1 — OLSP Ecosystem**
- `r/Affiliatemarketing` (direct)
- `r/juststart` (adjacent — beginner affiliate journey)
- `r/passive_income` (adjacent)
- `r/Affiliate` (direct)
- `r/sidehustle` (adjacent)

**Pillar 2 — Affiliate Traffic & List Building**
- `r/Emailmarketing` (direct)
- `r/soloads` (direct — but low activity)
- `r/SEO` (adjacent — traffic)
- `r/juststart` (direct — traffic strategies)
- `r/Blogging` (adjacent)

**Pillar 3 — Lead Generation**
- `r/LeadGeneration` (direct)
- `r/DigitalMarketing` (direct)
- `r/AskMarketing` (direct)
- `r/sales` (adjacent — B2B)
- `r/microsaas` (adjacent — tools)
- `r/Entrepreneur` (adjacent)

**Pillar 4 — Online Income for Beginners**
- `r/beermoney` (direct)
- `r/sidehustle` (direct)
- `r/passive_income` (direct)
- `r/Affiliatemarketing` (adjacent)
- `r/workonline` (direct)
- `r/freelance` (adjacent)
- `r/Entrepreneur` (peripheral)

**Pillar 5 — AI Tools**
- `r/ArtificialIntelligence` (direct)
- `r/ChatGPT` (adjacent)
- `r/SaaS` (adjacent)
- `r/technology` (peripheral)
- `r/SEO` (adjacent — AI writing tools)

### Platform Strategy

| Platform | Role in Discovery | Scrape Creators endpoint |
|---|---|---|
| **Reddit** | Primary — recurring questions, objections, self-reported failures | `GET /v1/reddit/search` |
| **YouTube** | Secondary — comment mining for audience pain points | `GET /v1/youtube/video/comments` |
| **X/Twitter** | Secondary — real-time discussion and emerging trends | `GET /v1/twitter/community/tweets` |
| **Facebook Groups** | Tertiary — niche communities (planned) | `GET /v1/facebook/group/posts` |
| **TikTok** | Tertiary — emerging trend detection | `GET /v1/tiktok/search/keyword` |
| **LinkedIn** | Tertiary — B2B/professional pain points | `GET /v1/linkedin/search/posts` |

---

## Recommended Search Inputs

### For Community Intelligence Agent

The CI agent should receive search inputs organized by **topic cluster**, not by brand. The inputs replace product names with problem-oriented search queries.

**Current input format (brand-first):**
```yaml
target_niche: "OLSP Academy"
community_list: ["r/Affiliatemarketing"]
```

**Proposed input format (opportunity-first):**
```yaml
pillar: "Online Income for Beginners"
cluster: "Beginner Affiliate Marketing"
search_queries:
  - "how to start affiliate marketing with no experience"
  - "affiliate marketing without money"
  - "affiliate marketing beginner overwhelmed"
  - "best affiliate training for beginners 2026"
  - "affiliate marketing mistakes beginners make"
community_list:
  - "r/Affiliatemarketing"
  - "r/juststart"
  - "r/passive_income"
  - "r/sidehustle"
  - "r/workonline"
brands: ["OLSP Academy"]  # used only for solution mapping, not for search
```

### Brand-in-Context Only

Brands remain useful for exactly two contexts:

1. **Solution mapping** — after an opportunity is identified, the CI agent asks: "Does our product suite solve this problem?"
2. **Competitive intelligence** — when explicitly researching competitor positioning, brand search is valid. But this is a separate task from opportunity discovery.

---

## Example Search Trees

### Example 1: Lead Generation Pillar

```
PILLAR: Lead Generation
    │
    ├── CLUSTER: Lead Generation for Beginners
    │       │
    │       ├── PROBLEM: "I don't know how to start generating leads"
    │       │       └── SEARCH: "how to generate leads for beginners", "lead generation step by step"
    │       │
    │       ├── PROBLEM: "I have no budget for tools"
    │       │       └── SEARCH: "free lead generation methods", "lead generation no money"
    │       │
    │       └── PROBLEM: "I tried lead generation and got no results"
    │               └── SEARCH: "lead generation not working", "why is my lead generation failing"
    │
    ├── CLUSTER: B2B Lead Generation
    │       │
    │       ├── PROBLEM: "I can't reach decision-makers"
    │       │       └── SEARCH: "B2B lead generation strategies 2026", "how to reach decision makers"
    │       │
    │       ├── PROBLEM: "LinkedIn outreach feels spammy"
    │       │       └── SEARCH: "LinkedIn lead generation without being spammy"
    │       │
    │       └── PROBLEM: "Cold email open rates are dropping"
    │               └── SEARCH: "cold email not working 2026", "cold email alternatives"
    │
    └── CLUSTER: Lead Generation Tools
            │
            ├── PROBLEM: "Which lead gen tool actually works?"
            │       └── SEARCH: "best lead generation tools 2026", "lead generation tool review"
            │
            ├── PROBLEM: "Too many tools, can't choose"
            │       └── SEARCH: "lead generation software comparison", "lead gen tool vs tool"
            │
            └── PROBLEM: "Tools are too expensive"
                    └── SEARCH: "affordable lead generation tools", "free lead generation software"
```

### Example 2: AI Tools Pillar

```
PILLAR: AI Tools
    │
    ├── CLUSTER: AI Writing
    │       │
    │       ├── PROBLEM: "AI content gets penalized by Google"
    │       │       └── SEARCH: "does Google penalize AI content", "AI writing SEO safe"
    │       │
    │       ├── PROBLEM: "AI writing sounds robotic"
    │       │       └── SEARCH: "best AI writing tool human quality", "make AI content sound human"
    │       │
    │       └── PROBLEM: "Which AI writer is best for affiliate marketing?"
    │               └── SEARCH: "best AI writing tool for affiliate marketing", "AI writing for SEO content"
    │
    ├── CLUSTER: AI Video
    │       │
    │       ├── PROBLEM: "I don't want to appear on camera"
    │       │       └── SEARCH: "AI avatar video creation", "fakeless video for marketing"
    │       │
    │       ├── PROBLEM: "Video production is too expensive"
    │       │       └── SEARCH: "cheap AI video generation", "affordable video creation AI"
    │       │
    │       └── PROBLEM: "AI avatars look fake"
    │               └── SEARCH: "best realistic AI avatar", "AI video generation review 2026"
    │
    └── CLUSTER: AI SEO & Research
            │
            ├── PROBLEM: "SEO tools are too expensive for beginners"
            │       └── SEARCH: "affordable SEO tools 2026", "best cheap SEO tools"
            │
            ├── PROBLEM: "I can't rank my content anymore"
            │       └── SEARCH: "SEO not working 2026", "why is my content not ranking"
            │
            └── PROBLEM: "AI content needs optimization"
                    └── SEARCH: "how to optimize AI content for SEO", "AI content optimization tools"
```

### Example 3: Online Income for Beginners Pillar

```
PILLAR: Online Income for Beginners
    │
    ├── CLUSTER: Getting Started
    │       │
    │       ├── PROBLEM: "I have no skills or experience"
    │       │       └── SEARCH: "make money online no experience", "online income no skills"
    │       │
    │       ├── PROBLEM: "I have no money to invest"
    │       │       └── SEARCH: "make money online with no money", "free ways to earn online"
    │       │
    │       ├── PROBLEM: "I don't know which method to choose"
    │       │       └── SEARCH: "best way to make money online 2026", "online income methods comparison"
    │       │
    │       ├── PROBLEM: "I tried things and they didn't work"
    │       │       └── SEARCH: "online income scams to avoid", "why can't I make money online"
    │       │
    │       └── PROBLEM: "How much can I realistically earn?"
    │               └── SEARCH: "realistic online income 2026", "how much can beginners earn"
    │
    ├── CLUSTER: Affiliate Marketing Path
    │       │
    │       ├── PROBLEM: "I have no audience"
    │       │       └── SEARCH: "affiliate marketing without followers", "affiliate marketing no audience"
    │       │
    │       ├── PROBLEM: "I tried affiliate marketing and made nothing"
    │       │       └── SEARCH: "affiliate marketing not working", "why am I not making money affiliate marketing"
    │       │
    │       ├── PROBLEM: "I'm overwhelmed by advice"
    │       │       └── SEARCH: "affiliate marketing overwhelmed beginner", "affiliate marketing too much information"
    │       │
    │       └── PROBLEM: "Which affiliate program should I join?"
    │               └── SEARCH: "best affiliate programs beginners 2026", "affiliate marketing training reviews"
    │
    └── CLUSTER: Niche Opportunities
            │
            ├── PROBLEM: "I have limited time (full-time job, kids)"
            │       └── SEARCH: "side hustle from home part time", "make money online in spare time"
            │
            ├── PROBLEM: "I can't do this from my phone"
            │       └── SEARCH: "make money from phone", "online income no computer"
            │
            └── PROBLEM: "I need a job, not a business"
                    └── SEARCH: "remote jobs no experience", "online jobs work from home"
```

---

## Integration with Community Intelligence

### What Changes

The CI agent's search methodology changes from:

1. Receive `target_niche` (often a brand name)
2. Search Reddit for that exact term
3. Extract signals from results

To:

1. Receive `pillar` + `cluster` + `search_queries` (problem-oriented phrases)
2. Search Reddit (via Scrape Creators or redditwarp) for each query
3. Aggregate results across queries
4. Deduplicate (the same thread may match multiple queries)
5. Extract signals from the full aggregated set
6. Map validated problems back to potential solutions (brands)

### What Does NOT Change

| Aspect | Status |
|---|---|
| CI pipeline position (Stage 1) | Unchanged |
| CI deliverables (Community Intelligence Report) | Unchanged |
| CI output schema | Unchanged |
| CI → EI handoff | Unchanged |
| Findings object (Extracted → Verified → Referenced) | Unchanged |
| Cluster object | Unchanged |
| Opportunity object | Unchanged |
| Stage isolation rules | Unchanged |

### Scrape Creators Role

In this strategy, Scrape Creators is used with **problem-oriented queries**, not brand names. This means:

- **Search Reddit** for "affiliate marketing not working" — returns 6+ relevant posts across 4+ subreddits
- **Search YouTube comments** on popular "how to do affiliate marketing" videos — surfaces audience pain points
- **Search X/Twitter communities** in r/Affiliatemarketing-adjacent spaces — surfaces real-time objections
- **Search TikTok** for trending affiliate marketing questions — surfaces emerging concerns

The Scrape Creators endpoint selection does not change. Only the query input changes.

---

## Final Recommendation

### Adopt Opportunity-First Search

Replace brand-first search queries with problem-oriented search queries in the CI agent's workflow. This is a **search strategy change**, not an architectural change.

### What to Update

1. **CI agent prompts** — change how search queries are formulated. Instead of searching for brand names, search for recurring problems identified from the pillar and cluster taxonomy.

2. **Scrape Creators PoC → production** — use the same Reddit search endpoint but pass problem-oriented queries instead of brand names. The PoC already demonstrated this works: "Affiliate Marketing" and "Lead Generation" returned clean, relevant results across diverse subreddits.

3. **Community Intelligence inputs** — define CI tasks by pillar+cluster+problem, not by brand.

### What NOT to Change

- No changes to AI-EDITORIAL-OPERATING-SYSTEM.md
- No changes to EDITORIAL-OBJECT-MODEL.md
- No changes to AGENT-CONTRACT.md
- No changes to PIPELINE-ARCHITECTURE.md
- No changes to WHY.md
- No new pipeline stages
- No new canonical objects
- No new gates

### Expected Outcome

| Metric | Brand-First | Opportunity-First | Improvement |
|---|---|---|---|
| Results per query | 0–7 (noisy) | 6–7 (clean) | More signal, less noise |
| Subreddit diversity | 1–2 | 4–7 | Broader community coverage |
| False positive rate | ~40% (3/7) | ~0% (0/6, 0/7) | Nearly eliminated |
| Alignment with WHY.md | Violates | Enforces | Philosophical compliance |
| New opportunity discovery | None | Continuous | Editorial pipeline fed with validated problems |

The opportunity-first search strategy fixes the architectural issue revealed by the Scrape Creators PoC without changing the architecture itself. The only change is in *what* we search for, not *how* we process the results.

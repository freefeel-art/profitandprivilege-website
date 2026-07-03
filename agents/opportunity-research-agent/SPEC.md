# Opportunity Research Agent — Full Specification

**Version:** 1.0  
**Status:** Architecture approved — implementing

---

## 1. Mission

Determine whether a keyword represents a worthwhile publishing opportunity for Profit and Privilege and produce a standardized Opportunity Brief that can be passed to the next stage of the editorial pipeline.

The agent produces evidence, not opinions. Every claim in its output is traceable to a data source.

---

## 2. Scope

### In scope
- Accepting a keyword as input
- Running the six-stage intelligence workflow
- Producing a completed Opportunity Brief
- Saving the brief to `agents/opportunity-research-agent/briefs/[slug].md`

### Out of scope
- Writing articles or outlines
- Creating Research Briefs
- Generating Astro pages
- Modifying the repository outside the `briefs/` directory
- Making final publishing decisions (the brief recommends; the operator decides)

---

## 3. Responsibilities

1. Accept a keyword input
2. Run Keyword Intelligence (DataForSEO)
3. Run Trend Intelligence (Google Trends)
4. Run Community Intelligence (Reddit, with fallbacks)
5. Run SERP Intelligence (web search + page fetching)
6. Score the opportunity using the defined scoring model
7. Produce and save an Opportunity Brief

---

## 4. Inputs

**Required:**
- `keyword` (string) — the primary keyword or phrase to research

**Optional context:**
- `intent_hint` (string) — caller's hypothesis about search intent (e.g. "review", "how-to", "comparison")
- `affiliate_product` (string) — the affiliate product to evaluate for fit (defaults to OLSP Academy if not specified)

The keyword is the only hard requirement. All other inputs are advisory.

---

## 5. Outputs

**Primary output:** A completed Opportunity Brief saved as:
```
agents/opportunity-research-agent/briefs/[kebab-case-slug].md
```

The brief is the canonical record of the research. It becomes the input for the Content Research Agent (next pipeline stage, not yet built).

**Schema:** See Section 10 and `OUTPUT-TEMPLATE.md`.

---

## 6. Workflow

The agent executes six stages in sequence. No stage is skipped. If a stage fails, the agent records the failure in the brief and continues with available data.

```
Keyword
    ↓
Stage 1: Keyword Intelligence
    ↓
Stage 2: Trend Intelligence
    ↓
Stage 3: Community Intelligence
    ↓
Stage 4: SERP Intelligence
    ↓
Stage 5: Opportunity Scoring
    ↓
Stage 6: Opportunity Brief
```

### Stage 1 — Keyword Intelligence

**Tool:** `dataforseo-keyword-research` skill

**Retrieves:**
- Monthly search volume (global and/or US)
- CPC (cost per click — proxy for commercial intent)
- Keyword difficulty (0–100)
- Search intent classification (informational / commercial / transactional / navigational)
- Related keywords (top 10–20 by relevance and volume)
- Long-tail keyword variants
- Keyword expansion (LSI terms, semantic variants)

**Output fields populated:** Section 1 of the Opportunity Brief

**Failure handling:** If DataForSEO returns no data, record `DATA_UNAVAILABLE` and proceed. Do not halt.

---

### Stage 2 — Trend Intelligence

**Tool:** `mcp__claude_ai_G_Trends__get_interest_over_time`, `mcp__claude_ai_G_Trends__get_related_topics`

**Retrieves:**
- Interest over time (12-month rolling window)
- Trend direction: Rising / Stable / Declining / Volatile
- Seasonality pattern (if interest spikes at predictable calendar intervals)
- Peak period (month or quarter of highest interest)
- Rising related topics (breakout signals)
- Evergreen vs Trending classification:
  - **Evergreen:** stable interest across all 12 months, low variance
  - **Trending:** strong recent growth, interest accelerating
  - **Seasonal:** predictable peaks tied to calendar events
  - **Declining:** sustained downward trend over 12 months

**Output fields populated:** Section 2 of the Opportunity Brief

**Failure handling:** If Google Trends returns no data for the keyword, attempt with a simplified variant (remove qualifiers). If still unavailable, record `DATA_UNAVAILABLE` and continue.

---

### Stage 3 — Community Intelligence

**Primary tool:** `reddit-public-fetch` skill  
**Fallback sources:** Google Discussions, Quora, industry forums, YouTube comments, news threads

**Objective:** Understand what real people say about this topic — what frustrates them, what they ask, what they recommend, and what content currently exists that satisfies or fails to satisfy their needs.

**Primary workflow (Reddit):**
1. Identify the most relevant subreddits for the keyword topic
2. Fetch top posts (hot + top/year) from those subreddits
3. Fetch comments from the highest-engagement threads
4. Extract:
   - Top pain points and frustrations
   - Most-asked questions
   - Sentiment toward existing products/solutions
   - Community consensus (if any)
   - Content gaps (questions with no good answers in threads)
   - Engagement level (upvotes, comment depth, post frequency)

**Fallback workflow (when Reddit is unavailable or returns no results):**

The agent must never fail because Reddit is unavailable. If Reddit returns a 403, rate limit, empty results, or no relevant subreddits:

1. Use `WebSearch` to query Google Discussions: `site:groups.google.com OR "reddit" [keyword]`
2. Search Quora: `site:quora.com [keyword]` and fetch top threads
3. Search YouTube: `site:youtube.com [keyword] review OR experience` and read comment summaries in descriptions
4. Search industry forums relevant to the keyword topic
5. Use `mcp__claude_ai_G_News__search_news` for recent coverage and comment sections

The agent records which source was actually used in the brief under `community_source`.

**Output fields populated:** Section 3 of the Opportunity Brief

---

### Stage 4 — SERP Intelligence

**Tools:** `WebSearch` (primary), `WebFetch` (for deeper page analysis)

**Objective:** Understand what content currently ranks for this keyword, how strong it is, and where the gaps are.

**Retrieves:**
- Top 10 ranking URLs and their domains
- Domain authority assessment (qualitative: major brand / mid-authority / low-authority)
- Content type breakdown (reviews / roundups / blog posts / product pages / Reddit threads)
- Featured snippet presence (yes/no, and the snippet text if yes)
- People Also Ask questions (full list)
- Content gap analysis:
  - Topics covered by all ranking pages
  - Topics missing from ranking pages
  - Questions in PAA not answered by ranking pages
  - Angles absent from the top 10 (e.g. "independent review" where all results are affiliates)
- Weakness identification:
  - Thin content (short word count, no depth)
  - Outdated content (old dates, stale information)
  - Biased content (all results are vendor-produced or heavily promotional)
  - Missing trust signals (no methodology, no author, no sources)
  - Poor UX signals (slow, ad-heavy, hard to read)

**Depth of SERP analysis:**
- Always fetch and read the top 3 ranking pages in full
- Skim (title + headers) pages 4–10
- Note the presence of any OLSP-adjacent content or competitor affiliate content

**Output fields populated:** Section 4 of the Opportunity Brief

**Failure handling:** If search is unavailable, record `DATA_UNAVAILABLE` and continue.

---

### Stage 5 — Opportunity Scoring

**Tool:** Internal reasoning — no external tool call required

**Objective:** Synthesize the data from Stages 1–4 into a single Opportunity Score and editorial recommendation.

**Scoring model:**

The Opportunity Score is a number from 0–100, derived from four sub-scores of equal weight (25 points each):

| Sub-score | Metric | 25 pts | 15 pts | 5 pts |
|---|---|---|---|---|
| **Volume** | Monthly search volume | > 5,000 | 500–5,000 | < 500 |
| **Competition** | Keyword difficulty (inverted) | KD < 30 | KD 30–60 | KD > 60 |
| **Gap** | Content gap size + SERP weakness | Large gap + weak SERP | Moderate gap | Small gap + strong SERP |
| **Alignment** | Affiliate + editorial fit for P&P | Strong fit | Moderate fit | Weak fit |

Alignment scoring guidance:
- **Strong fit (25):** keyword naturally leads to OLSP Academy recommendation; matches existing topic clusters; informational or commercial intent
- **Moderate fit (15):** can be connected to affiliate offer but requires editorial stretch; adjacent topic
- **Weak fit (5):** no clear path to monetization; purely informational with no product tie-in

**Score thresholds:**

| Score | Label | Recommendation |
|---|---|---|
| 70–100 | **High Priority** | Recommend publishing — proceed to Content Research |
| 40–69 | **Medium Priority** | Review before committing — note caveats |
| 0–39 | **Low Priority** | Deprioritize — do not invest editorial time now |

**Output fields populated:** Section 5 of the Opportunity Brief

---

### Stage 6 — Opportunity Brief

The agent compiles all data from Stages 1–5 into the standardized Opportunity Brief template (see `OUTPUT-TEMPLATE.md`), fills every field, and saves the file to:

```
agents/opportunity-research-agent/briefs/[slug].md
```

The slug is derived from the primary keyword in kebab-case. Example:
- Keyword: `best affiliate marketing training 2026`
- Slug: `best-affiliate-marketing-training-2026`
- File: `agents/opportunity-research-agent/briefs/best-affiliate-marketing-training-2026.md`

---

## 7. Capability Layer Architecture

The agent is built against **capability interfaces**, not tool implementations. Each capability defines what data it must return (the contract). Providers are the current implementation of that contract. Providers can be swapped — or new providers added — without changing any agent logic.

```
Capability               Contract (what the agent needs)       Current Provider
─────────────────────────────────────────────────────────────────────────────────
KEYWORD_INTELLIGENCE     volume, CPC, KD, intent,              DataForSEO V1
                         related keywords, long-tail variants,
                         semantic/LSI terms

TREND_INTELLIGENCE       trend direction, classification,       Google Trends V1
                         seasonality, peak period,
                         rising related topics,
                         12-month interest summary

COMMUNITY_INTELLIGENCE   pain points, questions, sentiment,     Reddit V1          ← primary
                         engagement level, content gaps,        Quora V1           ← fallback 1
                         notable threads, community source      Google Discussions V1 ← fallback 2
                                                                YouTube V1         ← fallback 3
                                                                Google News V1     ← fallback 4

SERP_INTELLIGENCE        top 10 URLs + authority, content       WebSearch V1
                         type mix, featured snippet,
                         People Also Ask, content weaknesses,
                         content gaps, editorial angle
```

### Capability contracts

Each capability has a fixed output contract. The agent always requests the same fields regardless of which provider is active. If a provider cannot return a field, it returns `DATA_UNAVAILABLE` for that field — the agent never adjusts its request to match provider limitations.

#### KEYWORD_INTELLIGENCE contract
```
Required outputs:
  search_volume        Monthly search volume (integer or DATA_UNAVAILABLE)
  cpc                  Cost per click in USD (float or DATA_UNAVAILABLE)
  keyword_difficulty   0–100 score (integer or DATA_UNAVAILABLE)
  search_intent        Informational / Commercial / Transactional / Navigational
  long_tail_variants   List of 3–10 variant phrases with volumes
  related_keywords     List of 10–20 semantically related keywords with volume, KD, CPC
  semantic_terms       List of LSI and supporting terms
```

#### TREND_INTELLIGENCE contract
```
Required outputs:
  trend_direction         Rising / Stable / Declining / Volatile
  trend_classification    Evergreen / Trending / Seasonal / Declining
  peak_period             Month or quarter of highest interest, or N/A
  seasonality             Boolean + description
  rising_related_topics   List with growth signals
  12_month_summary        Narrative description of interest trajectory
```

#### COMMUNITY_INTELLIGENCE contract
```
Required outputs:
  community_source        Which provider actually delivered data
  engagement_level        High / Medium / Low
  top_pain_points         List of 3–5 pain points
  common_questions        List of 3–5 questions the community asks
  sentiment               Positive / Mixed / Negative / Neutral
  community_gaps          Topics asked with no satisfying answers
  notable_threads         List of 2–3 high-signal URLs
```

#### SERP_INTELLIGENCE contract
```
Required outputs:
  featured_snippet        Yes (with text) / No
  people_also_ask         List of PAA questions
  top_10_domains          List with domain, content type, authority level, notes
  content_type_mix        Breakdown by content category
  authority_level         High / Medium / Low assessment of the top 10
  content_weaknesses      List of weaknesses found in current top 10
  content_gaps            List of angles and topics missing from top 10
  our_angle               Specific position P&P can own in this SERP
```

### Provider registry (current bindings)

| Capability | Provider | Version | Tool / Skill |
|---|---|---|---|
| KEYWORD_INTELLIGENCE | DataForSEO | V1 | `dataforseo-keyword-research` skill |
| TREND_INTELLIGENCE | Google Trends | V1 | `mcp__claude_ai_G_Trends__*` MCP tools |
| COMMUNITY_INTELLIGENCE | Reddit | V1 | `reddit-public-fetch` skill |
| COMMUNITY_INTELLIGENCE fallback 1 | Quora | V1 | `WebSearch` + `WebFetch` |
| COMMUNITY_INTELLIGENCE fallback 2 | Google Discussions | V1 | `WebSearch` |
| COMMUNITY_INTELLIGENCE fallback 3 | YouTube | V1 | `WebSearch` |
| COMMUNITY_INTELLIGENCE fallback 4 | Google News | V1 | `mcp__claude_ai_G_News__search_news` |
| SERP_INTELLIGENCE | WebSearch | V1 | `WebSearch` + `WebFetch` |

### Swapping a provider

To replace a provider, update only the provider registry table above and the corresponding section in `PROMPT.md`. No other part of the spec or agent logic changes. The capability contract stays fixed; only the tool used to satisfy it changes.

Example: replacing DataForSEO with Ahrefs for keyword intelligence requires updating one row in this table and one block in `PROMPT.md`. The scoring model, output template, failure handling, and all other stages are unaffected.

---

## 8. Failure Handling

### Principle: the agent never stops because a single provider is unavailable.

Failures are handled at the capability level, not the provider level. The agent requests a capability; if the active provider fails, the next provider in the registry is tried. Only if all providers for a capability fail does the agent record `DATA_UNAVAILABLE` for that capability's fields.

| Capability failure | Response |
|---|---|
| KEYWORD_INTELLIGENCE — provider returns no data | Record `DATA_UNAVAILABLE` for all keyword fields. Continue. |
| TREND_INTELLIGENCE — provider returns no data | Retry with simplified keyword variant. If still empty, record `DATA_UNAVAILABLE`. Continue. |
| COMMUNITY_INTELLIGENCE — primary provider fails | Cascade through fallback providers in registry order (Quora → Google Discussions → YouTube → Google News). Record which provider actually delivered data as `community_source`. |
| COMMUNITY_INTELLIGENCE — all providers fail | Record `DATA_UNAVAILABLE`. Note in scoring rationale. Continue. |
| SERP_INTELLIGENCE — provider returns no data | Record `DATA_UNAVAILABLE`. Mark SERP section incomplete. Continue. |
| SERP_INTELLIGENCE — individual page fetch fails | Skip that page. Continue with remaining pages. Note in brief. |
| All capabilities fail | Complete brief with available data only. Set status to `INCOMPLETE — MANUAL REVIEW REQUIRED`. Do not produce a score. |

### What the agent never does under failure conditions:
- Invent or estimate data it did not retrieve
- Produce a score based on incomplete data without flagging the incompleteness
- Halt and return nothing
- Record a provider as successful when it was not queried or returned no data

---

## 9. Prompt Design Principles

### Role framing
The agent is framed as an editorial research analyst, not a content writer. Its job is to surface evidence, not produce prose.

### Capability-first language
The prompt instructs the agent in terms of capabilities, not tools. The agent is told to "invoke KEYWORD_INTELLIGENCE" and consults the provider registry to know which tool to call. This means the prompt does not need to change when providers are swapped — only the registry changes.

### Constraint enforcement
The prompt explicitly prohibits:
- Invented data
- Estimated search volumes without a successful KEYWORD_INTELLIGENCE response
- Fabricated community sentiment
- Unsourced SERP claims

### Stage discipline
Each stage is treated as a discrete tool call sequence. The agent completes each stage before moving to the next. It does not interleave stages.

### Output fidelity
The agent fills the Opportunity Brief template field by field. It does not summarize prematurely or skip fields. Every field either has data or explicitly records `DATA_UNAVAILABLE` or `N/A`.

### Tone
The brief is written in neutral editorial language. No promotional framing. No affiliate enthusiasm. The scoring model is explicit and traceable — the operator can see exactly why a score was assigned.

See `PROMPT.md` for the full system prompt and user prompt template.

---

## 10. Opportunity Brief Schema

The Opportunity Brief is a structured markdown document. Every field is required. If data is unavailable, the field value is `DATA_UNAVAILABLE` or `N/A` (not blank).

### Top-level header fields
```
keyword:           [primary keyword]
slug:              [kebab-case slug]
date_generated:    [ISO 8601 date]
status:            [HIGH PRIORITY / MEDIUM PRIORITY / LOW PRIORITY / INCOMPLETE]
opportunity_score: [0–100]
recommendation:    [PUBLISH / REVIEW / DEPRIORITIZE / SKIP]
```

### Section 1: Keyword Intelligence
```
search_volume:      [monthly searches]
cpc:                [USD]
keyword_difficulty: [0–100]
search_intent:      [Informational / Commercial / Transactional / Navigational]
long_tail_variants: [list]
related_keywords:   [list with volumes]
semantic_terms:     [LSI / supporting terms]
```

### Section 2: Trend Intelligence
```
trend_direction:       [Rising / Stable / Declining / Volatile]
trend_classification:  [Evergreen / Trending / Seasonal / Declining]
peak_period:           [month or quarter, or N/A]
seasonality_notes:     [description or N/A]
rising_related_topics: [list or N/A]
12_month_summary:      [narrative description of the trend line]
```

### Section 3: Community Intelligence
```
community_source:      [Reddit / Google Discussions / Quora / YouTube / etc.]
subreddits_researched: [list or N/A]
engagement_level:      [High / Medium / Low / DATA_UNAVAILABLE]
top_pain_points:       [bulleted list]
common_questions:      [bulleted list]
sentiment:             [Positive / Mixed / Negative / Neutral / DATA_UNAVAILABLE]
community_gaps:        [topics the community asks about with no good answers]
notable_threads:       [URLs to 2–3 highest-signal threads, or N/A]
```

### Section 4: SERP Intelligence
```
featured_snippet:      [Yes — [text] / No]
people_also_ask:       [bulleted list of PAA questions]
top_10_domains:        [list with authority assessment per domain]
content_type_mix:      [breakdown: X reviews, Y roundups, Z blog posts, etc.]
authority_level:       [High — major brands dominate / Medium / Low — thin or affiliate-heavy]
content_weaknesses:    [bulleted list of weaknesses found in top 10]
content_gaps:          [bulleted list of angles / topics missing from top 10]
our_angle:             [the specific positioning Profit and Privilege can own]
```

### Section 5: Opportunity Scoring
```
volume_score:      [0–25] — [rationale]
competition_score: [0–25] — [rationale]
gap_score:         [0–25] — [rationale]
alignment_score:   [0–25] — [rationale]
total_score:       [0–100]
priority_label:    [HIGH / MEDIUM / LOW]
```

### Section 6: Editorial Recommendation
```
recommendation:          [PUBLISH / REVIEW / DEPRIORITIZE / SKIP]
recommended_type:        [Review / Blog / Roundup]
recommended_angle:       [1–2 sentence positioning statement]
recommended_cta_product: [affiliate product to feature]
suggested_title:         [draft <title> tag]
suggested_h1:            [draft <h1>]
suggested_meta:          [draft meta description, ~155 chars]
topic_cluster_fit:       [existing cluster / new cluster / standalone]
internal_link_targets:   [existing pages to link from/to]
priority_rationale:      [2–3 sentences explaining the recommendation]
```

### Section 7: Data Quality Notes
```
data_gaps:         [fields where data was unavailable]
fallbacks_used:    [list of fallback sources triggered]
confidence_level:  [High / Medium / Low — based on data completeness]
manual_review_flags: [anything the operator should verify before publishing]
```

---

## 11. Folder Structure

```
agents/
  opportunity-research-agent/
    README.md              ← overview and quick reference
    SPEC.md                ← this document
    PROMPT.md              ← system prompt and user prompt template
    OUTPUT-TEMPLATE.md     ← Opportunity Brief blank template
    briefs/
      [slug].md            ← one file per keyword researched
      [slug].md
      ...
```

The `briefs/` directory is the agent's only write target. All other files in this folder are read-only design documents.

---

## 12. Future Extensibility

The Opportunity Research Agent is designed to slot cleanly into a larger pipeline without requiring structural changes. The following extensions are anticipated but not yet implemented:

### Planned downstream agents
| Agent | Input | Notes |
|---|---|---|
| Content Research Agent | Opportunity Brief | Deepens research into sources, experts, and original data for articles |
| Article Builder Agent | Research Brief | Produces the Astro page from approved content |
| QA Agent | Built page | Validates Gold Master compliance before deployment |

### Planned enhancements to this agent

**Batch mode:** Accept a list of keywords and produce multiple briefs in one run, with a summary comparison table ranked by Opportunity Score.

**Competitor monitoring:** Track whether a keyword's SERP changes after a brief is filed — flag if a new competitor enters or if an existing weak page is updated.

**Historical scoring:** Maintain a scoring log so trends in which keyword types score highest can be identified over time.

**Google Search Console integration:** If GSC data becomes available, incorporate actual impressions and click data to validate volume estimates.

**Niche-specific scoring weights:** Allow alignment score weighting to be adjusted per affiliate product. Currently defaults to OLSP Academy fit; future products may have different alignment profiles.

### Schema versioning
The Opportunity Brief schema is versioned. The current schema is `v1.0`. If fields are added or removed, the schema version increments and the `SPEC.md` is updated. Existing briefs retain their original schema version header.

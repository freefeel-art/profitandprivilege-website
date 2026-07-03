# Opportunity Queue — Online Income for Beginners

**Schema version:** 0.4
**Last updated:** 2026-07-03
**Last run:** Online Income for Beginners (re-run under v0.4 scoring — DataForSEO removed as a required dependency)

This file is the live, ranked backlog produced by the Opportunity Discovery Agent. It is updated, not replaced, on every run — new candidates are appended, existing rows have their `status` updated in place. Every field is required; unavailable data is recorded explicitly as `Unavailable`, never left blank.

Every candidate carries **two separate scores** — they are never averaged or collapsed into one:
- **Opportunity Score (preliminary)** — is this a good opportunity, on its own merits? (Trend / Community / Gap, rescaled to 0–100 — DataForSEO/Demand is optional and never scored)
- **Priority Score** — should it be produced *now*, given the rest of the portfolio? (Opportunity Quality / Pillar Coverage & Balance / Authority Cluster & Internal-Linking Fit / Strategic Priority Fit)

The summary table below is sorted by **Priority Score**, not Opportunity Score.

**Run-wide data quality note (updated from the prior version of this run):** DataForSEO (`SEARCH_DEMAND`) is an **optional enrichment source**, disabled by default, and was not configured for this run. This is not a failure and is not treated as one — the Opportunity Score model has no Demand dimension for its absence to affect. All six candidates below are re-scored from the same underlying Trend/Community/Gap evidence gathered in the original run; only the scoring formula changed (three dimensions, rescaled ×4/3, instead of four). `TREND_INTELLIGENCE` related-topics enrichment timed out twice on two seeds and is marked `Unavailable` for that sub-signal only — interest-over-time data (the primary trend signal) succeeded for all 8 seeds. `COMMUNITY_INTELLIGENCE` cascaded past Reddit (Cloudflare-blocked site-wide, confirmed against two unrelated subreddits) to Quora (fallback provider 2) for all candidates.

---

## Summary Table

| Rank | Candidate ID | Pillar | Priority Score | Priority Label | Opportunity Score | Status | Date Discovered |
|---|---|---|---|---|---|---|---|
| 1 | make-money-online-no-money-to-start | Online Income for Beginners | 90 | Produce soon | 87 | unclaimed | 2026-07-03 |
| 2 | how-much-can-beginners-realistically-earn-online | Online Income for Beginners | 90 | Produce soon | 73 | unclaimed | 2026-07-03 |
| 3 | side-hustles-stay-at-home-moms | Online Income for Beginners | 90 | Produce soon | 73 | unclaimed | 2026-07-03 |
| 4 | make-money-online-from-your-phone | Online Income for Beginners | 80 | Produce soon | 73 | unclaimed | 2026-07-03 |
| 5 | make-money-online-without-social-media | Online Income for Beginners | 60 | Hold — reasonable, not urgent | 33 | unclaimed | 2026-07-03 |
| 6 | online-income-scams-to-avoid | Online Income for Beginners | 60 | Hold — reasonable, not urgent | 33 | unclaimed | 2026-07-03 |

Ranks 1/2/3 are tied on Priority Score; ordered by Opportunity Score descending, then alphabetically by candidate ID (candidates 2 and 3 are also tied on Opportunity Score). Ranks 5/6 are tied on both scores; ordered alphabetically by candidate ID.

---

## Candidate Detail Blocks

### make-money-online-no-money-to-start

| Field | Value |
|---|---|
| Pillar | Online Income for Beginners |
| Opportunity summary | Zero-budget constraint is the single most recurring framing across Quora's "make money online" questions — beginners specifically want confirmation that no upfront investment is required, and warnings about scams that ask for payment. |
| Candidate keyword | make money online with no money to start |
| Status | unclaimed |
| Date discovered | 2026-07-03 |
| Date status changed | 2026-07-03 |
| Promoted brief path | N/A |

#### Opportunity Score (preliminary) — is this a good opportunity?

| Dimension | Raw score (0–25) | Rationale |
|---|---|---|
| Trend | 25 | Google Trends interest-over-time shows a sustained rising trajectory across the 12-month window (roughly 20–40 in Jul–Sep 2025 rising to 60–100 in Feb–May 2026), not a one-off spike. |
| Community | 25 | 10 distinct, actively-answered Quora threads asking near-identical versions of this question; strong recurring "is this a scam" sub-theme. |
| Gap | 15 | Top-ranking results (iubenda, Wise, NerdWallet, a personal Medium post, a niche finance blog, a BlackHatWorld forum guide) are a mix of high-authority generic listicles and low-authority forum/blog content — no ranking page combines a beginner framework with an honest scam-risk callout the way this site's existing anchor article does. Moderate, not large, gap. |
| Raw total (max 75) | 65 | Sum of the three rows above |
| **Opportunity Score** | **87** | 65 × 4/3, rounded. Preliminary — not ORA's Opportunity Score; superseded once promoted and researched. |

#### Priority Score — should this be produced now?

| Dimension | Score | Rationale |
|---|---|---|
| Opportunity Quality | 25 | Opportunity Score 87 (≥70 band). |
| Pillar Coverage & Balance | 25 | Pillar has only 3 pages (`CONTENT-REGISTRY.md` § Content Pillars) despite being described there as "the highest-traffic-potential pillar" — thin relative to its own stated importance and to Lead Generation's 9 pages. |
| Authority Cluster & Internal-Linking Fit | 25 | `make-money-online-for-beginners` is currently listed as orphaned (no inbound links) in `CONTENT-REGISTRY.md` § Internal Link Map. This candidate is a natural, distinct sub-angle (zero-budget constraint vs. the anchor's general method comparison) that could both link to the anchor and be linked from it — directly resolves a documented gap. |
| Strategic / Business Priority Fit | 15 | No `strategic_priorities` supplied for this run — neutral default. |
| **Priority Score** | **90** | |
| **Priority Label** | **Produce soon** | |

#### Evidence

- **Demand (optional enrichment, not scored):** Not configured this run — DataForSEO is an optional source; no impact on scoring.
- **Trend:** Google Trends (US, 12-month): sustained rise from ~20–40 baseline (mid-2025) to 60–100 (early-to-mid 2026), with a brief late-June pullback to 29–54. Classified Rising based on the full-year trajectory rather than the most recent weeks alone.
- **Community:** Quora (fallback — Reddit's anonymous JSON endpoint returned HTTP 403/Cloudflare-blocked site-wide, confirmed against r/WorkOnline, r/beermoney, and r/personalfinance). 10 distinct threads found, e.g. "What are the free (legitimate) ways to start making money online when you have no money at all?" Consensus methods raised: freelancing, microtasks/surveys, affiliate marketing, skill-building, digital products. Recurring explicit warning: "there really is no easy way to get rich quickly online... almost certainly a scam."
- **Competitor gap:** Top results (iubenda, Wise, NerdWallet, Medium, makingsenseofcents, BlackHatWorld) confirmed via WebSearch. No ranking page pairs a zero-budget beginner framework with explicit scam-risk guidance; several are generic multi-topic listicles, not built specifically around the "$0 to start" constraint.
- **Portfolio context:** Pillar has 3 pages total. `make-money-online-for-beginners` (the pillar's own anchor article) is orphaned — 0 inbound internal links per `CONTENT-REGISTRY.md`. No `strategic_priorities` supplied for this run.

#### Coverage check

| Field | Value |
|---|---|
| Match status | None |
| Sources checked | docs/CONTENT-REGISTRY.md, src/pages/{reviews,blog,roundups}/**, agents/opportunity-research-agent/briefs/, docs/research/, OPPORTUNITY-QUEUE.md |
| Matched artifact | N/A |
| Reasoning | Semantically adjacent to the existing pillar anchor (`make-money-online-for-beginners`, primary keyword "make money online for beginners") but not a trivial variant — the zero-budget constraint is a distinct, more specific commercial-investigation angle, not a reordering or synonym of the anchor's general framing. Judged a genuine sub-angle, not a duplicate. Flagged here for operator visibility given the adjacency. |
| Checked on | 2026-07-03 |

---

### how-much-can-beginners-realistically-earn-online

| Field | Value |
|---|---|
| Pillar | Online Income for Beginners |
| Opportunity summary | Beginners consistently ask for a concrete, honest income range before committing time to any method — an expectation-setting angle distinct from "how to start." |
| Candidate keyword | how much can beginners realistically make online |
| Status | unclaimed |
| Date discovered | 2026-07-03 |
| Date status changed | 2026-07-03 |
| Promoted brief path | N/A |

#### Opportunity Score (preliminary) — is this a good opportunity?

| Dimension | Raw score (0–25) | Rationale |
|---|---|---|
| Trend | 15 | Consistently active all 12 months (40–100 range) with no sharp acceleration or decline — a strong, stable baseline rather than a breakout. |
| Community | 25 | 10 distinct Quora threads on close variants of this exact question, with concrete consensus figures (e.g. "$100–$500/month realistic for most beginners"). |
| Gap | 15 | Top results mix strong incumbents (Acorns, Shopify, NerdWallet, SideHustleNation — a dedicated niche authority) with clearly tangential/weak entries (iubenda, a cookie-consent SaaS company's blog, and a generic tutoring-site search page) — the presence of off-topic weak rankings signals SERP softness. |
| Raw total (max 75) | 55 | Sum of the three rows above |
| **Opportunity Score** | **73** | 55 × 4/3, rounded. Preliminary. |

#### Priority Score — should this be produced now?

| Dimension | Score | Rationale |
|---|---|---|
| Opportunity Quality | 25 | Opportunity Score 73 (≥70 band). |
| Pillar Coverage & Balance | 25 | Same pillar-level thinness as above. |
| Authority Cluster & Internal-Linking Fit | 25 | The anchor article's own subtitle is "What Actually Works in 2026 (And What to Skip)" — an expectation-setting reality-check angle is a near-perfect companion piece, and could supply the anchor (currently orphaned) with an inbound link. |
| Strategic / Business Priority Fit | 15 | Not stated — neutral default. |
| **Priority Score** | **90** | |
| **Priority Label** | **Produce soon** | |

#### Evidence

- **Demand (optional enrichment, not scored):** Not configured this run — optional source, no impact on scoring.
- **Trend:** Google Trends (US, 12-month): consistently 40–100 range throughout, no clear rising or declining bias — a stable, high-baseline informational query.
- **Community:** Quora (fallback, same Reddit-block reason as above). 10 threads, e.g. "How much money can people realistically earn online and what are some ways to get started?" Consensus: $100–$500/month typical for beginners, $500–$2,000+/month achievable for freelancers after 6–12 months, explicit pushback against "$10,000+/month" claims.
- **Competitor gap:** Acorns, Quora, Shopify, NerdWallet, SideHustleNation are credible incumbents; iubenda (a privacy-compliance SaaS blog) and a generic tutoring-site search page ranking for this query indicate real softness in the current top 10.
- **Portfolio context:** Same 3-page pillar; anchor article's stated angle ("what works / what to skip") directly complements this candidate.

#### Coverage check

| Field | Value |
|---|---|
| Match status | None |
| Sources checked | docs/CONTENT-REGISTRY.md, src/pages/{reviews,blog,roundups}/**, agents/opportunity-research-agent/briefs/, docs/research/, OPPORTUNITY-QUEUE.md |
| Matched artifact | N/A |
| Reasoning | No existing page, brief, or research doc addresses realistic income expectations specifically; distinct from the anchor's method-comparison framing. |
| Checked on | 2026-07-03 |

---

### side-hustles-stay-at-home-moms

| Field | Value |
|---|---|
| Pillar | Online Income for Beginners |
| Opportunity summary | A named-audience angle (stay-at-home parents needing childcare-compatible flexibility) that the pillar's existing general-audience pages don't address directly. |
| Candidate keyword | side hustles for stay-at-home moms |
| Status | unclaimed |
| Date discovered | 2026-07-03 |
| Date status changed | 2026-07-03 |
| Promoted brief path | N/A |

#### Opportunity Score (preliminary) — is this a good opportunity?

| Dimension | Raw score (0–25) | Rationale |
|---|---|---|
| Trend | 5 | Google Trends shows near-zero interest for essentially the entire 12-month window, then a sharp jump to 91–100 only in the final two weeks of data. Treated as a low-confidence/noisy signal (sparse-data artifact or genuine breakout — cannot distinguish from interest-over-time alone), not a confirmed trend. |
| Community | 25 | 10 distinct Quora threads specifically framed around the stay-at-home-parent audience; consistent theme of needing childcare-compatible flexibility. |
| Gap | 25 | Top-10 includes a Facebook group post and an "Institute of Pediatric Sleep and Parenting" site ranking for a side-hustle query — a clearly tangential/weak result occupying a top-10 slot is a strong SERP-weakness signal, alongside otherwise-credible entries (Upwork, Indeed). |
| Raw total (max 75) | 55 | Sum of the three rows above |
| **Opportunity Score** | **73** | 55 × 4/3, rounded. Preliminary. |

#### Priority Score — should this be produced now?

| Dimension | Score | Rationale |
|---|---|---|
| Opportunity Quality | 25 | Opportunity Score 73 (≥70 band). |
| Pillar Coverage & Balance | 25 | Same pillar-level thinness. |
| Authority Cluster & Internal-Linking Fit | 25 | `part-time-jobs-near-me-no-experience` is also listed as orphaned (no inbound links) in the Internal Link Map, and its "offline-inclusive practical guide" framing is a natural link target for a parent-audience piece that likely covers both online and local/offline options — directly addresses a second documented orphan. |
| Strategic / Business Priority Fit | 15 | Not stated — neutral default. |
| **Priority Score** | **90** | |
| **Priority Label** | **Produce soon** | |

#### Evidence

- **Demand (optional enrichment, not scored):** Not configured this run — optional source, no impact on scoring.
- **Trend:** Near-zero for ~50 weeks, then 24 → 91 → 100 in the final three data points. Flagged explicitly as low-confidence given the near-total absence of signal beforehand.
- **Community:** Quora (fallback). 10 threads, e.g. "What are some realistic side hustles for a stay-at-home mom of 2?" Recurring theme: flexibility around childcare is the binding constraint, more than income ceiling.
- **Competitor gap:** Upwork and Indeed are credible; a Facebook group post and a pediatric-sleep-consulting site ranking in the same top 10 indicate the SERP has real room for a more authoritative, purpose-built page.
- **Portfolio context:** `part-time-jobs-near-me-no-experience` is orphaned; this candidate is a plausible source of its first inbound link.

#### Coverage check

| Field | Value |
|---|---|
| Match status | None |
| Sources checked | docs/CONTENT-REGISTRY.md, src/pages/{reviews,blog,roundups}/**, agents/opportunity-research-agent/briefs/, docs/research/, OPPORTUNITY-QUEUE.md |
| Matched artifact | N/A |
| Reasoning | No existing page targets this named audience; the closest existing page (`no-experience-online-income`) is method-organized, not audience-organized. |
| Checked on | 2026-07-03 |

---

### make-money-online-from-your-phone

| Field | Value |
|---|---|
| Pillar | Online Income for Beginners |
| Opportunity summary | A device-constraint angle (mobile-only, no computer) distinct from the pillar's existing method-comparison and audience-based framings. |
| Candidate keyword | make money online from your phone |
| Status | unclaimed |
| Date discovered | 2026-07-03 |
| Date status changed | 2026-07-03 |
| Promoted brief path | N/A |

#### Opportunity Score (preliminary) — is this a good opportunity?

| Dimension | Raw score (0–25) | Rationale |
|---|---|---|
| Trend | 15 | Volatile week-to-week (frequent drops to 0 mixed with 30–80 readings) but a recognizable moderate baseline with a mild uptick April–May 2026. Classified Stable rather than clearly Rising given the noise. |
| Community | 25 | 10 distinct Quora threads on the exact device constraint ("no PC, only a mobile phone"). |
| Gap | 15 | Top results include several high-authority finance/tech brands (NerdWallet, Shopify, Yahoo Finance, Quicken) alongside one vendor-promotional blog (Honeygain, a data-sharing app promoting itself) — a moderately competitive but not saturated SERP. |
| Raw total (max 75) | 55 | Sum of the three rows above |
| **Opportunity Score** | **73** | 55 × 4/3, rounded. Preliminary. |

#### Priority Score — should this be produced now?

| Dimension | Score | Rationale |
|---|---|---|
| Opportunity Quality | 25 | Opportunity Score 73 (≥70 band). |
| Pillar Coverage & Balance | 25 | Same pillar-level thinness. |
| Authority Cluster & Internal-Linking Fit | 15 | Fits the existing hub (`no-experience-online-income`) as a natural extension but doesn't specifically resolve either documented orphan — neutral, not zero, fit. |
| Strategic / Business Priority Fit | 15 | Not stated — neutral default. |
| **Priority Score** | **80** | |
| **Priority Label** | **Produce soon** | |

#### Evidence

- **Demand (optional enrichment, not scored):** Not configured this run — optional source, no impact on scoring.
- **Trend:** Volatile, frequent zero-readings interspersed with 30–80 values; mild upward drift into April–May 2026 (peak 100 the week of May 3–9).
- **Community:** Quora (fallback). 10 threads, e.g. "How is it possible to earn money online with a mobile without a computer or laptop?" Recurring caveat: options are more limited and lower-earning than desktop-based methods.
- **Competitor gap:** NerdWallet, Shopify, Yahoo Finance, Quicken are credible incumbents; Honeygain's entry is self-promotional rather than an independent comparison — some room for an unbiased, OLSP-adjacent take.
- **Portfolio context:** Fits the existing 8-method hub as a device-specific extension; no specific orphan resolved.

#### Coverage check

| Field | Value |
|---|---|
| Match status | None |
| Sources checked | docs/CONTENT-REGISTRY.md, src/pages/{reviews,blog,roundups}/**, agents/opportunity-research-agent/briefs/, docs/research/, OPPORTUNITY-QUEUE.md |
| Matched artifact | N/A |
| Reasoning | `no-experience-online-income` covers 8 general methods but is not built around the mobile-only constraint specifically. |
| Checked on | 2026-07-03 |

---

### make-money-online-without-social-media

| Field | Value |
|---|---|
| Pillar | Online Income for Beginners |
| Opportunity summary | An angle explicitly avoiding social-media/audience-building requirements — already directly addressed by several dedicated competitor articles. |
| Candidate keyword | make money online without social media |
| Status | unclaimed |
| Date discovered | 2026-07-03 |
| Date status changed | 2026-07-03 |
| Promoted brief path | N/A |

#### Opportunity Score (preliminary) — is this a good opportunity?

| Dimension | Raw score (0–25) | Rationale |
|---|---|---|
| Trend | 5 | Near-zero for the entire 12-month window except an isolated two-week spike (78, then 100) in late March/early April 2026, dropping back to near-zero after. Treated as noise/a single viral moment, not sustained demand. |
| Community | 15 | Only 2 distinct Quora threads found specifically on this angle (most of the coverage found was published blog content, not raw community Q&A) — weaker unmet-demand signal than the other candidates. |
| Gap | 5 | Multiple already-published, directly-on-topic competitor articles found, including one (financialbinder.com) with a near-identical title ("How to Make Money Online Without Social Media or Followers in 2026: A Realistic Guide") plus financebuzz, joindebbie, knockedupmoney, and a Substack post — this specific angle is not underserved. |
| Raw total (max 75) | 25 | Sum of the three rows above |
| **Opportunity Score** | **33** | 25 × 4/3, rounded. Preliminary. |

#### Priority Score — should this be produced now?

| Dimension | Score | Rationale |
|---|---|---|
| Opportunity Quality | 5 | Opportunity Score 33 (<40 band). |
| Pillar Coverage & Balance | 25 | Same pillar-level thinness (this factor alone doesn't rescue a weak opportunity — see total). |
| Authority Cluster & Internal-Linking Fit | 15 | Neutral — no specific orphan resolved. |
| Strategic / Business Priority Fit | 15 | Not stated — neutral default. |
| **Priority Score** | **60** | |
| **Priority Label** | **Hold — reasonable, not urgent** | |

#### Evidence

- **Demand (optional enrichment, not scored):** Not configured this run — optional source, no impact on scoring.
- **Trend:** Near-zero all year except a two-week spike to 78–100 in late March/early April 2026, then a return to near-zero.
- **Community:** Quora (fallback) — only 2 directly relevant threads found; most search results were already-published articles rather than raw questions, suggesting the demand is being satisfied by existing content rather than going unanswered.
- **Competitor gap:** financialbinder.com's article title is nearly identical to this candidate's framing; financebuzz, joindebbie.com, knockedupmoney.com, and a Substack post also cover it directly. Not a clear gap.
- **Portfolio context:** Pillar thinness applies generically; no specific structural gap resolved.

#### Coverage check

| Field | Value |
|---|---|
| Match status | None |
| Sources checked | docs/CONTENT-REGISTRY.md, src/pages/{reviews,blog,roundups}/**, agents/opportunity-research-agent/briefs/, docs/research/, OPPORTUNITY-QUEUE.md |
| Matched artifact | N/A |
| Reasoning | No match within this site's own content — the competing coverage found is entirely on other domains, which affects Gap (above), not this check. |
| Checked on | 2026-07-03 |

---

### online-income-scams-to-avoid

| Field | Value |
|---|---|
| Pillar | Online Income for Beginners |
| Opportunity summary | A trust/safety angle warning beginners away from common online-income scams — high community concern, but the SERP is dominated by an unbeatable institutional incumbent. |
| Candidate keyword | online income scams to avoid |
| Status | unclaimed |
| Date discovered | 2026-07-03 |
| Date status changed | 2026-07-03 |
| Promoted brief path | N/A |

#### Opportunity Score (preliminary) — is this a good opportunity?

| Dimension | Raw score (0–25) | Rationale |
|---|---|---|
| Trend | 5 | Near-zero for the entire 12-month window except one isolated spike (100) the week of Nov 30–Dec 6, 2025, likely holiday-season scam-news-driven; negligible recent signal (6–7). |
| Community | 15 | 5 distinct Quora threads found — a real but smaller cluster than most other candidates, consistent with this being a well-covered topic elsewhere (see Gap) rather than an unanswered one. |
| Gap | 5 | Top results are dominated by FTC.gov (appearing three times) plus other institutional/consumer-advocacy sources (Inc. Magazine, LinkedIn Pulse) — an authoritative incumbent that a small affiliate site cannot realistically outrank or compete credibly against on this exact framing. |
| Raw total (max 75) | 25 | Sum of the three rows above |
| **Opportunity Score** | **33** | 25 × 4/3, rounded. Preliminary. |

#### Priority Score — should this be produced now?

| Dimension | Score | Rationale |
|---|---|---|
| Opportunity Quality | 5 | Opportunity Score 33 (<40 band). |
| Pillar Coverage & Balance | 25 | Same pillar-level thinness. |
| Authority Cluster & Internal-Linking Fit | 15 | Could plausibly link to/from all three existing pages as a "before you start" companion, but doesn't specifically resolve either documented orphan. |
| Strategic / Business Priority Fit | 15 | Not stated — neutral default. |
| **Priority Score** | **60** | |
| **Priority Label** | **Hold — reasonable, not urgent** | |

#### Evidence

- **Demand (optional enrichment, not scored):** Not configured this run — optional source, no impact on scoring.
- **Trend:** Near-zero all year with one isolated Dec 2025 spike (likely seasonal/news-driven), negligible recent interest.
- **Community:** Quora (fallback). 5 threads on scam-identification; recurring red flags cited: upfront payment requests, guaranteed-income promises, pressure to join fast.
- **Competitor gap:** FTC.gov ranks three times in the visible results; Inc. Magazine and a LinkedIn Pulse post also present. A government-authority incumbent at this density is a poor target for a new affiliate-site page on the identical framing.
- **Portfolio context:** Pillar thinness applies generically; worth noting this topic is also implicitly relevant to affiliate-fit risk (a "how to avoid scams" page adjacent to an affiliate CTA needs careful, credible handling) — an editorial consideration for ORA/the operator if this is ever promoted, not something this agent scores.

#### Coverage check

| Field | Value |
|---|---|
| Match status | None |
| Sources checked | docs/CONTENT-REGISTRY.md, src/pages/{reviews,blog,roundups}/**, agents/opportunity-research-agent/briefs/, docs/research/, OPPORTUNITY-QUEUE.md |
| Matched artifact | N/A |
| Reasoning | No existing page addresses scam identification directly. |
| Checked on | 2026-07-03 |

---

## Run Log

| Date | Pillar(s) run | Surfaced | Queued | Dropped (duplicate) | Flagged (ambiguous) | Strategic priorities supplied |
|---|---|---|---|---|---|---|
| 2026-07-03 | Online Income for Beginners | 6 (from 8 seeds — 1 seed merged into a queued candidate as supporting evidence, 1 seed dropped pre-clustering for insufficient signal: "passive income ideas for beginners" showed near-total zero interest on Google Trends with no distinct community or gap evidence gathered, and was not carried forward as a standalone candidate) | 6 | 0 | 0 | No |
| 2026-07-03 | Online Income for Beginners (re-run: rescored under v0.4 — DataForSEO removed as a required dependency and as a scored dimension) | 6 (same candidates, no new discovery) | 6 | 0 | 0 | No |

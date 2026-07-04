# Opportunity Queue — All Pillars

**Schema version:** 0.6
**Last updated:** 2026-07-04
**Last run:** All 4 production pillars (Online Income for Beginners, OLSP Ecosystem, Affiliate Traffic & List Building, Lead Generation) — first full-site Discovery pass under v0.4 scoring. v0.5 (2026-07-04) added the Authority Value column and backfilled it for all 23 existing candidates from evidence already on file — no candidate was re-scored or re-discovered. v0.6 (2026-07-04) added the Pipeline Type column (Heavy / Light, SPEC.md § 5b) and backfilled it for all 23 existing candidates from each candidate's already-recorded subject matter — again, no candidate was re-scored or re-discovered. See `docs/PIPELINE-ARCHITECTURE.md` for what Heavy/Light routing means downstream.

This file is the live, ranked backlog produced by the Opportunity Discovery Agent. It is updated, not replaced, on every run — new candidates are appended, existing rows have their `status` updated in place. Every field is required; unavailable data is recorded explicitly as `Unavailable`, never left blank.

Every candidate carries **four separate fields** — they are never averaged or collapsed into one another:
- **Opportunity Score (preliminary)** — is this a good opportunity, on its own merits? (Trend / Community / Gap, rescaled to 0–100 — DataForSEO/Demand is optional and never scored)
- **Priority Score** — should it be produced *now*, given the rest of the portfolio? (Opportunity Quality / Pillar Coverage & Balance / Authority Cluster & Internal-Linking Fit / Strategic Priority Fit)
- **Authority Value** *(added v0.5, SPEC.md § 5a)* — editorial planning field only: if produced, how much would it strengthen the site's long-term topical authority and internal-linking structure (⭐ to ⭐⭐⭐⭐⭐)? Derived from the same Authority Cluster & Internal-Linking Fit evidence already gathered for the Priority Score, but never itself a scored input to the Opportunity Score or Priority Score — it does not change either number and does not change the table's sort order.
- **Pipeline Type** *(added v0.6, SPEC.md § 5b)* — editorial routing field only: Heavy or Light, determining which downstream production pipeline (`docs/PIPELINE-ARCHITECTURE.md`) this candidate enters if promoted. Heavy = core subject is a specific named Company/Product/Platform/Service/Founder/Tool/Pillar Page/Major Comparison; Light = general topic or audience-scoped guide with no single named entity at its center. Never a scored input, never changes the table's sort order.

The summary table below is sorted by **Priority Score**, not Opportunity Score.

**Run-wide data quality note (updated from the prior version of this run):** DataForSEO (`SEARCH_DEMAND`) is an **optional enrichment source**, disabled by default, and was not configured for this run. This is not a failure and is not treated as one — the Opportunity Score model has no Demand dimension for its absence to affect. All six candidates below are re-scored from the same underlying Trend/Community/Gap evidence gathered in the original run; only the scoring formula changed (three dimensions, rescaled ×4/3, instead of four). `TREND_INTELLIGENCE` related-topics enrichment timed out twice on two seeds and is marked `Unavailable` for that sub-signal only — interest-over-time data (the primary trend signal) succeeded for all 8 seeds. `COMMUNITY_INTELLIGENCE` cascaded past Reddit (Cloudflare-blocked site-wide, confirmed against two unrelated subreddits) to Quora (fallback provider 2) for all candidates.

---

## Summary Table

| Rank | Candidate ID | Pillar | Priority Score | Priority Label | Opportunity Score | Authority Value | Pipeline Type | Status | Date Discovered |
|---|---|---|---|---|---|---|---|---|---|
| 1 | make-money-online-no-money-to-start | Online Income for Beginners | 90 | Produce soon | 87 | ⭐⭐⭐⭐ | Light | unclaimed | 2026-07-03 |
| 2 | how-much-can-beginners-realistically-earn-online | Online Income for Beginners | 90 | Produce soon | 73 | ⭐⭐⭐⭐ | Light | unclaimed | 2026-07-03 |
| 3 | side-hustles-stay-at-home-moms | Online Income for Beginners | 90 | Produce soon | 73 | ⭐⭐⭐⭐ | Light | unclaimed | 2026-07-03 |
| 4 | make-money-online-from-your-phone | Online Income for Beginners | 80 | Produce soon | 73 | ⭐⭐⭐ | Light | unclaimed | 2026-07-03 |
| 5 | make-money-online-without-social-media | Online Income for Beginners | 60 | Hold — reasonable, not urgent | 33 | ⭐⭐⭐ | Light | unclaimed | 2026-07-03 |
| 6 | online-income-scams-to-avoid | Online Income for Beginners | 60 | Hold — reasonable, not urgent | 33 | ⭐⭐⭐ | Light | unclaimed | 2026-07-03 |
| 7 | olsp-ecosystem-complete-guide-hub | OLSP Ecosystem | 80 | Produce soon | 87 | ⭐⭐⭐⭐⭐ | Heavy | published | 2026-07-03 |
| 8 | wayne-crowe-founder-background | OLSP Ecosystem | 70 | Produce soon | 73 | ⭐⭐⭐⭐ | Heavy | unclaimed | 2026-07-03 |
| 9 | olsp-academy-total-cost-across-upsells | OLSP Ecosystem | 70 | Produce soon | 60 | ⭐⭐⭐⭐ | Heavy | unclaimed | 2026-07-03 |
| 10 | which-olsp-upgrade-to-buy-first | OLSP Ecosystem | 70 | Produce soon | 60 | ⭐⭐⭐⭐ | Heavy | unclaimed | 2026-07-03 |
| 11 | olsp-academy-legit-scam-complaints-review | OLSP Ecosystem | 60 | Hold — reasonable, not urgent | 60 | ⭐⭐⭐ | Heavy | unclaimed | 2026-07-03 |
| 12 | olsp-academy-refund-policy-explained | OLSP Ecosystem | 60 | Hold — reasonable, not urgent | 60 | ⭐⭐⭐ | Heavy | unclaimed | 2026-07-03 |
| 13 | olsp-academy-income-proof-realistic-earnings | OLSP Ecosystem | 60 | Hold — reasonable, not urgent | 47 | ⭐⭐⭐ | Heavy | unclaimed | 2026-07-03 |
| 14 | build-email-list-affiliate-marketing-no-website | Affiliate Traffic & List Building | 80 | Produce soon | 60 | ⭐⭐⭐⭐ | Light | promoted | 2026-07-04 |
| 15 | best-free-traffic-sources-affiliate-marketing | Affiliate Traffic & List Building | 80 | Produce soon | 47 | ⭐⭐⭐⭐ | Light | unclaimed | 2026-07-03 |
| 16 | megalink-traffic-rotator-alternatives-comparison | Affiliate Traffic & List Building | 80 | Produce soon | 47 | ⭐⭐⭐⭐ | Heavy | unclaimed | 2026-07-03 |
| 17 | leadsminer-pro-alternatives-facebook-lead-tools | Affiliate Traffic & List Building | 70 | Produce soon | 33 | ⭐⭐⭐⭐ | Heavy | unclaimed | 2026-07-03 |
| 18 | affiliate-link-cloaking-safety-guide | Affiliate Traffic & List Building | 60 | Hold — reasonable, not urgent | 33 | ⭐⭐⭐ | Light | unclaimed | 2026-07-03 |
| 19 | email-lead-generation-for-affiliate-marketers | Lead Generation | 70 | Produce soon | 73 | ⭐⭐⭐⭐ | Light | unclaimed | 2026-07-03 |
| 20 | ai-chatbots-for-lead-generation | Lead Generation | 60 | Hold — reasonable, not urgent | 87 | ⭐⭐⭐ | Light | unclaimed | 2026-07-03 |
| 21 | real-estate-lead-generation | Lead Generation | 60 | Hold — reasonable, not urgent | 73 | ⭐⭐⭐ | Light | unclaimed | 2026-07-03 |
| 22 | cold-email-outreach-for-lead-generation | Lead Generation | 50 | Hold — reasonable, not urgent | 60 | ⭐⭐⭐ | Light | unclaimed | 2026-07-03 |
| 23 | lead-generation-for-coaches-and-consultants | Lead Generation | 50 | Hold — reasonable, not urgent | 60 | ⭐⭐⭐ | Light | unclaimed | 2026-07-03 |

Ranks 1/2/3 are tied on Priority Score; ordered by Opportunity Score descending, then alphabetically by candidate ID (candidates 2 and 3 are also tied on Opportunity Score). Ranks 5/6 are tied on both scores; ordered alphabetically by candidate ID.

**OLSP Ecosystem group (ranks 7–13):** Ranks 8/9/10 are tied on Priority Score (70); ordered by Opportunity Score descending (rank 8 at 73), then alphabetically by candidate ID for the remaining tie between ranks 9 and 10 (both Opportunity Score 60 — "olsp-academy-total-cost-across-upsells" precedes "which-olsp-upgrade-to-buy-first"). Ranks 11/12/13 are tied on Priority Score (60); ranks 11 and 12 are also tied on Opportunity Score (60) and ordered alphabetically by candidate ID ("olsp-academy-legit-scam-complaints-review" precedes "olsp-academy-refund-policy-explained"); rank 13 is last on this Priority tier due to its lower Opportunity Score (47).

**Affiliate Traffic & List Building group (ranks 14–18):** Ranks 14/15/16 are tied on Priority Score (80); ordered by Opportunity Score descending (rank 14 at 60), then alphabetically by candidate ID for the remaining tie between ranks 15 and 16 (both Opportunity Score 47 — "best-free-traffic-sources-affiliate-marketing" precedes "megalink-traffic-rotator-alternatives-comparison"). Rank 17 (Priority 70) and rank 18 (Priority 60) are each tied on both scores with no other candidate in their tier, so no further tie-break is needed.

**Lead Generation group (ranks 19–23):** Rank 19 (Priority 70) has no tie. Ranks 20/21 are tied on Priority Score (60); ordered by Opportunity Score descending — rank 20 ("ai-chatbots-for-lead-generation", Opportunity 87) precedes rank 21 ("real-estate-lead-generation", Opportunity 73). Ranks 22/23 are tied on both Priority (50) and Opportunity Score (60); ordered alphabetically by candidate ID ("cold-email-outreach-for-lead-generation" precedes "lead-generation-for-coaches-and-consultants"). This pillar shows the lowest Priority Score ceiling and the lowest average Pillar Coverage & Balance sub-score (5/25 for every candidate this run) of any pillar run today, consistent with Lead Generation being the site's most comprehensively covered cluster (9 pages, per CONTENT-REGISTRY.md) rather than a thin or under-served one.

**Authority Value methodology note (v0.5 backfill, 2026-07-04):** Ratings below were derived directly from each candidate's already-recorded Authority Cluster & Internal-Linking Fit sub-score (see each candidate's Priority Score breakdown) — no new discovery source or re-scoring occurred. A sub-score of 25 (directly resolves a documented structural gap: an orphaned page or an isolated review cluster) maps to ⭐⭐⭐⭐; a sub-score of 15 (neutral cluster fit) maps to ⭐⭐⭐. `olsp-ecosystem-complete-guide-hub` is elevated to ⭐⭐⭐⭐⭐ because it is, by design, the pillar/cluster hub itself — the one candidate this run whose entire purpose is synthesizing an existing cluster rather than joining one. `wayne-crowe-founder-background` is elevated one tier above its sub-score (15 → ⭐⭐⭐⭐, not ⭐⭐⭐) because its evidence describes a page that would plausibly link to/from all 5 OLSP product reviews plus the training roundup — broader cross-cluster reach than a "neutral fit" sub-score alone conveys, even though it doesn't resolve one specific named gap. No candidate this run scored a 5 (isolated, no linking path) on the underlying sub-score, so ⭐⭐ and ⭐ are unused in this backfill — the scale remains available for future candidates that do.

**Pipeline Type methodology note (v0.6 backfill, 2026-07-04, SPEC.md § 5b):** Classified directly from each candidate's already-recorded `opportunity_summary` and `candidate_keyword` — no new discovery source, re-scoring, or re-research occurred. **Heavy** (9 candidates): all 6 OLSP Ecosystem candidates whose core subject is OLSP Academy or its founder (`olsp-ecosystem-complete-guide-hub` — Pillar Page; `wayne-crowe-founder-background` — Founder; `olsp-academy-total-cost-across-upsells`, `which-olsp-upgrade-to-buy-first`, `olsp-academy-legit-scam-complaints-review`, `olsp-academy-refund-policy-explained`, `olsp-academy-income-proof-realistic-earnings` — all Product-centric), plus the 2 Affiliate Traffic & List Building candidates structured as a Major Comparison anchored to one named, already-reviewed product (`megalink-traffic-rotator-alternatives-comparison`, `leadsminer-pro-alternatives-facebook-lead-tools`). **Light** (14 candidates): all 6 Online Income for Beginners candidates and all 5 Lead Generation candidates (general topic or audience-scoped guides — no single named company/product/platform/founder at their center), plus 3 Affiliate Traffic & List Building candidates that are general how-to/safety guides (`build-email-list-affiliate-marketing-no-website`, `best-free-traffic-sources-affiliate-marketing`, `affiliate-link-cloaking-safety-guide`) — each of these cites a reviewed product (LeadsMiner Pro, Megalink Traffic Rotator, TD Pages & Magick Link respectively) only as a supporting tactic or companion mention, not as the candidate's actual subject, so the "mention vs. subject" test in SPEC.md § 5b keeps them Light despite the topical adjacency.

---

## Candidate Detail Blocks

### make-money-online-no-money-to-start

| Field | Value |
|---|---|
| Pillar | Online Income for Beginners |
| Opportunity summary | Zero-budget constraint is the single most recurring framing across Quora's "make money online" questions — beginners specifically want confirmation that no upfront investment is required, and warnings about scams that ask for payment. |
| Candidate keyword | make money online with no money to start |
| Authority Value | ⭐⭐⭐⭐ — resolves the anchor article's orphan status; direct link path to/from `make-money-online-for-beginners` |
| Pipeline Type | Light — general zero-budget beginner guide; no named company/product/platform/founder at its center |
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
| Authority Value | ⭐⭐⭐⭐ — direct companion to the anchor's "what works / what to skip" framing; resolves the same orphan |
| Pipeline Type | Light — general expectation-setting guide; no named company/product/platform/founder at its center |
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
| Authority Value | ⭐⭐⭐⭐ — resolves a second documented orphan (`part-time-jobs-near-me-no-experience`) |
| Pipeline Type | Light — audience-specific beginner guide; no named company/product/platform/founder at its center |
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
| Authority Value | ⭐⭐⭐ — extends the `no-experience-online-income` hub as a device-specific angle, but resolves no named orphan |
| Pipeline Type | Light — device-constraint how-to guide; no named company/product/platform/founder at its center |
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
| Authority Value | ⭐⭐⭐ — neutral cluster fit; no orphan resolved |
| Pipeline Type | Light — general topic guide; no named company/product/platform/founder at its center |
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
| Authority Value | ⭐⭐⭐ — plausible companion to all 3 pillar pages, but no orphan resolved |
| Pipeline Type | Light — trust/safety topic guide; no named company/product/platform/founder at its center |
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

### olsp-ecosystem-complete-guide-hub

| Field | Value |
|---|---|
| Pillar | OLSP Ecosystem |
| Opportunity summary | No page on the site currently ties together all 6 OLSP Ecosystem pages (5 product reviews + the training roundup) into one synthesized overview; third-party blogs publish single bundled "OLSP System Review" pieces, but none function as a true hub linking discrete, already-published product reviews together. |
| Candidate keyword | olsp academy complete guide to all products and upgrades |
| Authority Value | ⭐⭐⭐⭐⭐ — this candidate IS the pillar/cluster hub: synthesizes and cross-links all 6 OLSP Ecosystem pages |
| Pipeline Type | Heavy — Pillar Page synthesizing the entire OLSP Academy product suite; already produced a Research Brief cataloged in `docs/HEAVY-ASSET-LIBRARY.md` |
| Status | published |
| Date discovered | 2026-07-03 |
| Date status changed | 2026-07-04 |
| Promoted brief path | `agents/opportunity-research-agent/briefs/olsp-ecosystem-complete-guide-hub.md` |

#### Opportunity Score (preliminary) — is this a good opportunity?

| Dimension | Raw score (0–25) | Rationale |
|---|---|---|
| Trend | 15 | Two independent brand-level Google Trends queries — "OLSP" (0 all year → 100 → 78) and "Wayne Crowe" (0 all year → 25 → 100 → 56) — both spike in the same final two-to-three weeks of the 12-month window (Jun 21–Jul 4, 2026), a corroborated signal across two terms rather than one noisy series. Scored Stable/moderate rather than full Rising given the short (2–3 week) window. |
| Community | 25 | WebSearch found a large volume of ongoing third-party OLSP discussion — Trustpilot reviews spanning 10+ pages, a dedicated Facebook group (r/olspwins-style groups), and multiple independent blogs each attempting their own "full OLSP review" — consistent with real, recurring demand for one synthesized overview rather than scattered single-product pieces. |
| Gap | 25 | Competitor coverage (ippei.com, theonlineblogger.com, internetmoneypro.com, bloggingworks.com) treats OLSP as one bundled review, not a hub connecting discrete reviewed products with a decision framework; this exact gap is also independently documented in `docs/CONTENT-REGISTRY.md` § Content Gaps & Planning Notes ("No pillar page for the OLSP Ecosystem"). |
| Raw total (max 75) | 65 | Sum of the three rows above |
| **Opportunity Score** | **87** | 65 × 4/3, rounded. Preliminary — not ORA's Opportunity Score; superseded once promoted and researched. DataForSEO/Demand plays no part in this score even when available (see Evidence). |

#### Priority Score — should this be produced now?

| Dimension | Score | Rationale |
|---|---|---|
| Opportunity Quality | 25 | Opportunity Score 87 (≥70 band). |
| Pillar Coverage & Balance | 15 | Pillar has 6 pages (`CONTENT-REGISTRY.md` § Content Pillars) — mid-range relative to Lead Generation's 9 and Online Income for Beginners' 3; roughly balanced by page count even though it lacks a hub-type page. |
| Authority Cluster & Internal-Linking Fit | 25 | Directly resolves the two structural gaps named explicitly in `CONTENT-REGISTRY.md` § Content Gaps & Planning Notes: "No pillar page for the OLSP Ecosystem" and "the review cluster is isolated... none of the 8 review pages link to each other." A hub page would receive links from, and send links to, all 6 existing pages. |
| Strategic / Business Priority Fit | 15 | No `strategic_priorities` supplied for this run — neutral default. |
| **Priority Score** | **80** | |
| **Priority Label** | **Produce soon** | |

#### Evidence

- **Demand (optional enrichment, not scored):** Not configured this run — DataForSEO is an optional source; no impact on scoring.
- **Trend:** Google Trends (US, 12-month): "OLSP" and "Wayne Crowe" both near-zero for ~49 weeks, then a corroborated rise to 100/78 and 25/100/56 respectively in the final 2–3 weeks (Jun 21–Jul 4, 2026). Long-tail combination queries specific to a "complete guide" framing returned no data (insufficient absolute volume for this small brand — expected, not treated as a failure).
- **Community:** Reddit blocked site-wide (HTTP 403/Cloudflare, confirmed against r/WorkOnline and r/affiliatemarketing as unrelated control subreddits). Cascaded to WebSearch (Quora/Trustpilot/Facebook/blog fallback tier). Found: Trustpilot page with reviews spanning at least 10 pages, an active OLSP-specific Facebook group, and at least 6 independent third-party blogs each publishing their own full "OLSP System Review."
- **Competitor gap:** ippei.com, theonlineblogger.com, internetmoneypro.com, bloggingworks.com, eliteaffiliatehacks.com all publish single bundled reviews of the OLSP system as a whole; none function as a hub linking out to dedicated, in-depth reviews of each individual product (Community Builders, Live Profit Builders, MineeMe, Solo Ads) the way this site's own review cluster could support.
- **Portfolio context:** Pillar has 6 pages. `CONTENT-REGISTRY.md` § Content Gaps & Planning Notes item 4 ("No pillar page for the OLSP Ecosystem") and item 2 ("Review cluster is isolated... None of the 8 review pages link to each other or to any blog page") are both directly addressed by this candidate. No `strategic_priorities` supplied for this run.

#### Coverage check

| Field | Value |
|---|---|
| Match status | None |
| Sources checked | docs/CONTENT-REGISTRY.md, src/pages/{reviews,blog,roundups}/**, agents/opportunity-research-agent/briefs/, docs/research/, OPPORTUNITY-QUEUE.md |
| Matched artifact | N/A |
| Reasoning | No existing page, brief, or research doc functions as an OLSP Ecosystem hub; the closest existing page is the training-platform roundup, which compares OLSP Academy against competitors rather than linking together OLSP's own product suite. |
| Checked on | 2026-07-03 |

---

### wayne-crowe-founder-background

| Field | Value |
|---|---|
| Pillar | OLSP Ecosystem |
| Opportunity summary | An independent profile of Wayne Crowe (OLSP's founder) — background, track record, and credibility — distinct from the existing product-focused reviews; coincides with a recent, corroborated search-interest spike in both "Wayne Crowe" and "OLSP" as bare brand terms. |
| Candidate keyword | who is wayne crowe olsp academy founder |
| Authority Value | ⭐⭐⭐⭐ — plausible link source to/from all 5 product reviews plus the training roundup, broader cross-cluster reach than its "neutral" Priority sub-score alone implies |
| Pipeline Type | Heavy — Founder profile; core subject is Wayne Crowe himself, a named individual, not a general topic |
| Status | unclaimed |
| Date discovered | 2026-07-03 |
| Date status changed | 2026-07-03 |
| Promoted brief path | N/A |

#### Opportunity Score (preliminary) — is this a good opportunity?

| Dimension | Raw score (0–25) | Rationale |
|---|---|---|
| Trend | 25 | Google Trends (US, 12-month): "Wayne Crowe" is 0 for ~49 weeks then rises to 25 → 100 → 56 in the final 3 weeks; "OLSP" (bare term) shows the same pattern (0 → 100 → 78) in the same final 2 weeks. Classified Rising on the strength of this cross-term corroboration, though the window is short (see Evidence caveat). |
| Community | 15 | Several third-party pieces reference Wayne Crowe by name (bloggingworks.com, ippei.com, a Medium profile piece, olspbuilders.com "Wayne Crowe's Secrets") and one source cites a specific claim ("$15 million in commissions... since 2019"), but most raw community Q&A found was about the product, not the founder specifically — moderate, not strong, dedicated signal. |
| Gap | 15 | The one existing founder-focused piece found (olspbuilders.com, "Wayne Crowe's Secrets: The Driving Force Behind OLSP System Success") is promotional/affiliate-toned rather than independent; no neutral, fact-checked founder profile exists, but the topic is not entirely uncovered either. Partial gap. |
| Raw total (max 75) | 55 | Sum of the three rows above |
| **Opportunity Score** | **73** | 55 × 4/3, rounded. Preliminary. |

#### Priority Score — should this be produced now?

| Dimension | Score | Rationale |
|---|---|---|
| Opportunity Quality | 25 | Opportunity Score 73 (≥70 band). |
| Pillar Coverage & Balance | 15 | Same 6-page, mid-range pillar as above. |
| Authority Cluster & Internal-Linking Fit | 15 | A founder profile is a plausible link source to/from all 5 product reviews and the roundup, but is a new page type rather than a direct fix for the specific "isolated review cluster" or "missing hub" gaps named in the registry — neutral fit. |
| Strategic / Business Priority Fit | 15 | Not stated — neutral default. |
| **Priority Score** | **70** | |
| **Priority Label** | **Produce soon** | |

#### Evidence

- **Demand (optional enrichment, not scored):** Not configured this run — optional source, no impact on scoring.
- **Trend:** See Trend rationale above. Caveat per Constraint 2: this is a real, corroborated signal (two independent brand terms moving together), but the window is only 2–3 weeks long within a 12-month series that was otherwise flat at zero — presented as Rising, not as a confirmed, sustained trend.
- **Community:** Reddit blocked site-wide (same confirmed 403/Cloudflare block as above). WebSearch/blog fallback found founder-specific mentions across bloggingworks.com, ippei.com, a Medium profile, and olspbuilders.com; one source describes Wayne Crowe as "a British affiliate marketing expert and coach from Norwich, England" active since 2019/2020.
- **Competitor gap:** olspbuilders.com's founder piece is affiliate-promotional in tone; no independent, source-checked founder profile was found in the top results.
- **Portfolio context:** Same 6-page pillar. Would plausibly cross-link to all 5 product reviews and the roundup as supporting citations, though it doesn't resolve a named structural gap as directly as the hub or upgrade-selection candidates. No `strategic_priorities` supplied for this run.

#### Coverage check

| Field | Value |
|---|---|
| Match status | None |
| Sources checked | docs/CONTENT-REGISTRY.md, src/pages/{reviews,blog,roundups}/**, agents/opportunity-research-agent/briefs/, docs/research/, OPPORTUNITY-QUEUE.md |
| Matched artifact | N/A |
| Reasoning | No existing page profiles Wayne Crowe as an individual; all 6 existing OLSP Ecosystem pages are product- or platform-focused, not founder-focused. |
| Checked on | 2026-07-03 |

---

### olsp-academy-total-cost-across-upsells

| Field | Value |
|---|---|
| Pillar | OLSP Ecosystem |
| Opportunity summary | Beginners and skeptics want a single, honest breakdown of what OLSP Academy actually costs once every upsell tier is counted (reported range: $7 entry to $25,000 "Elite Plus"), distinct from any one product's own review-page pricing section. |
| Candidate keyword | how much does olsp academy actually cost with all upsells |
| Authority Value | ⭐⭐⭐⭐ — inherently cross-product; must cite and link all 5 reviewed OLSP products, resolving the isolated-review-cluster gap |
| Pipeline Type | Heavy — Product-centric cost breakdown; core subject is OLSP Academy's pricing structure across its named upsell tiers |
| Status | unclaimed |
| Date discovered | 2026-07-03 |
| Date status changed | 2026-07-03 |
| Promoted brief path | N/A |

#### Opportunity Score (preliminary) — is this a good opportunity?

| Dimension | Raw score (0–25) | Rationale |
|---|---|---|
| Trend | 5 | Google Trends returned no data for cost/pricing-framed long-tail queries ("OLSP Academy total cost") — insufficient absolute search volume for this small brand to register; scored at the Unavailable floor. |
| Community | 25 | Strong, specific signal: behindmlm.com's review is explicitly titled "OLSP System Review: Marketing suite with $25,000+ upsells," and jaymarketer.com published a dedicated "Understanding OLSP System Cost" post — both independent indicators of real, recurring scrutiny of OLSP's pricing structure. |
| Gap | 15 | Several third-party sources (ippei.com, theonlineblogger.com, jaymarketer.com, behindmlm.com) already break down the upsell tiers fairly thoroughly; a real but partial gap remains for a neutral, single-source breakdown that also cross-references this site's own 5 product reviews. |
| Raw total (max 75) | 45 | Sum of the three rows above |
| **Opportunity Score** | **60** | 45 × 4/3, rounded. Preliminary. |

#### Priority Score — should this be produced now?

| Dimension | Score | Rationale |
|---|---|---|
| Opportunity Quality | 15 | Opportunity Score 60 (40–69 band). |
| Pillar Coverage & Balance | 15 | Same 6-page, mid-range pillar. |
| Authority Cluster & Internal-Linking Fit | 25 | A cost-breakdown page is inherently cross-product — it must cite and link to the price of each of the 5 reviewed OLSP products — directly helping resolve the documented "isolated review cluster" gap. |
| Strategic / Business Priority Fit | 15 | Not stated — neutral default. |
| **Priority Score** | **70** | |
| **Priority Label** | **Produce soon** | |

#### Evidence

- **Demand (optional enrichment, not scored):** Not configured this run — optional source, no impact on scoring.
- **Trend:** No data returned for cost/pricing-specific long-tail queries (empty result set, not a failure — expected given the brand's small absolute search volume).
- **Community:** Reddit blocked site-wide (confirmed 403/Cloudflare). WebSearch fallback surfaced explicit upsell-tier figures across multiple sources: $12/$27/$47 low-tier, $99–$199/month mid-tier (Mega Builder / Team Builder), $997–$1,997 high-tier, $6,500 VIP, and $25,000 "Elite Plus" lifetime tier.
- **Competitor gap:** behindmlm.com and jaymarketer.com already cover this cost-transparency angle in some depth; ippei.com and theonlineblogger.com touch on it within broader reviews. Existing coverage is real but scattered across third-party, non-affiliated sites rather than consolidated.
- **Portfolio context:** Same 6-page pillar; this candidate would necessarily link to all 5 product reviews as pricing citations, directly supporting the "isolated review cluster" fix. No `strategic_priorities` supplied for this run.

#### Coverage check

| Field | Value |
|---|---|
| Match status | None |
| Sources checked | docs/CONTENT-REGISTRY.md, src/pages/{reviews,blog,roundups}/**, agents/opportunity-research-agent/briefs/, docs/research/, OPPORTUNITY-QUEUE.md |
| Matched artifact | N/A |
| Reasoning | Each individual review covers only its own product's price; no existing page aggregates cost across the full OLSP upsell funnel. |
| Checked on | 2026-07-03 |

---

### which-olsp-upgrade-to-buy-first

| Field | Value |
|---|---|
| Pillar | OLSP Ecosystem |
| Opportunity summary | Beginners repeatedly ask which OLSP upgrade to purchase first (or whether to upgrade at all) — a cross-product decision-guide angle distinct from any single product review. |
| Candidate keyword | which olsp academy upgrade should i buy first |
| Authority Value | ⭐⭐⭐⭐ — same cross-product linking requirement as the cost-breakdown candidate; must reference all 5 reviewed products |
| Pipeline Type | Heavy — Major Comparison across the named OLSP Academy upgrade tiers |
| Status | unclaimed |
| Date discovered | 2026-07-03 |
| Date status changed | 2026-07-03 |
| Promoted brief path | N/A |

#### Opportunity Score (preliminary) — is this a good opportunity?

| Dimension | Raw score (0–25) | Rationale |
|---|---|---|
| Trend | 5 | Google Trends returned no data for this long-tail decision-framed query — scored at the Unavailable floor, consistent with this brand's generally sparse long-tail Trends coverage. |
| Community | 25 | WebSearch surfaced explicit, conflicting third-party guidance ("best value for beginners is Mega Link," "best upgrade if you're committed is MegaBuilder," "do not upgrade if you only have 2,000 targeted subscribers") — a real, recurring decision point with no single consistent answer, indicating genuine unmet demand for a clear framework. |
| Gap | 15 | bloggingworks.com, theonlineblogger.com, and joyhealey.com ("OLSP Academy Two Years On") each offer some upgrade-order advice, but none structure it as a decision-matrix referencing this site's own 5 already-reviewed products directly. Partial gap. |
| Raw total (max 75) | 45 | Sum of the three rows above |
| **Opportunity Score** | **60** | 45 × 4/3, rounded. Preliminary. |

#### Priority Score — should this be produced now?

| Dimension | Score | Rationale |
|---|---|---|
| Opportunity Quality | 15 | Opportunity Score 60 (40–69 band). |
| Pillar Coverage & Balance | 15 | Same 6-page, mid-range pillar. |
| Authority Cluster & Internal-Linking Fit | 25 | A buy-order decision guide must reference and link to all 5 already-reviewed OLSP upgrade products with clear go/no-go criteria — directly resolves the "isolated review cluster" gap by design. |
| Strategic / Business Priority Fit | 15 | Not stated — neutral default. |
| **Priority Score** | **70** | |
| **Priority Label** | **Produce soon** | |

#### Evidence

- **Demand (optional enrichment, not scored):** Not configured this run — optional source, no impact on scoring.
- **Trend:** No data returned for this long-tail query (empty result set, not a failure).
- **Community:** Reddit blocked site-wide (confirmed 403/Cloudflare). WebSearch fallback found conflicting upgrade-order advice across multiple independent sources, plus a repeated caution against buying every upsell without first mastering the $7 entry tier.
- **Competitor gap:** bloggingworks.com, theonlineblogger.com, and joyhealey.com each give partial upgrade-order guidance; none present it as a structured comparison across this site's specific 5 reviewed products.
- **Portfolio context:** Same 6-page pillar; this candidate directly requires linking to all 5 product reviews, supporting the documented cluster-isolation fix. No `strategic_priorities` supplied for this run.

#### Coverage check

| Field | Value |
|---|---|
| Match status | None |
| Sources checked | docs/CONTENT-REGISTRY.md, src/pages/{reviews,blog,roundups}/**, agents/opportunity-research-agent/briefs/, docs/research/, OPPORTUNITY-QUEUE.md |
| Matched artifact | N/A |
| Reasoning | Each review covers its own product in isolation; no existing page compares the upgrade path across products or gives buy-order guidance. Adjacent to, but distinct from, each individual product review — flagged here for operator visibility given that adjacency, though not judged a duplicate. |
| Checked on | 2026-07-03 |

---

### olsp-academy-legit-scam-complaints-review

| Field | Value |
|---|---|
| Pillar | OLSP Ecosystem |
| Opportunity summary | A dedicated trust/legitimacy angle — "is OLSP Academy legit or a scam" merged with the closely related "complaints" angle at clustering, since both surfaced the same underlying Quora/Trustpilot evidence — distinct from the existing product-by-product reviews. |
| Candidate keyword | is olsp academy legit or a scam |
| Authority Value | ⭐⭐⭐ — neutral fit; links naturally to the OLSP Academy review only, no cross-product requirement |
| Pipeline Type | Heavy — Product-centric trust/legitimacy investigation; core subject is OLSP Academy specifically |
| Status | unclaimed |
| Date discovered | 2026-07-03 |
| Date status changed | 2026-07-03 |
| Promoted brief path | N/A |

#### Opportunity Score (preliminary) — is this a good opportunity?

| Dimension | Raw score (0–25) | Rationale |
|---|---|---|
| Trend | 5 | Google Trends returned no data for "is OLSP Academy legit" or "OLSP Academy complaints" — scored at the Unavailable floor. |
| Community | 25 | A direct Quora thread was found ("Is the OLSP platform affiliate marketing program good?"), plus Trustpilot reviews spanning 10+ pages including explicit scam-alert warnings about the VIP course and at least one report of paying $7 and receiving nothing — strong, specific trust-related community signal. |
| Gap | 15 | Several existing third-party pages already address legitimacy directly (weaverpowerboost.com "is OLSP legit or a scam," olspgroup johnsmithpublishing "clear honest overview"), though many appear to be affiliate-toned rather than independently skeptical. Partial gap. |
| Raw total (max 75) | 45 | Sum of the three rows above |
| **Opportunity Score** | **60** | 45 × 4/3, rounded. Preliminary. |

#### Priority Score — should this be produced now?

| Dimension | Score | Rationale |
|---|---|---|
| Opportunity Quality | 15 | Opportunity Score 60 (40–69 band). |
| Pillar Coverage & Balance | 15 | Same 6-page, mid-range pillar. |
| Authority Cluster & Internal-Linking Fit | 15 | Would naturally link to the OLSP Academy review as its closest match, but doesn't specifically require citing all 5 products the way the hub, cost, or upgrade-selection candidates do — neutral fit. |
| Strategic / Business Priority Fit | 15 | Not stated — neutral default. |
| **Priority Score** | **60** | |
| **Priority Label** | **Hold — reasonable, not urgent** | |

#### Evidence

- **Demand (optional enrichment, not scored):** Not configured this run — optional source, no impact on scoring.
- **Trend:** No data returned for either merged seed query (empty result set, not a failure).
- **Community:** Reddit blocked site-wide (confirmed 403/Cloudflare). WebSearch fallback found a direct Quora thread on OLSP's legitimacy, Trustpilot reviews across 10+ pages (rated "Great," 4.2/5 overall) alongside specific scam-alert complaints about the VIP course and at least one no-value-received report.
- **Competitor gap:** weaverpowerboost.com and olspgroup.johnsmithpublishing.com both directly address the legit-or-scam question; existing coverage is real, though mixed in independence/tone.
- **Portfolio context:** Same 6-page pillar. Adjacent to the existing OLSP Academy review, which likely touches legitimacy as part of a full product review, but a dedicated trust/complaints page is a distinct angle, not a trivial variant. No `strategic_priorities` supplied for this run.

#### Coverage check

| Field | Value |
|---|---|
| Match status | None |
| Sources checked | docs/CONTENT-REGISTRY.md, src/pages/{reviews,blog,roundups}/**, agents/opportunity-research-agent/briefs/, docs/research/, OPPORTUNITY-QUEUE.md |
| Matched artifact | N/A |
| Reasoning | No page title, primary keyword, or slug in the registry or `src/pages/reviews/` matches a dedicated trust/complaints angle; the existing OLSP Academy review is a full product review, not a trust-focused piece — judged adjacent, not duplicate, and flagged here for operator visibility. |
| Checked on | 2026-07-03 |

---

### olsp-academy-refund-policy-explained

| Field | Value |
|---|---|
| Pillar | OLSP Ecosystem |
| Opportunity summary | Recurring uncertainty about whether OLSP Academy offers refunds, and under what terms across its many upsell tiers — no single page directly and neutrally answers this. |
| Candidate keyword | does olsp academy have a refund policy |
| Authority Value | ⭐⭐⭐ — neutral fit; single-product focus, not cross-cluster |
| Pipeline Type | Heavy — Product-centric policy explainer; core subject is OLSP Academy's refund terms specifically |
| Status | unclaimed |
| Date discovered | 2026-07-03 |
| Date status changed | 2026-07-03 |
| Promoted brief path | N/A |

#### Opportunity Score (preliminary) — is this a good opportunity?

| Dimension | Raw score (0–25) | Rationale |
|---|---|---|
| Trend | 5 | Google Trends returned no data for "OLSP Academy refund policy" — scored at the Unavailable floor. |
| Community | 15 | WebSearch found conflicting refund-experience reports (some Trustpilot reviewers report refunds issued on request; others report difficulty or delays) — a real but moderate signal, less concentrated than the legit/scam or cost-transparency candidates. |
| Gap | 25 | No single page found that neutrally and directly answers "does OLSP Academy have a refund policy" — existing information is scattered across Trustpilot testimonials and inconsistent mentions inside broader reviews, not a dedicated explainer. |
| Raw total (max 75) | 45 | Sum of the three rows above |
| **Opportunity Score** | **60** | 45 × 4/3, rounded. Preliminary. |

#### Priority Score — should this be produced now?

| Dimension | Score | Rationale |
|---|---|---|
| Opportunity Quality | 15 | Opportunity Score 60 (40–69 band). |
| Pillar Coverage & Balance | 15 | Same 6-page, mid-range pillar. |
| Authority Cluster & Internal-Linking Fit | 15 | Would link naturally to the OLSP Academy review (its closest reference point) but is single-product-focused rather than requiring cross-links across the full review cluster — neutral fit. |
| Strategic / Business Priority Fit | 15 | Not stated — neutral default. |
| **Priority Score** | **60** | |
| **Priority Label** | **Hold — reasonable, not urgent** | |

#### Evidence

- **Demand (optional enrichment, not scored):** Not configured this run — optional source, no impact on scoring.
- **Trend:** No data returned (empty result set, not a failure).
- **Community:** Reddit blocked site-wide (confirmed 403/Cloudflare). WebSearch fallback found a stated "30-day money-back guarantee" referenced by one source, alongside Trustpilot reports of mixed refund experiences (some resolved via support email, others reporting delay/difficulty).
- **Competitor gap:** No dedicated refund-policy explainer page found among competitor results; information is fragmented across testimonials and passing mentions inside broader system reviews.
- **Portfolio context:** Same 6-page pillar. This is the same candidate cited as the worked example in this agent's own `SPEC.md` § 8 — included here because it independently surfaced from real Stage D1 evidence this run, not copied from the spec. No `strategic_priorities` supplied for this run.

#### Coverage check

| Field | Value |
|---|---|
| Match status | None |
| Sources checked | docs/CONTENT-REGISTRY.md, src/pages/{reviews,blog,roundups}/**, agents/opportunity-research-agent/briefs/, docs/research/, OPPORTUNITY-QUEUE.md |
| Matched artifact | N/A |
| Reasoning | No existing page, brief, or research doc addresses refund/money-back terms directly. |
| Checked on | 2026-07-03 |

---

### olsp-academy-income-proof-realistic-earnings

| Field | Value |
|---|---|
| Pillar | OLSP Ecosystem |
| Opportunity summary | An OLSP-specific realistic-earnings angle ("what do members actually make") distinct from the site's general Online Income for Beginners pillar — moderate signal, and the angle is already partly covered by existing personal-experience blog posts elsewhere. |
| Candidate keyword | how much can you realistically earn with olsp academy |
| Authority Value | ⭐⭐⭐ — neutral fit; single-product focus, not cross-cluster |
| Pipeline Type | Heavy — Product-centric earnings investigation; core subject is OLSP Academy specifically |
| Status | unclaimed |
| Date discovered | 2026-07-03 |
| Date status changed | 2026-07-03 |
| Promoted brief path | N/A |

#### Opportunity Score (preliminary) — is this a good opportunity?

| Dimension | Raw score (0–25) | Rationale |
|---|---|---|
| Trend | 5 | Google Trends returned no data for "OLSP Academy income proof" — scored at the Unavailable floor. |
| Community | 15 | Some signal (a Medium "I Tried The OLSP System for 30 Days" post, another "OLSP Still Works: My Honest Review After 1 Year," and a mention of the system "paying out commissions to 820 affiliates" in the last 24 hours per one source), but fewer distinct raw community threads than the stronger candidates above. |
| Gap | 15 | Two personal-experience narratives (Medium, x2) already cover a similar "I tried it, here's what happened" angle; a real but only partial gap remains for a more structured, evidence-based realistic-earnings breakdown. |
| Raw total (max 75) | 35 | Sum of the three rows above |
| **Opportunity Score** | **47** | 35 × 4/3, rounded. Preliminary. |

#### Priority Score — should this be produced now?

| Dimension | Score | Rationale |
|---|---|---|
| Opportunity Quality | 15 | Opportunity Score 47 (40–69 band). |
| Pillar Coverage & Balance | 15 | Same 6-page, mid-range pillar. |
| Authority Cluster & Internal-Linking Fit | 15 | Would link naturally to the OLSP Academy review but doesn't specifically resolve either the missing-hub or isolated-cluster gap — neutral fit. |
| Strategic / Business Priority Fit | 15 | Not stated — neutral default. |
| **Priority Score** | **60** | |
| **Priority Label** | **Hold — reasonable, not urgent** | |

#### Evidence

- **Demand (optional enrichment, not scored):** Not configured this run — optional source, no impact on scoring.
- **Trend:** No data returned (empty result set, not a failure).
- **Community:** Reddit blocked site-wide (confirmed 403/Cloudflare). WebSearch fallback found two personal-experience Medium posts and one figure ("paying out commissions to 820 affiliates" in a 24-hour period, per one source) but no large cluster of raw "how much can I earn" questions specific to OLSP (distinguishing this from the sister Online Income for Beginners pillar's much stronger general-earnings candidate).
- **Competitor gap:** Two Medium posts already cover a similar personal-narrative angle; existing coverage is real but not comprehensive or structured.
- **Portfolio context:** Same 6-page pillar. No `strategic_priorities` supplied for this run.

#### Coverage check

| Field | Value |
|---|---|
| Match status | None |
| Sources checked | docs/CONTENT-REGISTRY.md, src/pages/{reviews,blog,roundups}/**, agents/opportunity-research-agent/briefs/, docs/research/, OPPORTUNITY-QUEUE.md |
| Matched artifact | N/A |
| Reasoning | No existing page addresses realistic OLSP-specific earnings; distinct from the sister Online Income for Beginners pillar's general "how much can beginners realistically earn online" candidate, which is platform-agnostic rather than OLSP-specific. |
| Checked on | 2026-07-03 |

---

### build-email-list-affiliate-marketing-no-website

| Field | Value |
|---|---|
| Pillar | Affiliate Traffic & List Building |
| Opportunity summary | Beginners repeatedly ask how to start building an email list for affiliate marketing when they have no website — a recurring, specific constraint distinct from general list-building advice; this pillar currently has zero blog/informational pages to answer it. |
| Candidate keyword | how to build an email list for affiliate marketing without a website |
| Authority Value | ⭐⭐⭐⭐ — gives LeadsMiner Pro its first outbound-linked companion piece, resolving the pillar's zero-outbound-link gap |
| Pipeline Type | Light — general list-building how-to guide; cites LeadsMiner Pro as a supporting tactic, not as the subject |
| Status | promoted |
| Date discovered | 2026-07-03 |
| Date status changed | 2026-07-04 |
| Promoted brief path | `agents/opportunity-research-agent/briefs/build-email-list-affiliate-marketing-no-website.md` |

#### Opportunity Score (preliminary) — is this a good opportunity?

| Dimension | Raw score (0–25) | Rationale |
|---|---|---|
| Trend | 5 | Google Trends (US, 12-month) for both "email list building for affiliate marketing" and "build email list with no website" returned near-total zero interest with a single isolated one-week spike to 100 (Mar 29–Apr 4, 2026, and no comparable data elsewhere) — a normalization artifact typical of very low absolute-volume long-tail queries, not a confirmed trend. Scored at the Unavailable floor. |
| Community | 25 | Reddit blocked (see run-level note below). WebSearch/Quora fallback surfaced 9 distinct, directly on-topic Quora threads (e.g. "How can I collect email addresses without a website or blog for affiliate marketing," "What are the best programs to earn affiliate marketing income through e-mail list-building only (no website)?") — strong, concentrated, recurring demand specifically around the no-website constraint. |
| Gap | 15 | Unrestricted WebSearch shows this is not a wide-open gap: several dedicated, current articles already answer this exact question (emercury.net "How to Build an Email List for Affiliate Marketing," ivanmana.com "Affiliate Marketing Without a Website," nethustler.com), alongside generic ESP-vendor guides (beehiiv, SiteGround, EmailOctopus, Flodesk) that address "no website" generally but not the affiliate-marketing framing specifically. Real but partial gap: no existing piece connects the answer to this site's own reviewed prospecting tool (LeadsMiner Pro) or Megalink/TD Pages ecosystem. |
| Raw total (max 75) | 45 | Sum of the three rows above |
| **Opportunity Score** | **60** | 45 × 4/3, rounded. Preliminary — not ORA's Opportunity Score; superseded once promoted and researched. DataForSEO/Demand plays no part in this score even when available (see Evidence). |

#### Priority Score — should this be produced now?

| Dimension | Score | Rationale |
|---|---|---|
| Opportunity Quality | 15 | Opportunity Score 60 (40–69 band). |
| Pillar Coverage & Balance | 25 | Pillar has only 3 pages (`CONTENT-REGISTRY.md` § Content Pillars) — explicitly the thinnest pillar on the site, and the only one with zero blog/informational content; all three existing pages are reviews. |
| Authority Cluster & Internal-Linking Fit | 25 | `CONTENT-REGISTRY.md` § Content Gaps & Planning Notes item 2 ("Review cluster is isolated... None of the 8 review pages link to each other or to any blog page") applies directly here — all 3 pillar pages (LeadsMiner Pro, Megalink Traffic Rotator, TD Pages) show "Internal Links Out: None in body copy." A list-building guide would naturally cite LeadsMiner Pro's Facebook prospecting as a no-website-compatible tactic, giving that review its first outbound-linked companion piece — directly resolves the documented gap. |
| Strategic / Business Priority Fit | 15 | No `strategic_priorities` supplied for this run — neutral default. |
| **Priority Score** | **80** | |
| **Priority Label** | **Produce soon** | |

#### Evidence

- **Demand (optional enrichment, not scored):** Not configured this run — DataForSEO is an optional source; no impact on scoring.
- **Trend:** Google Trends (US, 12-month): near-zero across the full window for both phrasings tested, with an isolated single-week spike (likely a sparse-data normalization artifact, not sustained interest).
- **Community:** Reddit's public JSON endpoints returned HTTP 403 site-wide (confirmed against r/affiliatemarketing, r/Emailmarketing, r/WorkOnline as an unrelated control subreddit — all three blocked identically, consistent with the Cloudflare-level block documented in this file's earlier pillar runs). Cascaded to WebSearch/Quora (fallback provider 2). Found 9 distinct threads with consistent guidance clusters: funnel/landing-page tools as a website substitute, lead-magnet exchange, and multi-channel promotion (social, guest posting, communities).
- **Competitor gap:** beehiiv, SiteGround, EmailOctopus, and Flodesk rank with general "no website" guides; emercury.net, ivanmana.com, and nethustler.com rank with affiliate-marketing-specific versions of this exact question. Real competition exists, but none connect the answer to a reviewed, OLSP-adjacent Facebook prospecting tool the way this site could.
- **Portfolio context:** Pillar has 3 pages total, all reviews, zero blog/informational content — the thinnest and least-diversified pillar on the site. All 3 reviews are outbound-link orphans per the Internal Link Map. No `strategic_priorities` supplied for this run.

#### Coverage check

| Field | Value |
|---|---|
| Match status | None |
| Sources checked | docs/CONTENT-REGISTRY.md, src/pages/{reviews,blog,roundups}/**, agents/opportunity-research-agent/briefs/, docs/research/, OPPORTUNITY-QUEUE.md |
| Matched artifact | N/A |
| Reasoning | `grep` across `src/pages/blog/*.astro` and `src/pages/reviews/*.astro` for "no website" / "without a website" found only a generic, unrelated mention in `make-money-online-for-beginners.astro` ("Freelancing works... no website required" — a different pillar, a different framing, about earning methods generally, not list-building tactics). No page addresses email-list-building for affiliate marketers specifically constrained by the absence of a website. Judged a genuine gap, not a duplicate. |
| Checked on | 2026-07-03 |

---

### best-free-traffic-sources-affiliate-marketing

| Field | Value |
|---|---|
| Pillar | Affiliate Traffic & List Building |
| Opportunity summary | A recurring Quora question cluster asks specifically for free (non-paid) traffic channels for affiliate offers — distinct from Megalink Traffic Rotator's paid-traffic positioning and from Pillar 3's broader, lead-gen-framed strategy content. |
| Candidate keyword | best free traffic sources for affiliate marketing |
| Authority Value | ⭐⭐⭐⭐ — gives Megalink Traffic Rotator its first outbound link, positioned as the paid-traffic counterpart |
| Pipeline Type | Light — general free-channel roundup; cites Megalink Traffic Rotator as a companion contrast, not as the subject |
| Status | unclaimed |
| Date discovered | 2026-07-03 |
| Date status changed | 2026-07-03 |
| Promoted brief path | N/A |

#### Opportunity Score (preliminary) — is this a good opportunity?

| Dimension | Raw score (0–25) | Rationale |
|---|---|---|
| Trend | 5 | Google Trends (US, 12-month) for "free traffic affiliate marketing" returned near-zero interest for the entire window with one isolated single-week spike (Jun 21–27, 2026) — a sparse-data artifact, not a confirmed trend. Scored at the Unavailable floor. |
| Community | 25 | WebSearch/Quora fallback surfaced 9 distinct, directly on-topic threads (e.g. "What are my top 5 free traffic sources for affiliate marketing (10,000 clicks/month)?", "What's the best free traffic source for affiliate blogs in 2025?") — a strong, concentrated cluster of near-identical questions. |
| Gap | 5 | Unrestricted WebSearch shows this topic is heavily saturated: 10 dedicated, current (2026-dated) competitor articles rank directly on this exact framing (wecantrack, cpvlab.pro, adsterra, cuelinks, mthink, crakrevenue, digistore24 ×2, fluentaffiliate, mobidea) — no meaningful gap in the general topic itself. |
| Raw total (max 75) | 35 | Sum of the three rows above |
| **Opportunity Score** | **47** | 35 × 4/3, rounded. Preliminary. |

#### Priority Score — should this be produced now?

| Dimension | Score | Rationale |
|---|---|---|
| Opportunity Quality | 15 | Opportunity Score 47 (40–69 band). |
| Pillar Coverage & Balance | 25 | Same 3-page, thinnest-pillar-on-the-site status as above. |
| Authority Cluster & Internal-Linking Fit | 25 | A free-traffic guide is a natural companion/contrast piece to the existing paid-traffic reviews (Megalink Traffic Rotator, and OLSP Solo Ads in the sister pillar) — it would cite Megalink Traffic Rotator as "when you're ready to add paid traffic," giving that orphaned-outbound review its first outbound link from this pillar. Directly addresses the documented isolated-review-cluster gap. |
| Strategic / Business Priority Fit | 15 | Not stated — neutral default. |
| **Priority Score** | **80** | |
| **Priority Label** | **Produce soon** | |

#### Evidence

- **Demand (optional enrichment, not scored):** Not configured this run — optional source, no impact on scoring.
- **Trend:** Near-zero across the full 12-month window with one isolated single-week spike, treated as noise rather than sustained interest.
- **Community:** Reddit blocked site-wide (same confirmed 403/Cloudflare block as the candidate above). Quora fallback found 9 threads consistently naming SEO/blog content, YouTube, Pinterest, TikTok, Reddit, and email as the recurring "free traffic" channel set for affiliate marketers.
- **Competitor gap:** wecantrack.com, cpvlab.pro, adsterra.com, cuelinks.com, mthink.com, crakrevenue.com, digistore24.com (×2), fluentaffiliate.com, and mobidea.com all publish current, dedicated "free traffic sources for affiliate marketing" roundups — a genuinely saturated SERP with strong incumbents; no clear content gap in the general topic.
- **Portfolio context:** Same 3-page pillar. Would naturally complement and cross-link to the Megalink Traffic Rotator review as the "paid" counterpart to a free-channel guide. No `strategic_priorities` supplied for this run.

#### Coverage check

| Field | Value |
|---|---|
| Match status | None |
| Sources checked | docs/CONTENT-REGISTRY.md, src/pages/{reviews,blog,roundups}/**, agents/opportunity-research-agent/briefs/, docs/research/, OPPORTUNITY-QUEUE.md |
| Matched artifact | N/A |
| Reasoning | `lead-generation-strategies.astro` (Pillar 3) covers a 7-strategy lead-generation framework including organic Facebook prospecting and SEO, but is framed around lead capture broadly, not specifically as a "free traffic channels for affiliate offers" listicle; no page on this site directly addresses free traffic channel selection for affiliate monetization. Judged a genuine, non-trivial sub-angle — flagged here for operator visibility given the topical adjacency to `lead-generation-strategies`. |
| Checked on | 2026-07-03 |

---

### megalink-traffic-rotator-alternatives-comparison

| Field | Value |
|---|---|
| Pillar | Affiliate Traffic & List Building |
| Opportunity summary | No page on the site compares the already-reviewed Megalink Traffic Rotator against the broader link-rotator/traffic-routing tool market (ClickMagick, GeniusLink, LinkSplit, Pixelfy, RotatorLinks) — third-party roundups of this tool category exist but never mention Megalink or connect to this site's own review. |
| Candidate keyword | megalink traffic rotator alternatives compared |
| Authority Value | ⭐⭐⭐⭐ — direct fix for Megalink Traffic Rotator's zero-outbound-link status |
| Pipeline Type | Heavy — Major Comparison anchored to the named Product Megalink Traffic Rotator |
| Status | unclaimed |
| Date discovered | 2026-07-03 |
| Date status changed | 2026-07-03 |
| Promoted brief path | N/A |

#### Opportunity Score (preliminary) — is this a good opportunity?

| Dimension | Raw score (0–25) | Rationale |
|---|---|---|
| Trend | 5 | Google Trends returned an empty result set for "traffic rotator service" and "link rotator comparison" (insufficient absolute search volume for this small brand/category combination to register) — scored at the Unavailable floor, consistent with this brand's generally sparse long-tail Trends coverage seen elsewhere in this queue. |
| Community | 15 | Reddit blocked (see below). WebSearch/Quora fallback found a real but moderate trust-concern pattern specific to this product category — 3 distinct Quora threads asking whether other named traffic-rotator/exchange services ("WebTrafficGeeks," "TrafficMasters," "Simple Traffic.co") are scams — a recurring pattern directly relevant to Megalink's category, though not naming Megalink itself. |
| Gap | 15 | The general "link rotator tools" category is covered by several established roundups (geekflare.com, replug.io, marketingscoop.com, pitiya.com, linklyhq.com) featuring ClickMagick, LinkSplit, Pixelfy, RotatorLinks, and GeniusLink — a real, moderately competitive category. None of these roundups mention Megalink Traffic Rotator or connect to any OLSP-ecosystem context — a clear gap remains for a comparison anchored to this site's own reviewed product. |
| Raw total (max 75) | 35 | Sum of the three rows above |
| **Opportunity Score** | **47** | 35 × 4/3, rounded. Preliminary — not ORA's Opportunity Score; superseded once promoted and researched. |

#### Priority Score — should this be produced now?

| Dimension | Score | Rationale |
|---|---|---|
| Opportunity Quality | 15 | Opportunity Score 47 (40–69 band). |
| Pillar Coverage & Balance | 25 | Same 3-page, thinnest-pillar status. |
| Authority Cluster & Internal-Linking Fit | 25 | An alternatives-comparison piece anchored to Megalink Traffic Rotator would directly link to and from the existing Megalink review — the most direct possible resolution of the "isolated review cluster" gap for this specific page, exactly analogous to the OLSP Ecosystem pillar's upgrade-selection and cost-breakdown candidates in this same queue. |
| Strategic / Business Priority Fit | 15 | Not stated — neutral default. |
| **Priority Score** | **80** | |
| **Priority Label** | **Produce soon** | |

#### Evidence

- **Demand (optional enrichment, not scored):** Not configured this run — optional source, no impact on scoring.
- **Trend:** Empty result set for both queries tested (expected given this brand/category's small absolute search volume, not treated as a failure).
- **Community:** Reddit blocked site-wide (confirmed 403/Cloudflare against r/WorkOnline and r/Emailmarketing as unrelated control subreddits, same block documented across this file's prior pillar runs). Quora fallback found a recurring "is this rotator/traffic service a scam" question pattern across named competitor services, indicating real, category-wide trust scrutiny that a neutral comparison piece could credibly address.
- **Competitor gap:** geekflare.com, replug.io, marketingscoop.com, pitiya.com, and linklyhq.com all publish "best link rotator" roundups featuring ClickMagick ($79–169/mo), LinkSplit, Pixelfy, RotatorLinks, and GeniusLink — real competing coverage of the category, but none reference Megalink Traffic Rotator specifically or this site's own review.
- **Portfolio context:** Same 3-page pillar. This candidate is a direct structural fix for Megalink Traffic Rotator's zero-outbound-link status per the Internal Link Map. No `strategic_priorities` supplied for this run.

#### Coverage check

| Field | Value |
|---|---|
| Match status | None |
| Sources checked | docs/CONTENT-REGISTRY.md, src/pages/{reviews,blog,roundups}/**, agents/opportunity-research-agent/briefs/, docs/research/, OPPORTUNITY-QUEUE.md |
| Matched artifact | N/A |
| Reasoning | `grep` for "ClickMagick," "GeniusLink," "LinkSplit," "Pixelfy," and "RotatorLinks" across all `src/pages/blog/*.astro` and `src/pages/reviews/*.astro` files returned zero matches — no existing page compares Megalink Traffic Rotator against any named competitor. The existing Megalink review is a single-product review, not a comparison piece. |
| Checked on | 2026-07-03 |

---

### leadsminer-pro-alternatives-facebook-lead-tools

| Field | Value |
|---|---|
| Pillar | Affiliate Traffic & List Building |
| Opportunity summary | No page compares the already-reviewed LeadsMiner Pro against the broader Facebook-lead-capture tool market (Groupboss, Chatfuel, native Facebook Lead Ads) — general category roundups exist but never mention LeadsMiner Pro or this site's own review. |
| Candidate keyword | leadsminer pro alternatives for facebook lead generation |
| Authority Value | ⭐⭐⭐⭐ — direct fix for LeadsMiner Pro's zero-outbound-link status |
| Pipeline Type | Heavy — Major Comparison anchored to the named Product LeadsMiner Pro |
| Status | unclaimed |
| Date discovered | 2026-07-03 |
| Date status changed | 2026-07-03 |
| Promoted brief path | N/A |

#### Opportunity Score (preliminary) — is this a good opportunity?

| Dimension | Raw score (0–25) | Rationale |
|---|---|---|
| Trend | 5 | Google Trends returned an empty result set for "LeadsMiner Pro alternative" — insufficient absolute search volume for this small-brand long-tail query to register. Scored at the Unavailable floor. |
| Community | 5 | Reddit blocked (see below). WebSearch fallback surfaced only established vendor/blog content (Groupboss's own site, pyrsonalize.com, privyr.com, clicksgeek.com, HubSpot, Cognism, LeadsBridge) — no raw community Q&A thread specifically comparing LeadsMiner Pro to alternatives was found. Weak, vendor-content-only signal. |
| Gap | 15 | The general "Facebook lead generation tools" category is covered by multiple vendor and blog roundups (Groupboss, pyrsonalize, clicksgeek, HubSpot), but none mention LeadsMiner Pro or connect to this site's own review — a real but category-level (not brand-specific) gap remains. |
| Raw total (max 75) | 25 | Sum of the three rows above |
| **Opportunity Score** | **33** | 25 × 4/3, rounded. Preliminary. |

#### Priority Score — should this be produced now?

| Dimension | Score | Rationale |
|---|---|---|
| Opportunity Quality | 5 | Opportunity Score 33 (<40 band). |
| Pillar Coverage & Balance | 25 | Same 3-page, thinnest-pillar status (this factor alone doesn't rescue a weak opportunity — see total). |
| Authority Cluster & Internal-Linking Fit | 25 | Same direct-resolution logic as the Megalink alternatives candidate above: an alternatives-comparison piece anchored to LeadsMiner Pro would directly link to/from the existing LeadsMiner Pro review, resolving its zero-outbound-link status per the Internal Link Map. |
| Strategic / Business Priority Fit | 15 | Not stated — neutral default. |
| **Priority Score** | **70** | |
| **Priority Label** | **Produce soon** | |

#### Evidence

- **Demand (optional enrichment, not scored):** Not configured this run — optional source, no impact on scoring.
- **Trend:** Empty result set (expected given this brand's small absolute search volume, not treated as a failure).
- **Community:** Reddit blocked site-wide (confirmed 403/Cloudflare, same block documented across this file's prior pillar runs, tested here against r/WorkOnline and r/Emailmarketing as unrelated controls). WebSearch fallback found only vendor-authored and blog-roundup content, not raw community pain-point discussion — a weaker signal than the other candidates in this run.
- **Competitor gap:** Groupboss.io (self-promotional), pyrsonalize.com, privyr.com, clicksgeek.com, HubSpot, Cognism, and LeadsBridge all publish Facebook lead-generation tool content; none reference LeadsMiner Pro or position it against these alternatives.
- **Portfolio context:** Same 3-page pillar. Directly resolves LeadsMiner Pro's zero-outbound-link status per the Internal Link Map. No `strategic_priorities` supplied for this run.

#### Coverage check

| Field | Value |
|---|---|
| Match status | None |
| Sources checked | docs/CONTENT-REGISTRY.md, src/pages/{reviews,blog,roundups}/**, agents/opportunity-research-agent/briefs/, docs/research/, OPPORTUNITY-QUEUE.md |
| Matched artifact | N/A |
| Reasoning | `grep` for "Groupboss" and "Chatfuel" across all `src/pages/blog/*.astro` and `src/pages/reviews/*.astro` files returned zero matches. `social-media-lead-generation.astro` and `local-business-lead-generation.astro` (Pillar 3) discuss native Facebook Lead Ads generically as an ad format, but neither names LeadsMiner Pro, Groupboss, or Chatfuel, nor frames it as an alternatives comparison. No existing page addresses this candidate's specific angle. |
| Checked on | 2026-07-03 |

---

### affiliate-link-cloaking-safety-guide

| Field | Value |
|---|---|
| Pillar | Affiliate Traffic & List Building |
| Opportunity summary | A recurring "how to cloak affiliate links / is it safe" question cluster on Quora, but the topic is already thoroughly and authoritatively covered by established WordPress/marketing-tool sites — the weakest opportunity surfaced this run. |
| Candidate keyword | how to cloak affiliate links safely |
| Authority Value | ⭐⭐⭐ — neutral fit; only an indirect, plausible reference to TD Pages & Magick Link |
| Pipeline Type | Light — general safety/how-to guide; only an indirect, plausible mention of TD Pages & Magick Link, not the subject |
| Status | unclaimed |
| Date discovered | 2026-07-03 |
| Date status changed | 2026-07-03 |
| Promoted brief path | N/A |

#### Opportunity Score (preliminary) — is this a good opportunity?

| Dimension | Raw score (0–25) | Rationale |
|---|---|---|
| Trend | 5 | Google Trends (US, 12-month) for "affiliate link cloaking tool" and "is link cloaking safe" both returned near-zero interest for the entire window with one isolated single-week spike each (Jun 28–Jul 4, 2026 and Apr 26–May 2, 2026 respectively, on different weeks — not corroborating) — sparse-data artifacts, not a confirmed trend. Scored at the Unavailable floor. |
| Community | 15 | Reddit blocked (see below). WebSearch/Quora fallback found 10 distinct threads on link cloaking, but most are "how does this work" / definitional questions (e.g. "How does cloak work in affiliate links?", "What is link cloaking in affiliate marketing?") rather than concentrated pain-point or unmet-demand signal — moderate, not strong. |
| Gap | 5 | Unrestricted WebSearch shows this topic is thoroughly covered by strong, specific incumbents: Hostinger, PrettyLinks (the plugin vendor itself), WPBeginner, Linkly, OptinMonster, Cloudways, and Steve Scott's blog all publish detailed, tool-specific guides (Pretty Links, ThirstyAffiliates, Linkly) including compliance caveats (Amazon ToS, Facebook/Google Ads policy, FTC disclosure) — no meaningful gap. |
| Raw total (max 75) | 25 | Sum of the three rows above |
| **Opportunity Score** | **33** | 25 × 4/3, rounded. Preliminary. |

#### Priority Score — should this be produced now?

| Dimension | Score | Rationale |
|---|---|---|
| Opportunity Quality | 5 | Opportunity Score 33 (<40 band). |
| Pillar Coverage & Balance | 25 | Same 3-page, thinnest-pillar status (does not rescue a weak opportunity — see total). |
| Authority Cluster & Internal-Linking Fit | 15 | A cloaking-safety guide could plausibly reference TD Pages & Magick Link (the pillar's third review) as a supporting mention, but the connection is less direct than the two alternatives-comparison candidates above — neutral fit, not a confirmed direct resolution of a named gap. |
| Strategic / Business Priority Fit | 15 | Not stated — neutral default. |
| **Priority Score** | **60** | |
| **Priority Label** | **Hold — reasonable, not urgent** | |

#### Evidence

- **Demand (optional enrichment, not scored):** Not configured this run — optional source, no impact on scoring.
- **Trend:** Near-zero across the full 12-month window for both phrasings tested, each with a single, non-corroborating isolated spike — treated as noise.
- **Community:** Reddit blocked site-wide (confirmed 403/Cloudflare, same block documented across this file's prior pillar runs). Quora fallback found 10 threads, mostly definitional/how-to framed rather than a concentrated unmet-demand cluster; one recurring caution theme: cloaking must not be used to deceive users about the affiliate relationship.
- **Competitor gap:** Hostinger, PrettyLinks, WPBeginner, Linkly, OptinMonster, Cloudways, and stevescottsite.com all rank with detailed, tool-specific cloaking guides, including named plugins (Pretty Links, ThirstyAffiliates) and platform-compliance caveats (Amazon, Facebook/Google Ads, FTC). A strong, saturated incumbent set.
- **Portfolio context:** Same 3-page pillar. No `strategic_priorities` supplied for this run.

#### Coverage check

| Field | Value |
|---|---|
| Match status | None |
| Sources checked | docs/CONTENT-REGISTRY.md, src/pages/{reviews,blog,roundups}/**, agents/opportunity-research-agent/briefs/, docs/research/, OPPORTUNITY-QUEUE.md |
| Matched artifact | N/A |
| Reasoning | `grep -rin "cloak" src/pages/` returned zero matches anywhere on the site — no existing page addresses link cloaking. Not a duplicate, but the Gap dimension above reflects that third-party coverage elsewhere on the web is strong. |
| Checked on | 2026-07-03 |

---

### email-lead-generation-for-affiliate-marketers

| Field | Value |
|---|---|
| Pillar | Lead Generation |
| Opportunity summary | Beginners and affiliate marketers routinely ask how to turn email specifically into a lead-generation channel for promoting affiliate offers; `CONTENT-REGISTRY.md` § Content Gaps & Planning Notes (item 5) explicitly names this as the pillar's next logical extension, and no existing page treats it as its own dedicated, standalone topic — the closest content treats email only as a supporting mechanism inside a broader beginner framework or paid-traffic strategy. |
| Candidate keyword | email lead generation for affiliate marketers |
| Authority Value | ⭐⭐⭐⭐ — resolves `social-media-lead-generation`'s orphan status; the pillar's own explicitly named next extension |
| Pipeline Type | Light — general channel-specific lead-gen guide; no named company/product/platform/founder at its center |
| Status | unclaimed |
| Date discovered | 2026-07-03 |
| Date status changed | 2026-07-03 |
| Promoted brief path | N/A |

#### Opportunity Score (preliminary) — is this a good opportunity?

| Dimension | Raw score (0–25) | Rationale |
|---|---|---|
| Trend | 25 | Google Trends (US, 12-month) for "email lead generation" shows a sustained climb from a ~20–40 baseline (Jul 2025–Feb 2026) to a consistently higher 55–100 range from March through mid-June 2026, before pulling back sharply in the final two weeks (26, 22) — real, sustained growth across most of the year, not an isolated spike. |
| Community | 15 | WebSearch (site:quora.com returned no direct Quora hits for this compound query; broader web search surfaced mostly published blog content rather than raw Q&A) found real, recurring emphasis on email as affiliate marketing's highest-ROI channel and on lead-magnet/automation sequences, but not a concentrated cluster of raw unanswered community questions the way narrower seeds (cold email, real estate, coaches) produced this run. |
| Gap | 15 | Broad "lead generation for affiliate marketing" is a crowded space (fractalmax.agency, impact.com, devweboic.com, misterelly.com, businessofapps.com, callingagency.com, postaffiliatepro.com, legiit.com, propellerads.com, plus 2026-dated pieces from greedleads.com, cpa.leadgid.com, abmatic.ai), but none is built specifically around "email lead generation" as its own dedicated angle paired with a single low-cost entry product — a real but partial gap. |
| Raw total (max 75) | 55 | Sum of the three rows above |
| **Opportunity Score** | **73** | 55 × 4/3, rounded. Preliminary — not ORA's Opportunity Score; superseded once promoted and researched. DataForSEO/Demand plays no part in this score even when available (see Evidence). |

#### Priority Score — should this be produced now?

| Dimension | Score | Rationale |
|---|---|---|
| Opportunity Quality | 25 | Opportunity Score 73 (≥70 band). |
| Pillar Coverage & Balance | 5 | Lead Generation has 9 pages — the most of any pillar on the site — and `CONTENT-REGISTRY.md` § Content Gaps & Planning Notes item 5 describes the cluster as spanning "every major intent type... comprehensive coverage." Already well-covered/saturated relative to the site's other pillars. |
| Authority Cluster & Internal-Linking Fit | 25 | `CONTENT-REGISTRY.md` § Internal Link Map lists `/blog/social-media-lead-generation/` as orphaned (no inbound links — the newest article). An email-lead-gen guide would naturally cross-link to it as a complementary channel, and would extend rather than duplicate `lead-generation-for-beginners.astro`'s existing nurture-sequence/lead-magnet framework — directly addresses a documented gap and is the pillar's own explicitly named next extension. |
| Strategic / Business Priority Fit | 15 | No `strategic_priorities` supplied for this run — neutral default. |
| **Priority Score** | **70** | |
| **Priority Label** | **Produce soon** | |

#### Evidence

- **Demand (optional enrichment, not scored):** Not configured this run — DataForSEO is an optional source; no impact on scoring.
- **Trend:** Google Trends (US, 12-month): ~20–40 baseline Jul 2025–Feb 2026, rising to a sustained 55–100 range March–mid-June 2026, pulling back to 26/22 in the final two weeks.
- **Community:** Reddit blocked site-wide (HTTP 403/Cloudflare, re-confirmed this run against r/EmailMarketing and r/sales as control subreddits). WebSearch/Quora fallback (site:quora.com) returned no directly on-topic Quora URLs for this compound query; broader WebSearch found the topic discussed mainly through published content (email as highest-ROI affiliate channel; lead magnets and automated sequences as the standard mechanism) rather than raw unanswered questions.
- **Competitor gap:** fractalmax.agency, impact.com, devweboic.com, misterelly.com, businessofapps.com, callingagency.com, postaffiliatepro.com, legiit.com, propellerads.com, greedleads.com, cpa.leadgid.com, and abmatic.ai all publish general "lead generation for affiliate marketing" guides; none is built specifically around email as a dedicated, standalone lead-generation channel paired with a single low-cost entry product.
- **Portfolio context:** Lead Generation pillar has 9 pages, described in `CONTENT-REGISTRY.md` as comprehensive across every major intent type, with "email lead generation... for affiliate marketers" explicitly named as the next logical extension (§ Content Gaps & Planning Notes item 5). `/blog/social-media-lead-generation/` is currently orphaned. No `strategic_priorities` supplied for this run.

#### Coverage check

| Field | Value |
|---|---|
| Match status | None |
| Sources checked | docs/CONTENT-REGISTRY.md, src/pages/{reviews,blog,roundups}/**, agents/opportunity-research-agent/briefs/, docs/research/, OPPORTUNITY-QUEUE.md |
| Matched artifact | N/A |
| Reasoning | `grep` across `lead-generation-for-beginners.astro`, `lead-generation-software.astro`, `lead-generation-strategies.astro`, and `what-is-lead-generation.astro` confirms email is discussed throughout as a supporting mechanism (lead capture platform, nurture sequences, "Strategy 3 — Paid email traffic") but no page treats "email lead generation" as its own dedicated, standalone topic the way `social-media-lead-generation` or `local-business-lead-generation` each get their own page. Judged a genuine, documented sub-angle (confirmed by `CONTENT-REGISTRY.md`'s own gap notes), not a duplicate — flagged here for operator visibility given the real adjacency to existing beginner/strategy content. |
| Checked on | 2026-07-03 |

---

### ai-chatbots-for-lead-generation

| Field | Value |
|---|---|
| Pillar | Lead Generation |
| Opportunity summary | A breakout, previously-absent-on-Trends search pattern for AI-chatbot-driven lead capture, with strong dedicated Quora demand and zero existing coverage anywhere on this site — the newest, least-covered channel in the pillar. |
| Candidate keyword | AI chatbots for lead generation |
| Authority Value | ⭐⭐⭐ — plausible but not required fit with existing tool/software pages |
| Pipeline Type | Light — general emerging-channel guide; no named company/product/platform/founder at its center |
| Status | unclaimed |
| Date discovered | 2026-07-03 |
| Date status changed | 2026-07-03 |
| Promoted brief path | N/A |

#### Opportunity Score (preliminary) — is this a good opportunity?

| Dimension | Raw score (0–25) | Rationale |
|---|---|---|
| Trend | 25 | Google Trends (US, 12-month) for "AI chatbot lead generation" is 0 for the entire window until literally the final two weeks (Jun 21–27: 98; Jun 28–Jul 4: 100) — a fresh, corroborated breakout, though the window is short (2 weeks), so presented as Rising rather than a confirmed sustained trend. |
| Community | 25 | WebSearch (site:quora.com) surfaced 10 distinct, directly on-topic Quora threads (e.g. "What are some good AI chatbots for lead generation?", "How can businesses use chatbots for lead generation on their website?", "Can a chatbot help in lead generation?") — a large, concentrated cluster of genuine questions. |
| Gap | 15 | Broader WebSearch found a real, moderately dense competitor set (improvado.io, featurebase.app, digitalapplied.com, tailortalk.ai, botpress.com, lindy.ai, viston.tech, digitalharshraj.com, tidio.com, fastbots.ai) — several are chatbot-SaaS-vendor content, but the category is markedly newer/less entrenched than long-established genres (consistent with the near-zero-until-breakout Trends pattern), leaving room for a differentiated, decision-focused angle rather than a tool comparison. |
| Raw total (max 75) | 65 | Sum of the three rows above |
| **Opportunity Score** | **87** | 65 × 4/3, rounded. Preliminary — not ORA's Opportunity Score; superseded once promoted and researched. DataForSEO/Demand plays no part in this score even when available (see Evidence). |

#### Priority Score — should this be produced now?

| Dimension | Score | Rationale |
|---|---|---|
| Opportunity Quality | 25 | Opportunity Score 87 (≥70 band). |
| Pillar Coverage & Balance | 5 | Same 9-page, already-comprehensive pillar as above. |
| Authority Cluster & Internal-Linking Fit | 15 | Would plausibly link to `lead-generation-software.astro` and `best-lead-generation-tools.astro` as a new tool category, and could give `social-media-lead-generation.astro` an inbound link since chatbots often live on social/website chat widgets, but doesn't specifically require it the way the email candidate does — neutral, plausible fit. |
| Strategic / Business Priority Fit | 15 | No `strategic_priorities` supplied for this run — neutral default. |
| **Priority Score** | **60** | |
| **Priority Label** | **Hold — reasonable, not urgent** | |

#### Evidence

- **Demand (optional enrichment, not scored):** Not configured this run — optional source, no impact on scoring.
- **Trend:** 0 across the entire 12-month window except the final two weeks (98, 100) — a fresh, short-window breakout.
- **Community:** Reddit blocked site-wide (confirmed 403/Cloudflare, same block re-confirmed this run). Quora fallback (site:quora.com) found 10 distinct, directly on-topic threads spanning general chatbot-vs-voicebot comparisons, lead qualification, real-estate-specific chatbot use, and RAG-based chatbot strategy.
- **Competitor gap:** improvado.io, featurebase.app, digitalapplied.com, tailortalk.ai, botpress.com, lindy.ai, viston.tech, digitalharshraj.com, tidio.com, and fastbots.ai all publish 2026-dated guides, several from chatbot-SaaS vendors; the category is real but newer/less entrenched than long-established lead-gen content genres.
- **Portfolio context:** Lead Generation pillar has 9 pages, described as comprehensive. `grep -rin "chatbot" src/pages/` returns zero matches anywhere on the site — the only candidate this run with a complete, unambiguous zero-coverage gap on-site. No `strategic_priorities` supplied for this run.

#### Coverage check

| Field | Value |
|---|---|
| Match status | None |
| Sources checked | docs/CONTENT-REGISTRY.md, src/pages/{reviews,blog,roundups}/**, agents/opportunity-research-agent/briefs/, docs/research/, OPPORTUNITY-QUEUE.md |
| Matched artifact | N/A |
| Reasoning | `grep -rin "chatbot" src/pages/` returned zero matches across the entire site (blog, reviews, roundups) — no existing page mentions chatbots in any lead-generation context. Not a duplicate. |
| Checked on | 2026-07-03 |

---

### real-estate-lead-generation

| Field | Value |
|---|---|
| Pillar | Lead Generation |
| Opportunity summary | A high-volume, sustained-interest vertical-specific angle with strong community demand, but externally dominated by dedicated real-estate-technology incumbents rather than general affiliate/marketing sites. |
| Candidate keyword | real estate lead generation |
| Authority Value | ⭐⭐⭐ — a new vertical with no existing cluster around it; neutral fit |
| Pipeline Type | Light — general vertical-specific guide; no named company/product/platform/founder at its center |
| Status | unclaimed |
| Date discovered | 2026-07-03 |
| Date status changed | 2026-07-03 |
| Promoted brief path | N/A |

#### Opportunity Score (preliminary) — is this a good opportunity?

| Dimension | Raw score (0–25) | Rationale |
|---|---|---|
| Trend | 25 | Google Trends (US, 12-month) shows a real, non-sparse, sustained climb from a ~30 baseline (Jul 2025) to a consistent 55–100 range by spring 2026 (peaking at 100 the week of May 3–9), before a 3-week pullback into early July — a genuine, substantial trend, not noise. |
| Community | 25 | WebSearch (site:quora.com) surfaced 10 distinct, directly on-topic Quora threads (e.g. "What are the real estate lead generation strategies?", "What are the best lead generation methods for beginner real estate agents?") — a large, concentrated cluster. |
| Gap | 5 | Broader WebSearch shows this topic dominated by dedicated real-estate-technology incumbents (Opendoor, HousingWire, HomeStack, Wave Connect, Goliath Data, Jigsawkraft, aihomedesign, Jamil Academy, LeadsuiteNow, ListingsToLeads) — vertical-specific authorities with far deeper real-estate subject-matter depth than a general affiliate-marketing-training site could credibly match; no meaningful gap for this site specifically to fill. |
| Raw total (max 75) | 55 | Sum of the three rows above |
| **Opportunity Score** | **73** | 55 × 4/3, rounded. Preliminary. |

#### Priority Score — should this be produced now?

| Dimension | Score | Rationale |
|---|---|---|
| Opportunity Quality | 25 | Opportunity Score 73 (≥70 band). |
| Pillar Coverage & Balance | 5 | Same 9-page, already-comprehensive pillar. |
| Authority Cluster & Internal-Linking Fit | 15 | Would plausibly cross-link to `local-business-lead-generation.astro` (the closest existing analog) and `lead-generation-strategies.astro`, but is a new vertical the pillar has no existing cluster around — neutral fit, not a documented gap resolution. |
| Strategic / Business Priority Fit | 15 | Not stated — neutral default. |
| **Priority Score** | **60** | |
| **Priority Label** | **Hold — reasonable, not urgent** | |

#### Evidence

- **Demand (optional enrichment, not scored):** Not configured this run — optional source, no impact on scoring.
- **Trend:** ~30 baseline Jul 2025, rising to a sustained 55–100 range by spring 2026 (peak 100, week of May 3–9), pulling back over the final 3 weeks.
- **Community:** Reddit blocked site-wide (confirmed 403/Cloudflare). Quora fallback (site:quora.com) found 10 threads covering community-building, social media, video marketing, referrals, and free/low-cost lead tactics for agents.
- **Competitor gap:** Opendoor, HousingWire, HomeStack, Wave Connect, Goliath Data, Jigsawkraft, aihomedesign, Jamil Academy, LeadsuiteNow, and ListingsToLeads all publish 2026-dated, vertical-specialist guides — a saturated, authority-dominated SERP.
- **Portfolio context:** Lead Generation pillar has 9 pages. `local-business-lead-generation.astro` mentions "real estate agent" only once, as one example within a cross-referral-partnership list (line 504) — not a dedicated treatment. No `strategic_priorities` supplied for this run.

#### Coverage check

| Field | Value |
|---|---|
| Match status | None |
| Sources checked | docs/CONTENT-REGISTRY.md, src/pages/{reviews,blog,roundups}/**, agents/opportunity-research-agent/briefs/, docs/research/, OPPORTUNITY-QUEUE.md |
| Matched artifact | N/A |
| Reasoning | `grep -n "real estate" src/pages/blog/*.astro` returns exactly one hit, a passing example inside `local-business-lead-generation.astro`'s partnership-referral list — not a dedicated real-estate guide. Judged a genuine gap on-site, though the Gap dimension above reflects that external competitor coverage is dense and vertical-specialist. |
| Checked on | 2026-07-03 |

---

### cold-email-outreach-for-lead-generation

| Field | Value |
|---|---|
| Pillar | Lead Generation |
| Opportunity summary | Strong, concentrated community demand for cold-email tactics, but the topic is both partially covered on-site already (as one tactic within several existing frameworks) and heavily saturated externally by cold-email-tool vendors who dominate the SERP with their own content marketing. |
| Candidate keyword | cold email outreach for lead generation |
| Authority Value | ⭐⭐⭐ — plausible companion to 4 existing pages, but resolves no named orphan |
| Pipeline Type | Light — general tactic guide; no named company/product/platform/founder at its center |
| Status | unclaimed |
| Date discovered | 2026-07-03 |
| Date status changed | 2026-07-03 |
| Promoted brief path | N/A |

#### Opportunity Score (preliminary) — is this a good opportunity?

| Dimension | Raw score (0–25) | Rationale |
|---|---|---|
| Trend | 15 | Google Trends (US, 12-month) shows real but volatile recurring bursts spread across many months (Aug–Oct cluster, one Nov spike, one Feb spike, Mar–Apr cluster, one May spike, a Jun peak of 76 declining to 23/18) — a genuine, recurring signal, but not a clean sustained rise; classified Stable. |
| Community | 25 | WebSearch (site:quora.com) surfaced 10 distinct, directly on-topic Quora threads (e.g. "How do I start cold emailing for lead generation?", "What are the best ways to use cold emails for lead generation?", "The Ultimate Cold Email Checklist") — a large, concentrated cluster. |
| Gap | 5 | Broader WebSearch shows this topic thoroughly dominated by cold-email-tool vendors publishing extensive content specifically to rank for this exact query (Mailshake, Instantly, Snov.io, Saleshandy, Outreachbloom, AiSDR, Hypergen, plus leadscrape.com, mailmeteor.com, devcommx.com) — a mature, deeply entrenched competitive genre with no meaningful gap. |
| Raw total (max 75) | 45 | Sum of the three rows above |
| **Opportunity Score** | **60** | 45 × 4/3, rounded. Preliminary. |

#### Priority Score — should this be produced now?

| Dimension | Score | Rationale |
|---|---|---|
| Opportunity Quality | 15 | Opportunity Score 60 (40–69 band). |
| Pillar Coverage & Balance | 5 | Same 9-page, already-comprehensive pillar. |
| Authority Cluster & Internal-Linking Fit | 15 | Would naturally link to `b2b-lead-generation.astro` and `sales-lead-generation.astro`, both of which already reference cold email as one outbound tactic, and to `what-is-lead-generation.astro` — a plausible companion but doesn't resolve a documented orphan or missing-hub gap. |
| Strategic / Business Priority Fit | 15 | Not stated — neutral default. |
| **Priority Score** | **50** | |
| **Priority Label** | **Hold — reasonable, not urgent** | |

#### Evidence

- **Demand (optional enrichment, not scored):** Not configured this run — optional source, no impact on scoring.
- **Trend:** Recurring non-consecutive bursts across Aug 2025–Jun 2026 (values up to 100 in isolated weeks), declining to 23/18 in the final two weeks — real but volatile, not a clean rise.
- **Community:** Reddit blocked site-wide (confirmed 403/Cloudflare). Quora fallback (site:quora.com) found 10 threads on starting cold email, effectiveness, list-building for outreach, standing out, tool recommendations, and templates.
- **Competitor gap:** Mailshake, Instantly, Snov.io, Saleshandy, Outreachbloom, AiSDR, Hypergen, leadscrape.com, mailmeteor.com, and devcommx.com all publish extensive, SEO-optimized 2026 content specifically targeting this query — a saturated, vendor-dominated genre.
- **Portfolio context:** Lead Generation pillar has 9 pages; cold email is already referenced (not deeply) in `b2b-lead-generation.astro`, `sales-lead-generation.astro` (Outbound Model section), `lead-generation-strategies.astro`, and `what-is-lead-generation.astro`. No `strategic_priorities` supplied for this run.

#### Coverage check

| Field | Value |
|---|---|
| Match status | None |
| Sources checked | docs/CONTENT-REGISTRY.md, src/pages/{reviews,blog,roundups}/**, agents/opportunity-research-agent/briefs/, docs/research/, OPPORTUNITY-QUEUE.md |
| Matched artifact | N/A |
| Reasoning | `grep -oni "cold email" src/pages/blog/*.astro` shows cold email mentioned as one tactic within `b2b-lead-generation.astro` (outbound sequence description), `sales-lead-generation.astro` (Outbound Model section), `lead-generation-strategies.astro`, and `what-is-lead-generation.astro` — but no page is dedicated to cold email as its own standalone topic (templates, deliverability, compliance, sequencing). Judged a genuine, if partial, sub-angle rather than a duplicate — flagged here for operator visibility given the real existing adjacency across four pages. |
| Checked on | 2026-07-03 |

---

### lead-generation-for-coaches-and-consultants

| Field | Value |
|---|---|
| Pillar | Lead Generation |
| Opportunity summary | An audience-specific angle (coaches and consultants selling their own expertise) that fits the pillar's established audience-specific pattern (paralleling `b2b-lead-generation`, `sales-lead-generation`, `local-business-lead-generation`) but is not yet covered, with a plausible cross-sell fit to OLSP Academy's own coach/consultant-adjacent customer base. |
| Candidate keyword | lead generation for coaches and consultants |
| Authority Value | ⭐⭐⭐ — extends the pillar's existing audience-specific pattern, but resolves no named orphan |
| Pipeline Type | Light — general audience-specific guide; no named company/product/platform/founder at its center |
| Status | unclaimed |
| Date discovered | 2026-07-03 |
| Date status changed | 2026-07-03 |
| Promoted brief path | N/A |

#### Opportunity Score (preliminary) — is this a good opportunity?

| Dimension | Raw score (0–25) | Rationale |
|---|---|---|
| Trend | 5 | Google Trends (US, 12-month) for "lead generation for coaches" is 0 for the entire window except a single isolated spike (100) in the final full week before the cutoff (Jun 21–27), dropping back to 0 immediately after — a sparse-data artifact, not a confirmed trend. |
| Community | 25 | WebSearch (site:quora.com) surfaced 10 distinct, directly on-topic Quora threads spanning general coaching, business coaching, health coaching, consulting, and fitness-coaching lead generation (e.g. "What strategy do you use to attract leads to your coaching business?", "How do I generate leads for a consulting business?") — a large, concentrated cluster across coaching sub-niches. |
| Gap | 15 | WebSearch found a real but moderate competitor set (salesbread.com, clickfunnels.com, fuziatalent.com, wiseowlmarketing.com ×2, overloop.com, alphacoast.com, planetarylabour.com) — genuine coverage exists, but it is less vendor-monopolized and less deeply entrenched than cold email or real estate, leaving room for a differentiated take tied to this site's own beginner/OLSP framing. |
| Raw total (max 75) | 45 | Sum of the three rows above |
| **Opportunity Score** | **60** | 45 × 4/3, rounded. Preliminary. |

#### Priority Score — should this be produced now?

| Dimension | Score | Rationale |
|---|---|---|
| Opportunity Quality | 15 | Opportunity Score 60 (40–69 band). |
| Pillar Coverage & Balance | 5 | Same 9-page, already-comprehensive pillar. |
| Authority Cluster & Internal-Linking Fit | 15 | Fits the pillar's existing audience-specific pattern (b2b, sales, local-business) and would plausibly link to `social-media-lead-generation.astro` — coaches skew heavily toward LinkedIn/Instagram per the community evidence — but does not specifically require it the way the email candidate does; neutral fit. |
| Strategic / Business Priority Fit | 15 | Not stated — neutral default. |
| **Priority Score** | **50** | |
| **Priority Label** | **Hold — reasonable, not urgent** | |

#### Evidence

- **Demand (optional enrichment, not scored):** Not configured this run — optional source, no impact on scoring.
- **Trend:** 0 across the entire 12-month window except one isolated spike (100) in the final full week, dropping back to 0 immediately after.
- **Community:** Reddit blocked site-wide (confirmed 403/Cloudflare). Quora fallback (site:quora.com) found 10 threads spanning business coaching, health coaching, consulting, management consulting, and fitness/personal-training coaching lead generation.
- **Competitor gap:** salesbread.com, clickfunnels.com, fuziatalent.com, wiseowlmarketing.com (×2), overloop.com, alphacoast.com, and planetarylabour.com all publish 2026-dated guides — real coverage, but less vendor-monopolized than cold email or real estate.
- **Portfolio context:** Lead Generation pillar has 9 pages including three existing audience-specific guides (b2b, sales, local-business); a coaches/consultants guide would extend that established pattern to a fourth audience segment. `social-media-lead-generation.astro` mentions "coaching" only once, as an audience example within a platform-selection matrix (line 581) — not a dedicated treatment. No `strategic_priorities` supplied for this run.

#### Coverage check

| Field | Value |
|---|---|
| Match status | None |
| Sources checked | docs/CONTENT-REGISTRY.md, src/pages/{reviews,blog,roundups}/**, agents/opportunity-research-agent/briefs/, docs/research/, OPPORTUNITY-QUEUE.md |
| Matched artifact | N/A |
| Reasoning | `grep -oni "coach\|consultant" src/pages/blog/*.astro` shows "coaching" used only as a passing audience example in `social-media-lead-generation.astro` (channel-selection matrix) and in two unrelated Online Income for Beginners pillar pages (as an income method, not a lead-gen audience). No page treats coaches/consultants as a dedicated lead-generation audience. Not a duplicate. |
| Checked on | 2026-07-03 |

---

## Run Log

| Date | Pillar(s) run | Surfaced | Queued | Dropped (duplicate) | Flagged (ambiguous) | Strategic priorities supplied |
|---|---|---|---|---|---|---|
| 2026-07-03 | Online Income for Beginners | 6 (from 8 seeds — 1 seed merged into a queued candidate as supporting evidence, 1 seed dropped pre-clustering for insufficient signal: "passive income ideas for beginners" showed near-total zero interest on Google Trends with no distinct community or gap evidence gathered, and was not carried forward as a standalone candidate) | 6 | 0 | 0 | No |
| 2026-07-03 | Online Income for Beginners (re-run: rescored under v0.4 — DataForSEO removed as a required dependency and as a scored dimension) | 6 (same candidates, no new discovery) | 6 | 0 | 0 | No |
| 2026-07-03 | OLSP Ecosystem | 9 (from 10 seeds — "OLSP Academy alternatives" and "OLSP Academy vs Wealthy Affiliate vs Legendary Marketer" clustered as 2 separate raw candidates before Stage D2; "is OLSP Academy legit" and "OLSP Academy complaints" seeds merged into one candidate at clustering since their community evidence overlapped substantially) | 7 | 2 (both matched the existing roundup `best-affiliate-marketing-training-platforms-2026`, which already compares OLSP Academy against Wealthy Affiliate, Legendary Marketer, and Spark) | 0 | No |
| 2026-07-03 | Affiliate Traffic & List Building | 8 (from 10 seeds — "build email list with no website" merged into `build-email-list-affiliate-marketing-no-website` as corroborating evidence; "traffic rotator service" (general trust framing) merged into `megalink-traffic-rotator-alternatives-comparison` as corroborating evidence rather than standing as separate candidates) | 5 | 3 (`are-solo-ads-worth-it-for-affiliate-marketing` matched `lead-generation-strategies.astro`'s dedicated "Strategy 5: Paid Email Traffic (Solo Ads & Traffic Rotators)" section, which already links to the OLSP Solo Ads and Megalink Traffic Rotator reviews; `best-autoresponder-for-affiliate-marketing` matched `best-lead-generation-tools.astro`'s existing GetResponse/AWeber/MailerLite/ConvertKit comparison framed specifically for affiliate marketers; `landing-page-builder-for-affiliate-marketing` (TD Pages alternatives) matched the same article's existing Systeme.io/Carrd/TD Pages landing-page comparison) | 0 | No |
| 2026-07-03 | Lead Generation | 12 (from 12 seeds derived from `CONTENT-REGISTRY.md` § Content Pillars Pillar 3 description and its Content Gaps note 5 explicit steer toward "email lead generation or paid traffic for affiliate marketers"; each seed clustered 1:1 into a named candidate — no merges) | 5 | 6 (`paid-traffic-for-lead-generation` matched `lead-generation-strategies.astro`'s dedicated "Strategy 3 — Paid email traffic" section and is also adjacent to the already-queued Affiliate Traffic & List Building candidate `best-free-traffic-sources-affiliate-marketing` (rank 15); `lead-magnet-ideas-and-templates` matched `lead-generation-for-beginners.astro`'s dedicated "Component 1 — The lead magnet" section (5 named formats); `lead-scoring-and-qualification` matched `b2b-lead-generation.astro`'s "Qualify" process stage and `sales-lead-generation.astro`'s dedicated "Qualification & Lead Scoring" section; `lead-nurturing-email-sequences` matched `lead-generation-for-beginners.astro`'s dedicated "Set up your first nurture sequence" section, `b2b-lead-generation.astro`'s "Nurture" process stage, and `lead-generation-strategies.astro`'s "Strategy 6 — Email list nurture and reactivation"; `lead-generation-kpis-and-metrics` matched `sales-lead-generation.astro`'s dedicated "Measuring Sales Lead Generation Performance" section (8-row metrics table); `lead-generation-mistakes-to-avoid` matched the "Common Mistakes" sections present in `lead-generation-for-beginners.astro` (5 named mistakes), `b2b-lead-generation.astro`, `best-lead-generation-tools.astro`, `lead-generation-strategies.astro`, `local-business-lead-generation.astro`, and `what-is-lead-generation.astro`) | 1 (`webinar-lead-generation` — webinars already carry real CPL/lead-quality statistics in `b2b-lead-generation.astro` and `sales-lead-generation.astro`, but no page gives step-by-step tactical how-to guidance on planning, hosting, and following up on a lead-generating webinar the way `social-media-lead-generation.astro` and `local-business-lead-generation.astro` are each given a dedicated channel guide; genuinely unclear whether this is a new angle or a duplicate of existing statistical coverage — left for operator judgement) | No |

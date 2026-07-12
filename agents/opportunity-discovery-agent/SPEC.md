# Opportunity Discovery Agent — Functional Specification

**Version:** 0.8
**Status:** Question-first — every opportunity starts with a real user question from Community Intelligence, never a keyword or product name (see § 1, § 4 D0, § 7); 5-field output requirement added (see § 7)

---

## 1. Mission

### What problem does it solve?

This site exists to solve real user problems in the affiliate marketing and online income space — not to promote products. Every article starts with a question someone asked on Reddit, Quora, a forum, or Google. OLSP is never the topic. It is the natural next step only when it genuinely helps solve the user's problem. A keyword may support an opportunity but may never define it.

Today, the editorial pipeline is **keyword-first**: a human manually picks a keyword, and only then does the Opportunity Research Agent (ORA) validate whether it's worth writing. This specification converts it to **question-first**: Community Intelligence provides the raw user questions; the agent derives problems, then opportunities, from those questions. That manual step has three costs:

1. **It doesn't scale.** Every candidate topic depends on an operator happening to think of it.
2. **It's not evidence-based until after the fact.** ORA proves a keyword was a good pick; nothing proves it was the *best available* pick, or even a *reasonable* one, before an ORA run is spent on it.
3. **It's the only place duplicate work can slip in undetected.** ORA's Stage 0 catches a duplicate once a specific keyword is proposed, but nothing today explores a whole content pillar and asks "what are we systematically missing?"

There is a fourth cost this version adds explicit scope for: **individual opportunity quality and portfolio fit are different questions.** A candidate can be an excellent opportunity in isolation and still be the wrong thing to produce next — because the pillar is already saturated, because it does nothing for internal linking, or because it doesn't match what the Product Owner has decided matters this quarter. Nothing today separates "is this a good opportunity" from "should this be produced now."

### Why it exists

To convert the pipeline from **keyword-first** → **opportunity-first** → **problem-first**. A candidate is not worth pursuing because a keyword has search volume. It is worth pursuing because it solves a real user problem, and the evidence shows people are actively looking for that solution.

This agent produces two distinct outputs per candidate, deliberately kept separate (see Section 5):

- **Opportunity Score** — how good is this opportunity, on its own merits (trend, community signal, competitive gap; demand data included only when DataForSEO happens to be configured, and only as an evidence note, never as a scored dimension — see Section 5).
- **Priority Score** — should it be produced *now*, given everything else already published, in progress, or strategically prioritized across the whole site.

Every candidate is evaluated against the same standard: does this solve a real problem people are asking about, and can the resulting article strengthen the site's content network by linking to existing solutions? Products and tools are never the subject — they are supporting evidence for a solution.

---

## 2. Inputs

**Required:**

| Field | Type | Description |
|---|---|---|
| `pillar` | string (enum) | One of the pillars defined in `docs/CONTENT-REGISTRY.md` § Content Pillars: `OLSP Ecosystem`, `Affiliate Traffic & List Building`, `Lead Generation`, `Online Income for Beginners` — or `all` to run every pillar in sequence. |

**Optional constraints:**

| Field | Type | Default | Description |
|---|---|---|---|
| `seed_topics` | list of strings | derived from `CONTENT-REGISTRY.md` | Operator-supplied starting points within the pillar. Merged with, not a replacement for, derived seeds. |
| `language` | string | `EN` | Passed through to `dataforseo-keyword-research` and Google Trends calls. The underlying skill already auto-routes Nordic languages (Swedish, Finnish, Norwegian, Danish) to Sweden/SV — this agent inherits that behavior rather than reimplementing language logic. |
| `region` | string | `United States` | Passed through to DataForSEO's location parameter and, where geo-relevance is clear, to `mcp__claude_ai_G_Trends__get_interest_by_region`. |
| `audience_hint` | string | none | Optional operator note narrowing exploration (e.g. "beginner-focused only", "US remote workers") — advisory only, same spirit as ORA's `intent_hint`. |
| `max_candidates` | integer | 15 | Cap on new candidates queued per pillar per run, to keep the queue reviewable. |
| `strategic_priorities` | list of strings | none | Optional Product-Owner-defined priorities for this run (e.g. "favor OLSP Ecosystem hub content this quarter", "de-prioritize new Lead Generation long-tail"). Feeds Priority Scoring, Section 5. Absent by default — see Section 5 for how the agent behaves with no stated priorities. |

The pillar is the only hard requirement — everything else narrows, seeds, or weights the exploration without being required to run it.

---

## 3. Discovery Sources

Every source below is one already installed and already used by ORA, or already maintained as a repository artifact. This agent introduces no new external integration — only new invocation modes (bulk/exploratory across a pillar, instead of pinpoint against one keyword) and two new internal capabilities (`CONTENT_COVERAGE` and `PORTFOLIO_CONTEXT`, rows 5 and 6).

**Mandatory sources** (a run cannot proceed meaningfully without these; if one fails, the run continues rather than halting — see Section 4's per-stage failure handling — but the capability itself is always invoked):

| # | Source | Capability | Provider / tool | Contributes |
|---|---|---|---|---|
| 1 | **Google Trends** | `TREND_INTELLIGENCE` | `mcp__claude_ai_G_Trends__get_interest_over_time`, `get_related_topics`, `get_interest_by_region` | Trend direction, rising related topics, regional interest, per seed topic |
| 2 | **Reddit** | `COMMUNITY_INTELLIGENCE` (primary) | `reddit-public-fetch` skill | Recurring questions, pain points, sentiment, unmet demand |
| 3 | **Community discussions / Google News** (fallback chain) | `COMMUNITY_INTELLIGENCE` (fallback) | `WebSearch`/`WebFetch` (Quora, Google Discussions, YouTube) + `mcp__claude_ai_G_News__search_news` | Same signal as Reddit, when Reddit is unavailable — identical cascade order ORA already uses |
| 4 | **Competitor / content-gap research** | `COMPETITOR_GAP` | `WebSearch`/`WebFetch` | Confirms whether a candidate angle is actually absent from currently ranking pages |
| 5 | **Existing content coverage** | `CONTENT_COVERAGE` (new) | `Grep`/`Read` over repo files + this agent's own queue | Filters out anything already published, drafted, briefed, researched, or queued — see Section 6 |
| 6 | **Portfolio & strategic priorities** *(new)* | `PORTFOLIO_CONTEXT` (new) | `Read` over `docs/CONTENT-REGISTRY.md` (Content Pillars table, Internal Link Map, Content Gaps & Planning Notes) + operator-supplied `strategic_priorities` input | Pillar coverage/balance, existing authority-cluster fit, internal-linking potential, business-priority alignment — feeds Priority Scoring, Section 5 |

**Optional enrichment sources** (never required; a run is fully valid and fully scored with these absent — see Section 5 for how each plugs in without altering the workflow):

| # | Source | Capability | Provider / tool | Contributes |
|---|---|---|---|---|
| 7 | **DataForSEO** *(optional — disabled by default)* | `SEARCH_DEMAND` *(optional)* | `dataforseo-keyword-research` skill, if configured | Search demand tier, related/suggested keywords, when credentials are available. Not invoked by default; not scored even when available (Section 5). |
| 8 | **Google Search Console** *(future — not yet available)* | `GSC_INTELLIGENCE` *(planned)* | Not yet wired to any provider | Actual impressions/clicks/position data, once GSC access exists. Not invoked in this version. |

Sources 1–6 are mandatory and active in this version. Sources 7 and 8 are both optional by design — 7 because it depends on external credentials this agent does not control, 8 because no provider exists yet. Neither can ever block a run; see Section 5 for the reactivation path for source 7 and the general principle that this agent's core workflow is identical whether either is present or absent.

---

## 4. Workflow

Six stages, executed in strict sequence. Stages D1–D4 process many candidates per run (this agent explores broadly); ORA, by contrast, processes exactly one keyword per run (it researches deeply). That difference in cardinality is the core architectural distinction between the two agents.

```
Pillar (+ optional constraints)
    ↓
Stage D0: Community-Driven Seed Generation  → gather real user questions from COMMUNITY_INTELLIGENCE;
                                                derive seed questions from community signals, not
                                                from keywords or pillar names alone
    ↓
Stage D1: Multi-Source Exploration           → for each seed question, invoke TREND_INTELLIGENCE,
                                                COMPETITOR_GAP; cluster into named candidates
    ↓
Stage D2: Bulk Content-Coverage Check ────── match found ──→ DROP candidate, do not score or queue
    ↓ survivors only
Stage D2b: Editorial Relevance Filter ─────── fails check ──→ REJECT candidate, skip recommendation
    ↓ passes only
Stage D3: Opportunity Scoring                (quality of the opportunity, in isolation)
    ↓
Stage D4: Portfolio-Aware Priority Scoring   (should it be produced now, given everything else)
    ↓
Stage D5: Opportunity Queue Write            → every candidate must include all 5 required fields:
                                                User Question, User Problem, Evidence,
                                                Recommended Article, Natural Solution
```

### Stage D0 — Community-Driven Seed Generation
Invoke `COMMUNITY_INTELLIGENCE` (sources 2/3) to gather real user questions from Reddit, Quora, forums, and Google Discussions. For each question, identify the underlying user problem — what is the user trying to accomplish, avoid, or understand? Derive 5–15 seed questions from these community signals. Read the pillar's stated primary subject and existing pages from `docs/CONTENT-REGISTRY.md` for context, but never generate a seed from a keyword, pillar name, or product name alone. Merge with any operator-supplied `seed_topics`. A seed question describes a user problem (e.g. "How do I avoid common affiliate marketing mistakes as a beginner?"), not a keyword or product name.

### Stage D1 — Multi-Source Exploration
For each seed topic, invoke `TREND_INTELLIGENCE` and `COMMUNITY_INTELLIGENCE` (sources 1–3). Cluster raw results into named **candidates** — a candidate is a specific, nameable angle, not a bare seed. For each candidate, invoke `COMPETITOR_GAP` (source 4) to confirm a real gap exists. If DataForSEO (source 7) is configured, `SEARCH_DEMAND` is also attempted per seed and its result attached as an optional evidence line — its presence or absence never changes which candidates are clustered or how they proceed to Stage D2. Every candidate carries its supporting evidence forward — which source produced or confirmed it, and what it said.

### Stage D2 — Bulk Content-Coverage Check
Run `CONTENT_COVERAGE` (source 5) against every candidate from D1, before any candidate is scored. Full rules in Section 6. Candidates with no match proceed; clear matches are dropped; ambiguous matches are set aside for human judgement rather than resolved automatically in either direction.

### Stage D2b — Editorial Relevance Filter
Apply the Editorial Relevance Filter (Section 6a) to every surviving candidate. Candidates that fail either check are rejected for recommendation purposes but remain in the queue with their scores intact — the filter is a recommendation gate, not a deletion. Never stop evaluating the next candidate because one fails. Full rules in Section 6a.

### Stage D3 — Opportunity Scoring
Score each surviving candidate across three equally-weighted sub-scores (25 pts each, mandatory sources only): **Trend** (source 1), **Community** (sources 2/3), **Gap** (source 4). Sum the three (max 75) and rescale to 0–100 by multiplying by 4/3, rounding to the nearest integer. This produces the **Opportunity Score** — a measure of the candidate's quality in isolation, independent of what else exists on the site, computed identically whether or not DataForSEO happens to be configured. It is a cheap triage score, not a substitute for ORA's own (deeper, post-research) Opportunity Score — see the naming note in Section 5.

### Stage D4 — Portfolio-Aware Priority Scoring
Score each surviving candidate 0–100 across four equally-weighted sub-scores (25 pts each), using `PORTFOLIO_CONTEXT` (source 6) plus the Opportunity Score from D3: **Opportunity Quality**, **Pillar Coverage & Balance**, **Authority Cluster & Internal-Linking Fit**, **Strategic/Business Priority Fit**. This produces the **Priority Score** — full model in Section 5.

### Stage D5 — Opportunity Queue Write
Append surviving, scored candidates to `OPPORTUNITY-QUEUE.md`, sorted by **Priority Score** within pillar (not Opportunity Score — see Section 5 for why). Update the `status` of any existing row that changed (e.g. an operator promoted it to ORA since the last run) rather than duplicating it. Report a run summary: candidates surfaced vs. queued vs. dropped (duplicate) vs. flagged (ambiguous), and the top 3 by Priority Score.

---

## 5. Portfolio Awareness & Priority Scoring

This is the one genuinely new responsibility added in this version. Everything else in this specification was either already true of ORA (reused capability providers) or a direct restatement of duplicate-suppression discipline already approved for ORA's Stage 0. Portfolio awareness has no ORA equivalent — ORA evaluates one keyword with no knowledge of the rest of the site's portfolio, and that remains true; this agent is where portfolio-level judgement belongs instead.

### Two separate concepts — kept separate throughout

| Concept | Question it answers | Computed at | Inputs |
|---|---|---|---|
| **Opportunity Score** | Is this a good opportunity, on its own merits? | Stage D3 | Trend, Community, Gap (sources 1, 2/3, 4) — rescaled to 0–100 |
| **Priority Score** | Should this be produced *now*, relative to everything else? | Stage D4 | Opportunity Score, plus pillar coverage, authority clusters, internal linking, strategic priorities (source 6) |

A candidate can score High on Opportunity and Low on Priority (a genuinely strong topic, but the pillar is already saturated with similar coverage, or the Product Owner has deprioritized this pillar this quarter). The reverse can also happen (a moderate opportunity that resolves a known structural gap — e.g. the missing OLSP Ecosystem hub page identified in `CONTENT-REGISTRY.md`'s own Content Gaps notes — may deserve high priority precisely because of that gap). The queue must preserve both numbers and never collapse them into one.

**Naming note:** ORA already has a field called "Opportunity Score," computed after ORA's full six-stage research (Volume/Competition/Gap/Alignment). This agent's Opportunity Score (Trend/Community/Gap) is the same concept at an earlier, cheaper confidence level — a preliminary read, not a competing definition. Where the distinction needs to be explicit (e.g. in the queue, or in any document read by someone unfamiliar with both agents), this agent's score should be labeled **"Opportunity Score (preliminary)"**, and is understood to be superseded by ORA's own Opportunity Score once a candidate is promoted and researched — the same "estimated → confirmed" pattern ORA already uses internally for its own proxy-scoring rules.

**DataForSEO is not part of this score.** Earlier drafts of this specification included a fourth, equally-weighted Demand dimension sourced from DataForSEO. That dependency has been removed: DataForSEO requires external credentials this agent does not control, and a discovery run must never be blocked, degraded in reliability, or made to silently under-score candidates because those credentials are missing, expired, or rate-limited. The Opportunity Score is now computed from three mandatory sources only (Trend, Community, Gap — Section 4, Stage D3), each still built entirely from capabilities already installed and already used by ORA.

### Priority Score model

Four equally-weighted sub-scores (25 pts each), 0–100 total:

| Sub-score | Signal | 25 pts | 15 pts | 5 pts |
|---|---|---|---|---|
| **Opportunity Quality** | This candidate's Opportunity Score from Stage D3 | ≥ 70 | 40–69 | < 40 |
| **Pillar Coverage & Balance** | Relative page count and stated scope per pillar, from `CONTENT-REGISTRY.md` § Content Pillars | Pillar is thin / under-served relative to its ambition or the other pillars | Roughly balanced | Pillar already well-covered or saturated |
| **Authority Cluster & Internal-Linking Fit** | Whether the candidate would strengthen an existing cluster or resolve a known structural gap, from `CONTENT-REGISTRY.md` § Internal Link Map and § Content Gaps & Planning Notes | Directly resolves a documented gap (e.g. an orphaned cluster, a missing pillar hub, a one-directional link pattern) | Neutral — fits a cluster but doesn't resolve a known issue | Would create an isolated page with no clear linking path in or out |
| **Strategic / Business Priority Fit** | Match against operator-supplied `strategic_priorities` (Section 2) | Explicitly matches a stated priority | No priorities stated for this run (neutral default — absence of a stated priority is never treated as a penalty) | Explicitly conflicts with, or is named as deprioritized by, a stated priority |

**Why "no priorities stated" defaults to 15, not 5:** the Product Owner will not always populate `strategic_priorities` for every run. Silence must not read as deprioritization — only an explicit statement should move this sub-score away from neutral, in either direction.

**Priority labels** (kept visually and terminologically distinct from Stage D3's Opportunity Score labels, to avoid the two being confused when scanning the queue):

| Score | Label |
|---|---|
| 70–100 | Produce soon |
| 40–69 | Hold — reasonable, not urgent |
| 0–39 | Defer |

### Data sources reused, not newly built

- **Pillar Coverage & Balance** and **Authority Cluster & Internal-Linking Fit** are both computed from `docs/CONTENT-REGISTRY.md`, which this agent already reads in Stage D0. No new document needs to be created for this version — the Content Pillars table and the existing Content Gaps & Planning Notes section (which already documents things like the isolated review cluster and the missing OLSP Ecosystem hub page) are sufficient inputs today.
- **Strategic / Business Priority Fit** is the one input this specification does not assume a standing repository artifact for. It is satisfied by the optional `strategic_priorities` operator input (Section 2) for this version. A future, more durable version could formalize this as a Product-Owner-maintained document (analogous to how `CONTENT-REGISTRY.md` is the standing source of truth for published content) — noted as a future extension, not a precondition for approval.

### DataForSEO reactivation path

DataForSEO (`SEARCH_DEMAND`, Section 3 row 7) is designed to be turned back on without any change to the workflow above:

1. **While disabled or unconfigured (default):** Stage D1 never attempts the call. No evidence field references it. The Opportunity Score model (Stage D3) has no Demand dimension to fail, degrade, or floor — there is nothing for its absence to affect.
2. **If credentials become available:** Stage D1 attempts `SEARCH_DEMAND` per seed and its result is attached to each candidate's Evidence section as a labeled, informational line (e.g. "Demand (optional enrichment): ..."). This is visible to the operator but does **not** enter the Opportunity Score formula — the three-dimension model in Stage D3 does not change automatically just because data becomes available.
3. **Reintroducing Demand as a scored, weighted dimension** (restoring something like the original four-dimension model) is a deliberate specification change requiring its own version bump and explicit approval, exactly like any other change to the scoring model. It does not happen implicitly just because the underlying credentials start working again.

This keeps the guarantee absolute: a discovery run's behavior, output shape, and scoring never depend on whether an external, operator-managed credential happens to be valid on a given day.

---

## 5a. Authority Value (editorial planning field — never scored)

**Added in v0.5.** A third, deliberately separate concept, sitting alongside Opportunity Score and Priority Score without feeding either:

| Concept | Question it answers | Computed at | Feeds into a 0–100 score? |
|---|---|---|---|
| Opportunity Score | Is this a good opportunity, on its own merits? | Stage D3 | Yes |
| Priority Score | Should this be produced *now*, relative to everything else? | Stage D4 | Yes |
| **Authority Value** | **If produced, how much does it strengthen the site's long-term topical authority and internal-linking structure?** | **Stage D4, alongside Priority Scoring** | **No — qualitative only** |

Authority Value is a **long-horizon, architectural** judgement — "what kind of page would this become" — distinct from the Priority Score's **Authority Cluster & Internal-Linking Fit** sub-score, which asks the narrower, tactical question "does this resolve a specific documented gap right now." A candidate can score moderately on that tactical sub-score while still being the kind of page (a hub, a cross-cluster synthesis) that matters more once written than its Priority Score alone implies — Authority Value exists to carry that judgement forward without distorting either 0–100 score.

**Scale (qualitative, not numeric):**

| Rating | Meaning |
|---|---|
| ⭐⭐⭐⭐⭐ | Foundational / Pillar / Cluster Hub — would function as the hub tying together an existing cluster of already-published pages |
| ⭐⭐⭐⭐ | Strong supporting page — directly resolves a documented structural gap (orphaned page, isolated cluster) |
| ⭐⭐⭐ | Useful supporting content — neutral cluster fit; links in and out but resolves no documented gap |
| ⭐⭐ | Standalone article — would be published with a weak or no clear internal-linking path |
| ⭐ | Limited authority impact — isolated, no meaningful linking path in or out |

**Rules:**
- Authority Value **never** modifies the Opportunity Score (Stage D3) or the Priority Score (Stage D4). It is recorded alongside them, never averaged or combined into either.
- It is assigned using the same evidence already gathered for the Priority Score's Authority Cluster & Internal-Linking Fit sub-score (`PORTFOLIO_CONTEXT`, source 6) — no new discovery source or tool call is required.
- It is an editorial planning signal only: it informs which `unclaimed` row an operator chooses to promote next when Priority Scores are tied or close, and it informs future internal-linking strategy once a candidate is written. It is never used to reorder the summary table (which remains sorted by Priority Score) and never substitutes for either score in Stage D5's queue write.

---

## 5b. Pipeline Type (editorial routing field — never scored)

**Added in v0.6.** A fourth field, sitting alongside Opportunity Score, Priority Score, and Authority Value without feeding any of them. Where those three answer "is this good," "is this urgent," and "how much authority would it build," Pipeline Type answers a different question entirely: **which downstream production pipeline should this candidate enter if promoted?**

Production now splits into two independent tracks after Discovery:

- **Heavy Pipeline** — Opportunity → Research Compiler → Research Brief (cataloged as a reusable Knowledge Asset in `docs/HEAVY-ASSET-LIBRARY.md`) → (optional) Editorial Builder. For candidates whose core subject is a reusable, long-lived editorial asset.
- **Light Pipeline** — Opportunity → ORA (Light Research) → Writer → QA → Publish. For candidates that are single-article-scoped and don't need a standing research asset.

See `docs/PIPELINE-ARCHITECTURE.md` for the full end-to-end diagram of both tracks.

**Classification rule** (assigned at Stage D4, from the candidate's own subject — no new discovery source or tool call required):

| Pipeline Type | Applies to |
|---|---|
| **Heavy** | Companies, Products, Platforms, Services, Founders, Tools, Pillar Pages, Major Comparisons — i.e. the candidate's core subject *is* a specific named entity (e.g. "OLSP Academy," "Wayne Crowe," "Megalink Traffic Rotator") or a synthesis/comparison across several such entities |
| **Light** | Information Articles, How-To Articles, FAQ, Beginner Guides, Problem-Solving, General Opportunity Articles — i.e. the candidate is a general topic or audience-scoped guide that does not center on one specific named entity |

**Worked examples from the current queue:** `wayne-crowe-founder-background` (Founder) and `megalink-traffic-rotator-alternatives-comparison` (Major Comparison anchored to a named Product) are Heavy. `make-money-online-no-money-to-start` and `real-estate-lead-generation` (general audience/topic guides, no single named product at their center) are Light. A candidate that merely *mentions* a reviewed product in passing (e.g. `build-email-list-affiliate-marketing-no-website`, which cites LeadsMiner Pro as a supporting tactic) stays Light — the test is whether the product/company/founder/platform is the subject, not whether it's cited.

**Rules:**
- Pipeline Type **never** modifies the Opportunity Score, Priority Score, or Authority Value, and none of those ever modify it. It is recorded alongside them, never averaged or combined into any of them.
- It never changes the summary table's sort order (which remains sorted by Priority Score).
- It is assigned once, at Stage D4, and does not change after promotion — if research later reveals a Light candidate is actually product-centric, that is a Research Compiler / ORA judgement call to escalate, not a retroactive edit to this field.
- Heavy-classified candidates route to the Research Compiler (`agents/research-compiler/`) when promoted, **not** to ORA. Light-classified candidates route to ORA (`agents/opportunity-research-agent/`), now scoped as the Light Pipeline's research stage. See `docs/PIPELINE-ARCHITECTURE.md`.

---

## 6. Duplicate Prevention

The agent must never suggest, and never queue, a topic that is already published, already in production, already covered by manually written content, already the subject of an existing Opportunity Brief, or already the subject of an existing Research Brief. This runs as Stage D2, once per candidate, before either scoring stage — a duplicate is never allowed to consume Stage D3, D4, or D5 effort.

| Case | How it's caught | Where checked |
|---|---|---|
| **Already published** | Match against title, primary keyword, or URL slug | `docs/CONTENT-REGISTRY.md` |
| **Already in production** (drafted, not yet in the registry) | Match against filename slug | `src/pages/{reviews,blog,roundups}/**/*.astro` |
| **Already covered by manually written content** | Same check as "published" — the check is content-based, not authorship-based. A manually written page is caught exactly the same way an AI-produced one is, because both live in the same registry and page tree. No separate "manual content" path exists or is needed. | `docs/CONTENT-REGISTRY.md` + `src/pages/**` |
| **Duplicate Opportunity Brief** | Match against slug or `Primary keyword` field | `agents/opportunity-research-agent/briefs/` |
| **Duplicate Research Brief** | Match against topic | `docs/research/` |
| **Already in the Opportunity Queue** *(new — no ORA equivalent, since the queue is new)* | Match against existing `unclaimed`/`promoted`/`published` rows; `rejected`/`stale` rows do not block a re-surface | `agents/opportunity-discovery-agent/OPPORTUNITY-QUEUE.md` |

**Judgement standard:** a trivial variant — singular/plural, reordered words, "best X" vs. "top X" for the same topic — counts as already covered. This is the same standard already defined and approved in ORA's Stage 0. When genuinely uncertain whether a candidate is a new angle or a duplicate, the candidate is neither dropped nor queued — it is reported separately as needing human judgement.

**Conservatism exception:** if the coverage check itself cannot read one of its sources (file missing, unreadable), the candidate is **not** queued. Every other stage in this agent continues on partial data when a source fails; this is the one stage where failure means "don't queue," because its entire purpose is duplicate suppression and a false negative here directly causes wasted ORA runs or duplicate content.

---

## 6a. Editorial Relevance Filter

**Added in v0.7.** A mandatory pre-scoring check applied to every candidate that survives Stage D2. The filter ensures the Opportunity Queue only contains topics that belong on OLSP.PROFITANDPRIVILEGE.COM — topics that solve real problems and strengthen the existing content network.

### Checks

Every candidate must pass BOTH checks before entering Stage D3:

**Check 1 — Real Problem Evidence:**
Does the topic solve a real problem that people are actively discussing? At least one of these sources must provide evidence:
- Reddit (recurring questions, pain points, confusion)
- Quora (posted questions with engagement)
- Forums and community discussions
- Google search demand
- Verified social/community signals

Evidence is drawn from the candidate's `Rationale` field, which must cite at least one real-world signal source. Topics surfaced only by trend data or competitive gap analysis, without community evidence, do not pass this check.

**Check 2 — Content Network Strength:**
Can the finished article naturally strengthen the existing OLSP content network? The candidate's `Internal link potential` field must reference at least one specific existing page or content cluster on the site. Candidates with no clear internal-linking path do not pass this check.

### Behaviour on failure

- If either check fails, the candidate is **rejected** for the purpose of the "next recommended" selection.
- The rejected candidate remains in the queue (its scores are still valid — the filter is a recommendation gate, not a deletion).
- The next candidate is evaluated automatically.
- **Never stop production because one opportunity fails.** Continue evaluating the next opportunity.

### Relationship to other stages

| Stage | Relationship |
|---|---|
| Stage D2 (Duplicate Prevention) | Runs first — removes duplicates. Survivors enter this filter. |
| Stage D2b (Editorial Relevance Filter) | Applies the two checks above. Pass → continue to scoring. Fail → mark as rejected, do not advance. |
| Stage D3 (Opportunity Scoring) | Receives only candidates that passed both checks. |
| Stage D4 (Priority Scoring) | Receives only candidates that passed all prior stages. |
| Stage D5 (Queue Write) | Writes all surviving candidates. Rejected candidates remain in the queue with a note but are skipped by the "next recommended" selector. |

### Distinction from the existing OLSP product filter

This filter is NOT an OLSP product filter. It does not require that a candidate directly promote OLSP. The test is whether the topic:

1. Solves a real user problem (evidence-based)
2. Creates natural internal-linking value for the existing content network

OLSP becomes the natural next step where appropriate — not a requirement.

---

## 7. Outputs

### Opportunity Queue (owned entirely by this agent)

**File:** `agents/opportunity-discovery-agent/OPPORTUNITY-QUEUE.md`
One file, updated (not replaced) on every run, all pillars together, ranked by **Priority Score** within each pillar.

**Every candidate detail block must include all five required output fields:**

| Field | Type | Description |
|---|---|---|
| **User Question** | string | The exact question a real person asked — quoted from the community source. This is the origin of the opportunity. |
| **User Problem** | string | The underlying problem the question reveals — what the user is trying to accomplish, avoid, or understand. |
| **Evidence** | string | Where this question was found: source, frequency, context, thread engagement. |
| **Recommended Article** | string | What the article should be about — a solution description, never a product name. A keyword may appear as supporting detail but may never be the defining field. |
| **Natural Solution** | string | How the article solves the problem and what makes it authoritative. Tools, platforms, or training may be mentioned as part of the solution but are never the subject. |

A keyword may support the opportunity but may never define it. The User Question field is the primary identifier of the opportunity — not the Candidate ID, not a keyword, not a product name.

```
pillar:                    [pillar name]
candidate_id:              [kebab-case slug — becomes the ORA candidate_keyword if promoted]
opportunity_summary:       [1–2 sentence description of the angle/gap/question — not just a keyword]
candidate_keyword:         [the keyword/phrase to hand to ORA if promoted]

opportunity_score:         [0–100 — preliminary; see Section 5 naming note]
opportunity_breakdown:     [trend / community / gap sub-scores, each with rationale + source, rescaled to 0-100]

priority_score:            [0–100]
priority_label:            [Produce soon / Hold — reasonable, not urgent / Defer]
priority_breakdown:        [opportunity-quality / pillar-coverage / authority-cluster / strategic-fit
                             sub-scores, each with rationale + source]

authority_value:           [⭐ / ⭐⭐ / ⭐⭐⭐ / ⭐⭐⭐⭐ / ⭐⭐⭐⭐⭐ — editorial planning field, see Section 5a.
                             Never scored, never feeds opportunity_score or priority_score.]
authority_value_rationale: [1 line — why this rating, citing the same Authority Cluster & Internal-
                             Linking Fit evidence used in priority_breakdown]

pipeline_type:             [Heavy / Light — editorial routing field, see Section 5b. Never scored,
                             never feeds opportunity_score or priority_score, never changes sort order.]
pipeline_type_rationale:   [1 line — why this candidate's core subject does or doesn't center on a
                             specific named company/product/platform/service/founder/tool]

evidence:                  [what each discovery source returned, or "Unavailable — reason"]
coverage_check:            [match_status: None, confirmed at Stage D2, with date and sources checked]
status:                    [unclaimed / promoted / rejected / stale / published]
promoted_brief_path:       [path to the Opportunity Brief once promoted / N/A]
date_discovered:           [YYYY-MM-DD]
date_status_changed:       [YYYY-MM-DD]
```

Full blank structure (summary table + per-candidate detail block + run log) is defined in `OUTPUT-TEMPLATE.md`.

### Opportunity Brief (existing — owned entirely by ORA, unchanged)

This agent does not define, produce, or modify the Opportunity Brief. It is included here only to make the handoff explicit: ORA's existing schema (`agents/opportunity-research-agent/OUTPUT-TEMPLATE.md`, unchanged) is what a promoted queue candidate eventually becomes, once ORA runs its own six-stage research on it. ORA's Opportunity Score, computed post-research, is the confirmed successor to this agent's preliminary Opportunity Score — not a second, unrelated metric. The mapping from queue row to ORA input is:

| Queue field | ORA input field |
|---|---|
| `candidate_keyword` | `keyword` (required) |
| `opportunity_summary` | `intent_hint` (optional — operator's discretion whether to pass it) |
| — (not carried over) | `affiliate_product` (defaults to OLSP Academy in ORA, same as today) |

Nothing about ORA's Opportunity Brief schema, scoring model, or stage sequence changes as a result of this agent existing. Note that it is the **Priority Score**, not the Opportunity Score alone, that should guide which `unclaimed` row an operator promotes next — a high-Opportunity, low-Priority candidate is deliberately ranked below a moderate-Opportunity, high-Priority one in the queue.

---

## 8. Integration — exact handoff to ORA

This agent and ORA are connected by **one manual step**, not by any code or shared state: an operator reads a queue row and pastes its `candidate_keyword` into ORA's existing, unmodified user prompt template.

**Concrete example.** Suppose Stage D5 writes this row:

```
candidate_id:        olsp-academy-refund-policy-explained
candidate_keyword:   does olsp academy have a refund policy
opportunity_summary: Reddit and Quora threads show recurring uncertainty about whether
                      OLSP Academy offers refunds; no ranking page directly answers it.
opportunity_score:   78
priority_score:      82   (boosted: resolves a documented gap — no FAQ/policy page exists
                           in the OLSP Ecosystem cluster; matches stated strategic priority
                           "reduce OLSP Academy purchase-hesitation content this quarter")
priority_label:      Produce soon
status:              unclaimed
```

The operator then invokes ORA exactly as they do today, using ORA's own `PROMPT.md` user template verbatim — nothing added, nothing new:

```
Research this keyword for a publishing opportunity:

Keyword: does olsp academy have a refund policy

Intent hint (optional): Reddit and Quora threads show recurring uncertainty about
whether OLSP Academy offers refunds; no ranking page directly answers it.
Affiliate product (optional): OLSP Academy (default)

Run all six stages of the Opportunity Research workflow as defined in your system prompt...
```

ORA has no way to distinguish this from a keyword an operator thought of unaided — because it isn't given one. **This is the entire integration.** After the operator submits this prompt, this agent updates the queue row's `status` to `promoted` and fills `promoted_brief_path` once ORA's brief exists, at the start of the *next* Discovery run (via the same coverage check that already reads `agents/opportunity-research-agent/briefs/`) — not synchronously, since this agent never invokes ORA itself.

**What this guarantees:**
- Zero changes to ORA's input contract, prompt, stages, or schema.
- Zero shared code, shared state, or runtime coupling between the two agents.
- The pipeline stays inspectable: an operator can run ORA standalone on a manually chosen keyword at any time, exactly as before — this agent is additive, not a required gate.

---

## 9. Repository Structure

**Recommendation:** a sibling folder to ORA, at the same nesting level, mirroring its internal layout exactly.

```
agents/
  opportunity-discovery-agent/     ← NEW
    README.md                     ← overview and quick reference
    SPEC.md                       ← this document
    PROMPT.md                     ← system prompt and user prompt template
    OUTPUT-TEMPLATE.md            ← blank Opportunity Queue structure
    OPPORTUNITY-QUEUE.md          ← output — created on first run
  opportunity-research-agent/      ← UNCHANGED
    README.md
    SPEC.md
    PROMPT.md
    OUTPUT-TEMPLATE.md
    briefs/
      [slug].md
```

**Rationale:**
- **Mirrors ORA's own convention** (`README`/`SPEC`/`PROMPT`/`OUTPUT-TEMPLATE` + one write-target subfolder), so anyone who already understands ORA's layout understands this agent's layout for free.
- **No shared code exists to factor out.** Both agents are prompt-driven specifications, not a shared library — there is nothing to place in a common parent beyond the `agents/` folder they already share.
- **Isolates the write target.** Exactly as `briefs/` is ORA's only write target, `OPPORTUNITY-QUEUE.md` is this agent's only write target. Neither agent's folder is ever written to by the other.
- **No changes required inside `opportunity-research-agent/`.** Placing the new agent as a sibling, rather than nesting it under or inside ORA's folder, keeps that guarantee structurally obvious rather than just documented.

One follow-up noted but explicitly not actioned in this spec: the duplicate-check rules in Section 6 are substantively identical to ORA's Stage 0. Extracting them into one shared reference doc (e.g. `docs/DUPLICATE-CHECK-STANDARD.md`) that both `SPEC.md` files point to would prevent drift, but is a mechanical follow-up, not a precondition for approving this specification. A second, related follow-up: formalizing `strategic_priorities` (Section 5) as a standing Product-Owner-maintained document rather than a per-run operator input, once the informal version proves useful.

---

## Approval

This document defines the complete functional specification for the Opportunity Discovery Agent, including portfolio-aware Priority Scoring as a distinct responsibility from Opportunity Scoring, DataForSEO as a strictly optional enrichment source that can never block or degrade a run, Authority Value (§ 5a) as a third, editorial-only planning field that never feeds either 0–100 score, and Pipeline Type (§ 5b) as a fourth, editorial-only routing field that determines whether a promoted candidate enters the Heavy or Light production pipeline. **Approved.** `README.md`, `PROMPT.md`, and `OUTPUT-TEMPLATE.md` have been implemented to match this specification (version 0.6, six-stage D0–D5 workflow, dual Opportunity/Priority scoring computed from mandatory sources only, plus the Authority Value and Pipeline Type fields). A first dry run was executed against the Online Income for Beginners pillar under the prior (v0.3, DataForSEO-dependent) model and has been re-run under this version to confirm identical stage behavior with DataForSEO absent by design rather than by failure. Pipeline Type was backfilled for all 23 existing queue candidates from their already-recorded subject matter — no candidate was re-scored or re-discovered (see `OPPORTUNITY-QUEUE.md`).

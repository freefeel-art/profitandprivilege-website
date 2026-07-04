# Opportunity Queue — [PILLAR or "All Pillars"]

**Schema version:** 0.6
**Last updated:** [YYYY-MM-DD]
**Last run:** [pillar(s) run, e.g. "Online Income for Beginners"]

This file is the live, ranked backlog produced by the Opportunity Discovery Agent. It is updated, not replaced, on every run — new candidates are appended, existing rows have their `status` updated in place. Every field is required; unavailable data is recorded explicitly as `Unavailable`, never left blank.

Every candidate carries **four separate fields** — they are never averaged or collapsed into one another:
- **Opportunity Score (preliminary)** — is this a good opportunity, on its own merits? (Trend / Community / Gap, rescaled to 0–100 — Demand/DataForSEO is optional and never scored; see Evidence below)
- **Priority Score** — should it be produced *now*, given the rest of the portfolio? (Opportunity Quality / Pillar Coverage & Balance / Authority Cluster & Internal-Linking Fit / Strategic Priority Fit)
- **Authority Value** — *editorial planning only, see SPEC.md § 5a* — if produced, how much would it strengthen the site's long-term topical authority and internal-linking structure (⭐ to ⭐⭐⭐⭐⭐)? Never a scored input to either number above.
- **Pipeline Type** — *editorial routing only, see SPEC.md § 5b* — Heavy or Light: which downstream production pipeline (see `docs/PIPELINE-ARCHITECTURE.md`) does this candidate enter if promoted? Never a scored input, never changes sort order.

The summary table below is sorted by **Priority Score**, not Opportunity Score — a high-quality opportunity in a saturated pillar can rank below a moderate one that resolves a documented structural gap.

---

## Summary Table

Sorted by Priority Score descending, grouped by pillar. Use the detail blocks below for evidence before promoting anything.

| Rank | Candidate ID | Pillar | Priority Score | Priority Label | Opportunity Score | Authority Value | Pipeline Type | Status | Date Discovered |
|---|---|---|---|---|---|---|---|---|---|
| 1 | [kebab-case-slug] | [pillar name] | [0–100] | [Produce soon / Hold — reasonable, not urgent / Defer] | [0–100] | [⭐–⭐⭐⭐⭐⭐] | [Heavy / Light] | [unclaimed / promoted / rejected / stale / published] | [YYYY-MM-DD] |
| 2 | [kebab-case-slug] | [pillar name] | [0–100] | [Produce soon / Hold — reasonable, not urgent / Defer] | [0–100] | [⭐–⭐⭐⭐⭐⭐] | [Heavy / Light] | [unclaimed / promoted / rejected / stale / published] | [YYYY-MM-DD] |

---

## Candidate Detail Blocks

One block per candidate in the summary table above, in the same rank order. `candidate_id` anchors the block to its summary row.

### [candidate_id]

| Field | Value |
|---|---|
| Pillar | [OLSP Ecosystem / Affiliate Traffic & List Building / Lead Generation / Online Income for Beginners] |
| Opportunity summary | [1–2 sentence description of the angle/gap/question — not just a keyword] |
| Candidate keyword | [the exact keyword/phrase to hand to ORA if promoted] |
| Authority Value | [⭐ / ⭐⭐ / ⭐⭐⭐ / ⭐⭐⭐⭐ / ⭐⭐⭐⭐⭐ — [1-line rationale, see SPEC.md § 5a; never affects Opportunity or Priority Score] |
| Pipeline Type | [Heavy / Light — 1-line rationale, see SPEC.md § 5b; never affects Opportunity or Priority Score] |
| Status | [unclaimed / promoted / rejected / stale / published] |
| Date discovered | [YYYY-MM-DD] |
| Date status changed | [YYYY-MM-DD] |
| Promoted brief path | [path to Opportunity Brief, once promoted / N/A] |

#### Opportunity Score (preliminary) — is this a good opportunity?

| Dimension | Raw score (0–25) | Rationale |
|---|---|---|
| Trend | [0–25] | [one-line rationale citing the TREND_INTELLIGENCE signal] |
| Community | [0–25] | [one-line rationale citing the COMMUNITY_INTELLIGENCE signal] |
| Gap | [0–25] | [one-line rationale citing the COMPETITOR_GAP signal] |
| Raw total (max 75) | [0–75] | Sum of the three rows above |
| **Opportunity Score** | **[0–100]** | Raw total × 4/3, rounded. Preliminary — not ORA's Opportunity Score; superseded once promoted and researched. DataForSEO/Demand plays no part in this score even when available (see Evidence). |

#### Priority Score — should this be produced now?

| Dimension | Score | Rationale |
|---|---|---|
| Opportunity Quality | [0–25] | [derived directly from the Opportunity Score above] |
| Pillar Coverage & Balance | [0–25] | [one-line rationale citing CONTENT-REGISTRY.md § Content Pillars] |
| Authority Cluster & Internal-Linking Fit | [0–25] | [one-line rationale citing CONTENT-REGISTRY.md § Internal Link Map / § Content Gaps & Planning Notes] |
| Strategic / Business Priority Fit | [0–25] | [one-line rationale — cite the matched strategic_priorities entry, or "not stated — neutral default (15)"] |
| **Priority Score** | **[0–100]** | |
| **Priority Label** | **[Produce soon / Hold — reasonable, not urgent / Defer]** | |

#### Evidence

- **Demand (optional enrichment, not scored):** [what SEARCH_DEMAND/DataForSEO returned, if configured — demand tier, related terms — or "Not configured this run — optional source, no impact on scoring"]
- **Trend:** [what TREND_INTELLIGENCE returned — direction, rising topics — or "Unavailable — [reason]"]
- **Community:** [what COMMUNITY_INTELLIGENCE returned — which provider, what it found — or "Unavailable — [reason]"]
- **Competitor gap:** [what COMPETITOR_GAP confirmed — the specific angle missing from ranking pages — or "Unavailable — unconfirmed, capped at 5 pts"]
- **Portfolio context:** [what PORTFOLIO_CONTEXT found — pillar page count/balance, any documented gap this candidate resolves, whether strategic_priorities were supplied for this run]

#### Coverage check

| Field | Value |
|---|---|
| Match status | [None / Clear match / Ambiguous] |
| Sources checked | docs/CONTENT-REGISTRY.md, src/pages/{reviews,blog,roundups}/**, agents/opportunity-research-agent/briefs/, docs/research/, OPPORTUNITY-QUEUE.md |
| Matched artifact | [path or identifier, or N/A] |
| Reasoning | [one line — why this counts as clear, no match, or ambiguous] |
| Checked on | [YYYY-MM-DD] |

---

## Run Log

Appended after every Discovery run — a running history, oldest first, not replaced.

| Date | Pillar(s) run | Surfaced | Queued | Dropped (duplicate) | Flagged (ambiguous) | Strategic priorities supplied |
|---|---|---|---|---|---|---|
| [YYYY-MM-DD] | [pillar(s)] | [count] | [count] | [count] | [count] | [Yes — summary / No] |

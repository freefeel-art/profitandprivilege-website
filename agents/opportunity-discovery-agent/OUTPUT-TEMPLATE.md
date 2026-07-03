# Opportunity Queue — [PILLAR or "All Pillars"]

**Schema version:** 0.1
**Last updated:** [YYYY-MM-DD]
**Last run:** [pillar(s) run, e.g. "Online Income for Beginners"]

This file is the live, ranked backlog produced by the Opportunity Discovery Agent. It is updated, not replaced, on every run — new candidates are appended, existing rows have their `status` updated in place. Every field is required; unavailable data is recorded explicitly as `Unavailable`, never left blank.

---

## Summary Table

Sorted by Discovery Score descending, grouped by pillar. This table is the 30-second scan — use the detail blocks below for evidence before promoting anything.

| Rank | Candidate ID | Pillar | Discovery Score | Priority | Status | Date Discovered |
|---|---|---|---|---|---|---|
| 1 | [kebab-case-slug] | [pillar name] | [0–100] | [High / Medium / Low] | [unclaimed / promoted / rejected / stale] | [YYYY-MM-DD] |
| 2 | [kebab-case-slug] | [pillar name] | [0–100] | [High / Medium / Low] | [unclaimed / promoted / rejected / stale] | [YYYY-MM-DD] |

---

## Candidate Detail Blocks

One block per candidate in the summary table above, in the same rank order. `candidate_id` anchors the block to its summary row.

### [candidate_id]

| Field | Value |
|---|---|
| Pillar | [OLSP Ecosystem / Affiliate Traffic & List Building / Lead Generation / Online Income for Beginners] |
| Opportunity summary | [1–2 sentence description of the angle/gap/question — not just a keyword] |
| Candidate keyword | [the exact keyword/phrase to hand to ORA if promoted] |
| Discovery Score | [0–100] |
| Priority | [High / Medium / Low] |
| Status | [unclaimed / promoted / rejected / stale] |
| Date discovered | [YYYY-MM-DD] |
| Date status changed | [YYYY-MM-DD] |
| Promoted brief path | [path to Opportunity Brief, once promoted / N/A] |

#### Score breakdown

| Dimension | Score | Rationale |
|---|---|---|
| Demand | [0–25] | [one-line rationale citing the SEARCH_DEMAND signal] |
| Trend | [0–25] | [one-line rationale citing the TREND_INTELLIGENCE signal] |
| Community | [0–25] | [one-line rationale citing the COMMUNITY_INTELLIGENCE signal] |
| Gap | [0–25] | [one-line rationale citing the COMPETITOR_GAP signal] |
| **Total** | **[0–100]** | |

#### Evidence

- **Search demand:** [what SEARCH_DEMAND returned — demand tier, related terms — or "Unavailable — [reason]"]
- **Trend:** [what TREND_INTELLIGENCE returned — direction, rising topics — or "Unavailable — [reason]"]
- **Community:** [what COMMUNITY_INTELLIGENCE returned — which provider, what it found — or "Unavailable — [reason]"]
- **Competitor gap:** [what COMPETITOR_GAP confirmed — the specific angle missing from ranking pages — or "Unavailable — unconfirmed, capped at 5 pts"]

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

| Date | Pillar(s) run | Surfaced | Queued | Dropped (duplicate) | Flagged (ambiguous) |
|---|---|---|---|---|---|
| [YYYY-MM-DD] | [pillar(s)] | [count] | [count] | [count] | [count] |

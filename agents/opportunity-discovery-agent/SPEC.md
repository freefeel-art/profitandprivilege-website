# Opportunity Discovery Agent — Full Specification

**Version:** 0.1
**Status:** Draft — Proposed, not yet implemented

---

## 1. Mission

Explore a content pillar using available intelligence sources and surface candidate publishing opportunities — before any keyword has been manually chosen. Validate, score, and de-duplicate those candidates against everything Profit and Privilege has already published, drafted, briefed, or researched, then produce a ranked **Opportunity Queue**.

The agent discovers opportunities, not keywords. A discovered opportunity may be a content gap, a recurring community question, a rising trend, or a competitor weakness — a keyword is only the eventual label attached to it once it's handed to the Opportunity Research Agent (ORA).

This agent replaces manual keyword selection as the entry point to the editorial pipeline. It does not replace, modify, or duplicate any stage of the existing pipeline downstream of the Opportunity Brief.

---

## 2. Relationship to the Opportunity Research Agent (ORA)

This is a **new, separate agent** that sits immediately upstream of ORA. It is the only change to the pipeline.

```
BEFORE (keyword-first, current production):
  [Operator picks a keyword] → ORA → Opportunity Brief → Research Brief → Production Article → Validation → Publish

AFTER (opportunity-first, this proposal):
  Pillar → Opportunity Discovery Agent → Opportunity Queue → [Operator or automation selects top item]
    → ORA → Opportunity Brief → Research Brief → Production Article → Validation → Publish
                └──────────────────────── UNCHANGED ────────────────────────┘
```

**Nothing about ORA changes:**
- Its input contract is unchanged — it still accepts one `keyword` (string), with optional `intent_hint` and `affiliate_product`. A queue item's candidate keyword is passed in exactly as a manually-chosen keyword would be today.
- Its six research stages, capability layer, scoring model, Opportunity Brief schema, and Stage 0 pre-flight check are unchanged.
- Everything from the Opportunity Brief onward (Research Brief → Production Article → Validation → Publish) is unaffected and out of scope for this spec.

**What is genuinely new:**
- This agent operates on a **pillar**, not a keyword, and produces **many** candidate opportunities per run, not one brief.
- It reuses the same capability providers ORA already has (DataForSEO, Google Trends, Reddit + fallbacks, WebSearch/SERP) in an exploratory, bulk mode rather than ORA's pinpoint, single-keyword mode.
- It introduces one genuinely new capability, `CONTENT_COVERAGE` — a bulk version of the duplicate-check logic already defined in ORA `SPEC.md` Stage 0. See Section 8 for how these should be kept in sync.
- It introduces one new artifact, the **Opportunity Queue**, which does not exist today.

**Known follow-up (not part of this spec, flagged for later):** ORA's Stage 0 duplicate-check rules and this agent's `CONTENT_COVERAGE` capability check the same things. To avoid the two definitions drifting apart, the check rules should eventually be extracted into a single shared reference (e.g. `docs/DUPLICATE-CHECK-STANDARD.md`) that both `SPEC.md` documents point to. This spec defines the ruleset in full (Section 8) so it can be reviewed and approved; extraction is a mechanical follow-up once both specs exist.

---

## 3. Scope

### In scope
- Accepting a content pillar as input (one of the pillars defined in `docs/CONTENT-REGISTRY.md`, or "all pillars")
- Exploring that pillar via the intelligence capability layer to surface candidate opportunities
- Running a bulk content-coverage check against every candidate before it is scored or queued
- Scoring surviving candidates with a lightweight Discovery Score
- Prioritizing and writing candidates to the Opportunity Queue
- Updating the status of existing queue entries (e.g. marking an entry `promoted` once ORA has produced a brief for it)

### Out of scope
- Producing an Opportunity Brief (ORA's job, unchanged)
- Running ORA's six-stage deep-research workflow on any candidate
- Writing articles, outlines, or Astro pages
- Making the final "write this now" editorial call — this agent prioritizes; ORA and the operator still decide
- Modifying any file outside `agents/opportunity-discovery-agent/OPPORTUNITY-QUEUE.md`
- Automatically invoking ORA (at least in this version — see Section 11)

---

## 4. Inputs

**Required:**
- `pillar` (string) — one of the pillar names in `docs/CONTENT-REGISTRY.md` § Content Pillars (currently: `OLSP Ecosystem`, `Affiliate Traffic & List Building`, `Lead Generation`, `Online Income for Beginners`), or `all` to run every pillar in sequence.

**Optional context:**
- `seed_topics` (list of strings) — operator-supplied starting points within the pillar (e.g. specific product names, subtopics). If omitted, the agent derives seed topics from the pillar's existing published pages and stated primary subject in `CONTENT-REGISTRY.md`.
- `max_candidates` (integer) — cap on how many surviving candidates to write to the queue in one run (default: 15 per pillar, to keep the queue reviewable).

---

## 5. Outputs

**Primary output:** Updated `agents/opportunity-discovery-agent/OPPORTUNITY-QUEUE.md` — a single ranked table covering all pillars, with new rows appended (or existing rows updated in the case of a status change).

The queue is a backlog, not a decision. It becomes the input a human (or, later, an automated selector) reads from when choosing what to hand to ORA next.

**Schema:** See Section 9.

---

## 6. Workflow

The agent executes five stages per pillar run. Unlike ORA, it processes many candidates per run rather than one keyword — Stage D2 (coverage check) and Stage D3 (scoring) run once per surviving candidate, not once per invocation.

```
Pillar
    ↓
Stage D0: Seed Generation
    ↓
Stage D1: Multi-Source Exploration
    ↓
Stage D2: Bulk Content-Coverage Check ──── match found ──→ DROP candidate, do not score or queue
    ↓ survivors only
Stage D3: Discovery Scoring
    ↓
Stage D4: Opportunity Queue Write
```

### Stage D0 — Seed Generation

**Tools:** `Read` over `docs/CONTENT-REGISTRY.md` — no external API call required

**Objective:** Establish a starting set of seed topics for the pillar before invoking any external intelligence source.

**Process:**
1. Read the pillar's entry in `docs/CONTENT-REGISTRY.md` (primary subject, existing pages, stated audience).
2. If the operator supplied `seed_topics`, merge them with the derived seeds rather than replacing them.
3. Produce a working seed list of 5–15 topics/phrases broad enough to explore, not narrow enough to already be a keyword (e.g. "OLSP Academy alternatives" rather than "olsp academy vs xyz review").

**Output:** Seed list, carried into Stage D1. Not written to the queue.

---

### Stage D1 — Multi-Source Exploration

**Objective:** Surface raw candidate opportunities from every available intelligence source, for every seed topic. This stage generates volume — it deliberately over-produces; filtering happens in D2 and D3.

**Sources invoked (see Section 8 for capability/provider mapping):**

| Source | What it surfaces |
|---|---|
| Search demand (DataForSEO) | Keyword ideas / related searches at volume, per seed topic — not single-keyword lookups |
| Trend analysis (Google Trends) | Rising or breakout related topics per seed |
| Reddit / community discussions | Recurring questions, complaints, and requests with no satisfying existing answer |
| Competitor gap scan (WebSearch/SERP) | Angles, questions, or sub-topics absent from top-ranking pages across the seed set |
| Existing content coverage (internal) | Not a discovery source — read in D0/D2, used to shape what's worth exploring vs. already owned |

**Process:**
1. For each seed topic, invoke `SEARCH_DEMAND`, `TREND_INTELLIGENCE`, and `COMMUNITY_INTELLIGENCE`.
2. Cluster raw results into distinct **candidate opportunities** — a candidate is a specific, nameable angle (e.g. "readers asking whether OLSP Academy works outside the US" is a candidate; "OLSP Academy" alone is not — that's a seed, not an opportunity).
3. For each candidate, run `COMPETITOR_GAP` to confirm there is in fact a gap worth writing into.
4. Attach every candidate's supporting signals (which sources produced it, what they said) — this becomes the evidence trail for Stage D3 scoring, mirroring ORA's principle that every claim is traceable to a source.

**Failure handling:** Identical cascade principle to ORA (Section 8/10 below) — if a source is unavailable, the agent notes it and continues with remaining sources. A pillar run never halts because one intelligence source failed.

**Output fields populated:** Draft candidate list with supporting evidence, carried into Stage D2. Not written to the queue yet — nothing is queued before the coverage check.

---

### Stage D2 — Bulk Content-Coverage Check

**Tools:** `Grep`/`Read` over repository files and the Opportunity Queue itself — no external API call required

**Objective:** Apply the same "never suggest a duplicate" discipline as ORA's Stage 0, but across every candidate produced in D1 at once, before any candidate is scored.

This is the `CONTENT_COVERAGE` capability. Its contract and check order are defined once, in Section 8, and are intended to be identical in substance to ORA `SPEC.md` § Stage 0 — see Section 2's note on shared-standard extraction.

**Checks performed, per candidate, in order:**

1. **Published content** — does `docs/CONTENT-REGISTRY.md` already cover this candidate (matching or clearly overlapping keyword, title, or slug)?
2. **In-production / drafted pages** — does a file under `src/pages/{reviews,blog,roundups}/**/*.astro` already match?
3. **Existing Opportunity Brief** — does `agents/opportunity-research-agent/briefs/` already have a brief whose slug or primary keyword clearly overlaps?
4. **Existing Research Brief** — does `docs/research/` already cover the same or clearly overlapping topic?
5. **Already in the Opportunity Queue** — does `OPPORTUNITY-QUEUE.md` already contain this candidate as an active (`unclaimed` or `promoted`) row? This check has no ORA equivalent — it exists only because the queue itself is new.

Same judgement standard as ORA Stage 0: a trivial variant (singular/plural, reordered words, "best X" vs "top X" for the same topic) counts as already covered. Genuinely ambiguous overlap is not silently resolved either way.

**Outcomes:**

| Result | Action |
|---|---|
| No match found | Candidate proceeds to Stage D3. |
| Clear match found | Drop the candidate silently from this run's output. Do not score it, do not queue it. (Unlike ORA's single-keyword Stage 0, there is no single "operator decision point" to pause on — at pillar-scan volume, dropping clear duplicates automatically and reporting a count is the right default. See run summary in Section 6 output.) |
| Uncertain / partial overlap | Do not drop and do not queue automatically. Carry the candidate into the run summary under a separate "needs human judgement" list, with the ambiguous match cited, but do not add it to the ranked queue table until resolved. |

**Output fields populated:** Section "Coverage Check" of each surviving candidate's queue row (Section 9). Dropped and ambiguous candidates are reported in the run summary but not written as queue rows.

---

### Stage D3 — Discovery Scoring

**Tool:** Internal reasoning — no external tool call required

**Objective:** Rank surviving candidates cheaply, so the operator (or a future automated selector) can see what's most worth promoting to a full ORA run next. This is deliberately **not** ORA's Opportunity Score — it is a lighter triage signal built only from what Stage D1 already collected, so the agent is not re-running ORA's expensive four-capability deep dive for every candidate before anyone has even decided the candidate is worth that spend.

**Discovery Score model:**

The Discovery Score is 0–100, from four sub-scores of equal weight (25 points each):

| Sub-score | Signal | 25 pts | 15 pts | 5 pts |
|---|---|---|---|---|
| **Demand** | Search demand signal from Stage D1 (DataForSEO keyword ideas volume tier) | High | Medium | Low / Unavailable |
| **Trend** | Trend direction from Stage D1 (Google Trends) | Rising / breakout | Stable | Declining / Unavailable |
| **Community** | Community engagement + unmet-question signal from Stage D1 (Reddit or fallback) | Strong, unmet demand | Some signal | Weak / Unavailable |
| **Gap** | Competitor gap confirmed in Stage D1 | Clear gap, weak/absent coverage in top 10 | Partial gap | No real gap |

**Explicitly not part of this score:** keyword difficulty, CPC, and editorial/affiliate alignment. Those require ORA's full KEYWORD_INTELLIGENCE and editorial-judgement passes and are computed later, once a candidate is promoted. A high Discovery Score means "worth spending a full ORA run on" — it is not a substitute for ORA's Opportunity Score and must never be presented as one.

**Priority labels:**

| Score | Label |
|---|---|
| 70–100 | High priority — recommend promoting to ORA soon |
| 40–69 | Medium priority — worth keeping in the queue |
| 0–39 | Low priority — retained for visibility, not recommended next |

**Output fields populated:** `discovery_score`, `priority`, and per-sub-score rationale in each candidate's queue row.

---

### Stage D4 — Opportunity Queue Write

The agent appends surviving, scored candidates to `agents/opportunity-discovery-agent/OPPORTUNITY-QUEUE.md`, sorted by `discovery_score` descending within each pillar. If a candidate's status changed (e.g. an operator promoted a prior entry to ORA and a brief now exists), the agent updates that row's `status` field rather than duplicating it.

At the end of the run, the agent reports to the operator:
- Pillar(s) run
- Number of candidates surfaced (Stage D1) vs. surviving to the queue (post Stage D2/D3)
- Number dropped as clear duplicates, and number flagged as ambiguous (needing human judgement)
- Top 3 candidates by Discovery Score this run

---

## 7. Duplicate-Suppression Guarantees

These map directly to the constraints this agent must enforce, restated as explicit rules:

| Rule | Enforced by |
|---|---|
| Never suggest opportunities already published | Stage D2, check 1 |
| Never suggest opportunities already in production | Stage D2, check 2 |
| Never duplicate an existing Opportunity Brief | Stage D2, check 3 |
| Never duplicate an existing Research Brief | Stage D2, check 4 |
| Skip topics already covered manually | Checks 1–4 are content-based, not pipeline-based — a manually-written page in `src/pages/**` or a manually-maintained registry entry is caught the same way an AI-produced one is. No separate "manual" path exists or is needed. |
| Never re-add a candidate already sitting in the queue | Stage D2, check 5 (new — has no ORA equivalent, since the queue itself is new) |

---

## 8. Capability Layer Architecture

This agent reuses ORA's existing capability/provider pattern (`SPEC.md` § 7 in ORA) rather than introducing a parallel one. Where a capability already exists, this agent invokes it in **bulk/exploratory mode** (many seeds, many candidates) instead of ORA's **pinpoint mode** (one keyword). Only `CONTENT_COVERAGE` is new.

```
Capability               Contract (what the agent needs)         Provider                    Mode vs. ORA
──────────────────────────────────────────────────────────────────────────────────────────────────────────
SEARCH_DEMAND            demand tier + related/rising terms       DataForSEO V1               Bulk: keyword-ideas
                         per seed topic                                                        per seed, not single lookup

TREND_INTELLIGENCE       trend direction, rising related topics    Google Trends V1             Same provider as ORA;
                         per seed topic                                                        run once per seed

COMMUNITY_INTELLIGENCE   recurring questions, unmet demand,        Reddit V1 → Quora V1 →      Same provider chain
                         sentiment, per seed topic                 Google Discussions V1 →     as ORA; run once per
                                                                    YouTube V1 → Google News V1  seed, not per keyword

COMPETITOR_GAP           confirmed gap per candidate               WebSearch V1                 Reuses ORA's
                         (angle absent from top-ranking pages)                                  SERP_INTELLIGENCE
                                                                                                logic, run per
                                                                                                candidate not
                                                                                                per single keyword

CONTENT_COVERAGE         match / no-match / ambiguous against      Internal (Grep/Read over     NEW — bulk version
                         registry, drafted pages, briefs,          repo files + queue file)     of ORA Stage 0,
                         research briefs, and the queue itself                                  run per candidate
```

### CONTENT_COVERAGE contract (new)

```
Required outputs (per candidate):
  match_status       None / Clear match / Ambiguous
  matched_artifact   Path or identifier of the matching registry entry, page, brief,
                      research brief, or queue row (or N/A if no match)
  reasoning          One-line explanation of why this counts as covered or overlapping
```

### Provider registry (proposed bindings)

| Capability | Provider | Notes |
|---|---|---|
| SEARCH_DEMAND | DataForSEO V1 | Same provider ORA uses for KEYWORD_INTELLIGENCE; different call shape (keyword-ideas/suggestions for a seed, not exact-match metrics for a keyword) |
| TREND_INTELLIGENCE | Google Trends V1 | Identical to ORA's binding |
| COMMUNITY_INTELLIGENCE | Reddit V1 (+ same fallback chain as ORA) | Identical to ORA's binding and cascade order |
| COMPETITOR_GAP | WebSearch V1 | Reuses ORA's SERP_INTELLIGENCE provider; narrower per-call scope (gap confirmation, not full top-10 teardown) |
| CONTENT_COVERAGE | Internal (Grep/Read) | Same sources ORA Stage 0 reads, plus `OPPORTUNITY-QUEUE.md` |

No new external integrations are required to implement this agent.

---

## 9. Opportunity Queue Schema

**File:** `agents/opportunity-discovery-agent/OPPORTUNITY-QUEUE.md`
**Schema version:** 0.1

One ranked table, all pillars together, sorted by `discovery_score` descending within each pillar grouping. Every field is required; unavailable data is recorded explicitly, never left blank — same discipline as ORA's Opportunity Brief.

```
pillar:               [OLSP Ecosystem / Affiliate Traffic & List Building / Lead Generation / Online Income for Beginners]
candidate_id:         [kebab-case slug for this candidate — becomes the ORA keyword input if promoted]
opportunity_summary:  [1–2 sentence description of the angle/gap/question — not just a keyword]
candidate_keyword:    [the keyword/phrase to hand to ORA if promoted]
discovery_score:      [0–100]
priority:             [High / Medium / Low]
score_breakdown:      [demand / trend / community / gap sub-scores with one-line rationale each]
evidence:             [which sources produced this candidate, with links/citations where available]
coverage_check:       [match_status: None — confirmed clear at Stage D2, with date]
status:               [unclaimed / promoted / rejected / stale]
promoted_brief_path:  [path to the Opportunity Brief, once promoted — N/A until then]
date_discovered:      [YYYY-MM-DD]
date_status_changed:  [YYYY-MM-DD — updated whenever status changes]
```

`status` lifecycle: `unclaimed` → `promoted` (an operator has run this candidate through ORA) or `rejected` (operator reviewed and declined) or `stale` (evidence is old enough that it should be re-discovered rather than promoted as-is — threshold to be defined operationally, not in this spec).

---

## 10. Failure Handling

Same principle as ORA: **the agent never stops a pillar run because a single source is unavailable.**

| Failure | Response |
|---|---|
| SEARCH_DEMAND unavailable for a seed | Note it, continue exploration with TREND_INTELLIGENCE and COMMUNITY_INTELLIGENCE only for that seed; Demand sub-score becomes `Unavailable` (5 pts floor) rather than blocking the candidate |
| TREND_INTELLIGENCE unavailable | Same pattern — Trend sub-score `Unavailable` |
| COMMUNITY_INTELLIGENCE — all providers in the cascade fail | Same pattern — Community sub-score `Unavailable` |
| COMPETITOR_GAP unavailable | Candidate proceeds without a confirmed gap; Gap sub-score capped at 5 pts and flagged, since an unconfirmed gap should not rank highly |
| CONTENT_COVERAGE check fails to read a source file | Do not queue the candidate. Report it as "coverage check incomplete" in the run summary rather than risk queuing a duplicate. This is the one failure mode where the agent is more conservative than "continue with partial data," because the entire purpose of this stage is duplicate suppression. |
| All sources fail for a seed | Drop the seed for this run, note it in the run summary, continue with remaining seeds |

---

## 11. Prompt Design Principles

Same discipline as ORA, restated for this agent:

- **Role framing:** an opportunity scout, not a writer or a researcher. It surfaces candidates and evidence; it does not draft content and does not run ORA's deep research.
- **Capability-first language:** the prompt instructs in terms of capabilities (`SEARCH_DEMAND`, `CONTENT_COVERAGE`, etc.), consulting the provider registry — identical pattern to ORA, so provider swaps never require a prompt rewrite.
- **Coverage-check conservatism:** unlike every other stage, Stage D2 is the one place where "continue on failure" is the wrong default — an unreadable coverage source means "don't queue," not "queue anyway."
- **No auto-promotion:** this agent never invokes ORA itself in this version. It writes to the queue and stops. Promotion is a human action (or a future explicit automation decision, out of scope here — see Section 12).
- **Evidence traceability:** every queued candidate must cite which source(s) produced it, matching ORA's "evidence, not opinions" principle.

Full system/user prompt to be written in a companion `PROMPT.md`, following ORA's `PROMPT.md` structure, once this spec is approved.

---

## 12. Folder Structure

```
agents/
  opportunity-discovery-agent/
    README.md                ← overview and quick reference (to be written, mirrors ORA's README.md)
    SPEC.md                  ← this document
    PROMPT.md                ← system prompt and user prompt template (to be written)
    OUTPUT-TEMPLATE.md       ← blank Opportunity Queue row template (to be written)
    OPPORTUNITY-QUEUE.md     ← the queue itself — this agent's only write target
  opportunity-research-agent/ ← UNCHANGED — no files in this folder are modified by this proposal
```

The `OPPORTUNITY-QUEUE.md` file is this agent's only write target, mirroring ORA's constraint that `briefs/` is its only write target.

---

## 13. Future Extensibility (not part of this proposal)

- **Automated promotion:** once queue quality is proven out manually, allow this agent (or a thin orchestrator) to auto-invoke ORA for `High` priority, `unclaimed` candidates above a threshold, without operator selection.
- **Scheduled runs:** run Discovery on a cadence per pillar (e.g. weekly) rather than on-demand, so the queue stays warm.
- **Staleness detection:** revisit `unclaimed` queue rows older than N days and re-run Stage D1–D3 signals to confirm they're still worth promoting, flagging `stale` per Section 9.
- **Shared standard extraction:** factor the coverage-check rules (Section 7/8 here, Stage 0 in ORA `SPEC.md`) into one shared doc both specs reference, per the note in Section 2.
- **Cross-candidate deduplication within a single run:** if two candidates surfaced in the same D1 pass are near-duplicates of each other (not of existing content), merge them before scoring rather than queuing both.

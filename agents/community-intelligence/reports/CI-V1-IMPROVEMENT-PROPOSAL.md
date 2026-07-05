# Community Intelligence Agent V1 — Improvement Proposal

**Generated:** 2026-07-05
**Based on:** Production validation run against OLSP Academy (see `OLSP-Academy-CI-Report-2026-07.md`)

---

## Critical

### C-1: Add Confidence Normalisation Rules

**Problem:** During the validation run, every root cause analysis (Section 5) was assigned "High" confidence. This is not realistic — in production, some findings will inherently be Medium or Low. The agent inflated confidence because the prompt did not provide proportional guidelines.

**Fix:** Add explicit frequency-to-confidence mapping in PROMPT.md and OUTPUT-SCHEMA.md:

| Confidence | Required Evidence |
|---|---|
| High | Seen in 3+ communities, 5+ independent threads, consistent pattern |
| Medium | Seen in 2 communities, 3+ threads, or strong in one community |
| Low | Seen in 1-2 threads, contradictory evidence, or single community |

Enforce that no more than 60% of findings in a single report section may be "High" confidence. If the agent cannot meet this threshold naturally, it indicates insufficient research depth.

### C-2: Resolve the Section 7–8 Redundancy

**Problem:** Solution Feasibility Gate (Section 7) and OLSP Alignment Gate (Section 8) ask related but distinct questions. In practice, for a topic like "OLSP Academy" itself, they produce repetitive entries — both sections tend to answer "yes" for most findings.

**Fix:** Either:

- **Option A (Merge):** Combine into a single "Content & Platform Feasibility Gate" section with two sub-fields: `can_content_solve` and `platform_alignment`. Reduces schema surface area by one section.
- **Option B (Conditional):** Make Section 8 optional, activated only when the report niche is directly related to OLSP. For unrelated niches, omit Section 8 entirely.

Recommended: Option B, implemented via a `niche_relevance` flag in the report metadata. If `niche_relevance != "OLSP-adjacent"`, Section 8 is skipped.

### C-3: Define "Existing Content" Scope for Section 6

**Problem:** Section 6 (Existing Content Failures) analyses why existing content fails to solve each problem. During the validation run, some entries analysed other independent reviews as "existing content." This conflates two categories: (1) the platform's own marketing content and (2) third-party reviews. These categories fail differently.

**Fix:** Split Section 6 into two sub-sections or add a `content_type` field per entry:

```yaml
- name: "content_type"
  type: "enum: Platform marketing | Independent review | Community advice | Educational resource"
  required: true
```

This enables separate gap analysis for each content type and prevents category confusion.

### C-4: Add Validation Rules to the PROMPT

**Problem:** The PROMPT.md references the OUTPUT-SCHEMA.md for validation rules but does not include explicit pre-submission checks. During the validation run, several quality checks (confidence distribution, source count, intent diversity) were verified manually rather than by the agent.

**Fix:** Append a mandatory pre-submission checklist to PROMPT.md that the agent must verify before outputting the report:

```
PRE-SUBMISSION CHECKLIST (run before outputting report):
- [ ] All finding_ids are unique and sequential
- [ ] No more than 60% of Section 5 entries are "High" confidence
- [ ] Every finding_id referenced in Sections 5-12 appears in Section 3 or 4
- [ ] Every thread_id referenced appears in Section 13
- [ ] Every community_id referenced appears in Section 2
- [ ] Section 10 has 3-5 angles per opportunity
- [ ] Section 11 has ≥5 articles
- [ ] Section 3 spans ≥3 intent types
- [ ] Section 13 entries reference finding_ids, not free text
```

---

## Recommended

### R-1: Add an ID Registry Automatically

**Problem:** ID management across 13 sections was manual and error-prone. The ID Registry (documented in the schema) is not automatically populated.

**Fix:** Add an instruction at the top of PROMPT.md requiring the agent to build a running ID registry during generation and include it in the report metadata. The registry should be updated as each section is completed.

**Implementation:** Before outputting the final report, the agent collects all IDs used across all sections into a single `id_registry` block. This also serves as a validation cross-check (any ID referenced but not in the registry is a bug).

### R-2: Add Opportunity Score Normalisation

**Problem:** OPP-001 scored 44/50. Without a normalisation mechanism, 44 vs 35 vs 37 has no cross-report meaning. Scores within a report are ordinal (relative ranking) but not cardinal (absolute quality).

**Fix:** Add a relative ranking field alongside the raw score:

```yaml
- name: "relative_rank"
  type: "integer (1-N)"
  required: true
  description: "Rank within this report. 1 = highest priority opportunity."
```

And add a normalisation note in OUTPUT-SCHEMA.md:
> Opportunity scores are report-relative. A score of 44 in one report and 38 in another do not indicate higher absolute opportunity — they indicate relative priority within each report.

### R-3: Add Source Quality Scoring

**Problem:** Communities are described qualitatively in Section 2 but not scored for reliability. A high-activity community with low moderation (e.g., r/sidehustle) produces different signal quality from a structured review platform (e.g., Trustpilot).

**Fix:** Add a `source_reliability` field to Section 2 entries:

```yaml
- name: "source_reliability"
  type: "enum: High | Medium | Low"
  description: "High = verified users, structured feedback, active moderation. Medium = open platform with some signal verification. Low = anonymous, unmoderated, or promotional."
```

And add a note in PROMPT.md: "When multiple communities provide conflicting signals, weight findings from High-reliability sources more heavily."

### R-4: Add Confidence Rating for the Report as a Whole

**Problem:** Individual findings have confidence ratings, but the report has no aggregate confidence rating. A reader cannot tell whether the agent thinks this research is reliable or tentative.

**Fix:** Add an optional `report_confidence` field to Section 1:

```yaml
- name: "report_confidence"
  type: "enum: High | Medium | Low"
  description: "The agent's overall confidence in this report's findings. High = strong signal across multiple communities with consistent patterns. Medium = clear patterns but limited community breadth. Low = insufficient signal strength — flag for re-research."
```

### R-5: Add a Cross-Reference Table Between Findings and Opportunities

**Problem:** The report contains findings (Sections 3-4) and opportunities (Section 9), and the Executive Summary references the top opportunity by ID. But there is no structural map showing which findings aggregate into which opportunities.

**Fix:** Add a dedicated sub-section within Section 1 (or a standalone Section 1a) mapping the finding-to-opportunity structure:

```yaml
finding_opportunity_map:
  - opportunity_id: "OPP-001"
    supporting_finding_ids: ["FND-001", "FND-003", "FND-012", "FND-018", "FND-022"]
  - opportunity_id: "OPP-002"
    supporting_finding_ids: ["FND-010", "FND-014", "FND-016"]
```

This makes the synthesis logic transparent to downstream agents.

---

## Optional

### O-1: Remove Evidence Snippet Duplication Across Traceability Layers

The current schema requires `evidence_snippet` on primary findings (Sections 3-4), derived findings (Section 5-6), and gate entries (Sections 7-8). This creates substantial duplication — the same snippet appears up to 4 times for the same finding chain.

**Possible fix:** Allow derived and gate entries to link to the primary finding's evidence snippet rather than repeating it. Replace `evidence_snippet` with `evidence_ref: "FND-003.evidence_snippet"` for non-primary entries. This reduces verbosity but requires downstream agents to resolve references.

**Trade-off:** Breaks the "self-contained entry" traceability rule. Not recommended until the downstream agent (Editorial Intelligence) confirms it can resolve cross-entry references.

### O-2: Add Platform Source Type Weighting

Different platform types produce different signal quality:
- Reddit: Anonymous, high skepticism, high candidness
- Trustpilot: Verified reviews but potential bias patterns
- Quora: Lower skepticism but more promotional content

A formal weighting system could help the agent prioritise findings from higher-candour sources. However, this adds complexity and risks false precision. Revisit after 5+ production reports exist.

### O-3: Automate the Minimum Entry Count Validation

Currently, the validation rules specify minimum counts (10 questions, 5 communities, 5 articles, etc.) but these are checked manually. A structured pre-submission validation block in the PROMPT could automate this check.

**Implementation:** Add a final section to the PROMPT:

```
VALIDATION BLOCK (fill before completing):
- communities_found: 7 (min: 5) ✓
- recurring_questions: 14 (min: 10) ✓
- intent_types_represented: 4 (min: 3) ✓
- recurring_problems: 8 (min: 5) ✓
- opportunities_scored: 5 (min: 5) ✓
- articles_recommended: 7 (min: 5) ✓
- confidence_high_percentage: 100% (max: 60%) ✗ (see C-1)
```

### O-4: Standardise Date Format in Source Log

The current schema specifies `date_consulted` as "ISO date" but does not enforce YYYY-MM-DD format. Standardise to ISO 8601 to prevent parsing errors in automated downstream processing.

### O-5: Add a "Research Coverage Map"

Visual or tabular map showing which communities were searched for which questions. Currently, each question lists its `communities` field but there is no community-by-question matrix. A coverage map would reveal gaps — communities that were identified but not mined for certain question types.

---

## Summary by Priority

| Priority | Count | Items |
|----------|-------|-------|
| Critical | 4 | C-1 (confidence normalisation), C-2 (gate redundancy), C-3 (content scope), C-4 (validation checklist) |
| Recommended | 5 | R-1 (ID registry), R-2 (score normalisation), R-3 (source quality), R-4 (report confidence), R-5 (finding-opportunity map) |
| Optional | 5 | O-1 (snippet dedup), O-2 (source weighting), O-3 (auto-validation), O-4 (date format), O-5 (coverage map) |

**Next action:** Review and prioritise with the editorial team before implementing any changes to the specification.

# Research Brief — Output Schema

This document defines the canonical structure of a Research Brief. Every brief produced by the Research Factory Agent must conform to this schema.

---

## Identifier System

### ID Prefixes

| Prefix | ID Type | Defining Section | Assignment |
|--------|---------|-----------------|------------|
| `BRF` | brief_id | Metadata | Sequential. BRF-001 for first brief. |
| `SRC` | source_id | Section 2 — Source Inventory | Sequential in inventory order |
| `CLM` | claim_id | Section 3 — Evidence Library | Section-internal, sequential within claims |
| `GAP` | gap_id | Section 5 — Knowledge Gap Log | Section-internal, sequential within gaps |

### Determinism Rules

1. IDs are assigned during brief generation, based on the canonical section order defined in this schema.
2. BRF IDs are assigned sequentially across all Research Briefs (BRF-001, BRF-002, ...).
3. SRC IDs are assigned sequentially in the order sources appear in the Source Inventory.
4. CLM and GAP IDs are section-internal — they reset per brief and are meaningful only within that brief.
5. IDs are never reused. If a source is removed during revision, its ID is retired.

### ID Reservation

| ID Type | Reserved Range |
|---------|---------------|
| brief_id | BRF-001 — BRF-099 |
| source_id | SRC-001 — SRC-999 |
| claim_id | CLM-001 — CLM-999 |
| gap_id | GAP-001 — GAP-999 |

---

## Report Structure

```
Research Brief
├── 1. Metadata
├── 2. Source Inventory
├── 3. Evidence Library
├── 4. Fact Summary
├── 5. Knowledge Gap Log
├── 6. Vendor Claims Registry
└── 7. Editorial Notes
```

---

## 1. Metadata

### Schema

```yaml
section: "1. Metadata"
type: "structured metadata object"
required: true
fields:
  - name: "brief_id"
    type: "string (BRF-NNN)"
    required: true
    description: "Permanent canonical identifier for this Research Brief"
  - name: "opportunity_id"
    type: "string (OPP-NNN)"
    required: true
    description: "The opportunity this brief supports"
  - name: "opportunity_title"
    type: "string"
    required: true
    description: "Working title of the opportunity"
  - name: "state"
    type: "enum: Drafted | Complete | Consumed | Archived"
    required: true
    description: "Current lifecycle state. Should be 'Complete' at handoff."
  - name: "generated"
    type: "string (ISO date)"
    required: true
    description: "When the brief was generated"
  - name: "p0_requirements_total"
    type: "integer"
    required: true
    description: "Total P0 research requirements from the Opportunity Brief"
  - name: "p0_requirements_fulfilled"
    type: "integer"
    required: true
    description: "How many P0 requirements were fulfilled"
  - name: "p0_requirements_critical_gaps"
    type: "integer"
    required: true
    description: "How many P0 requirements are logged as critical knowledge gaps"
  - name: "p1_requirements_total"
    type: "integer"
    required: true
  - name: "p1_requirements_fulfilled"
    type: "integer"
    required: true
  - name: "p2_requirements_total"
    type: "integer"
    required: true
  - name: "p2_requirements_fulfilled"
    type: "integer"
    required: true
  - name: "source_count"
    type: "integer"
    required: true
    description: "Total sources in the Source Inventory"
  - name: "claim_count"
    type: "integer"
    required: true
    description: "Total claims in the Fact Summary"
  - name: "knowledge_gap_count"
    type: "integer"
    required: true
    description: "Total entries in the Knowledge Gap Log"
  - name: "id_registry"
    type: "object"
    required: true
    description: "All IDs used in this brief"
    fields:
      - name: "source_ids"
        type: "array of strings (SRC-NNN)"
      - name: "claim_ids"
        type: "array of strings (CLM-NNN)"
      - name: "gap_ids"
        type: "array of strings (GAP-NNN)"
```

### Example

```json
{
  "section": "1. Metadata",
  "brief_id": "BRF-001",
  "opportunity_id": "OPP-001",
  "opportunity_title": "Is OLSP Academy an MLM? An Evidence-Based Investigation",
  "state": "Complete",
  "generated": "2026-07-05",
  "p0_requirements_total": 3,
  "p0_requirements_fulfilled": 2,
  "p0_requirements_critical_gaps": 1,
  "p1_requirements_total": 3,
  "p1_requirements_fulfilled": 2,
  "p2_requirements_total": 2,
  "p2_requirements_fulfilled": 1,
  "source_count": 14,
  "claim_count": 8,
  "knowledge_gap_count": 3,
  "id_registry": {
    "source_ids": ["SRC-001", "SRC-002", "SRC-003"],
    "claim_ids": ["CLM-001", "CLM-002"],
    "gap_ids": ["GAP-001", "GAP-002"]
  }
}
```

---

## 2. Source Inventory

### Schema

```yaml
section: "2. Source Inventory"
type: "array of source entries"
required: true
description: "Every source collected during research, classified by type and reliability."
entry:
  fields:
    - name: "source_id"
      type: "string (SRC-NNN)"
      required: true
      description: "Permanent source identifier. Assigned sequentially in inventory order."
    - name: "title"
      type: "string"
      required: true
      description: "Source title or page title"
    - name: "url"
      type: "string (URL)"
      required: true
      description: "Direct URL to the source"
    - name: "source_type"
      type: "enum: Official_documentation | Third-party_review | News_article | Community_thread | Academic_source | Regulatory_document | Vendor_page"
      required: true
    - name: "reliability_label"
      type: "enum: Verified | Vendor_claim | Third-party_reported | Self-reported | Unverified"
      required: true
      description: "See SPEC.md section 4 Step 2 for definitions"
    - name: "accessed_date"
      type: "string (ISO date)"
      required: true
      description: "When the source was consulted"
    - name: "relevant_claims"
      type: "array of strings"
      required: true
      description: "Which claims this source supports (referenced by claim text, not CLM IDs, for readability)"
    - name: "satisfies_requirement"
      type: "string"
      required: true
      description: "Which research requirement this source satisfies (e.g., 'P0: MLM definition from FTC')"
    - name: "notes"
      type: "string"
      required: false
      description: "Any context about this source (access limitations, partial relevance, etc.)"
```

### Example

```json
{
  "section": "2. Source Inventory",
  "entries": [
    {
      "source_id": "SRC-001",
      "title": "Business Opportunities Rule",
      "url": "https://www.ftc.gov/business-guidance/resources/business-opportunities-rule",
      "source_type": "Regulatory_document",
      "reliability_label": "Verified",
      "accessed_date": "2026-07-05",
      "relevant_claims": [
        "FTC definition of MLM/pyramid scheme",
        "Criteria that distinguish legal MLMs from illegal pyramid schemes"
      ],
      "satisfies_requirement": "P0: Official MLM definition from FTC or equivalent regulatory body",
      "notes": ""
    },
    {
      "source_id": "SRC-002",
      "title": "OLSP Academy Pricing Page",
      "url": "https://olspacademy.com/pricing",
      "source_type": "Vendor_page",
      "reliability_label": "Vendor_claim",
      "accessed_date": "2026-07-05",
      "relevant_claims": [
        "OLSP commission structure",
        "OLSP pricing tiers"
      ],
      "satisfies_requirement": "P0: OLSP official terms of service and commission structure documentation",
      "notes": "Pricing page captured on 2026-07-05. May change."
    }
  ]
}
```

---

## 3. Evidence Library

### Schema

```yaml
section: "3. Evidence Library"
type: "array of evidence entries, organised by claim"
required: true
description: "Sources organised by claim. The writer's primary working reference."
entry:
  fields:
    - name: "article_section"
      type: "string"
      required: true
      description: "Which section of the planned article this evidence supports (from Opportunity Brief's Recommended Structure)"
    - name: "claim_id"
      type: "string (CLM-NNN)"
      required: true
      description: "Section-internal claim identifier"
    - name: "claim_statement"
      type: "string"
      required: true
      description: "The specific claim. Expressed as a testable proposition."
    - name: "source_ids"
      type: "array of strings (SRC-NNN)"
      required: true
      min_entries: 1
      description: "All sources that support this claim"
    - name: "evidence_summary"
      type: "string"
      required: true
      description: "What the evidence says (1-3 sentences)"
    - name: "confidence"
      type: "enum: High | Medium | Low"
      required: true
    - name: "confidence_rationale"
      type: "string"
      required: true
      description: "Why this confidence level was assigned"
    - name: "contradictions"
      type: "array of objects"
      required: false
      description: "Any sources that contradict this claim"
      items:
        fields:
          - name: "source_id"
            type: "string (SRC-NNN)"
          - name: "contradictory_claim"
            type: "string"
    - name: "writer_guidance"
      type: "string"
      required: false
      description: "How the writer should present this evidence in the article"
    - name: "citation_ready"
      type: "boolean"
      required: true
      description: "True if this claim can be cited directly with source attribution"
```

### Example

```json
{
  "section": "3. Evidence Library",
  "entries": [
    {
      "article_section": "Section 3: What the legal definition of MLM actually is",
      "claim_id": "CLM-001",
      "claim_statement": "The FTC defines an illegal pyramid scheme as a program where compensation is primarily derived from recruitment rather than product sales.",
      "source_ids": ["SRC-001"],
      "evidence_summary": "FTC Business Opportunities Rule guidance states that pyramid schemes promise rewards for recruiting new members rather than for selling products. Key criteria include: recruitment is emphasised over product sales, inventory loading requirements, and lack of genuine retail sales.",
      "confidence": "High",
      "confidence_rationale": "Single verified source (FTC regulatory guidance), but FTC is the definitive authority on this question. No contradictory legal sources found.",
      "contradictions": [],
      "writer_guidance": "State this as the authoritative definition. Note it is a US federal definition — other jurisdictions may vary.",
      "citation_ready": true
    }
  ]
}
```

---

## 4. Fact Summary

### Schema

```yaml
section: "4. Fact Summary"
type: "array of claim summary entries"
required: true
description: "Quick-reference table of all key claims with confidence, evidence, and contradictions."
entry:
  fields:
    - name: "claim_id"
      type: "string (CLM-NNN)"
      required: true
      description: "References the full entry in Section 3"
    - name: "claim_statement"
      type: "string"
      required: true
      description: "The specific claim (concise)"
    - name: "claim_type"
      type: "enum: Verification | Definition | Comparison | Attribution | Quantification"
      required: true
    - name: "confidence"
      type: "enum: High | Medium | Low"
      required: true
    - name: "key_sources"
      type: "array of strings (SRC-NNN)"
      required: true
      min_entries: 1
      description: "Primary supporting sources (most reliable)"
    - name: "has_contradictions"
      type: "boolean"
      required: true
    - name: "is_single_source"
      type: "boolean"
      required: true
      description: "True if this claim depends on a single source"
    - name: "citation_ready"
      type: "boolean"
      required: true
    - name: "writer_guidance"
      type: "string"
      required: false
```

### Example

```json
{
  "section": "4. Fact Summary",
  "entries": [
    {
      "claim_id": "CLM-001",
      "claim_statement": "FTC defines illegal pyramid schemes by recruitment emphasis vs. product sales",
      "claim_type": "Definition",
      "confidence": "High",
      "key_sources": ["SRC-001"],
      "has_contradictions": false,
      "is_single_source": true,
      "citation_ready": true,
      "writer_guidance": "Single source but it's the definitive regulatory authority. Sufficient for citation."
    }
  ]
}
```

---

## 5. Knowledge Gap Log

### Schema

```yaml
section: "5. Knowledge Gap Log"
type: "array of gap entries"
required: true
description: "Every claim or question that could not be verified from available sources."
entry:
  fields:
    - name: "gap_id"
      type: "string (GAP-NNN)"
      required: true
      description: "Section-internal gap identifier"
    - name: "claim_or_question"
      type: "string"
      required: true
      description: "The claim or question with insufficient evidence"
    - name: "gap_type"
      type: "enum: Unverifiable | Missing_data | Contradictory | Single_source | Outdated | Speculative"
      required: true
    - name: "originates_from"
      type: "string"
      required: true
      description: "Where this gap originates (Opportunity Brief section, research requirement, or community finding)"
    - name: "attempted_sources"
      type: "string"
      required: true
      description: "What was searched and what (if anything) was found"
    - name: "closest_available"
      type: "string"
      required: false
      description: "The nearest information found, even if inadequate"
    - name: "impact"
      type: "string"
      required: true
      description: "How this gap affects the article's ability to answer the primary question"
    - name: "is_critical"
      type: "boolean"
      required: true
      description: "True if this is a P0 requirement that could not be fulfilled"
    - name: "recommended_treatment"
      type: "string"
      required: true
      description: "How the writer should handle this gap. Must be specific and actionable."
```

### Example

```json
{
  "section": "5. Knowledge Gap Log",
  "entries": [
    {
      "gap_id": "GAP-001",
      "claim_or_question": "What percentage of OLSP Academy members actually earn money?",
      "gap_type": "Missing_data",
      "originates_from": "Opportunity Brief: Related Question 6",
      "attempted_sources": "Searched OLSP official site, independent reviews, Trustpilot, Reddit threads. No published income data found. OLSP does not publish member earnings statistics. Trustpilot reviews mention earnings but are self-reported and unaudited.",
      "closest_available": "Community threads contain individual self-reported earnings figures, but these are not representative and cannot be verified.",
      "impact": "Moderate. Article cannot state a figure for typical earnings. Must acknowledge that OLSP does not publish earnings data.",
      "is_critical": false,
      "recommended_treatment": "Acknowledge the data gap explicitly: 'OLSP Academy does not publish member earnings data. The only available earnings figures are self-reported in community discussions and cannot be independently verified.' Label as unverifiable."
    }
  ]
}
```

---

## 6. Vendor Claims Registry

### Schema

```yaml
section: "6. Vendor Claims Registry"
type: "array of vendor claim entries"
required: true
description: "All claims from vendor/official sources that could not be independently verified. The writer must label these explicitly."
entry:
  fields:
    - name: "claim_id"
      type: "string (CLM-NNN)"
      required: true
      description: "References the claim in Section 3"
    - name: "claim_statement"
      type: "string"
      required: true
      description: "The claim as published by the vendor"
    - name: "vendor_source_id"
      type: "string (SRC-NNN)"
      required: true
      description: "The source where this claim was found"
    - name: "vendor"
      type: "string"
      required: true
      description: "The entity making the claim (e.g., 'OLSP Academy')"
    - name: "claim_context"
      type: "string"
      required: true
      description: "How the claim was presented (e.g., 'Homepage headline', 'Testimonial page')"
    - name: "independent_verification_attempted"
      type: "boolean"
      required: true
    - name: "verification_result"
      type: "string"
      required: true
      description: "What the attempted verification found (e.g., 'No independent source confirms this claim')"
    - name: "required_writer_label"
      type: "string"
      required: true
      description: "How the writer must label this in the article (e.g., 'According to OLSP Academy's official site...')"
```

### Example

```json
{
  "section": "6. Vendor Claims Registry",
  "entries": [
    {
      "claim_id": "CLM-005",
      "claim_statement": "OLSP Academy has helped thousands of students succeed in affiliate marketing",
      "vendor_source_id": "SRC-003",
      "vendor": "OLSP Academy",
      "claim_context": "Homepage headline",
      "independent_verification_attempted": true,
      "verification_result": "No independent source confirms aggregate student success numbers. Individual testimonials exist on site but are self-reported.",
      "required_writer_label": "According to OLSP Academy's official website"
    }
  ]
}
```

---

## 7. Editorial Notes

### Schema

```yaml
section: "7. Editorial Notes"
type: "array of note entries"
required: true
description: "Research context, caveats, warnings, and author guidance."
entry:
  fields:
    - name: "note_id"
      type: "string (sequential within section)"
      required: true
      description: "Simple sequential identifier (N-001, N-002, ...)"
    - name: "note_type"
      type: "enum: Warning | Caveat | Context | Data_freshness | Methodology | Writer_direction"
      required: true
    - name: "note"
      type: "string"
      required: true
      description: "The note content"
    - name: "affects_section"
      type: "string"
      required: false
      description: "Which article section this note applies to (from Opportunity Brief)"
    - name: "action_required"
      type: "boolean"
      required: true
      description: "True if the writer must take action based on this note"
    - name: "action"
      type: "string"
      required: false
      description: "What the writer should do"
```

### Example

```json
{
  "section": "7. Editorial Notes",
  "entries": [
    {
      "note_id": "N-001",
      "note_type": "Data_freshness",
      "note": "FTC Business Opportunities Rule guidance was most recently updated in 2023. Verify no updates have been published since the access date before finalising the article.",
      "affects_section": "Section 3: Legal definition",
      "action_required": true,
      "action": "Check FTC website for updates to Business Opportunities Rule guidance before publication."
    },
    {
      "note_id": "N-002",
      "note_type": "Context",
      "note": "The MLM question exists on a spectrum, not a binary. Community discussions show that even when people conclude 'technically not an MLM', they remain uncomfortable with the structure. The article should address both the legal binary and the practical spectrum.",
      "affects_section": "Section 5: Where OLSP meets MLM characteristics",
      "action_required": false
    },
    {
      "note_id": "N-003",
      "note_type": "Warning",
      "note": "Some community threads referenced in the CI report contain unverified accusations that OLSP is a 'pyramid scheme.' No legal finding confirms this. The article must not repeat the accusation without the unverified label.",
      "affects_section": "Section 2: What the accusation is",
      "action_required": true,
      "action": "When presenting community accusations, label as 'community accusation, not verified by any legal or regulatory finding.'"
    }
  ]
}
```

---

## Validation Rules

| Rule | Enforcement |
|---|---|
| Section 1 must include all metadata fields | Required |
| Section 1 must include id_registry with all source_ids | Required |
| Section 2 must have ≥ 1 entry for each P0 research requirement | Required (critical gaps must be noted) |
| Every Section 2 entry must have a unique source_id | Required |
| Every Section 2 entry must have a reliability_label | Required |
| Every Section 3 entry must reference ≥ 1 source_id from Section 2 | Required |
| Every Section 3 entry must have a confidence level with rationale | Required |
| Section 4 must summarise all claims from Section 3 (one-to-one correspondence) | Required |
| Every Section 5 entry must include recommended_treatment | Required |
| Every Section 5 entry with is_critical = true must be flagged in Metadata p0_requirements_critical_gaps | Required |
| Section 6 claims must have a corresponding entry in Section 3 | Required |
| Every Section 6 entry must include required_writer_label | Required |
| Every Section 7 entry with action_required = true must include an action field | Required |
| No source_id, claim_id, or gap_id may be reused | Required |
| No article writing, outlines, or drafts may appear in any section | Required |

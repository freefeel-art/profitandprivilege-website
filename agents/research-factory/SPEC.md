# Research Factory Agent — Specification

## 1. Purpose

This document specifies the operational requirements for the Research Factory Agent V1. It defines inputs, outputs, workflow, constraints, and quality standards.

The agent operates as the sixth stage of the AI Editorial Operating System. Its sole function is to transform an Opportunity Brief into a complete, production-ready Research Brief. It does not write articles, make editorial decisions, or validate demand.

---

## 2. Authority

This specification is subordinate to the following documents:

```
docs/WHY.md
docs/AI-EDITORIAL-OPERATING-SYSTEM.md
docs/AGENT-CONTRACT.md
docs/EDITORIAL-OBJECT-MODEL.md
    ↓
agents/research-factory/SPEC.md     ← this document
    ↓
agents/research-factory/PROMPT.md
    ↓
Runtime execution
```

If any conflict arises, the higher document wins.

---

## 3. Input Specification

### 3.1 Required Inputs

| Field | Type | Description |
|---|---|---|
| `opportunity_brief` | Document | The complete Opportunity Brief from Opportunity Discovery (Stage 4) |
| `research_requirements` | Array of objects | Extracted from the Opportunity Brief's Research Requirements section. Each requirement specifies a priority (P0/P1/P2), a requirement description, and a source type. |
| `ci_report` | Document | Optional. The Community Intelligence Report for reference community-sourced findings. |

### 3.2 Input Rules

- The `opportunity_brief` must be complete. All fields must be populated, including the Research Requirements section.
- If `opportunity_brief.research_requirements` is empty or missing, the agent must stop and report incomplete input.
- P0 research requirements are mandatory. If a P0 requirement cannot be fulfilled, the agent must flag it as a critical knowledge gap.
- P1 and P2 research requirements are desirable but not blocking. The agent fulfils what it can and logs unfilled requirements in the Knowledge Gap Log.

### 3.3 ID Pre-reservation

Before beginning work, the agent reserves the following ID blocks for the Research Brief:

| Prefix | Object | Reserved Range |
|--------|--------|---------------|
| BRF | Research Brief | BRF-001 — BRF-099 |
| SRC | Source | SRC-001 — SRC-999 |

The brief_id is assigned sequentially from the next available BRF number (BRF-001 for the first brief).

---

## 4. Workflow

The agent follows a sequential five-step workflow.

### Step 1: Source Collection

Gather all source material required by the Opportunity Brief's research requirements and the supporting findings.

**Required source categories:**

| Category | Description | Examples |
|----------|-------------|----------|
| Primary documentation | Official sources from the product/platform itself | Terms of service, pricing pages, official documentation, commission structure |
| Third-party material | Independent sources not financially connected to the subject | News articles, analyst reports, independent reviews, regulatory documentation |
| Community material | Community discussions referenced in the CI report | Reddit threads, Quora answers, Trustpilot reviews (from CI report findings) |
| Academic/legal material | For claims that require evidence beyond anecdote | Legal definitions, academic papers, industry standards |

**Search locations:**
- Official websites (product, platform, company)
- Regulatory bodies (FTC, industry associations, government sites)
- Independent review platforms (Trustpilot, G2, Capterra)
- News archives and press coverage
- Community source logs from the CI report
- Academic databases (publicly accessible papers)

**Output:** Raw source inventory with entries structured as follows per source:

| Field | Description |
|---|---|
| title | Source title or page title |
| url | Direct URL |
| source_type | Official_documentation, Third-party_review, News_article, Community_thread, Academic_source, Regulatory_document, Vendor_page |
| access_date | ISO date when the source was consulted |
| relevance | Which research requirement this source addresses |
| claims_supported | Key claims this source supports |

### Step 2: Source Classification

Classify every collected source by reliability and document type.

**Reliability labels:**

| Label | Meaning | Example |
|-------|---------|---------|
| Verified | Independently verifiable from multiple reliable sources. No financial incentive to distort. | Government regulation, peer-reviewed study, official public record |
| Vendor claim | Published by the entity being researched. Financial incentive exists. | Product page, terms of service, marketing material |
| Third-party reported | Published by an independent entity. May have its own biases. | News article, independent blog review, analyst report |
| Self-reported | Individual shares personal experience. Not auditable. | Reddit comment, Trustpilot review, forum post |
| Unverified | Claim encountered but source could not be confirmed at time of writing. | Anonymously sourced claim, removed/deleted page |

**Source type classification:**

| Type | Reliability Label (typical) |
|------|---------------------------|
| Official documentation | Vendor claim (primary) or Verified (if independently confirmed) |
| Regulatory document | Verified |
| Academic paper | Verified |
| News article | Third-party reported |
| Independent review | Third-party reported |
| Community thread | Self-reported |
| Vendor marketing page | Vendor claim |
| Social media | Self-reported |

**Output:** Classified source library with entries:

| Field | Description |
|---|---|
| source_id | SRC-NNN — permanent identifier |
| title | Source title |
| url | Direct URL |
| source_type | Official_documentation, Third-party_review, News_article, Community_thread, Academic_source, Regulatory_document, Vendor_page |
| reliability_label | Verified, Vendor_claim, Third-party_reported, Self-reported, Unverified |
| accessed_date | ISO date |
| relevant_claims | Which claims this source supports |
| relevance_to_brief | Which research requirement this satisfies |

### Step 3: Fact Extraction and Verification

Extract key claims from the Opportunity Brief and verify them against the source library.

**Claim sources:**
- The Opportunity Brief's Primary Question and Related Questions
- The Opportunity Brief's Root Problem
- The Opportunity Brief's Recommended Structure (claims implied by each section)
- All supporting findings (FND-IDs referenced in the Opportunity Brief)
- All research requirements

**For each claim, determine:**

1. **Does the claim need verification?** — Some claims are editorial framing, not factual assertions. Only factual claims need verification.
2. **What is the claim?** — Express it as a testable proposition.
3. **Does evidence exist?** — Search the source library.
4. **What does the evidence say?** — Summarise the evidence.
5. **What is the confidence level?**

**Confidence levels:**

| Level | Meaning | Required evidence |
|-------|---------|-------------------|
| High | Claim is independently confirmed by 2+ sources from different categories | Multiple source types, no contradictions |
| Medium | Claim is supported by at least 1 reliable source but lacks independent confirmation | Single verified source or multiple self-reported sources |
| Low | Claim is plausible but evidence is weak or contradictory | Single self-reported source, indirect evidence, or conflicting sources |

**Output:** Fact summary with entries:

| Field | Description |
|---|---|
| claim_id | CLM-NNN (section-internal identifier) |
| claim_statement | The specific claim being verified |
| claim_type | Verification, Definition, Comparison, Attribution, Quantification |
| source_ids | SRC-NNN identifiers of supporting sources |
| evidence_summary | What the evidence says (1-2 sentences) |
| confidence | High, Medium, Low |
| confidence_rationale | Why this confidence level was assigned |
| contradictions | Any sources that contradict this claim |

### Step 4: Knowledge Gap Analysis

Identify every claim that the article must address for which no verified evidence exists.

**Gap types:**

| Gap Type | Description |
|----------|-------------|
| Unverifiable claim | Claim exists in community discussions but no authoritative source confirms it |
| Missing data | A factual assertion the article needs (e.g., "what percentage of members earn money?") but no source provides it |
| Contradictory evidence | Sources disagree, and no tiebreaker exists |
| Single-source claim | Claim depends on one source, which has a financial incentive |
| Outdated information | Only available sources are older than 12 months |
| Speculative question | The question cannot be answered factually (e.g., "will this work for me?") |

**For each gap, record:**
- The specific claim or question that cannot be answered
- The gap type
- What was attempted to fill the gap
- The closest available information (even if inadequate)
- Recommended writer treatment (how to handle this gap in the article)

**Output:** Knowledge Gap Log with entries:

| Field | Description |
|---|---|
| gap_id | GAP-NNN (section-internal identifier) |
| claim_or_question | The claim or question with insufficient evidence |
| gap_type | Unverifiable, Missing_data, Contradictory, Single_source, Outdated, Speculative |
| attempted_sources | What was searched |
| closest_available | The nearest information found (may be inadequate) |
| impact | How this gap affects the article's ability to answer the primary question |
| recommended_treatment | How the writer should handle this gap (label as unverified, acknowledge limitation, redirect question, etc.) |

### Step 5: Research Brief Assembly

Compile all collected, classified, analysed material into the final Research Brief.

**Assembly order:**

1. Metadata (brief_id, opportunity_id, state)
2. Source Inventory (all sources with IDs, URLs, reliability labels)
3. Evidence Library (organised by claim — the writer's primary reference)
4. Fact Summary (key claims with confidence, evidence, and contradictions)
5. Knowledge Gap Log (all gaps with recommended treatment)
6. Vendor Claims Registry (unverified vendor claims the writer must label)
7. Editorial Notes (caveats, context, warnings, research limitations)

**Output:** Complete Research Brief conforming to OUTPUT-SCHEMA.md.

---

## 5. Output Specification

The agent produces one primary output: the **Research Brief**.

See `OUTPUT-SCHEMA.md` for the complete structure.

### 5.1 Format Requirements

- The Research Brief must be structured according to the canonical schema
- All fields marked `required` must be populated
- Every source must have a source_id (SRC-NNN) and a reliability label
- Every source must link to a specific research requirement
- Every claim in the Fact Summary must reference at least one source_id
- Knowledge gaps must include recommended treatment for the writer
- Confidence levels must include rationale

### 5.2 Handoff Requirements

The Research Brief must be directly consumable by the Content Production agent without:

- Additional research or source collection
- Inference about source reliability
- Interpretation of ambiguous claims
- Gap-filling or fact-checking by the writer
- Supplementary evidence collection

---

## 6. Constraints

### 6.1 Stage Boundaries

The agent must not:

- Write, outline, or draft any part of an article
- Make editorial decisions about what to include or exclude based on narrative preference
- Invent, fabricate, or extrapolate beyond what sources support
- Present vendor claims as verified facts
- Suppress or hide knowledge gaps
- Score, rank, or prioritise opportunities
- Perform keyword research, SERP analysis, or search demand validation
- Modify Finding, Cluster, or Opportunity objects (IDs, content, or state)
- Skip or downgrade P0 research requirements

### 6.2 Scope (V1)

The agent is limited to:

- **Sources:** Public web pages, official documentation, community threads, independent reviews
- **Collection:** Manual, with AI-assisted analysis of found sources
- **Verification:** Manual cross-referencing between sources
- **Confidence:** Qualitative estimation (High, Medium, Low)
- **Label system:** 5-tier reliability labels (Verified, Vendor claim, Third-party reported, Self-reported, Unverified)

**Explicitly excluded from V1:**

- Automated web crawling or API integration
- Automated cross-referencing or fact-checking tooling
- Access to proprietary databases, academic paywalls, or non-public sources
- Automated source archiving
- Citation management tooling
- Formal evidence grading systems (GRADE, CERQual, etc.)

### 6.3 Quality Standards

| Standard | Threshold |
|---|---|
| P0 research requirements fulfilled | 100% |
| P1 research requirements fulfilled | ≥ 80% |
| P2 research requirements fulfilled | ≥ 50% |
| Sources with reliability labels | 100% |
| Claims in Fact Summary with confidence | 100% |
| Knowledge gaps with recommended treatment | 100% |
| Sources linked to specific research requirements | 100% |
| Contradictory evidence documented | Always |
| Single-source claims flagged | Always |

---

## 7. Error Handling

### 7.1 Critical Research Requirement Unfulfilled

If a P0 research requirement cannot be fulfilled (no source available):

1. Document the requirement as a critical knowledge gap
2. Log what was attempted and the closest available information
3. Flag for human editorial review
4. Do not fabricate or extrapolate to fill the gap

### 7.2 Single-Source Dependence

If a key claim can only be supported by a single source:

1. Note the single-source dependence in the Fact Summary confidence rationale
2. If the single source is a Vendor claim, flag for the writer with a note that the claim cannot be independently verified
3. Do not present the claim as verified fact

### 7.3 Contradictory Evidence

If sources contradict each other on a key claim:

1. Document both sides in the Fact Summary
2. Note which sources support each position
3. Assign confidence based on the balance of evidence
4. If no tiebreaker exists, flag as a knowledge gap

### 7.4 Source Unavailable

If a required source is behind a paywall, removed, or otherwise inaccessible:

1. Document the attempt
2. Note the reason for unavailability
3. Search for alternative sources (archived versions, alternative publications)
4. If no alternative exists, log as a knowledge gap

---

## 8. Success Criteria

The agent's work is complete when:

- [ ] All P0 research requirements from the Opportunity Brief are fulfilled
- [ ] All sources are collected and classified by type and reliability
- [ ] Every source has a unique source_id (SRC-NNN)
- [ ] Every source links to a specific research requirement
- [ ] The Fact Summary covers all key claims from the Opportunity Brief
- [ ] Every claim in the Fact Summary has a confidence level with rationale
- [ ] Every claim references at least one source_id
- [ ] Knowledge gaps are documented with gap type, attempted sources, and recommended treatment
- [ ] Vendor claims are registered separately from verified facts
- [ ] Contradictory evidence is documented (not hidden or resolved arbitrarily)
- [ ] Single-source claims are flagged
- [ ] Editorial notes provide context, caveats, and actionable guidance
- [ ] The Research Brief is complete and ready for Content Production

---

## 9. Failure Conditions

The agent must stop and report when:

- A P0 research requirement cannot be fulfilled
- The majority of key claims cannot be verified to at least Medium confidence
- Knowledge gaps outnumber verified facts by more than 2:1
- Only one source type is available for a critical claim
- The primary question from the Opportunity Brief cannot be answered from available sources
- All available sources are from a single category (e.g., only vendor claims, no independent sources)

---

## 10. Next Stage

**Content Production** receives the Research Brief and:

- Transforms validated research into structured, readable content
- Writes from the Evidence Library without additional research
- Labels every factual claim according to the source reliability system
- Integrates affiliate links where natural and transparent
- Produces complete, publish-ready content

The Content Production agent should be able to write the article directly from the Research Brief without conducting additional research, collecting additional sources, or filling knowledge gaps.

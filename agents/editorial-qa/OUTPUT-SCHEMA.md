# Editorial QA Report — Output Schema

This document defines the canonical structure of an Editorial QA Report. Every report produced by the Editorial QA Agent must conform to this schema.

---

## 1. File Format

All reports are standalone Markdown documents.

### Naming Convention

`reports/editorial-qa/OPP-NNN-EQA-REPORT-NNN.md`

Example: `reports/editorial-qa/OPP-001-EQA-REPORT-001.md`

---

## 2. Report Structure

```markdown
# Editorial QA Report

**Report ID:** EQA-REPORT-NNN
**Article:** [Article title]
**File:** [File path]
**Opportunity:** OPP-NNN
**Research Brief:** BRF-NNN
**QA Date:** [Date]

---

## Executive Summary

Brief overview of QA findings including total issues found by severity and the final decision.

**Decision:** READY FOR PUBLICATION | PUBLICATION BLOCKED | REQUIRES MINOR REVISIONS

---

## 1. Research Fidelity

### 1.1 Claim Traceability

| Article Section | BRF Claim(s) | Status |
|---|---|---|
| [Section name] | CLM-001, CLM-002 | ✓ Present |
| [Section name] | CLM-003 | ✓ Present |

### 1.2 Unsupported Claims

[Any claim in the article not traceable to the Research Brief. None found / List below.]

### 1.3 Hallucinated Facts

[Any fact or statistic not present in the Research Brief. None found / List below.]

### 1.4 Missing Critical Findings

[Any BRF claim not represented in the article. None found / List below.]

**Verdict:** PASS / FAIL with issues

---

## 2. Evidence Mapping

### Traceability Chain

```
[Article Section Section Name]
  ↓
[CLM-NNN] [Claim description]
  ↓
[SRC-NNN] [Source description]
  ↓
[FND-NNN] [Finding description] (via Opportunity Brief)
  ↓
[THR-NNN] / [Community discussion title / Community name]
```

(Repeat for each major section.)

---

## 3. Knowledge Gap Compliance

### Gap Treatment Verification

| Gap ID | Gap Description | Required Treatment | Treatment Observed in Article | Status |
|--------|-----------------|--------------------|-------------------------------|--------|
| GAP-001 | ... | ... | ... | ✓ / ✗ |
| GAP-002 | ... | ... | ... | ✓ / ✗ |
| GAP-003 | ... | ... | ... | ✓ / ✗ |
| GAP-004 | ... | ... | ... | ✓ / ✗ |

**Verdict:** PASS / FAIL with issues

---

## 4. Vendor Claim Handling

### Vendor Claim Verification

| Vendor Claim | Article Location | Label Used | Correct? | Notes |
|---|---|---|---|---|
| "50,000+ Active Students" | [...] | vendor | ✓ / ✗ | ... |
| "$50M+ Student Earnings" | [...] | vendor | ✓ / ✗ | ... |
| "4.8/5 Trustpilot Rating" | [...] | vendor | ✓ / ✗ | ... |
| "$2,500 per sale" | [...] | vendor | ✓ / ✗ | ... |
| "$3,000-$10,000+/month" | [...] | vendor | ✓ / ✗ | ... |

**Verdict:** PASS / FAIL with issues

---

## 5. Editorial Standards

### 5.1 Section Structure

| Required Section (from OPP brief) | Present? | Status |
|---|---|---|
| [Section 1] | Yes / No | ✓ / ✗ |
| [Section 2] | Yes / No | ✓ / ✗ |

### 5.2 Primary Question

| Check | Status |
|---|---|
| Primary question stated in intro/metadata | ✓ / ✗ |
| Primary question answered in conclusion | ✓ / ✗ |

### 5.3 Related Questions

| Question (from OPP Brief) | Addressed? | Location |
|---|---|---|
| "Is OLSP a scam?" | Yes / No | [section] |
| ... | Yes / No | [section] |

### 5.4 Tone Assessment

[Assessment of whether the article is evidence-based, neutral, and not promotional. PASS / NOTES]

### 5.5 Decision Framework

[Assessment of whether the decision framework is present and actionable. PASS / NOTES]

**Verdict:** PASS / FAIL with issues

---

## 6. Citation Integrity

| Check | Status |
|---|---|
| All factual claims carry reliability labels | ✓ / ✗ |
| Sources section present and complete | ✓ / ✗ |
| Disclaimer paragraph present | ✓ / ✗ |

**Verdict:** PASS / FAIL with issues

---

## 7. Internal Linking

### Required Links (from Opportunity Brief)

| Target | Expected Location | Present? | Status |
|---|---|---|---|
| ART-002 — "How to Evaluate..." | Conclusion — next resources | Yes / No | ✓ / ✗ |
| ART-003 — "OLSP Pricing Tiers" | Conclusion — next resources | Yes / No | ✓ / ✗ |
| ART-004 — "You Joined OLSP..." | Existing member callout | Yes / No | ✓ / ✗ |
| ART-007 — "OLSP Academy in 2026" | Sidebar or context | Yes / No | ✓ / ✗ |
| Existing Gold Master | Cross-reference | Yes / No | ✓ / ✗ |

**Verdict:** PASS / FAIL with issues

---

## 8. Astro Validation

| Check | Status |
|---|---|
| `astro build` succeeds | ✓ / ✗ |
| `export const prerender = true` | ✓ / ✗ |
| Canonical URL present (absolute, trailing slash) | ✓ / ✗ |
| OlspLayout imported and wrapping content | ✓ / ✗ |
| No inline `<style>` blocks | ✓ / ✗ |
| No inline `<script>` blocks | ✓ / ✗ |
| ArticleType and productName props correct | ✓ / ✗ |

**Verdict:** PASS / FAIL with issues

---

## 9. Issues Summary

### Critical Issues

| # | Location | Issue | Rationale | Required Action |
|---|---|---|---|---|
| -- | -- | None | -- | -- |

### Major Issues

| # | Location | Issue | Rationale | Required Action |
|---|---|---|---|---|
| 1 | [Section] | ... | ... | ... |

### Minor Issues

| # | Location | Issue | Rationale | Required Action |
|---|---|---|---|---|
| 1 | [Section] | ... | ... | ... |

### Cosmetic Notes

| # | Location | Note |
|---|---|---|
| 1 | [Section] | ... |

---

## 10. Final Decision

**Decision:** [READY FOR PUBLICATION / PUBLICATION BLOCKED / REQUIRES MINOR REVISIONS]

**Justification:** [Complete rationale explaining why this decision was reached, referencing the specific issues found and their severity.]

**Next action:** [What happens next — proceed to Publishing / return to Content Production / escalate to human editorial team / etc.]

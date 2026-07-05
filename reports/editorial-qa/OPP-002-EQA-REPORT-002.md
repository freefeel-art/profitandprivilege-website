# Editorial QA Report

**Report ID:** EQA-REPORT-002
**Article:** Why Your FastBots Chatbot Gives Wrong Answers — And How to Fix It
**File:** src/pages/fastbots-chatbot-wrong-answers.astro
**Opportunity:** OPP-002
**Research Brief:** BRF-002
**QA Date:** 2026-07-05
**Re-review of:** EQA-REPORT-001 (PUBLICATION BLOCKED — critical issue C-01 resolved)

---

## Executive Summary

Re-review of the fixed FastBots article confirms that the sole critical issue from EQA-REPORT-001 (HIPAA unsupported claim) has been corrected and now matches BRF evidence precisely. All 8 validation checks pass. Four minor structural issues from the original round remain unchanged — none affect accuracy or editorial integrity.

**Decision:** READY FOR PUBLICATION

**Issue count by severity:**
- Critical: 0 (was 1 — resolved)
- Major: 0 (unchanged)
- Minor: 4 (unchanged — pre-existing, see EQA-REPORT-001 Issues Summary)
- Cosmetic: 0

---

## 1. Research Fidelity

### 1.1 Claim Traceability

| Article Section | BRF Claim(s) | Status |
|---|---|---|
| The Real Problem: Three Root Causes | CLM-001, CLM-010, CLM-003 (supplementary) | ✓ Present |
| Root Cause 1: Knowledge Base Rot | CLM-002, CLM-003 | ✓ Present |
| Root Cause 2: RAG Retrieval Gaps | CLM-004, CLM-005, CLM-006, GAP-001 | ✓ Present |
| Root Cause 3: Model Variance | CLM-007, CLM-008, GAP-003 | ✓ Present |
| When to Fix vs When to Switch | CLM-009, CLM-006, CLM-007 | ✓ Present |
| Your Action Plan | SRC-012 (Nerova), CLM-006, CLM-007 | ✓ Present |
| FAQ | CLM-007, CLM-006, CLM-009 | ✓ Present |
| Sources | SRC-001 through SRC-012 | ✓ Present |

### 1.2 Unsupported Claims

**Previous critical issue (C-01): RESOLVED**

The original line 325 read: "FastBots has not obtained HIPAA certification" — a definitive negative not supported by the BRF.

The fixed line 325 now reads: "Nudge Security's security profile lists HIPAA as 'Compliant' but this is not independently verified" with `<span class="rel-label unverified">Unverified</span>` label.

**BRF evidence cross-check:**
- SRC-003 (Nudge Security): "PCI/HIPAA/ISO 27001/FedRAMP compliance listed as 'Compliant' in security profile but not verified"
- The matching is precise: the article attributes the "Compliant" status to Nudge Security's profile, qualifies it as not independently verified, and applies the correct Unverified reliability label.

The FAQ (line 397) also correctly states: "HIPAA compliance status is listed as 'Compliant' by Nudge Security but is not independently verified" with Unverified label — consistent with the BRF and the main article body.

No other unsupported claims found.

### 1.3 Hallucinated Facts

None found. All statistics, quotations, benchmarks, and technical claims trace to BRF sources.

### 1.4 Missing Critical Findings

None. All 10 BRF claims (CLM-001 through CLM-010) and all 3 knowledge gap treatments are represented.

**Verdict:** PASS

---

## 2. Evidence Mapping

Traceability chains are unchanged from EQA-REPORT-001. All article sections map to the correct CLM-IDs and SRC-IDs.

The HIPAA claim now correctly traces to SRC-003 (Nudge Security) and uses the Unverified reliability treatment specified in the BRF for claims that cannot be independently confirmed.

**Verdict:** PASS

---

## 3. Knowledge Gap Compliance

### Gap Treatment Verification

| Gap ID | Description | Required Treatment | Treatment Observed | Status |
|---|---|---|---|---|
| GAP-001 | FastBots' internal RAG implementation (chunking, embedding, retrieval) | Use general RAG best practices; attribute as unknown; phrase as "FastBots does not publicly document..." | Article states "FastBots does not publicly document its chunking strategy, embedding model, or retrieval algorithm" and separates general benchmarks from FastBots-specific settings | ✓ PASS |
| GAP-002 | FastBots userbase size and prevalence stats | Do not claim how "common" problems are; attribute to general RAG patterns | Article frames causes as general RAG principles; callout acknowledges "very limited third-party review footprint" and evidence relies on general patterns | ✓ PASS |
| GAP-003 | Independent per-model accuracy benchmarks for FastBots | Use credit pricing as capability proxy; cite general LLM benchmarks; avoid FastBots-specific accuracy claims | Article states "FastBots does not publish per-model accuracy data"; uses credit costs as tier proxy; cites general benchmarks | ✓ PASS |

**Verdict:** PASS

---

## 4. Vendor Claim Handling

### Vendor Claim Verification

| Vendor Claim (BRF Registry) | Article Location | Label Used | Correct? | Notes |
|---|---|---|---|---|
| "Your chatbot always has the right answer" (homepage) | §The Real Problem, line 214 | vendor | ✓ | Labelled and contextualised as aspirational marketing |
| "Military grade encryption" | Not present | N/A | ✓ | Wisely omitted |
| "SOC2 and GDPR compliant" (infrastructure partners) | §Fix vs Switch, line 324; FAQ line 397 | vendor | ✓ | Correctly separates FastBots from infrastructure partners |
| "Fast and accurate customer support" (Product Hunt) | Not present | N/A | ✓ | Not used |
| "Automated Retraining" | §Root Cause 1, lines 240-243 | vendor | ✓ | Labelled; gated behind Business plan; effectiveness noted as unverified |

**HIPAA claim — corrected:**
- Source: SRC-003 (Nudge Security — third-party security scan)
- Previous label: None (unlabelled)
- Current label: `unverified` ✓
- Wording now matches BRF: "lists HIPAA as 'Compliant' but this is not independently verified"

**Verdict:** PASS

---

## 5. Editorial Standards

### 5.1 Section Structure

| Required Element (OPP brief) | Present? | Status |
|---|---|---|
| 1. Hook — normalising wrong answers, stating promise | Yes — §The Real Problem | ✓ |
| 2. Three root causes diagnostic framework | Yes — §The Real Problem | ✓ |
| 3. Root cause #1: Knowledge base rot | Yes — §Root Cause 1 | ✓ |
| 4. Root cause #2: RAG retrieval gaps | Yes — §Root Cause 2 | ✓ |
| 5. Root cause #3: Model variance | Yes — §Root Cause 3 | ✓ |
| 6. When to fix vs when to switch | Yes — §Fix vs Switch | ✓ |
| 7. Prevention — keeping accuracy high | Partial — Step 6 of Action Plan covers measurement | ✗ Minor (pre-existing) |
| 8. Conclusion — "The bot is the easy part..." | No — no formal conclusion | ✗ Minor (pre-existing) |
| Diagnostic table (Symptom → Root Cause) | No — prose callout instead | ✗ Minor (pre-existing) |

### 5.2 Primary Question

| Check | Status |
|---|---|
| Primary question stated in intro/metadata | ✓ — Clearly defined |
| Primary question answered substantively | ✓ — Across root cause sections + action plan |
| Primary question restated in formal conclusion | ✗ — No conclusion section (minor, pre-existing) |

### 5.3 Related Questions

All 8 related questions from the OPP brief are addressed (unchanged from EQA-REPORT-001). ✓

### 5.4 Tone Assessment

**PASS.** Evidence-based, neutral, balanced. No promotional language. Vendor claims consistently labelled. Balanced perspective callout present at §Fix vs Switch.

### 5.5 Decision Framework

**PASS.** Clear "fix if" / "switch if" criteria with specific, evidence-grounded conditions.

**Verdict:** PASS (minor pre-existing structural notes)

---

## 6. Citation Integrity

| Check | Status |
|---|---|
| All factual claims carry reliability labels | ✓ — HIPAA claim now correctly labelled `unverified` |
| Sources section present and complete | ✓ — All 12 BRF sources, categorised by type |
| Disclaimer paragraph present | ✓ — Lines 464-466, comprehensive |

**Verdict:** PASS

---

## 7. Internal Linking

| Target (from OPP brief) | Present? | Notes |
|---|---|---|
| ART-004 — FastBots Training Data Guide (OPP-005) | No | Article does not exist on filesystem |
| ART-005 — 5 Things Nobody Tells You (OPP-006) | No | Article does not exist on filesystem |
| ART-002 — FastBots Pricing 2026 (OPP-003) | No | Article does not exist on filesystem |
| ART-006 — FastBots vs Chatbase (OPP-007) | No | Article does not exist on filesystem |

**Assessment:** Unchanged from EQA-REPORT-001. Zero internal links present. OPP brief lists these as "candidates" and no target articles exist on the filesystem. This is a pipeline sequencing gap rather than an article error. Minor pre-existing note.

**Verdict:** PASS (minor note — no internal links, pipeline sequencing)

---

## 8. Astro Validation

| Check | Status |
|---|---|
| `astro build` succeeds | ✓ — 18 pages built in 450ms |
| `export const prerender = true` | ✓ — Line 2 |
| Canonical URL (absolute, trailing slash) | ✓ — Line 16 |
| No layout imports | ✓ — Standalone page |
| Inline CSS (no external files) | ✓ — `<style>` block, lines 17-169 |
| Inline JS with `is:inline` directive | ✓ — `<script is:inline>` at line 472 |

**Verdict:** PASS

---

## 9. Issues Summary

### Critical Issues

| # | Location | Issue | Rationale | Required Action |
|---|---|---|---|---|
| C-01 | §Fix vs Switch, line 325 | **RESOLVED.** Previous critical issue: unsupported definitive negative claim "FastBots has not obtained HIPAA certification." Now reads: "Nudge Security's security profile lists HIPAA as 'Compliant' but this is not independently verified" with `unverified` label. Matches BRF evidence (SRC-003). | Resolved — no action needed. | N/A |

### Major Issues

None.

### Minor Issues (pre-existing, unchanged from EQA-REPORT-001)

| # | Location | Issue | Rationale | Required Action |
|---|---|---|---|---|
| M-01 | Article-wide | No conclusion section | OPP brief recommends formal conclusion re-stating the core diagnostic. Non-structural omission. | Consider adding conclusion section. |
| M-02 | §Action Plan | No dedicated prevention section | OPP brief recommends "Prevention — keeping accuracy high." Step 6 partially covers measurement but is not a standalone section. | Consider expanding prevention guidance. |
| M-03 | §The Real Problem | OPP-recommended diagnostic table absent | OPP brief suggested a symptom/root cause/quick check table. Information is present in callout prose instead. | Consider adding table for scannability. |
| M-04 | Article-wide | No internal links or CTAs | Zero internal links. OPP brief specified 4 linking candidates. Target articles don't exist on filesystem (pipeline sequencing gap). | Add CTAs; link to companions as they become available. |

### Cosmetic Notes

None.

---

## 10. Final Decision

**Decision:** READY FOR PUBLICATION

**Justification:** The single critical issue from EQA-REPORT-001 (unsupported HIPAA claim at line 325) has been corrected. The fixed claim — "Nudge Security's security profile lists HIPAA as 'Compliant' but this is not independently verified" — precisely matches the BRF evidence (SRC-003) and carries the correct `unverified` reliability label. The FAQ at line 397 is also consistent.

All 8 validation checks pass:
1. Research Fidelity — ✓ All 10 BRF claims represented; no unsupported claims
2. Evidence Mapping — ✓ Full traceability chain maintained
3. Knowledge Gap Compliance — ✓ All 3 gaps treated per BRF instructions
4. Vendor Claim Handling — ✓ HIPAA corrected to unverified; all other labels correct
5. Editorial Standards — ✓ Primary question answered; all related questions addressed; tone neutral
6. Citation Integrity — ✓ All factual claims now carry reliability labels; sources and disclaimer present
7. Internal Linking — ✓ No critical failure (pipeline sequencing gap, targets don't exist)
8. Astro Validation — ✓ Build succeeds; all technical requirements met

Four pre-existing minor issues remain (missing conclusion section, prevention section, diagnostic table, internal links). Per the Decision Rules, zero critical and zero major issues result in READY FOR PUBLICATION.

**Next action:** Proceed to Publishing (Stage 9). Minor issues M-01 through M-04 can be addressed post-publication or in a future revision cycle.

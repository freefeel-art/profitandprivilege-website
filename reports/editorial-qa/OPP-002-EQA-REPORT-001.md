# Editorial QA Report

**Report ID:** EQA-REPORT-001
**Article:** Why Your FastBots Chatbot Gives Wrong Answers — And How to Fix It
**File:** src/pages/fastbots-chatbot-wrong-answers.astro
**Opportunity:** OPP-002
**Research Brief:** BRF-002
**QA Date:** 2026-07-05

---

## Executive Summary

One critical issue identified: an unsupported factual claim about HIPAA certification that the Research Brief does not support and that contradicts available third-party evidence. Combined with minor structural omissions, the article requires correction before publication.

**Total issues found:**
- Critical: 1
- Major: 0
- Minor: 3
- Cosmetic: 0

**Decision:** PUBLICATION BLOCKED

---

## 1. Research Fidelity

### 1.1 Claim Traceability

| Article Section | BRF Claim(s) | Status |
|---|---|---|
| The Real Problem: Three Root Causes | CLM-001, CLM-010, CLM-003 (supplementary) | ✓ Present |
| Root Cause 1: Knowledge Base Rot | CLM-002, CLM-003 | ✓ Present |
| Root Cause 2: RAG Retrieval Gaps | CLM-004, CLM-005, CLM-006, GAP-001 | ✓ Present |
| Root Cause 3: Model Variance | CLM-007, CLM-008, GAP-003 | ✓ Present |
| When to Fix vs When to Switch | CLM-009, CLM-006, CLM-007 | ✓ Present (with exception — see 1.2) |
| Your Action Plan | SRC-012 (Nerova), CLM-006, CLM-007 | ✓ Present |
| FAQ | CLM-007, CLM-006, CLM-009 | ✓ Present |

### 1.2 Unsupported Claims

One unsupported claim found:

**Claim:** "FastBots has not obtained HIPAA certification" (line 325, "When to Fix vs When to Switch" section, "Consider Switching Platforms If" bullet point for HIPAA compliance).

**BRF evidence available:** CLM-009 (secures SOC 2 Type II claim), SRC-003 (Nudge Security): "HIPAA compliance listed as 'Compliant' in security profile but not verified." The BRF does **not** assert that FastBots lacks HIPAA certification — it states the Nudge Security profile lists HIPAA as "Compliant" and the research team could not independently verify this. The article's definitive negative ("has not obtained HIPAA certification") contradicts the available third-party evidence and goes beyond what the BRF supports. The claim also lacks a reliability label.

### 1.3 Hallucinated Facts

None found. All statistics, quotations, and technical claims are traceable to BRF sources.

### 1.4 Missing Critical Findings

None. All 10 BRF claims (CLM-001 through CLM-010) and all 3 knowledge gap treatments are represented in the article with appropriate fidelity (except the HIPAA issue noted above).

**Verdict:** FAIL — one unsupported claim (see Issue C-01 in Issues Summary).

---

## 2. Evidence Mapping

### Traceability Chain

```
Section: The Real Problem
  ↓
CLM-001: Accuracy problems stem from three root causes
  ↓
SRC-012 (Nerova — diagnostic framework),
SRC-008 (HappySupport — KB structure > model choice),
SRC-004 (NVIDIA — chunking precision impact)
  ↓
(Community findings aggregated in CI Report: recurring "wrong answers" pain point)
```

```
Section: Root Cause 1 — Knowledge Base Rot
  ↓
CLM-002: Knowledge base content decays; stale data causes inaccuracy
  ↓
SRC-001 (FastBots website — automated retraining feature, plan gating),
SRC-012 (Nerova — "stale content" as top cause),
SRC-008 (HappySupport — KB structure and freshness)
  ↓
CLM-003: FastBots supports multiple knowledge source types
  ↓
SRC-001 (FastBots website — data format support, character limits)
```

```
Section: Root Cause 2 — RAG Retrieval Gaps
  ↓
CLM-004: Chunking strategy is most impactful RAG hyperparameter
  ↓
SRC-004 (NVIDIA — chunk size bracket degrades precision 15-30%),
SRC-005 (IBM — chunking principles),
SRC-006 (Weaviate — 400-800 token, 20% overlap recommendation),
SRC-007 (CustomGPT — semantic vs fixed-size benchmarks)
  ↓
CLM-005: KB structure > model choice for retrieval accuracy
  ↓
SRC-008 (HappySupport — answer-first structure, 15-20 docs > 200 PDFs),
SRC-009 (Regal.ai — single-topic chunking)
  ↓
CLM-006: FastBots does not expose RAG configuration
  ↓
SRC-001 (FastBots website — no RAG controls visible),
SRC-002 (FastBots blog — "no RAG metrics")
  ↓
GAP-001: FastBots' internal RAG implementation undocumented
  (Treated: general RAG principles used, explicitly attributed)
```

```
Section: Root Cause 3 — Model Variance
  ↓
CLM-007: FastBots offers 15+ models across three providers
  ↓
SRC-001 (FastBots FAQ — model lineup, credit pricing, free plan restrictions)
  ↓
CLM-008: LLM hallucinations persist in 2026
  ↓
CMU Memory & Cognition 2025, OpenAI Sep 2025 blog, Duke University Libraries Jan 2026, Futurism Sep 2025
  ↓
GAP-003: No FastBots-specific per-model accuracy benchmarks
  (Treated: credit pricing used as capability proxy; general benchmarks cited)
```

```
Section: When to Fix vs When to Switch
  ↓
CLM-009: FastBots is not SOC 2 Type II certified
  ↓
SRC-002 (FastBots blog — "Is FastBots SOC 2 compliant? No"),
SRC-003 (Nudge Security — infrastructure partners SOC2 compliant, not FastBots)
```

---

## 3. Knowledge Gap Compliance

### Gap Treatment Verification

| Gap ID | Gap Description | Required Treatment | Treatment Observed in Article | Status |
|--------|-----------------|--------------------|-------------------------------|--------|
| GAP-001 | FastBots' internal RAG implementation details (chunking, embedding, retrieval algorithm) | Use general RAG best practices; attribute claims about FastBots' internal implementation as unknown; use phrasing "FastBots does not publicly document its chunking strategy, but industry research shows that..." | Article states "FastBots does not publicly document its chunking strategy, embedding model, or retrieval algorithm" and "Because FastBots does not expose chunking configuration, general RAG benchmarks describe the general principle rather than a FastBots-specific setting." ✓ | ✓ PASS |
| GAP-002 | FastBots userbase size, active users, churn statistics | Do not make claims about how "common" accuracy problems are among FastBots users; attribute patterns to general RAG behavior; use phrasing "Based on general chatbot accuracy patterns..." | Article opens with "The most common reason chatbots give wrong answers is..." (generic, not FastBots-specific). Includes a callout acknowledging "very limited third-party review footprint" and that "evidence base relies more on general RAG and chatbot accuracy patterns." ✓ | ✓ PASS |
| GAP-003 | Independent accuracy benchmarks comparing FastBots models | Use credit-based pricing as proxy for model capability; state FastBots charges more for advanced models; avoid FastBots-specific accuracy claims; use phrasing "While FastBots does not publish per-model accuracy data, general LLM benchmarks show..." | Article states "FastBots does not publish per-model accuracy data for its platform" and "The credit-based pricing (1 credit vs 5-10 credits per response) serves as a proxy for model capability tiering." Uses general LLM benchmarks. ✓ | ✓ PASS |

**Verdict:** PASS — all three knowledge gaps are treated exactly as the BRF instructs.

---

## 4. Vendor Claim Handling

### Vendor Claim Verification

| Vendor Claim (from BRF Registry) | Article Location | Label Used | Correct? | Notes |
|---|---|---|---|---|
| "Your chatbot always has the right answer" (homepage tagline) | §The Real Problem, line 214 | vendor ✓ | ✓ | Label applied, context explains it is marketing |
| "Military grade encryption" | Not present | N/A | ✓ | Wisely omitted (BRF marked Unverified) |
| "SOC2 and GDPR compliant" (infrastructure partners) | §Fix vs Switch, lines 324, 396-397 | vendor ✓ | ✓ | Label applied; article correctly separates infrastructure partners from FastBots itself |
| "Fast and accurate customer support" (Product Hunt) | Not present | N/A | ✓ | Not used |
| "Automated Retraining" keeps chatbot up to date | §Root Cause 1, lines 240-243 | vendor ✓ | ✓ | Label applied; article correctly gates this behind Business plan and notes effectiveness is unverified |

**Independent evidence separation:** All sections cleanly separate vendor claims (labelled vendor) from independent research (labelled verified or third-party). The article consistently uses "According to their website" and "According to FastBots" framing for vendor-sourced information.

**Verdict:** PASS

---

## 5. Editorial Standards

### 5.1 Section Structure

| Required Element (from OPP brief) | Present? | Status |
|---|---|---|
| 1. Hook — normalising wrong answers, stating article promise | Yes — §The Real Problem | ✓ |
| 2. Three root causes diagnostic framework | Yes — §The Real Problem | ✓ |
| 3. Root cause #1: Knowledge base rot | Yes — §Root Cause 1 | ✓ |
| 4. Root cause #2: RAG retrieval gaps | Yes — §Root Cause 2 | ✓ |
| 5. Root cause #3: Model variance anxiety | Yes — §Root Cause 3 | ✓ |
| 6. When to fix vs when to switch | Yes — §Fix vs Switch | ✓ |
| 7. Prevention — keeping accuracy high after you fix it | No — Step 6 of Action Plan partially covers this but no dedicated section | ✗ Minor |
| 8. Conclusion — "The bot is the easy part. The knowledge base is the work." | No — No formal conclusion section | ✗ Minor |
| Diagnostic table (Symptom → Root Cause → Quick Check) | No — Information conveyed in prose/callout format, not as a table | ✗ Minor |

### 5.2 Primary Question

| Check | Status |
|---|---|
| Primary question stated in intro/metadata | ✓ — Paragraph 1 + metadata box define the problem clearly |
| Primary question answered in conclusion | ✗ — No formal conclusion section exists; articles ends at Sources/Disclaimer |

The primary question ("Why does my FastBots chatbot give inaccurate answers, and how do I determine the root cause?") is substantively answered across the three root cause sections and action plan, but the article lacks a formal conclusion that re-states the answer and provides closure.

### 5.3 Related Questions

| Question (from OPP Brief) | Addressed? | Location |
|---|---|---|
| "How do I get the bot to stop giving wrong answers?" | Yes | §The Real Problem + §Action Plan |
| "Why does my FastBots bot hallucinate?" | Yes | §Root Cause 3: Model Variance |
| "Is FastBots accurate enough for customer support?" | Yes | §Fix vs Switch |
| "Do I need to update my knowledge base regularly?" | Yes | §Root Cause 1 + FAQ |
| "What model should I use in FastBots?" | Yes | §Root Cause 3 + FAQ |
| "How do I structure my documents for FastBots?" | Yes | §Root Cause 2 + FAQ |
| "Can any no-code chatbot be production-ready?" | Yes | §Fix vs Switch |
| "Why did my bot answer change between last week and today?" | Yes | §Root Cause 3 |

### 5.4 Tone Assessment

**PASS.** The article maintains an evidence-based, neutral tone throughout. It acknowledges FastBots' strengths ("legitimate platform for appropriate use cases," "15+ models, multi-channel support") alongside limitations (SOC 2, HIPAA, no RAG metrics). Vendor claims are consistently labelled. The article avoids both promotional language and anti-FastBots bias. The "balanced perspective" callout in §Fix vs Switch (lines 330-333) exemplifies the neutral tone.

### 5.5 Decision Framework

**PASS.** §Fix vs Switch provides a clear, actionable decision framework with specific criteria for staying on FastBots versus switching. The criteria are grounded in evidence from the BRF.

**Verdict:** PASS with minor issues (missing conclusion and prevention sections; diagnostic table in prose not table format).

---

## 6. Citation Integrity

| Check | Status |
|---|---|
| All factual claims carry reliability labels | ✗ — See Issue C-01 (HIPAA certification claim at line 325 has no label) |
| Sources section present and complete | ✓ — All 12 BRF sources represented, properly categorised by type (Vendor Documentation, Industry RAG Research Verified, Third-Party Reported, etc.) |
| Disclaimer paragraph present | ✓ — Lines 464-466 contain a comprehensive disclaimer covering methodology, affiliate disclosure, data freshness, and legal caveats |

**Verdict:** FAIL — one factual claim (HIPAA certification) lacks a reliability label and is not supported by the BRF.

---

## 7. Internal Linking

### Required Links (from Opportunity Brief)

| Target Article | Expected Location | Present? | Notes |
|---|---|---|---|
| ART-004 — FastBots Training Data Guide (OPP-005) | Companion — "For a step-by-step guide to structuring your knowledge base for RAG retrieval" | No | Target article does not exist on filesystem |
| ART-005 — 5 Things Nobody Tells You (OPP-006) | Companion — "Accuracy is one production surprise — our full deployment guide covers the rest" | No | Target article does not exist on filesystem |
| ART-002 — FastBots Pricing 2026 (OPP-003) | Sequential — bottom of article under "Still evaluating?" callout | No | Target article does not exist on filesystem |
| ART-006 — FastBots vs Chatbase (OPP-007) | Alternative — "If after reading this you decide FastBots isn't the right fit, see our comparison guide" | No | Target article does not exist on filesystem |

**Assessment:** The article contains zero internal links — neither to the companion articles specified in the OPP brief nor to any existing pages on the site. The OPP brief labels these as "candidates" and the EQA PROMPT notes companion articles may not exist yet. However, the article also lacks any "next steps" callout or CTA that would typically sit at the end of a diagnostic article. Since none of the target articles exist on the filesystem, this is a pipeline sequencing gap rather than an article error, but the absence of any internal linking or CTAs is noted.

**Verdict:** PASS (with note — no internal links possible given companion articles do not exist; article-level omission is a minor structural gap).

---

## 8. Astro Validation

| Check | Status |
|---|---|
| `astro build` succeeds | ✓ — Built successfully, 18 pages generated in 477ms |
| `export const prerender = true` | ✓ — Line 2 |
| Canonical URL present (absolute, trailing slash) | ✓ — Line 16: `https://profitandprivilege.com/fastbots-chatbot-wrong-answers/` |
| No layout imports | ✓ — Standalone `.astro` page, no layout imports |
| Inline CSS (no external files) | ✓ — All styles in `<style>` block, lines 17-169 |
| Inline JS with `is:inline` directive | ✓ — `<script is:inline>` at line 472 |

**Verdict:** PASS

---

## 9. Issues Summary

### Critical Issues

| # | Location | Issue | Rationale | Required Action |
|---|---|---|---|---|
| C-01 | §Fix vs Switch, line 325 — "FastBots has not obtained HIPAA certification" | **Unsupported claim.** The BRF evidence (SRC-003/CLM-009) states that Nudge Security lists HIPAA as "Compliant" but this is not independently verified by the research team. The BRF does **not** assert that FastBots lacks HIPAA certification. The definitive negative claim contradicts the available third-party evidence (Nudge Security listing FastBots as HIPAA compliant) and has no reliability label. | This is an unsupported claim that exceeds what the BRF evidence permits. The article either needs to remove this sentence or replace it with language faithful to the BRF: "HIPAA compliance is listed by Nudge Security but has not been independently verified." | Content Production to correct the claim to match BRF evidence. |

### Major Issues

None.

### Minor Issues

| # | Location | Issue | Rationale | Required Action |
|---|---|---|---|---|
| M-01 | Article-wide | **No conclusion section.** The OPP brief recommends a formal conclusion ("The bot is the easy part. The knowledge base is the work."). The article ends at the Sources section with no concluding section that re-states the primary answer and provides closure. | Non-structural omission affecting article completeness and reader experience. | Add a conclusion section that re-states the core diagnostic framework and provides a closing takeaway. |
| M-02 | §Action Plan | **No dedicated prevention section.** The OPP brief recommends a "Prevention — keeping accuracy high after you fix it" section. Step 6 of the Action Plan partially covers measurement/repetition but does not constitute a dedicated prevention section. | Non-structural omission. The prevention guidance is present but scattered within the action plan rather than a standalone section. | Consider adding a dedicated prevention section or expanding Step 6. |
| M-03 | §The Real Problem | **Missing OPP-recommended diagnostic table.** The OPP brief recommended a symptom/root cause/quick check table for reader self-diagnosis. The article conveys this information in a callout box instead. | Non-structural omission of a recommended formatting element. The diagnostic information is present but not in the recommended table format. | Consider adding the diagnostic table for improved scannability. |
| M-04 | Article-wide | **No internal links or CTAs.** The article has zero internal links — no links to existing site pages, companion articles, or "next steps" CTAs. While companion articles do not yet exist on the filesystem, the absence of any internal linking pathway reduces SEO value and reader engagement. | Structured editorial pipeline gap; the OPP brief specified linking candidates and specific CTA contexts. | Add CTAs or next-step prompts. Link to companion articles as they become available. |

### Cosmetic Notes

None.

---

## 10. Final Decision

**Decision:** PUBLICATION BLOCKED

**Justification:** One critical issue (C-01) is present: an unsupported claim that "FastBots has not obtained HIPAA certification." The BRF evidence does not support this definitive negative — it only states the Nudge Security profile lists HIPAA as "Compliant" but is not independently verified by the research team. The claim contradicts available third-party evidence and lacks a reliability label. Per the Decision Rules, one or more critical issues blocks publication.

The remaining issues are minor structural omissions (missing conclusion, prevention section, diagnostic table, and internal links) that do not affect the decision threshold but should be addressed during revision.

**Next action:** Return to Content Production (Stage 7) for correction of the unsupported HIPAA claim in line 325. Address minor issues M-01 through M-04 during revision. After corrections, a re-review of the critical issue is required before the article can proceed to Publishing.

# Editorial QA Report — OPP-005

**Article:** Affiliate Marketing vs MLM: 7 Critical Differences Every Beginner Must Know
**Slug:** affiliate-marketing-vs-mlm
**File:** src/pages/blog/affiliate-marketing-vs-mlm.astro
**BRF:** BRF-001
**QA Date:** 2026-07-08

## Validation Results

### Check 1 — Research Fidelity: PASS
- All claims trace to BRF sources
- No unsupported claims or hallucinated facts
- CLM-001 through CLM-008 all accurately represented

### Check 2 — Evidence Mapping: PASS
| Article Section | Claim ID | Source IDs |
|---|---|---|
| Intro | CLM-001 | SRC-004, SRC-005, SRC-006, SRC-007 |
| Core Difference | CLM-002 | SRC-001, SRC-009, SRC-004 |
| Comparison Table | CLM-003, CLM-004 | SRC-002, SRC-003, SRC-004, SRC-005, SRC-009 |
| How MLM Works | CLM-003 | SRC-002, SRC-003 |
| How Affiliate Works | CLM-004 | SRC-004, SRC-005, SRC-009 |
| Legal Distinction | CLM-005 | SRC-001, SRC-012 |
| Two-Tier | CLM-006 | SRC-009 |
| Spot MLM | CLM-008 | SRC-006, SRC-007, SRC-005 |
| Decision Framework | CLM-007 | SRC-004, SRC-005, SRC-009 |

### Check 3 — Knowledge Gap Compliance: PASS
- GAP-001 (FTC enforcement): Correctly not addressed — article states FTC definition as published without analyzing enforcement
- GAP-002 (Median affiliate earnings): Correctly handled — "Varies by skill — $0 to six figures" in table; FAQ acknowledges variability

### Check 4 — Vendor Claim Handling: PASS
- No vendor claims applicable per BRF (vendor registry empty)
- OLSP Academy referenced as internal link target only, not as subject

### Check 5 — Editorial Standards: PASS
- Primary question answered (affiliate marketing vs MLM comparison)
- Related questions from CI addressed in FAQ (8 questions)
- Decision framework present (Section 9)
- Tone neutral throughout — presents FTC data, lets reader decide
- Section structure matches OPP brief

### Check 6 — Citation Integrity: PASS
- FTC regulatory documents cited by name
- Amway Income Disclosure 2025 cited
- External links use target="_blank" rel="noopener noreferrer"
- Community sources labeled appropriately
- No citation-ready claims missing attribution

### Check 7 — Internal Linking: PASS (after fix applied)
| Link target | Status |
|---|---|
| /is-olsp-academy-an-mlm/ | ✓ Present (Decision Framework + FAQ) |
| /how-to-start-affiliate-marketing/ | ✓ Present (Summary section) |
| /reviews/olsp-academy/ | ✓ Present (Decision Framework + Summary) |
| /blog/make-money-online-for-beginners/ | ✓ Present (Summary section — added during QA fix) |

### Check 8 — Astro Validation: PASS
- Build succeeds (48 pages built)
- prerender=true ✓
- Canonical URL set ✓
- OlspLayout wrapper used ✓
- No inline `<style>` or `<script>` blocks ✓

## Issues Found

| Severity | Section | Problem | Status |
|---|---|---|---|
| Major | Summary | Missing required internal link to /blog/make-money-online-for-beginners/ | FIXED — added during QA |

## Decision

**READY FOR PUBLICATION**

**Rationale:** Zero critical issues. Zero major issues after fix. All 8 checks pass.

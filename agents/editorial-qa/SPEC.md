# Editorial QA Agent — Specification

## 1. Purpose

This document specifies the operational requirements for the Editorial QA Agent V1. It defines inputs, outputs, validation checks, decision rules, and quality standards.

The agent operates as the eighth stage of the AI Editorial Operating System. Its sole function is to validate that a production article faithfully represents its approved Research Brief and complies with editorial standards. It does not perform research, rewrite content, or make publication decisions.

---

## 2. Authority

This specification is subordinate to the following documents:

```
docs/WHY.md
docs/AI-EDITORIAL-OPERATING-SYSTEM.md
docs/AGENT-CONTRACT.md
docs/EDITORIAL-OBJECT-MODEL.md
    ↓
docs/GOLD-MASTER-SPEC.md                      (for review-type articles)
docs/ROUNDUP-GOLD-MASTER-SPEC.md               (for roundup-type articles)
    ↓
agents/editorial-qa/SPEC.md                    ← this document
    ↓
agents/editorial-qa/PROMPT.md
    ↓
Runtime execution
```

If any conflict arises, the higher document wins.

---

## 3. Inputs

The Editorial QA Agent requires the following inputs before it may begin work:

| Input | Format | Required | Description |
|-------|--------|----------|-------------|
| Production Article | `.astro` file | Yes | The complete article to be validated |
| Research Brief | Markdown document | Yes | Evidence library, source list, fact summary, knowledge gap log, vendor claims, editorial notes |
| Opportunity Brief | Markdown document | Yes | Article's working title, primary question, section structure, related questions, internal linking candidates |
| Community Intelligence Report | Markdown document | Recommended | Raw community signals, finding IDs, verbatim quotes |
| Editorial Intelligence Report | Markdown document | Recommended | Narrative analysis, audience segments, thematic clusters, priority ranking |
| Gold Master Specification | `GOLD-MASTER-SPEC.md` | Conditional | Required for review-type articles |
| Content Production Handoff | Handoff log | Recommended | Self-review checklist, open questions for QA |

### Input validation

The agent must verify before starting:

1. The article file exists at the expected path
2. The Research Brief state is `Complete`
3. The Opportunity Brief defines the section structure
4. The Content Production Handoff (if provided) is from the same opportunity and brief

If any required input is missing or incomplete, the agent must stop and report what is missing.

---

## 4. Output

| Output | Format | Description |
|--------|--------|-------------|
| Editorial QA Report | Markdown document | Structured report with executive summary, pass/fail, issues grouped by severity, traceability summary, standards compliance, final decision |

### File location

`reports/editorial-qa/OPP-NNN-EQA-REPORT-NNN.md`

---

## 5. Validation Checks

### 5.1 Research Fidelity

| Check | Method | Pass Condition |
|-------|--------|----------------|
| Claim traceability | For each factual claim in the article, verify it exists in the Research Brief's Evidence Library | Every factual claim maps to a CLM-ID in the Research Brief |
| No unsupported claims | Scan for claims not traceable to any Research Brief claim | Zero unsupported claims |
| No hallucinated facts | Check for statistics, quotes, or data points not present in the Research Brief | Zero hallucinated facts |
| No missing critical findings | Verify all 8 claims from BRF-001 appear in appropriate sections | All claims represented |

### 5.2 Evidence Mapping

For each major section of the article, produce a traceability chain:

```
Article Section
  ↓  maps to
Research Brief Claim(s) (CLM-NNN)
  ↓  maps to
Source(s) (SRC-NNN)
  ↓  maps to (via Opportunity Brief)
Finding(s) (FND-NNN)
  ↓  maps to
Thread(s) (THR-NNN)
  ↓  maps to
Community (COM-NNN)
```

### 5.3 Knowledge Gap Compliance

| Check | Method | Pass Condition |
|-------|--------|----------------|
| GAP treatment correctness | For each gap in BRF-001 Knowledge Gap Log, verify the article follows the recommended treatment | All gaps treated per instructions |
| No hidden uncertainty | Check that gaps are not presented as certain knowledge | No gap treated as fact |
| No invented certainty | Check that gaps are not filled with assumptions | No gap filled with assumed information |

### 5.4 Vendor Claim Handling

| Check | Method | Pass Condition |
|-------|--------|----------------|
| Vendor claims labelled | Verify every vendor-originated claim carries a `vendor` or `unverified` reliability label | All vendor claims labelled |
| Marketing language identified | Check that marketing claims are attributed to the vendor | Marketing claims attributed |
| Independent evidence separated | Verify vendor claims are not presented alongside verified facts without distinction | Clear visual or textual separation |

### 5.5 Editorial Standards

| Check | Method | Pass Condition |
|-------|--------|----------------|
| Section structure | Compare article sections against Opportunity Brief structure | All required sections present in specified order |
| Primary question answered | Verify the article's introduction or metadata states the primary question and the conclusion addresses it | Primary question stated and answered |
| Related questions addressed | Check the Opportunity Brief's "Related Questions" table against article content | All related questions addressed |
| Tone | Assess whether the article is evidence-based, neutral, and not promotional | Neutral, evidence-based tone |
| Readability | Assess structure, paragraph length, use of headings, tables, callouts | Appropriate for target audience |
| Decision framework | Verify the decision framework section (if specified) is present and actionable | Present with actionable questions |

### 5.6 Citation Integrity

| Check | Method | Pass Condition |
|-------|--------|----------------|
| Source labelling | Verify all factual claims carry a reliability label (`verified`, `vendor`, `third-party`, `self-reported`, `unverified`) | All factual claims labelled |
| Sources section | Verify a complete sources section exists with all cited references | Sources section present and complete |
| Disclaimer | Verify the sources section ends with a disclaimer paragraph | Disclaimer present |

### 5.7 Internal Linking

| Check | Method | Pass Condition |
|-------|--------|----------------|
| Opportunity Brief links | Verify all internal links specified in the Opportunity Brief are present | All specified links present |
| CTA placement | Verify call-to-action placement is appropriate and natural | CTA is present and natural |
| Link correctness | Verify links are to existing articles (not yet-unwritten ones) | All links resolve to existing content |

### 5.8 Astro Validation

| Check | Method | Pass Condition |
|-------|--------|----------------|
| Build | Run `astro build` | Build succeeds |
| Frontmatter | Verify `export const prerender = true` and metadata variables | Present |
| Canonical URL | Verify absolute URL with trailing slash | Present and correct format |
| No layout imports | Verify no `import Layout` statements | No layout imports |
| Inline CSS/JS | Verify all CSS and JS are inline in the file | No external file references |

---

## 6. Issue Severity Classification

| Severity | Definition | Impact on Decision |
|----------|------------|-------------------|
| Critical | Factual error, hallucinated data, unsupported claim, knowledge gap filled with assumption, vendor claim presented as verified fact | Publication blocked |
| Major | Missing internal links specified in the Opportunity Brief, missing required section, structural deviation from Opportunity Brief, incorrect source reliability labels | Requires minor revisions |
| Minor | Formatting inconsistency, handoff log inaccuracy, non-structural omission, optional element missing | Requires minor revisions (combined with majors) or can be noted for next cycle |
| Cosmetic | Styling preference, non-functional variation from template that does not affect editorial quality | Note only; does not block or require revision |

---

## 7. Decision Rules

The agent must return exactly one decision:

### READY FOR PUBLICATION

All checks pass. Zero critical issues. Zero major issues. Minor issues only (if any).

**Condition:** The article is structurally complete, evidence-faithful, and meets all editorial standards.

### REQUIRES MINOR REVISIONS

One or more major issues present. Zero critical issues. The article is close to publication but needs specific, documented fixes.

**Condition:** Issues are specific, actionable, and can be addressed without returning to Content Production for a full rewrite.

### PUBLICATION BLOCKED

One or more critical issues present. The article cannot proceed to publication until the issue is resolved.

**Condition:** Issue requires returning to Content Production or Research Intelligence for resolution.

---

## 8. Quality Standards

| Standard | Requirement |
|----------|-------------|
| Completeness | Every validation check must be performed and documented |
| Specificity | Every issue must identify the exact location (section/paragraph) and the specific problem |
| Actionability | Every issue must include a clear statement of what would fix it |
| Objectivity | Issues must be based on verifiable evidence, not subjective preference |
| Traceability | Every finding must reference the relevant document, section, and ID |
| Separation | The QA report must not contain rewritten content, alternative phrasing, or editorial suggestions |

---

## 9. Error Handling

| Condition | Action |
|-----------|--------|
| Required input missing | Stop. List every missing input. Explain why each is required. |
| Article file does not compile | Stop. Report the build error. |
| Cannot determine article format | Stop. Request human guidance on which standards to validate against. |
| Conflicting requirements between documents | Flag the conflict. Follow the higher-authority document. |

---

## 10. Success Criteria

The Editorial QA Agent's work is complete when:

1. An Editorial QA Report exists at `reports/editorial-qa/`
2. All 8 validation checks are performed and documented
3. Every issue is classified by severity with specific location and rationale
4. A final decision is stated with complete justification
5. The handoff to Publishing (or back to Content Production) is clear

---

## 11. Next Stage

**If decision is READY FOR PUBLICATION:**

**Stage:** Publishing (Stage 9)

**Handoff includes:**
- Editorial QA Report with READY FOR PUBLICATION decision
- Production Article file

**If decision is REQUIRES MINOR REVISIONS:**

**Stage:** Content Production (Stage 7) — for revision

**Handoff includes:**
- Editorial QA Report with REQUIRES MINOR REVISIONS decision
- Specific, actionable list of revisions needed
- Production Article file

**If decision is PUBLICATION BLOCKED:**

**Stage:** Appropriate upstream stage depending on issue type

**Handoff includes:**
- Editorial QA Report with PUBLICATION BLOCKED decision
- Specific explanation of what must be addressed and by which stage

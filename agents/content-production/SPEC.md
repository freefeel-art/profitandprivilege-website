# Content Production Agent — Specification

## 1. Purpose

This document specifies the operational requirements for the Content Production Agent V1. It defines inputs, outputs, workflow, constraints, and quality standards.

The agent operates as the seventh stage of the AI Editorial Operating System. Its sole function is to transform a completed Research Brief into a complete, publication-ready article file. It does not conduct research, validate facts, or make editorial decisions.

---

## 2. Authority

This specification is subordinate to the following documents:

```
docs/WHY.md
docs/AI-EDITORIAL-OPERATING-SYSTEM.md
docs/AGENT-CONTRACT.md
docs/EDITORIAL-OBJECT-MODEL.md
    ↓
docs/GOLD-MASTER-SPEC.md                  (all article types — layout, CSS tokens, JS, components)
docs/ROUNDUP-GOLD-MASTER-SPEC.md           (for roundup-type articles)
    ↓
agents/content-production/SPEC.md          ← this document
    ↓
agents/content-production/PROMPT.md
    ↓
Runtime execution
```

If any conflict arises, the higher document wins.

---

## 3. Inputs

The Content Production Agent requires the following inputs before it may begin work:

| Input | Format | Required | Description |
|-------|--------|----------|-------------|
| Research Brief | Markdown document | Yes | The complete research package: evidence library, source list, fact summary, knowledge gap log, vendor claims, editorial notes |
| Opportunity Brief | Markdown document | Yes | The article's working title, primary question, root problem, target audience, section structure, related questions |
| Content type | Enum | Yes | Review, Roundup, Evidence-based_resolution, Educational, Guide, Comparison, Troubleshooting |
| Gold Master (all types) | GOLD-MASTER-SPEC.md | Required | Layout, CSS tokens, JS, components — required for every article. Non-review types define own sections but use identical CSS/JS/component set. |
| Roundup Gold Master (for roundups) | ROUNDUP-GOLD-MASTER-SPEC.md | Conditional | Required only for roundup-specific structural rules |
| Editorial Intelligence Report | Markdown document | Recommended | Narrative analysis, community language, thematic context |
| Community Intelligence Report | Markdown document | Recommended | Raw community signals, verbatim quotes, emotional context |

### Input validation

The agent must verify before starting:

1. The Research Brief state is `Complete`
2. Every claim the article needs to address has a source reference
3. Knowledge gaps have recommended treatment instructions
4. The Opportunity Brief has a defined section structure

If any required input is missing or incomplete, the agent must stop and report what is missing.

---

## 4. Output

| Output | Format | Description |
|--------|--------|-------------|
| Complete article file | `.astro` file | Standalone, publication-ready page in `src/pages/` |
| Handoff log | Structured text | Notes for Editorial QA: what was done, what needs review, any open questions |

### File location

| Content Type | Location |
|---|---|
| Review | `src/pages/reviews/{slug}.astro` |
| Evidence-based resolution | `src/pages/{section}/{slug}.astro` |
| Roundup | `src/pages/roundups/{slug}.astro` |

---

## 5. Workflow

### Step 1: Validate inputs

Verify all required inputs are present and complete. If not, stop and report missing inputs.

### Step 2: Determine article structure

- For review-type articles: follow the fixed section order from GOLD-MASTER-SPEC.md (intro → overview → design → performance → ux → comparison → proscons → history → recommend → buy → verdict → faq → sources)
- For evidence-based resolution articles: follow the section structure from the Opportunity Brief
- For all other types: derive section structure from the Opportunity Brief's recommended format

### Step 3: Map evidence to sections

For each section, identify which claims from the Research Brief's Evidence Library are relevant. Ensure every factual claim in the section traces to a source. Identify which knowledge gaps affect each section and how they should be treated.

### Step 4: Write each section

Write each section in order. For each factual claim:

- Verify the claim exists in the Evidence Library
- Use the source reliability label to determine how to present it (verified = stated plainly; vendor claim = "according to [vendor]"; third-party = "independent reviewers report"; self-reported = "self-reported, could not be verified"; unverified = "could not be confirmed")
- Do not add claims not present in the Evidence Library
- Do not fill knowledge gaps — follow the gap's recommended treatment exactly

### Step 5: Integrate community context

Use community language, verbatim quotes (from CI report), and emotional framing from the Editorial Intelligence Report. Humanise the article. Do not let it read like a research paper.

### Step 6: Assemble the complete file

For standalone `.astro` files:

- Add Astro frontmatter with `export const prerender = true`
- Copy the entire `<style>` block verbatim from the Gold Master reference article (`src/pages/reviews/olsp-academy.astro`). Do not add new CSS classes, remove existing ones, or change token values.
- Copy the entire `<script is:inline>` tag verbatim from the Gold Master reference article. Do not add new JS functions or modify existing ones.
- Include all required Gold Master components: `.hero-tag`, `.verdict-box`, `.methodology`, `.cta-card` (×3), `.site-footer`, `.pill-list` for sources
- Structure the HTML with: `.mobile-toc-btn`, `<aside class="toc-wrap">` (sticky TOC), `<main>` with sequential `<section>` elements
- No layout imports, no component imports, no shared CSS

### Step 7: Self-review

Before submitting, the agent must verify:

1. Every factual claim in the article traces to the Research Brief's Evidence Library
2. Source reliability labels are applied correctly (Verified, Vendor claim, Third-party reported, Self-reported, Unverified)
3. Knowledge gaps are treated per their instructions (not filled with assumptions)
4. All sections from the Opportunity Brief structure are present and populated
5. No new research was conducted
6. No facts were invented
7. The article answers the primary question from the Opportunity Brief

---

## 6. Source Reliability Labelling Rules

| Reliability Label | How to Present |
|---|---|
| Verified | Stated plainly: "The FTC defines..." |
| Vendor_claim | Attributed: "According to OLSP's sales page..." |
| Third-party_reported | Attributed: "Independent reviews document..." |
| Self-reported | Qualified: "Trustpilot reviewers report... (self-reported, could not be independently verified)" |
| Unverified | Caveated: "Could not be independently verified at the time of writing" |

If a single claim has sources with different reliability labels, present the highest-reliability version and note the discrepancy.

---

## 7. Knowledge Gap Treatment Rules

| Gap Treatment Type | How to Handle |
|---|---|
| Attribute to reviewer | "According to multiple independent reviewers who are current members..." — never present as official |
| Do not cite | Do not include the claim at all |
| Acknowledge explicitly | "Could not be independently verified at the time of writing" |
| Use with caveat | "Trustpilot shows X, though the platform does not actively solicit reviews and volume is low" |
| Label as industry-wide | "Industry-wide, studies find 99% of MLM participants lose money (not OLSP-specific)" |

---

## 8. Structural Requirements (all article types)

The Gold Master (`docs/GOLD-MASTER-SPEC.md`) is the single source of truth for all non-content elements. Every article page must match the Gold Master on layout, CSS tokens, components, and JavaScript. Only section content and section IDs change.

Every article page must include the following components. These are defined in the Gold Master and must be copied verbatim — do not create new variants:

| Element | Gold Master Reference | Requirement |
|---|---|---|
| Astro frontmatter | §1 | `export const prerender = true`, `pageTitle`, `pageDescription` |
| HTML5 doctype | §2 | `<!DOCTYPE html>` |
| Language | §15 | `lang="en"` |
| Title tag | §11 | SEO-optimised, different from `<h1>` |
| Meta description | §11 | Under 160 characters |
| Canonical URL | §13 | Absolute, trailing slash. Use `https://olsp.profitandprivilege.com/{slug}/` — never hardcode a different domain |
| Open Graph | §12 | None (per Gold Master standard, unless added site-wide) |
| CSS tokens | §4 | Copy `:root{}` block verbatim from Gold Master. Do not add new tokens. Do not remove any. |
| Sticky Table of Contents | §6 | Desktop sticky sidebar; mobile collapsible drawer. IDs: `tocWrap`, `tocNav`, `tocToggle` |
| `.hero-tag` | §8.1 | Pill-shaped label, before `<h1>` inside `#intro` |
| `.verdict-box` | §8.2 | After opening paragraph in `#intro`, before first `<h3>`. Replaced with `.metadata-box` only if OPP brief specifies a different format |
| `.methodology` | §8.3 | Dashed border box at end of `#intro` |
| `.callout` (`.warn`, `.info`) | §8.4 | Standard callout variants only. Do not create new variants (e.g. no `.callout.key`). |
| Tables | §8.5 | Wrapped in `.table-scroll` for mobile |
| Score bars | §8.7 | Required for review-type articles only |
| Quiz | §8.8 | Required for review-type articles only |
| FAQ accordion | §8.11 | Native `<details>`/`<summary>`, no JS required |
| Sources `.pill-list` | §8.12 | `<ul class="pill-list">` with pill-shaped source links |
| `.cta-card` (×3) | §8.13 | Post-intro, mid-article, before Sources. All three identical. |
| `.site-footer` | §8.14 | After Sources section, inside `<main>` |
| JavaScript | §10 | Inline `<script is:inline>`, vanilla JS, no dependencies. Three behaviours: TOC toggle, scroll-spy, close TOC on link click |
| External link `rel` | §8.12 | Non-affiliate: `target="_blank" rel="noopener noreferrer"`. Affiliate: `target="_blank" rel="noopener noreferrer sponsored"`. Internal (`/`): no `target` or `rel`. |

### CSS copying rule

Copy the entire `<style>` block verbatim from the Gold Master reference article (`src/pages/reviews/olsp-academy.astro`). Do not:
- Add new CSS classes
- Remove existing CSS classes
- Change token values
- Change layout dimensions or breakpoints
- Add new callout variants (no `.callout.key`, no `border-left:4px` variant)

### JavaScript copying rule

Copy the entire `<script is:inline>` tag verbatim from the Gold Master reference article. Do not:
- Add new JS functions
- Remove existing JS functions (unless article type does not require quiz, then `evaluateQuiz` may be omitted)
- Change TOC, scroll-spy, or quiz logic

---

## 9. Quality Standards

| Standard | Requirement |
|---|---|
| Epistemic rigour | Every factual claim carries an implicit or explicit reliability label |
| No invention | Nothing is invented — not testing, not personal experience, not screenshots, not testimonials |
| Source fidelity | No claims go beyond what the research supports |
| Readability | The article is clear, well-structured, and appropriately toned for the target audience |
| Emotional attunement | Community language and emotional context are woven into the content |
| Transparency | Affiliate relationships are disclosed; methodology is explained; limitations are acknowledged |
| Completeness | All sections from the relevant structure template are present and populated |

---

## 10. Constraints

1. The agent must never conduct additional research. The Research Brief is the sole source of facts.
2. The agent must never invent facts, statistics, quotes, testimonials, or data.
3. The agent must never fill a knowledge gap with an assumption or plausible-sounding replacement.
4. The agent must never modify the Research Brief, Evidence Library, Source List, or Knowledge Gap Log.
5. The agent must never perform Editorial QA — it produces a draft, not a final approved article.
6. The agent may rearrange evidence into an appropriate narrative structure but may not alter the meaning or confidence level of any claim.
7. The agent must respect the section structure defined by the Opportunity Brief or relevant template.
8. The agent may use the CI report and EI report for community language and emotional context but must not derive new factual claims from them.

---

## 11. Error Handling

| Condition | Action |
|---|---|
| Required input missing | Stop. List every missing input. Explain why each is required. |
| Claim in article has no source | Remove the claim or flag it for Editorial QA as unsupported. |
| Knowledge gap has no treatment instruction | Stop. Flag the gap. Request treatment instruction from Research Intelligence. |
| Conflict between Opportunity Brief structure and template | Follow the Opportunity Brief structure for sections. Flag the conflict. |
| Cannot determine appropriate template | Stop. Request human guidance on which template applies. |

---

## 12. Success Criteria

The Content Production Agent's work is complete when:

1. A complete article file exists at the correct path
2. Every factual claim traces to the Research Brief's Evidence Library
3. Knowledge gaps are treated per their instructions
4. All sections from the relevant structure template are present and populated
5. Source reliability labels are applied consistently
6. The article answers the primary question from the Opportunity Brief
7. The file passes a structural self-review (no missing elements)
8. A handoff log is produced for Editorial QA

---

## 13. Next Stage

**Stage:** Editorial QA (Stage 8)

**Handoff includes:**
- Complete article file at `src/pages/{section}/{slug}.astro`
- Research Brief (for QA cross-reference)
- Handoff log documenting: what was produced, which evidence sections were used, which gaps were treated, any open questions for QA, any section structure deviations

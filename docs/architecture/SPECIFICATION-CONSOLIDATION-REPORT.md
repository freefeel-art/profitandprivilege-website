# Specification Consolidation Report

**Date:** 2026-07-08
**Status:** Draft — analysis only, no implementation
**Architecture Freeze:** ACTIVE

---

## 1. Executive Summary

The AI Editorial Operating System has grown to 16+ specification/prompt documents across 3 agent directories + docs/ root. During the first real production cycle (OPP-005, `affiliate-marketing-vs-mlm`), overlapping authority claims and contradictory output format requirements created ambiguity that risks generating articles that don't match any spec's full requirements.

**Core problem:** Two "writer" agents (Editorial Builder and Content Production) are specified to do the same work but produce fundamentally different output — one uses shared components (`OlspLayout` + imports), the other uses standalone inline everything. Additionally, the Gold Master SPEC describes a shared-component architecture (v2.1) while Content Production PROMPT tells agents to copy CSS/JS verbatim from a reference file.

**Root cause:** The system evolved incrementally — a new spec/prompt was written for each new agent without auditing whether the existing chain was consistent. The Review Gold Master came first (shared components), then Blog Master Spec (inline approach), then ROUNDUP and BLOG-MASTER-PROMPT documents — each adjusting the pattern without reconciling with the others.

---

## 2. Complete Document Inventory

### Tier 1 — Foundational (no changes needed)

| # | Document | Path | Type | Lines | Purpose |
|---|----------|------|------|-------|---------|
| F1 | WHY.md | `docs/WHY.md` | Strategic | — | Site mission, authority chain root |
| F2 | AI-EDITORIAL-OPERATING-SYSTEM.md | `docs/AI-EDITORIAL-OPERATING-SYSTEM.md` | Architecture | — | 9-stage pipeline definition |
| F3 | AGENT-CONTRACT.md | `docs/AGENT-CONTRACT.md` | Contract | — | Cross-agent rules, stage isolation |
| F4 | EDITORIAL-OBJECT-MODEL.md | `docs/EDITORIAL-OBJECT-MODEL.md` | Data model | — | Shared vocabulary, artifact types |
| F5 | PIPELINE-ARCHITECTURE.md | `docs/PIPELINE-ARCHITECTURE.md` | Architecture | 86 | Heavy/Light pipeline tracks |

### Tier 2 — Article Type Specifications (conflict zone)

| # | Document | Path | Type | Lines | Article Types | Output Format |
|---|----------|------|------|-------|---------------|---------------|
| S1 | GOLD-MASTER-SPEC.md | `docs/GOLD-MASTER-SPEC.md` | Spec | 528 | Reviews | Shared components (OlspLayout + 11 imports) |
| S2 | BLOG-MASTER-SPEC.md | `docs/BLOG-MASTER-SPEC.md` | Spec | 257 | Blog/informational | Standalone inline (no layout imports) |
| S3 | ROUNDUP-GOLD-MASTER-SPEC.md | `docs/ROUNDUP-GOLD-MASTER-SPEC.md` | Spec | — | Roundups | — |

### Tier 3 — Agent Prompts (conflict zone)

| # | Document | Path | Type | Lines | Agent | Output Format |
|---|----------|------|------|-------|-------|---------------|
| P1 | Editorial Builder SPEC | `agents/editorial-builder/SPEC.md` | Spec | 141 | Editorial Builder (Stage 3) | Shared components (OlspLayout) |
| P2 | Editorial Builder PROMPT | `agents/editorial-builder/PROMPT.md` | Prompt | 173 | Editorial Builder | Shared components (OlspLayout) |
| P3 | Content Production SPEC | `agents/content-production/SPEC.md` | Spec | 269 | Content Production (Stage 7) | Standalone inline (no imports) |
| P4 | Content Production PROMPT | `agents/content-production/PROMPT.md` | Prompt | 123 | Content Production | Standalone inline (no imports) |
| P5 | Content Production OUTPUT-SCHEMA | `agents/content-production/OUTPUT-SCHEMA.md` | Schema | 308 | Content Production | Standalone inline |
| P6 | Editorial QA SPEC | `agents/editorial-qa/SPEC.md` | Spec | 254 | Editorial QA (Stage 8) | Validates against spec chain |
| P7 | Editorial QA PROMPT | `agents/editorial-qa/PROMPT.md` | Prompt | — | Editorial QA | — |
| P8 | PRODUCTION-MASTER-PROMPT.md | `docs/PRODUCTION-MASTER-PROMPT.md` | Prompt | — | Review article builder | Shared components |
| P9 | BLOG-MASTER-PROMPT.md | `docs/BLOG-MASTER-PROMPT.md` | Prompt | — | Blog article builder | Standalone inline |
| P10 | ROUNDUP-MASTER-PROMPT.md | `docs/ROUNDUP-MASTER-PROMPT.md` | Prompt | — | Roundup article builder | — |

### Agency Files

| # | Document | Path | Type |
|---|----------|------|------|
| A1 | Opportunity Discovery SPEC | `agents/opportunity-discovery-agent/SPEC.md` | Spec |
| A2 | Opportunity Discovery PROMPT | `agents/opportunity-discovery-agent/PROMPT.md` | Prompt |
| A3 | Opportunity Research SPEC | `agents/opportunity-research-agent/SPEC.md` | Spec |
| A4 | Opportunity Research PROMPT | `agents/opportunity-research-agent/PROMPT.md` | Prompt |
| A5 | Publisher SPEC | `agents/publisher/SPEC.md` | Spec |
| A6 | Publisher PROMPT | `agents/publisher/PROMPT.md` | Prompt |

---

## 3. Dependency Graph

```
docs/WHY.md
  └─ docs/AI-EDITORIAL-OPERATING-SYSTEM.md
       └─ docs/AGENT-CONTRACT.md
            └─ docs/EDITORIAL-OBJECT-MODEL.md
                 └─ docs/PIPELINE-ARCHITECTURE.md
                      │
                      ├── Heavy Track ──► docs/GOLD-MASTER-SPEC.md (shared components)
                      │                       └─ agents/editorial-builder/SPEC.md
                      │                            └─ agents/editorial-builder/PROMPT.md
                      │
                      ├── Light Track ──► docs/BLOG-MASTER-SPEC.md (inline standalone)
                      │                       └─ (no direct agent mapping to builder)
                      │
                      └── Roundups ────► docs/ROUNDUP-GOLD-MASTER-SPEC.md
```

**Actual (current) structure — where the overlap occurs:**

```
docs/GOLD-MASTER-SPEC.md (v2.1 — says "required for ALL article types" in Content Production PROMPT)
  ├── agents/editorial-builder/SPEC.md ──── "all article types" authority chain shows BLOG-MASTER-SPEC
  │     └── agents/editorial-builder/PROMPT.md ─── uses OlspLayout (shared components)
  │
  └── agents/content-production/SPEC.md ─── "all article types" authority chain shows GOLD-MASTER-SPEC only
        └── agents/content-production/PROMPT.md ─── inline CSS/JS copy (standalone)

docs/BLOG-MASTER-SPEC.md (2026-07-04 — blog-specific)
  ├── Referenced by Editorial Builder SPEC authority chain (line 23)
  ├── NOT referenced by Content Production SPEC (line 21 — only GOLD-MASTER-SPEC)
  └── NOT referenced by Editorial QA SPEC (line 21 — only GOLD-MASTER-SPEC and ROUNDUP)

docs/ROUNDUP-GOLD-MASTER-SPEC.md
  ├── Referenced by Editorial Builder SPEC authority chain
  ├── Referenced by Content Production SPEC authority chain (line 22)
  └── Referenced by Editorial QA SPEC authority chain (line 22)
```

**Key finding: BLOG-MASTER-SPEC is a dangling dependency — it does not appear in the authority chains of the agents that actually produce content.**

---

## 4. Conflict Matrix

### Conflict 1: Output Format — Shared Components vs. Standalone Inline

| Source | Says | Approach |
|--------|------|----------|
| GOLD-MASTER-SPEC.md §1 (lines 5-6) | "The Gold Master is a reusable component system — not a single file to copy. Structure, CSS tokens, JS behavior, SEO metadata, and CTA architecture are shared across all articles through OlspLayout and 10 Gold Master components." | **Shared components** |
| Editorial Builder PROMPT §Layout (line 26) | "Use `OlspLayout` from `src/components/olsp-standard/OlspLayout.astro` as the page wrapper." | **Shared components** |
| Editorial Builder PROMPT §Checklist (line 133) | "No inline `<style>` blocks or inline `<script>` tags exist" | **Shared components** |
| Content Production SPEC §6 Step 6 (lines 112-114) | "Copy the entire `<style>` block verbatim from the Gold Master reference article... Copy the entire `<script is:inline>` tag verbatim" | **Standalone inline** |
| Content Production PROMPT §Gold Master Alignment (lines 31-36) | "Copy the entire `<style>` block verbatim... Copy the entire `<script is:inline>` tag verbatim" | **Standalone inline** |
| Content Production PROMPT §Assembly (line 117) | "No layout imports, no component imports, no shared CSS" | **Standalone inline** |

**Impact:** Two agents claim to do the same work but produce files with completely different architectures. A Content Production-generated article (inline) cannot be processed by Editorial QA expecting shared-component patterns, and vice versa.

### Conflict 2: Authority Chain — Which Spec Applies to Blog Articles?

| Source | Says | Blog included? |
|--------|------|----------------|
| Content Production SPEC §2 (line 21) | `GOLD-MASTER-SPEC.md (all article types — layout, CSS tokens, JS, components)` | Yes — says "all article types" |
| Content Production SPEC §2 (line 22) | `ROUNDUP-GOLD-MASTER-SPEC.md (for roundup-type articles)` | Only roundups |
| Content Production SPEC §2 | **BLOG-MASTER-SPEC.md not listed** | **No** |
| Content Production PROMPT §Inputs (line 22) | `Gold Master Specification (docs/GOLD-MASTER-SPEC.md) — REQUIRED for ALL article types` | Yes — says "ALL" |
| Editorial Builder SPEC §2 (line 21-23) | `GOLD-MASTER-SPEC.md (all article types), ROUNDUP-GOLD-MASTER-SPEC.md (for roundups), BLOG-MASTER-SPEC.md (for informational/blog articles)` | **Yes — correctly listed** |
| Editorial QA SPEC §2 (lines 21-23) | `GOLD-MASTER-SPEC.md (for review-type articles), ROUNDUP-GOLD-MASTER-SPEC.md (for roundup-type articles)` | **No — blog not listed** |

**Impact:** Content Production and Editorial QA have no awareness of BLOG-MASTER-SPEC. They apply GOLD-MASTER-SPEC rules to blog articles, which means missing components that only BLOG-MASTER-SPEC requires (QuoteBanner, Standard CTA, OG tags, JSON-LD).

### Conflict 3: Component Set for Blog Articles

| Component | GOLD-MASTER-SPEC §8 | BLOG-MASTER-SPEC §4 | In generated article? |
|-----------|---------------------|---------------------|----------------------|
| `.hero-tag` | ✓ Required | ✓ Required | ✓ |
| `.verdict-box` | ✓ Required | ✓ Required | ✓ |
| `.methodology` | ✓ Required | ✗ Not used in blog | ✓ (should be omitted per blog spec) |
| `.cta-card` (×3) | ✓ Required | ✗ Replaced by QuoteBanner | ✓ (3 present as CTA cards) |
| `.quote-banner` (×3) | ✗ Not mentioned | ✓ Required | ✗ (missing per blog spec) |
| `.standard-cta` (×1) | ✗ Not mentioned | ✓ Required | ✗ (missing per blog spec) |
| GoldMasterQuote (×3) | ✓ Required | ✗ Not mentioned | ✓ (10 present) |
| OG tags + JSON-LD | ✗ "No OG tags" (§9) | ✓ Required (§5) | ✓ Present (added by prompt) |
| `.site-footer` | ✓ Required | ✓ Required | ✓ |
| Sources `.pill-list` | ✓ Required | ✓ Required | ✓ |
| FAQ accordion | ✓ Required | ✓ Required | ✓ |

**Impact:** The generated article follows Content Production PROMPT's GOLD-MASTER-SPEC mandate exactly — it has methodology, 3 CTA cards, 10 GoldMasterQuotes — but omits QuoteBanner and Standard CTA. Which spec is correct for blog articles? Currently unanswerable.

### Conflict 4: Canonical URL Pattern

| Source | Pattern |
|--------|---------|
| Content Production PROMPT §Canonical URL | `https://olsp.profitandprivilege.com/{slug}/` |
| Content Production OUTPUT-SCHEMA §3 | `https://profitandprivilege.com/.../` (missing `olsp.` subdomain) |
| Editorial Builder PROMPT §Canonical URL | `https://olsp.profitandprivilege.com/{section}/{slug}/` |
| BLOG-MASTER-SPEC §5 | `https://olsp.profitandprivilege.com/blog/{slug}/` |
| GOLD-MASTER-SPEC §2 | `https://olsp.profitandprivilege.com/reviews/{slug}/` |

**Impact:** OUTPUT-SCHEMA.md has the wrong domain (missing `olsp.` subdomain). The other sources agree on the `olsp.` subdomain but differ on `{section}` inclusion. Blog articles need `/blog/` prefix per BLOG-MASTER-SPEC.

### Conflict 5: SEO Metadata Ownership

| Source | Says |
|--------|------|
| GOLD-MASTER-SPEC §9 (line 369) | "SEO metadata is generated by OlspLayout — no article page should add its own `<meta>`, OG, or schema tags." |
| GOLD-MASTER-SPEC §16 Rule 19 (line 508-509) | "SEO metadata is generated by OlspLayout, not article pages. Do not add `<meta>`, OG, Twitter, or schema tags to individual article files." |
| BLOG-MASTER-SPEC §5 (lines 150-190) | Full OG tags + JSON-LD `<head>` block must be hardcoded in every blog article |
| Editorial Builder PROMPT (lines 26-34) | "The layout handles all presentation... Do NOT add inline `<style>` blocks" — implies layout handles OG too |

**Impact:** GOLD-MASTER-SPEC says "no OG/schema in articles — layout handles it." BLOG-MASTER-SPEC says "OG + JSON-LD must be hardcoded in every blog article." These are contradictory. The generated article has hardcoded OG + JSON-LD (following BLOG-MASTER-SPEC / Content Production PROMPT), which contradicts GOLD-MASTER-SPEC §9 and §16 Rule 19.

### Conflict 6: Frontmatter Format

| Source | Format |
|--------|--------|
| GOLD-MASTER-SPEC §3 | `pageTitle`, `pageDescription`, `tocLinks`, optional props — Astro variables |
| BLOG-MASTER-SPEC §1 (line 17) | "Frontmatter contains **only** `export const prerender = true;` — no other variables, no imports. `<title>` and `<meta name="description">` are hardcoded strings in `<head>`" |
| Editorial Builder PROMPT (lines 81-101) | Uses frontmatter variables `pageTitle`, `pageDescription`, `tocLinks` passed as props to OlspLayout |
| Content Production PROMPT (output) | Uses frontmatter variables (from OUTPUT-SCHEMA) |

**Impact:** BLOG-MASTER-SPEC explicitly prohibits the frontmatter pattern that GOLD-MASTER-SPEC and Editorial Builder PROMPT require. If a blog article is generated following the Builder approach (OlspLayout), it *must* have frontmatter variables. If generated following the blog spec, it must *not* have them.

### Conflict 7: Component Include/Exclude for Blog

| Source | Methodology | Score Bars | Quiz | SVG Diagram | Video Embed |
|--------|------------|------------|------|-------------|-------------|
| GOLD-MASTER-SPEC §8 | Required in intro | Required in verdict | Required in verdict | Optional | Optional |
| BLOG-MASTER-SPEC §4 | "Not used in blog articles" | "Not used" | "Not used" | "Not used" | "Not used" |
| Content Production SPEC §8 | Required (all types) | Required (review only) | Required (review only) | — | — |
| Generated article | ✓ Present | ✗ Omitted | ✗ Omitted | ✗ Omitted | ✗ Omitted |

**Impact:** The generated article correctly omitted review-specific components (following Content Production's spec that only lists those as "required for review type"). But it *included* `.methodology` — which BLOG-MASTER-SPEC explicitly says not to use in blog articles.

### Conflict 8: Quote Count

| Source | GoldMasterQuote count |
|--------|-----------------------|
| GOLD-MASTER-SPEC §8 (line 355) | "Three GoldMasterQuote placements are fixed" (line 300 shows placements at post-intro, after-UX, pre-sources) |
| BLOG-MASTER-SPEC §3 | Three QuoteBanner components (the blog equivalent), no GoldMasterQuote |
| Content Production PROMPT §Required Components | No mention of GoldMasterQuote — but GOLD-MASTER-SPEC requires it as a component |
| Generated article | 10 GoldMasterQuotes (one per section, not following either spec) |

**Impact:** The generated article has 10 GoldMasterQuotes, far exceeding the 3 that GOLD-MASTER-SPEC requires. The Content Production PROMPT doesn't mention GoldMasterQuote in its 8-component list, but the PROMPT says to copy CSS/JS verbatim from the reference article — the agent used the reference incorrectly.

### Conflict 9: Agent Role Overlap — Builder vs Content Production

| Source | Specified as |
|--------|-------------|
| PIPELINE-ARCHITECTURE.md | Editorial Builder = "Writer" (Stage 3 light / Stage 7 heavy) |
| Editorial Builder SPEC §1 | "Operates as Stage 3 of two-track pipeline and Stage 7" |
| Content Production SPEC §1 | "Operates as seventh stage" |
| Editorial Builder PROMPT §Role | "Stage 3 of the two-track production pipeline" |
| Content Production PROMPT §Role | "Stage 7 of the AI Editorial Operating System" |

**Impact:** Two agents claim to be Stage 7. The Editorial Builder SPEC says it IS the writer (for both tracks). The Content Production SPEC says IT is the writer. They have identical responsibilities but incompatible output formats. This is the core architectural duplication.

---

## 5. Canonical Hierarchy Recommendation

Based on document authority levels and the dates they were written:

```
docs/WHY.md                               ← Strategic intent
docs/AI-EDITORIAL-OPERATING-SYSTEM.md     ← Pipeline structure (9 stages)
docs/AGENT-CONTRACT.md                    ← Cross-agent discipline
docs/EDITORIAL-OBJECT-MODEL.md            ← Shared data model
docs/PIPELINE-ARCHITECTURE.md             ← Heavy/Light tracks
    │
    ├──[if review]──► docs/GOLD-MASTER-SPEC.md (v2.1 — shared components)
    │                     └─ src/pages/reviews/olsp-mineeme.astro (validated reference)
    │                     └─ agents/editorial-builder/ (for heavy pipeline articles)
    │
    ├──[if blog]────► docs/BLOG-MASTER-SPEC.md (2026-07-04 — standalone inline)
    │                     └─ src/pages/blog/part-time-jobs-near-me-no-experience.astro (structure ref)
    │                     └─ src/pages/blog/make-money-online-for-beginners.astro (metadata ref)
    │
    ├──[if roundup]──► docs/ROUNDUP-GOLD-MASTER-SPEC.md
    │
    └──[all types]──► agents/{agent}/SPEC.md → PROMPT.md → Runtime
```

**Recommended resolution:**
- The `Editors/` directory (or whichever agent is "the writer") should reference the correct article-type spec in its authority chain
- `Content Production` and `Editorial Builder` should be clarified as: **one is the implementation**, not two separate agents
- The output format decision (shared components vs. standalone) should be made once, for all types — not per-prompt

---

## 6. Migration Plan to Canonical State

### Phase 1 — Immediate Fix (no architectural change)
1. **Content Production SPEC §2** — add `BLOG-MASTER-SPEC.md` to authority chain
2. **Editorial QA SPEC §2** — add `BLOG-MASTER-SPEC.md` to authority chain
3. **Content Production OUTPUT-SCHEMA §3** — fix canonical URL (add `olsp.` subdomain)
4. **Copy BLOG-MASTER-SPEC's canonical URL pattern** into Content Production PROMPT for blog articles
5. **Document explicitly** that Content Production is the active writer agent; Editorial Builder is the designated future replacement (or vice versa, but not both active)

### Phase 2 — Reconcile Components
6. Determine: does BLOG-MASTER-SPEC's QuoteBanner/Standard CTA override GOLD-MASTER-SPEC's CTA card/QB for blog articles? (PIPELINE-ARCHITECTURE says Light/Blog follows blog spec.)
7. If yes: update Content Production PROMPT's 8-component list to vary by type
8. If no: update BLOG-MASTER-SPEC to remove QuoteBanner and Standard CTA

### Phase 3 — Consolidate Writer Agents (after Architecture Freeze)
9. Merge Editorial Builder and Content Production into a single writer agent with one PROMPT
10. That single PROMPT references all three article-type specs conditionally
11. Remove duplicate prompts from `agents/editorial-builder/` or `agents/content-production/`

---

## 7. Risk Assessment

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| New blog articles generated without QuoteBanner/Standard CTA | Medium | High (certain — current behavior) | Apply Phase 1 item 1 immediately |
| New blog articles generated with Methodology block | Low | High (certain) | Apply Phase 1 — teach agent blog spec excludes it |
| New blog articles generated with CTA cards (3×) instead of QuoteBanner (3×) + Standard CTA (1×) | Medium | High | Content Production PROMPT follows GOLD-MASTER-SPEC only; fix per Phase 1 |
| Editorial QA passes blog articles that lack blog-required components | High | High | QA spec has no blog authority; fix per Phase 1 item 2 |
| Future roundup articles inherit same ambiguity | Medium | Medium | Roundup spec is correctly referenced in all chains; less risk |
| Canonical URL inconsistency between OUTPUT-SCHEMA and actual output | Low | High | Fix per Phase 1 item 3 |
| Confusion about which agent is the actual writer during daily production | Medium | Medium | Resolve per Phase 1 item 5 |

---

## 8. Specific File Changes Required

### Phase 1 (Architecture Freeze compatible — no structural change, just citation fixes)

| File | Change | Rationale |
|------|--------|-----------|
| `agents/content-production/SPEC.md` §2 | Add `BLOG-MASTER-SPEC.md` to authority chain, after line 22 | Content Production must be aware of blog-specific rules |
| `agents/content-production/SPEC.md` §8 | Add note: ".methodology is optional per article type; blog articles omit it per BLOG-MASTER-SPEC §4" | Currently says methodology is required for all types |
| `agents/content-production/PROMPT.md` §Inputs | Add `BLOG-MASTER-SPEC.md` as conditional input (line 22-23 area) | Currently PROMPT only lists GOLD-MASTER-SPEC as required for all |
| `agents/content-production/PROMPT.md` §Required Components | Add conditional note: "for blog articles, replace .cta-card (×3) with .quote-banner (×3) + .standard-cta (×1) per BLOG-MASTER-SPEC §3" | Currently lists 3 CTA cards unconditionally |
| `agents/content-production/PROMPT.md` §Quality Checklist | Add blog-specific checklist items | Currently no blog-specific checks |
| `agents/editorial-qa/SPEC.md` §2 | Add `BLOG-MASTER-SPEC.md` to authority chain, between lines 22 and 23 | QA must validate against blog spec |
| `agents/editorial-qa/SPEC.md` §5.5 Editorial Standards | Add blog-type variant checks | Currently only checks review/article structure |
| `agents/editorial-qa/SPEC.md` §5.7 Internal Linking | Add QuoteBanner/Standard CTA presence checks for blog type | Currently QA doesn't check for blog-specific components |
| `agents/content-production/OUTPUT-SCHEMA.md` §3 | Fix canonical URL: change `https://profitandprivilege.com/.../` to `https://olsp.profitandprivilege.com/.../` | Line 47 has the wrong domain (missing `olsp.` subdomain) |

### Phase 2 (Requires architectural design decision — freeze lift)

| File | Change | Decision Required |
|------|--------|-------------------|
| `docs/BLOG-MASTER-SPEC.md` | Either remove QuoteBanner/Standard CTA (if blog reverts to CTA cards) — or promote it as canonical (if QuoteBanner/Standard CTA is the blog standard) | Which component set is the blog gold standard? |
| `docs/PRODUCTION-MASTER-PROMPT.md` | Update to reference BLOG-MASTER-SPEC for blog articles | Currently references GOLD-MASTER-SPEC only |
| `docs/BLOG-MASTER-PROMPT.md` | Update to match BLOG-MASTER-SPEC v1.0 exactly | May already be in sync |
| `docs/ROUNDUP-MASTER-PROMPT.md` | Verify it references ROUNDUP-GOLD-MASTER-SPEC correctly | Cross-reference check |

### Phase 3 (Requires full architecture freeze lift — structural change)

| Change | Description | Why |
|--------|-------------|-----|
| Merge Editorial Builder and Content Production | One writer agent, one PROMPT, one SPEC | Two agents doing identical work is technical debt |
| Decide shared components vs. standalone | Pick one approach for ALL article types | Hybrid creates maintenance burden |
| Single canonical output format | All three specs agree on same output structure | Consistency across review/blog/roundup |

---

## 9. State of the Generated Article

`src/pages/blog/affiliate-marketing-vs-mlm.astro` was generated by the Content Production Agent using GOLD-MASTER-SPEC as its sole reference (Content Production PROMPT line 22: "Gold Master Specification — REQUIRED for ALL article types"). Per the regression analysis:

**Following GOLD-MASTER-SPEC (review spec) correctly:**
- ✅ Standalone `.astro` with inline CSS/JS
- ✅ `.hero-tag`, `.verdict-box`, `.methodology`, `.cta-card` (×3), `.site-footer`, `.pill-list` sources
- ✅ FAQ accordion with 8 items
- ✅ Canonical URL with `olsp.` subdomain
- ✅ OG tags + JSON-LD (added by agent beyond spec requirement — matches blog spec)
- ✅ External link rules
- ✅ Build passes, HTTP 200

**Missing per BLOG-MASTER-SPEC (blog spec, not referenced by the agent):**
- ❌ `.quote-banner` (×3) — should replace `.cta-card`
- ❌ `.standard-cta` (×1) — post-FAQ, pre-author
- ❌ Frontmatter: has `pageTitle`/`pageDescription` — BLOG-MASTER-SPEC says "hardcoded strings only"
- ❌ `.methodology` present — BLOG-MASTER-SPEC says "not used in blog articles"
- ❌ Has GoldMasterQuote (10×) — BLOG-MASTER-SPEC doesn't use it; GOLD-MASTER-SPEC requires 3×
- ❌ TOC has no link for author section (author is at bottom of #conclusion, not separate #author)

**Verdict:** The article faithfully follows Content Production PROMPT's mandate. It is correct *against the spec the agent was told to follow*. The fix is in the specification chain, not in the article.

---

## 10. Recommendations

### Immediate (within Architecture Freeze)
1. **Correct the authority chains** — add BLOG-MASTER-SPEC to Content Production SPEC and Editorial QA SPEC (Phase 1 changes). These are documentation changes, not architectural ones.
2. **Update Content Production PROMPT** to reference BLOG-MASTER-SPEC conditionally for blog articles (as Editorial Builder SPEC already does). This is the minimum change to make future blog articles correct.

### Before lifting Architecture Freeze
3. **Answer the design question:** Does the site use shared components (OlspLayout + imports) or standalone inline files? This is the single most impactful decision.
4. **Answer the blog component question:** Are blog articles "Reviews minus some components" (applying GOLD-MASTER-SPEC selectively) or "A different architecture with QuoteBanner and Standard CTA" (BLOG-MASTER-SPEC)?

### After lifting Architecture Freeze
5. **Merge Editorial Builder and Content Production** into one writer agent path
6. **Rewrite the surviving writer PROMPT** to reference all three article-type specs with per-type component lists
7. **Regenerate or patch** `affiliate-marketing-vs-mlm.astro` to match the chosen blog spec

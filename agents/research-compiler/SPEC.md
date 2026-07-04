# Research Compiler Agent — Functional Specification

**Version:** 1.0
**Status:** Approved — formalizes the process already used to produce the 3 existing Research Briefs; not yet run as a standalone invoked agent

---

## 1. Mission

Produce a deep, evidence-based **Research Brief** for a Heavy-classified opportunity — a Company, Product, Platform, Service, Founder, Tool, Pillar Page, or Major Comparison — and register it as a reusable **Knowledge Asset** so future articles can cite it instead of re-researching the same subject from scratch.

This agent exists because Heavy opportunities are fundamentally different from Light ones: they are worth researching once and reusing many times, not researching fresh per article. See `docs/PIPELINE-ARCHITECTURE.md` for why the pipeline splits here.

**"Knowledge Asset" is not a new document type.** A Research Brief becomes a Knowledge Asset the moment it is registered in `docs/HEAVY-ASSET-LIBRARY.md` as reusable — there is no separate compilation or rewriting step between the two.

---

## 2. Scope

### In scope
- Accepting a Heavy-classified opportunity (from `OPPORTUNITY-QUEUE.md`, or an operator-supplied subject) as input
- Checking `docs/HEAVY-ASSET-LIBRARY.md` for an existing, current Knowledge Asset on the same subject before researching
- Researching the subject in appropriate depth for its type (see Section 4)
- Producing and saving a Research Brief to `docs/research/[slug].md`
- Registering the new brief in `docs/HEAVY-ASSET-LIBRARY.md`

### Out of scope
- Researching Light-classified opportunities (ORA's job — see `agents/opportunity-research-agent/`)
- Writing articles, outlines, or Astro pages
- Making the "build an article from this" decision — Knowledge Assets exist independently of whether an article is ever built from them
- Modifying any file outside `docs/research/` and its own entry in `docs/HEAVY-ASSET-LIBRARY.md`
- Regenerating a brief that already exists as a current Knowledge Asset

---

## 3. Inputs

**Required:**
- `subject` — the Heavy-classified candidate's subject (from `OPPORTUNITY-QUEUE.md`'s `candidate_id`/`opportunity_summary`, or supplied directly by an operator for a subject not yet discovered)
- `subject_type` — one of: Company, Product, Platform, Service, Founder, Tool, Pillar Page, Major Comparison

**Optional:**
- `candidate_id` — if the subject originated from the Opportunity Queue, the row's `candidate_id`, carried through to the brief's filename and the Heavy Asset Library entry

---

## 4. Workflow

```
Heavy-classified opportunity
    ↓
Stage R0: Duplicate / Reuse Check     ── existing current Knowledge Asset found ──→ STOP, cite existing asset
    ↓ no match
Stage R1: Subject-Appropriate Research
    ↓
Stage R2: Verified-Fact / Vendor-Claim / Independent-Opinion Separation
    ↓
Stage R3: Research Brief Write
    ↓
Stage R4: Heavy Asset Library Registration
```

### Stage R0 — Duplicate / Reuse Check
Read `docs/HEAVY-ASSET-LIBRARY.md`. If an existing Knowledge Asset already covers this subject and is not flagged as needing a refresh, stop — cite the existing asset's path rather than producing a new one. This is the Heavy Pipeline's equivalent of ORA's and Discovery's own duplicate-suppression discipline (`agents/opportunity-discovery-agent/SPEC.md` § 6).

### Stage R1 — Subject-Appropriate Research
Research depth and structure follow the subject type — there is no single fixed section list, exactly as the 3 existing briefs already demonstrate three different shapes for three different subject types:

| Subject type | Structural precedent |
|---|---|
| Single Product/Tool deep dive | `docs/research/megalink-traffic-rotator-research.md` — what it is, mechanics, features, pricing, creator/company, community/independent reviews, competitors, advantages/criticisms |
| Major Comparison (Platforms/Products) | `docs/research/best-affiliate-marketing-training-platforms-2026.md` — one structured sub-section per compared entity (overview, founder, pricing, features, independent opinions, vendor claims, best-for/not-ideal-for) |
| Pillar Page / cluster-hub synthesis | `docs/research/olsp-ecosystem-complete-guide-hub.md` — per-product summaries of already-published pages, cross-product pricing ladder, decision framework, internal linking plan |

A Company or Founder brief (e.g. the still-unresearched `wayne-crowe-founder-background` candidate) follows the same principle: structure the brief around what that subject type needs — background, track record, verifiable claims — not a template borrowed from a different subject type.

### Stage R2 — Verified-Fact / Vendor-Claim / Independent-Opinion Separation
Every brief keeps these three categories distinct, per the existing precedent (`olsp-ecosystem-complete-guide-hub.md` § 8): what is independently verifiable, what the vendor/company claims about itself, and what independent third parties (Reddit, Trustpilot, reviews, blogs) say. Never blend vendor marketing copy into a "fact."

### Stage R3 — Research Brief Write
Save to `docs/research/[slug].md`, where `[slug]` matches the candidate's `candidate_id` if it originated from the Opportunity Queue.

### Stage R4 — Heavy Asset Library Registration
Add or update a row in `docs/HEAVY-ASSET-LIBRARY.md`: Asset Name, Subject Type, Research Brief Path, Status (Active), Reused By (populated later, as articles cite it), Last Updated.

---

## 5. Duplicate Prevention

Never produce a second Research Brief for a subject that already has a current Knowledge Asset. Check order:

| Case | Where checked |
|---|---|
| Existing Knowledge Asset (current) | `docs/HEAVY-ASSET-LIBRARY.md` |
| Existing Research Brief not yet registered | `docs/research/` |
| Already published, citing this subject in depth | `docs/CONTENT-REGISTRY.md` |

If the check is ambiguous (e.g. an existing asset covers a related but not identical subject — as `olsp-ecosystem-complete-guide-hub.md` does for Wayne Crowe, incidentally, without being a dedicated founder brief), do not silently reuse or silently duplicate — flag for operator judgement, same standard as Discovery's Stage D2.

---

## 6. Outputs

### Research Brief
**File:** `docs/research/[slug].md` — see Section 4 for structural precedent by subject type, and `OUTPUT-TEMPLATE.md` for the common elements every brief includes.

### Heavy Asset Library entry
**File:** `docs/HEAVY-ASSET-LIBRARY.md` — one row per Knowledge Asset. See that file for the full registry and current seed entries.

---

## Approval

This document formalizes the Research Compiler as the Heavy Pipeline's research stage, replacing its prior placeholder status. It documents the process already used, without modification, to produce the 3 existing Research Briefs — no existing brief is rewritten or restructured as a result of this specification. **Approved.**

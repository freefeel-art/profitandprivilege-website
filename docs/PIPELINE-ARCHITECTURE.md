# Pipeline Architecture — Heavy and Light Production Tracks

**Status:** Approved, 2026-07-04 — architectural/documentation refactor; no existing production interrupted, no existing asset rebuilt.

Single source of truth for how an opportunity moves from discovery to a published page. Read this before touching any of the per-agent `SPEC.md`/`README.md` files listed below — it explains how they connect.

---

## Why two pipelines

Not every opportunity needs the same research depth. A page about a specific Company, Product, Platform, Service, Founder, or Tool (or a Major Comparison across several) is worth researching once and reusing across many future articles — that research becomes a long-lived editorial asset. A general topic, how-to, FAQ, or beginner guide is scoped to one article and doesn't need a standing research asset behind it.

The Opportunity Discovery Agent now classifies every candidate with a **Pipeline Type** field (`Heavy` or `Light`) at the same stage it assigns Authority Value — see `agents/opportunity-discovery-agent/SPEC.md` §§ 5a–5b. That single field determines which of the two tracks below a candidate follows once promoted.

---

## Heavy Pipeline

**Applies to:** Companies, Products, Platforms, Services, Founders, Tools, Pillar Pages, Major Comparisons.

```
Opportunity (pipeline_type: Heavy)
    ↓
Research Compiler (agents/research-compiler/)
    ↓ — checks docs/HEAVY-ASSET-LIBRARY.md first; reuses an existing Knowledge Asset if one already covers the subject
Research Brief → docs/research/[slug].md
    ↓ — registered in docs/HEAVY-ASSET-LIBRARY.md
Knowledge Asset (same document — "Knowledge Asset" is a status, not a new artifact type)
    ↓ (optional)
Editorial Builder (agents/editorial-builder/, placeholder) → Production Article
```

Article production from a Knowledge Asset is **optional** — the asset's primary purpose is to exist and be reusable, not to force a 1:1 article. A single Knowledge Asset can be cited by, and feed, several future articles (as the OLSP Ecosystem hub brief already feeds multiple published pages' internal-linking plan).

**Existing seed assets** (produced before this classification existed, cataloged here for the first time — see `docs/HEAVY-ASSET-LIBRARY.md` for the full registry):
- OLSP Ecosystem Complete Guide Hub (Pillar Page)
- Megalink Traffic Rotator (Product)
- Best Affiliate Marketing Training Platforms 2026 (Major Comparison, covers OLSP Academy)

**Known gaps** (flagged, not yet researched): LeadsMiner Pro (Product), Wayne Crowe (Founder).

---

## Light Pipeline

**Applies to:** Information Articles, How-To Articles, FAQ, Beginner Guides, Problem-Solving, General Opportunity Articles.

```
Opportunity (pipeline_type: Light)
    ↓
Opportunity Research Agent (agents/opportunity-research-agent/) — "Light Research"
    ↓
Opportunity Brief → agents/opportunity-research-agent/briefs/[slug].md
    ↓
Editorial Builder (agents/editorial-builder/, placeholder) — Writer
    ↓
Editorial QA (agents/editorial-qa/, placeholder)
    ↓
Publisher (agents/publisher/, placeholder) → Publish Ready
```

This is the pipeline's fast track: single-article-scoped research, straight through to publication. It should reuse Heavy Pipeline Knowledge Assets whenever relevant (e.g. a Light article that mentions LeadsMiner Pro in passing can cite the existing review/registry entry rather than re-researching the product), but it does not create new Knowledge Assets itself.

---

## Where each stage lives

| Stage | Pipeline | Agent folder | Status |
|---|---|---|---|
| 0. Discovery + classification | Both | `agents/opportunity-discovery-agent/` | Implemented |
| 1L. Light Research | Light | `agents/opportunity-research-agent/` (ORA) | Production, now Light-scoped (SPEC.md § 1a) |
| 2H. Research Compiler | Heavy | `agents/research-compiler/` | Formalized v1.0 |
| — | Heavy | `docs/HEAVY-ASSET-LIBRARY.md` | New registry |
| 3. Writer / Editorial Builder | Both | `agents/editorial-builder/` | Placeholder — receives either an Opportunity Brief (Light) or an optional Knowledge Asset citation (Heavy) |
| 4. Editorial QA | Both | `agents/editorial-qa/` | Placeholder |
| 5. Publisher | Both | `agents/publisher/` | Placeholder |

---

## Rules that keep the split honest

- Pipeline Type is assigned once, at Discovery, and never changes an existing 0–100 score (Opportunity Score, Priority Score) or the summary table's sort order.
- A Heavy-classified candidate never runs through ORA; a Light-classified candidate never runs through the Research Compiler.
- "Knowledge Asset" is not a new document — it is the status a Research Brief gets once registered in `docs/HEAVY-ASSET-LIBRARY.md` as reusable.
- The 3 existing Research Briefs were not rewritten to fit this architecture — they were cataloged as-is.
- Building an article from a Knowledge Asset is always optional; the asset can exist and be reused without ever itself becoming a single dedicated page.

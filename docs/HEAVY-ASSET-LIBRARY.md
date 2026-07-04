# Heavy Asset Library — Profit and Privilege

**Single source of truth for reusable Knowledge Assets produced by the Heavy Pipeline.**

Last updated: 2026-07-04

---

## What this is

A **Knowledge Asset** is a Research Brief (`docs/research/[slug].md`) that has been registered here as reusable — it is not a new document type, just the status a Research Brief gets once cataloged (see `docs/PIPELINE-ARCHITECTURE.md` and `agents/research-compiler/SPEC.md`). Before the Research Compiler produces new research for a Heavy-classified opportunity, it checks this table first — reuse an existing, current asset rather than regenerating it.

This is a **documentation-only seed**: the 3 rows below are the site's existing Research Briefs, cataloged here for the first time. No new research was produced to create this file.

---

## Registry

| Asset Name | Subject Type | Research Brief Path | Status | Reused By | Last Updated |
|---|---|---|---|---|---|
| OLSP Ecosystem Complete Guide Hub | Pillar Page | `docs/research/olsp-ecosystem-complete-guide-hub.md` | Active | `/blog/olsp-academy-complete-guide/` | 2026-07-04 |
| Megalink Traffic Rotator | Product | `docs/research/megalink-traffic-rotator-research.md` | Active | `/reviews/megalink-traffic-rotator-review/` | 2026-07-03 |
| Best Affiliate Marketing Training Platforms 2026 | Major Comparison | `docs/research/best-affiliate-marketing-training-platforms-2026.md` | Active | `/roundups/best-affiliate-marketing-training-platforms-2026/` | 2026-07-03 |

**Note on OLSP Academy coverage:** OLSP Academy itself is covered as a subject across two existing assets above (as one compared platform in the Training Platforms comparison, and as part of the ecosystem hub's per-product synthesis) rather than as its own standalone Product brief. The Research Compiler should treat this as adequate existing coverage, not a gap, unless a future Heavy opportunity specifically requires OLSP-Academy-only depth beyond what these two already provide.

---

## Known gaps (not yet researched — flagged for future Heavy Pipeline runs, not created now)

| Subject | Subject Type | Why it's a gap | Related Queue candidates |
|---|---|---|---|
| LeadsMiner Pro | Product | Only has a published review (`/reviews/leadsminer-pro-review/`); no dedicated Research Brief exists in `docs/research/` | `leadsminer-pro-alternatives-facebook-lead-tools` (unclaimed) |
| Wayne Crowe | Founder | Covered only incidentally, as founder context inside the OLSP Ecosystem hub brief — no dedicated founder-focused brief exists | `wayne-crowe-founder-background` (unclaimed) |

These are documented as gaps for the Research Compiler to fill on a future run, per the ordinary Heavy Pipeline workflow — not produced as part of this architectural refactor.

---

## Maintenance

- **Adding a row:** the Research Compiler adds/updates a row after producing or reusing a Research Brief (`agents/research-compiler/SPEC.md` § R4).
- **Status:** `Active` (current, safe to reuse) or `Needs Refresh` (subject matter may have changed — e.g. a product's pricing or founder details — and should be re-verified before further reuse).
- **Reused By:** updated by whoever builds an article citing the asset — not automated.

# Research Brief — Common Elements

There is no single fixed section list for a Research Brief — structure is subject-appropriate (SPEC.md § 4). This document lists the elements every brief includes regardless of subject type, illustrated against the 3 existing briefs. Use it as a checklist, not a rigid template.

---

## Required in every brief

| Element | Purpose | Precedent |
|---|---|---|
| **Title identifying the subject and brief type** | e.g. "[Subject] – Research Brief" or "[Subject] – Comparison Research Brief" | All 3 existing briefs |
| **What/why framing up front** | What the subject is and why this brief exists, before any detail | `megalink-traffic-rotator-research.md` §§ 1–2; `olsp-ecosystem-complete-guide-hub.md` § 1 |
| **Verified Facts / Vendor Claims / Independent Opinions kept distinct** | Never blend vendor marketing copy into a "fact" (SPEC.md § R2) | `olsp-ecosystem-complete-guide-hub.md` § 8; implicit throughout the other two via labeled subsections ("Vendor Claims (Marketing)", "Independent Opinions") |
| **Community/independent-review evidence** | Reddit, Trustpilot, independent blogs/YouTube — same intelligence sources Discovery/ORA already use | All 3 |
| **Competitive/comparative context** | Closest competing products, or (for a Major Comparison brief) the compared set itself | `megalink-traffic-rotator-research.md` § 13; `best-affiliate-marketing-training-platforms-2026.md` (comparison is the whole document) |
| **References** | Sources cited, so claims are traceable | `olsp-ecosystem-complete-guide-hub.md` § 10 |

## Included when relevant to the subject type

| Element | When it applies |
|---|---|
| Pricing / plans / upsell structure | Product, Platform, Company briefs |
| Company, Founder(s), launch year | Product, Platform, Company briefs |
| Per-entity sub-sections (one per compared item) | Major Comparison briefs |
| Per-page summaries of already-published content + cross-linking plan | Pillar Page / cluster-hub synthesis briefs |
| Background, track record, verifiable claims about the individual | Founder briefs (no existing precedent yet — `wayne-crowe-founder-background` is the first candidate that will need this shape) |

---

## Heavy Asset Library registration (required for every brief, not part of the brief file itself)

After saving the brief, add or update its row in `docs/HEAVY-ASSET-LIBRARY.md`:

```
Asset Name:          [subject name]
Subject Type:        [Company / Product / Platform / Service / Founder / Tool / Pillar Page / Major Comparison]
Research Brief Path: docs/research/[slug].md
Status:              [Active / Needs Refresh]
Reused By:           [pages that cite this asset, updated as they're built]
Last Updated:        [YYYY-MM-DD]
```

# Research Compiler Agent

**Pipeline position:** Stage 2 of the AI Editorial Operating System — the Heavy Pipeline's sole research stage
**Status:** Formalized (v1.0) — documents the process already used to produce the 3 existing Research Briefs; not yet run as a standalone invoked agent

---

## What it does

The Research Compiler takes a Discovery Queue candidate tagged `pipeline_type: Heavy` (SPEC.md § 5b in `agents/opportunity-discovery-agent/`) and produces a **Research Brief** — a deep, subject-appropriate research document about a specific Company, Product, Platform, Service, Founder, Tool, Pillar Page, or Major Comparison. The brief is saved to `docs/research/[slug].md` and cataloged in `docs/HEAVY-ASSET-LIBRARY.md` as a reusable **Knowledge Asset** — the same document, no new artifact, just a "this exists and can be reused" registry entry.

It does not write articles. It does not decide whether an article gets built from the brief — that remains optional, per candidate.

---

## Where it fits (Heavy Pipeline)

```
[Discovery Queue] → candidate tagged Pipeline Type: Heavy
           ↓
     Check docs/HEAVY-ASSET-LIBRARY.md — does a reusable Knowledge Asset already cover this subject?
           ↓ no match
  2. Research Compiler          ← YOU ARE HERE
           ↓
     Research Brief → docs/research/[slug].md
           ↓
     Registered in docs/HEAVY-ASSET-LIBRARY.md as a Knowledge Asset
           ↓
  3. Editorial Builder          ← placeholder — (optional) Production Article
```

Heavy-classified candidates do **not** pass through the Opportunity Research Agent (ORA) — ORA is now scoped to the Light Pipeline only. See `docs/PIPELINE-ARCHITECTURE.md` for the full two-pipeline diagram.

---

## Inputs

**Required:**
- A Discovery Queue candidate (or an operator-supplied subject) whose `pipeline_type` is `Heavy`.

**Before starting new research:** check `docs/HEAVY-ASSET-LIBRARY.md` for an existing Knowledge Asset on the same subject. If one exists and is current, reuse it — do not regenerate. This mirrors ORA's own Stage 0 duplicate-check discipline.

---

## Output

A **Research Brief**, saved to:

```
docs/research/[slug].md
```

There is no single fixed section list — format is subject-appropriate, exactly as it already is across the 3 existing briefs (a single-product deep dive, a multi-product comparison, and a cross-product hub synthesis each look different). See `OUTPUT-TEMPLATE.md` for the common elements every brief includes regardless of subject type, and the 3 existing files as worked precedent:

- `docs/research/megalink-traffic-rotator-research.md` — single Product deep dive
- `docs/research/best-affiliate-marketing-training-platforms-2026.md` — Major Comparison across 4 Platforms
- `docs/research/olsp-ecosystem-complete-guide-hub.md` — Pillar Page / cluster-hub synthesis

Once written, register the brief as a Knowledge Asset in `docs/HEAVY-ASSET-LIBRARY.md`.

---

## Documents in this folder

| File | Purpose |
|---|---|
| `README.md` | This file — overview and quick reference |
| `SPEC.md` | Full specification: mission, workflow, duplicate-check, output format |
| `PROMPT.md` | The agent system prompt and user prompt template |
| `OUTPUT-TEMPLATE.md` | The common elements every Research Brief includes, regardless of subject-specific structure |

---

## What this agent does NOT do

- Research Light-classified candidates (those go to ORA)
- Write articles, outlines, or Astro pages
- Make publishing decisions
- Regenerate a Research Brief that already exists as a current Knowledge Asset in `docs/HEAVY-ASSET-LIBRARY.md`
- Modify any file outside `docs/research/` and its own registration entry in `docs/HEAVY-ASSET-LIBRARY.md`

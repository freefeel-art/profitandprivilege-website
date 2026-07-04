# Editorial Builder Agent — Placeholder

**Pipeline position:** Stage 3 of the AI Editorial Operating System — the "Writer" step for both pipelines
**Status:** Not yet designed — current Builder V1 (manual workflow) will migrate here

---

## Pipeline awareness (added with the Heavy/Light split, see `docs/PIPELINE-ARCHITECTURE.md`)

This stage now receives input from two possible upstream paths, not one:

- **Light Pipeline:** an Opportunity Brief from `agents/opportunity-research-agent/` (ORA).
- **Heavy Pipeline (optional):** a Knowledge Asset citation — a Research Brief registered in `docs/HEAVY-ASSET-LIBRARY.md` by the Research Compiler. Building an article from a Knowledge Asset is optional; the asset can exist and be reused without a dedicated article ever being built from it.

This does not change this stage's design status — it remains undesigned until Builder V1 migrates here — but any future design should account for both entry points rather than assuming a single upstream shape.

## Role

Takes an approved Research Brief as input and produces a complete, Gold Master-compliant Astro page ready for QA.

## Input

- Approved Research Brief from the Research Compiler Agent

## Output

- A fully built `.astro` file placed in the correct `src/pages/` subdirectory, matching the Gold Master specification exactly

## Notes

The current manual Builder workflow (documented in `docs/PRODUCTION-MASTER-PROMPT.md` and `docs/GOLD-MASTER-SPEC.md`) will be migrated into this agent when the upstream pipeline stages are stable.

## What it does NOT do

- Make publishing decisions
- Modify production without QA approval
- Alter any file outside `src/pages/`

---

Design begins after the Research Compiler Agent is live and producing approved Research Briefs.

# Editorial Builder Agent — Placeholder

**Pipeline position:** Stage 3 of the AI Editorial Operating System  
**Status:** Not yet designed — current Builder V1 (manual workflow) will migrate here

---

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

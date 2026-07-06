# Editorial Builder Agent — V1

## Pipeline Position

Stage 3 of the two-track production pipeline (PIPELINE-ARCHITECTURE.md). Receives from:
- **Light Pipeline:** Opportunity Brief from ORA
- **Heavy Pipeline:** Knowledge Asset / Research Brief from Research Compiler

## Purpose

Transform an approved brief into a complete, publication-ready article file.

## Responsibilities

- Read and interpret the brief (Opportunity Brief or Research Brief)
- Determine article structure from content type
- Write each section using only evidence from the brief
- Assemble complete standalone `.astro` file
- Copy CSS and JS verbatim from Gold Master reference

## Non-Responsibilities

- Conducting new research
- Inventing facts to fill gaps
- Making editorial decisions about what to publish
- Performing QA (Stage 4)
- Modifying briefs or any upstream files

## Output

A single `.astro` file at `src/pages/{section}/{slug}.astro`:

| Content Type | Location |
|---|---|
| Review | `src/pages/reviews/` |
| Blog / informational | `src/pages/blog/` |
| Roundup | `src/pages/roundups/` |
| Investigation | `src/pages/` (root) |

## Next Stage

Editorial QA — validates the article against the brief and editorial standards.

# Editorial QA Agent — Placeholder

**Pipeline position:** Stage 4 of the AI Editorial Operating System  
**Status:** Not yet designed — awaiting Editorial Builder design

---

## Role

Takes a built Astro page as input and validates it against the Gold Master specification before it is approved for publication.

## Input

- Built `.astro` file from the Editorial Builder Agent

## Output

- QA Report: a structured pass/fail checklist covering structural compliance, CTA placement, pill-list sources, site footer, canonical URL, metadata, accessibility, and build verification
- Status: APPROVED / REQUIRES REVISION / REJECTED

## Validation scope (anticipated)

- Gold Master layout compliance (grid, CSS tokens, JS)
- Three CTA cards present and identical, in correct positions
- Pill-list sources section present
- Site footer inside `<main>` after sources
- Canonical URL correct and absolute with trailing slash
- `prerender = true` present
- `<script is:inline>` directive present
- Build passes with zero errors
- No fabricated data, invented testing, or unverified claims flagged

## What it does NOT do

- Modify content
- Make editorial decisions
- Approve publication

---

Design begins after the Editorial Builder Agent is designed and the QA checklist is fully specified.

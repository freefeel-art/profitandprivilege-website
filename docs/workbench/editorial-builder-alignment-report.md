# Editorial Builder — ADR-001 Alignment Report

**Date:** 2026-07-12
**Status:** Aligned

## Background

ADR-001 (`docs/architecture/ADR-001-EDITORIAL-BUILDER-ARCHITECTURE.md`) mandates that the Editorial Builder shall produce complete, self-contained `.astro` files with zero imports — no layout components, no shared partials, no body-only output. Each output file must contain its own HTML document, CSS style block, and JavaScript behaviour block.

The previous v2.1 PROMPT.md (untracked draft) violated ADR-001 by referencing `OlspLayout`, body-only output, and a shared-component architecture that does not exist. The PLACEHOLDER.md was a stub that did not define the agent's behaviour.

## Previous Implementation Sprint — Completed Actions

| Action | File | Status |
|---|---|---|
| Rewrite system prompt for ADR-001 compliance | `agents/editorial-builder/PROMPT.md` | Done |
| Replace PLACEHOLDER.md with proper documentation | `agents/editorial-builder/README.md` | Done |
| Create technical output specification | `agents/editorial-builder/SPEC.md` | Done |
| Create structural output template | `agents/editorial-builder/OUTPUT-TEMPLATE.md` | Done |
| Delete PLACEHOLDER.md | — | Done |
| Scan all files for ADR-001 violations | All four files | Done — zero violations |

## Compliance Verification

Searched for: `OlspLayout`, `body-only`, `shared.component`, `import.*Layout`, `import.*from`, `body.only`

**Result:** Zero matches across all four files in `agents/editorial-builder/`.

Every file enforces the self-contained architecture:
- `PROMPT.md` — explicitly prohibits imports, mandates `prerender = true`, full HTML document
- `SPEC.md` — defines file format with `export const prerender = true;` as the only frontmatter entry
- `OUTPUT-TEMPLATE.md` — shows a complete `<!DOCTYPE html>` through `</html>` structure with inline CSS/JS
- `README.md` — documents the self-contained file architecture as a hard boundary

## Recommended Next Steps

1. Implementation sprint can begin: connect the Editorial Builder to an upstream research pipeline
2. When new article types are introduced (e.g., comparison, guide), update `SPEC.md` per-type mapping before the PROMPT.md
3. Gold Master spec changes (CSS tokens, new components) should be mirrored in the OUTPUT-TEMPLATE.md and SPEC.md before the PROMPT.md

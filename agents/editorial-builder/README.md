# Editorial Builder Agent

Generates complete, self-contained Astro article files for the Profit and Privilege website. Produces Gold Master-compliant `.astro` files for reviews, blog articles, and roundups.

## Architecture

The Editorial Builder follows a **self-contained file architecture** (ADR-001): every output is a single `.astro` file with zero imports, containing its own HTML, CSS, and JavaScript inline. No layout components, no shared partials, no external templates.

## Files

| File | Purpose |
|---|---|
| `PROMPT.md` | System prompt — the primary instruction set for the AI agent |
| `SPEC.md` | Technical output specification — component inventory, per-type mapping |
| `OUTPUT-TEMPLATE.md` | Structural template showing the expected `.astro` file layout |

## External Specs Referenced

| Spec | Applies To |
|---|---|
| `docs/GOLD-MASTER-SPEC.md` | All article types — CSS, JS, responsive, structural baseline |
| `docs/BLOG-MASTER-SPEC.md` | Blog articles — overrides Gold Master for OG/JSON-LD, QuoteBanner, Standard CTA |
| `docs/ROUNDUP-GOLD-MASTER-SPEC.md` | Roundup articles — comparison tables, Author Box, quiz logic |
| `docs/CONTENT-REGISTRY.md` | All article types — internal link targets |
| `docs/PRODUCTION-MASTER-PROMPT.md` | Manual builder prompt — reference for correct output format |

## Output Location

| Type | Path |
|---|---|
| Reviews | `src/pages/reviews/{slug}.astro` |
| Blog | `src/pages/blog/{slug}.astro` |
| Roundups | `src/pages/roundups/{slug}.astro` |

## Workflow

1. Read the relevant spec and builder prompt for the article type
2. Generate a self-contained `.astro` file matching the Gold Master structural standard
3. Verify zero imports, correct `target`/`rel` attributes on all external links
4. Run `astro build` and fix any errors
5. Start `astro dev --background` and verify the page returns HTTP 200

## Related

- `docs/architecture/ADR-001-EDITORIAL-BUILDER-ARCHITECTURE.md` — the approved architecture decision

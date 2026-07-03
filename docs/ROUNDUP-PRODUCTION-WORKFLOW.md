# Roundup Production Workflow

## Pipeline

Product Category
        ↓
Perplexity Comparison Research Brief
        ↓
Universal Article Builder (`docs/PRODUCTION-MASTER-PROMPT.md`)
        (Article Type: roundups)
        ↓
Astro Roundup Article → `src/pages/roundups/[slug].astro`
        ↓
npm run build
        ↓
Playwright QA
        ↓
Human QA
        ↓
git commit
        ↓
git push
        ↓
Cloudflare Pages
        ↓
Google Search Console

---

## Required Documents

- `docs/GOLD-MASTER-SPEC.md` — Universal layout, CSS, and JS standard
- `docs/PRODUCTION-MASTER-PROMPT.md` — Universal article builder
- `docs/ROUNDUP-GOLD-MASTER-SPEC.md` — Roundup-specific content structure
- `docs/ROUNDUP-MASTER-PROMPT.md` — Roundup-specific generation instructions
- Comparison Research Brief

---

## Editorial Rules

- Preserve the Gold Master architecture (layout, CSS tokens, JS, breakpoint).
- Never invent testing or personal experience.
- Distinguish verified facts, vendor claims, independent opinions, and editorial analysis.
- Prefer original sources whenever practical.
- Link naturally to detailed review pages.
- Link to supporting informational articles when available.

---

## Production Rule

The roundup pipeline is considered stable.

Do not redesign the architecture unless a genuine production issue is discovered.

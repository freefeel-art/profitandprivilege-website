# ROUNDUP PRODUCTION WORKFLOW

## Pipeline

Product Category
        ↓
Perplexity Comparison Research Brief
        ↓
Claude Code
        ↓
Astro Roundup Article
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

- ROUNDUP-GOLD-MASTER-SPEC.md
- ROUNDUP-MASTER-PROMPT.md
- Comparison Research Brief

---

## Editorial Rules

- Preserve the Gold Master architecture.
- Never invent testing or personal experience.
- Distinguish verified facts, vendor claims, independent opinions, and editorial analysis.
- Prefer original sources whenever practical.
- Link naturally to detailed review pages.
- Link to supporting informational articles when available.

---

## Production Rule

The roundup pipeline is considered stable.

Do not redesign the architecture unless a genuine production issue is discovered.

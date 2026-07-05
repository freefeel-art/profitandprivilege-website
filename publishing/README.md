# Publishing Engine V1

Deterministic workflow that safely transforms a QA-approved publication candidate into a published asset.

## Purpose

The Publishing Engine executes the publication workflow after Editorial QA has returned `READY FOR PUBLICATION`. It must never publish content that has not passed QA.

## Principles

- **Deterministic** — same inputs always produce same outputs. No AI reasoning.
- **Fail-safe** — any validation failure blocks publication with a precise reason.
- **Auditable** — every publication produces a complete Publication Report.
- **Non-destructive** — never modifies editorial content. Only commits, builds, and deploys.

## Usage

```bash
# Publish a single article by slug
node publishing/publish.js is-olsp-academy-an-mlm

# Publish multiple articles in one batch
node publishing/publish.js is-olsp-academy-an-mlm fastbots-chatbot-wrong-answers

# Publish all QA-approved articles
node publishing/publish.js --all
```

## Stages

1. **Publication Validation** — verify QA report, file existence, build, metadata, slug uniqueness
2. **Git** — commit publication changes to the repository
3. **Build** — production `astro build`, abort on errors
4. **Deploy** — deploy via Netlify CLI
5. **Post-Deployment Validation** — verify HTTP 200, metadata, canonical, sitemap
6. **Search Engine Submission** — prepare sitemap ping, note indexing is not immediate
7. **Publication Report** — generate comprehensive markdown report

## Output

Publication Reports are written to `reports/publication/`.

## Dependencies

- Node.js >= 22.12.0
- Netlify CLI (`netlify`)
- Astro (`astro`)
- Git

## Non-Goals

- Does not rewrite, edit, or improve content
- Does not make editorial decisions
- Does not replace AI agents in the editorial pipeline
- Does not create or delete files outside the publication workflow

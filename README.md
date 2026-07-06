# Profit and Privilege — olsp.profitandprivilege.com

An Astro static site publishing independent, research-based reviews and informational content in the affiliate marketing / online income niche. Primary monetization is the OLSP Academy affiliate program via the OLSP Megalink funnel.

Review articles use the **OLSP Standard V1** shared component system (`src/components/olsp-standard/`): OlspLayout provides the document shell, CSS tokens, SEO metadata (OG tags, Twitter Cards, JSON-LD), TOC, and JS. Blog and roundup articles remain fully self-contained `.astro` files. See `PROJECT-STATUS.md` for current site status and `docs/CONTENT-REGISTRY.md` for the full published content inventory.

## Key Documentation

Before making changes, read the relevant standard:

| Task | Read first |
|---|---|
| Editing or building a review article | `docs/GOLD-MASTER-SPEC.md`, `docs/PRODUCTION-MASTER-PROMPT.md` |
| Editing or building a roundup article | `docs/ROUNDUP-GOLD-MASTER-SPEC.md`, `docs/ROUNDUP-MASTER-PROMPT.md` |
| Editing or building a blog article | `docs/BLOG-MASTER-SPEC.md`, `docs/BLOG-MASTER-PROMPT.md` |
| Adding/updating internal links or new content | `docs/CONTENT-REGISTRY.md` |
| Running the Opportunity Research Agent | `agents/opportunity-research-agent/` |
| General working rules for AI agents on this repo | `AGENTS.md` |

## AI Onboarding

All AI assistants working in this repository must begin by reading:

/ai/01-CHATGPT-ARCHITECT.md

The remaining onboarding files are read in the order defined by:

/ai/03-READING-ORDER.md

## Project Structure

```text
/
├── docs/                        Production specs and builder prompts
├── agents/                      AI editorial pipeline (ORA + placeholder stages)
├── src
│   ├── pages
│   │   ├── reviews/              Review articles
│   │   ├── blog/                 Blog / informational articles
│   │   ├── roundups/             Roundup articles
│   │   └── authors/               Author profile page(s)
│   └── assets
└── package.json
```

## Commands

All commands are run from the root of the project, from a terminal:

| Command | Action |
|---|---|
| `npm install` | Installs dependencies |
| `npm run dev` | Starts local dev server at `localhost:4321` |
| `npm run build` | Build the production site to `./dist/` |
| `npm run preview` | Preview the build locally, before deploying |
| `npm run astro ...` | Run CLI commands like `astro add`, `astro check` |

For AI-agent sessions, prefer `astro dev --background` and manage it with `astro dev stop` / `astro dev status` / `astro dev logs` — see `CLAUDE.md`.

## Repository Scope

This repository is a static content site only. The following are intentionally **out of scope** — there is no code for any of these here, and none should be added without a deliberate architectural decision:

- **AI generation at runtime** — no LLM/API calls happen when the site serves a page. Article content is authored offline (via the builder prompts in `docs/`) and committed as static HTML/Astro; nothing is generated on request.
- **Image generation** — no image-generation APIs or pipelines. Images (e.g. author photo) are static assets checked into `src/assets` / `public`.
- **Backend APIs / server routes** — no `/api` directory, no serverless functions, no server-side request handling. Every page has `prerender = true` and ships as static HTML.
- **Authentication / user accounts** — no login, sessions, or user data of any kind.
- **Database / persistent storage** — no database, ORM, or data layer. Content lives in version-controlled files.
- **Environment variables / secrets** — no `.env` files or runtime secrets. There is nothing to configure at deploy time beyond the static build.
- **Payment processing / checkout** — monetization is affiliate links only (OLSP Megalink); no payment or checkout flow is handled by this site.
- **Analytics / tracking scripts** — no analytics integration is currently wired in, despite some article content discussing analytics/marketing tools editorially.

If a task assumes any of the above exists (e.g. an API integration, an `.env` variable, a generation pipeline), treat that as a sign the task targets a different repository, or as a deliberate new feature that needs explicit scoping before implementation.

## Documentation

Full Astro documentation: https://docs.astro.build

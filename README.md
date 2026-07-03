# Profit and Privilege — olsp.profitandprivilege.com

An Astro static site publishing independent, research-based reviews and informational content in the affiliate marketing / online income niche. Primary monetization is the OLSP Academy affiliate program via the OLSP Megalink funnel.

Every article page is a fully self-contained `.astro` file (`prerender = true`, no shared layouts) built to the **Gold Master V1** standard. See `PROJECT-STATUS.md` for current site status and `docs/CONTENT-REGISTRY.md` for the full published content inventory.

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

## Documentation

Full Astro documentation: https://docs.astro.build

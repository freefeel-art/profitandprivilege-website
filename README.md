# OLSP.PROFITANDPRIVILEGE.COM — Editorial Operating System

We solve real user problems in the affiliate marketing and online income space. Every article starts with a question someone is asking, a frustration they're hitting, or a goal they're trying to reach. We produce research-backed answers, not product pages. OLSP is never the topic — it's the natural next step only when it genuinely helps solve the user's problem. The site is built with [Astro](https://astro.build) and generated as a fully static site — no database, no backend, no runtime AI.

## Project Mission

Identify real user problems in the affiliate marketing and online income space. Produce authoritative, research-backed solutions. Always start with the problem — never with a product or promotion. Publish via a reproducible editorial pipeline. Every output is version-controlled, reviewed, and statically deployed.

## Editorial Operating System

The repository defines a structured editorial pipeline with eight stages, each backed by an agent prompt, output template, and handoff specification. Runtime readiness and execution status are not maintained in this table:

| Stage | Definition |
|---|---|
| Community Intelligence | `agents/community-intelligence/` |
| Editorial Intelligence | `agents/editorial-intelligence/` (via CI) |
| Opportunity Discovery | `agents/opportunity-discovery-agent/` |
| Opportunity Research | `agents/opportunity-research-agent/` |
| Research Factory | `agents/research-factory/` |
| Content Production | `agents/editorial-builder/` |
| Editorial QA | `agents/editorial-qa/` |
| Publishing | `publishing/publish.cjs` |

Pipeline definitions remain in `pipeline/`; mutable run state is tracked in
`runtime/editorial-pipeline/state.json`. Handoffs between stages follow
`docs/PIPELINE-HANDOFF-STANDARD.md`.

## Mission Control

The operational dashboard lives at `/mission-control/` — a single-page control center for the entire Editorial OS:

- **Run Pipeline** — natural language input + pipeline mode selection (Discover / Produce / Full)
- **Live Pipeline Console** — real-time event stream during pipeline execution
- **Pipeline Progress** — visual stage tracking (Queued → Starting → Running → Completed)
- **Pipeline Summary** — mode, topic, status, elapsed time, current stage
- **Results Panel** — output artifacts that populate after a pipeline run
- **Pipeline Health** — overall system status indicator
- **Pipeline Status** — live stage states from `runtime/editorial-pipeline/state.json`
- **Production Overview** — metrics dashboard (opportunities, briefs, articles, reports)
- **Quick Access** — links to all pipeline artifacts and documentation

Mission Control is the front door for all editorial operations. See `src/pages/mission-control.astro` and `src/components/mission-control/`.

## Architecture Capabilities

- **Production site**: [olsp.profitandprivilege.com](https://olsp.profitandprivilege.com); source routes are defined under `src/pages/`
- **OLSP Standard**: shared component system under `src/components/olsp-standard/`
- **Page architecture**: editorial pages use the shared layout contract where their article standard requires it
- **Editorial QA**: validates every article against OlspLayout compliance, SEO metadata, internal linking, and schema.org markup; generates structured QA reports
- **Publishing Engine**: `publishing/publish.cjs` — validates QA report, runs Astro build, writes publication report; supports both single-slug and full-site builds
- **Pipeline Integration**: handoff chain from opportunity queue through research, production, QA, and publishing; mutable state stays under `runtime/`
- **Production Reports**: pipeline readiness audit and production readiness verification completed — documented in `docs/reports/`

## Repository Structure

```
/
├── agents/                        # 8 pipeline agents (prompts + templates)
│   ├── community-intelligence/
│   ├── content-production/
│   ├── editorial-builder/
│   ├── editorial-qa/
│   ├── opportunity-discovery-agent/
│   ├── opportunity-research-agent/  # includes briefs/
│   ├── publisher/
│   ├── research-compiler/
│   └── research-factory/
├── docs/                          # Specs, reports, research
│   ├── reports/                   # Pipeline Readiness Report, Production Readiness Report
│   ├── research/                  # Heavy research briefs
│   ├── AI-EDITORIAL-OPERATING-SYSTEM.md
│   ├── CONTENT-REGISTRY.md        # Full published content inventory
│   ├── GOLD-MASTER-SPEC.md        # UI/UX standard
│   ├── PIPELINE-ARCHITECTURE.md   # Two-track pipeline architecture
│   └── PIPELINE-HANDOFF-STANDARD.md
├── publishing/                    # Publishing engine
│   ├── publish.cjs                # CLI: publish.cjs <slug> --qa <qa-report-path>
│   ├── CHECKLIST.md
│   └── WORKFLOW.md
├── reports/                       # Generated reports from pipeline runs
│   ├── community-intelligence/
│   ├── editorial-intelligence/
│   ├── editorial-qa/
│   ├── handoff/
│   ├── production-validation/
│   ├── publication/
│   └── research-briefs/
├── scripts/                       # Build and migration utilities
│   ├── prebuild.mjs               # Copies docs/reports to public/ for static serving
│   └── migrate-blog.js
├── src/
│   ├── components/
│   │   ├── mission-control/       # Dashboard components (7 panels)
│   │   └── olsp-standard/         # Shared layout system (11 components)
│   ├── data/
│   │   └── mission-control.js     # Build-time data layer
│   ├── pages/
│   │   ├── reviews/               # 14 review articles
│   │   ├── blog/                  # 25 blog / informational articles
│   │   ├── roundups/              # Roundup articles
│   │   ├── mission-control.astro  # Operational dashboard
│   │   └── index.astro
│   └── scripts/
│       └── pipeline-runner.js     # Pipeline state store + simulation engine
├── pipeline/
│   └── state.example.json         # Runtime-state schema example
├── astro.config.mjs
└── package.json
```

## Quick Start

```bash
npm install
npm run dev        # Start dev server at localhost:4321
npm run build      # Build production site to dist/
npm run preview    # Preview built site locally
```

For AI-agent sessions: `astro dev` runs in the background and is managed via process supervision. See `AGENTS.md` for working rules.

## Development Workflow

1. **Research** — Community Intelligence + Editorial Intelligence identify opportunities; Opportunity Discovery Agent scores and queues candidates; briefs go to the Research Factory
2. **Produce** — Editorial Builder generates articles from briefs using GOLD-MASTER-SPEC.md and the appropriate master prompt
3. **QA** — Editorial QA validates against OlspLayout, SEO, schema, internal linking
4. **Publish** — `publishing/publish.cjs <slug> --qa <qa-report-path>` builds and reports

All stages run offline. Output is committed to version control. No runtime AI generation.

## Future Roadmap

- **Pipeline Runner** — dedicated orchestration layer to execute full pipeline runs with a single command
- **Real-time Execution** — connect Mission Control Run Pipeline to live agent execution
- **Analytics Dashboard** — content performance tracking
- **Automated Scheduling** — recurring content opportunity scans via Community Intelligence

## Architecture

This repository enforces strict separation:

- **Mission Control** — visualizes and orchestrates (no agent calls)
- **Pipeline Runner** — single execution entry point (planned)
- **Agents** — perform the work (prompts + templates only)
- **Static Site** — production output (no backend, no database)

# Project Snapshot — 2026-07-07

## Architecture Status

| Component | Status | Notes |
|---|---|---|
| Production Site | **Live** | 44 static pages at olsp.profitandprivilege.com |
| OLSP Standard | **Complete** | 11 components, all pages migrated |
| Editorial QA | **Operational** | Validates every article pre-publish |
| Publishing Engine | **Operational** | CLI-based, QA-gated |
| Pipeline Integration | **Complete** | 8-stage handoff chain, state persisted |
| Mission Control V1 | **Complete** | Dashboard with Run Pipeline, metrics, reports |
| Mission Control V2 | **Complete** | Pipeline Console, Progress, Summary, Results, Health |
| Pipeline Runner | **Planned** | Interface defined in pipeline-runner.js, execution pending |
| Architecture Freeze | **Active** | No redesign permitted without review |

## Production Pipeline

The editorial pipeline runs offline. Each stage is a self-contained agent with a prompt and output template:

```
Community Intelligence
  → Editorial Intelligence (via CI agent)
    → Opportunity Discovery (OPPORTUNITY-QUEUE.md)
      → Opportunity Research (briefs/)
        → Research Factory (heavy research briefs)
          → Content Production (article .astro files)
            → Editorial QA (QA reports)
              → Publishing (astro build + pub reports)
```

**State file**: `pipeline/state.json`
**Handoff standard**: `docs/PIPELINE-HANDOFF-STANDARD.md`

## Mission Control

**URL**: `/mission-control/` (prerendered static page)

### Panels
1. **Run Pipeline** — natural language input + 3 pipeline modes (Discover/Produce/Full)
2. **Pipeline Health** — overall status indicator (Operational/Busy/Error)
3. **Live Pipeline Console** — dark-themed terminal event timeline
4. **Pipeline Progress** — numbered stage nodes with independent status
5. **Pipeline Summary** — mode, topic, status, current stage, elapsed timer
6. **Results** — slot-based output artifact placeholders
7. **Output Locations** — directory ready/waiting indicators
8. **Pipeline Status** — live stage states from `pipeline/state.json`
9. **Production Overview** — metrics (opportunities, briefs, articles, reports)
10. **Recent Activity** — last 15 git commits
11. **Production Reports** — indexed report files
12. **Quick Access** — 14 direct links to pipeline artifacts

### Key Files
- `src/pages/mission-control.astro` — page shell
- `src/data/mission-control.js` — build-time data layer (filesystem reads)
- `src/scripts/pipeline-runner.js` — client-side state store + mock simulation
- `src/components/mission-control/` — 10 Astro components
- `scripts/prebuild.mjs` — copies docs/reports to `public/` for static serving

## Implemented Components

### Production
- 44 static pages (14 reviews, 25 blog, 1 roundup, 3 root informational, 1 author)
- 11 OlspLayout components
- 8 agent directories with prompts and templates
- 10 documentation specs
- 7 report directories (CI, EI, QA, handoff, validation, publication, research-briefs)
- Publishing CLI (`publishing/publish.cjs`)

### Dashboard (Mission Control)
- 10 dashboard components (7 V2 panels + 3 utility)
- Build-time data layer
- Client-side pipeline state store
- Prebuild asset copy script

### Infrastructure
- Astro 7 static site
- @astrojs/sitemap integration
- 110+ git commits, main branch
- GitHub repository configured with description, homepage, 10 topics

## Remaining Work

### Pipeline Runner (Next Sprint)
- Dedicated orchestration layer
- Single entry point for full pipeline execution
- Connects Mission Control Run Pipeline to real agent execution
- Should call agents indirectly, never directly from Mission Control

### Future Opportunities
- Automated Community Intelligence scanning schedules
- Analytics dashboard integration
- Content performance tracking
- Agent output quality metrics

## Next Sprint: Pipeline Runner

**Objective**: Implement a dedicated Pipeline Runner that takes a topic and mode from Mission Control and orchestrates the full agent pipeline.

**Constraints**:
- Architecture Freeze remains active
- No redesign of Mission Control or existing pipeline
- Pipeline Runner is a NEW component, not a modification
- Must maintain separation: MC → Runner → Agents

**Integration point**: `src/scripts/pipeline-runner.js` — the `simulatePipeline()` function is the interface. Replace its mock implementation with real orchestration.

**Delivery**: Single command: `pipeline-runner.cjs <topic> --mode <mode>` that walks through all stages, generates artifacts, and updates `pipeline/state.json`.

## Key Contacts

- **Repository**: github.com/freefeel-art/profitandprivilege-website
- **Site**: olsp.profitandprivilege.com
- **Dashboard**: olsp.profitandprivilege.com/mission-control/

---

*Generated 2026-07-07. Update this document when architecture changes.*

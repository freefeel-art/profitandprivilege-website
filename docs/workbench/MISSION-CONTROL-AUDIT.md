# Mission Control — Repository Audit

**Audit Date:** 2026-07-12  
**Auditor:** OpenCode Production Mode  
**Purpose:** Document the current state of Mission Control as the operational front-end for the AI Editorial Operating System.

---

## 1. Repository Audit Summary

Mission Control is a fully implemented operational dashboard for the AI Editorial Operating System. It provides a visual interface for discovering content opportunities, running editorial pipelines, monitoring production metrics, and tracking repository status.

The implementation spans **10 Astro components**, **1 data module**, **1 runner script**, **1 page route**, and **1 state file**.

---

## 2. Located Files

### Core Page

| File | Exists | Purpose | Build Status | Completeness |
|------|--------|---------|-------------|--------------|
| `src/pages/mission-control.astro` | Yes | Main dashboard page — orchestrates all panels and sections, injected with live data | Builds cleanly (49 pages, 1.89s) | Complete |
| `dist/mission-control/index.html` | Yes | Built static output (57,974 bytes) | Generated | Complete |

### Components (`src/components/mission-control/`)

| File | Exists | Purpose | Completeness |
|------|--------|---------|--------------|
| `RunPipeline.astro` | Yes | Topic input, mode selection (Discover/Produce/Full), validation UI, run trigger with simulated pipeline execution | Complete |
| `PipelineHealth.astro` | Yes | Live status indicator bar showing pipeline operational state via store subscription | Complete |
| `PipelineConsole.astro` | Yes | Terminal-style event log with dot-based stage status indicators; live-updates via pipelineStore | Complete |
| `PipelineProgress.astro` | Yes | Visual stage progress track with numbered nodes, colour states, and pulse animation for active stage | Complete |
| `PipelineSummary.astro` | Yes | Summary card grid (Mode, Topic, Status, Current Stage, Elapsed, Runner status); live elapsed timer | Complete |
| `ResultsPanel.astro` | Yes | Displays pipeline run results (Opportunity, Research Brief, Article, QA Report, Publish Report) | Complete |
| `OutputLocations.astro` | Yes | Directory existence check for 5 output locations (reviews, blog, research, QA, pub reports) | Complete |
| `StatusBadge.astro` | Yes | Reusable pill badge with dot + label (complete/running/waiting/failed) — used in Pipeline Status section | Complete |
| `MetricCard.astro` | Yes | Reusable card displaying a large numeric value, label, and optional sublabel | Complete |
| `ActivityItem.astro` | Yes | Reusable row displaying git commit hash, subject, and relative timestamp | Complete |

### Data Layer

| File | Exists | Purpose | Completeness |
|------|--------|---------|--------------|
| `src/data/mission-control.js` | Yes | Server-side data module — reads pipeline state, infers stage status from file system, counts production metrics, fetches git activity and repo status, generates quick links with existence checks | Complete |

### Runner & Pipeline Scripts

| File | Exists | Purpose | Completeness |
|------|--------|---------|--------------|
| `src/scripts/pipeline-runner.js` | Yes | Client-side pipeline simulation engine — event-driven `PipelineStore` class with pub/sub, stage progression with templated event sequences, 3 mode configs (discover/produce/full), timer management for elapsed tracking | Complete |
| `pipeline/state.json` | Yes | Static state file — defines 5 pipeline stages (discovery, research, builder, QA, publish) with status, agent mapping, and run history array | Partial — `lastRun` is `null`, `runs` array empty |
| `pipeline/PROMPT.md` | Yes | Orchestrator execution prompt for AI agents — defines 5-stage pipeline workflow, handoff protocol, rules | Complete |
| `pipeline/run.sh` | Yes | Bash entrypoint that wraps the orchestrator prompt for CLI execution | Complete |

---

## 3. Current Architecture

### Page Route
- **URL:** `/mission-control/`  
- **Layout:** Wraps content in `OlspLayout` (standard site layout with TOC, CSS design tokens)  
- **Sections in order:** Pipeline Runner → Pipeline Health → V2 Grid (Console, Progress, Results + Output, Summary) → Pipeline Status → Production Overview → Recent Activity → Production Reports → Repository Status → Quick Access

### Data Flow

```
mission-control.astro (page)
  ├── imports components (10)
  ├── calls mission-control.js (data layer) on build
  │     ├── getStageStatus() — infers from filesystem
  │     ├── getProductionMetrics() — counts files/dirs
  │     ├── getRecentActivity() — git log
  │     ├── getReports() — dir listings
  │     ├── getRepoStatus() — git info
  │     └── getQuickLinks() — link list with existence checks
  └── client-side JS subscribes to pipelineStore
        ├── PipelineConsole — live event log
        ├── PipelineProgress — stage progress bars
        ├── PipelineSummary — elapsed timer + status
        ├── ResultsPanel — run results
        ├── PipelineHealth — status indicator
        └── RunPipeline — triggers simulatePipeline()
```

### Two Execution Modes
1. **Static (server-side):** The data layer (`mission-control.js`) reads the filesystem at build time to populate metrics, stage status, git info, and link checks. This data is written into the static HTML.
2. **Interactive (client-side):** The `pipelineStore` (pipeline-runner.js) is a reactive state store that drives the live pipeline simulation UI. Running a pipeline triggers `simulatePipeline()`, which progresses through stages with timed event emissions.

### Pipeline Stages (inferred status logic, not actual execution)

| Stage | Inference Method |
|-------|-----------------|
| Community Intelligence | Checks for agent PROMPT.md + reports in `reports/community-intelligence/` |
| Editorial Intelligence | Checks for reports in `reports/editorial-intelligence/` or dedicated agent |
| Opportunity Brief | Checks ODA + ORA PROMPT.md files + briefs directory |
| Research Factory | Checks `docs/research/` for briefs + `HEAVY-ASSET-LIBRARY.md` |
| Content Production | Checks Editorial Builder PROMPT.md + articles in `src/pages/blog/` or `reviews/` |
| Editorial QA | Checks QA agent PROMPT.md + reports in `reports/editorial-qa/` |
| Publishing | Checks `publishing/publish.cjs` + reports in `reports/publication/` |

---

## 4. Current Capabilities

- **Pipeline simulation:** Topic input with 3 modes (Discover, Produce, Full). Client-side simulation runs through all stages with timed events, updating console log, progress nodes, summary panel, and results in real time.
- **Production metrics dashboard:** Counts opportunities, briefs, articles (reviews/blog/roundups), QA reports, publication reports — all driven by filesystem inspection at build time.
- **Recent activity feed:** Shows last 15 git commits with hash, subject, and relative timestamp.
- **Repository status:** Displays branch, last commit, total commits, sprint, phase, architecture freeze status.
- **Quick access links:** 15 context-aware links to reports, specs, and directories — with "Coming Soon" fallback for missing files.
- **Output location status:** Checks 5 output directories and reports Ready/Waiting status.
- **Stage status inference:** 7 pipeline stages with auto-detected status based on filesystem evidence.
- **Report listings:** Documentation reports, QA reports, Publication reports — with existence checks and "Coming Soon" labels.
- **Health indicator:** Live status bar reflecting pipeline state (Operational/Queued/Starting/Busy/Complete/Error).
- **Elapsed timer:** Real-time running clock during pipeline execution.

---

## 5. Current Limitations

- **Pipeline simulation is not real execution.** The `simulatePipeline()` function runs timed event sequences — it does not invoke actual AI agents, generate real articles, or execute any production work. The results panel shows placeholder paths, not actual artifacts.
- **Stage status inference is heuristic.** The `infer*Status()` functions check for filesystem artifacts (PROMPT.md files, directory listings). This produces approximate status but can be misleading (e.g., a PROMPT.md file existing does not guarantee the stage is operational).
- **`pipeline/state.json` is static.** The `lastRun` field is `null` and the `runs` array is empty. No mechanism updates this file after real pipeline runs.
- **No authentication/access control.** The dashboard is publicly accessible if deployed.
- **No real-time data (beyond simulation).** The metrics, stage status, and activity feed are snapshot data captured at build time. Only the pipeline simulation UI updates in real time client-side.
- **Quick links reference non-existent static paths.** Links point to files like `/ops/opportunity-queue.md` and `/docs/research/index.html` which do not exist as public static routes — the `exists` check in the data layer evaluates against the source filesystem, not the built output.
- **No persistent state.** Refreshing the page resets the pipeline simulation state. Pipeline runs do not persist across sessions.
- **No error recovery in simulation.** The simulation always completes successfully — there is no failure path or error injection.
- **Report links point to unserved paths.** QA and publication report links reference `/reports/editorial-qa/` and `/reports/publication/` which are not part of the Astro build output — these files are in the repo but not served by the static site.

---

## 6. Canonical Implementation

| Layer | Canonical Source | Notes |
|-------|-----------------|-------|
| Page | `src/pages/mission-control.astro` | Single authoritative page |
| Components | `src/components/mission-control/*.astro` | 10 components, all active |
| Data | `src/data/mission-control.js` | Single authoritative data module |
| Runner | `src/scripts/pipeline-runner.js` | Single authoritative runner |
| State | `pipeline/state.json` | Static state reference |
| Pipeline Orchestrator | `pipeline/PROMPT.md` | Agent orchestration prompt |
| CLI Entrypoint | `pipeline/run.sh` | Bash wrapper |

---

## 7. Obsolete or Duplicate Files

**No obsolete or duplicate Mission Control files detected.** There is a single implementation with:
- 1 page file
- 10 component files in `src/components/mission-control/`
- 1 data module
- 1 client-side runner script
- 1 state file
- 1 orchestrator prompt
- 1 CLI script

No competing versions, no deprecated variants, no scattered implementations.

---

## 8. How to Use

### Start
The page is statically built and served as part of the Astro site.

```
astro dev            # local development
astro build          # production build
```

### URL
`http://localhost:4321/mission-control/`

### Capabilities (interactive)
1. Enter a research topic in the text field or click an example chip.
2. Select a pipeline mode: Discover Opportunities, Produce Content, or Full Production Run.
3. Click "Run Pipeline" — the simulation plays through each stage with the console log, progress track, summary panel, and health indicator updating in real time.
4. After completion, the Results panel shows generated artifact placeholders.

---

## 9. Recommendations for Future Cleanup

*Documentation only — no implementation intended.*

1. **Reconcile `pipeline/state.json`** — either add a mechanism that updates `lastRun` and `runs` after real pipeline executions, or remove the file if it is vestigial.
2. **Fix quick link `exists` checks** — the data layer currently checks source filesystem paths. If public static routes are intended, either generate the HTML pages for these files or change the existence check to evaluate against Astro's build output.
3. **Remove or rebuild report link paths** — QA and publication reports are tracked at `reports/editorial-qa/` and `reports/publication/` but are not served by the static site. Either make them build artifacts or remove the broken link references.
4. **Add failure paths to simulation** — the current `simulatePipeline()` always completes successfully. Adding random failure injection or configurable failure modes would make the dashboard more representative.
5. **Add persistent state** — if dashboard state should survive page reload, the pipelineStore could serialize to `sessionStorage` or `localStorage`.
6. **Consider removing `pipeline/state.json` duplication** — the data layer in `mission-control.js` has its own heuristic status inference that does not use `state.json` directly. The `state.json` and the inference functions are two parallel representations of the same concept, which increases maintenance surface.

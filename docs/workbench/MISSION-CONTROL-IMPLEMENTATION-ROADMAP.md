# Mission Control — Implementation Roadmap

**Date:** 2026-07-12  
**Based on audit:** `docs/workbench/MISSION-CONTROL-AUDIT.md`  
**Constraint:** Architecture freeze active — no redesign, no refactoring, no component rewrites.  
**Strategy:** Replace simulation data with real production data incrementally. Every phase produces a user-visible improvement. No phase touches more than 4 files.

---

## Current State Summary

| Layer | What exists | What is real |
|-------|-------------|--------------|
| **Pipeline state** | `pipeline/state.json` — static, `lastRun: null`, `runs: []` | Never updated — represents intent, not execution |
| **Data layer** | `src/data/mission-control.js` — 7 stage-inference functions | Partially real — checks filesystem for prompts and file counts, but does not read `state.json` |
| **Client store** | `src/scripts/pipeline-runner.js` — `simulatePipeline()` with timed fake events | Simulation only |
| **Run trigger** | `RunPipeline.astro` — topic input + mode selector + button | Triggers the simulation |
| **Publishing** | `publishing/publish.cjs` — 496-line Node.js script | Fully real — validates, commits, builds, deploys, writes reports |
| **Pipeline orchestrator** | `pipeline/run.sh` + `pipeline/PROMPT.md` | Real — launches the 5-stage AI pipeline |
| **Agent prompts** | 9 `PROMPT.md` files in `agents/` | Real — human/AI-executable instructions, not code |

**Key insight:** The real pipeline is human-in-the-loop guided by AI prompts. Only the publishing engine (`publish.cjs`) is fully automated. The dashboard's simulation layer lives entirely in the browser — the real pipeline lives in files, prompts, and manual execution.

---

## Phase 0 — State Recording (Foundation)

**Goal:** Make `pipeline/state.json` reflect real production activity by recording state after every publish.cjs execution.

**Why first:** Every subsequent phase reads from `state.json`. If it is never updated, the dashboard will always show stale data. This is the smallest possible change that unlocks all downstream improvements.

**Implementation:**

Append a state-update call at the end of the `publish.cjs` main function (before the final `process.exit(0)`):

```js
// After successful publication, update pipeline state
fs.writeFileSync('pipeline/state.json', JSON.stringify({
  pipeline: "OLSP.PROFITANDPRIVILEGE.COM",
  version: "2.0",
  lastRun: new Date().toISOString(),
  stages: { /* unchanged stage readiness */ },
  runs: [
    {
      slug: result.slug,
      title: article.title,
      opportunity: article.id,
      commit: result.commitHash,
      deployed: result.deployUrl || null,
      timestamp: new Date().toISOString(),
      artifacts: {
        article: article.file,
        qaReport: article.qaReport,
        pubReport: result.pubReport,
      },
    },
    ...previousRuns.slice(0, 19), // keep last 20
  ],
}, null, 2));
```

| Dimension | Value |
|-----------|-------|
| **Files affected** | `publishing/publish.cjs` (add ~25 lines at the end of main) |
| **Estimated complexity** | Very low — one block in an existing Node.js script with a well-defined schema |
| **User-visible improvement** | None yet directly, but unlocks Phases 1–3 |

---

## Phase 1 — Real Pipeline Store (Dashboard Reads Real State)

**Goal:** Replace the client-side simulation store with real data from `pipeline/state.json`, so the dashboard displays actual pipeline state instead of simulated state.

**Implementation:**

1. In `src/data/mission-control.js`, add a function that reads `pipeline/state.json` and returns the parsed state (including the `runs` array and `lastRun`). This is already partially implemented as `getPipelineState()` — verify it reads and parses correctly.

2. In `src/scripts/pipeline-runner.js`, add an `initFromState(state)` method to `PipelineStore` that pre-populates the store from the static state:

```js
initFromState(state) {
  if (!state) return;
  this.set({
    status: state.lastRun ? 'completed' : 'idle',
    lastRun: state.lastRun,
    runs: state.runs || [],
    mode: null,
    topic: '',
    currentStage: null,
    events: [],
  });
}
```

3. In `mission-control.astro`, pass the server-rendered `pipeline/state.json` data to the page and have the client-side store initialize from it. Add a small inline script that calls `pipelineStore.initFromState()` with the serialized state.

4. Update `PipelineConsole.astro` to show the **last run's events** (or a message like "No pipeline run recorded yet" if `state.lastRun` is null).

5. Update `PipelineSummary.astro` to show the **last run timestamp and slug** instead of "—".

**Key decision:** The simulation mode (`simulatePipeline()`) is NOT removed yet — it stays available for testing, accessible via a "Demo Mode" toggle. The default view shows real data.

| Dimension | Value |
|-----------|-------|
| **Files affected** | `src/data/mission-control.js` (add getter for parsed state), `src/scripts/pipeline-runner.js` (add `initFromState`), `src/pages/mission-control.astro` (pass state to client), `PipelineConsole.astro` (handle empty/last-run state), `PipelineSummary.astro` (display last run) |
| **Estimated complexity** | Low — ~50 lines total across 5 files; no architectural change |
| **User-visible improvement** | Dashboard shows real last-run timestamp, real slug, real commit hash — instead of simulation placeholders. Console shows "No runs yet" or the last run's recorded events. |

---

## Phase 2 — Pipeline Orchestrator Integration (Run Button Connects to Real Pipeline)

**Goal:** The "Run Pipeline" button stops triggering `simulatePipeline()` and instead guides the operator through the real production workflow.

**Implementation:**

1. In `RunPipeline.astro`, replace the click handler that calls `simulatePipeline()` with a new handler that:
   - Validates topic and mode (same as now)
   - **Copies the selected topic and mode to the clipboard** (or opens the orchestrator prompt directly)
   - Displays a clear call-to-action block showing the exact command to run in the terminal:
     ```
     ./pipeline/run.sh "{topic}"
     ```
   - Also shows the orchestrator prompt location: `pipeline/PROMPT.md`
   - Logs the launch intent to `pipeline/state.json` via a small API call or file write

2. The Run button text changes from "Run Pipeline" to "Start Production Pipeline". After clicking, a "Launch Instructions" panel replaces the validation status — showing the command and a "Copy Command" button.

3. The `RunPipeline` component gets a new `instruction-block` section (below the mode cards) that only appears after clicking the Run button.

**Important:** The simulation is NOT removed. It is demoted to a "Demo Mode" toggle accessible from the PipelineHealth bar. The default mode is "Production" which shows the real orchestrator instructions.

**Why this approach:** The real pipeline is human-in-the-loop (AI prompts executed by an operator). There is no single "run" API call. The dashboard's job is to be the operational launch point — show the operator what to run and track what was run.

| Dimension | Value |
|-----------|-------|
| **Files affected** | `RunPipeline.astro` (replace click handler, add instruction panel — ~30 lines), `PipelineHealth.astro` (add Demo Mode toggle — ~10 lines), `pipeline/state.json` (update launch tracking logic if any) |
| **Estimated complexity** | Low-Medium — mostly UI changes in existing components; no new components or architecture |
| **User-visible improvement** | Clicking "Start Production Pipeline" now shows the actual command to run instead of a fake animation. The operator can copy the command and execute the real pipeline. Demo Mode remains for testing the UI. |

---

## Phase 3 — Pipeline History Panel (Show Real Production Runs)

**Goal:** Display a history of recorded production runs in the dashboard, sourced from `state.json`'s `runs` array.

**Implementation:**

1. In `PipelineProgress.astro` (or as a new content section in `mission-control.astro`), add a **Pipeline History** section after the Results panel.

2. The history shows a table with columns:
   - Timestamp (when the run completed)
   - Slug / Title
   - Commit hash
   - Artifact links (QA report, Publication report)
   - Status (Success / Failed)

3. If no runs exist, show "No production runs recorded yet."

4. Server-side data flow: `mission-control.js` already reads `pipeline/state.json` via `getPipelineState()`. Add `getRunHistory()` that returns the `runs` array. Pass it to the page and render the history table.

| Dimension | Value |
|-----------|-------|
| **Files affected** | `src/data/mission-control.js` (add `getRunHistory()` — ~5 lines), `src/pages/mission-control.astro` (add history section after results — ~30 lines of template), possibly new small component or reuse existing ones |
| **Estimated complexity** | Low — simple data pass-through and table render |
| **User-visible improvement** | Dashboard shows the actual production history — every published article with its reports. Replaces the simulated "Results" panel with real data after a run. |

---

## Phase 4 — Report Viewer Integration (Clickable Artifacts)

**Goal:** Make the report links in Pipeline History and Quick Access actually resolve to viewable content.

**Current problem:** The Quick Access links and Report listings point to paths like `/reports/editorial-qa/` and `/reports/publication/` that are not served by the static site. The `exists` check in the data layer checks the source filesystem, not the build output.

**Implementation:**

Option A (recommended — smallest change): In `astro.config.mjs`, add a static redirect or copy rule that makes `reports/` content available at build time. Astro can copy static assets via the `public/` directory or via `viteStaticCopy`.

Option B: Change the `exists` check in `mission-control.js` to build aware — but this adds complexity.

Option C: Script that copies the latest reports to `public/reports/` before every build.

| Dimension | Value |
|-----------|-------|
| **Files affected** | `astro.config.mjs` (add a copy rule — ~5 lines) OR a small build script |
| **Estimated complexity** | Low — one config change |
| **User-visible improvement** | Report and Quick Access links now resolve to actual content instead of 404s |

---

## Phase 5 — Deprecate Simulation (Cleanup)

**Goal:** Remove the simulation code once the real pipeline is fully operational and tested.

**When:** Only after at least 3 real production runs have been executed through the Phase 2 integration and verified end-to-end.

**Implementation:**

1. Remove `simulatePipeline()` and `MODE_STAGES` / `EVENT_TEMPLATES` from `pipeline-runner.js`
2. Remove the "Demo Mode" toggle
3. Remove the `initFromState` store initialization for simulation (keep the real one)
4. Rename `pipeline-runner.js` to `pipeline-state.js` to reflect its actual purpose

| Dimension | Value |
|-----------|-------|
| **Files affected** | `src/scripts/pipeline-runner.js` (remove ~200 lines), `PipelineConsole.astro`, `PipelineProgress.astro`, `PipelineSummary.astro`, `RunPipeline.astro` (remove demo-related code) |
| **Estimated complexity** | Medium — straightforward deletion, but affects 5 files |
| **User-visible improvement** | No simulation artifacts in UI. Everything in the dashboard is real production data. |

---

## Recommended Order

```
Phase 0 ──→ Phase 1 ──→ Phase 2 ──→ Phase 3 ──→ Phase 4 ──→ Phase 5
(record)    (read)      (trigger)   (history)   (resolve)   (cleanup)
```

Each phase is independent and production-safe. Phases 0–4 can be deployed individually. Phase 5 should wait until at least 3 real runs confirm the new pipeline works end-to-end.

---

## Files That Never Change

Per architecture freeze, the following are never modified:

- `src/components/olsp-standard/OlspLayout.astro`
- `src/components/olsp-standard/` (any shared component)
- `src/pages/reviews/olsp-mineeme.astro`
- `src/pages/reviews/seo-writing-ai-review.astro`
- Any validated reference article

---

## Risk Assessment

| Risk | Phase | Mitigation |
|------|-------|------------|
| `publish.cjs` modification introduces regression | 0 | Add state writing in a single try/catch block after the exit; failure to write state does not block publication |
| Client store loads stale `state.json` | 1 | The store always reads the fresh file at build time — Astro rebuilds pick up latest state. For live updates, add a 30s polling interval. |
| "Run Pipeline" changes confuse operators | 2 | Keep the existing validation flow (topic, mode) intact; only change the click behavior. Label clearly: "Production Mode" vs "Demo Mode." |
| Report links remain broken | 4 | Separate phase, non-blocking for earlier phases |

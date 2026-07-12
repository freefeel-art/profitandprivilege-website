# Implementation Gap Report

**Date:** 2026-07-12
**Objective:** Prove or disprove every engineering conclusion using repository evidence

---

## Summary Table

| # | Problem | Evidence File | Impact | Smallest Fix |
|---|---------|--------------|--------|-------------|
| 1 | Pipeline orchestrator never executed | `pipeline/state.json` | Pipeline never runs | Add state persistence to run.sh |
| 2 | Editorial Builder not connected to briefs | `agents/editorial-builder/PROMPT.md` | No automated article generation | Add input contract to Builder |
| 3 | Produce button runs simulation | `src/scripts/pipeline-runner.js` | UI shows fake progress | Connect to real pipeline |
| 4 | Pipeline state never persisted | `pipeline/state.json` | No run history | Add filesystem write to PipelineStore |
| 5 | Python output never becomes articles | `research/content_production/producer.py` | 42 articles not auto-generated | Bridge Python output to Editorial Builder |

---

## Finding 1: Pipeline Orchestrator Has Never Executed

### Problem
The pipeline orchestrator (`pipeline/run.sh`) has never been successfully executed. `pipeline/state.json` shows `lastRun: null` and `runs: []`.

### Evidence

**File:** `pipeline/state.json`
```json
{
  "lastRun": null,
  "stages": {
    "0-discovery": { "status": "ready" },
    "1-research": { "status": "ready" },
    "2-builder": { "status": "ready" },
    "3-qa": { "status": "ready" },
    "4-publish": { "status": "ready" }
  },
  "runs": []
}
```

**File:** `pipeline/run.sh` — The script exists (48 lines) and depends on `opencode run`, but:
- `pipeline/state.json` has never been modified by the pipeline (git log shows only 2 commits: creation and reset)
- `.bash_history` has zero matches for `pipeline`, `run.sh`, or `orchestrat`
- No temp files exist in `/tmp/pipeline-*`
- The "demo" in commit `45e7040` was hand-authored data committed alongside code, not execution output

**File:** `src/components/mission-control/RunPipeline.astro` line 246 — The UI constructs `./pipeline/run.sh "${topic}"` as a **display string only**, never executes it.

### Expected Behaviour
`pipeline/run.sh "topic"` should execute all 5 stages, update `state.json` after each stage, and produce artifacts.

### Actual Behaviour
The script has never been invoked. `state.json` remains at initial seed state.

### Root Cause
The orchestrator was implemented as a thin `opencode run` wrapper (commit `157928b`) that replaced the original 470-line implementation. The original had stage execution logic; the replacement delegates everything to an AI agent prompt. No evidence of successful execution exists.

### Smallest Fix
Add state persistence to `pipeline/run.sh`: update `state.json` before and after each stage execution. Add a `--dry-run` flag for testing.

---

## Finding 2: Editorial Builder Not Connected to Research Briefs

### Problem
The Editorial Builder has no input contract. It does not know where briefs are or how to consume them.

### Evidence

**File:** `agents/editorial-builder/PROMPT.md` lines 42-46 — The "Before Generating" section lists 5 things to read:
```
1. Read docs/GOLD-MASTER-SPEC.md
2. Read docs/BLOG-MASTER-SPEC.md
3. Read agents/editorial-builder/SPEC.md
4. Read agents/editorial-builder/OUTPUT-TEMPLATE.md
5. Read docs/CONTENT-REGISTRY.md
```
**Zero mentions of briefs, research, Stage 1, or handoff.**

**File:** `agents/editorial-builder/SPEC.md` — Contains output format, component inventory, CSS/JS rules. **No "Inputs" section exists.** The builder does not declare what it consumes.

**File:** `pipeline/PROMPT.md` lines 54-59 — The orchestrator instructs:
```
Stage 2 — Editorial Builder
1. From Stage 1's handoff, get the brief path and seed keyword.
2. Read agents/editorial-builder/PROMPT.md — execute its workflow.
```
This is a text instruction for an AI agent, not executable code.

**File:** `agents/opportunity-research-agent/briefs/` — 21 brief files exist. They are real artifacts produced by individual agent runs, not by the pipeline orchestrator.

**File:** `agents/opportunity-research-agent/PROMPT.md` lines 528-535 — The ORA's handoff block template includes:
```
### Suggested Command / Prompt
Invoke the Editorial Builder with:
    Brief path: agents/opportunity-research-agent/briefs/[slug].md
    Seed keyword: [primary keyword]
```
This instruction exists in the ORA prompt but is never consumed by any code.

### Expected Behaviour
Stage 1 (Research) produces a brief → Stage 2 (Builder) reads that brief → generates an .astro article.

### Actual Behaviour
Briefs exist on disk. The Builder prompt does not reference them. No code connects Stage 1 output to Stage 2 input. The connection exists only as text instructions in `pipeline/PROMPT.md`.

### Root Cause
The Editorial Builder was designed as a standalone agent that receives its topic in the prompt, not as a pipeline stage that consumes upstream artifacts. The pipeline orchestrator prompt was written to chain them, but no code implements the chaining.

### Smallest Fix
Add an "Inputs" section to `agents/editorial-builder/PROMPT.md` that declares: "Read the brief at `[path]` and generate an article based on its content."

---

## Finding 3: Mission Control Produce Button Runs a Simulation

### Problem
The "Produce" button in Mission Control calls `simulatePipeline()` which fakes pipeline progress with setTimeout delays and produces no artifacts.

### Evidence

**File:** `src/pages/mission-control.astro` lines 466-475 — The click handler:
```js
simulatePipeline(topic, 'produce').then(() => {
  btn.textContent = 'Done';
  setTimeout(() => {
    btn.textContent = 'Produce';
    btn.disabled = false;
  }, 3000);
});
```

**File:** `src/scripts/pipeline-runner.js` line 257 — The function is literally named `simulatePipeline`.

**File:** `src/scripts/pipeline-runner.js` lines 196-201 — The delay mechanism:
```js
function delay(ms) {
  return new Promise(r => {
    const t = setTimeout(r, ms);
    pipelineStore.timers.push(t);
  });
}
```

**File:** `src/scripts/pipeline-runner.js` line 286 — Random timing for "realism":
```js
await delay(800 + Math.random() * 600);
```

**File:** `src/scripts/pipeline-runner.js` lines 301-319 — Fabricated results:
```js
const slug = topic.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const results = {
  article: { title: topic, slug, url: `/blog/${slug}/`, source: `src/pages/blog/${slug}.astro` },
  // ...
};
```
Results are derived from slug string interpolation. No files are created.

**File:** `src/scripts/pipeline-runner.js` — Grep for filesystem operations:
- `writeFile`: 0 matches
- `fs.`: 0 matches
- `exec`: 0 matches
- `createWriteStream`: 0 matches

### Expected Behaviour
Clicking "Produce" should trigger a real pipeline run that generates an actual article.

### Actual Behaviour
Clicking "Produce" runs a 3-second animation with fake log messages and fabricated URLs. No files are produced.

### Root Cause
`simulatePipeline()` is a UI-only simulation implemented as a browser-side function. It updates an in-memory state store (`PipelineStore`) with fake events and results. No server-side execution, no file I/O, no agent invocation.

### Smallest Fix
Replace the client-side simulation with a server-side pipeline trigger. The minimum change: add a `<form>` or `<script>` that POSTs to an API endpoint or triggers `pipeline/run.sh` via a server-side hook.

---

## Finding 4: Pipeline State Is Never Persisted

### Problem
`pipeline/state.json` is a static seed file that has never been updated by any code. The in-memory `PipelineStore` has no filesystem persistence.

### Evidence

**File:** `pipeline/state.json` — Content is static seed:
```json
{ "lastRun": null, "runs": [] }
```
Git log shows exactly 2 commits: creation (`45e7040`) and reset (`157928b`). Zero modifications since July 7.

**File:** `src/scripts/pipeline-runner.js` lines 114-192 — `PipelineStore` class:
```js
class PipelineStore {
  constructor() {
    this.state = createInitialState();
    this.subs = new Set();
  }
  set(partial) {
    this.state = { ...this.state, ...partial };
    this.notify();
  }
  // ...
}
```
No `fs` import, no `writeFile`, no `localStorage`, no `sessionStorage`. Pure in-memory pub/sub.

**File:** `src/data/mission-control.js` lines 37-45 — The only reader:
```js
export function getPipelineState() {
  const raw = readFile('pipeline/state.json');
  // ...
}
```
Reads at Astro build time only. Stage status is then overridden by filesystem heuristics (lines 72-127).

**File:** `pipeline/run.sh` — Zero references to `state.json`. The script reads `PROMPT.md` and passes it to `opencode run`.

**File:** `publishing/publish.cjs` — The only `writeFileSync` (line 171) writes publication reports, not state.

### Expected Behaviour
After each pipeline stage completes, `state.json` should be updated with the new stage status, timestamp, and artifact paths.

### Actual Behaviour
`state.json` has `lastRun: null` and `runs: []`. No code writes to it. The dashboard infers status from filesystem presence.

### Root Cause
The `PipelineStore` was implemented as a browser-side singleton for UI reactivity. The pipeline orchestrator was designed to run via `opencode run` (AI agent conversation), which has no filesystem write capability for `state.json`. The state persistence layer was never implemented.

### Smallest Fix
Add a `persist()` method to `PipelineStore` that writes to `pipeline/state.json` via a server-side API endpoint. Alternatively, have `pipeline/run.sh` update `state.json` via `jq` after each stage.

---

## Finding 5: Python Research Output Never Becomes Articles

### Problem
The Python research pipeline produces structured JSON metadata (outlines, briefs, research packages) but no article text. The gap between "publishing package" and "published .astro article" has no implementation.

### Evidence

**File:** `research/content_production/producer.py` line 7:
```python
# Only generates structured content data — presentation (HTML, Astro) remains outside this stage.
```
The content production stage explicitly states it does NOT produce article text.

**File:** `research/output/publishing-packages/affiliate_marketing-publishing-package.json` — Contains:
- `working_title`, `format`, `article_slug`, `gold_master_template` (reference to docs file)
- `sections`: array of `{section_id, heading, word_count_estimate}`
- `qa_status`: "PASSED"
- **No article body, no HTML, no Astro markup, no prose**

**File:** `research/content_production/producer.py` — The output is a JSON file with section outlines:
```python
# Produces structured content data, not article text
```

**File:** `agents/editorial-builder/PROMPT.md` — The Editorial Builder reads Gold Master specs but has no "Inputs" section. It does not consume Python pipeline output.

**File:** `pipeline/PROMPT.md` — The orchestrator defines 5 stages using agent prompts, not Python scripts. The Python pipeline and the orchestrator pipeline are completely separate systems.

### Trace

```
Research (Python)                    Editorial Builder (AI Agent)
  ↓                                    ↓
  research/output/research-reports/     agents/editorial-builder/PROMPT.md
  ↓                                    ↓
  research/output/content/             reads Gold Master specs
  ↓                                    ↓
  {pillar}-content.json                 generates .astro file
  (section outlines, no prose)          ↓
  ↓                                    src/pages/blog/{slug}.astro
  research/output/publishing-packages/  (actual article)
  ↓                                    
  {pillar}-publishing-package.json      
  (metadata, no article text)          
  ↓                                    
  ??? ← GAP HERE                      
  ↓                                    
  (nothing)                            
```

**The gap is between `research/output/publishing-packages/` and `src/pages/blog/`.** The Python pipeline produces structural metadata. The Editorial Builder produces article text. No code reads the metadata and invokes the builder.

### Expected Behaviour
Python pipeline produces a publishing package → Code reads the package → Invokes Editorial Builder with the metadata → Builder generates .astro article → Article is written to `src/pages/`.

### Actual Behaviour
Python pipeline produces a publishing package. Nothing reads it. The 42+ existing articles were created through manual/assisted AI sessions.

### Root Cause
The Python pipeline and the Editorial Builder are independent systems designed at different times. The Python pipeline was built to produce structured data for human review. The Editorial Builder was built as a standalone agent. No integration layer was implemented.

### Smallest Fix
Write a bridge script that:
1. Reads `research/output/publishing-packages/{pillar}-publishing-package.json`
2. Extracts `working_title`, `article_slug`, `sections`
3. Constructs a prompt for the Editorial Builder with this metadata
4. Invokes the builder (via `opencode run` or similar)
5. Writes the output .astro file to `src/pages/blog/{slug}.astro`

---

## Complete Implementation Trace

### Current Flow (Broken)

```
[Manual] User creates topic
    ↓
[Manual] ODA generates OPPORTUNITY-QUEUE.md (20 candidates)
    ↓
[Manual] ORA generates briefs (21 files)
    ↓
[MISSING] No code reads briefs
    ↓
[MISSING] No code invokes Editorial Builder
    ↓
[MISSING] No code generates .astro article
    ↓
[MISSING] No code runs QA
    ↓
[Manual] User runs publish.cjs
    ↓
[Real] Article deployed via git push
```

### Required Flow (Target)

```
[Automated] Pipeline receives seed keyword
    ↓
[Stage 0] ODA generates OPPORTUNITY-QUEUE.md
    ↓
[Stage 1] ORA generates brief
    ↓
[Stage 2] Editorial Builder reads brief → generates .astro
    ↓
[Stage 3] Editorial QA validates article
    ↓
[Stage 4] Publisher deploys via git push
    ↓
[State] state.json updated after each stage
```

### Exact Gaps

| Gap | From | To | Missing |
|-----|------|----|---------|
| Gap A | `pipeline/run.sh` | `pipeline/state.json` | State persistence after each stage |
| Gap B | `pipeline/PROMPT.md` | `agents/editorial-builder/PROMPT.md` | Brief-to-builder input contract |
| Gap C | `mission-control.astro` | `pipeline/run.sh` | Real pipeline trigger (not simulation) |
| Gap D | `pipeline-runner.js` `PipelineStore` | `pipeline/state.json` | Filesystem persistence layer |
| Gap E | `research/output/publishing-packages/` | `agents/editorial-builder/` | Python-to-Astro bridge script |
| Gap F | `publish.cjs` | `pipeline/state.json` | Post-publish state update |
| Gap G | `pipeline/PROMPT.md` | `pipeline/run.sh` | Stage-to-stage artifact passing |

### Smallest Set of Changes to Achieve End-to-End Production

1. **Add state persistence** to `pipeline/run.sh` — write to `state.json` after each stage (5 lines of `jq` per stage)
2. **Add input contract** to `agents/editorial-builder/PROMPT.md` — document brief path as required input (3 lines)
3. **Write bridge script** — read publishing package JSON, invoke Editorial Builder, write .astro file (50-100 lines)
4. **Connect Mission Control** — replace `simulatePipeline()` with real pipeline trigger (20-30 lines)
5. **Add state persistence to PipelineStore** — write to `state.json` via server endpoint (10-15 lines)

**Estimated total: ~100-150 lines of new code across 3-4 files.**

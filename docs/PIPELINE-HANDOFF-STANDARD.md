# Pipeline Handoff Standard

**Status:** Permanent pipeline UX standard  
**Applies to:** All pipeline stages — Discovery, Research, Writer, QA, Publish, and any future stage  
**Effective:** 2026-07-04

---

## 1. Purpose

Every pipeline stage must end with a standard handoff block. The user should never have to ask "what do I do next?" — the handoff block always answers that question explicitly.

A stage is not complete until the handoff block is written.

---

## 2. Handoff Block Template

```
## Stage Handoff

**Stage Status:** [Complete / In Progress / Blocked]

### Completed Items
- [item 1]
- [item 2]

### Produced Artifact(s)
| Artifact | Path |
|----------|------|
| [type] | `path/to/file` |

### Current Pipeline Position
[Stage name] → [Next stage name]

### Recommended Next Stage
[Stage name]

### Suggested Command / Prompt
[Exact prompt or command to invoke the next stage, with all required parameters filled in]
```

---

## 3. Field Definitions

| Field | Requirement | Rules |
|-------|-------------|-------|
| **Stage Status** | Always required | One of: `Complete` (all work finished), `In Progress` (partial progress, paused intentionally), `Blocked` (cannot proceed — blocker must be stated below) |
| **Completed Items** | Always required | Bullet list of what was actually done. Use past tense. Be specific — "Researched pricing for 6 tiers" not "Did pricing research." |
| **Produced Artifact(s)** | Always required | Table with Artifact name and file path. If no file was created (e.g. a failed check that produced no artifact), state `None — [reason]` |
| **Current Pipeline Position** | Always required | `[Completed stage] → [Next stage]`. Shows both where we are and where we are going in one line |
| **Recommended Next Stage** | Always required | The single next action. Never list multiple options — the pipeline must guide, not present a menu |
| **Suggested Command / Prompt** | Always required | A verbatim prompt or shell command that the user can copy and run to invoke the next stage. Fill in all parameters the next stage needs — do not leave blanks for the user to guess |

---

## 4. Stage-Specific Handoff Conventions

### 4.1 Discovery

| Field | Convention |
|-------|------------|
| **Stage Status** | `Complete` when queue is updated and summary reported |
| **Completed Items** | List seeds explored, candidates surfaced vs dropped vs queued |
| **Produced Artifact(s)** | Always includes `OPPORTUNITY-QUEUE.md` |
| **Current Pipeline Position** | `Discovery → Research` |
| **Recommended Next Stage** | `Promote candidate to Research` — or specify which queue row to promote |
| **Suggested Command / Prompt** | ORA's user prompt template with the chosen `candidate_keyword` filled in, plus `intent_hint` and `pipeline_type` context |

### 4.2 Research

| Field | Convention |
|-------|------------|
| **Stage Status** | `Complete` when brief is saved and registered |
| **Completed Items** | List stages executed, sources used, key findings |
| **Produced Artifact(s)** | Always includes the brief path (and Heavy Asset Library entry if Heavy pipeline) |
| **Current Pipeline Position** | `Research → Writer` |
| **Recommended Next Stage** | `Write article from brief` |
| **Suggested Command / Prompt** | The Writer prompt template with the brief path, research confidence, and any critical caveats pre-filled |

### 4.3 Writer

| Field | Convention |
|-------|------------|
| **Stage Status** | `Complete` when `.astro` file is written and first draft is done |
| **Completed Items** | List sections written, key content decisions |
| **Produced Artifact(s)** | Always includes the `.astro` file path |
| **Current Pipeline Position** | `Writer → QA` |
| **Recommended Next Stage** | `QA the article` |
| **Suggested Command / Prompt** | QA checklist or instruction, including any known risk areas (e.g. "verify scores match spec," "check affiliate disclosure compliance") |

### 4.4 QA

| Field | Convention |
|-------|------------|
| **Stage Status** | `Complete` when all checks pass; `Blocked` if an issue is found and cannot be auto-fixed |
| **Completed Items** | List checks performed and results (e.g. "CSS tokens match spec — pass", "Build clean — pass", "HTTP 200 — pass") |
| **Produced Artifact(s)** | Only produced if issues were found and fixed — list changed files. If no issues, `None — all checks passed` |
| **Current Pipeline Position** | `QA → Publish` |
| **Recommended Next Stage** | `Publish article` |
| **Suggested Command / Prompt** | The exact git commands to commit and push, with commit message pre-written |

### 4.5 Publish

| Field | Convention |
|-------|------------|
| **Stage Status** | `Complete` when commit is pushed and page is live |
| **Completed Items** | Commit SHA, deployment confirmation |
| **Produced Artifact(s)** | None — deployment produces no new file |
| **Current Pipeline Position** | `Publish → Done` |
| **Recommended Next Stage** | `Register in Content Registry` (if not already done) or `Start next article` |
| **Suggested Command / Prompt** | Registry update instructions or the next Discovery/Research prompt |

---

## 5. Rules

1. **The handoff block is part of the stage output.** It is not optional. It is the last thing written before reporting completion.

2. **The Suggested Command / Prompt must be copy-paste ready.** Fill in every parameter. The user should be able to copy the block and run it without editing. If the next stage needs a keyword, write the keyword. If it needs a file path, write the path. Never leave `[placeholder]` or `TODO` in this field.

3. **Never present options.** The handoff block recommends exactly one next stage with exactly one command/prompt. If the user wants alternatives, they will ask. The pipeline's job is to guide, not to offer a menu.

4. **Blocking is explicit.** If a stage cannot complete, Stage Status is `Blocked` and the Completed Items list includes the blocker. The handoff block still recommends a next stage — it recommends the corrective action rather than the normal successor.

5. **The handoff block is machine-readable by design.** The template is consistent enough that a future automation layer could parse Stage Status, artifact paths, and the next command from any handoff block without special-casing per stage.

6. **All artifacts are referenced by absolute or workspace-relative path.** Never say "the brief" — say `docs/research/fastbots-ai-research.md`.

7. **The handoff block does not repeat the article content.** It summarises what was produced and points to what should happen next. The produced artifacts contain the detail.

---

## 6. Example — Complete Handoff Block

```
## Stage Handoff

**Stage Status:** Complete

### Completed Items
- Researched FastBots.ai pricing (6 tiers, verified from PDF snapshot)
- Documented 12+ supported LLMs across 3 providers
- Identified 15 open questions requiring hands-on testing
- Catalogued 11 independent and vendor sources
- All 18 brief sections populated and frozen

### Produced Artifact(s)
| Artifact | Path |
|----------|------|
| Research Brief v1.1 | `docs/research/fastbots-ai-research.md` |

### Current Pipeline Position
Research → Writer

### Recommended Next Stage
Write article from Research Brief

### Suggested Command / Prompt
Write the review article for FastBots.ai to `src/pages/reviews/fastbots-ai-review.astro`
using the Gold Master template at `src/pages/reviews/olsp-academy.astro`.
Research Brief: `docs/research/fastbots-ai-research.md`.
Affiliate URL: `https://fastbots.ai/?via=jarmo`.
Research is documentation-based — no hands-on testing was performed.
15 open questions remain — state these transparently in the article rather than speculating.
```

---

## 7. Compatibility With Existing Pipeline Docs

This standard supplements, not replaces, the existing architecture:

| Document | Relationship |
|----------|--------------|
| `docs/PIPELINE-ARCHITECTURE.md` | Defines *which* stages exist and *how* they connect. This document defines *how each stage ends*. |
| `agents/opportunity-discovery-agent/SPEC.md` | Defines Discovery's internal workflow. This standard defines Discovery's output handoff format. |
| `agents/opportunity-research-agent/SPEC.md` | Defines Research's internal workflow. This standard defines Research's output handoff format. |
| `agents/research-compiler/SPEC.md` | Defines Heavy Research's internal workflow. This standard defines its output handoff format. |
| This document | Defines the handoff block that every stage append to its output. |

No existing SPEC.md or PROMPT.md file changes. The handoff block is appended to the stage's output, not embedded in its specification.

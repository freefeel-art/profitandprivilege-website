# Pipeline Orchestrator — Design Review

**Date:** 2026-07-12
**Status:** Design complete — not yet implemented

---

## How the Pipeline Orchestrator Fits Into the AI Editorial Operating System

The AI Editorial Operating System currently consists of six agents connected by documented handoff contracts:

```
ODA ──► ORA ──► Editorial Builder ──► Editorial QA ──► Publisher
 │         │
 │         └── (Light pipeline: general topics)
 │
 └──► Research Compiler ──► Editorial Builder ──► Editorial QA ──► Publisher
       (Heavy pipeline: products, companies, tools)
```

Each agent is independently functional. ODA discovers and scores candidates. ORA researches Light opportunities. Research Compiler creates reusable Knowledge Assets. Editorial Builder produces .astro files. Editorial QA validates. Publisher deploys.

What does not exist today is a **coordinator** — something that:

1. Reads a candidate from the queue
2. Decides which pipeline to run
3. Invokes each stage in sequence
4. Validates that each handoff succeeded
5. Decides whether to continue or stop
6. Records the run

The Pipeline Orchestrator fills that gap. It wraps the existing agents without modifying them. It is not another editorial stage — it is the **orchestration layer** that connects the stages the system already has.

### Position in the architecture

```
                    ┌──────────────────────────────────────┐
                    │         Pipeline Orchestrator               │
                    │  (orchestration — no content created) │
                    └──┬──────┬───────┬──────┬──────┬───────┘
                       │      │       │      │      │
                 ┌─────▼──┐ ┌─▼────┐ ┌▼─────┐ ┌▼───┐ ┌▼────┐
                 │  ODA   │ │ ORA  │ │  RC  │ │ EB  │ │ QA  │
                 │(queue) │ │(brief│ │(asset│ │(.astro││(check│
                 │        │ │ only)│ │ only)│ │ only)│ │ only)│
                 └────────┘ └──────┘ └──────┘ └─────┘ └─────┘
```

The Pipeline Orchestrator sits **above** the existing agents, not among them. It reads their inputs, invokes them, reads their handoff blocks, and decides the next action. It does not share their stage numbering — it is stage 0, the meta-stage.

---

## Why the Pipeline Orchestrator Becomes the Single Orchestration Point

### Problem 1: No single place to answer "what runs next?"

Today, the operator manually:
- Reads an OPPORTUNITY-QUEUE.md row
- Copies the keyword into an ORA prompt
- Reads the resulting brief
- Decides what article type to write
- Copies brief content into an Editorial Builder prompt
- Runs astro build manually
- Starts a dev server manually
- Checks HTTP 200 manually
- Decides whether to commit

Each of these decisions is implicit — held in the operator's head, not recorded anywhere reusable. The Pipeline Orchestrator makes every decision explicit and recordable.

### Problem 2: No contract enforcement between stages

The Pipeline Integration MVP (docs/workbench/pipeline-integration-mvp.md) found that the Editorial Builder has no input contract. The Research Brief has no next-stage handoff section. These gaps exist because no actor today checks whether stage N's output contains what stage N+1 needs.

The Pipeline Orchestrator's **Contract Registry** (SPEC.md § 7) formalizes these checks. Before invoking any stage, it verifies that every required input field is present. After the stage completes, it verifies that every required output field is present and valid. This makes contract gaps visible at design time, not discoverable at runtime.

### Problem 3: Pipeline state is invisible

When a pipeline run spans multiple invocations (ORA one day, Editorial Builder the next), the operator has to remember:
- Which candidate is being progressed
- Which stages have completed
- Which artifacts exist
- What decisions were made

The Pipeline Orchestrator's **Run Record** (OUTPUT-TEMPLATE.md) documents every stage execution, every handoff validation, every retry, and every operator intervention. State lives in a file, not in the operator's head.

### Problem 4: No consistent retry or failure handling

Today, a failed `astro build` means the operator debugs and re-runs manually. A failed ORA run means the operator decides whether to retry or abandon. There is no consistent policy for:
- How many retries a stage gets
- What triggers a retry vs a block
- What information is preserved when a pipeline blocks

The Pipeline Orchestrator's **Failure Handling** (SPEC.md § 10) defines a uniform retry policy across all stages. A failed build retries up to 2 times. A blocked handoff stops immediately. A DO NOT WRITE decision stops without invoking downstream stages. Every failure state is recorded in the run log.

### Problem 5: Pipeline completion is not recorded

When an article is finally published, nothing today updates the Opportunity Queue to mark the candidate as `published`. The queue becomes stale — showing `unclaimed` candidates that have already been produced. The Pipeline Orchestrator updates the queue row on every final disposition, keeping the queue accurate.

---

## Why No Existing Agent Responsibilities Change

### Design principle: orchestration without intrusion

The Pipeline Orchestrator is designed as a **reader and invoker**, never a **modifier** of other agents. It reads their:
- SPEC.md (to understand their input contracts)
- OUTPUT-TEMPLATE.md (to understand their output contracts)
- Handoff blocks (to determine Stage Status)

It does not modify any of these files. It does not rewrite agent behaviour. It does not insert itself into the agent's workflow.

### Each agent's scope is preserved unchanged

| Agent | Responsibility today | Pipeline Orchestrator's interaction |
|---|---|---|
| **ODA** | Discovers candidates, scores them, populates queue | Reads queue rows. Updates Status field on completion. Never invokes ODA — it's an independent exploration tool. |
| **ORA** | Researches a keyword, produces Opportunity Brief | Invokes ORA with keyword. Reads the brief's `editorial_decision` field. Reads the brief's Section 8 fields for next stage. |
| **Research Compiler** | Researches a Heavy subject, produces Research Brief + Heavy Asset Library entry | Invokes RC with subject + subject_type. Checks HEAVY-ASSET-LIBRARY.md for duplicates first. Validates both output files exist. |
| **Editorial Builder** | Produces self-contained .astro file | Invokes EB with brief path + article type. Runs astro build + HTTP 200 check on output. Never modifies the .astro file. |
| **Editorial QA** | Validates .astro file (future) | Invokes QA with .astro path. Reads QA report. Blocks if failed. |
| **Publisher** | Commits and deploys (future) | Invokes Publisher with .astro path + commit message. Confirms deployment. |

### No behavioural change required

The Pipeline Orchestrator does not require any agent to:
- Change what it produces
- Change how it produces it
- Change its input format
- Add new capabilities
- Share internal state
- Coordinate with other agents directly

Each agent continues to produce exactly what it produces today. The Pipeline Orchestrator reads the outputs, validates them, and routes them to the next stage. The only new requirement is that every agent includes a **handoff block** in its output (as specified by `docs/PIPELINE-HANDOFF-STANDARD.md`), but this is an existing documented standard that no agent currently implements — not a new constraint introduced by the Pipeline Orchestrator.

### Separation of concerns

The Pipeline Orchestrator enforces a strict separation that exists in the architecture documents but is not enforced in practice today:

| Concern | Owned by |
|---|---|
| *What* to write | Editorial Builder (from the brief) |
| *Whether* to write it | Pipeline Orchestrator (reads `editorial_decision` gate) |
| *When* to write it | Pipeline Orchestrator (pipeline sequencing) |
| *Whether it was written correctly* | Editorial QA (future) + Pipeline Orchestrator (build validation) |
| *Whether it gets deployed* | Publisher (future) + Pipeline Orchestrator (orchestration) |

Today, the operator makes all four decisions simultaneously. The Pipeline Orchestrator separates them into distinct, verifiable checkpoints without requiring any agent to change its behaviour.

---

## Summary

The Pipeline Orchestrator does not redesign the editorial pipeline. It **operationalizes** the design that already exists — making the decisions that are currently implicit (what runs next, did the handoff succeed, should we retry or block, is the pipeline done) explicit, recorded, and repeatable.

| Before Pipeline Orchestrator | After Pipeline Orchestrator |
|---|---|
| Operator reads queue and decides | Pipeline Orchestrator reads queue and routes |
| Operator checks if brief has required fields | Pipeline Orchestrator validates contract |
| Operator decides to retry or abandon | Pipeline Orchestrator applies retry policy |
| Operator remembers pipeline state | Pipeline Orchestrator writes run record |
| Operator leaves queue row unchanged | Pipeline Orchestrator updates queue status |
| No retry budget | Max 2 retries per stage |
| No contract enforcement | Pre/post invoke validation at every handoff |

The Pipeline Orchestrator is the layer that makes the AI Editorial Operating System **automated** rather than **manually operated** — without changing anything about how any individual agent works.

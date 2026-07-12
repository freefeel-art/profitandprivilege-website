# Architecture Finalization Report

**Date:** 2026-07-12
**Sprint:** Architecture Finalization
**Status:** Complete

---

## Objective

Separate the deterministic orchestration layer from the AI agent architecture. The Pipeline Runner was architecturally misclassified as an AI agent (with a PROMPT.md, co-located in `agents/`). The sprint moved its specification to a top-level `orchestration/` directory, removed the PROMPT.md, renamed all references to "Pipeline Orchestrator," and updated all repository documents for consistency.

This sprint followed the architecture review (`docs/workbench/pipeline-orchestrator-architecture-review.md`) which concluded: **The Pipeline Orchestrator is not an AI agent. It is an orchestration contract + deterministic implementation detail.**

---

## Changes Made

### Files created

| Path | Description |
|---|---|
| `orchestration/README.md` | Overview and quick reference — adapted from `agents/pipeline-runner/README.md` with "Pipeline Orchestrator" naming |
| `orchestration/SPEC.md` | Functional specification — adapted from `agents/pipeline-runner/SPEC.md` with "Pipeline Orchestrator" naming |
| `orchestration/OUTPUT-TEMPLATE.md` | Pipeline run record output template — adapted from `agents/pipeline-runner/OUTPUT-TEMPLATE.md` with "Pipeline Orchestrator" naming |
| `docs/workbench/architecture-finalization-report.md` | This report |

### Files relocated (redirect stubs)

The following files remain in `agents/pipeline-runner/` but their content was replaced with redirect stubs pointing to `orchestration/`:

| Path | Content after change |
|---|---|
| `agents/pipeline-runner/README.md` | Redirect stub → `orchestration/README.md` |
| `agents/pipeline-runner/SPEC.md` | Redirect stub → `orchestration/SPEC.md` |
| `agents/pipeline-runner/OUTPUT-TEMPLATE.md` | Redirect stub → `orchestration/OUTPUT-TEMPLATE.md` |

Redirect stubs are retained to prevent broken references from git history, bookmarks, and any unupdated cross-document links.

### Files removed

| Path | Reason |
|---|---|
| `agents/pipeline-runner/PROMPT.md` | Architecturally incorrect — the Pipeline Orchestrator is deterministic, not an LLM agent. All its decisions (field extraction, file checks, exit codes, HTTP status) are binary or procedural. |

### Files renamed

| Old path | New path |
|---|---|
| `docs/workbench/pipeline-runner-architecture-review.md` | `docs/workbench/pipeline-orchestrator-architecture-review.md` |
| `docs/workbench/pipeline-runner-design-review.md` | `docs/workbench/pipeline-orchestrator-design-review.md` |

### Terminology updates

| Old term | New term | Scope |
|---|---|---|
| "Pipeline Runner" (proper name) | "Pipeline Orchestrator" | All `.md` files — 90+ references renamed |
| `agents/pipeline-runner/` (path references) | `orchestration/` | All path references in architecture review docs |

### Architectural decisions

| Decision | Rationale |
|---|---|
| **Pipeline Orchestrator is NOT an AI agent** | Zero decisions require AI reasoning. Every decision is a binary check, field extraction, shell command, or template operation. Wrapping deterministic logic in a "You are..." LLM prompt adds latency, cost, and hallucination risk. |
| **PROMPT.md removed, not replaced** | The SPEC.md already defines the orchestration contract. Execution logic is a separate implementation artifact (script, CLI tool, GitHub Action) that belongs outside the agent directory structure. |
| **Specification documents stay in `orchestration/`** | The contract layer (stage connections, validation checkpoints, contract registry) is valuable architecture documentation. It belongs in the repository — just not in `agents/`. |
| **AI agents unchanged** | ODA, ORA, Research Compiler, Editorial Builder, Editorial QA, Publisher remain LLM-based creative agents. Their directories, prompts, and specs are untouched. |

### Repository consistency verification

| Check | Result |
|---|---|
| `orchestration/` directory exists | ✅ |
| Files inside `orchestration/` | README.md, SPEC.md, OUTPUT-TEMPLATE.md — all three canonical documents present |
| No references to "Pipeline Runner" as a proper name | ✅ — zero matches across all `.md` files |
| No references to `agents/pipeline-runner/` as a path (outside redirect stubs) | ✅ — zero matches across all `.md` files |
| No references to `orchestration/PROMPT.md` | ✅ — zero matches |
| No "Pipeline Runner as AI agent" framing | ✅ — zero matches |
| Redirect stubs resolve correctly | ✅ — all three stubs point to existing `orchestration/` files |
| All documents referenced by `orchestration/README.md` exist | ✅ — `docs/PIPELINE-ARCHITECTURE.md`, `docs/PIPELINE-HANDOFF-STANDARD.md`, all agent SPECs |
| Lowercase "runner" generic references cleaned up | ✅ — 2 instances in SPEC.md and architecture review updated to "orchestrator" |
| Renamed workbench files | ✅ — both `pipeline-orchestrator-architecture-review.md` and `pipeline-orchestrator-design-review.md` exist |

### Remaining future implementation work

The following tasks are outside the scope of this sprint (architecture finalization only — no implementation):

- Implement the Pipeline Orchestrator as a deterministic script or CLI tool
- Create `docs/pipeline-runs/` directory structure for run records
- Integrate the orchestrator with agent invocation mechanisms
- Implement Editorial QA and Publisher stages
- Add handoff blocks to agent OUTPUT-TEMPLATEs per PIPELINE-HANDOFF-STANDARD.md

---

Architecture Finalization Complete

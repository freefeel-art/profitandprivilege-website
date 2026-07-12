# Architecture Review — Pipeline Orchestrator Role

**Date:** 2026-07-12
**Status:** Complete

---

## Question

Is the Pipeline Orchestrator:
- A) an AI agent,
- B) an orchestration contract,
- C) an implementation detail,
- or D) something else?

---

## Evidence

### 1. Every "agent" in this repository produces creative content

All existing agent PROMPT.md files follow the same pattern — a "You are..." system prompt designed for an LLM:

| Agent | PROMPT.md opening line | What it produces | Why an LLM is needed |
|---|---|---|---|
| **Opportunity Research Agent** | "You are the Opportunity Research Agent for Profit and Privilege..." | Evidence-based research brief | Synthesizes search results, trends, and community data into structured analysis — creative synthesis |
| **Research Compiler** | "You are the Research Compiler for Profit and Privilege..." | Deep research brief | Same — research synthesis requires language understanding and evidence evaluation |
| **Editorial Builder** | "You are the Editorial Builder..." | Self-contained .astro article | Writes article prose, structures sections, formats HTML — pure content generation |
| **Opportunity Discovery Agent** | [Not read in full, same pattern established] | Opportunity queue | Generates candidate opportunities from trends and community signals — creative exploration |

Every LLM agent in this system produces **creative output** that requires natural language understanding and generation. That is what the "AI Editorial Operating System" automates — the creative editorial workflow.

### 2. Pipeline Orchestrator decisions are all deterministic

The Pipeline Orchestrator design (the version created in the previous sprint) defines these responsibilities:

| Responsibility | Decision type | Requires LLM? |
|---|---|---|
| Read `pipeline_type` from candidate | Field extraction | No — read a YAML/JSON field |
| Route to Light or Heavy pipeline | If/else branch | No — `if pipeline_type == "Light"` |
| Check if file exists at expected path | File system check | No — `test -f path` |
| Check if required fields are present | String/field presence check | No — grep/parse |
| Run `astro build` and check exit code | Shell command + exit code | No — `$?` |
| Check HTTP 200 | HTTP status code | No — `curl -s -o /dev/null -w "%{http_code}"` |
| Retry or block based on threshold | Counter comparison | No — `if retries < max_retries` |
| Write run record from template | Template filling | No — string substitution |
| Update queue status | String replacement | No — `sed` or equivalent |

**Zero decisions require AI reasoning.** Every decision is a binary check, a field extraction, a shell command, or a template operation.

### 3. The handoff standard explicitly envisions deterministic automation

`docs/PIPELINE-HANDOFF-STANDARD.md` § 5, Rule 5:

> "The handoff block is machine-readable by design. The template is consistent enough that a **future automation layer** could parse Stage Status, artifact paths, and the next command from any handoff block without special-casing per stage."

Key phrase: **"future automation layer"** — not "future AI agent." The standard describes a parser, not a reasoning engine. It envisions something that reads structured fields and acts on them deterministically.

The same document § 5, Rule 2 also states:

> "The Suggested Command / Prompt must be copy-paste ready. Fill in every parameter. The user should be able to copy the block and run it without editing."

The handoff standard is designed so a human can copy the command and run it — or, in the future, so a deterministic automation layer can read the command and execute it. Neither requires an LLM.

### 4. The Architecture Freeze constrains what can change

The consolidation report (`docs/workbench/ARCHITECTURE-CONSOLIDATION-REPORT.md`) states:

> "Preserves the Architecture Freeze. No production code is modified. No spec is rewritten."

ADR-001 (`docs/architecture/ADR-001-EDITORIAL-BUILDER-ARCHITECTURE.md`) further constrains:
- Output format: self-contained `.astro` files
- Zero imports
- No new components

Neither document addresses orchestration — because orchestration does not produce content. The Architecture Freeze applies to the **content production system**, not to the **operational layer** that coordinates it. This means the Pipeline Orchestrator has architectural freedom in how it is implemented — but it must respect that all agents it coordinates are LLM-based and produce deterministic output formats.

### 5. The production system today is a human operator

The consolidation report clearly states:

> "All 30 published pages were produced this way [manual prompt into an LLM]."
> "Pipeline stages 0–2 are documented and could theoretically be run manually. Stages 3–5 are not implemented."

The "automated pipeline" is a **future design**. Today, the orchestrator is a human:
1. Reads the queue
2. Copies a keyword into an ORA prompt
3. Reads the resulting brief
4. Copies brief content into a Builder prompt
5. Runs `astro build`
6. Verifies HTTP 200
7. Commits

The Pipeline Orchestrator's job is to **replace the human as orchestrator** — not by reasoning like a human, but by executing the deterministic steps the human currently follows manually.

### 6. The Pipeline Orchestrator design already reads like an orchestration script

The PROMPT.md I wrote in the previous sprint reads like a procedural script pretending to be an AI prompt. Compare:

- **ORA PROMPT.md** (genuine AI prompt): "You are the Opportunity Research Agent... Investigate this keyword..."
- **Editorial Builder PROMPT.md** (genuine AI prompt): "You are the Editorial Builder... Generate a self-contained .astro file..."
- **Pipeline Orchestrator PROMPT.md** (my design): "Read pipeline_type. If Light, execute Stage 1. Pre-invoke checks: candidate_keyword is non-empty. Post-invoke checks: brief file exists..."

The first two describe **creative tasks** that require an LLM. The third describes **procedural logic** that would be better expressed as code.

---

## Analysis

### Option A: AI agent — REJECTED

The Pipeline Orchestrator should NOT be an AI agent because:

1. **None of its decisions require AI reasoning.** Every decision is a deterministic check — file exists, field is present, exit code is 0, status code is 200. Wrapping deterministic logic in an "You are..." LLM prompt adds latency, cost, and hallucination risk to tasks that need none of those things.

2. **An AI agent would introduce reasoning errors into deterministic tasks.** An LLM might "think" a field exists when it doesn't, interpret a 404 as a "successful empty response," or decide to retry when the contract says block. Deterministic orchestration should be deterministic.

3. **The pattern already exists in this repo.** AGENTS.md describes running `astro build`, `astro dev --background`, and checking HTTP 200 as post-article tasks — all executed as shell commands by the AI agent currently running them (Claude Code). The Pipeline Orchestrator would formalize these checks into a reusable layer.

### Option B: Orchestration contract — PARTIALLY CORRECT

The Pipeline Orchestrator's **specification** (what it defines about how stages connect and what contracts exist between them) IS an orchestration contract. The SPEC.md's Contract Registry, validation checkpoints, and pipeline routing logic define the inter-stage relationships that currently exist only as implicit knowledge.

This contract layer is valuable and should exist — it makes explicit what is currently implicit. But a contract is not an implementation. The contract defines what should happen; something else executes it.

### Option C: Implementation detail — PARTIALLY CORRECT

The Pipeline Orchestrator's **execution** (reading fields, checking files, running builds, recording runs) IS an implementation detail of the pipeline architecture. These are operational tasks that any CI/CD system, CLI tool, or orchestration script could perform.

The implementation detail includes:
- Field extraction from markdown/YAML files
- File existence checks
- Shell command execution (astro build, curl)
- Template filling for run records
- Status updates to queue files

These are not architecture decisions — they are engineering choices about how to execute the orchestration contract.

### Option D: Something else — CORRECT when combined

The Pipeline Orchestrator is **both** an orchestration contract AND an implementation detail:

- **As a contract:** The SPEC.md defines how stages connect, what fields must exist at each handoff, and what constitutes a pass/fail. This is architecture documentation, not code. It belongs in the repository as a specification document.

- **As an implementation:** The actual execution of checks, invocations, and recordings is a deterministic automation layer. This could be:
  - A CLI tool (`pipeline-runner promote --candidate <id>`)
  - A set of npm scripts or Makefile targets
  - A GitHub Actions workflow
  - An orchestration script in Python, Bash, or Node.js
  - Embedded in an existing tool (Claude Code already runs `astro build` and `curl` in AGENTS.md)

The key insight: **the implementation detail does not need its own agent directory with a PROMPT.md.** It needs:
- A SPEC or README defining the orchestration contract (already designed)
- A script or tool that executes the contract (not yet designed)

---

## What the Pipeline Orchestrator IS, specifically

```
Pipeline Orchestrator = Orchestration Contract + Orchestration Executor
                        ↑                           ↑
                    SPEC.md                      CLI tool / script
                    README.md                    GitHub Actions / Makefile
                    (defines what                 (executes the checks
                     connects, what                and stage invocations
                     the contracts                 deterministically)
                     are, and what
                     validates)
```

### The contract layer (already designed in previous sprint)

This layer is correct as designed:
- `orchestration/SPEC.md` — defines stage connections, contract registry, validation checkpoints, failure handling
- `orchestration/README.md` — overview
- `orchestration/OUTPUT-TEMPLATE.md` — run record format

### The execution layer (needs redesign)

This layer should NOT be a PROMPT.md. It should be replaced with:
- `orchestration/run.sh` or `orchestration/pipeline-runner.mjs` — a deterministic script
- Or incorporated into the project's tooling (Makefile, npm scripts)
- Or implemented as a GitHub Actions workflow

### What needs to change

| File | Current state | Recommendation |
|---|---|---|
| `orchestration/README.md` | Exists — correct as overview | **Keep** |
| `orchestration/SPEC.md` | Exists — defines orchestration contract | **Keep** (the most valuable file) |
| ~~`agents/pipeline-runner/PROMPT.md`~~ | ~~Existed — pretended Pipeline Orchestrator was an AI agent~~ | **Removed** — see Architecture Finalization sprint |
| `orchestration/OUTPUT-TEMPLATE.md` | Exists — run record format | **Keep** — the run record is a valid output artifact |

---

## Recommendation

**The Pipeline Orchestrator is not an AI agent. It is an orchestration contract + deterministic implementation detail.**

It should NOT have a PROMPT.md in the style of an LLM system prompt. It does NOT need "You are the Pipeline Orchestrator..." — that framing is architecturally incorrect for a component whose every decision is deterministic.

### Immediate actions

1. **Keep `orchestration/SPEC.md`** — it defines the orchestration contract (which stages connect, what contracts exist, what validates). This is the most valuable artifact.

2. **Keep `orchestration/OUTPUT-TEMPLATE.md`** — the run record format is valid and useful.

3. **Keep `orchestration/README.md`** — the overview is correct.

4. ~~**Remove or replace `agents/pipeline-runner/PROMPT.md`** — it presents the Pipeline Orchestrator as an AI agent, which it is not.~~ **Done** — removed in Architecture Finalization sprint.

### Implementation guidance (when ready)

When the Pipeline Orchestrator is implemented, it should be:

- A **deterministic script or CLI tool** — not an LLM invocation
- Able to read candidate data from OPPORTUNITY-QUEUE.md
- Able to run shell commands (astro build, curl)
- Able to parse fields from markdown/YAML files
- Able to write run records to docs/pipeline-runs/
- Able to update queue status

Language: whatever is most practical for the project (Bash, Node.js, Python — the project already uses Node.js for Astro).

The AI agents (ORA, Research Compiler, Editorial Builder) remain LLM-based and produce creative output. The Pipeline Orchestrator coordinates them deterministically — it reads their structured output fields and routes accordingly, without needing to understand their content.

---

## Summary

| Question | Answer |
|---|---|
| Is Pipeline Orchestrator an AI agent? | **No** |
| Is it an orchestration contract? | **Yes** — the SPEC defines stage relationships |
| Is it an implementation detail? | **Yes** — the execution is deterministic script logic |
| What should a PROMPT.md contain? | **Nothing** — the orchestrator is not an LLM agent. Replace with execution spec or remove. |
| Can the existing SPEC.md stay? | **Yes** — it defines the orchestration contract correctly. |
| Does the Pipeline Orchestrator change any existing agent? | **No** — it orchestrates around them without modification. |
| Should implementation proceed? | **Yes** — but as a deterministic script, not an AI agent. |

# Pipeline Orchestrator

Orchestrates the AI Editorial Operating System — routes candidates through the correct production pipeline, validates handoffs, and decides whether execution should continue.

## What It Does

The Pipeline Orchestrator is the single orchestration point for the editorial pipeline. It does not create content, perform research, or edit articles. It determines:

- **Which pipeline** should execute (Light or Heavy)
- **Which agent** executes next
- **Whether required contracts exist** between stages
- **Whether a stage passed validation**
- **Whether execution should continue, retry, or block**

## What It Does NOT Do

- Create content (Editorial Builder's job)
- Perform research (ORA / Research Compiler's job)
- Edit articles (Editorial QA's job)
- Deploy (Publisher's job)
- Discover opportunities (ODA's job)

## Files

| File | Purpose |
|---|---|
| `README.md` | Overview and quick reference |
| `SPEC.md` | Functional specification — mission, routing logic, failure handling |
| `OUTPUT-TEMPLATE.md` | Run log and stage result output format |

## Pipeline Stages

| Stage | Agent | Light Pipeline | Heavy Pipeline |
|---|---|---|---|
| Discovery | `agents/opportunity-discovery-agent/` | ✅ | ✅ |
| Research | `agents/opportunity-research-agent/` | ✅ | ❌ |
| Research Compiler | `agents/research-compiler/` | ❌ | ✅ |
| Writer | `agents/editorial-builder/` | ✅ | ✅ (optional) |
| QA | `agents/editorial-qa/` | ✅ | ✅ |
| Publisher | `agents/publisher/` | ✅ | ✅ |

## Routing Decision

The Pipeline Orchestrator reads the candidate's `pipeline_type` field (set at Discovery) to determine which pipeline to execute. A single field determines the entire downstream route — no manual routing decisions needed.

## Related Documents

| Document | Relationship |
|---|---|
| `docs/PIPELINE-ARCHITECTURE.md` | Defines which stages exist and how they connect |
| `docs/PIPELINE-HANDOFF-STANDARD.md` | Defines how each stage ends (handoff block format) |
| `agents/opportunity-discovery-agent/SPEC.md` | Defines Discovery's output (OPPORTUNITY-QUEUE.md) |
| `agents/opportunity-research-agent/SPEC.md` | Defines ORA's output (Opportunity Brief) |
| `agents/research-compiler/SPEC.md` | Defines Research Compiler's output (Research Brief) |
| `agents/editorial-builder/SPEC.md` | Defines Editorial Builder's output (.astro file) |

# Agent Usability Audit

**Date:** 2026-08-05  
**Scope:** Whether the defined agents are executable in today's production, and the evidence for each limitation.  
**Change status:** Audit only. No implementation changes were made.

## Executive finding

The project's agent directories contain definitions, prompts, schemas, and templates, but no non-Markdown executable agent source files. The verified daily OLSP production path is instead implemented by `commander/executors.py`, the social planner, funnel/measurement components, and related providers.

## Directly usable in today's OLSP production

### Commander executor registry

**Evidence:** `commander/executors.py:131-241, 603-679`.

The registered executor IDs are:

- `olsp-baseline-access`
- `content-funnel-review`
- `olsp-content-improvement-plan`
- `olsp-evidence-review`
- `olsp-minimum-daily-production-system`
- `prepare-content-plan`
- `social-production`
- `video-production`

These are the only project components directly registered in the `EXECUTORS` dictionary. They are callable project functions, not agent-directory agents.

### Social Planner

**Evidence:** `commander/social_planner.py`.

It reads the OLSP article, builds a Facebook plan, tracks publication state, and writes runtime plan data. It is a working component, not a separately defined agent.

### OLSP measurement and funnel checks

**Evidence:** `commander/executors.py`, `app/commander/content_funnel.py`, and `app/providers/olsp_dashboard.py`.

These components have a project executor path and are directly relevant to the daily OLSP cycle.

## Usable local research components, but not bound to the defined agents

### Community Intelligence

**Evidence:** `research/community_intelligence/processor.py`.

The processor has a defined JSON input and output:

```text
Input:  research/output/discovery/{pillar}-discovery.json
Output: research/output/community-intelligence/{pillar}-community-intelligence.json
```

It can process an existing Discovery Package. The defined agent remains manual for community discovery; the processor does not collect community discussions itself.

### Opportunity Discovery

**Evidence:** `research/discovery/runner.py`.

The runner has a `main()` entry point and writes Discovery Packages. It requires a configuration file and provider. A direct `--help` invocation is not supported: the argument is interpreted as a configuration path and fails with `Config file not found: --help`.

The file `research/discovery/test_discovery.py` is an executable diagnostic script, not a pytest test suite. Running it through pytest collected no tests.

### Research Factory

**Evidence:** `research/research_factory/factory.py`.

It has a `main()` entry point and produces `research-packages` JSON from Opportunity Brief JSON. It is locally callable for existing artifacts, but the active Heavy architecture names Research Compiler instead.

### Content Production

**Evidence:** `research/content_production/producer.py`.

It has a `main()` entry point and writes:

```text
research/output/content/{pillar}-content.json
```

This does not satisfy the agent definition's promised publication-ready `.astro` output. The implementation produces structured JSON content data.

### Editorial QA

**Evidence:** `research/editorial_qa/validator.py`.

It has a `main()` entry point and writes QA JSON. Its inputs are JSON content and research reports, while the agent definition describes validation of a production `.astro` article. The handoff is therefore not proven equivalent.

### Publishing Engine

**Evidence:** `publishing/publish.cjs`.

The command's help output works and requires a QA report. This is a real publishing tool, but it is not proof that the Publisher agent itself is an independently executable agent.

## Defined agents not usable as verified production agents

### Opportunity Research Agent (ORA)

**Evidence:** `agents/opportunity-research-agent/` exists, but no matching `research/opportunity_research/` implementation or Commander executor exists.

**Blocker:** The six-stage ORA definition has no verified callable implementation.

### Research Compiler

**Evidence:** `agents/research-compiler/` exists, but no separate `research_compiler` implementation exists. `research/research_factory/factory.py` is a different component.

**Blocker:** The defined agent and executable implementation are not bound.

### Editorial Builder

**Evidence:** `pipeline/bridge-to-builder.sh` exists and invokes `opencode run --auto`.

**Blockers:** It depends on the external OpenCode runtime, references legacy research paths, and the active pipeline architecture marks Editorial Builder as `Placeholder`.

### Pipeline Orchestrator

**Evidence:** `orchestration/SPEC.md:3-4` states `Status: Design — not yet implemented`.

`pipeline/run.sh` only constructs a prompt and invokes `opencode run`; it is not an independently validated orchestrator implementation.

## Common production blockers

1. Agent directories contain no non-Markdown executable source files.
2. Definitions and `research/` implementations are not bound by a registry.
3. Input/output contracts do not match: agent definitions promise `.astro` output while implementations produce JSON packages.
4. Research Factory and Research Compiler overlap, while the active architecture selects Research Compiler.
5. Editorial Builder, QA, and Publisher are described as production-capable in some files but as `Placeholder` in `docs/PIPELINE-ARCHITECTURE.md`.
6. Orchestration depends on `opencode run` rather than a verified project-native execution chain.
7. The discovery diagnostic file is not a collected pytest suite.

## Final classification

**Usable today:** Commander executor registry, social planner, OLSP measurement/funnel components, and the standalone publishing engine when its QA and deployment prerequisites exist.

**Conditionally usable:** Discovery, community processing, Research Factory, content production, and QA Python components when their exact JSON inputs are present and their output mismatch is accepted.

**Not verified as production agents:** ORA, Research Compiler, Editorial Builder as a bound agent, Publisher as a bound agent, and the Pipeline Orchestrator.

The main limitation is not that every specification is empty. The limitation is that the definitions, executable implementations, input/output contracts, and orchestration layer do not form one verified production system.

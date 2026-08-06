# Commander Organization Inventory

**Date:** 2026-08-05  
**Scope:** Existing project agents, roles, skills, permanent responsibilities, and their fit with the Commander operating model.  
**Change status:** Inventory only. No implementation or organizational changes were made.

## Authority boundary

The authoritative coordination role is defined by `ROLE.md` and Hermes `docs/commander/SOUL.md`. The project agent contract is defined by `docs/AGENT-CONTRACT.md`. The active editorial pipeline is defined by `docs/PIPELINE-ARCHITECTURE.md`.

The previously authored documents `docs/DAILY-OPERATIONAL-LEADERSHIP-PLAN.md` and `docs/CONTINUOUS-PRODUCTION-LEADERSHIP-MODEL.md` are Commander proposals, not authoritative agent definitions. Their named members must not be treated as existing agents without an underlying definition.

## Existing roles

### Hermes

- **Source:** `ROLE.md:3-24`
- **Purpose:** Executive AI, coordinator, planner, and quality controller.
- **Permanent responsibility:** Understand the repository and Owner objectives, plan, prioritize, delegate, validate, maintain documentation, and protect repository quality.
- **Today's use:** Coordinate the OLSP daily cycle and validate executor evidence.
- **Failure:** Work remains incomplete or unverifiable.

### Commander

- **Sources:** Hermes `docs/commander/SOUL.md`; project `STRATEGY.md:97-112`.
- **Purpose:** Select and execute the highest-probability action toward the measurable daily objective.
- **Permanent responsibility:** Observe, learn, analyse, plan, delegate, execute, measure, review, and maintain operational integrity.
- **Today's use:** Operate through the registered project executors in `commander/executors.py`.
- **Failure:** Wrong prioritization, unverifiable completion, or stopping at analysis/reporting.

### Pipeline Orchestrator

- **Source:** `orchestration/SPEC.md:1-10`
- **Purpose:** Route editorial candidates through Light or Heavy pipelines and validate stage handoffs.
- **Status:** Design only; the specification explicitly says `not yet implemented`.
- **Today's use:** None in the verified daily OLSP cycle.

## Existing project agent definitions

The repository contains these agent directories:

`community-intelligence`, `content-production`, `editorial-builder`, `editorial-qa`, `opportunity-discovery-agent`, `opportunity-research-agent`, `pipeline-runner`, `publisher`, `research-compiler`, and `research-factory`.

### Community Intelligence Agent

- **Sources:** `agents/community-intelligence/{README,SPEC,PROMPT,OUTPUT-SCHEMA}.md`
- **Purpose:** Discover and analyse real questions, problems, and gaps in Reddit, Quora, and niche forums.
- **Boundaries:** Does not perform keyword research, demand validation, content production, or publication decisions.
- **Today's use:** Manual community intelligence for future editorial opportunities.
- **Status:** V1 defined; README documents manual discovery and no automated crawling.

### Content Production Agent

- **Sources:** `agents/content-production/{README,SPEC,PROMPT,OUTPUT-SCHEMA}.md`
- **Purpose:** Convert a completed Research Brief into a publication-ready `.astro` article.
- **Today's use:** Only when an editorial content task is selected.
- **Status:** Defined, but no corresponding project executor is registered.

### Editorial Builder Agent

- **Sources:** `agents/editorial-builder/{README,SPEC,PROMPT,OUTPUT-TEMPLATE}.md`
- **Purpose:** Generate self-contained Astro article files.
- **Today's use:** Potential downstream writer after research.
- **Status:** Contradictory. Its README describes an operating workflow, while `docs/PIPELINE-ARCHITECTURE.md:68-76` marks it as `Placeholder`.

### Editorial QA Agent

- **Sources:** `agents/editorial-qa/{README,SPEC,PROMPT,OUTPUT-SCHEMA}.md`
- **Purpose:** Verify research fidelity, evidence, links, metadata, Astro compatibility, and publication readiness.
- **Today's use:** Validate a completed article before publication.
- **Status:** Defined, but the active pipeline architecture marks it as `Placeholder`.

### Opportunity Discovery Agent

- **Sources:** `agents/opportunity-discovery-agent/{README,SPEC,PROMPT,OUTPUT-TEMPLATE}.md`
- **Purpose:** Discover and prioritize editorial opportunities and write `runtime/editorial-pipeline/OPPORTUNITY-QUEUE.md`.
- **Today's use:** Future content opportunity discovery, not direct daily traffic execution.
- **Status:** README reports `Implemented — dry-run validated`.
- **Boundary:** It does not invoke ORA or make the final publishing decision.

### Opportunity Research Agent (ORA)

- **Sources:** `agents/opportunity-research-agent/{README,SPEC,PROMPT,OUTPUT-TEMPLATE}.md`
- **Purpose:** Research one Light Pipeline keyword and produce an Opportunity Brief.
- **Today's use:** Research a selected future editorial candidate.
- **Status:** README reports Production, but execution is prompt/file based and not a registered daily OLSP executor.
- **Boundary:** It does not write articles or publish.

### Pipeline Runner

- **Sources:** `agents/pipeline-runner/README.md`, `orchestration/*`
- **Purpose:** Deterministic orchestration layer.
- **Status:** Not an independent AI agent. Its specification was moved to `orchestration/`, whose status is design/not implemented.
- **Today's use:** No verified execution path.

### Publisher Agent

- **Sources:** `agents/publisher/{README,SPEC,PROMPT}.md`
- **Purpose:** Build-verify, commit, push, and post-publish verify a QA-approved article.
- **Today's use:** Only for a completed editorial publication.
- **Status:** Defined, but `docs/PIPELINE-ARCHITECTURE.md:74-76` marks it as `Placeholder`. `publishing/publish.cjs` is a real engine, not proof of an independently executable Publisher agent.

### Research Compiler Agent

- **Sources:** `agents/research-compiler/{README,SPEC,PROMPT,OUTPUT-TEMPLATE}.md`
- **Purpose:** Research Heavy Pipeline subjects and register reusable Knowledge Assets.
- **Today's use:** Heavy editorial research when selected.
- **Status:** Formalized, but README states it has not been run as a standalone invoked agent.

### Research Factory Agent

- **Sources:** `agents/research-factory/{README,SPEC,PROMPT,OUTPUT-SCHEMA}.md`
- **Purpose:** Convert an Opportunity Brief into a Research Brief.
- **Today's use:** No verified active route in the current Heavy/Light architecture.
- **Status:** Overlaps the Research Compiler. The active pipeline architecture names Research Compiler, not Research Factory.

## Registered OLSP production executors

These are implementation components, not agent definitions. They are registered in `commander/executors.py:1-5, 131-241, 603-679`:

1. `olsp-baseline-access` — verify repository and measurement baseline.
2. `content-funnel-review` — inspect article, CTA, and MegaLink path.
3. `olsp-content-improvement-plan` — produce a read-only improvement proposal.
4. `olsp-evidence-review` — classify available and missing evidence.
5. `olsp-minimum-daily-production-system` — run the smallest truthful daily OLSP cycle.
6. `prepare-content-plan` — prepare a content plan.
7. `social-production` — build the daily Facebook plan.
8. `video-production` — invoke the shared video capability; current strategy excludes video publication.

The daily OLSP cycle therefore uses executor functions rather than the editorial agent folders above.

## Skills

There is no project-local `skills/` directory. The relevant shared Hermes skill is:

### Video Skill

- **Source:** `/home/yampa/projects/active/hermes/skills/video/SKILL.md`
- **Purpose:** Convert approved written content into a vertical publish-ready video, preferably through OpenMontage.
- **Today's use:** Excluded by `STRATEGY.md:61-67` and the current user instruction to skip video production.
- **Status:** Active shared capability, not an OLSP-specific agent.

External skills referenced by agent specifications are not local project definitions and cannot be counted as verified permanent project roles.

## Missing roles and contradictions

### Missing

1. No `agents/editorial-intelligence/` directory exists although `README.md:16` references it.
2. The Agent Contract defines Performance Intelligence (`docs/AGENT-CONTRACT.md:95-106`), but no corresponding agent directory exists.
3. The Pipeline Orchestrator is specified but not implemented (`orchestration/SPEC.md:4`).
4. No named agent owns end-to-end GA4/OLSP attribution and resource reallocation.
5. No Reddit, forum, or Facebook-group publisher is implemented; strategy explicitly marks Reddit `not_a_channel` (`STRATEGY.md:74-77`).
6. Email scripts exist, but the strategy requires approval before sending (`STRATEGY.md:79-92`).

### Overlap or conflict

1. Content Production and Editorial Builder both describe article production.
2. Research Factory and Research Compiler both describe Research Brief creation; the active architecture selects Research Compiler.
3. Publisher Agent and `publishing/publish.cjs` have overlapping publication responsibilities without a verified agent invocation path.
4. Pipeline Runner and Pipeline Orchestrator describe the same orchestration layer, while the orchestrator remains unimplemented.
5. README says eight pipeline agents, but ten agent directories exist and one referenced directory is missing.
6. Several agents are described as production-capable in their own READMEs but as `Placeholder` in the active pipeline architecture.

## Fit with the Commander leadership model

**Verdict: PARTIAL FIT.**

The high-level model fits: Hermes/Commander is defined as coordinator, delegation is required, stages are isolated, and the OLSP repository has a concrete executor registry.

The organization is not yet a single trustworthy operational team. Most named agents are specifications and prompts rather than callable executors; the editorial orchestrator is not implemented; measurement ownership is fragmented; and several roles have overlapping or contradictory status definitions.

No organizational change is recommended in this inventory. The evidence supports a follow-up authority reconciliation before adding or renaming any role.

# Commander Operating Organization

**Status:** Authoritative project operating map  
**Project:** Profit and Privilege / OLSP  
**Effective:** 2026-08-05  
**Purpose:** Define the one-Commander organization for the single active project.

This document describes the current organization by binding each role to an existing, inspectable component. A role is not considered production-capable merely because a prompt or historical profile exists.

The machine-readable binding registry is `commander/organization.py`. This
document defines the role meaning; the registry defines the current entrypoint
and status for runtime checks.

## Operating authority

The authority chain is:

1. Owner — mission, strategic direction, and genuine authority boundaries.
2. Commander — operational decisions and coordination inside the approved strategy.
3. Role implementation — bounded execution component assigned by Commander.
4. Project state, runtime evidence, and external services — inputs and verification evidence.

The daily business objective remains defined by `OBJECTIVES.md`: five new OLSP signups and one $7 OLSP sale per day.

## Organization

### Commander — business lead

- **Purpose:** Select, coordinate, execute, verify, and close the highest-probability action toward the daily objective.
- **Implementation:** Hermes Commander core plus `commander/executors.py`.
- **Entry path:** `hermes next`, `hermes run`, and the Commander execution loop.
- **Today:** Read objective, strategy, state, funnel, measurement, and campaign evidence; select one executable action; verify its result.
- **Failure response:** Stop the failed branch, classify the cause, and select the highest-probability remaining action.

### Scout — evidence and opportunity intelligence

- **Purpose:** Find and verify audience questions, market signals, community problems, and acquisition opportunities.
- **Existing implementations:** `research/discovery/runner.py`, `research/community_intelligence/processor.py`, and the project `agents/community-intelligence/` specifications.
- **Status:** Conditional. The local processors exist, but community discovery remains manual and is not registered as a Commander executor.
- **Today:** Use only when current business evidence shows that new audience or opportunity intelligence is the highest-value action.
- **Failure response:** Mark evidence incomplete; do not invent demand or convert observations into facts.

### Reach — traffic, conversion, and growth operator

- **Purpose:** Turn verified business evidence into traffic, conversion, and resource-allocation decisions.
- **Existing implementations:** `commander/goal_plan.py`, `commander/social_planner.py`, `commander/content_funnel.py`, `app/providers/ga4_metrics.py`, `app/providers/olsp_dashboard.py`, and approved campaign evaluators.
- **Status:** Operational as a responsibility distributed across Commander components; no separate Reach agent exists.
- **Today:** Evaluate the article → CTA → MegaLink path, social plan readiness, attributed traffic, and verified OLSP outcomes.
- **Failure response:** Do not scale traffic when the funnel or measurement is invalid; select repair or verification instead.

### Scribe — evidence-based content production

- **Purpose:** Convert verified research into accurate English-language articles and campaign content.
- **Existing implementations:** `research/content_production/producer.py`, `agents/content-production/`, `agents/editorial-builder/`, and `pipeline/bridge-to-builder.sh`.
- **Status:** Operational for the content-package stage. `commander/scribe.py` validates the JSON package and writes a `READY_FOR_BUILDER` handoff. Editorial Builder remains a separate downstream Astro stage.
- **Today:** Produce or revise content only when Commander selects content as the highest-value action and the required evidence contract exists.
- **Failure response:** Stop on missing evidence, unsupported claims, or an output-contract mismatch.

### Coder — technical repair and reliability

- **Purpose:** Repair local code, paths, tests, configuration, and runtime defects required by the approved objective.
- **Existing implementations:** Project source code and tests; the Hermes `agents/coder/` profile is only a stub and uses a legacy `./projects/<id>` path.
- **Status:** Conditional and not currently delegated through a canonical project executor.
- **Today:** Commander may perform or assign local, reversible technical repairs through the repository's existing execution path.
- **Failure response:** Preserve a recoverable state, classify the defect, and do not use the legacy project path.

### Measurement — reality and attribution verification

- **Purpose:** Establish what actually happened: signups, sales, revenue, traffic, source attribution, and funnel outcomes.
- **Existing implementations:** `app/providers/olsp_dashboard.py`, `app/providers/ga4_metrics.py`, `app/commander/measurement.py`, and `runtime/` evidence artifacts.
- **Status:** Operational for read-only collection, with known limits when external data is unavailable or period-scoped fields are incomplete.
- **Today:** Verify daily outcomes before and after production actions; never relabel aggregate data as daily results.
- **Failure response:** Mark the metric unknown or partial and prevent false optimization decisions.

### Publisher — controlled delivery

- **Purpose:** Deliver a verified article or approved production artifact through the current deployment path and verify the result.
- **Existing implementation:** `publishing/publish.cjs` and the project publishing documentation.
- **Status:** Conditional. The publishing engine exists; the Publisher agent and Worker deployment invoker are not fully bound into one verified autonomous path.
- **Today:** Use only when the artifact, QA evidence, and deployment access are present.
- **Failure response:** Stop before publication or deployment and report the exact missing contract or permission.

## Delegation rule

Commander does not dispatch fictional agents. It selects the role that owns the next action and invokes the existing implementation bound to that role. If no implementation exists, the role is reported as conditional or blocked and is not presented as an executable production capability.

## Current binding status

| Role | Status | Current entrypoint evidence |
|---|---|---|
| Commander | Operational | `hermes next`, `hermes run`, `app/commander/` |
| Scout | Conditional | `research/discovery/runner.py`, `research/community_intelligence/processor.py` |
| Reach | Operational | `commander/executors.py`, `commander/goal_plan.py` |
| Scribe | Operational | `commander/scribe.py`, `research/content_production/producer.py` |
| Coder | Conditional | `/home/yampa/projects/active/hermes/agents/coder/run.sh --check`; editing still depends on Aider |
| Measurement | Operational | `app/providers/olsp_dashboard.py`, `app/providers/ga4_metrics.py` |
| Publisher | Conditional | `publishing/publish.cjs` with QA and deployment prerequisites |

## Current daily execution path

The verified OLSP path is:

```text
Commander
  → Measurement / Funnel verification
  → Reach decision
  → Social Planner or local repair executor
  → Provider or local artifact
  → Measurement verification
  → Commander closes the action and selects the next one
```

Scout and Scribe are supporting roles, not automatic first steps. They are selected only when current evidence shows that intelligence or content will move the business objective faster than measurement, funnel repair, or approved traffic execution.

## Historical role status

The archived Hermes profiles remain historical references:

- `_archive/docs/SCOUT.md` — research and intelligence, not a traffic publisher.
- `_archive/docs/REACH.md` — growth, SEO, monetization, email, analytics, and conversion.
- `_archive/docs/SCRIBE.md` — writing and documentation.

They are role precedents, not current executable agents. Their responsibilities are represented here only where a current implementation exists.

## Superseded proposal documents

The following documents are supporting planning material and are not independent organization authorities:

- `docs/DAILY-OPERATIONAL-LEADERSHIP-PLAN.md`
- `docs/CONTINUOUS-PRODUCTION-LEADERSHIP-MODEL.md`

This document is the single project-scoped organization map. It does not authorize a new channel, external service, or strategic change.

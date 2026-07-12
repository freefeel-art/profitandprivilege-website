# Pipeline Orchestrator — Functional Specification

**Version:** 1.0
**Status:** Design — not yet implemented

---

## 1. Mission

Route an editorial candidate through the correct production pipeline by orchestrating stage execution, validating handoff contracts, and deciding whether execution should continue, retry, or block. The Pipeline Orchestrator is the single orchestration point of the AI Editorial Operating System. It does not create content, perform research, or edit articles.

---

## 2. Scope

### In scope

- Accepting a candidate promotion from the Opportunity Queue (ODA output) or a direct operator-specified subject
- Reading the candidate's `pipeline_type` field and routing to the correct pipeline
- Validating that the required input contract exists before invoking each stage
- Invoking each stage agent with the correct parameters
- Reading each stage's handoff block to determine Stage Status
- Validating that each stage's output artifact exists at the expected path
- Checking for required fields in handoff artifacts before proceeding
- Deciding whether to continue to the next stage, retry the current stage, or block the pipeline
- Logging the pipeline run to a run record
- Reporting final disposition (article published, Knowledge Asset registered, or blocked with reason)

### Out of scope

- Creating content (Editorial Builder's job)
- Performing research (ORA / Research Compiler's job)
- Editing or QA-checking articles (Editorial QA's job)
- Deploying or publishing (Publisher's job)
- Discovering or scoring opportunities (ODA's job)
- Modifying any agent's SPEC, PROMPT, or OUTPUT-TEMPLATE
- Making editorial decisions about what to write
- Generating SEO metadata, internal link plans, or CTA placement

---

## 3. Decision Boundaries

The Pipeline Orchestrator is the **single decision point** for all pipeline-state questions. No other agent answers these:

| Decision | Authority | Source of truth |
|---|---|---|
| Which pipeline (Light / Heavy)? | Pipeline Orchestrator | Candidate's `pipeline_type` field |
| Which agent executes next? | Pipeline Orchestrator | Pipeline stage map (Section 6) |
| Does the input contract exist? | Pipeline Orchestrator | Contract registry (Section 7) |
| Did the stage pass validation? | Pipeline Orchestrator | Handoff block Stage Status + artifact check |
| Should we retry or block? | Pipeline Orchestrator | Failure handling rules (Section 10) |
| Should the pipeline continue? | Pipeline Orchestrator | Validation checkpoints (Section 9) |
| Is the pipeline run complete? | Pipeline Orchestrator | Final disposition rules |

No agent decides its own successor. No agent decides whether its own output is adequate for the next stage. No agent decides whether the pipeline continues after a failure.

---

## 4. Inputs

### Required

| Field | Type | Description | Source |
|---|---|---|---|
| `candidate_id` | string | The candidate to promote, from ODA's OPPORTUNITY-QUEUE.md | ODA queue row |
| `candidate_keyword` | string | The search keyword for this candidate | ODA queue row |
| `pipeline_type` | enum: `Light` / `Heavy` | Which pipeline to execute | ODA queue row |
| `pillar` | string | Content pillar from CONTENT-REGISTRY.md | ODA queue row |

### Optional (override defaults)

| Field | Type | Description |
|---|---|---|
| `article_type` | enum: `review` / `blog` / `roundup` | Override the article type if the candidate does not specify one |
| `affiliate_product` | string | Override the CTA product |
| `skip_qa` | boolean | Skip Editorial QA stage (dev/test only) |
| `skip_publish` | boolean | Stop after QA without publishing |
| `max_retries` | integer | Override default retry count per stage (default: 2) |

---

## 5. Outputs

### Primary output

A **Pipeline Run Record** saved to:
```
docs/pipeline-runs/[candidate-id]-[timestamp].md
```

The run record documents every stage executed, every handoff validated, and the final disposition.

### Side effects

Each stage produces its own artifact:

| Stage | Artifact |
|---|---|
| ORA (Light) | `agents/opportunity-research-agent/briefs/[slug].md` |
| Research Compiler (Heavy) | `docs/research/[slug].md` + Heavy Asset Library entry |
| Editorial Builder | `src/pages/{type}/[slug].astro` |
| Editorial QA | Validation report (future) |
| Publisher | Git commit + deployment (future) |

---

## 6. Pipeline Routing Logic

### 6.1 Entry Point

```
Operator promotes candidate (candidate_id, pipeline_type)
    │
    ▼
Pipeline Orchestrator reads OPPORTUNITY-QUEUE.md row for candidate_id
    │
    ▼
Pipeline Orchestrator reads the candidate's pipeline_type field
    │
    ├── Light ───────────────────────────────────────────▶ Light Pipeline
    │
    └── Heavy ───────────────────────────────────────────▶ Heavy Pipeline
```

### 6.2 Light Pipeline Flow

```
Stage 1L: Opportunity Research Agent (ORA)
    Input:  candidate_keyword, intent_hint (from queue), affiliate_product (from queue)
    Output: Opportunity Brief at agents/opportunity-research-agent/briefs/[slug].md
    Contract check: brief file exists, Section 8 fields present
    │
    ▼
Stage 2:  Editorial Builder
    Input:  Opportunity Brief path, article_type (from Section 8 recommended_content_type)
    Output: .astro file at src/pages/{type}/[slug].astro
    Contract check: file exists, astro build passes, HTTP 200
    │
    ▼
Stage 3:  Editorial QA (if not skipped)
    Input:  .astro file path
    Output: QA report (future)
    Contract check: QA passes or issues are documented
    │
    ▼
Stage 4:  Publisher (if not skipped)
    Input:  .astro file path, commit message
    Output: Git commit + deployment
    │
    ▼
Complete: Run record finalized, OPPORTUNITY-QUEUE.md status → published
```

### 6.3 Heavy Pipeline Flow

```
Stage 1H: Research Compiler
    Input:  subject (candidate_keyword), subject_type (derived from queue row)
    Output: Research Brief at docs/research/[slug].md + Heavy Asset Library entry
    Contract check: brief file exists, Heavy Asset Library entry present
    │
    ▼
    Decision: Build article from this Knowledge Asset?
    │             │
    │             ├── Yes ──▶ Continue to Stage 2
    │             │
    │             └── No ───▶ Complete — Knowledge Asset registered, no article built
    │
    ▼
Stage 2:  Editorial Builder
    Input:  Research Brief path, article_type (determined by operator or candidate),
            cta_product, internal_link_targets
    Output: .astro file at src/pages/{type}/[slug].astro
    Contract check: file exists, astro build passes, HTTP 200
    │
    ▼
Stage 3:  Editorial QA (if not skipped)
Stage 4:  Publisher (if not skipped)
    │
    ▼
Complete: Run record finalized, OPPORTUNITY-QUEUE.md status → published
```

---

## 7. Contract Registry

The Pipeline Orchestrator maintains a contract registry — a list of verifiable checks for each stage handoff. Before invoking a stage, the orchestrator checks that the required input exists. After the stage completes, it checks that the required output exists.

### 7.1 Light Pipeline Contracts

| Handoff | Pre-invoke check | Post-invoke check |
|---|---|---|
| ORA → Opportunity Brief | `candidate_keyword` is non-empty | File exists at `agents/opportunity-research-agent/briefs/[slug].md`; field `editorial_decision` is one of `WRITE NOW` / `WAIT` / `DO NOT WRITE`; if `DO NOT WRITE`, pipeline stops |
| Opp Brief → Editorial Builder | File exists; `recommended_content_type` is one of `Review` / `Blog` / `Roundup`; `cta_product` is non-empty; `internal_link_targets` is non-empty | File exists at `src/pages/{type}/[slug].astro`; `astro build` returns exit code 0; HTTP 200 on dev server |
| .astro → Editorial QA | File exists; `astro build` passed | QA check results documented (future) |
| QA → Publisher | QA passed or explicit override | Git commit created; deployment confirmed (future) |

### 7.2 Heavy Pipeline Contracts

| Handoff | Pre-invoke check | Post-invoke check |
|---|---|---|
| Research Compiler → Research Brief | `subject` is non-empty; `subject_type` is valid enum value; no existing Knowledge Asset covers this subject (checked via HEAVY-ASSET-LIBRARY.md) | File exists at `docs/research/[slug].md`; entry exists in `docs/HEAVY-ASSET-LIBRARY.md` with Status `Active` |
| Research Brief → Editorial Builder | File exists; `article_type` is non-empty; `cta_product` is non-empty; `internal_link_targets` is non-empty | File exists at `src/pages/{type}/[slug].astro`; `astro build` passes; HTTP 200 |
| .astro → Editorial QA | Same as Light | Same as Light |
| QA → Publisher | Same as Light | Same as Light |

---

## 8. Required Metadata

The Pipeline Orchestrator reads and writes the following metadata fields. These are consumed from upstream stage artifacts and written to the pipeline run record.

### 8.1 Read from Opportunity Queue (ODA output)

| Field | Used for |
|---|---|
| `candidate_id` | Pipeline run record identity |
| `candidate_keyword` | ORA input (Light) / Research Compiler subject (Heavy) |
| `pipeline_type` | Pipeline routing decision |
| `pillar` | Run record context |
| `Opportunity Score` | Priority context for operator review |
| `Priority Score` | Priority context for operator review |

### 8.2 Read from Opportunity Brief (ORA output)

| Field | Used for |
|---|---|
| `editorial_decision` | Gate — if `DO NOT WRITE`, stop pipeline |
| `recommended_content_type` | Editorial Builder article type selection |
| `cta_product` | Editorial Builder CTA product |
| `internal_link_targets` | Editorial Builder internal link plan |
| `suggested_title` | Editorial Builder title copy |
| `suggested_h1` | Editorial Builder H1 copy |
| `suggested_meta` | Editorial Builder meta description |
| `opportunity_name` | Run record context |
| `primary_seo_target` | Run record context |

### 8.3 Read from Research Brief / Heavy Asset Library

| Field | Used for |
|---|---|
| `subject_type` | Context for article type selection (operator judgement call) |
| Asset Status | Gate — if `Needs Refresh`, flag for operator decision |
| `Reused By` | Internal linking context |

### 8.4 Read from Handoff Block (every stage)

| Field | Used for |
|---|---|
| `Stage Status` | Gate — `Complete` = proceed; `In Progress` = wait; `Blocked` = stop |
| `Produced Artifact(s)` | File path validation |
| `Current Pipeline Position` | Run record position tracking |
| `Recommended Next Stage` | Cross-reference against expected next stage |

---

## 9. Validation Checkpoints

Before each stage transition, the Pipeline Orchestrator executes these checks in order:

### Pre-invoke

1. **Input contract check** — Does every field in the contract registry (Section 7) for this handoff exist and have a non-empty value?
2. **Stage gating** — Is the stage enabled? (QA/Publisher may be skipped)
3. **Retry budget check** — Has this stage already failed the maximum number of retries?
4. **Operator override check** — Has the operator explicitly overridden any pre-flight checks?

### Post-invoke

1. **Stage Status check** — Read the handoff block's `Stage Status` field. If `Blocked`, stop. If `In Progress`, wait.
2. **Artifact existence check** — Does the artifact exist at the expected path?
3. **Artifact content check** — Does the artifact contain the required fields for the next handoff?
4. **Pipeline position check** — Does the handoff block's `Current Pipeline Position` match the expected transition?
5. **Build check (Editorial Builder only)** — Does `astro build` pass? Does the page return HTTP 200?

### Go / No-Go Decision

| All checks pass | Proceed to next stage |
|---|---|
| Any check fails (retries remaining) | Retry current stage up to `max_retries` |
| Any check fails (retries exhausted) | Block pipeline — record failure in run record |
| Handoff reports `Blocked` | Block pipeline — record blocker in run record |

---

## 10. Failure Handling

### 10.1 Stage-level failures

| Failure | Response |
|---|---|
| Stage agent does not produce expected artifact | Retry up to `max_retries`; if exhausted, block |
| Stage agent reports Stage Status `Blocked` | Record blocker from handoff block; do not retry |
| Stage agent reports Stage Status `In Progress` | Wait and re-check on next polling cycle |
| Artifact exists but fails contract validation | Retry with updated parameters if applicable; otherwise block |
| `astro build` fails | Block — do not pass broken build to next stage |
| External tool failure (DataForSEO, Google Trends, etc.) | Stage agent handles internally (per agent's own failure handling); Pipeline Orchestrator only checks the final handoff |

### 10.2 Retry behaviour

| Parameter | Default |
|---|---|
| `max_retries` per stage | 2 |
| Retry delay | Immediate (no cool-down in current design) |
| Retry trigger | Any post-invoke check failure in Section 9 |
| Retry scope | Full stage re-invocation (not partial) |
| Retry exhaustion | After `max_retries` failures, set stage status to `Failed` and pipeline status to `Blocked` |

### 10.3 Pipeline-level failures

| Failure | Response |
|---|---|
| `editorial_decision` is `DO NOT WRITE` | Stop pipeline. Record: "Candidate scored below WRITE NOW threshold — no article produced." Do not invoke Editorial Builder. |
| `editorial_decision` is `WAIT` | Stop pipeline. Record: "Candidate scored WAIT — operator should re-assess." Do not proceed. |
| Heavy Pipeline: Knowledge Asset exists and is current | Stop pipeline after Research Compiler (article build is optional). Record: "Knowledge Asset reused — no article built." |
| Heavy Pipeline: Knowledge Asset exists but is `Needs Refresh` | Flag for operator decision before proceeding |
| Pipeline already running for this candidate | Reject duplicate invocation |

### 10.4 What the Pipeline Orchestrator never does under failure

- Invoke a stage without its required input fields present
- Skip validation checks
- Produce content to fill a gap
- Modify an agent's output to make it pass validation
- Guess missing metadata values
- Retry indefinitely

---

## 11. Interaction With Other Agents

| Agent | How Pipeline Orchestrator interacts |
|---|---|
| **Opportunity Discovery Agent** | Reads OPPORTUNITY-QUEUE.md rows. Does not modify queue except to update `Status` and `Promoted brief path` fields. Does not invoke ODA — ODA is an independent exploration tool. |
| **Opportunity Research Agent** | Invokes ORA with `candidate_keyword` and optional context fields. Waits for ORA to produce Opportunity Brief. Reads handoff block from ORA output. |
| **Research Compiler** | Invokes Research Compiler with `subject` and `subject_type`. Waits for Research Brief and Heavy Asset Library entry. Reads handoff block. |
| **Editorial Builder** | Invokes Editorial Builder with the upstream artifact path and derived parameters (article type, CTA product, internal links). Waits for .astro file. Runs `astro build` as post-invoke validation. |
| **Editorial QA** | Invokes QA agent with the .astro file path (future). Reads QA report. Blocks if QA fails. |
| **Publisher** | Invokes Publisher with .astro file path and commit message (future). Confirms deployment. Updates OPPORTUNITY-QUEUE.md status to `published`. |

The Pipeline Orchestrator never modifies any agent's internal files (PROMPT.md, SPEC.md, OUTPUT-TEMPLATE.md). The only artifacts it writes are its own run record (`docs/pipeline-runs/[candidate-id]-[timestamp].md`) and status updates to the Opportunity Queue.

---

## 12. Run Record Schema

Every pipeline run produces a run record. See `OUTPUT-TEMPLATE.md` for the full template.

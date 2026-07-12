# Pipeline Run Record — [candidate_id]

**Run ID:** `[candidate-id]-[YYYY-MM-DD-HHMMSS]`
**Started:** [YYYY-MM-DD HH:MM:SS]
**Completed:** [YYYY-MM-DD HH:MM:SS / In Progress / Blocked]
**Status:** [Complete / In Progress / Blocked]

---

## Candidate

| Field | Value |
|---|---|
| Candidate ID | [candidate_id] |
| Keyword | [candidate_keyword] |
| Pipeline Type | [Light / Heavy] |
| Pillar | [pillar name] |
| Opportunity Score | [0–100] |
| Priority Score | [0–100] |
| Priority Label | [Produce soon / Hold / Defer] |

---

## Pipeline Execution Log

### Stage 1: [ORA / Research Compiler]

| Field | Value |
|---|---|
| Status | [Complete / In Progress / Blocked / Skipped] |
| Agent | [agents/opportunity-research-agent/ / agents/research-compiler/] |
| Pre-invoke checks | [Pass / Fail — detail] |
| Post-invoke checks | [Pass / Fail — detail] |
| Retries attempted | [0 / 1 / 2] |
| Artifact path | [path to produced artifact] |
| Handoff Stage Status | [Complete / In Progress / Blocked] |
| Handoff Next Stage | [next stage name] |

**Notes:**
- [Any notable observations, data gaps, or warnings from this stage]

---

### Stage 2: Editorial Builder

| Field | Value |
|---|---|
| Status | [Complete / In Progress / Blocked / Skipped] |
| Agent | agents/editorial-builder/ |
| Input artifact | [path to Opportunity Brief or Research Brief] |
| Article type | [review / blog / roundup] |
| CTA product | [affiliate product] |
| Internal link targets | [list of target paths] |
| Pre-invoke checks | [Pass / Fail — detail] |
| Post-invoke checks | [Pass / Fail — detail] |
| astro build | [Pass / Fail — exit code] |
| HTTP 200 | [Pass / Fail — status code] |
| Retries attempted | [0 / 1 / 2] |
| Artifact path | [path to .astro file] |

**Notes:**
- [Any notable observations, build warnings, or content decisions]

---

### Stage 3: Editorial QA

| Field | Value |
|---|---|
| Status | [Complete / In Progress / Blocked / Skipped] |
| Agent | agents/editorial-qa/ |
| Skipped reason | [skip_qa flag / not yet implemented] |

**Notes:**
- [QA findings, if applicable]

---

### Stage 4: Publisher

| Field | Value |
|---|---|
| Status | [Complete / In Progress / Blocked / Skipped] |
| Agent | agents/publisher/ |
| Skipped reason | [skip_publish flag / not yet implemented] |

**Notes:**
- [Publish confirmation, if applicable]

---

## Pipeline Summary

| Field | Value |
|---|---|
| **Final Disposition** | [Published / Knowledge Asset Registered / Blocked / Cancelled] |
| **Article URL** | [URL if published, or N/A] |
| **Knowledge Asset** | [path if registered, or N/A] |
| **Blocked at** | [stage name if blocked, or N/A] |
| **Block reason** | [specific reason if blocked, or N/A] |
| **Total stages executed** | [count] |
| **Total retries** | [count] |
| **Operator interventions** | [list of manual overrides or decisions, or None] |

---

## Opportunity Queue Update

| Field | Value |
|---|---|
| Status | [published / promoted / rejected — updated in OPPORTUNITY-QUEUE.md] |
| Promoted brief path | [path to the upstream artifact, if applicable] |

---

## Stage Handoff

**Stage Status:** Complete

### Completed Items
- [e.g. Routed candidate through Light pipeline (4 stages)]
- [e.g. Validated 4 handoff contracts — all passed]
- [e.g. Registered Knowledge Asset in Heavy Asset Library]
- [e.g. Article published at src/pages/blog/make-money-online-from-your-phone.astro]
- [e.g. OPPORTUNITY-QUEUE.md updated — status set to published]

### Produced Artifact(s)
| Artifact | Path |
|----------|------|
| Pipeline Run Record | `docs/pipeline-runs/[candidate-id]-[timestamp].md` |

### Current Pipeline Position
Pipeline Orchestrator → Done

### Recommended Next Stage
[Promote next candidate from OPPORTUNITY-QUEUE.md / Register new content in CONTENT-REGISTRY.md / Investigate blocker]

### Suggested Command / Prompt
```
[Candidate ID: next_candidate_id_from_queue]
[Keyword: next_candidate_keyword]
[Pipeline type: Light / Heavy]
[Pillar: pillar name]
```

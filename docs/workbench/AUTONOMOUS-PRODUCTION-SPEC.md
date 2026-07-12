# Autonomous Production Specification

## Overview

Mission Control supports three operating modes that determine how much of the production pipeline is automated. These modes are a permanent architectural feature of the AI Editorial Operating System.

---

## Operating Modes

### Manual

The operator starts every step manually. Mission Control assists by preparing recommendations, surfacing context, and showing the next logical action — but executes nothing automatically.

**What Mission Control does:**
- Displays today's recommended opportunity
- Shows current research and article state
- Prepares terminal commands for the operator to copy-and-execute
- Reports results after each manual step

**What the operator does:**
- Every action: topic selection, research trigger, article generation, QA, build, publish

### Assisted (Default)

Mission Control automatically executes the full content production workflow up to the point of publication. The article is produced and QA'd automatically, then waits for operator approval before publishing.

**What Mission Control does automatically:**
- Opportunity Discovery
- Research
- Research Brief generation
- Writer / Content Production
- Editorial QA
- Build

**What remains manual:**
- Publishing
- Final approval before publication

**Daily automation trigger (future):**
- 07:00 — Mission Control starts the assisted workflow automatically
- Article is ready for operator review by the time the operator starts work

### Autonomous (Not Enabled by Default)

Mission Control executes the entire production workflow including publication, commit, and push. A production report is generated after completion.

**What Mission Control does automatically:**
- Discovery
- Research
- Writer
- QA
- Build
- Commit
- Push
- Publish
- Production report generation

**Safeguards:**
- Must be explicitly enabled by the operator
- Operator can set a "publish window" (e.g. 09:00–17:00 only)
- Every autonomous run generates a full production report
- Operator can pause/resume autonomous mode at any time

---

## Daily Production Workflow

### Scheduled Run (Future)

The system supports a daily scheduled production cycle. The start time is configurable (default 07:00).

**Behaviour depends on operating mode:**

| Mode | 07:00 Behaviour |
|------|----------------|
| Manual | Prepare recommendations only. No automation. |
| Assisted | Run Discovery → Research → Brief → Writer → QA → Build. Wait for approval. |
| Autonomous | Run full workflow including publication. Generate production report. |

### Current (Pre-Scheduler) Behaviour

Without the scheduler, the operator initiates production manually via the "Start Production" / "Prepare Recommendations" button. The mode determines what happens after the button is clicked.

---

## Dashboard Fields

The Mission Control dashboard displays:

| Field | Source |
|-------|--------|
| Today's Goal | Computed from queue + operating mode |
| Current Opportunity | First incomplete opportunity from Opportunity Queue |
| Current Research | Latest research brief |
| Current Article | Most recently generated article |
| Pipeline Status | Current stage and its status |
| Last Published | Most recent publication report |
| Next Recommended Opportunity | Next unconsumed queue item |
| Current Operating Mode | `assisted` (default), `manual`, or `autonomous` |
| Next Scheduled Run | Configurable time (default 07:00) |

---

## Required Components

| Component | Status |
|-----------|--------|
| Operating mode selector (Manual / Assisted / Autonomous) | Sprint #2 |
| Mode-aware launch panel | Sprint #2 |
| Dashboard production status section | Sprint #2 |
| PipelineStore mode tracking | Sprint #2 |
| Mode badge in PipelineHealth | Sprint #2 |
| Mode-aware PipelineConsole messages | Sprint #2 |

### Future Components

| Component | Sprint |
|-----------|--------|
| Background scheduler service | Sprint #3 |
| Notification system (email/Slack/dashboard) | Sprint #3 |
| Autonomous publishing workflow | Sprint #4 |
| Publish window configuration | Sprint #4 |
| Production report templates | Sprint #4 |
| Mode transition confirmation dialogs | Sprint #3 |

---

## Safety Rules

1. **Autonomous mode is never enabled by default.** The operator must explicitly enable it.
2. **Autonomous publishing requires an additional confirmation** before the first autonomous run.
3. **Assisted mode always stops before publishing.** Publishing remains a manual gate.
4. **All mode transitions log an event** in the PipelineStore event log.
5. **Scheduled runs respect the operating mode.** Changing the mode mid-schedule cancels the current run.
6. **Architecture freeze:** No existing component is redesigned or replaced. Only extended.

---

## Future Scheduler Integration

The scheduler will be implemented as a standalone service that:
- Reads the configured operating mode
- Triggers production at the configured time (default 07:00)
- Respects operator-defined publish windows
- Logs all scheduled events
- Reports completion or failure

**Integration points:**
- `PipelineStore.setScheduledRun(time)` — configure the daily run time
- `PipelineStore.get().scheduledRun` — read current schedule
- Mode check before execution: read `PipelineStore.get().operatingMode`

---

## Future Notification System

Notifications will use a publish/subscribe pattern:
- **Channels:** Dashboard badge, email, Slack webhook
- **Events:** Production started, article ready for review, publish failed, daily report ready
- **Configuration:** Stored in `pipeline/config.json`

---

## Future Autonomous Publishing

Autonomous publishing requires:
- A publish window configuration (start/end time)
- An automatic `git commit && git push` step
- Integration with the Astro build system
- A production report written after completion
- A rollback mechanism in case of build failure

The architecture in Sprint #2 lays the foundation by:
- Adding the `operatingMode` field to PipelineStore
- Creating the mode selector UI
- Defining the stage boundaries per mode
- Establishing the safety rules

---

## Implementation Sprint #2

1. Create this specification document
2. Update PipelineStore with `operatingMode`, `scheduledRun`, `setOperatingMode()`
3. Update `mission-control.js` with mode-aware production state
4. Add operating mode selector to `RunPipeline.astro`
5. Mode-aware button text and launch panel per mode
6. Mode badge in `PipelineHealth.astro`
7. Mode-aware empty state in `PipelineConsole.astro`
8. Update dashboard section in `mission-control.astro` with all required fields
9. Build, verify, commit

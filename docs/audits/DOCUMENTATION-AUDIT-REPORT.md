# Documentation Audit Report

**Date:** 2026-07-12
**Scope:** All markdown files in `docs/`, `agents/`, and `pipeline/`
**Total docs/ files:** 66
**Referenced by code:** 14
**Never referenced:** 35

---

## 1. Active Architecture Documents (14)

| Document | Referenced by |
|---|---|
| `docs/AGENT-CONTRACT.md` | 12 agents, 1 pipeline |
| `docs/AI-EDITORIAL-OPERATING-SYSTEM.md` | 9 agents, 1 pipeline, 1 src |
| `docs/BLOG-MASTER-SPEC.md` | 5 agents |
| `docs/COMMUNITY-INTELLIGENCE.md` | 4 agents |
| `docs/CONTENT-REGISTRY.md` | 22 agents, 1 src |
| `docs/EDITORIAL-OBJECT-MODEL.md` | 5 agents |
| `docs/GOLD-MASTER-SPEC.md` | 6 agents, 1 src |
| `docs/HEAVY-ASSET-LIBRARY.md` | 7 agents, 1 src |
| `docs/PIPELINE-ARCHITECTURE.md` | 7 agents, 1 pipeline, 1 src |
| `docs/PIPELINE-HANDOFF-STANDARD.md` | 4 agents, 1 pipeline |
| `docs/WHY.md` | 10 agents |
| `docs/BLOG-MASTER-PROMPT.md` | 1 agent |
| `docs/PRODUCTION-MASTER-PROMPT.md` | 1 agent |
| `docs/ROUNDUP-GOLD-MASTER-SPEC.md` | 4 agents |

## 2. Active Specifications (4)

| Document | Status |
|---|---|
| `docs/BLOG-MASTER-SPEC.md` | Active, referenced |
| `docs/GOLD-MASTER-SPEC.md` | Active, referenced |
| `docs/ROUNDUP-GOLD-MASTER-SPEC.md` | Active, referenced |
| `docs/COMMUNITY-INTELLIGENCE-SPEC.md` | Orphan — never referenced |

## 3. Active Contracts (2)

| Document | Status |
|---|---|
| `docs/AGENT-CONTRACT.md` | Active, referenced by 12 agents |
| `docs/architecture/ADR-001-EDITORIAL-BUILDER-ARCHITECTURE.md` | Active, referenced by 3 workbench docs |

## 4. Active Prompts (12)

| Document | Status |
|---|---|
| `agents/community-intelligence/PROMPT.md` | Active |
| `agents/content-production/PROMPT.md` | Active |
| `agents/editorial-builder/PROMPT.md` | Active (updated today) |
| `agents/editorial-qa/PROMPT.md` | Active |
| `agents/opportunity-discovery-agent/PROMPT.md` | Active |
| `agents/opportunity-research-agent/PROMPT.md` | Active |
| `agents/publisher/PROMPT.md` | Active |
| `agents/research-compiler/PROMPT.md` | Active |
| `agents/research-factory/PROMPT.md` | Active |
| `docs/BLOG-MASTER-PROMPT.md` | Active |
| `docs/PRODUCTION-MASTER-PROMPT.md` | Active |
| `docs/ROUNDUP-MASTER-PROMPT.md` | Orphan — never referenced |

## 5. Active Templates (5)

| Document | Status |
|---|---|
| `agents/editorial-builder/OUTPUT-TEMPLATE.md` | Active (updated today) |
| `agents/opportunity-discovery-agent/OUTPUT-TEMPLATE.md` | Active |
| `agents/opportunity-research-agent/OUTPUT-TEMPLATE.md` | Active |
| `agents/pipeline-runner/OUTPUT-TEMPLATE.md` | Active |
| `agents/research-compiler/OUTPUT-TEMPLATE.md` | Active |
| `docs/reports/PIPELINE-READINESS-REPORT-TEMPLATE.md` | Duplicated in dist/ and public/ |

## 6. Duplicate Documents

| Document | Locations |
|---|---|
| `PIPELINE-READINESS-REPORT-TEMPLATE.md` | `docs/reports/`, `dist/client/docs/reports/`, `public/docs/reports/` |
| Research briefs | `docs/research/` (10 files) + `agents/opportunity-research-agent/briefs/` (21 files) |

## 7. Orphan Documents (35 never referenced)

| Directory | Files | Status |
|---|---|---|
| `docs/workbench/` | 13 | All orphans — stale workbench archives |
| `docs/implementation/` | 12 | All orphans — stale implementation docs |
| `docs/architecture/` | 4 of 5 | Orphans (DISCOVERY-SEARCH-STRATEGY, PROJECT-SNAPSHOT, SCRAPE-CREATORS, VIDEO-ANALYSIS) |
| `docs/testing/` | 1 | Orphan |
| `docs/audits/` | 1 | Orphan |
| `docs/` root | 4 | Orphans (AI-TOOLS-EDITORIAL-ROADMAP, COMMUNITY-INTELLIGENCE-SPEC, ROUNDUP-MASTER-PROMPT, ROUNDUP-PRODUCTION-WORKFLOW) |

## 8. Documents Referenced by Code (14)

`AGENT-CONTRACT`, `AI-EDITORIAL-OPERATING-SYSTEM`, `BLOG-MASTER-SPEC`, `COMMUNITY-INTELLIGENCE`, `CONTENT-REGISTRY`, `EDITORIAL-OBJECT-MODEL`, `GOLD-MASTER-SPEC`, `HEAVY-ASSET-LIBRARY`, `PIPELINE-ARCHITECTURE`, `PIPELINE-HANDOFF-STANDARD`, `WHY`, `BLOG-MASTER-PROMPT`, `PRODUCTION-MASTER-PROMPT`, `ROUNDUP-GOLD-MASTER-SPEC`

## 9. Documents Never Referenced (35)

All 13 `docs/workbench/` files, all 12 `docs/implementation/` files, 4 of 5 `docs/architecture/` files, `docs/testing/SCRAPE-CREATORS-POC.md`, `docs/audits/LEVNYTT-SKILL-V2-AUDIT.md`, and 4 `docs/` root files.

---

## 10. Classification of All 35 Orphan Documents

### docs/ root orphans (4)

| # | Document | Classification | Reason |
|---|---|---|---|
| 1 | `AI-TOOLS-EDITORIAL-ROADMAP.md` | Archive Candidate | Pillar strategy doc. Useful for historical context but not referenced by any code. |
| 2 | `COMMUNITY-INTELLIGENCE-SPEC.md` | Archive Candidate | Spec for CI module. Superseded by agent PROMPT.md files. |
| 3 | `ROUNDUP-MASTER-PROMPT.md` | Safe to Delete | Orphan — no code references it. Roundup workflow exists in agent prompts. |
| 4 | `ROUNDUP-PRODUCTION-WORKFLOW.md` | Safe to Delete | Orphan — no code references it. |

### docs/architecture/ orphans (4)

| # | Document | Classification | Reason |
|---|---|---|---|
| 5 | `DISCOVERY-SEARCH-STRATEGY.md` | Safe to Delete | Strategy doc marked "no implementation". Never implemented. |
| 6 | `PROJECT-SNAPSHOT-2026-07-07.md` | Safe to Delete | Point-in-time snapshot. Superseded by current state. |
| 7 | `SCRAPE-CREATORS-DISCOVERY-ANALYSIS.md` | Safe to Delete | Analysis doc marked "no implementation approved". Never implemented. |
| 8 | `VIDEO-ANALYSIS-CONTENT-PRODUCTION-REVIEW.md` | Safe to Delete | Review doc marked "no implementation approved". Never implemented. |

### docs/implementation/ orphans (12)

| # | Document | Classification | Reason |
|---|---|---|---|
| 9 | `COMMUNITY-INTELLIGENCE-PROCESSOR.md` | Archive Candidate | Implementation doc. Useful for understanding CI architecture. |
| 10 | `COMMUNITY-INTELLIGENCE-REPORT.md` | Archive Candidate | Implementation doc. Useful for understanding CI output format. |
| 11 | `CONTENT-PRODUCTION.md` | Archive Candidate | Implementation doc. Useful for understanding content pipeline. |
| 12 | `DISCOVERY-QUERY-LIBRARY.md` | Archive Candidate | Implementation doc. Useful for understanding query patterns. |
| 13 | `DISCOVERY-RUNNER.md` | Archive Candidate | Implementation doc. Useful for understanding discovery flow. |
| 14 | `EDITORIAL-INTELLIGENCE-PROCESSOR.md` | Archive Candidate | Implementation doc. Useful for understanding EI architecture. |
| 15 | `EDITORIAL-QA.md` | Archive Candidate | Implementation doc. Useful for understanding QA process. |
| 16 | `OPPORTUNITY-BRIEF-GENERATOR.md` | Archive Candidate | Implementation doc. Useful for understanding brief generation. |
| 17 | `PIPELINE-COMPLETION-REPORT.md` | Archive Candidate | Historical report. Documents first pipeline run. |
| 18 | `PUBLISHING-PACKAGE.md` | Archive Candidate | Implementation doc. Useful for understanding publishing. |
| 19 | `RESEARCH-FACTORY.md` | Archive Candidate | Implementation doc. Useful for understanding research pipeline. |
| 20 | `RESEARCH-REPORT-GENERATOR.md` | Archive Candidate | Implementation doc. Useful for understanding research output. |

### docs/workbench/ orphans (13)

| # | Document | Classification | Reason |
|---|---|---|---|
| 21 | `ARCHITECTURE-CONSOLIDATION-REPORT.md` | Archive Candidate | Architecture analysis. Useful for understanding design decisions. |
| 22 | `architecture-finalization-report.md` | Archive Candidate | Architecture finalization. Documents completed work. |
| 23 | `architecture-intent-audit.md` | Archive Candidate | Architecture audit. Useful for understanding intent vs reality. |
| 24 | `AUTONOMOUS-PRODUCTION-SPEC.md` | Archive Candidate | Autonomous mode spec. Useful for understanding operating modes. |
| 25 | `editorial-builder-alignment-report.md` | Archive Candidate | Alignment report. Documents ADR-001 compliance. |
| 26 | `editorial-builder-inspection.md` | Archive Candidate | Inspection report. Documents builder state. |
| 27 | `editorial-builder-mvp-validation.md` | Archive Candidate | MVP validation. Documents validation results. |
| 28 | `MISSION-CONTROL-AUDIT.md` | Archive Candidate | Audit report. Documents Mission Control state. |
| 29 | `MISSION-CONTROL-IMPLEMENTATION-ROADMAP.md` | Archive Candidate | Roadmap. Documents implementation plan. |
| 30 | `pipeline-integration-mvp.md` | Archive Candidate | MVP validation. Documents integration state. |
| 31 | `pipeline-orchestrator-architecture-review.md` | Archive Candidate | Architecture review. Documents orchestrator design. |
| 32 | `pipeline-orchestrator-design-review.md` | Archive Candidate | Design review. Documents design decisions. |
| 33 | `production-pipeline-audit.md` | Archive Candidate | Audit report. Documents pipeline state. |

### Other orphans (2)

| # | Document | Classification | Reason |
|---|---|---|---|
| 34 | `docs/testing/SCRAPE-CREATORS-POC.md` | Safe to Delete | POC doc. Experimental, never implemented. |
| 35 | `docs/audits/LEVNYTT-SKILL-V2-AUDIT.md` | Safe to Delete | Audit doc marked "IN PROGRESS". Never completed. |

---

## 11. Deletion Plan

### Safe to Delete (9 files)

| File | Reason |
|---|---|
| `docs/ROUNDUP-MASTER-PROMPT.md` | Orphan, no references |
| `docs/ROUNDUP-PRODUCTION-WORKFLOW.md` | Orphan, no references |
| `docs/architecture/DISCOVERY-SEARCH-STRATEGY.md` | Never implemented |
| `docs/architecture/PROJECT-SNAPSHOT-2026-07-07.md` | Superseded by current state |
| `docs/architecture/SCRAPE-CREATORS-DISCOVERY-ANALYSIS.md` | Never implemented |
| `docs/architecture/VIDEO-ANALYSIS-CONTENT-PRODUCTION-REVIEW.md` | Never implemented |
| `docs/testing/SCRAPE-CREATORS-POC.md` | Experimental, never implemented |
| `docs/audits/LEVNYTT-SKILL-V2-AUDIT.md` | Never completed |
| `docs/workbench/README.md` | Workbench index, not needed if workbench is archived |

### Archive Candidate — Move to `docs/archive/` (24 files)

| Directory | Files | Reason |
|---|---|---|
| `docs/` root | `AI-TOOLS-EDITORIAL-ROADMAP.md`, `COMMUNITY-INTELLIGENCE-SPEC.md` | Useful historical context |
| `docs/architecture/` | (0 files — all safe to delete) | — |
| `docs/implementation/` | All 12 files | Implementation docs, useful for architecture understanding |
| `docs/workbench/` | All 12 non-README files | Workbench analysis, useful for design history |

### Duplicate — Remove (2 files)

| File | Reason |
|---|---|
| `dist/client/docs/reports/PIPELINE-READINESS-REPORT-TEMPLATE.md` | Build artifact duplicate |
| `public/docs/reports/PIPELINE-READINESS-REPORT-TEMPLATE.md` | Public duplicate of docs/ version |

### Summary

| Action | Count |
|---|---|
| Safe to Delete | 9 |
| Archive to `docs/archive/` | 24 |
| Remove duplicates | 2 |
| **Total** | **35** |

### Execution Order

1. Create `docs/archive/` directory
2. Move 24 archive candidates to `docs/archive/`
3. Delete 9 safe-to-delete files
4. Remove 2 duplicate files from `dist/` and `public/`
5. Remove empty directories (`docs/architecture/`, `docs/implementation/`, `docs/workbench/`, `docs/testing/`, `docs/audits/`)

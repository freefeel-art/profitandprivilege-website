# Pipeline Readiness Report Template

**Date:** {{REPORT_DATE}}
**Repository root:** {{REPOSITORY_ROOT}}
**Source of Truth:** Repository files only — no assumptions, no external references, no vendor claims
**Architecture Freeze:** {{ACTIVE_OR_INACTIVE}}
**Scope:** Audit of {{N}} documented pipeline stages against repository evidence

---

## Executive Summary

{{1–2 paragraph summary covering overall status, key gaps, and highest priority action}}

---

## Repository Topology

```
{{Directory structure overview — list all agent directories, pipeline docs, src structure, reports}}
```

---

## Stage-by-Stage Audit

### Stage {{N}}: {{Stage Name}}

| Aspect | Detail |
|--------|--------|
| **Status** | {{Complete / Partial / Placeholder / Missing}} |
| **Evidence** | {{File paths, agent contents, reports produced, output schemas found}} |
| **Agent(s)** | {{List of agents implementing this stage}} |
| **Connected to pipeline** | {{Yes/No/Partial — describe handoff contracts, artifact flow}} |
| **Gaps** | {{What is missing, incomplete, or disconnected}} |
| **Next step** | {{Single actionable next step}} |

*(Repeat for each pipeline stage)*

---

## Summary Table

| Stage | Status | Evidence | Next Action |
|-------|--------|----------|-------------|
| {{Stage 1}} | {{Status}} | {{Key evidence}} | {{Next action}} |
| {{Stage 2}} | {{Status}} | {{Key evidence}} | {{Next action}} |
| ... | ... | ... | ... |

---

## Special Focus: {{Presentation / Component Layer Name}}

### Extracted Components

| Component | File | Purpose |
|-----------|------|---------|
| {{Name}} | {{Path}} | {{Description}} |

### Pages Using {{Component System}} (X of Y)

```
{{List of pages using the new component system}}
```

### Pages Still Hardcoded (X of Y)

```
{{List of pages still using hardcoded presentation}}
```

### Gaps

{{Description of what remains to be migrated}}

---

## Highest Priority Implementation Task

{{Single recommended next action with rationale}}

---

## Verifications Performed

| Check | Result |
|-------|--------|
| Build succeeds (N pages) | ✅/❌ |
| New article compiles without errors | ✅/❌ |
| Internal links resolve | ✅/❌ — {{list of paths checked}} |
| External links use correct attributes | ✅/❌ — {{list of paths checked}} |
| No inline `<style>` or `<script>` in generated articles | ✅/❌ |
| Components correctly imported per article type | ✅/❌ |

---

## Report Metadata

| Field | Value |
|-------|-------|
| Auditor | {{Name}} |
| Date | {{DATE}} |
| Repository | {{REPO_NAME}} |
| Architecture freeze | {{Active/Inactive}} |
| Files read | {{Count}} |
| Files modified during audit | {{List of files changed}} |

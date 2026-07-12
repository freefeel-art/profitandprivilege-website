# Workbench — Shared AI Workspace

**Location:** `docs/workbench/`

## Purpose

The workbench is a shared space for AI assistants and the Product Owner to store temporary inspection reports, audit findings, repository snapshots, pipeline investigations, architecture reviews, QA findings, and development notes.

## What belongs here

- **Inspection reports** — detailed examinations of implementation status (e.g., `editorial-builder-inspection.md`)
- **Audit reports** — compliance checks against specs, standards, and requirements
- **Repository snapshots** — point-in-time analysis of structure, content, and state
- **Pipeline investigations** — deep dives into agent pipeline stages and their readiness
- **Architecture reviews** — analysis of architectural decisions and their implementation
- **QA findings** — quality assurance observations found during reviews
- **Development notes** — temporary notes and planning documents

## What does NOT belong here

- Production documentation (specs, prompts, standards — keep in `docs/`)
- Agent implementation files (keep in `agents/`)
- Source code (keep in `src/`)
- Configuration files
- Any file that is part of the build or deployment pipeline

## Rules

- **Shared workspace.** Both AI assistants and the Product Owner may create and read files here.
- **Never overwrite** an existing report unless explicitly requested. Create new files with descriptive, unique filenames.
- **Temporary but persistent.** Files may be temporary in nature but should not be deleted automatically. Clean up manually when the information is no longer relevant.
- **Descriptive filenames.** Use clear, self-explanatory names (e.g., `editorial-builder-inspection.md`, `pipeline-stage-4-gap-analysis.md`).
- **Keep it organized.** Group related reports thematically. Archive or remove outdated content periodically.

## Version control

This directory is under version control and is shared across all workstations. Commit workbench documents when they represent a complete, useful analysis — not after every edit.

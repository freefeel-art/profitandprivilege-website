# Publishing Package — Implementation

**Date:** 2026-07-08
**Status:** Implemented

Prepares the final publishing-ready package from QA-approved content. No deployment. No publishing. Only package preparation.

**Input:** `research/output/content/{pillar}-content.json` + QA Report
**Output:** `research/output/publishing-packages/{pillar}-publishing-package.json`

## Package contents per article

- working_title, format, article_slug
- gold_master_template (which GM spec to use)
- sections with headings and word counts
- estimated_total_words
- qa_status
- pre_flight_checks (GM available, research complete, QA approved, sections structured, evidence available)

## Usage

```bash
python -m research.publishing_package.packager
```

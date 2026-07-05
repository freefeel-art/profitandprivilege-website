# Publishing Engine V1 — Specification

## 1. Purpose

This document specifies the operational requirements for the Publishing Engine V1. It defines inputs, outputs, stages, decision rules, and quality standards.

The engine operates as the ninth stage of the AI Editorial Operating System. Its sole function is to safely and deterministically publish QA-approved content. It does not perform research, edit content, or make editorial decisions.

## 2. Authority

This specification is subordinate to the following documents:

```
docs/WHY.md
docs/AI-EDITORIAL-OPERATING-SYSTEM.md
docs/AGENT-CONTRACT.md
docs/EDITORIAL-OBJECT-MODEL.md
    ↓
agents/editorial-qa/SPEC.md
    ↓
publishing/SPEC.md                          ← this document
    ↓
publishing/publish.js
```

If any conflict arises, the higher document wins.

## 3. Inputs

| Input | Format | Required | Description |
|-------|--------|----------|-------------|
| Editorial QA Report | Markdown | Yes | Must contain `READY FOR PUBLICATION` decision |
| Astro page | `.astro` file | Yes | The article file to publish |
| Publication metadata | Inline in article | Yes | Canonical URL, title, prerender flag |

### Input validation

Before any work begins, the engine must verify:

1. The Editorial QA Report exists and its decision is `READY FOR PUBLICATION`
2. The Astro page file exists at the expected path
3. `astro build` succeeds (structural validation)
4. The article's frontmatter contains required metadata (`canonical URL`, `prerender = true`)
5. The slug does not conflict with any existing page

If any input is missing or invalid, the engine must stop with `PUBLICATION BLOCKED`.

## 4. Stages

### Stage 1 — Publication Validation

| Check | Method | Pass Condition |
|-------|--------|----------------|
| QA status | Parse QA report for decision line | Decision is `READY FOR PUBLICATION` |
| File exists | Check filesystem | `.astro` file exists |
| Build passes | Run `astro build` | Exit code 0 |
| Metadata present | Parse `.astro` frontmatter | `prerender = true`, canonical URL present |
| Slug uniqueness | Check against existing built pages | No duplicate route |

### Stage 2 — Git

| Action | Command | Notes |
|--------|---------|-------|
| Stage files | `git add <article-file> <qa-report> <publication-report>` | Only intended files |
| Commit | `git commit -m "publish: <article-title>"` | Standard commit message |
| Branch validation | `git rev-parse --abbrev-ref HEAD` | Confirm on main branch |

### Stage 3 — Build

| Action | Command | Notes |
|--------|---------|-------|
| Production build | `npx astro build` | Abort on any error |
| Output verification | Check `dist/` exists | Confirm build produced output |

### Stage 4 — Deploy

| Action | Command | Notes |
|--------|---------|-------|
| Deploy to production | `netlify deploy --prod --dir=dist` | Uses existing Netlify site configuration |
| Capture deploy URL | Parse deploy output | Used for post-deployment validation |

### Stage 5 — Post-Deployment Validation

| Check | Method | Pass Condition |
|-------|--------|----------------|
| Page reachable | HTTP GET article URL | Status 200 |
| Canonical URL | Parse `<link rel="canonical">` | Matches expected canonical |
| Sitemap updated | Check `dist/sitemap-index.xml` | Article URL present in sitemap |

### Stage 6 — Search Engine Submission

| Action | Details |
|--------|---------|
| Prepare sitemap ping URL | `https://www.google.com/ping?sitemap=<sitemap-url>` |
| Log submission | Record that indexing was queued (not immediate) |

### Stage 7 — Publication Report

Generate a markdown report at `reports/publication/<slug>-PUB-REPORT-<timestamp>.md`

## 5. Outputs

| Output | Format | Location |
|--------|--------|----------|
| Publication Report | Markdown | `reports/publication/<slug>-PUB-REPORT-<timestamp>.md` |

### Report structure

```markdown
# Publication Report

**Article:** <title>
**Slug:** <slug>
**Opportunity:** <OPP-NNN>
**QA Report:** <path>
**Publication timestamp:** <ISO datetime>
**Commit hash:** <sha>
**Build result:** PASS/FAIL
**Deployment result:** PASS/FAIL
**Deploy URL:** <url>
**Validation result:** PASS/FAIL
**Sitemap status:** UPDATED/NOT FOUND
**Indexing status:** QUEUED

## Stage Results

### Stage 1 — Publication Validation
Result: PASS/FAIL
Details: ...

### Stage 2 — Git
Result: PASS/FAIL
Details: ...

[etc for all 7 stages]

## Final Decision

PUBLISHED / PUBLICATION BLOCKED
```

## 6. Decision Rules

| Decision | Condition |
|----------|-----------|
| PUBLISHED | All 7 stages completed successfully |
| PUBLICATION BLOCKED | Any stage fails. Report includes precise reason and stage. |

## 7. Error Handling

| Condition | Action |
|-----------|--------|
| QA report missing | Stop. Report missing file. |
| QA status not READY FOR PUBLICATION | Stop. Report current QA status. |
| Astro file missing | Stop. Report missing file. |
| Build fails | Stop. Report build error. |
| Deploy fails | Stop. Report deploy error. |
| Post-deploy validation fails | Report validation failure. Article considered published but requires manual verification. |

## 8. Security

- Never deploy without QA approval
- Only stage intended files in git commits
- Use existing deployment credentials (Netlify), never embed secrets in scripts
- Publication reports are generated locally, not pushed to any external service

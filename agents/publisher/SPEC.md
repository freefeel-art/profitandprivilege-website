# Publisher Agent — Specification

## 1. Purpose

This document specifies the operational requirements for the Publisher Agent V1. It defines inputs, outputs, workflow, constraints, and quality standards.

The agent operates as Stage 5 of the two-track production pipeline and corresponds to Stage 9 (Publishing) of the AI Editorial Operating System. Its sole function is to execute the publication workflow for a QA-approved article.

It does not modify content, approve publication, or make editorial decisions.

---

## 2. Authority

```
docs/WHY.md
docs/AI-EDITORIAL-OPERATING-SYSTEM.md
docs/AGENT-CONTRACT.md
    ↓
agents/publisher/SPEC.md       ← this document
    ↓
agents/publisher/PROMPT.md
    ↓
publishing/publish.cjs         ← automated publication script
```

If any conflict arises, the higher document wins.

---

## 3. Inputs

| Input | Format | Required | Description |
|-------|--------|----------|-------------|
| QA-approved article | `.astro` file | Yes | Complete article file that passed Editorial QA |
| Article slug | String | Yes | The URL slug for the article |
| Article section | String | Yes | Section subdirectory (reviews, blog, roundups, or root) |

---

## 4. Output

| Output | Format | Description |
|--------|--------|-------------|
| Git commit | Git commit | Standardized commit message with article reference |
| Git push | Remote push | Push to production branch for deployment |
| Publication log | Markdown | Entry in publication records |
| Content registry update | Commit | Update to `docs/CONTENT-REGISTRY.md` |

---

## 5. Workflow

### Step 1: Stage article file
```
git add {article_path}
```

### Step 2: Stage registry update (if applicable)
```
git add docs/CONTENT-REGISTRY.md
```

### Step 3: Commit
```
git commit -m "publish: {article_slug} — {article_title}"
```

### Step 4: Build verification
```
npx astro build
```
Verify build succeeds with zero errors.

### Step 5: Push
```
git push
```

### Step 6: Post-publish verification
- Verify HTTP 200 on the published URL
- Verify canonical URL resolves correctly

---

## 6. Constraints

1. Never push without a successful build.
2. Never push without operator confirmation (human approval required).
3. Never modify article content after QA approval.
4. Never publish pages that have not passed QA.
5. The commit message must follow the standardized format.

---

## 7. Next Stage

**Stage:** Performance Intelligence (Stage 10 of AI Editorial OS)

**Handoff includes:**
- Published article URL
- Commit SHA
- Content registry update confirmation

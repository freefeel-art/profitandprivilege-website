# Publishing Engine V1 — Workflow Reference

## Complete Publication Sequence

```
┌─────────────────────────────────────────────────────────────┐
│  Stage 1: Publication Validation                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────┐   │
│  │ QA       │→│ File     │→│ Build    │→│ Metadata  │   │
│  │ Approved │  │ Exists   │  │ Passes   │  │ Complete  │   │
│  └──────────┘  └──────────┘  └──────────┘  └───────────┘   │
│                          ↓                                  │
│                    ┌──────────────┐                         │
│                    │ Slug Unique  │                         │
│                    └──────────────┘                         │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  Stage 2: Git                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐          │
│  │ git add  │→│ git      │→│ Branch Confirm   │          │
│  │          │  │ commit   │  │ (main)           │          │
│  └──────────┘  └──────────┘  └──────────────────┘          │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  Stage 3: Build                                             │
│  ┌────────────────┐  ┌──────────────────────────┐           │
│  │ astro build    │→│ Verify dist/ output      │           │
│  └────────────────┘  └──────────────────────────┘           │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  Stage 4: Deploy                                            │
│  ┌──────────────────────────────┐                           │
│  │ netlify deploy --prod       │                           │
│  │ --dir=dist                  │                           │
│  └──────────────────────────────┘                           │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  Stage 5: Post-Deployment Validation                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────┐   │
│  │ HTTP 200 │→│ Canonical │→│ Metadata │→│ Sitemap   │   │
│  │ Check    │  │ Check    │  │ Check    │  │ Check     │   │
│  └──────────┘  └──────────┘  └──────────┘  └───────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  Stage 6: Search Engine Submission                          │
│  ┌──────────────────────────────┐                           │
│  │ Prepare sitemap ping URL    │                           │
│  │ Log: indexing QUEUED        │                           │
│  └──────────────────────────────┘                           │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  Stage 7: Publication Report                                │
│  ┌──────────────────────────────┐                           │
│  │ Generate markdown report    │                           │
│  │ → reports/publication/      │                           │
│  └──────────────────────────────┘                           │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
                    ┌──────────┐
                    │ PUBLISHED│
                    └──────────┘
```

## Command Reference

### Single article
```bash
node publishing/publish.js <article-slug>
```

### Multiple articles
```bash
node publishing/publish.js <slug-1> <slug-2> <slug-3>
```

### Required environment
- Current directory must be project root
- Netlify CLI must be authenticated (`netlify status` should succeed)
- Git must be configured with user.name and user.email

## Article Slug Mapping

| Slug | File | OPP |
|------|------|-----|
| `is-olsp-academy-an-mlm` | `src/pages/is-olsp-academy-an-mlm.astro` | OPP-001 |
| `fastbots-chatbot-wrong-answers` | `src/pages/fastbots-chatbot-wrong-answers.astro` | OPP-002 |
| `does-google-penalize-ai-content` | `src/pages/does-google-penalize-ai-content.astro` | OPP-003 |

## Rollback

If a publication needs to be rolled back:

```bash
git revert <commit-hash>
git push origin main
netlify deploy --prod --dir=dist
```

This reverts both the git state and the live site.

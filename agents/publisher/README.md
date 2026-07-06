# Publisher Agent — V1

## Pipeline Position

Stage 5 of the two-track production pipeline — shared by both Heavy and Light pipelines. This is the final stage before the article goes live.

## Purpose

Execute the publication workflow for a QA-approved article: stage, build-verify, commit, push, and verify.

## Responsibilities

- Stage article file(s) for commit
- Verify build succeeds before pushing
- Create standardized git commit
- Push to production branch
- Verify post-publish (HTTP 200, canonical URL)

## Non-Responsibilities

- Modifying article content after QA approval
- Approving publication (human decision)
- Publishing pages that have not passed QA

## Dependencies

- QA-approved article file
- `npx astro build` command
- Git access to production branch
- `publishing/publish.cjs` for extended automation

## Output

- Git commit with standardized message
- Push to production
- Published article URL
- Content registry update

## Next Stage

Performance Intelligence — collect data and feed back to Community Intelligence.

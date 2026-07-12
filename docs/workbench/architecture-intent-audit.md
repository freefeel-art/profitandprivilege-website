# Architecture Intent Investigation

## What was the intended future architecture of this repository?

---

## 1. Was the Agent Pipeline intended to replace the Manual Builder?

**Yes — the committed repository evidence is unambiguous.**

- `de1d240` (2026-07-03): "feat: add AI Editorial Operating System agent architecture"
  - Created the `/agents` directory with a 5-stage pipeline structure
  - `agents/editorial-builder/PLACEHOLDER.md`: "**Status:** Not yet designed — current Builder V1 (manual workflow) will **migrate here**"
  - `agents/editorial-builder/PLACEHOLDER.md` — Notes section: "The current manual Builder workflow (documented in `docs/PRODUCTION-MASTER-PROMPT.md` and `docs/GOLD-MASTER-SPEC.md`) will be **migrated into this agent** when the upstream pipeline stages are stable"

- `docs/PIPELINE-ARCHITECTURE.md` (2026-07-04): Shows Editorial Builder as Stage 3 with status "Placeholder — receives either an Opportunity Brief (Light) or an optional Knowledge Asset citation (Heavy)"

- `docs/PIPELINE-HANDOFF-STANDARD.md` (2026-07-04): Defines the Writer stage (Editorial Builder) as producing an `.astro` file, with a handoff to QA.

The word "migrate" is used intentionally — the manual workflow would be converted into an automated agent, not replaced by a different system.

---

## 2. Was the Manual Builder intended to remain permanently?

**No — the manual Builder was intended to be retired after migration.**

Three pieces of evidence:

1. **Placeholder status.** The Editorial Builder agent folder was created as a placeholder specifically "for migration" of the manual Builder. If both were intended to coexist, there would be no need to create an agent folder.

2. **Pipeline Architecture.** `docs/PIPELINE-ARCHITECTURE.md` shows the Editorial Builder as the sole Writer stage. There is no parallel "manual track" in the documented pipeline — all production routes through the agent stages.

3. **Opportunity Discovery intent.** `agents/opportunity-discovery-agent/SPEC.md` (v0.6) states the pipeline was being converted from "keyword-first" to "opportunity-first" — implying automation of the entire flow from discovery to publication. Manual keyword selection was the legacy approach.

However, the production prompts (`docs/PRODUCTION-MASTER-PROMPT.md`, `BLOG-MASTER-PROMPT.md`, `ROUNDUP-MASTER-PROMPT.md`) were never marked as deprecated. They remain the sole active production tools. This creates an ambiguity: the prompts were intended to be replaced but were never phased out because the replacement was never built.

---

## 3. Was a migration started but left incomplete?

**Yes — multiple migrations were started. None completed.**

### Migration 1: Shared components (ArticleNavigation) — started and reverted

| Commit | Action |
|---|---|
| `683fe8b` (Jun 26) | Created `src/components/ArticleNavigation.astro` — a shared component |
| `8c5ae16` (Jun 26) | Added `import ArticleNavigation` to all 7 OLSP review pages |
| `4b54edd` (Jun 26) | **Reverted.** Restored all review pages to pre-import state. |

The shared-component approach was attempted, rolled out to production, then rolled back within ~1 hour. The component and data file were retained in the repository but no article page uses them. This is the *only attempted migration that touched production code*.

### Migration 2: Gold Master standardization — completed

| Commit | Action |
|---|---|
| `bac24d0` (Jul 3) | Migrated all 14 production pages to Gold Master V1 standard |

This migration **succeeded** — it standardized 14 pages to the self-contained Gold Master format (3 CTA cards, pill-list sources, site footer). It was not an architectural change; it was a formatting unification.

### Migration 3: Agent pipeline — started (documentation), incomplete (implementation)

| Stage | Created | Status |
|---|---|---|
| Stage 0: Discovery | `48db234` (Jul 3) — SPEC, PROMPT, OUTPUT-TEMPLATE, README | **Documented.** Not yet run as a standalone agent. |
| Stage 1L: ORA (Light Research) | `de1d240` (Jul 3) — SPEC, PROMPT, OUTPUT-TEMPLATE, README | **Documented and manually usable.** Briefs produced manually by copy-pasting prompts. Not automated. |
| Stage 2H: Research Compiler | `de1d240` → `4dacee8` (Jul 3→4) — placeholder replaced with SPEC, PROMPT, README, OUTPUT-TEMPLATE | **Documented.** Never run as a standalone agent. |
| Stage 3: Editorial Builder | `de1d240` (Jul 3) — PLACEHOLDER.md | **Not designed.** PROMPT.md v2.1 exists as an untracked draft. |
| Stage 4: Editorial QA | `de1d240` (Jul 3) — PLACEHOLDER.md | **Not designed.** |
| Stage 5: Publisher | `de1d240` (Jul 3) — PLACEHOLDER.md | **Not designed.** |

Every agent stage beyond ORA is documented but unimplemented. The migration from manual to automated was started (documentation) but never reached production code.

---

## 4. Which documents describe the target architecture?

Four documents, in order of authority:

### Primary: `docs/GOLD-MASTER-SPEC.md` (598 lines)
**Status:** Production standard
**Architecture:** Self-contained `.astro` files. "Every article is a standalone `.astro` file... no shared layout imports, no component imports, and no framework components."
**Authoritative for:** What production files look like.

### Primary: `docs/BLOG-MASTER-SPEC.md` (257 lines)
**Status:** Production standard (blog variant)
**Architecture:** Same as Gold Master. "A single, fully self-contained `.astro` file. Frontmatter contains **only** `export const prerender = true;` — no other variables, no imports."
**Authoritative for:** Blog article structure and CTA placement (QuoteBanner + Standard CTA).

### Secondary: `docs/PIPELINE-ARCHITECTURE.md` (86 lines)
**Status:** Architectural design document
**Architecture:** 5-stage automated pipeline: Discovery → Research (ORA or Research Compiler) → Editorial Builder → Editorial QA → Publisher.
**Describes:** How the stages connect, not what they produce.

### Secondary: `agents/editorial-builder/PLACEHOLDER.md`
**Status:** Intent statement for Stage 3
**Architecture (committed version):** "A fully built `.astro` file placed in the correct `src/pages/` subdirectory, matching the Gold Master specification exactly."
**Authoritative for:** What the Editorial Builder was intended to produce — a complete self-contained Gold Master file.

### Divergent: `agents/editorial-builder/PROMPT.md` (untracked draft)
**Status:** Uncommitted exploration
**Architecture (draft version):** Component-based. Output is "the **body content only**" — a content block wrapped in `<OlspLayout>`, using shared imported components (`QuoteBanner`, `StandardCta`, `AuthorBox`, `ScoreBars`, etc.).
**Relationship to committed architecture:** **Conflicting.** Describes components that don't exist and an architecture that contradicts the Gold Master standard.

---

## 5. Which commits introduced that direction?

### Origin of the self-contained architecture
| Commit | Date | What it did |
|---|---|---|
| `12db228` | 2026-06-25 | Initial OLSP Content Engine |
| `7e3cb46` | 2026-06-25 | Add Gold Master spec for review pages |
| `b2330e9` | 2026-06-25 | docs: add production master prompt |

These established the self-contained `.astro` file architecture that continues today.

### Origin of the component experiment (abandoned)
| Commit | Date | What it did |
|---|---|---|
| `683fe8b` | 2026-06-26 | Add Gold Master article navigation component |
| `8c5ae16` | 2026-06-26 | Add ArticleNavigation to all OLSP review pages |
| `4b54edd` | 2026-06-26 | **Reverted** — restore to pre-ArticleNavigation baseline |

### Origin of the Agent Pipeline
| Commit | Date | What it did |
|---|---|---|
| `de1d240` | 2026-07-03 | **feat: add AI Editorial Operating System agent architecture** |
| `fc5022a` | 2026-07-03 | feat: upgrade Opportunity Research Agent to v1.1 |
| `48db234` | 2026-07-03 | docs: design Opportunity Discovery Agent |
| `4dacee8` | 2026-07-04 | **feat: split production into Heavy and Light pipelines** |
| `bcd13cb` | 2026-07-04 | feat: replace CTA cards with QuoteBanner + Standard CTA |

---

## 6. Which commits stopped or changed that direction?

### No explicit stop was committed.

The architectural direction was never formally halted or reversed. Instead, it was **paused by inaction**:

- After `4dacee8` (pipeline split, 2026-07-04), the next commits were all **content production** — 13 new articles using the manual prompts, not agent implementations.
- The last commit (`08fc82b`) was a content-registry update.
- `agents/editorial-builder/PROMPT.md` v2.1 was drafted but **never committed** — it exists as an untracked file, representing an architectural direction that was explored but never finalized or approved.

### Direction change via the untracked PROMPT.md v2.1

The untracked `agents/editorial-builder/PROMPT.md` v2.1 represents a **silent direction change** from the committed PLACEHOLDER.md:

| Aspect | Committed PLACEHOLDER.md | Untracked PROMPT.md v2.1 |
|---|---|---|
| Output | Complete self-contained `.astro` file | Content block wrapped in `<OlspLayout>` |
| Architecture | Self-contained (matches Gold Master) | Component-based (contradicts Gold Master Section 1) |
| Dependencies | None — produces standalone file | Requires `src/layouts/OlspLayout.astro` + 12+ shared components — none exist |
| Template reference | Gold Master spec (`docs/GOLD-MASTER-SPEC.md`) | OLSP Standard v2.1 layout system (does not exist) |
| Status | Committed, explicit "Not yet designed" | Untracked draft, no status |

This direction change was never committed, never merged, and never reconciled with the Gold Master standard.

---

## Timeline of Architectural Evolution

```
2026-06-25 ──── Initial project setup
                 │
                 ├── 12db228: Initial OLSP Content Engine
                 ├── 7e3cb46: Gold Master spec — self-contained .astro files
                 └── b2330e9: Production Master Prompt (manual workflow)
                 │
                 ▼
     [Production: Manual prompt → self-contained .astro files]
     [All 8 OLSP Ecosystem articles published this way]
                 │
2026-06-26 ──── First component experiment
                 │
                 ├── 683fe8b: ArticleNavigation component created
                 ├── 8c5ae16: Added to all 7 review pages
                 └── 4b54edd: ★ REVERTED — back to self-contained files
                 │
                 ▼
     [Lesson learned: shared components cause issues, revert to self-contained]
                 │
2026-07-03 ──── Standardization + Agent architecture
                 │
                 ├── bac24d0: Gold Master V1 applied to all 14 pages
                 ├── de1d240: ★ AI Editorial Operating System introduced
                 │   ├── ORA: fully specified
                 │   ├── Research Compiler: placeholder
                 │   ├── Editorial Builder: placeholder (migration target)
                 │   ├── Editorial QA: placeholder
                 │   └── Publisher: placeholder
                 ├── fc5022a: ORA v1.1
                 ├── 48db234: Opportunity Discovery Agent designed
                 └── 23c85ae: Blog spec/prompt added
                 │
                 ▼
     [Two tracks: production continues manually; agent pipeline documented]
                 │
2026-07-04 ──── Pipeline split
                 │
                 ├── 4dacee8: ★ Heavy/Light pipeline split
                 │   ├── Research Compiler formalized (SPEC, README, PROMPT)
                 │   ├── PIPELINE-ARCHITECTURE.md created
                 │   └── HEAVY-ASSET-LIBRARY.md created
                 ├── bcd13cb: QuoteBanner + Standard CTA (blog spec)
                 └── 11714d9:  9 Light Pipeline articles published
                 │
                 ▼
     [Production: manual prompts, 13 more articles]
     [Documentation: full pipeline design exists]
     [Implementation gap: no agent beyond ORA is operational]
                 │
Post-commit ──── Divergent draft
                 │
                 └── (untracked) Editorial Builder PROMPT.md v2.1
                     └── Component-based architecture (uncommitted, diverges from committed spec)
                 │
                 ▼
     === PRESENT STATE ===
     Production:   Manual prompt → self-contained .astro files
     Committed:    Gold Master self-contained architecture
     Uncommitted:  Component-based architecture (draft)
```

---

## 7. Current Production vs Planned Architecture vs Completed Migration vs Incomplete Migration vs Abandoned

### Current Production
- **Process:** Human copies prompt from `docs/*-MASTER-PROMPT.md`, pastes into Claude with research, commits generated `.astro` file.
- **Output:** Self-contained `.astro` files with inline CSS/JS, no imports (defined by `docs/GOLD-MASTER-SPEC.md`).
- **30 pages published** using this method.

### Planned Architecture (committed)
- **Process:** Automated 5-stage pipeline: Discovery → Research → Writer → QA → Publish.
- **Output (original intent):** Complete self-contained `.astro` files matching the Gold Master (defined by `agents/editorial-builder/PLACEHOLDER.md`).
- **Components:** No shared components. Same architecture as production.
- **Documented in:** `docs/PIPELINE-ARCHITECTURE.md`, `agents/*/SPEC.md`.

### Planned Architecture (uncommitted draft)
- **Process:** Same automated 5-stage pipeline.
- **Output (draft divergence):** Content blocks wrapped in `<OlspLayout>` with imported shared components.
- **Components:** Requires `OlspLayout`, `QuoteBanner`, `StandardCta`, `AuthorBox`, `ScoreBars`, `Quiz`, `ComparisonTable`, `ProsCons`, `SvgDiagram`, `VideoEmbed` — none exist.
- **Documented in:** `agents/editorial-builder/PROMPT.md` (untracked).

### Completed Migrations
- **Gold Master V1 standardization** (`bac24d0`): All pages unified to the same self-contained template format.

### Incomplete Migrations
- **Agent pipeline implementation:** All stages beyond ORA are documented but not built.
- **Editorial Builder specification:** PLACEHOLDER.md exists; PROMPT.md drafted but uncommitted and architecturally divergent.
- **Research Compiler operationalization:** Fully specified (SPEC, README, PROMPT, OUTPUT-TEMPLATE) but never run as a standalone agent.

### Abandoned Ideas
- **Shared `ArticleNavigation` component on review pages** (2026-06-26): Created, deployed, reverted within ~1 hour. The component file remains in `src/components/` but is unused by any page.
- **`src/layouts/Layout.astro`:** Created as a default Astro layout, used only by `index.astro` and `authors/jarmo-halonen.astro`. Never used by any article page.

---

## 8. If development continues today, what architecture should implementation follow?

### The committed architecture is the Gold Master self-contained file standard.

All evidence points to this conclusion:

1. **The Gold Master spec** (`docs/GOLD-MASTER-SPEC.md` § 1, § 18 Rule 1) explicitly mandates self-contained files with no shared components. It is the production standard.

2. **The BLOG-MASTER-SPEC.md** (§ 1) explicitly follows the same rule.

3. **The original Editorial Builder PLACEHOLDER.md** (committed) states its output is "a complete, Gold Master-compliant Astro page" — meaning self-contained, matching the existing spec.

4. **The ArticleNavigation experiment** that attempted shared components was reverted within hours, indicating a deliberate architectural decision against shared components.

5. **The untracked PROMPT.md v2.1** that describes a component-based architecture was never committed, never approved, and conflicts with every committed specification.

### The Editorial Builder agent should produce the same self-contained files the manual Builder produces today.

The migration plan committed in `de1d240` states: "The current manual Builder workflow (documented in `docs/PRODUCTION-MASTER-PROMPT.md` and `docs/GOLD-MASTER-SPEC.md`) will be migrated into this agent." This means:

- The agent prompt should describe producing **complete self-contained `.astro` files** — not content blocks.
- The agent should reference `docs/GOLD-MASTER-SPEC.md` / `BLOG-MASTER-SPEC.md` / `ROUNDUP-GOLD-MASTER-SPEC.md` as its structural templates.
- The agent should NOT reference `OlspLayout` or any shared component system that doesn't exist.

### The untracked Editorial Builder PROMPT.md v2.1 requires resolution.

The PROMPT.md v2.1 contradicts the committed architecture in two ways:
1. It describes a component-based output (`OlspLayout` + shared components) that doesn't exist
2. It eliminates the self-contained file structure that the Gold Master requires

Before implementation continues on the Editorial Builder, this conflict must be resolved by either:
- **Revising the prompt** to match the committed Gold Master self-contained architecture, OR
- **Updating the Gold Master spec** to the component-based architecture AND building all required components

The committed evidence favors the first option (maintain self-contained files), but the decision belongs to the Product Owner.

---

Architecture Intent Investigation Complete

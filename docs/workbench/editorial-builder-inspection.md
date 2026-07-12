# Editorial Builder Inspection

## Repository information

| Field | Value |
|---|---|
| Current branch | `main` |
| Current commit | `08fc82b26563c1664d7b6f7a5d2c7fe70406c1c9` |
| Upstream | `origin/main` — up to date |
| Repository status | Clean working tree; 3 untracked items (`.mimocode/`, `OpenMontage/`, `agents/editorial-builder/PROMPT.md`) |
| All published pages | 30 (14 reviews, 13 blog, 1 roundup, 2 infrastructure) |

## Pipeline status

Source: `docs/PIPELINE-ARCHITECTURE.md`

| Stage | Pipeline | Agent folder | Status |
|---|---|---|---|
| 0. Discovery + classification | Both | `agents/opportunity-discovery-agent/` | **Production-ready** — implemented and operational |
| 1L. Light Research | Light | `agents/opportunity-research-agent/` (ORA) | **Production-ready** — scoped to Light pipeline only |
| 2H. Research Compiler | Heavy | `agents/research-compiler/` | **Formalized v1.0** — SPEC, README, PROMPT, OUTPUT-TEMPLATE all committed; not yet run as a standalone agent |
| 3. Writer / Editorial Builder | Both | `agents/editorial-builder/` | **Placeholder** — PROMPT.md drafted but untracked |
| 4. Editorial QA | Both | `agents/editorial-qa/` | **Placeholder** — only PLACEHOLDER.md exists |
| 5. Publisher | Both | `agents/publisher/` | **Placeholder** — only PLACEHOLDER.md exists |

### Production-ready stages
- Stage 0 (Opportunity Discovery Agent)
- Stage 1L (Opportunity Research Agent / ORA)

### Stages under development
- Stage 2H (Research Compiler) — formalized, not yet run
- Stage 3 (Editorial Builder) — PROMPT.md drafted (untracked)

### Placeholders (not yet designed)
- Stage 4 (Editorial QA)
- Stage 5 (Publisher)

## Editorial Builder — file inventory

### Directory tree

```
agents/editorial-builder/
├── PLACEHOLDER.md
└── PROMPT.md
```

### File purposes

| File | Status | Purpose |
|---|---|---|
| `PLACEHOLDER.md` | Committed (tracked) | Original placeholder document. States Stage 3 is "Not yet designed" and that design begins after the Research Compiler is live. Describes dual-pipeline input but predates the PROMPT.md draft. |
| `PROMPT.md` | Untracked (new) | Draft agent system prompt (207 lines, v2.1). Defines the writer role, architecture boundaries, output format, article type routing, generation instructions, structural rules, content/editorial rules, component rules, and a 26-item pre-delivery checklist. |

### What should exist (by Research Compiler precedent)

The Research Compiler (`agents/research-compiler/`) is the canonical model for a complete Stage 2+ agent. It has four files:

| File | Editorial Builder equivalent | Exists? |
|---|---|---|
| `SPEC.md` | — | **Missing** |
| `README.md` | — | **Missing** |
| `PROMPT.md` | `PROMPT.md` | Exists (untracked) |
| `OUTPUT-TEMPLATE.md` | — | **Missing** |

## Current implementation

### What is already implemented
- A detailed agent prompt (`PROMPT.md`, 207 lines) covering: role, architecture freeze boundaries, output format template (Astro block with `OlspLayout`), article type routing table, 3-step generation process, structural rules, content/editorial rules (source fidelity, epistemic labelling five categories, income claim handling, no-first-hand-testing, tone), component rules per article type, and a 26-item pre-delivery checklist.
- The manual Builder V1 workflow exists in production as `docs/PRODUCTION-MASTER-PROMPT.md`, `docs/BLOG-MASTER-PROMPT.md`, and `docs/ROUNDUP-MASTER-PROMPT.md`.

### What is missing
- **`SPEC.md`** — formal specification: mission, scope (in/out), workflow stages, input handling (dual pipeline: Light Opportunity Brief vs Heavy Knowledge Asset), output specification, duplicate prevention, error handling, approval criteria.
- **`README.md`** — operational overview: pipeline position, inputs, outputs, quick reference, list of documents in the folder.
- **`OUTPUT-TEMPLATE.md`** — concrete output template showing what the agent produces (distinct from the inline template in PROMPT.md which is a fragment).
- **Migration of Builder V1** — the manual workflow in `docs/PRODUCTION-MASTER-PROMPT.md` etc. has not been consolidated into or referenced by the agent specification.
- **Pipeline integration** — no invocation mechanism, no contract with upstream (ORA / Research Compiler) or downstream (Editorial QA).

### What is only a placeholder
Everything except the PROMPT.md draft. The PLACEHOLDER.md is still the committed state and explicitly says "Not yet designed."

## PROMPT.md analysis

### Purpose
Defines the Editorial Builder agent's behavior as an AI content generator. It instructs an LLM to produce editorial content (Astro body blocks) given a research package input, without touching presentation/layout code. It enforces architecture boundaries, source fidelity, epistemic labelling, and Gold Master compliance.

### Completeness assessment

| Aspect | Completeness | Notes |
|---|---|---|
| Role definition | Complete | Clear boundary between content (Builder) and presentation (OLSP Standard) |
| Architecture freeze | Complete | Lists 10 categories the Builder must never generate |
| Output format | Complete | Shows the Astro block template |
| Article type routing | Complete | Table covers reviews, blog, roundups with spec references |
| Generation instructions | Complete | 3 steps: read spec → plan sections → generate content |
| Structural rules | Complete | 13 explicit rules covering sections, IDs, links |
| Content/editorial rules | Complete | Source fidelity, epistemic labelling (5 categories), income claims, no-first-hand-testing, tone |
| Component rules | Complete | Per-component rules for hero tag, verdict box, methodology, pricing table, comparison table, pros/cons, SVG diagram, score bars, quiz, FAQ, video embed, sources, internal links, CTA |
| Pre-delivery checklist | Complete | 26 items, checkbox format |
| Dual-pipeline input handling | **Missing** | PROMPT.md mentions "research package" generically but does not distinguish Light Opportunity Brief vs Heavy Knowledge Asset inputs |
| Error handling | **Missing** | No guidance on what to do if the research package is incomplete, contradictory, or missing required fields |
| Invocation/execution | **Missing** | No instructions on how this prompt is used — no system message template, no user message template, no invocation context |
| Validation rules | **Partial** | Checklist covers output quality but not input validation |

### Missing sections overall
- How to handle dual-pipeline input (Opportunity Brief vs Knowledge Asset)
- Error/incomplete-input handling
- Invocation context and system message template
- Relationship to downstream Editorial QA stage

## Dependencies

### Upstream — Light Pipeline: Opportunity Brief
**Path:** `agents/opportunity-research-agent/briefs/[slug].md`
**Format:** Single-article-scoped research document with keyword scoring, editorial decision (WRITE NOW / WAIT / DO NOT WRITE)
**Contract:** Builder receives a scored, approved opportunity. The brief contains the target keyword, audience, and content direction. The Builder must not re-evaluate the write decision.

### Upstream — Heavy Pipeline: Knowledge Asset (Research Brief)
**Path:** `docs/research/[slug].md` (registered in `docs/HEAVY-ASSET-LIBRARY.md`)
**Format:** Subject-appropriate deep research (product deep dive, comparison, or pillar synthesis)
**Contract:** Builder receives a reusable research document. Article production from a Knowledge Asset is optional — the Builder may be invoked with a Knowledge Asset citation but no requirement to produce a page. The Builder must not re-research the subject.

### Gold Master specifications
- **Reviews:** `docs/GOLD-MASTER-SPEC.md` — canonical structural/CSS/JS standard; canonical reference file at `src/pages/reviews/olsp-academy.astro`
- **Blog:** `docs/BLOG-MASTER-SPEC.md` — blog-specific variant with QuoteBanner and StandardCta components
- **Roundups:** `docs/ROUNDUP-GOLD-MASTER-SPEC.md` — roundup-specific variant with RankingTable, ProductCard, CtaCard

The Builder is instructed to read the relevant spec before generating content and to use only the shared components defined there.

### OLSP Standard v2.1 layout system
**Location:** `src/layouts/OlspLayout.astro`
**Role:** Provides page architecture (`<html>`, `<head>`, `<header>`, navigation, `<footer>`, scripts, SEO, Open Graph). The Builder's output is injected as children of `OlspLayout`. The Builder must never reproduce layout elements.

### Downstream — Editorial QA (Stage 4)
**Status:** Placeholder (`agents/editorial-qa/PLACEHOLDER.md`)
**Contract:** The Builder's output is validated against the Gold Master specification before publication. QA checks for: structural compliance, CTA placement, source citations, canonical URL, `prerender = true`, no fabricated data. The Builder must produce output that passes these checks — but the QA checklist is not yet finalized (Stage 4 is placeholder).

### Manual Builder V1
**Location:** `docs/PRODUCTION-MASTER-PROMPT.md`, `docs/BLOG-MASTER-PROMPT.md`, `docs/ROUNDUP-MASTER-PROMPT.md`
**Status:** The current production workflow. Not yet migrated into the Editorial Builder agent. The agent PROMPT.md references these indirectly through the Gold Master specs.

## Gap analysis

The following work is required before Stage 3 (Editorial Builder) can be considered production-ready:

| # | Gap | Priority | Notes |
|---|---|---|---|
| 1 | **No SPEC.md** — formal specification of agent mission, scope, workflow, inputs, outputs, error handling | High | The canonical pattern is established by Research Compiler's SPEC.md |
| 2 | **No README.md** — operational overview, quick reference, document index | High | Every other agent stage has one |
| 3 | **No OUTPUT-TEMPLATE.md** — concrete output example showing a complete generated content block | Medium | PROMPT.md has an inline template fragment but no worked example |
| 4 | **Dual-pipeline input handling unspecified in PROMPT.md** — the prompt says "research package" generically but doesn't distinguish Opportunity Brief (Light) from Knowledge Asset (Heavy) | High | The two inputs have different structures and constraints |
| 5 | **No invocation/execution instructions** — no system message template, no user message template, no context about how the prompt is used | Medium | PROMPT.md reads as a standalone instruction set but lacks invocation scaffolding |
| 6 | **No error/incomplete-input handling** — what to do when the research package is missing required fields | Medium | Could cause silent failures or fabricated content |
| 7 | **Builder V1 manual workflow not migrated** — `docs/PRODUCTION-MASTER-PROMPT.md` and siblings remain the production workflow | Low | Migration can happen incrementally |
| 8 | **No integration contract with Editorial QA** — Stage 4 output requirements not finalized | Low | Stage 4 is also placeholder; can be defined in parallel |

## Recommended next implementation task

**Create `agents/editorial-builder/SPEC.md` following the Research Compiler pattern.**

The Research Compiler (`agents/research-compiler/SPEC.md`) establishes the canonical spec structure for agent stages in this pipeline. Write an equivalent SPEC.md for the Editorial Builder that formalizes:

- **Mission** — what the agent does (generate Gold Master-compliant editorial content from a research package)
- **Scope** — explicitly list what is in scope and out of scope (dual-pipeline input handling, output format, file placement)
- **Workflow stages** — define the internal stages the agent follows (e.g., E0: Input validation, E1: Spec selection, E2: Content planning, E3: Content generation, E4: Self-check against checklist)
- **Inputs** — define both input paths (Light Opportunity Brief vs Heavy Knowledge Asset) with their structures and constraints
- **Outputs** — define the output contract (Astro content block, error documents for invalid inputs)
- **Duplicate/reuse prevention** — what to check before generating
- **Error handling** — what to do when inputs are incomplete or contradictory

This task is small, self-contained, follows an established pattern, and unblocks the remaining Editorial Builder work (PROMPT.md refinement, README.md, OUTPUT-TEMPLATE.md).

**Rationale for choosing SPEC.md over other gaps:** All other agent stages follow the pattern of SPEC.md → README.md → PROMPT.md → OUTPUT-TEMPLATE.md. The PROMPT.md already exists (draft). Writing the SPEC.md first establishes the formal boundaries and workflow, which then guides the remaining refinements. Without a SPEC.md, the PROMPT.md lacks architectural context and cannot be validated for completeness.

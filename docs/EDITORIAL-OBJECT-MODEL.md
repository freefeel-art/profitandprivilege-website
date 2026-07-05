# Editorial Object Model

**Canonical Shared Vocabulary — Architecture Freeze v1**

*This document defines every canonical object shared by agents in the AI Editorial Operating System. It is the system's data model. No agent, prompt, or specification may introduce terminology that duplicates, conflicts with, or bypasses these objects.*

*Read this after WHY.md, AI-EDITORIAL-OPERATING-SYSTEM.md, and AGENT-CONTRACT.md.*

*Read this before creating any new agent specification, prompt, or implementation.*

---

## 1. Purpose

The AI Editorial Operating System has multiple agents, multiple stages, and multiple deliverables. Without a shared vocabulary, agents invent overlapping terminology, handoffs become ambiguous, and the system accumulates inconsistent data.

This document solves that problem by defining the exact set of objects every agent operates on, owns, consumes, or produces.

### What this document is

- A data model — defines objects, fields, relationships, and constraints
- An ownership map — specifies which stage creates, modifies, and retires each object
- A lifecycle reference — documents how objects progress through the pipeline
- A vocabulary authority — the single source of truth for canonical terminology

### What this document is not

- Not a workflow — the pipeline is specified in `AI-EDITORIAL-OPERATING-SYSTEM.md`
- Not a prompt — agent prompts are in per-agent `PROMPT.md` files
- Not an implementation guide — code, storage, and automation decisions belong in `SPEC.md` files
- Not a schema — field-level output specifications belong in per-agent `OUTPUT-SCHEMA.md` files

### How to use this document

| Role | Use |
|------|-----|
| Agent spec writer | Check whether an object already exists before defining a new one. Reference canonical IDs. |
| Prompt writer | Use canonical terminology. Do not rename objects. |
| Agent implementer | Store objects with canonical fields. Use canonical ID format. |
| Reviewer | Verify that no agent introduces vocabulary that conflicts with this model. |

---

## 2. Authority

This document sits alongside the existing authority hierarchy:

```
WHY.md                                                  ← highest authority
    ↓
AI-EDITORIAL-OPERATING-SYSTEM.md
    ↓
AGENT-CONTRACT.md
    ↓
EDITORIAL-OBJECT-MODEL.md                               ← this document
    ↓
Agent Specification (per-agent)
    ↓
Prompt (per-execution)
    ↓
Implementation (code, tooling, automation)
```

This document is subordinate to the AGENT-CONTRACT.md but supersedes any agent specification. If an agent specification defines an object differently from this model, this model wins. If an agent specification introduces an object not in this model, it must be proposed for addition to this model before use.

---

## 3. Object Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                         DISCOVERY LAYER                             │
│                                                                     │
│  ┌───────────┐     ┌──────────┐     ┌───────────┐     ┌─────────┐ │
│  │ Community │────▶│  Thread  │────▶│  Finding  │────▶│ Cluster │ │
│  └───────────┘     └──────────┘     └───────────┘     └─────────┘ │
│                                                           │         │
│                    ┌──────────────────────────────────────┘         │
│                    ▼                                                 │
│              ┌────────────┐                                          │
│              │ Opportunity│                                          │
│              └────────────┘                                          │
│                    │                                                 │
└────────────────────┼─────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                         RESEARCH LAYER                              │
│                                                                     │
│              ┌───────────────┐                                       │
│              │ Research Brief│                                       │
│              └───────┬───────┘                                       │
│                      │                                               │
│              ┌───────▼───────┐                                       │
│              │  Article      │                                       │
│              └───────┬───────┘                                       │
│                      │                                               │
└──────────────────────┼───────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                       KNOWLEDGE LAYER                               │
│                                                                     │
│           ┌─────────────────────────────────┐                       │
│           │        Asset Library            │                       │
│           │  ┌──────┐ ┌───────┐ ┌────────┐  │                       │
│           │  │Profile│ │Citation│ │ Dataset │  │                       │
│           │  └──────┘ └───────┘ └────────┘  │                       │
│           │  ┌──────┐ ┌───────┐             │                       │
│           │  │ Stat │ │ Image │             │                       │
│           │  └──────┘ └───────┘             │                       │
│           └─────────────────────────────────┘                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. Canonical Objects

### 4.1 Community

**Definition:** A discussion source where the target audience communicates.

**Stage ownership:** Community Intelligence (Stage 1)

**Lifecycle:**

```
Identified ──▶ Active ──▶ Archived
   │                         │
   └──(never promoted)───────┘
```

| State | Meaning |
|-------|---------|
| Identified | Community has been found. Not yet mined for signals. |
| Active | Community is actively monitored for new threads and signals. |
| Archived | Community is no longer producing relevant discussion. May be reactivated. |

**Canonical fields:**

| Field | Type | Description |
|-------|------|-------------|
| `community_id` | `COM-NNN` | Permanent canonical identifier |
| `name` | String | Human-readable name (e.g., "r/Affiliatemarketing") |
| `url` | URL | Canonical URL |
| `platform_type` | Enum | Reddit, Quora, Forum, Facebook, Discord, YouTube, X, LinkedIn, Other |
| `relevance` | Enum | Direct, Adjacent, Peripheral |
| `activity_level` | Enum | High, Medium, Low |
| `member_count` | Integer (approx) | Estimated active members |
| `cultural_notes` | Text | Community norms, moderation style, signal patterns |
| `state` | Enum | Identified, Active, Archived |

**Relationship rules:**
- A Community contains zero or more Threads
- A Community is created by Community Intelligence
- A Community is never modified by a downstream stage

---

### 4.2 Thread

**Definition:** A single discussion inside a Community. The smallest addressable discussion unit.

**Stage ownership:** Community Intelligence (Stage 1)

**Lifecycle:**

```
Discovered ──▶ Analysed ──▶ Exhausted
```

| State | Meaning |
|-------|---------|
| Discovered | Thread found. Not yet mined for findings. |
| Analysed | Thread has been mined. Findings extracted. |
| Exhausted | Thread has been fully analysed. No further signals expected. |

**Canonical fields:**

| Field | Type | Description |
|-------|------|-------------|
| `thread_id` | `THR-NNN` | Permanent canonical identifier |
| `community_id` | `COM-NNN` | Parent community |
| `title` | String | Thread title |
| `url` | URL | Direct link to thread |
| `date_consulted` | ISO date | When the thread was analysed |
| `state` | Enum | Discovered, Analysed, Exhausted |
| `finding_ids` | `[FND-NNN]` | All findings extracted from this thread |

**Relationship rules:**
- A Thread belongs to exactly one Community
- A Thread produces zero or more Findings
- A Thread is created by Community Intelligence
- A Thread is never consumed by a stage before Community Intelligence

---

### 4.3 Finding

**Definition:** The smallest reusable evidence unit. One verified observation extracted from a Thread. Findings are immutable — no agent may rewrite a Finding after creation. Later agents may only reference it.

**Stage ownership:** Community Intelligence (Stage 1)

**Lifecycle:**

```
Extracted ──▶ Verified ──▶ Referenced
                               │
                    (immutable — never modified after this point)
```

| State | Meaning |
|-------|---------|
| Extracted | Finding pulled from a thread. Not yet confidence-checked. |
| Verified | Finding has been checked for accuracy and confidence assigned. |
| Referenced | Finding is referenced by at least one downstream object. |

**Canonical fields:**

| Field | Type | Description |
|-------|------|-------------|
| `finding_id` | `FND-NNN` | Permanent canonical identifier |
| `originating_thread_id` | `THR-NNN` | Source thread |
| `originating_community_id` | `COM-NNN` | Source community (denormalised for query efficiency) |
| `evidence_snippet` | Text | Verbatim or close-paraphrase evidence from the thread |
| `finding_type` | Enum | Question, Problem, Misconception, Objection, Comparison, Self-reported_failure, Conflicting_advice |
| `confidence` | Enum | High, Medium, Low |
| `intent_type` | Enum | Information, How-to, Decision, Verification, Troubleshooting |
| `problem_category` | Enum | Knowledge_gap, Skill_gap, Resource_gap, Trust_gap, Execution_gap, Decision_gap, Emotional_barrier |
| `state` | Enum | Extracted, Verified, Referenced |

**Immutability rules:**
- Once a Finding transitions to `Verified`, it cannot be modified
- Corrections create a new Finding that supersedes the old one
- The superseded Finding is marked `Referenced` with a `superseded_by` field pointing to the new Finding
- No downstream agent may edit, rephrase, or reinterpret a Finding
- A Finding may only be deleted if it has never been referenced

**Relationship rules:**
- A Finding originates from exactly one Thread (the `originating_thread_id`)
- A Finding may be referenced by multiple Clusters, Opportunities, Research Briefs, and Articles
- A Finding is created by Community Intelligence
- A Finding is read-only for every downstream stage

---

### 4.4 Cluster

**Definition:** A group of related Findings that share a common root cause or topic. Clusters enable the system to treat multiple individual signals as a single editorial unit.

**Stage ownership:** Community Intelligence (Stage 1). Refined by Editorial Intelligence (Stage 2).

**Lifecycle:**

```
Proposed ──▶ Validated ──▶ Active ──▶ Archived
                              │
                    (may be refined by Editorial Intelligence)
```

| State | Meaning |
|-------|---------|
| Proposed | Cluster created by CI. Membership may change. |
| Validated | Cluster confirmed as coherent. Membership frozen. |
| Active | Cluster is currently driving editorial work. |
| Archived | Cluster no longer active. May be re-activated. |

**Canonical fields:**

| Field | Type | Description |
|-------|------|-------------|
| `cluster_id` | `CLU-NNN` | Permanent canonical identifier |
| `member_finding_ids` | `[FND-NNN]` | All findings in this cluster |
| `summary` | Text | Concise description of what binds these findings |
| `root_problem` | Text | The underlying problem the cluster represents |
| `confidence` | Enum | High, Medium, Low |
| `state` | Enum | Proposed, Validated, Active, Archived |

**Refinement rules:**
- CI creates the initial cluster proposal
- EI may add or remove findings within the cluster (EI's refinement is the final membership)
- No stage after EI may modify cluster membership
- A cluster not validated by EI is marked Archived

**Relationship rules:**
- A Cluster contains 2 or more Findings
- A Finding may belong to zero or more Clusters
- A Cluster may produce zero or more Opportunities

---

### 4.5 Opportunity

**Definition:** A specific editorial opportunity derived from one or more Findings or Clusters. The Opportunity is the central object that travels through the pipeline, accumulating state as it passes each stage.

**Stage ownership:** Multi-stage lifecycle. Created by Community Intelligence (Stage 1). Refined by Editorial Intelligence (Stage 2). Gated by Editorial Decision (Stage 3). Expanded by Opportunity Discovery (Stage 4). Validated by Research Validation (Stage 5). Consumed by Research Intelligence (Stage 6) and Content Production (Stage 7). Measured by Performance Intelligence (Stage 10).

**Lifecycle:**

```
         ┌─────────────────────────────────────────────────────────┐
         │                                                         │
         ▼                                                         │
Discovered ──▶ Refined ──▶ Approved ──▶ Briefed ──▶ Validated ────┼──▶ Active
    │            │            │              │           │         │       │
    │            │            │              │           │         │       │
    └─── Archived (rejected at any gate)     │           │         │       │
                                             │           │         │       │
                                             ▼           ▼         ▼       ▼
                                        Archived    Archived    Hold    Produced
                                                                           │
                                                                           ▼
                                                                       Measured
                                                                           │
                                                                           ▼
                                                                       Archived
                                                                     (or updated)
```

| State | Meaning | Owner |
|-------|---------|-------|
| Discovered | Created by CI from findings/clusters. Not yet reviewed. | CI |
| Refined | Reviewed and structured by EI. Ready for editorial decision. | EI |
| Approved | Passed Editorial Decision gate. Ready for Opportunity Discovery. | ED |
| Briefed | Opportunity Brief produced by OD. Ready for Research Validation. | OD |
| Validated | Passed Research Validation gate. Ready for research. | RV |
| Active | Research is underway or content is being produced. | RI / CP |
| Produced | Article is published. | CP / P |
| Measured | Performance data has been collected and analysed. | PI |
| Hold | Deferred. Will be re-evaluated later. | Any gate |
| Archived | No longer active. Reason recorded. | Any gate |

**Canonical fields:**

| Field | Type | Description |
|-------|------|-------------|
| `opportunity_id` | `OPP-NNN` | Permanent canonical identifier |
| `source_finding_ids` | `[FND-NNN]` | Findings that support this opportunity |
| `source_cluster_ids` | `[CLU-NNN]` | Optional — clusters that informed this opportunity |
| `working_title` | String | Current working title (may change during refinement) |
| `primary_question` | String | The core question this opportunity answers |
| `root_problem` | Text | The underlying problem being addressed |
| `opportunity_type` | Enum | Review, Roundup, Guide, Comparison, Explainer, Troubleshooting, Myth-busting, Empathy-driven, Evidence-based |
| `editorial_priority` | Integer (1-N) | Priority rank within the current editorial cycle |
| `state` | Enum | Discovered, Refined, Approved, Briefed, Validated, Active, Produced, Measured, Hold, Archived |
| `article_id` | `ART-NNN` | Optional — populated when the article is created |
| `performance_data_ref` | `PRF-NNN` | Optional — populated after measurement |

**Transition rules:**
- Only the owning stage may transition an Opportunity to its next state
- Any gate (ED, RV, EQA) may transition to Hold or Archived
- An Archived Opportunity may be reactivated (transition back to Refined) if community signals change
- The `article_id` is set when Content Production creates the Article
- The `performance_data_ref` is set when Performance Intelligence completes analysis

**Relationship rules:**
- An Opportunity references 1 or more Findings
- An Opportunity may reference 0 or more Clusters
- An Opportunity produces exactly 0 or 1 Article (if it reaches production)
- An Opportunity is the only object that crosses stage boundaries

---

### 4.6 Research Brief

**Definition:** A formal research package created by Research Intelligence. Contains the evidence library, source list, fact summary, and knowledge gaps that define what an Article can responsibly claim. The Research Brief is the complete factual foundation — a Content Production agent must never need to conduct additional research.

**Stage ownership:** Research Intelligence (Stage 6)

**Lifecycle:**

```
Drafted ──▶ Complete ──▶ Consumed ──▶ Archived
```

| State | Meaning |
|-------|---------|
| Drafted | Research in progress. Not yet complete. |
| Complete | All research tasks finished. Ready for content production. |
| Consumed | The Article has been created from this brief. |
| Archived | Brief is no longer needed. May be referenced as an Asset. |

**Canonical fields:**

| Field | Type | Description |
|-------|------|-------------|
| `brief_id` | `BRF-NNN` | Permanent canonical identifier |
| `opportunity_id` | `OPP-NNN` | The opportunity this brief supports |
| `evidence_library` | Collection of Source entries | All sources with reliability labels |
| `source_list` | `[SRC-NNN]` | All sources cited in the article |
| `fact_summary` | Structured text | Key claims with verified answers |
| `knowledge_gap_log` | Structured text | Claims that could not be verified |
| `state` | Enum | Drafted, Complete, Consumed, Archived |

**Evidence Library entry (Source):**

| Field | Type | Description |
|-------|------|-------------|
| `source_id` | `SRC-NNN` | Permanent canonical identifier |
| `source_type` | Enum | Official_documentation, Independent_review, Academic_paper, News_article, Community_thread, Vendor_page, Self-reported |
| `reliability_label` | Enum | Verified, Vendor_claim, Third-party_reported, Self-reported, Unverified |
| `url` | URL | Source URL |
| `accessed_date` | ISO date | When the source was consulted |
| `relevant_claims` | Text | What claims this source supports |

**Relationship rules:**
- A Research Brief serves exactly one Opportunity
- A Research Brief is consumed by exactly one Article
- A Research Brief may be promoted to an Asset after consumption (for reuse)
- A Research Brief never creates or modifies Findings

---

### 4.7 Article

**Definition:** The final published asset. Created by Content Production from a Research Brief. The Article is the only object that reaches the public.

**Stage ownership:** Content Production (Stage 7). Validated by Editorial QA (Stage 8). Published by Publishing (Stage 9).

**Lifecycle:**

```
Draft ──▶ Review ──▶ Approved ──▶ Published ──▶ Updated
   │          │                           │
   │          └── Revision Request ───▶ Draft
   │                                        │
   └── Archived (abandoned during review)
```

| State | Meaning | Owner |
|-------|---------|-------|
| Draft | Initial draft produced by CP. | CP |
| Review | Under QA review. | EQA |
| Revision Request | QA found issues. Back to CP. | EQA → CP |
| Approved | QA passed. Ready to publish. | EQA |
| Published | Live on the site. | P |
| Updated | Revised after publication. | CP |
| Archived | Removed or replaced. | P |

**Canonical fields:**

| Field | Type | Description |
|-------|------|-------------|
| `article_id` | `ART-NNN` | Permanent canonical identifier |
| `opportunity_id` | `OPP-NNN` | The opportunity this article fulfils |
| `brief_id` | `BRF-NNN` | The research brief this article was written from |
| `title` | String | Published title |
| `url` | URL | Live URL |
| `content_format` | Enum | Review, Roundup, Guide, Comparison, Explainer, Troubleshooting, Myth-busting |
| `word_count` | Integer | Published word count |
| `state` | Enum | Draft, Review, Revision_Request, Approved, Published, Updated, Archived |
| `published_date` | ISO date | When the article went live |

**Relationship rules:**
- An Article is created from exactly one Research Brief
- An Article fulfils exactly one Opportunity
- An Article references zero or more Findings (through the Opportunity)
- An Article may reference zero or more Assets (Company Profiles, Statistics, etc.)
- An Article never creates, modifies, or interprets Findings
- An Article never performs research — it only consumes the Research Brief

---

### 4.8 Asset

**Definition:** A reusable long-term knowledge object. Assets span across articles and projects. They are created once and referenced many times. The Asset Library is the system's institutional memory.

**Stage ownership:** Knowledge Layer (cross-cutting). Assets may be created by any stage that produces reusable knowledge.

**Lifecycle:**

```
Created ──▶ Verified ──▶ Available ──▶ Deprecated
```

| State | Meaning |
|-------|---------|
| Created | Asset entered into the library. Not yet verified. |
| Verified | Asset has been checked for accuracy. |
| Available | Asset is ready for reference by any stage. |
| Deprecated | Asset is outdated. New asset supersedes it. |

**Asset types:**

| Type | Canonical ID Prefix | Description | Example |
|------|---------------------|-------------|---------|
| Company Profile | `CPR-NNN` | Verified company information | OLSP Academy company profile |
| Product Profile | `PPR-NNN` | Verified product or platform specs | Mega Link product profile |
| Statistic | `STA-NNN` | Verified numerical data point | "77% of Trustpilot reviews are 5-star" |
| Citation | `CIT-NNN` | Academic or industry source | Peer-reviewed study on affiliate marketing |
| Image | `IMG-NNN` | Licensed or created visual asset | Infographic: OLSP pricing tiers |
| Dataset | `DS-NNN` | Structured research data | Survey results, scraped data |
| Source | `SRC-NNN` | Archived source document | Official documentation, web crawl |
| Performance Snapshot | `PRF-NNN` | Aggregated performance data | Article performance at 90 days |

**Canonical fields (all asset types):**

| Field | Type | Description |
|-------|------|-------------|
| `asset_id` | `{PREFIX}-NNN` | Permanent canonical identifier (prefix varies by type) |
| `asset_type` | Enum | Company_profile, Product_profile, Statistic, Citation, Image, Dataset, Source, Performance_snapshot |
| `title` | String | Human-readable name |
| `source_url` | URL | Where the asset's data was obtained |
| `verified_date` | ISO date | When the asset was last verified |
| `reliability_label` | Enum | Verified, Vendor_claim, Third-party_reported, Self-reported, Unverified |
| `state` | Enum | Created, Verified, Available, Deprecated |
| `superseded_by` | `{PREFIX}-NNN` | Optional — newer asset that replaces this one |
| `referenced_by` | `[object_id]` | Agents/objects that reference this asset |

**Relationship rules:**
- An Asset is created by any stage that produces reusable knowledge
- An Asset is referenced by any object that needs its data
- An Asset never references a specific Article (it is article-agnostic)
- When an Asset is Deprecated, the superseding Asset is noted in `superseded_by`
- Assets are the only objects in the Knowledge Layer

---

## 5. Ownership Matrix

| Object | Created By | Can Modify | Can Archive | Read-only For |
|--------|-----------|------------|-------------|---------------|
| Community | CI | CI | CI | All downstream stages |
| Thread | CI | CI (state only) | CI | All downstream stages |
| Finding | CI | CI (state only, before Verified) | CI (if never referenced) | All downstream stages |
| Cluster | CI | CI, EI (membership) | CI, EI | All stages after EI |
| Opportunity | CI | CI, EI, ED, OD | Any gate | RI (reads only), CP (reads only) |
| Research Brief | RI | RI (before Complete) | RI | CP (reads only), EQA (reads only) |
| Article | CP | CP (before Published), P (state only) | P | All upstream stages (reads only) |
| Asset | Any stage | Creating stage (before Verified) | Creating stage | All stages (reads only) |

This matrix enforces **stage isolation**: each stage owns its objects fully. No stage modifies objects owned by another stage (except state transitions in the pipeline flow).

---

## 6. Identifier System

### 6.1 Canonical ID Prefixes

| Prefix | Object | Defining Stage |
|--------|--------|----------------|
| `COM` | Community | Community Intelligence |
| `THR` | Thread | Community Intelligence |
| `FND` | Finding | Community Intelligence |
| `CLU` | Cluster | Community Intelligence |
| `OPP` | Opportunity | Community Intelligence |
| `BRF` | Research Brief | Research Intelligence |
| `SRC` | Source (Evidence Library entry) | Research Intelligence |
| `ART` | Article | Content Production |
| `CPR` | Company Profile (Asset) | Knowledge Layer |
| `PPR` | Product Profile (Asset) | Knowledge Layer |
| `STA` | Statistic (Asset) | Knowledge Layer |
| `CIT` | Citation (Asset) | Knowledge Layer |
| `IMG` | Image (Asset) | Knowledge Layer |
| `DS` | Dataset (Asset) | Knowledge Layer |
| `PRF` | Performance Snapshot (Asset) | Performance Intelligence |

### 6.2 ID Format

```
{PREFIX}-{NNN}
```

- `{PREFIX}` — three uppercase letters
- `{NNN}` — zero-padded three-digit sequence number (001, 002, ..., 999)
- IDs are assigned sequentially within each prefix
- IDs are never reused. If an object is deleted, its ID is retired.
- IDs are permanent once assigned. An ID always refers to the same object.

### 6.3 ID Registry

Every report or data export must include an `id_registry` that lists every ID used:

```yaml
id_registry:
  community_ids: ["COM-001", "COM-002", ...]
  thread_ids: ["THR-001", "THR-002", ...]
  finding_ids: ["FND-001", "FND-002", ...]
  cluster_ids: ["CLU-001", ...]
  opportunity_ids: ["OPP-001", ...]
  article_ids: ["ART-001", ...]
```

---

## 7. Object Relationships

### 7.1 Relationship Diagram

```
┌────────────┐
│ Community  │─── has many ──▶ ┌────────┐
│ (COM-NNN)  │                  │ Thread │─── mined into ──▶ ┌─────────┐
└────────────┘                  │(THR-NNN)│                  │ Finding │
                                └────────┘                  │(FND-NNN)│
                                      │                      └────┬────┘
                                      │                          │
                                      │                          ▼
                                      │                  ┌───────────┐
                                      │                  │  Cluster  │
                                      │                  │(CLU-NNN)  │
                                      │                  └─────┬─────┘
                                      │                        │
                                      ▼                        ▼
                              ┌──────────────────────────────────┐
                              │           Opportunity            │
                              │           (OPP-NNN)              │
                              └──────────────┬───────────────────┘
                                             │
                                             ▼
                              ┌──────────────────────────────────┐
                              │         Research Brief           │
                              │          (BRF-NNN)               │
                              │  ┌──────┐ ┌──────┐ ┌──────────┐  │
                              │  │Source│ │ Fact │ │ Knowledge │  │
                              │  │Library│ │Summary│ │ Gap Log  │  │
                              │  └──────┘ └──────┘ └──────────┘  │
                              └──────────────┬───────────────────┘
                                             │
                                             ▼
                              ┌──────────────────────────────────┐
                              │            Article                │
                              │           (ART-NNN)               │
                              └──────────────┬───────────────────┘
                                             │
                                             ▼
                              ┌──────────────────────────────────┐
                              │         Asset Library            │
                              │  ┌──────┐ ┌──────┐ ┌──────────┐  │
                              │  │Profile│ │Citation│ │ Statistic│  │
                              │  └──────┘ └──────┘ └──────────┘  │
                              └──────────────────────────────────┘

Cross-object references (non-hierarchical):
  Finding ────── references ──── Thread (originating_thread_id)
  Cluster ────── contains ────── Finding (member_finding_ids)
  Opportunity ── references ──── Finding (source_finding_ids)
  Opportunity ── references ──── Cluster (source_cluster_ids)
  Research Brief ── serves ───── Opportunity (opportunity_id)
  Article ────── fulfils ─────── Opportunity (opportunity_id)
  Article ────── consumes ────── Research Brief (brief_id)
  Article ────── may reference ─ Asset (any type)
  Research Brief ── may become ─ Asset (promoted after consumption)
```

### 7.2 Cardinality Summary

| From | To | Cardinality |
|------|----|-------------|
| Community | Thread | 1:N |
| Thread | Finding | 1:N |
| Finding | Cluster | M:N |
| Finding | Opportunity | M:N |
| Cluster | Opportunity | M:N |
| Opportunity | Research Brief | 1:1 |
| Research Brief | Article | 1:1 |
| Article | Asset | M:N |
| Research Brief | Asset | M:N (promoted sources) |

---

## 8. Immutable Rules

### Rule 1: Findings Are Immutable

Once a Finding transitions to `Verified` state, no agent may modify its `evidence_snippet`, `finding_type`, `confidence`, or `intent_type`. Corrections create a new Finding that supersedes the old one. The superseded Finding is marked with `superseded_by: "FND-NNN"`.

**Rationale:** Downstream agents (EI, OD, RI, CP) reference Findings by ID. If a Finding's content could change, every downstream reference becomes potentially invalid. Immutability guarantees referential integrity.

### Rule 2: Opportunities Reference Findings

An Opportunity must always reference at least one Finding via `source_finding_ids`. An Opportunity may not be created from editorial intuition, keyword data, or any source that does not trace to a verified Finding.

**Rationale:** This enforces the pipeline's ordering (Problems Before Keywords). Every article originates from a community discussion. Bypassing Findings breaks the chain of evidence.

### Rule 3: Articles Never Create Findings

An Article may reference Findings (through its Opportunity chain), but it may never create, modify, or interpret Findings. The direction of knowledge is always upstream to downstream: Communities → Findings → Opportunities → Articles.

**Rationale:** If Articles could create Findings, the feedback loop becomes a closed circle. The system would publish content based on its own previous publications rather than on fresh community signal.

### Rule 4: Research Briefs Never Modify Opportunities

A Research Brief serves an Opportunity. It does not modify the Opportunity's content, priority, or state beyond what the Opportunity Brief already defines. If research reveals that the Opportunity cannot be supported, the Brief flags this via the Knowledge Gap Log — it does not rewrite the Opportunity.

**Rationale:** The Opportunity represents an editorial hypothesis. The Research Brief tests that hypothesis. If the test fails, the editorial team (not the research agent) decides whether to revise or reject the Opportunity.

### Rule 5: Assets Are Reusable Across Projects

An Asset in the Knowledge Layer has no project or Article affiliation. It may be referenced by any Research Brief or Article in any editorial cycle. Asset verification is independent of article production.

**Rationale:** Company profiles, statistics, and citations are expensive to create and verify. They should serve the entire system, not a single article.

### Rule 6: IDs Are Permanent

Once an ID (of any prefix) is assigned, it refers to the same object forever. ID reuse is prohibited. Deleted objects retire their IDs. Superseded objects note their replacement but retain their original ID.

**Rationale:** Downstream references use IDs. If an ID could change meaning, every reference becomes unreliable. Permanent IDs guarantee stable cross-references.

### Rule 7: Every Object Has Exactly One Owner Stage

The Ownership Matrix (Section 5) defines which stage may create, modify, archive, and delete each object. No object has multiple owners for the same operation type. Stage isolation is mandatory.

**Rationale:** If two stages could both modify an object, the system loses determinism. Each object has a single source of truth at each lifecycle phase.

### Rule 8: No Object Is Skipped

Every approved Opportunity must pass through the full lifecycle: Discovered → Refined → Approved → Briefed → Validated → Active → Produced → Measured. Skipping a state violates the pipeline specification.

**Rationale:** Each state corresponds to a pipeline stage that performs a specific validation. Skipping a state means skipping a validation — which means producing content that has not been properly vetted.

---

## 9. Layer Architecture

The Editorial Object Model organises objects into three conceptual layers. These layers correspond to the three questions from `AI-EDITORIAL-OPERATING-SYSTEM.md` (Section 3):

| Layer | Question | Stages | Objects |
|-------|----------|--------|---------|
| Discovery | WHY does this exist? | CI, EI, ED | Community, Thread, Finding, Cluster, Opportunity |
| Research | WHAT should we produce? | OD, RV, RI | Research Brief, Source, Evidence Library |
| Production | HOW do we deliver it? | CP, EQA, P, PI | Article, Performance Snapshot |

The Knowledge Layer crosses all three layers:

| Layer | Objects | Access |
|-------|---------|--------|
| Knowledge | Asset (all types) | Read/write by any stage; verified independently |

---

## 10. Object State Machine (Summary)

```
Legend:
  ──▶  State transition
  (X)  Stage that performs the transition

Finding:       Extracted ──▶ Verified ──▶ Referenced
                (CI)         (CI)         (any downstream)

Cluster:       Proposed ──▶ Validated ──▶ Active ──▶ Archived
                (CI)         (EI)         (EI)      (CI, EI)

Opportunity:   Discovered ──▶ Refined ──▶ Approved ──▶ Briefed ──▶ Validated ──▶ Active ──▶ Produced ──▶ Measured
                (CI)          (EI)         (ED)         (OD)         (RV)        (RI/CP)    (CP/P)      (PI)

Research Brief: Drafted ──▶ Complete ──▶ Consumed ──▶ Archived
                (RI)         (RI)         (CP)         (RI)

Article:       Draft ──▶ Review ──▶ Approved ──▶ Published ──▶ Updated
                (CP)      (EQA)       (EQA)        (P)          (CP)

Asset:         Created ──▶ Verified ──▶ Available ──▶ Deprecated
                (any)      (creator)    (creator)     (creator)
```

Any gate state (Hold, Archived, Rejected) may interrupt the forward flow from any state.

---

## 11. Relationship to Existing Documents

| Document | Relationship |
|----------|--------------|
| `WHY.md` | This model operates within WHY.md's philosophical boundaries. No object should exist to produce content that violates WHY.md. |
| `AI-EDITORIAL-OPERATING-SYSTEM.md` | This model is the data layer for the pipeline defined in that document. Each stage spec in that document references these objects. |
| `AGENT-CONTRACT.md` | This model is a shared vocabulary that helps agents comply with the contract's stage isolation and handoff rules. |
| `COMMUNITY-INTELLIGENCE.md` | That stage spec defines the CI workflow. This model defines the objects CI produces (Community, Thread, Finding, Cluster, Opportunity). |
| `agents/community-intelligence/OUTPUT-SCHEMA.md` | That schema is an instance of this model — it defines the CI-specific fields for Community, Thread, Finding, Cluster, and Opportunity. |
| Future agent OUTPUT-SCHEMA files | Each must align with this model's object definitions. They may add stage-specific fields but may not change canonical fields. |

---

## 12. Design Principles

### 12.1 One Object, One Owner

Every object has exactly one stage that owns its lifecycle. This prevents conflicting modifications and makes the system deterministic. If an object needs to be modified, the owning stage makes the change.

### 12.2 Read-Only Downstream

Downstream stages read objects created by upstream stages. They never modify them. This enforces pipeline ordering and prevents feedback loops within a single editorial cycle.

### 12.3 Immutable Evidence

Findings are the system's atomic evidence unit. Once verified, they do not change. This guarantees that every downstream decision traces back to stable, auditable evidence.

### 12.4 IDs Over Text

All cross-object references use canonical IDs, not text matching. This prevents drift, enables automated cross-referencing, and makes the system machine-readable.

### 12.5 Discovery Before Validation

The object lifecycle enforces the editorial philosophy: discover first (Finding, Opportunity), validate later (Research Brief). An object cannot reach the Research or Production layers without first passing through the Discovery layer.

---

## 13. Architecture Freeze v1

With the completion of this document, the AI Editorial Operating System's foundation is frozen at version 1.

The following foundation documents are now considered complete and stable:

| Document | Status |
|----------|--------|
| `docs/WHY.md` | Final |
| `docs/AI-EDITORIAL-OPERATING-SYSTEM.md` | Final |
| `docs/AGENT-CONTRACT.md` | Final |
| `docs/COMMUNITY-INTELLIGENCE.md` | Final |
| `docs/EDITORIAL-OBJECT-MODEL.md` | **Final** (this document) |

No additional foundation documents should be created. All future work should proceed to agent-specific implementation within the boundaries defined by these documents.

If production experience reveals a concrete architectural deficiency in these documents, the deficiency must be documented, proposed to the editorial team, and only modified upon approval. The architecture freeze exists to prevent scope expansion — it does not prohibit necessary corrections.

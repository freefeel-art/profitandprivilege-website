# AI Editorial Operating System v2

**Canonical Reference**

*This document is the definitive specification for the AI Editorial Operating System used by OLSP. Every agent, prompt, and workflow in the editorial pipeline derives from this document. Do not modify this document without updating all derived artifacts.*

---

## 1. Mission

The AI Editorial Operating System produces content that solves real human problems, validated by search demand, grounded in research, and continuously improved through performance feedback.

The system does not chase keywords. It does not publish for volume. It does not invent topics from tools.

The system discovers what people genuinely struggle with, validates that enough people share that struggle to warrant publication, researches the topic rigorously, produces content that answers the question better than anything else, and learns from the results.

### What the system produces

- **Review pages** — independent, research-based evaluations of products and platforms
- **Roundup articles** — editorial comparisons across multiple products
- **Informational articles** — educational content addressing recurring community questions
- **Authority articles** — research-backed deep dives that establish topical expertise

### What the system does not produce

- Content created solely because a keyword tool showed volume
- Content that answers a question nobody actually asked
- Content that cannot be supported by research
- Content that exists to fill a publishing calendar

---

## 2. Editorial Philosophy

### 2.1 Human First

Topics originate from people. Never from keyword tools.

A keyword tool can tell you how many people search for a phrase. It cannot tell you why they search, what they actually want, or why existing answers fail them. Community discussions reveal the human context that keyword data cannot capture.

Every article must answer a question a real person actually asked in a community discussion.

### 2.2 Problems Before Keywords

Community problems create opportunities. Search demand validates opportunities. Search demand never creates opportunities.

The editorial pipeline enforces a strict ordering:

1. Discover the problem (from communities)
2. Validate the demand (from search data)
3. Produce the solution (the article)

Reversing this order produces content that matches a search query but solves no human problem. The article ranks, people click, they bounce, nothing converts.

### 2.3 Research Before Opinion

Editorial decisions must be supported by evidence. Research exists to verify, not to invent.

Every factual claim in published content must be traceable to a source. Sources must be labelled by reliability:

| Source type | Label |
|-------------|-------|
| Independently verified fact | Stated plainly with source noted |
| Vendor claim | "According to the official site..." |
| Third-party reported | "Independent reviewers describe..." |
| Self-reported / unaudited | "Self-reported, could not be independently verified" |
| Could not be verified | "Could not be confirmed at the time of writing" |

No claim may be presented as verified fact if it comes only from a source with a financial incentive.

### 2.4 Publish Only Valuable Content

Publishing is not the goal. Helping readers is the goal.

Every article must pass three gates before reaching production:

1. **Does this answer a real question someone is asking?** (Community Intelligence)
2. **Can we answer it better than existing content?** (Solution Gap Analysis)
3. **Can we support our answer with evidence?** (Research Validation)

If any gate fails, the article does not proceed.

---

## 3. The Three Questions Behind Every Editorial Decision

Every article published by this system should be able to answer three questions. These questions form a conceptual stack that governs how the pipeline is organised.

```
WHY does this exist?
        ↓
WHAT should we produce?
        ↓
HOW do we deliver it?
```

The pipeline stages map to these questions. Understanding the mapping makes the system's logic visible: every stage exists to answer one of these three questions. No stage exists without a question it answers.

### 3.1 WHY: Significance

**Purpose:** Determine whether something deserves to exist.

Before any article is produced, the system must establish that the topic matters. Significance is not determined by search volume. It is determined by human need.

**Questions the WHY layer answers:**
- Why does this problem matter to the people experiencing it?
- Why are people discussing it repeatedly across communities?
- Why do existing articles fail to solve it?
- Why should OLSP write about this specific topic?
- Why would solving this improve someone's decision?

**Stages that belong to the WHY layer:**

| Stage | Role in WHY |
|-------|-------------|
| Community Intelligence | Discovers what problems people are actually discussing. Establishes that the problem is real, recurring, and unresolved. |
| Editorial Intelligence | Clusters and prioritises problems. Determines which problems represent genuine editorial opportunities. |
| Editorial Decision | Makes the final call: does this opportunity justify publication? The gate that enforces WHY before anything else proceeds. |

If the WHY layer cannot produce a compelling reason for a topic to exist, the topic stops here. It does not proceed to WHAT.

### 3.2 WHAT: Correctness

**Purpose:** Determine what should actually be produced.

Once the system establishes that a topic matters, it must determine what the correct response looks like. What is the right solution to propose? What evidence supports it? What claims can be made responsibly?

**Questions the WHAT layer answers:**
- What is the real opportunity beneath the surface question?
- What evidence exists to support a recommendation?
- What needs to be researched and verified?
- What claims are supportable by the available evidence?
- What should the final recommendation be?

**Stages that belong to the WHAT layer:**

| Stage | Role in WHAT |
|-------|--------------|
| Opportunity Discovery | Validates and scores the opportunity. Produces the structured brief that defines what the article will cover. |
| Research Validation | Verifies demand, competition, feasibility, and legality. Confirms the opportunity is viable before research begins. |
| Research Intelligence | Builds the factual foundation. Produces the evidence library, source list, and fact summary that define what the article can responsibly claim. |

The WHAT layer produces the truth the article will communicate. If the evidence does not support a clear recommendation, the system flags the gap. It does not proceed to HOW with an unsupported conclusion.

### 3.3 HOW: Execution

**Purpose:** Determine how value is delivered.

Once the system knows WHY something matters and WHAT the correct response is, it determines HOW to deliver that response well. Execution is not an afterthought. A correct answer delivered poorly helps no one.

**Questions the HOW layer answers:**
- How should this explanation be structured for clarity?
- How should the article be organised to serve the reader's question?
- How is quality verified before publication?
- How is the article published, indexed, and distributed?
- How do we learn from the outcome?

**Stages that belong to the HOW layer:**

| Stage | Role in HOW |
|-------|-------------|
| Content Production | Transforms validated research into structured, readable content. |
| Editorial QA | Verifies accuracy, completeness, readability, and editorial standards. |
| Publishing | Makes the content live, indexed, and discoverable. |
| Performance Intelligence | Collects data and community reactions. Feeds insights back into the next WHY cycle. |

### 3.4 Visual Overview

The relationship between the three questions and the pipeline:

```
                   ┌─────────────────────────────────────────────┐
                   │                                             │
                   ▼                                             │
         ┌─────────────────┐                                     │
         │   COMMUNITY     │                                     │
    ┌───▶│  INTELLIGENCE   │────┐                                │
    │    └─────────────────┘    │                                │
    │                           ▼                                │
    │    ┌─────────────────┐                                     │
    │    │   EDITORIAL     │          WHY                         │
    │    │  INTELLIGENCE   │     Discover the right               │
    │    └─────────────────┘     problem to solve                 │
    │                           │                                │
    │                           ▼                                │
    │    ┌─────────────────┐                                     │
    │    │   EDITORIAL     │                                     │
    │    │    DECISION     │──── gate ──── or ────► stop         │
    │    └─────────────────┘                                     │
    │                           │                                │
    │                           ▼                                │
    │    ┌─────────────────┐                                     │
    │    │   OPPORTUNITY   │          WHAT                        │
    │    │   DISCOVERY     │     Discover the right               │
    │    └─────────────────┘      solution to propose            │
    │                           │                                │
    │                           ▼                                │
    │    ┌─────────────────┐                                     │
    │    │    RESEARCH     │                                     │
    │    │   VALIDATION    │──── gate ──── or ────► stop         │
    │    └─────────────────┘                                     │
    │                           │                                │
    │                           ▼                                │
    │    ┌─────────────────┐                                     │
    │    │    RESEARCH     │          WHAT                        │
    │    │  INTELLIGENCE   │     Build the evidence               │
    │    └─────────────────┘      foundation                     │
    │                           │                                │
    │                           ▼                                │
    │    ┌─────────────────┐                                     │
    │    │    CONTENT      │          HOW                         │
    │    │   PRODUCTION    │     Deliver the solution             │
    │    └─────────────────┘      exceptionally well             │
    │                           │                                │
    │                           ▼                                │
    │    ┌─────────────────┐                                     │
    │    │  EDITORIAL QA   │──── gate ──── or ────► revise       │
    │    └─────────────────┘                                     │
    │                           │                                │
    │                           ▼                                │
    │    ┌─────────────────┐                                     │
    │    │   PUBLISHING    │          HOW                         │
    │    └─────────────────┘     Index, distribute, track        │
    │                           │                                │
    │                           ▼                                │
    │    ┌─────────────────┐                                     │
    │    │  PERFORMANCE    │          LEARN                       │
    │    │  INTELLIGENCE   │─── feedback ─────────────────────────┘
    │    └─────────────────┘          │
    │                                 │
    └─────────────────────────────────┘
```

The learning from HOW feeds back into WHY. Each cycle improves the next.

### 3.5 Relationship to WHY.md

`WHY.md` is the organizational manifesto. It explains why OLSP exists as a publisher, what it believes, and what it will not do. It is the philosophical foundation of the entire system.

The WHY layer inside the Editorial Operating System is different. It explains why a specific editorial opportunity deserves to become content. It is an operational question applied to individual topics, not a philosophical question applied to the organisation.

They are complementary:

| | WHY.md | WHY layer in the pipeline |
|---|--------|--------------------------|
| **Scope** | Organisational | Editorial |
| **Question** | Why does OLSP exist? | Why does this topic deserve an article? |
| **Applies to** | Everything the publisher does | Each individual editorial opportunity |
| **Changes when** | The publisher's mission changes | The community's needs change |

The pipeline's WHY layer operates within the boundaries set by WHY.md. No editorial opportunity may violate the organisational philosophy.

### 3.6 Editorial Principle

Many organisations begin with HOW. They choose a format, a platform, or a content type, and they optimise execution. Some organisations begin with WHAT. They identify a topic they want to cover and work backwards to the rationale.

The OLSP Editorial Operating System deliberately begins with WHY.

If we cannot explain why a reader benefits from a piece of content, the system should stop before Research Validation. No amount of excellent execution can rescue content that should not exist.

This ordering is enforced by the gates:

1. **Editorial Decision** enforces WHY. If the topic does not matter, stop.
2. **Research Validation** enforces WHAT. If the evidence does not support it, stop.
3. **Editorial QA** enforces HOW. If the execution does not meet standards, revise.

The three gates map to the three questions. Every gate must be passed before publication.

---

## 4. Final Editorial Pipeline

The editorial pipeline is a closed-loop system. Content originates from human communities and returns to them as solutions, generating new signals that feed back into discovery.

```
Human Communities
        │
        ▼
COMMUNITY INTELLIGENCE
  Discover what people actually discuss
        │
        ▼
EDITORIAL INTELLIGENCE
  Transform community knowledge into editorial opportunities
        │
        ▼
EDITORIAL DECISION
  Decide whether an opportunity deserves publication
        │
        ▼
OPPORTUNITY DISCOVERY
  Validate and prioritise community-derived opportunities
        │
        ▼
RESEARCH VALIDATION
  Verify demand, competition, feasibility, and legality
        │
        ▼
RESEARCH INTELLIGENCE
  Build the factual foundation for the article
        │
        ▼
CONTENT PRODUCTION
  Transform validated research into published content
        │
        ▼
EDITORIAL QA
  Verify accuracy, completeness, and editorial standards
        │
        ▼
PUBLISHING
  Index, distribute, and track the published article
        │
        ▼
PERFORMANCE INTELLIGENCE
  Collect performance data and community reactions
        │
        ▼
    (feedback loop returns to Community Intelligence)
```

### Pipeline rules

1. **No stage may be skipped.** Every article must pass through every stage sequentially.
2. **Any stage may reject an opportunity.** Rejection halts progress and returns the opportunity to the prior stage for re-evaluation or archival.
3. **The feedback loop is mandatory.** Performance data and new community signals are collected after publishing and fed back into Community Intelligence.
4. **Stages are independent.** Each stage produces a defined deliverable. No stage depends on the internal process of another stage.

---

## 5. Stage Specifications

### 5.1 Community Intelligence

**Purpose:** Discover what people actually discuss, ask, struggle with, and misunderstand across online communities. This is the origin point for every editorial opportunity. No topic enters the pipeline without first appearing in a community discussion.

**Inputs:**
- Reddit threads (r/Affiliatemarketing, r/marketing, r/sidehustle, r/juststart, r/passive_income, niche subreddits)
- Quora questions and answers
- Niche forum discussions
- (Planned: Facebook Groups, Discord, YouTube comments, X, LinkedIn, Amazon reviews, support tickets)

**Signals extracted:**
- Recurring questions (exact phrasing)
- Recurring frustrations (emotional language)
- Recurring misconceptions (stated as fact but incorrect)
- Recurring buying objections (reasons people do not buy)
- Recurring comparisons (products or approaches compared)
- Emerging discussions (new topics gaining traction)
- Unsolved problems (questions with no adequate answer)
- Self-reported failures ("I tried X for months and it did not work")
- Conflicting advice ("One person says X, another says Y")

**Discovery process:**
1. Community Discovery — identify active communities for the target niche
2. Question Mining — extract recurring questions with frequency and spread
3. Problem Mining — capture problems, frustrations, and emotional signals
4. Root Cause Analysis — separate symptom from cause
5. Solution Gap Analysis — determine why existing content fails
6. Opportunity Mapping — map each problem to editorial formats
7. Editorial Planning — produce recommended article list

**Outputs:**
- Community Intelligence Report (Executive Summary, Recurring Questions, Recurring Problems, Root Causes, Existing Content Failures, Can Content Solve This?, Can OLSP Help?, Opportunity Score, Editorial Angles, Recommended Articles, Cluster Recommendations, Community Source Log)

**Success criteria:**
- All recurring questions for the target niche are identified
- Root causes are distinguished from surface expressions
- Existing content failures are analysed, not assumed
- Every recommended article traces back to a specific community discussion
- Opportunity scores are assigned with rationale

**Failure criteria:**
- Insufficient community signal (fewer than 3 independent sources confirming the same question)
- Cannot determine root cause with confidence
- Existing content already answers the question adequately
- The problem cannot be solved by content

**Next stage:** Editorial Intelligence

**Required deliverables:**
- Community Intelligence Report (complete with all 12 sections)
- Raw source log (links to all community discussions consulted)

---

### 5.2 Editorial Intelligence

**Purpose:** Transform raw community knowledge into structured editorial opportunities. Community Intelligence surfaces what people discuss. Editorial Intelligence determines what those discussions mean for the editorial calendar.

**Inputs:**
- Community Intelligence Report
- Community Source Log

**Tasks:**
- Cluster related questions into topical groups (a single root problem often produces 3-5 related questions)
- Prioritise clusters by community frequency and emotional intensity
- Identify recurring narratives (the story the community keeps telling itself)
- Identify thematic gaps (topics the community should be discussing but is not)
- Generate article concepts from each cluster
- Recommend content format for each concept (review, roundup, guide, comparison, myth-busting, case study, troubleshooting)
- Estimate effort level for each concept (word count, research depth, complexity)

**Outputs:**
- Editorial Opportunity Map
  - Clustered opportunity groups with priority ranking
  - Article concepts with recommended formats
  - Narrative analysis (what the community believes, what it fears, what it wants)
  - Thematic gap analysis (missed opportunities the community has not yet articulated)

**Success criteria:**
- Every recurring question from the CI Report is assigned to a topical cluster
- Each cluster produces at least one article concept
- Content formats are matched to problem types (not arbitrarily chosen)
- Priority ranking reflects community intensity, not editorial preference

**Failure criteria:**
- Clusters are too broad (lumping unrelated questions together)
- Clusters are too narrow (treating every question as its own topic)
- Article concepts do not trace back to community signals
- Format recommendations do not fit the problem type

**Next stage:** Editorial Decision

**Required deliverables:**
- Editorial Opportunity Map
- Article concept briefs (one per recommended article)

---

### 5.3 Editorial Decision

**Purpose:** Decide whether each opportunity from Editorial Intelligence deserves to move forward into production. This is a gate. Not everything the community discusses is worth publishing.

**Inputs:**
- Editorial Opportunity Map
- Article concept briefs

**Evaluation criteria:**

| Criterion | Question |
|-----------|----------|
| Reader Value | Does this help a reader solve a real problem? |
| Business Value | Does this support the site's mission and positioning? |
| Evergreen Potential | Will this content be useful 12 months from now? |
| Authority Potential | Can this content establish or reinforce topical authority? |
| OLSP Fit | Can OLSP be positioned as part of the solution naturally? |
| Differentiation | Can we produce something genuinely better than existing content? |

**Decisions:**

| Decision | Meaning |
|----------|---------|
| Publish | Proceed to Opportunity Discovery |
| Research Further | Returns to Editorial Intelligence for more analysis |
| Reject | Opportunity is archived. May be revisited if community signals change. |
| Hold | Deferred. Will be re-evaluated at the next editorial cycle. |

**Outputs:**
- Approved opportunity list with rationale for each approval
- Rejected opportunity log with rationale for each rejection
- Research Further requests sent back to Editorial Intelligence

**Success criteria:**
- Every approved opportunity has a clear rationale across all 6 evaluation criteria
- Rejections are documented with specific reasoning (not "not a fit")
- The pass-through rate is tracked (what percentage of opportunities are approved)

**Failure criteria:**
- Opportunities approved without clear reader value
- Opportunities rejected for reasons that contradict the editorial philosophy
- Editorial preference overrides community signals

**Next stage:** Opportunity Discovery (for approved opportunities)

**Required deliverables:**
- Approved opportunity list
- Rejected opportunity log
- Hold queue

---

### 5.4 Opportunity Discovery

**Purpose:** Validate and structure approved editorial opportunities. This stage does not invent topics. It only prioritises, scores, clusters, and recommends.

**Inputs:**
- Approved opportunity list
- Article concept briefs

**Tasks:**
- Prioritise opportunities by combined community intensity and editorial value
- Score opportunities against editorial criteria (standardised scoring rubric)
- Cluster related opportunities into content groups for coordinated production
- Recommend content structure for each opportunity

**Outputs:**
- Opportunity Brief (one per approved opportunity)
  - Working title
  - Primary question answered
  - Root problem addressed
  - Target audience
  - Recommended format and structure
  - Related questions to address within the article
  - Candidate affiliate products for natural integration
  - Internal linking candidates
  - Priority score

**Success criteria:**
- Every opportunity has a complete Opportunity Brief before proceeding
- Priority scores are consistent and reproducible
- Clusters are internally coherent

**Failure criteria:**
- Topics are invented (not traced to a community signal)
- Briefs lack sufficient detail for the next stage
- Priority scoring is inconsistent

**Next stage:** Research Validation

**Required deliverables:**
- Opportunity Brief (one per approved opportunity)

---

### 5.5 Research Validation

**Purpose:** Verify that an opportunity is viable before committing to full research and production. This is the search-side gate that complements the Editorial Decision gate.

**Inputs:**
- Opportunity Brief

**Validation checks:**

| Check | Method | Minimum threshold |
|-------|--------|-------------------|
| Search demand | Keyword research tools, search volume estimates | Sufficient to justify effort |
| Competition analysis | SERP review, competitor content assessment | Gap exists or we can differentiate |
| Affiliate opportunities | Affiliate network search, program availability | At least one relevant program |
| Official sources | Manufacturer, vendor, or platform documentation | Available and accessible |
| Scientific / evidence base | Academic or industry research (for claims-heavy topics) | Verifiable evidence exists |
| Legal considerations | Regulatory compliance, disclosure requirements | No legal risks identified |
| Content feasibility | Can we produce better content than what exists? | Yes, with available resources |

**Decisions:**

| Decision | Meaning |
|----------|---------|
| Continue | Proceed to Research Intelligence |
| Hold | Demand is insufficient now; revisit in 3-6 months |
| Reject | Opportunity is not viable; return to Opportunity Discovery or archive |

**Outputs:**
- Validation report with pass/fail for each check
- Decision with rationale

**Success criteria:**
- Every validation check is completed before a decision is made
- Decisions are supported by data, not intuition
- Hold/Reject decisions include conditions for re-evaluation

**Failure criteria:**
- Validation checks are skipped or performed superficially
- Search demand is assumed without verification
- Competition is not assessed
- Legal considerations are ignored

**Next stage:** Research Intelligence (for validated opportunities)

**Required deliverables:**
- Validation report
- Decision and rationale

---

### 5.6 Research Intelligence

**Purpose:** Build the factual foundation that the article will be written from. No assumptions. No invention. Only verified evidence.

**Inputs:**
- Opportunity Brief
- Validation report
- Community source log

**Tasks:**
- Collect primary source documentation (official sites, documentation, pricing pages, terms of service)
- Collect third-party source material (news articles, analyst reports, independent reviews)
- Collect community source material (relevant threads, quoted user experiences)
- Build evidence library (organised collection of all sources with reliability labels)
- Build source list (all sources that will be cited in the article)
- Produce fact summary (key claims the article must address, with verified answers)
- Identify knowledge gaps (claims that could not be verified — must be labelled in the article)

**Outputs:**
- Research Brief
- Evidence Library
- Source List
- Fact Summary
- Knowledge Gap Log

**Success criteria:**
- Every claim the article will make is supported by a source in the Evidence Library
- Sources are labelled by reliability (verified, vendor claim, third-party, self-reported, unverified)
- Knowledge gaps are identified and documented (not hidden)
- The Research Brief is complete enough that the writer does not need to conduct additional research

**Failure criteria:**
- Sources are not labelled by reliability
- Knowledge gaps are not documented
- The Research Brief is incomplete (writer must conduct additional research)
- Sources are not diverse (single-source dependence)

**Next stage:** Content Production

**Required deliverables:**
- Research Brief
- Evidence Library
- Source List
- Fact Summary
- Knowledge Gap Log

---

### 5.7 Content Production

**Purpose:** Transform validated research into published content. The writer works from the Research Brief, Evidence Library, and Source List. No additional research. No assumptions. No invention.

**Inputs:**
- Research Brief
- Evidence Library
- Source List
- Fact Summary
- Knowledge Gap Log
- Appropriate Gold Master specification (GOLD-MASTER-SPEC.md for reviews, ROUNDUP-GOLD-MASTER-SPEC.md for roundups)

**Tasks:**
- Structure the article according to the appropriate Gold Master
- Write from the Evidence Library (no external supplementation)
- Label every factual claim according to the source reliability system
- Integrate internal links where they add value
- Integrate affiliate links where they are natural and transparent
- Include community-sourced context (the question, the frustration, the emotional weight)
- Produce complete, publish-ready content

**Outputs:**
- Complete article file (`.astro` for reviews/roundups, `.html` or `.md` for informational/authority articles)

**Success criteria:**
- All content traces directly to the Evidence Library
- Every factual claim is labelled by source reliability
- The article answers the question identified in the Opportunity Brief
- The article addresses the root cause, not just the surface question
- Community language and context are woven into the content
- The article is complete and requires no structural edits

**Failure criteria:**
- Claims made without source support
- Source reliability labels are missing
- The article does not answer the original community question
- The writer supplemented research from their own knowledge without labelling it
- The article sounds like it was generated, not written

**Next stage:** Editorial QA

**Required deliverables:**
- Complete, publish-ready article file

---

### 5.8 Editorial QA

**Purpose:** Verify that the article meets editorial standards before publication.

**Inputs:**
- Complete article file
- Research Brief, Evidence Library, Source List, Fact Summary, Knowledge Gap Log
- Appropriate Gold Master specification

**Validation checks:**

| Check | What to verify |
|-------|----------------|
| Accuracy | Every factual claim matches its source |
| Completeness | All sections from the Gold Master are present and populated |
| Readability | The article is clear, well-structured, and appropriately toned |
| Editorial standards | All editorial rules are followed (epistemic labelling, no invented testing, income claims labelled) |
| Internal links | All internal links are correct and add value |
| CTA | Call to action is present, natural, and appropriate |
| Formatting | Headings, lists, tables, and components meet the Gold Master standard |
| Source fidelity | No claims go beyond what the research supports |
| Affiliate compliance | Links use correct `rel` attributes, disclosures are present |
| Brand consistency | Tone matches the site's editorial voice |

**Outputs:**
- Publication Approval (if all checks pass)
- Revision Request (if any check fails, with specific items to fix)

**Success criteria:**
- All validation checks pass before publication approval is issued
- Every revision request is specific and actionable
- The QA process catches errors before they reach production

**Failure criteria:**
- Validation checks are performed superficially
- Errors reach production that should have been caught
- Revision requests are vague or unactionable
- QA is skipped or rushed

**Next stage:** Publishing

**Required deliverables:**
- Publication Approval or Revision Request

---

### 5.9 Publishing

**Purpose:** Make the article live, indexed, discoverable, and tracked.

**Inputs:**
- Approved article file
- Publication Approval

**Tasks:**
- Deploy the article to the production environment
- Verify the article renders correctly in production
- Submit to Google Search Console for indexing
- Distribute through appropriate channels (newsletter, social, community)
- Add internal links from related existing content
- Set up tracking (analytics, search console, conversion tracking)

**Outputs:**
- Published, indexed, live article
- Distribution log
- Internal linking update log

**Success criteria:**
- Article is live and renders correctly across devices and browsers
- Article is submitted for indexing within 24 hours of publication
- Internal links from related content are in place
- Tracking is verified to be working

**Failure criteria:**
- Article goes live with rendering errors
- Article is not indexed within 7 days
- Internal links are not updated
- Tracking is not verified

**Next stage:** Performance Intelligence

**Required deliverables:**
- Live published article
- Confirmation of indexing submission
- Confirmation of distribution
- Confirmation of internal linking

---

### 5.10 Performance Intelligence

**Purpose:** Collect performance data and community reactions to the published article, then feed everything back into Community Intelligence for the next cycle.

**Inputs:**
- Published article URL
- Analytics data (Google Search Console, site analytics)
- Community monitoring (Reddit, Quora, forums — for mentions of the article or its topic)

**Data collected:**

| Source | Data |
|--------|------|
| Search Console | Impressions, clicks, CTR, average position, queries |
| Site analytics | Pageviews, time on page, bounce rate, conversions |
| Community reactions | New mentions of the article, new questions about the topic, new objections, new misconceptions |
| Comments | Reader questions, criticisms, corrections, thanks |

**Tasks:**
- Collect performance metrics 30, 60, and 90 days after publication
- Monitor communities for new signals related to the article's topic
- Identify new questions the article did not answer
- Identify new objections the article did not address
- Identify new misconceptions that emerged since publication
- Feed all new signals into the next Community Intelligence cycle

**Outputs:**
- Performance Report (30/60/90 day metrics)
- New Signal Report (new questions, objections, misconceptions, opportunities)
- Community feedback log

**Success criteria:**
- Performance data is collected at all three checkpoints
- New community signals are identified and documented
- The feedback loop delivers new signals to Community Intelligence

**Failure criteria:**
- Performance data is not collected
- Community signals are not monitored
- The feedback loop is broken (new signals do not reach Community Intelligence)
- Data is collected but not acted upon

**Next stage:** Community Intelligence (feedback loop returns to the start)

**Required deliverables:**
- Performance Report
- New Signal Report
- Community feedback log

---

## 6. Intelligence Relationships

The AI Editorial Operating System contains five intelligence functions that interact throughout the pipeline.

### 6.1 Community Intelligence

**Role:** Discovery

**What it produces:** Raw audience insight — what people are discussing, asking, struggling with, and misunderstanding.

**Relationship to others:** Feeds into Editorial Intelligence. Receives feedback from Performance Intelligence.

**Position:** Pipeline origin and feedback destination.

### 6.2 Editorial Intelligence

**Role:** Transformation

**What it produces:** Structured editorial opportunities — clustered, prioritised, formatted, and scoped.

**Relationship to others:** Receives raw insight from Community Intelligence. Feeds into Editorial Decision.

**Position:** Second stage. The bridge between raw data and editorial action.

### 6.3 Opportunity Discovery

**Role:** Validation and prioritisation

**What it produces:** Validated opportunity briefs — scored, structured, and ready for research.

**Relationship to others:** Receives approved opportunities from Editorial Decision. Feeds into Research Validation.

**Position:** Fourth stage (after Editorial Decision gate). Does not invent topics — only processes what earlier stages produced.

### 6.4 Research Intelligence

**Role:** Evidence foundation

**What it produces:** Verified evidence — a complete factual foundation for the article.

**Relationship to others:** Receives validated Opportunity Brief. Feeds into Content Production.

**Position:** Sixth stage (after Research Validation gate). The last stage before content creation.

### 6.5 Performance Intelligence

**Role:** Measurement and feedback

**What it produces:** Performance data and new community signals.

**Relationship to others:** Receives published article data. Feeds back into Community Intelligence.

**Position:** Tenth and final stage. Closes the loop.

### Information flow diagram

```
CI ──raw insight──► EI ──opportunities──► ED ──approved──► OD ──briefs──► RV
 ▲                                                                           │
 │                                                                           ▼
 │                                                                        RI ──evidence──► CP ──content──► EQ ──approved──► P ──data──► PI
 │                                                                                                              │
 └────────────────────────────────────────feedback (new signals)───────────────────────────────────────────────┘
```

---

## 7. Editorial Principles

These principles govern every stage of the pipeline. They are not optional.

### 7.1 We do not chase keywords

A keyword with high search volume is not a reason to publish. The only reason to publish is that a real person has a real problem and our article can help. Keywords validate demand after the fact. They do not create editorial direction.

### 7.2 We solve problems

Every article exists to solve a specific problem that was identified in a community discussion. If the problem is not real, specific, and unresolved, the article does not get written.

### 7.3 We do not publish because volume exists

Search volume is a gate, not a source. An opportunity passes through search validation to confirm that enough people search for the topic to justify the effort. But the opportunity itself was born in a community discussion, not in a keyword tool.

### 7.4 We publish because readers benefit

The ultimate measure of an article is whether it helps its reader. Not whether it ranks. Not whether it converts. Not whether it generates traffic. Whether it helps the specific person who arrived with a specific question.

### 7.5 Authority comes from research

Authority is not declared. It is demonstrated through the quality of evidence presented. Every claim supported by a reliable source builds authority. Every claim made without support erodes it.

### 7.6 Trust comes from honesty

Trust is built by being honest about what we know and what we do not know. Knowledge gaps are disclosed. Unverified claims are labelled. Vendor claims are distinguished from verified facts. Income figures are never presented as typical.

### 7.7 Community drives the editorial calendar

The editorial calendar is a response to community signals, not a predetermined schedule. If the community is discussing X, the calendar shifts to X. If the community has no questions about Y, Y is not published regardless of its search volume.

### 7.8 Performance improves future decisions

Data from published articles feeds back into the system. What worked is repeated. What did not work is examined. New questions that emerged after publication become new opportunities. The system learns.

### 7.9 Epistemic rigour is non-negotiable

Every factual claim in published content must carry an implicit or explicit reliability label. Readers must be able to distinguish between verified facts, vendor claims, third-party reports, and editorial analysis. This is not optional for SEO or convenience.

### 7.10 No invention

Nothing is invented. Not testing. Not personal experience. Not screenshots. Not testimonials. Not benchmarks. Not conclusions. If it cannot be supported by the evidence, it does not appear in the content.

---

## 8. Pipeline Governance

### 8.1 Stage transitions

Each stage transition requires a deliverable handoff. No stage begins until the prior stage's deliverable is approved.

| From | To | Required handoff |
|------|----|------------------|
| Community Intelligence | Editorial Intelligence | Community Intelligence Report |
| Editorial Intelligence | Editorial Decision | Editorial Opportunity Map |
| Editorial Decision | Opportunity Discovery | Approved opportunity list |
| Opportunity Discovery | Research Validation | Opportunity Brief |
| Research Validation | Research Intelligence | Validation report ("Continue" decision) |
| Research Intelligence | Content Production | Research Brief + Evidence Library + Source List |
| Content Production | Editorial QA | Complete article file |
| Editorial QA | Publishing | Publication Approval |
| Publishing | Performance Intelligence | Published article URL + tracking setup |
| Performance Intelligence | Community Intelligence | Performance Report + New Signal Report |

### 8.2 Rejection handling

Any stage may reject an opportunity. Rejection handling follows these rules:

- **Rejection reason must be documented.** Vague rejections ("not a fit") are not permitted.
- **Rejected opportunities are archived with conditions for re-evaluation.**
- **Rejected opportunities may be re-submitted** if new community signals or search data warrant reconsideration.
- **Stage bypass is not permitted.** An opportunity cannot skip a stage by being rejected and re-submitted at a later stage.

### 8.3 Feedback loop governance

The feedback loop from Performance Intelligence to Community Intelligence is mandatory:

- Performance data must be collected at 30, 60, and 90 days post-publication
- New community signals must be monitored starting 30 days post-publication
- A New Signal Report is produced at each checkpoint
- New signals enter the pipeline as fresh Community Intelligence inputs (not modifications to the original article)
- The original article may be updated if new signals indicate factual errors or significant gaps

---

## 9. Future Expansion

The following capabilities are reserved for future implementation. They are documented here for architectural awareness. No implementation work is planned.

### 9.1 Automated Community Crawling

Periodic automated collection of community discussions from Reddit, Quora, niche forums, and other sources. Collected data stored for analysis without real-time API dependencies. Would reduce manual discovery effort and increase signal volume.

### 9.2 Sentiment Analysis

Natural language processing to classify community posts by emotional valence (positive, negative, neutral), emotional intensity (frustrated, curious, satisfied), and intent category (information, purchase, troubleshooting, comparison).

### 9.3 Discussion Clustering

Automated grouping of similar questions and problems across sources using semantic similarity matching, FAQ clustering algorithms, and topic modelling. A single root problem expressed in 50 different ways across 10 communities would be automatically clustered into one opportunity.

### 9.4 Trend Detection

Identification of rising question frequency (a problem growing in importance), new terminology (emerging concepts), shifting sentiment (a previously accepted solution falling out of favour), and seasonal patterns (questions that recur on a schedule).

### 9.5 Knowledge Graph

A structured graph of known topics, questions, entities, and their relationships. Would enable the system to understand what it already knows, what it has already published, and where gaps exist. Would prevent redundant production and identify cluster opportunities automatically.

### 9.6 Editorial Memory

The system would retain knowledge of past editorial decisions, performance outcomes, and community signals across publishing cycles. Would reduce duplicate analysis and enable the system to build on past work rather than rediscovering it each cycle.

### 9.7 AI Prioritisation

ML-based opportunity scoring trained on historical performance data. Would predict likely search demand, optimal content format, and conversion probability for community-identified questions. Would augment (not replace) human editorial judgement.

### 9.8 Feedback Loop Automation

Automated collection of performance data from Search Console and analytics. Automated community monitoring for new signals related to published topics. Automated generation of New Signal Reports. Human review remains for editorial decisions.

### 9.9 Human Review Requirement

All future expansion, regardless of automation level, must preserve human review at key decision points: Editorial Decision, Editorial QA, and final performance analysis. Automation supports discovery and analysis. Editorial judgement remains with humans.

---

## 10. Acceptance Criteria

This document is the definitive reference for the AI Editorial Operating System when:

1. It clearly articulates the editorial philosophy (Human First, Problems Before Keywords, Research Before Opinion, Publish Only Valuable Content)
2. It documents the complete editorial pipeline from Human Communities through the Performance Intelligence feedback loop
3. It specifies every stage with Purpose, Inputs, Outputs, Success Criteria, Failure Criteria, Next Stage, and Required Deliverables
4. It shows the full feedback loop: Performance Intelligence feeds back into Community Intelligence
5. It explains why Community Intelligence precedes Opportunity Discovery (problems before keywords)
6. It documents how opportunities emerge from community problems, not keyword volume
7. It defines the relationship between all five intelligence functions
8. It establishes editorial principles that govern every stage of the pipeline
9. It covers pipeline governance (stage transitions, rejection handling, feedback loop rules)
10. It reserves future expansion capabilities without specifying implementation
11. It is structured so that future agents, prompts, and workflows can be derived from it

Future agents and prompts should reference this document as their source of authority. Any conflict between this document and a derived artifact should be resolved in favour of this document.

---

*End of AI Editorial Operating System v2 — Canonical Reference*

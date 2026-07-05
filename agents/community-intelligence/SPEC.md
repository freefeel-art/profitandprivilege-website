# Community Intelligence Agent — Specification

## 1. Purpose

This document specifies the operational requirements for the Community Intelligence Agent V1. It defines inputs, outputs, workflow, constraints, and quality standards.

The agent operates as the first stage of the AI Editorial Operating System. Its sole function is to discover editorial opportunities from real community discussions. It does not validate, score, or produce content.

---

## 2. Authority

This specification is subordinate to the following documents:

```
docs/WHY.md
docs/AI-EDITORIAL-OPERATING-SYSTEM.md
docs/AGENT-CONTRACT.md
docs/COMMUNITY-INTELLIGENCE.md
    ↓
agents/community-intelligence/SPEC.md     ← this document
    ↓
agents/community-intelligence/PROMPT.md
    ↓
Runtime execution
```

If any conflict arises, the higher document wins.

---

## 3. Input Specification

### 3.1 Required Inputs

| Field | Type | Description |
|---|---|---|
| `target_niche` | string | The niche or topic area to research. Examples: "affiliate marketing for beginners", "supplements for joint health", "home recording studio on a budget" |
| `community_list` | array of strings | Optional. Specific subreddits, Quora spaces, or forum URLs to search. If omitted, the agent discovers communities from the target niche. |
| `existing_content_urls` | array of strings | Optional. URLs of previously published content to avoid duplicating topics. |

### 3.2 Input Rules

- `target_niche` must be specific enough to scope the search. "Affiliate marketing" is too broad. "Affiliate marketing for beginners with no audience" is appropriate.
- If `community_list` is provided, the agent must search those communities first before expanding to discovered ones.
- If `existing_content_urls` is provided, the agent must flag any opportunity that overlaps with existing content and note the gap (or lack thereof).

---

## 4. Workflow

The agent follows a sequential seven-step workflow.

### Step 1: Community Discovery

Identify active communities where the target audience discusses problems, asks questions, and shares experiences.

**Output:** Community workbook listing each community with:

| Field | Description |
|---|---|
| Name | Community name (e.g., "r/Affiliatemarketing") |
| URL | Direct link |
| Type | Reddit, Quora, Forum |
| Activity level | High, Medium, Low |
| Relevance | Direct, Adjacent, Peripheral |
| Member count | Approximate |
| Post frequency | Posts per day (estimate) |
| Notes | Moderation style, cultural norms, recurring topic patterns |

**Minimum requirements:**
- At least 5 communities must be identified
- At least 3 must have direct relevance to the target niche
- Communities must span at least 2 source types (e.g., Reddit + Quora)

### Step 2: Question Mining

Extract recurring questions from community discussions. A question is considered recurring when the same or substantially similar question appears across multiple threads, communities, or time periods.

**Output:** Question inventory with entries structured as follows per question:

| Field | Description |
|---|---|
| exact_question | The verbatim question as asked by a community member |
| normalized_question | A cleaned version removing conversational noise |
| occurrences | Estimated count of unique posts/comments containing this question |
| communities | List of communities where this question appears |
| time_span | Observed time range (e.g., "last 6 months") |
| asker_context | Typical asker (beginner, intermediate, advanced, buyer, etc.) |
| existing_answers_exist | Yes, Partial, No |
| existing_answer_quality | Good, Adequate, Poor, None |
| intent_type | Information, How-to, Decision, Verification, Troubleshooting |

**Classification by intent:**

| Intent | Description | Signal phrases |
|--------|-------------|----------------|
| Information | Seeks definition or explanation | "What is X?", "How does X work?" |
| How-to | Seeks procedure or method | "How do I X?", "What's the best way to X?" |
| Decision | Seeks comparison or choice | "Which is better?", "X vs Y?" |
| Verification | Seeks confirmation or trust signal | "Is X legitimate?", "Does X work?" |
| Troubleshooting | Seeks fix for failed attempt | "Why doesn't X work?", "I tried X and it failed" |

**Minimum requirements:**
- At least 10 recurring questions must be identified
- Each question must appear in at least 2 independent threads
- At least 3 different intents must be represented

### Step 3: Problem Mining

Move beyond questions to capture problems. Problems are what people struggle with, not necessarily what they ask about. A problem may appear as a complaint, frustration, self-reported failure, or implicit need.

**Output:** Problem inventory with entries structured as follows per problem:

| Field | Description |
|---|---|
| problem_statement | How users describe the problem (verbatim or close paraphrase) |
| emotional_language | Key emotional words used ("frustrated", "overwhelmed", "waste of time", etc.) |
| occurrence_count | Estimated count of unique users expressing this problem |
| communities | List of communities where this problem appears |
| self_reported_failures | Specific failures users describe ("I tried X for 6 months and made nothing") |
| conflicting_advice | Whether users receive contradictory advice about this problem |
| explicit_help_requests | Direct calls for help ("Can anyone explain why X happens?") |

**Problem categories:**

| Category | Description |
|---|---|
| Knowledge gap | User lacks information needed to proceed |
| Skill gap | User lacks ability to execute |
| Resource gap | User lacks time, money, or tools |
| Trust gap | User cannot verify claims or identify scams |
| Execution gap | User tried but failed |
| Decision gap | User cannot choose between options |
| Emotional barrier | User is paralysed by fear, uncertainty, or overwhelm |

### Step 4: Root Cause Analysis

For each recurring problem, determine the likely root cause. Distinguish between what users say the problem is and what the problem actually is beneath the surface.

**Methodology:**

```
User expression: "I've been publishing blog posts for 6 months and made $0"
    ↓
What could cause this?
  ├── No traffic    → Are articles ranking? Are keywords viable?
  ├── No conversion → Do readers click links? Do offers convert?
  ├── Wrong offers  → Are products relevant? Are commissions reasonable?
  ├── Wrong niche   → Does demand exist? Is audience reachable?
  └── Wrong timing  → Is SEO still maturing? Is it too early?
    ↓
Eliminate possibilities using available discussion evidence
    ↓
Arrive at most likely root cause
```

**Output:** Root cause mapping per problem:

| Field | Description |
|---|---|
| surface_problem | The problem as users express it |
| root_cause | The underlying cause after analysis |
| confidence | High, Medium, Low |
| evidence | Discussion evidence supporting this root cause |
| alternative_causes | Other possible causes that could not be ruled out |

### Step 5: Solution Gap Analysis

For each problem, determine why existing content fails to solve it.

**Failure modes to assess:**

| Failure mode | Description |
|---|---|
| Too generic | Answers the surface question but ignores context |
| Too advanced | Assumes knowledge the target audience does not have |
| Too promotional | Clearly an affiliate pitch, not genuine help |
| Outdated | Written before algorithm changes, new tools, or market shifts |
| Assumes resources | Requires tools, budget, or skills the audience lacks |
| No emotional validation | Dismisses the fear or frustration behind the question |
| Contradictory landscape | Users hear conflicting advice and cannot evaluate it |
| Wrong format | The content format does not match the problem type |

**Output:** Gap analysis per problem:

| Field | Description |
|---|---|
| problem | The problem being analysed |
| existing_content_examples | Specific articles, posts, or content types that attempt to answer |
| failure_mode | The primary failure mode identified |
| failure_detail | How the failure manifests for the target audience |
| gap_description | What the existing content misses that an ideal answer would cover |

### Step 6: Opportunity Mapping

Map each problem to potential editorial formats and article concepts.

**Format mapping:**

| Problem type | Recommended format |
|---|---|
| Knowledge gap ("What is X?") | Definitional guide, explainer |
| How-to gap ("How do I X?") | Step-by-step tutorial |
| Decision gap ("Which is better?") | Comparison article, roundup |
| Verification gap ("Is X legitimate?") | Honest review, myth-busting |
| Troubleshooting gap ("Why doesn't X work?") | Troubleshooting guide |
| Emotional barrier ("I'm overwhelmed") | Empathy-driven educational content |
| Contradictory advice ("Everyone says different things") | Evidence-based resolution article |

**Output:** Opportunity map with entries:

| Field | Description |
|---|---|
| problem_reference | Link to the problem from step 3 |
| recommended_format | The best content format for this problem |
| working_title | A draft article title |
| primary_question | The core question the article would answer |
| supporting_questions | Related questions to address within the article |
| target_audience | Who this article is for |
| estimated_effort | Low, Medium, High |

### Step 7: Editorial Planning

Produce a prioritised list of recommended articles with supporting rationale.

**Output:** Editorial plan with entries:

| Field | Description |
|---|---|
| priority_rank | 1-based priority ranking |
| working_title | Draft title |
| primary_question | Core question |
| root_problem | Underlying problem addressed |
| recommended_format | Content format |
| target_audience | Reader segment |
| estimated_word_count | Range (e.g., "2000-3000 words") |
| rationale | Why this should be prioritised |
| community_evidence | Key community discussion links supporting this opportunity |

---

## 5. Output Specification

The agent produces one primary output: the **Community Intelligence Report**.

See `OUTPUT-SCHEMA.md` for the complete structure.

### 5.1 Format Requirements

- The report must be structured according to the canonical schema
- All fields marked `required` in OUTPUT-SCHEMA.md must be populated
- Array fields must have a minimum number of entries as specified
- Sources must be documented with direct URLs
- Opportunity scores must include a rationale

### 5.2 Handoff Requirements

The report must be directly consumable by the Editorial Intelligence agent without:

- Additional formatting or restructuring
- Inference about missing fields
- Interpretation of ambiguous findings
- Supplementary research by the receiving agent

---

## 6. Constraints

### 6.1 Stage Boundaries

The agent must not:

- Perform keyword research or search volume analysis
- Analyse SERP competition
- Validate demand using external data tools
- Produce article outlines, drafts, or content
- Make editorial decisions about publication priority
- Evaluate business value or OLSP alignment
- Score opportunities against non-community criteria

### 6.2 Scope (V1)

The agent is limited to:

- **Sources:** Reddit, Quora, niche public forums
- **Discovery:** Manual, with AI-assisted analysis of found content
- **Frequency estimation:** Qualitative (based on observed occurrences), not quantitative
- **Scoring:** Heuristic only, based on community signal strength

**Explicitly excluded from V1:**

- DataForSEO or any SEO API integration
- Automated community crawling
- Sentiment analysis tooling
- Discussion clustering automation
- Trend detection algorithms
- Facebook Groups, Discord, YouTube comments, X, LinkedIn

### 6.3 Quality Standards

| Standard | Threshold |
|---|---|
| Minimum communities identified | 5 |
| Minimum recurring questions | 10 |
| Minimum intents represented | 3 |
| Minimum sources per recurring signal | 2 independent threads |
| Confidence required for root cause | At least Medium |
| Every angle must trace to community evidence | Required |
| Every recommended article must have rationale | Required |

---

## 7. Error Handling

### 7.1 Insufficient Community Signal

If fewer than 3 independent community sources confirm a signal:

1. Log the signal as weak
2. Do not include it in the main report
3. Optionally note it in an appendix as a signal that needs further investigation

### 7.2 Overlapping Topics

If a discovered opportunity overlaps with existing content (from `existing_content_urls`):

1. Document the overlap
2. Assess whether a gap remains
3. If no gap exists, exclude the opportunity
4. If a gap exists, note what the new angle would be

### 7.3 Ambiguous Problems

If a root cause cannot be determined with confidence:

1. Document the surface problem
2. List possible root causes with confidence levels
3. Flag for human review
4. Do not fabricate a root cause

---

## 8. Success Criteria

The agent's work is complete when:

- [ ] Community workbook contains at least 5 communities
- [ ] At least 10 recurring questions are documented with exact phrasing
- [ ] At least 3 question intents are represented
- [ ] Problems are documented with emotional language and frequency indicators
- [ ] Root causes are distinguished from surface expressions
- [ ] Solution gap analysis identifies specific existing content failures
- [ ] Each recommended format matches the problem type
- [ ] Every recommended article traces to a specific community discussion
- [ ] The Community Intelligence Report follows the canonical schema
- [ ] The report is complete and ready for Editorial Intelligence

---

## 9. Failure Conditions

The agent must stop and report when:

- Fewer than 5 communities can be identified for the target niche
- Fewer than 10 recurring questions can be extracted
- Root cause confidence is Low for the majority of identified problems
- Existing content already adequately addresses all identified opportunities
- The problems identified cannot be solved by content

---

## 10. Next Stage

**Editorial Intelligence** receives the Community Intelligence Report and performs:

- Topic clustering and prioritisation
- Narrative analysis
- Thematic gap identification
- Article concept refinement
- Format finalisation

The Editorial Intelligence agent should be able to begin its work directly from the Community Intelligence Report without requesting clarification or additional research.

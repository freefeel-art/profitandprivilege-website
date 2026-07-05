# Community Intelligence Report — Output Schema

This document defines the canonical structure of a Community Intelligence Report. Every report produced by the Community Intelligence Agent must conform to this schema.

---

## Identifier System

Every reusable object in a Community Intelligence Report receives a stable, deterministic identifier.

### ID Format

```
{PREFIX}-{NNN}
```

Where `{PREFIX}` is a three-letter type code and `{NNN}` is a zero-padded three-digit sequence number (001, 002, ..., 999).

### ID Prefixes

| Prefix | ID Type | Defining Section | Assignment |
|--------|---------|-----------------|------------|
| `COM` | community_id | Section 2 — Community Workbook | Sequential in workbook order |
| `THR` | thread_id | Section 13 — Community Source Log | Sequential in source log order |
| `FND` | finding_id | Section 3 — Recurring Questions, then Section 4 — Recurring Problems | Sequential in order of first appearance. Q1 → FND-001, Q2 → FND-002, P1 → FND-011, etc. |
| `OPP` | opportunity_id | Section 9 — Opportunity Scores | Sequential in score priority order |
| `CLU` | cluster_id | Section 12 — Cluster Recommendations | Sequential in cluster order |

### Determinism Rules

1. **IDs are assigned during report generation, based on the canonical section order defined in this schema.** The order of sections is fixed. IDs derived from a section's entry order are therefore deterministic for a given set of findings.
2. **IDs remain stable if sections are reordered in display or export.** An ID is assigned from its defining section (the section where the object is created), not from the section where it is referenced. Moving section 5 before section 3 does not change any ID.
3. **Finding IDs follow a two-phase assignment:** Questions in Section 3 receive FND-001 through FND-N. Problems in Section 4 continue the sequence (FND-N+1 onward). This prevents ID collision and preserves a stable sequence within each report.
4. **IDs are never reused.** If a finding is removed during revision, its ID is retired and not reassigned.
5. **Cross-section references use IDs, not text.** A Root Cause entry references `finding_id: "FND-003"` rather than repeating the problem statement. This prevents drift if problem wording is refined.

### ID Reservation

Each report reserves 100 IDs per prefix (except FND, which reserves 200). This accommodates inserts during revision without renumbering.

| ID Type | Reserved Range | Practical Limit |
|---------|---------------|-----------------|
| community_id | COM-001 — COM-099 | 99 communities |
| thread_id | THR-001 — THR-999 | 999 threads |
| finding_id | FND-001 — FND-999 | 999 findings |
| opportunity_id | OPP-001 — OPP-099 | 99 opportunities |
| cluster_id | CLU-001 — CLU-099 | 99 clusters |

---

## Traceability Requirements

Every finding entry must carry its own traceability chain. A downstream agent must never need to infer where a finding originated.

### Required Traceability Fields

Every entry in Sections 3, 4, 5, 6, 7, and 8 must include:

| Field | Type | Description |
|-------|------|-------------|
| `finding_id` | `string` (FND-NNN) | Stable identifier for this finding |
| `originating_community_id` | `string` (COM-NNN) | The primary community where this finding was observed |
| `originating_thread_id` | `string` (THR-NNN) | The primary thread where this finding was first or most clearly observed |
| `evidence_snippet` | `string` | A verbatim or close-paraphrase snippet from the discussion that grounds this finding |
| `confidence` | `enum: High \| Medium \| Low` | How confident the agent is in this finding based on available evidence |
| `section_first_appeared` | `integer` | The section number where this finding is primarily defined (3 for questions, 4 for problems, etc.) |

### Traceability Inheritance

- **Section 3 (Questions)** and **Section 4 (Problems)** are primary findings. They carry full traceability.
- **Section 5 (Root Causes)** and **Section 6 (Content Failures)** are derived findings. They link to their source finding via `finding_id` and repeat the traceability fields for self-contained consumption.
- **Sections 7 (Feasibility Gate)** and **8 (Alignment Gate)** are gates applied to findings. They reference the source `finding_id` and carry abbreviated traceability (confidence and evidence only, since community/thread are inherited).
- **Sections 9 (Scores), 10 (Angles), 11 (Articles)** are synthetic. They reference `opportunity_id` and `finding_id` but do not carry independent traceability — they are aggregations.
- **Section 12 (Clusters)** references `cluster_id` and lists article references.
- **Section 13 (Source Log)** is the thread-level audit trail. Every thread referenced anywhere in the report appears here with its `thread_id`.

### Traceability Rule

If a finding appears in a section that is not its defining section, it MUST carry its `finding_id` so a reader or downstream agent can locate its full traceability chain in the defining section.

---

## Report Structure

```
Community Intelligence Report
├── 1. Executive Summary
├── 2. Community Workbook
├── 3. Recurring Questions
├── 4. Recurring Problems
├── 5. Root Cause Analysis
├── 6. Existing Content Failures
├── 7. Solution Feasibility Gate
├── 8. OLSP Alignment Gate
├── 9. Opportunity Scores
├── 10. Editorial Angles
├── 11. Recommended Articles
├── 12. Cluster Recommendations
└── 13. Community Source Log
```

---

## 1. Executive Summary

### Schema

```yaml
section: "1. Executive Summary"
type: "structured narrative"
required: true
fields:
  - name: "overview"
    type: "string (2-3 paragraphs)"
    description: "Summary of the most important findings. What is the single biggest editorial opportunity? What pattern emerged most strongly? What should the editorial team act on immediately?"
  - name: "niche"
    type: "string"
    description: "The target niche being researched"
  - name: "research_period"
    type: "string"
    description: "The date range when research was conducted"
  - name: "communities_consulted"
    type: "integer"
    description: "Total number of communities reviewed"
  - name: "total_findings"
    type: "object"
    description: "Counts of all findings in the report"
    fields:
      - name: "recurring_questions"
        type: "integer"
      - name: "recurring_problems"
        type: "integer"
      - name: "root_causes_analysed"
        type: "integer"
      - name: "content_gaps_identified"
        type: "integer"
      - name: "opportunities_scored"
        type: "integer"
      - name: "articles_recommended"
        type: "integer"
  - name: "top_opportunity"
    type: "object"
    fields:
      - name: "opportunity_id"
        type: "string"
      - name: "title"
        type: "string"
      - name: "finding_id"
        type: "string"
  - name: "urgent_finding"
    type: "object"
    fields:
      - name: "finding_id"
        type: "string"
      - name: "description"
        type: "string"
```

### Example

```json
{
  "section": "1. Executive Summary",
  "overview": "...",
  "niche": "affiliate marketing for beginners with no audience",
  "research_period": "2026-06-01 to 2026-06-14",
  "communities_consulted": 8,
  "total_findings": {
    "recurring_questions": 14,
    "recurring_problems": 9,
    "root_causes_analysed": 9,
    "content_gaps_identified": 7,
    "opportunities_scored": 5,
    "articles_recommended": 7
  },
  "top_opportunity": {
    "opportunity_id": "OPP-001",
    "title": "How to choose a profitable niche as a complete beginner",
    "finding_id": "FND-001"
  },
  "urgent_finding": {
    "finding_id": "FND-003",
    "description": "Beginners are receiving fundamentally contradictory advice about whether to niche down or stay broad, and no existing content resolves this tension."
  }
}
```

---

## 2. Community Workbook

### Schema

```yaml
section: "2. Community Workbook"
type: "array of community entries"
required: true
min_entries: 5
entry:
  fields:
    - name: "community_id"
      type: "string (COM-NNN)"
      required: true
      description: "Stable identifier. Assigned sequentially in workbook order."
    - name: "name"
      type: "string"
      required: true
    - name: "url"
      type: "string (URL)"
      required: true
    - name: "type"
      type: "enum: Reddit | Quora | Forum | Other"
      required: true
    - name: "activity_level"
      type: "enum: High | Medium | Low"
      required: true
      description: "Based on posts per day"
    - name: "relevance"
      type: "enum: Direct | Adjacent | Peripheral"
      required: true
      description: "Direct = audience matches target exactly. Adjacent = related niche with overlap. Peripheral = tangential relevance."
    - name: "member_count"
      type: "string"
      required: false
      description: "Approximate count, e.g. '120k members'"
    - name: "post_frequency"
      type: "string"
      required: false
      description: "Posts per day estimate, e.g. '15-20 posts/day'"
    - name: "cultural_notes"
      type: "string"
      required: true
      description: "Moderation style, community norms, recurring topic patterns"
```

### Example

```json
{
  "section": "2. Community Workbook",
  "entries": [
    {
      "community_id": "COM-001",
      "name": "r/Affiliatemarketing",
      "url": "https://www.reddit.com/r/Affiliatemarketing/",
      "type": "Reddit",
      "activity_level": "High",
      "relevance": "Direct",
      "member_count": "150k",
      "post_frequency": "20-30 posts/day",
      "cultural_notes": "Mix of beginners asking basic questions and experienced marketers sharing strategies. Moderation is light. Heavy on Amazon Associates and niche site discussions."
    }
  ]
}
```

---

## 3. Recurring Questions

### Schema

```yaml
section: "3. Recurring Questions"
type: "array of question entries"
required: true
min_entries: 10
entry:
  traceability:
    - finding_id                    # FND-NNN (primary finding — questions get first block of IDs)
    - originating_community_id      # COM-NNN
    - originating_thread_id         # THR-NNN
    - evidence_snippet              # Verbatim quote from the discussion
    - confidence                    # High | Medium | Low
    - section_first_appeared        # 3
  fields:
    - name: "finding_id"
      type: "string (FND-NNN)"
      required: true
      description: "Stable identifier. Assigned sequentially across questions then problems."
    - name: "exact_question"
      type: "string"
      required: true
      description: "The verbatim question as asked by a community member"
    - name: "normalized_question"
      type: "string"
      required: true
      description: "Cleaned version removing conversational noise"
    - name: "occurrences"
      type: "integer"
      required: true
      description: "Estimated count of unique posts/comments containing this question"
    - name: "originating_community_id"
      type: "string (COM-NNN)"
      required: true
      description: "The primary community where this question was most frequently or clearly observed"
    - name: "originating_thread_id"
      type: "string (THR-NNN)"
      required: true
      description: "The thread where this question was first or most clearly expressed"
    - name: "evidence_snippet"
      type: "string"
      required: true
      description: "A verbatim quote from the thread that contains this question"
    - name: "confidence"
      type: "enum: High | Medium | Low"
      required: true
      description: "High = seen in 3+ communities, 5+ threads. Medium = seen in 2 communities, 3+ threads. Low = seen in 1-2 threads."
    - name: "section_first_appeared"
      type: "integer"
      required: true
      description: "Always 3 for question entries"
    - name: "communities"
      type: "array of strings (community_id)"
      required: true
      description: "List of community_ids where this question appears"
      min_entries: 2
    - name: "time_span"
      type: "string"
      required: true
      description: "Observed time range, e.g. 'last 6 months'"
    - name: "asker_context"
      type: "string"
      required: true
      description: "Typical asker description, e.g. 'complete beginner with no following'"
    - name: "intent_type"
      type: "enum: Information | How-to | Decision | Verification | Troubleshooting"
      required: true
    - name: "existing_answers"
      type: "enum: Yes | Partial | No"
      required: true
    - name: "answer_quality"
      type: "enum: Good | Adequate | Poor | None"
      required: true
    - name: "why_insufficient"
      type: "string"
      required: false
      description: "Why existing answers fail to solve the question"
    - name: "source_thread_ids"
      type: "array of strings (THR-NNN)"
      required: true
      description: "All thread_ids containing this question"
      min_entries: 2
```

### Example

```json
{
  "section": "3. Recurring Questions",
  "entries": [
    {
      "finding_id": "FND-001",
      "exact_question": "How do I find a profitable niche as a complete beginner?",
      "normalized_question": "How to choose a profitable niche as a beginner",
      "occurrences": 12,
      "originating_community_id": "COM-001",
      "originating_thread_id": "THR-001",
      "evidence_snippet": "\"I've been reading about affiliate marketing for weeks but I still have no idea what niche to pick. Everyone says pick something you're passionate about but I don't know if that's actually a good strategy.\"",
      "confidence": "High",
      "section_first_appeared": 3,
      "communities": ["COM-001", "COM-002", "COM-004"],
      "time_span": "last 6 months",
      "asker_context": "Complete beginner with no audience, website, or experience",
      "intent_type": "How-to",
      "existing_answers": "Partial",
      "answer_quality": "Poor",
      "why_insufficient": "Most advice is either too generic ('choose what you're passionate about') or skips straight to keyword research without addressing the decision paralysis beginners feel.",
      "source_thread_ids": ["THR-001", "THR-002", "THR-004"]
    }
  ]
}
```

---

## 4. Recurring Problems

### Schema

```yaml
section: "4. Recurring Problems"
type: "array of problem entries"
required: true
min_entries: 5
entry:
  traceability:
    - finding_id                    # FND-NNN (continues from questions)
    - originating_community_id      # COM-NNN
    - originating_thread_id         # THR-NNN
    - evidence_snippet              # Verbatim quote from the discussion
    - confidence                    # High | Medium | Low
    - section_first_appeared        # 4
  fields:
    - name: "finding_id"
      type: "string (FND-NNN)"
      required: true
      description: "Stable identifier. Continues sequence from Section 3."
    - name: "problem_statement"
      type: "string"
      required: true
      description: "How users describe the problem (verbatim or close paraphrase)"
    - name: "emotional_language"
      type: "array of strings"
      required: true
      description: "Key emotional words used by the community"
    - name: "occurrence_count"
      type: "integer"
      required: true
      description: "Estimated count of unique users expressing this problem"
    - name: "originating_community_id"
      type: "string (COM-NNN)"
      required: true
      description: "The primary community where this problem was most frequently observed"
    - name: "originating_thread_id"
      type: "string (THR-NNN)"
      required: true
      description: "The thread where this problem was first or most clearly expressed"
    - name: "evidence_snippet"
      type: "string"
      required: true
      description: "A verbatim or close-paraphrase snippet expressing this problem"
    - name: "confidence"
      type: "enum: High | Medium | Low"
      required: true
      description: "High = seen in 3+ communities with strong emotional valence. Medium = seen in 2+ communities. Low = seen in 1-2 threads."
    - name: "section_first_appeared"
      type: "integer"
      required: true
      description: "Always 4 for problem entries"
    - name: "communities"
      type: "array of strings (community_id)"
      required: true
      min_entries: 1
    - name: "self_reported_failures"
      type: "array of strings"
      required: false
      description: "Specific failures users describe"
    - name: "conflicting_advice"
      type: "boolean"
      required: true
      description: "Whether users receive contradictory advice about this problem"
    - name: "conflicting_advice_detail"
      type: "string"
      required: false
      description: "Description of the contradictory advice landscape"
    - name: "help_requests"
      type: "array of strings"
      required: false
      description: "Direct calls for help (paraphrased or verbatim)"
    - name: "category"
      type: "enum: Knowledge gap | Skill gap | Resource gap | Trust gap | Execution gap | Decision gap | Emotional barrier"
      required: true
    - name: "source_thread_ids"
      type: "array of strings (THR-NNN)"
      required: true
      min_entries: 2
```

### Example

```json
{
  "section": "4. Recurring Problems",
  "entries": [
    {
      "finding_id": "FND-011",
      "problem_statement": "I've been publishing blog posts for 6 months and made $0. Everyone says affiliate marketing works but it's not working for me.",
      "emotional_language": ["frustrated", "scam", "waste of time", "hopeless", "lied to"],
      "occurrence_count": 18,
      "originating_community_id": "COM-001",
      "originating_thread_id": "THR-005",
      "evidence_snippet": "\"I have 35 blog posts up, I write every week, I've been doing this for 6 months, and I haven't made a single sale. What am I doing wrong or is this just a scam?\"",
      "confidence": "High",
      "section_first_appeared": 4,
      "communities": ["COM-001", "COM-002", "COM-005"],
      "self_reported_failures": [
        "Published 30+ posts, zero traffic",
        "Signed up for Amazon Associates, no sales in 3 months",
        "Followed all the tutorials but nothing happens"
      ],
      "conflicting_advice": true,
      "conflicting_advice_detail": "Some say 'keep publishing, it takes a year'. Others say 'your niche is wrong'. Others say 'you need backlinks'. Beginners receive all of these simultaneously with no framework to evaluate which advice applies to them.",
      "help_requests": ["Can anyone tell me what I'm doing wrong?", "Is affiliate marketing actually viable anymore?"],
      "category": "Execution gap",
      "source_thread_ids": ["THR-005", "THR-006", "THR-008"]
    }
  ]
}
```

---

## 5. Root Cause Analysis

### Schema

```yaml
section: "5. Root Cause Analysis"
type: "array of root cause entries"
required: true
description: "Derived findings. One entry per problem from Section 4."
entry:
  traceability:
    - finding_id                    # FND-NNN (new ID, continues from Section 4)
    - refers_to_finding_id          # FND-NNN of the source problem
    - originating_community_id      # Inherited from source problem
    - originating_thread_id         # Inherited from source problem
    - evidence_snippet              # New evidence supporting the root cause analysis
    - confidence                    # High | Medium | Low
    - section_first_appeared        # 5
  fields:
    - name: "finding_id"
      type: "string (FND-NNN)"
      required: true
      description: "Stable identifier for this derived finding"
    - name: "refers_to_finding_id"
      type: "string (FND-NNN)"
      required: true
      description: "The finding_id of the source problem from Section 4"
    - name: "surface_problem"
      type: "string"
      required: true
      description: "The problem as users express it"
    - name: "root_cause"
      type: "string"
      required: true
      description: "The underlying cause after analysis"
    - name: "originating_community_id"
      type: "string (COM-NNN)"
      required: true
      description: "Inherited from the source problem"
    - name: "originating_thread_id"
      type: "string (THR-NNN)"
      required: true
      description: "Inherited from the source problem"
    - name: "evidence_snippet"
      type: "string"
      required: true
      description: "Discussion evidence supporting this root cause, drawn from source threads"
    - name: "confidence"
      type: "enum: High | Medium | Low"
      required: true
      description: "Confidence in the root cause determination"
    - name: "section_first_appeared"
      type: "integer"
      required: true
      description: "Always 5 for root cause entries"
    - name: "alternative_causes"
      type: "array of strings"
      required: false
      description: "Other possible causes that could not be ruled out"
    - name: "marked_for_human_review"
      type: "boolean"
      required: true
      description: "True if confidence is Low or analysis requires human judgement"
```

### Example

```json
{
  "section": "5. Root Cause Analysis",
  "entries": [
    {
      "finding_id": "FND-021",
      "refers_to_finding_id": "FND-011",
      "surface_problem": "Published content for 6 months with zero results",
      "root_cause": "No keyword research foundation. Beginners are writing about topics they enjoy rather than topics with demonstrated search demand. The content is publish-and-pray.",
      "originating_community_id": "COM-001",
      "originating_thread_id": "THR-005",
      "evidence_snippet": "\"I just write about what I know. I haven't used any keyword tools. I didn't know I was supposed to.\" — multiple users across threads describe the same workflow of writing without demand validation.",
      "confidence": "High",
      "section_first_appeared": 5,
      "alternative_causes": [
        "Wrong niche with no search demand at all",
        "No backlinks or promotion strategy",
        "Poor site technical SEO"
      ],
      "marked_for_human_review": false
    }
  ]
}
```

---

## 6. Existing Content Failures

### Schema

```yaml
section: "6. Existing Content Failures"
type: "array of gap entries"
required: true
description: "Derived findings. One entry per gated-in problem."
entry:
  traceability:
    - finding_id                    # FND-NNN (new ID)
    - refers_to_finding_id          # FND-NNN of the source problem
    - originating_community_id      # Inherited
    - originating_thread_id         # Inherited
    - evidence_snippet              # Evidence that existing content fails
    - confidence                    # High | Medium | Low
    - section_first_appeared        # 6
  fields:
    - name: "finding_id"
      type: "string (FND-NNN)"
      required: true
    - name: "refers_to_finding_id"
      type: "string (FND-NNN)"
      required: true
      description: "The finding_id of the source problem from Section 4"
    - name: "originating_community_id"
      type: "string (COM-NNN)"
      required: true
    - name: "originating_thread_id"
      type: "string (THR-NNN)"
      required: true
    - name: "evidence_snippet"
      type: "string"
      required: true
      description: "Evidence from community discussions that existing content does not solve this problem"
    - name: "confidence"
      type: "enum: High | Medium | Low"
      required: true
    - name: "section_first_appeared"
      type: "integer"
      required: true
    - name: "existing_content_examples"
      type: "array of objects"
      required: true
      items:
        fields:
          - name: "title"
            type: "string"
            required: true
          - name: "url"
            type: "string (URL)"
            required: true
          - name: "source"
            type: "string"
            required: true
            description: "Site or publication name"
    - name: "primary_failure_mode"
      type: "enum: Too generic | Too advanced | Too promotional | Outdated | Assumes resources | No emotional validation | Contradictory landscape | Wrong format"
      required: true
    - name: "failure_detail"
      type: "string"
      required: true
      description: "How the failure manifests for the target audience"
    - name: "gap_description"
      type: "string"
      required: true
      description: "What an ideal answer would cover that existing content misses"
```

### Example

```json
{
  "section": "6. Existing Content Failures",
  "entries": [
    {
      "finding_id": "FND-031",
      "refers_to_finding_id": "FND-011",
      "originating_community_id": "COM-001",
      "originating_thread_id": "THR-005",
      "evidence_snippet": "In a thread with 47 comments, every piece of advice addresses a different problem (traffic, niche, offers, patience) but no single resource addresses all the failure modes at once. Users express frustration that 'everyone says something different.'",
      "confidence": "High",
      "section_first_appeared": 6,
      "existing_content_examples": [
        {
          "title": "How to Make Money with Affiliate Marketing in 2026",
          "url": "https://example.com/affiliate-marketing-2026",
          "source": "Generic affiliate blog"
        },
        {
          "title": "Beginner's Guide to Affiliate Marketing",
          "url": "https://example.com/beginner-guide",
          "source": "Established marketing site"
        }
      ],
      "primary_failure_mode": "Too generic",
      "failure_detail": "Both articles cover the basics of affiliate marketing (join programs, create content, add links) but neither addresses why zero traffic happens after months of effort. They assume the reader will eventually get traffic without explaining the specific failure patterns that cause zero results.",
      "gap_description": "An article that directly addresses 'I published content for 6 months and nothing happened' — troubleshooting the specific failure mode of 'writing without search demand validation' — would fill a gap that generic guides leave open."
    }
  ]
}
```

---

## 7. Solution Feasibility Gate

### Schema

```yaml
section: "7. Solution Feasibility Gate"
type: "array of gate entries"
required: true
description: "For each problem, assess whether publishing an article is a viable solution. Abbreviated traceability."
entry:
  traceability:
    - finding_id                    # FND-NNN (new ID)
    - refers_to_finding_id          # FND-NNN of the source problem
    - evidence_snippet              # Supports the feasibility judgement
    - confidence                    # High | Medium | Low
  fields:
    - name: "finding_id"
      type: "string (FND-NNN)"
      required: true
    - name: "refers_to_finding_id"
      type: "string (FND-NNN)"
      required: true
    - name: "evidence_snippet"
      type: "string"
      required: true
      description: "Evidence supporting the feasibility assessment"
    - name: "confidence"
      type: "enum: High | Medium | Low"
      required: true
    - name: "can_content_solve"
      type: "enum: Yes | Partial | No"
      required: true
    - name: "rationale"
      type: "string"
      required: true
      description: "Why content can or cannot solve this problem"
    - name: "what_content_cannot_do"
      type: "string"
      required: false
      description: "If Partial, what aspect content cannot address"
    - name: "non_content_solution"
      type: "string"
      required: false
      description: "If No, what kind of solution would actually help"
    - name: "gated_out"
      type: "boolean"
      required: true
      description: "True if this problem should not be pursued as a content opportunity"
```

---

## 8. OLSP Alignment Gate

### Schema

```yaml
section: "8. OLSP Alignment Gate"
type: "array of alignment entries"
required: true
description: "For problems that pass the solution feasibility gate, assess OLSP alignment. Abbreviated traceability."
entry:
  traceability:
    - finding_id                    # FND-NNN (new ID)
    - refers_to_finding_id          # FND-NNN of the source problem
    - evidence_snippet              # Evidence supporting the alignment assessment
    - confidence                    # High | Medium | Low
  fields:
    - name: "finding_id"
      type: "string (FND-NNN)"
      required: true
    - name: "refers_to_finding_id"
      type: "string (FND-NNN)"
      required: true
    - name: "evidence_snippet"
      type: "string"
      required: true
    - name: "confidence"
      type: "enum: High | Medium | Low"
      required: true
    - name: "can_olsp_help"
      type: "enum: Natural fit | Adjacent fit | Indirect fit | No"
      required: true
      description: "Natural = OLSP directly addresses this. No = forcing a connection would produce low-quality content."
    - name: "rationale"
      type: "string"
      required: true
    - name: "connection_approach"
      type: "string"
      required: false
      description: "How OLSP naturally relates to solving this problem"
    - name: "alignment_concern"
      type: "string"
      required: false
      description: "Any risk of forced positioning or inauthentic connection"
```

---

## 9. Opportunity Scores

### Schema

```yaml
section: "9. Opportunity Scores"
type: "array of scored opportunity entries"
required: true
min_entries: 5
description: "Heuristic scores based on community signal strength only. Synthetic findings — aggregate multiple signals."
entry:
  fields:
    - name: "opportunity_id"
      type: "string (OPP-NNN)"
      required: true
      description: "Stable identifier. Assigned sequentially in score priority order."
    - name: "finding_ids"
      type: "array of strings (FND-NNN)"
      required: true
      description: "All finding_ids that support this opportunity (questions + problems)"
    - name: "opportunity_name"
      type: "string"
      required: true
      description: "Short name for this opportunity"
    - name: "scores"
      type: "object"
      required: true
      fields:
        - name: "question_frequency"
          type: "integer (1-10)"
          description: "How often does this question appear?"
        - name: "community_spread"
          type: "integer (1-10)"
          description: "How many communities discuss it?"
        - name: "existing_content_quality"
          type: "integer (1-10)"
          description: "How poorly is this currently served? (10 = extremely poorly served)"
        - name: "emotional_intensity"
          type: "integer (1-10)"
          description: "How much frustration or confusion exists?"
        - name: "content_feasibility"
          type: "integer (1-10)"
          description: "Can we write something genuinely better?"
    - name: "total_score"
      type: "integer (1-50)"
      required: true
      description: "Sum of all five dimension scores"
    - name: "scoring_rationale"
      type: "string"
      required: true
      description: "Why each score was assigned, referencing community evidence"
```

### Scoring Notes

- Each dimension is scored 1-10 independently
- Total is the sum (max 50, min 5)
- These are heuristic estimates based on community signal, not data-driven scores
- The scoring rationale must reference specific community evidence
- Do not use search volume data, SERP features, or any SEO tooling to determine scores

---

## 10. Editorial Angles

### Schema

```yaml
section: "10. Editorial Angles"
type: "array of angle entries"
required: true
description: "3-5 distinct angles for each high-scoring opportunity."
entry:
  fields:
    - name: "opportunity_id"
      type: "string (OPP-NNN)"
      required: true
      description: "References the opportunity from Section 9"
    - name: "finding_ids"
      type: "array of strings (FND-NNN)"
      required: true
      description: "Finding_ids that these angles address"
    - name: "angles"
      type: "array of objects"
      required: true
      min_items: 3
      max_items: 5
      items:
        fields:
          - name: "angle_title"
            type: "string"
            required: true
            description: "A short, distinctive angle name"
          - name: "angle_description"
            type: "string (1-2 sentences)"
            required: true
            description: "What unique perspective or framing this angle takes"
          - name: "target_sub_audience"
            type: "string"
            required: true
            description: "Which segment of the audience this angle targets"
          - name: "emotional_hook"
            type: "string"
            required: true
            description: "The emotional entry point this angle uses"
          - name: "key_question"
            type: "string"
            required: true
            description: "The primary question this angle answers"
          - name: "distinctive_approach"
            type: "string"
            required: true
            description: "What makes this angle different from existing content"
```

### Example

```json
{
  "section": "10. Editorial Angles",
  "entries": [
    {
      "opportunity_id": "OPP-001",
      "finding_ids": ["FND-001", "FND-012"],
      "angles": [
        {
          "angle_title": "The Decision Framework Angle",
          "angle_description": "Rather than recommending specific niches, provide a framework for evaluating any niche against criteria beginners can assess without keyword tools.",
          "target_sub_audience": "Analysis-paralysis beginners who can't decide on a niche",
          "emotional_hook": "You don't need to pick the perfect niche. You need a framework to evaluate options.",
          "key_question": "How do I evaluate whether a niche is worth pursuing?",
          "distinctive_approach": "Replaces 'just pick what you love' with a structured evaluation lens that beginners can apply immediately."
        }
      ]
    }
  ]
}
```

---

## 11. Recommended Articles

### Schema

```yaml
section: "11. Recommended Articles"
type: "array of priority-ranked article entries"
required: true
min_entries: 5
entry:
  fields:
    - name: "opportunity_id"
      type: "string (OPP-NNN)"
      required: true
      description: "References the opportunity this article addresses"
    - name: "finding_ids"
      type: "array of strings (FND-NNN)"
      required: true
      description: "Finding_ids that support this recommendation"
    - name: "priority_rank"
      type: "integer (1-based)"
      required: true
    - name: "working_title"
      type: "string"
      required: true
    - name: "primary_question"
      type: "string"
      required: true
      description: "The core question this article answers"
    - name: "root_problem"
      type: "string"
      required: true
      description: "The underlying problem being addressed"
    - name: "recommended_format"
      type: "enum: Explainer | Tutorial | Comparison | Roundup | Honest review | Myth-busting | Troubleshooting guide | Empathy-driven educational | Evidence-based resolution"
      required: true
    - name: "target_audience"
      type: "string"
      required: true
    - name: "estimated_word_count"
      type: "string"
      required: true
      description: "Range, e.g. '2000-3000 words'"
    - name: "rationale"
      type: "string"
      required: true
      description: "Why this article should be prioritised over others"
    - name: "source_thread_ids"
      type: "array of strings (THR-NNN)"
      required: true
      description: "Thread_ids supporting this recommendation"
    - name: "related_angles"
      type: "array of strings"
      required: false
      description: "Angle titles from Section 10 that apply"
```

---

## 12. Cluster Recommendations

### Schema

```yaml
section: "12. Cluster Recommendations"
type: "array of cluster entries"
required: true
description: "Groups of related articles that should be produced as a content cluster."
entry:
  fields:
    - name: "cluster_id"
      type: "string (CLU-NNN)"
      required: true
      description: "Stable identifier. Assigned sequentially in cluster order."
    - name: "opportunity_ids"
      type: "array of strings (OPP-NNN)"
      required: true
      description: "Opportunities addressed by this cluster"
    - name: "finding_ids"
      type: "array of strings (FND-NNN)"
      required: true
      description: "All findings that inform this cluster"
    - name: "cluster_name"
      type: "string"
      required: true
      description: "Short name for this cluster"
    - name: "root_problem"
      type: "string"
      required: true
      description: "The single root problem this cluster addresses from multiple angles"
    - name: "cluster_rationale"
      type: "string"
      required: true
      description: "Why these articles should be produced together"
    - name: "articles"
      type: "array of objects"
      required: true
      min_items: 3
      items:
        fields:
          - name: "title"
            type: "string"
            required: true
          - name: "primary_question"
            type: "string"
            required: true
          - name: "angle"
            type: "string"
            required: true
            description: "The angle this article takes within the cluster"
          - name: "priority_rank"
            type: "integer"
            required: true
            description: "Order within the cluster"
          - name: "finding_id"
            type: "string (FND-NNN)"
            required: true
            description: "Primary finding this article addresses"
    - name: "interlinking_strategy"
      type: "string"
      required: false
      description: "How these articles should link to each other"
```

### Example

```json
{
  "section": "12. Cluster Recommendations",
  "entries": [
    {
      "cluster_id": "CLU-001",
      "opportunity_ids": ["OPP-001"],
      "finding_ids": ["FND-001", "FND-012", "FND-013"],
      "cluster_name": "Beginner Niche Selection Cluster",
      "root_problem": "Beginners cannot choose a profitable niche because they lack both evaluation criteria and confidence in their decision",
      "cluster_rationale": "Niche selection is the single most paralysing decision for beginners. A single article cannot address all the sub-questions, fears, and objections. A 3-5 article cluster can guide a beginner from 'I have no idea what niche to pick' to 'I have a validated niche and a plan to start'.",
      "articles": [
        {
          "title": "How to Choose a Profitable Niche: A Beginner's Framework",
          "primary_question": "What criteria should I use to evaluate niches?",
          "angle": "Decision framework",
          "priority_rank": 1,
          "finding_id": "FND-001"
        },
        {
          "title": "10 Profitable Affiliate Niches for Beginners in 2026",
          "primary_question": "Which niches are actually working for beginners right now?",
          "angle": "Concrete examples with evaluation walkthrough",
          "priority_rank": 2,
          "finding_id": "FND-012"
        },
        {
          "title": "How to Validate Your Niche Idea Before You Build a Single Page",
          "primary_question": "How do I know my niche has real search demand?",
          "angle": "Validation process",
          "priority_rank": 3,
          "finding_id": "FND-013"
        }
      ],
      "interlinking_strategy": "Article 1 links to Article 2 for examples and Article 3 for validation. Article 2 links to Article 1 for the framework and Article 3 for next steps. Article 3 links back to Article 1 and 2."
    }
  ]
}
```

---

## 13. Community Source Log

### Schema

```yaml
section: "13. Community Source Log"
type: "array of source log entries"
required: true
description: "Auditable log of every community discussion that informed the report. This is the primary registry for thread_ids."
entry:
  fields:
    - name: "thread_id"
      type: "string (THR-NNN)"
      required: true
      description: "Stable identifier. Assigned sequentially in source log order."
    - name: "community_id"
      type: "string (COM-NNN)"
      required: true
      description: "References the community from Section 2"
    - name: "community_name"
      type: "string"
      required: true
    - name: "community_url"
      type: "string (URL)"
      required: true
    - name: "thread_title"
      type: "string"
      required: true
    - name: "thread_url"
      type: "string (URL)"
      required: true
    - name: "date_consulted"
      type: "string (ISO date)"
      required: true
    - name: "finding_ids"
      type: "array of strings (FND-NNN)"
      required: true
      description: "All findings that came from this thread"
    - name: "relevance_summary"
      type: "string"
      required: true
      description: "What finding came from this source"
    - name: "sections_contributed_to"
      type: "array of integers"
      required: true
      description: "Which report sections this source informed"
```

### Example

```json
{
  "section": "13. Community Source Log",
  "entries": [
    {
      "thread_id": "THR-001",
      "community_id": "COM-001",
      "community_name": "r/Affiliatemarketing",
      "community_url": "https://www.reddit.com/r/Affiliatemarketing/",
      "thread_title": "6 months in, $0 earned. What am I doing wrong?",
      "thread_url": "https://www.reddit.com/r/Affiliatemarketing/comments/...",
      "date_consulted": "2026-06-10",
      "finding_ids": ["FND-011", "FND-021"],
      "relevance_summary": "Recurring problem: no results after months of content production. Emotional language: frustrated, scam, waste of time.",
      "sections_contributed_to": [3, 4, 5]
    }
  ]
}
```

---

## Full Example Structure (Minimal)

```yaml
report:
  metadata:
    agent: "Community Intelligence Agent V1"
    generated: "2026-06-14"
    niche: "affiliate marketing for beginners with no audience"
    research_period: "2026-06-01 to 2026-06-14"
    communities_consulted: 8
    total_findings:
      recurring_questions: 14
      recurring_problems: 9
      root_causes_analysed: 9
      content_gaps_identified: 7
      opportunities_scored: 5
      articles_recommended: 7

  id_registry:
    community_ids: ["COM-001".."COM-008"]
    thread_ids: ["THR-001".."THR-025"]
    finding_ids: ["FND-001".."FND-045"]
    opportunity_ids: ["OPP-001".."OPP-005"]
    cluster_ids: ["CLU-001".."CLU-003"]

  sections:
    - section_1: { executive_summary }               # Summary + key IDs
    - section_2: { community_workbook }              # min 5 entries, each with community_id
    - section_3: { recurring_questions }             # min 10 entries, FND-001 onward
    - section_4: { recurring_problems }              # min 5 entries, continues FND sequence
    - section_5: { root_cause_analysis }             # one per problem, continues FND
    - section_6: { existing_content_failures }       # entries for gated-in problems
    - section_7: { solution_feasibility_gate }       # one entry per problem
    - section_8: { olsp_alignment_gate }             # one entry per gated-in problem
    - section_9: { opportunity_scores }              # min 5 entries, OPP-001 onward
    - section_10: { editorial_angles }               # 3-5 per scored opportunity
    - section_11: { recommended_articles }           # min 5 entries
    - section_12: { cluster_recommendations }        # clusters of 3+ articles, CLU-001 onward
    - section_13: { community_source_log }           # one entry per unique thread, THR-001 onward
```

---

## Identifier Registry

In addition to the 13 sections, every report should include an `id_registry` in its metadata that lists all IDs used in the report. This registry serves as an index for downstream agents.

```yaml
id_registry:
  community_ids: ["COM-001", "COM-002", ...]
  thread_ids: ["THR-001", "THR-002", ...]
  finding_ids: ["FND-001", "FND-002", ...]
  opportunity_ids: ["OPP-001", "OPP-002", ...]
  cluster_ids: ["CLU-001", "CLU-002", ...]
```

---

## Validation Rules

| Rule | Enforcement |
|---|---|
| Section 1 must summarise findings from all other sections | Required |
| Section 1 must reference top_opportunity by OPP ID and urgent_finding by FND ID | Required |
| Section 2 must have ≥5 communities, ≥3 Direct relevance, ≥2 source types | Required |
| Every Section 2 entry must have a unique community_id | Required |
| Section 3 must have ≥10 questions, each with ≥2 source_thread_ids | Required |
| Section 3 must span ≥3 intent types | Required |
| Every Section 3 entry must have finding_id, originating_community_id, originating_thread_id, evidence_snippet, confidence | Required |
| Section 4 problems must be distinct from Section 3 questions (different framing) | Required |
| Every Section 4 entry must have finding_id, originating_community_id, originating_thread_id, evidence_snippet, confidence | Required |
| Section 3 and 4 finding_ids must form a contiguous sequence (FND-001 through FND-N) | Required |
| Section 5 confidence must be ≥Medium for majority of entries | Required |
| Every Section 5 entry must have refers_to_finding_id pointing to a Section 4 finding | Required |
| Section 6 must reference specific existing content (title + URL) | Required |
| Every Section 7 entry must have can_content_solve and gated_out | Required |
| Section 8 must honestly assess OLSP alignment — if No, state why | Required |
| Section 9 scores must include rationale referencing community evidence | Required |
| Section 9 must not use search volume data or SEO tooling | Required |
| Every Section 9 entry must have a unique opportunity_id | Required |
| Section 10 must have 3-5 angles per opportunity | Required |
| Every Section 10 entry must reference opportunity_id | Required |
| Section 11 must have ≥5 recommended articles with priority rankings | Required |
| Every Section 11 entry must reference opportunity_id and finding_ids | Required |
| Section 12 may be empty if no clustering opportunities exist | Optional |
| Every Section 12 entry must have a unique cluster_id | Required |
| Every entry in Section 13 must have a unique thread_id and reference at least one finding_id | Required |
| Every thread_id referenced in any section must appear in Section 13 | Required |
| Every community_id referenced in any section must appear in Section 2 | Required |
| Every finding_id referenced in any section must appear in Section 3 or 4 | Required |

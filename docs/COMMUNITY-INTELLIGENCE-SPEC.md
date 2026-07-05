# Community Intelligence Specification

## Purpose

Community Intelligence exists to discover real user problems, questions, and discussions before keyword research begins. Content discovery starts with people—not search volume. This module answers what audiences are actually talking about, not what algorithms predict they might search for.

Community Intelligence differs from Trend Intelligence by focusing on qualitative audience understanding rather than quantitative search data. While Trend Intelligence identifies rising search patterns, Community Intelligence reveals the human context behind those patterns—the actual conversations, pain points, and unmet needs that drive search behavior.

## Data Sources

| Source | Status |
|--------|--------|
| Reddit | Current |
| Quora | Current |
| Forums | Current |
| Product communities | Current |
| Facebook Groups | Planned |
| YouTube comments | Future |
| Discord | Future |

## Discovery Categories

### Questions
Identify frequently asked questions across communities that indicate information gaps or recurring interests.

### Pain Points
Capture specific problems, frustrations, and challenges that users repeatedly mention.

### Beginner Problems
Track questions and issues commonly raised by newcomers to a topic or industry.

### Product Comparisons
Collect discussions where users compare products, services, or solutions.

### Buying Questions
Identify questions that indicate purchase intent or pre-purchase research.

### Recommendations
Gather requests for product, service, or resource recommendations.

### Success Stories
Document user-shared positive experiences, results, and achievements.

### Complaints
Track negative experiences, dissatisfaction, and criticism of products or services.

### Objections
Identify common reasons why users hesitate, reject, or avoid certain solutions.

### Myths
Collect misconceptions, misunderstandings, and incorrect information that circulates in communities.

### Emerging Topics
Detect new discussions, trends, or themes that are gaining traction in communities.

## Community Report

The primary output of Community Intelligence is the Community Report, structured as follows:

### Top Communities
List of the most active and relevant communities for the target niche, ranked by engagement and relevance.

### Recurring Questions
Top 10-20 questions that appear repeatedly across communities, grouped by theme.

### Pain Points
Key problems and challenges that users consistently mention, with frequency indicators.

### Common Misconceptions
List of myths, misunderstandings, and incorrect beliefs that appear frequently in discussions.

### Frequently Compared Products
Products, services, or solutions that users often compare or ask about in relation to each other.

### Buying Intent Questions
Questions that indicate users are in a purchase decision phase, such as "Which is better?", "Should I buy?", or "What's the best option for...?".

### Emerging Discussions
New or growing topics that are gaining attention in communities, with momentum indicators.

### Potential Content Angles
Article ideas derived from community discussions, categorized by type and aligned with audience needs.

## Angle Generation

A single community discussion can generate multiple article ideas by addressing different aspects of the conversation.

**Example:**

**Question:** "Can I make money with affiliate marketing without showing my face?"

**Possible angles:**
- **Beginner Guide:** "Affiliate Marketing for Introverts: How to Succeed Without Showing Your Face"
- **Myth Busting:** "Debunking the Myth: You Don't Need to Be on Camera for Affiliate Marketing"
- **Comparison:** "Faceless vs. Face-Forward Affiliate Marketing: Which is More Profitable?"
- **Tutorial:** "Step-by-Step Guide to Building a Faceless Affiliate Marketing Business"
- **Case Study:** "How I Made $10,000/Month with Affiliate Marketing Without a Camera"
- **Product Recommendation:** "Best Tools for Faceless Affiliate Marketers in 2026"

## Connection to the Editorial Pipeline

Community Intelligence feeds into the AI Editorial Operating System as the first audience-driven discovery stage:

```
Community Intelligence
↓
Opportunity Discovery
↓
Search Validation
↓
Opportunity Brief
↓
Research Brief
↓
Writer
↓
QA
↓
Publish
```

### Integration Details

1. **Community Intelligence to Opportunity Discovery:**
   - Community Reports provide raw audience insights that Opportunity Discovery uses to identify potential content topics.
   - Discovery Categories map to Opportunity Discovery's topic clustering and prioritization.

2. **Opportunity Discovery to Search Validation:**
   - Validated community insights are cross-referenced with search data to confirm demand and competition levels.

3. **Search Validation to Opportunity Brief:**
   - Confirmed opportunities are structured into Opportunity Briefs that include both audience insights and search data.

4. **Opportunity Brief to Research Brief:**
   - Research Briefs incorporate community-driven angles and questions to guide content research.

5. **Research Brief to Writer:**
   - Writers receive briefs that include real audience questions, pain points, and discussion context to inform content creation.

## Scope

This specification defines the production requirements for Community Intelligence. The following are explicitly out of scope:

- APIs
- Crawlers
- Reddit integration
- DataForSEO
- Databases
- Implementation details

## Acceptance Criteria

The specification must clearly explain:

- [x] Why Community Intelligence exists
- [x] What information it collects
- [x] How it differs from Trend Intelligence
- [x] How it integrates with the AI Editorial Operating System
- [x] What reports it produces
- [x] How it generates article opportunities from real discussions

## Output

The Community Intelligence module produces:

1. **Community Reports:** Structured documents summarizing audience insights from community discussions.
2. **Content Angles:** Multiple article ideas derived from each significant community discussion.
3. **Audience Understanding:** Qualitative insights that inform all subsequent stages of the editorial pipeline.

The output is audience understanding, not keywords. The focus is on what people are discussing, what questions they ask, what problems they face, and what solutions they seek—not on search volume or ranking potential.
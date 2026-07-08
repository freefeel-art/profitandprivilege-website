#!/usr/bin/env python3
"""
Community Intelligence Processor.

Transforms raw Discovery Packages (from the Discovery Runner) into
structured Community Intelligence.

This processor extracts 12 categories of findings from community posts:
    1.  Recurring Questions
    2.  Pain Points
    3.  Frustrations
    4.  Misconceptions
    5.  Frequently Mentioned Tools
    6.  Frequently Mentioned Competitors
    7.  Desired Outcomes
    8.  Common Beginner Mistakes
    9.  Positive Signals
    10. Negative Signals
    11. Representative Quotes
    12. Supporting Evidence

Every finding includes:
    - finding       (the identified signal text)
    - frequency     (how many posts exhibited this signal)
    - confidence    (high >= 5, medium 2-4, low 1)
    - source_posts  (list of post refs with id, title, subreddit, url, timestamp, snippet)

This processor does NOT:
    - Make editorial recommendations
    - Generate Opportunity Briefs
    - Produce article content
    - Perform web searches
    - Use AI summarization

    Input:  research/output/discovery/{pillar}-discovery.json
    Output: research/output/community-intelligence/{pillar}-community-intelligence.json
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any, Counter as CounterType, Dict, List, Optional, Set, Tuple


# ──────────────────────────────────────────────────────────────
#  CONSTANTS
# ──────────────────────────────────────────────────────────────

CONFIDENCE_HIGH = "high"    # >= 5 occurrences
CONFIDENCE_MEDIUM = "medium"  # 2-4 occurrences
CONFIDENCE_LOW = "low"      # 1 occurrence

TOOL_KEYWORDS = [
    "Impact", "Admitad", "Takeads", "ClickBank", "Amazon Associates",
    "ShareASale", "CJ Affiliate", "Rakuten", "WordPress", "Elementor",
    "Canva", "ConvertKit", "Mailchimp", "AWeber", "GetResponse",
    "ActiveCampaign", "Klaviyo", "ThriveCart", "Builderall",
    "ClickFunnels", "Leadpages", "System.io", "Scalable", "Tailwind",
    "Buffer", "Hootsuite", "SEMrush", "Ahrefs", "Moz",
    "Google Analytics", "Google Search Console", "Yoast", "RankMath",
    "SurferSEO", "ChatGPT", "Claude", "Jasper", "Copy.ai", "Writer",
    "Synthesia", "HeyGen", "ElevenLabs", "Midjourney", "Canva",
    "Shopify", "WooCommerce", "Teachable", "Udemy", "Kajabi",
    "MemberPress", "OptinMonster", "Thrive Leads", "Pretty Links",
    "MonsterInsights", "RabbitLoader", "Litespeed Cache",
    "Fiverr", "Upwork", "Freelancer",
]

COMPETITOR_KEYWORDS = [
    "Wealthy Affiliate", "Commission Hero", "Super Affiliate System",
    "Empire Flippers", "Project 24", "Legendary Marketer",
    "Affiliate Lab", "Making Sense of Affiliate Marketing",
    "Authority Hacker", "Niche Pursuits", "Smart Passive Income",
    "Affiliate Marketing Mastery", "Affiliate Bootcamp",
    "MegaLink", "LeadsMiner", "OLSP Academy", "Solo ads",
    "Udimi", "TrafficForMe",
]

QUESTION_STARTERS = [
    "how", "what", "why", "is", "can", "should", "does", "are",
    "do", "which", "where", "when", "has", "have", "will", "would",
    "could", "did", "was", "were", "am", "anyone", "anybody",
    "does anyone", "has anyone", "is it", "are there",
]

PAIN_POINT_KEYWORDS = [
    "struggling", "struggle", "hard to", "difficult", "challenge",
    "problem", "issue", "trouble", "waste", "can't", "cannot",
    "no money", "no budget", "no experience", "no traffic",
    "no sales", "no results", "no audience", "no list",
    "no followers", "no idea", "no clue", "don't know where",
    "don't know how", "not sure", "confused", "lost",
    "overwhelmed", "overwhelming",
]

FRUSTRATION_KEYWORDS = [
    "frustrating", "frustrated", "annoying", "annoyed",
    "disappointed", "disappointing", "sick of", "tired of",
    "giving up", "give up", "quit", "quitting", "scam",
    "waste of time", "waste of money", "hopeless", "nothing works",
    "doesn't work", "not working", "failed", "failure",
    "no matter what", "tried everything", "never works",
    "impossible", "useless", "pointless",
]

MISCONCEPTION_KEYWORDS = [
    "myth", "misconception", "actually worth", "too late",
    "saturated", "overrated", "underrated", "not working",
    "scam or legit", "legitimate", "is it legit", "is it worth",
    "is it too late", "worth it in 202", "still relevant",
    "dead or alive", "is this real", "too good to be true",
    "honest review", "truth about", "the reality",
    "everyone says", "people say",
]

OUTCOME_KEYWORDS = [
    "goal", "target", "aim", "want to make", "hope to earn",
    "dream income", "full time", "full-time", "passive income",
    "quit my job", "quit job", "replace my income",
    "replace income", "financial freedom", "work from anywhere",
    "location independent", "scale", "grow", "consistent income",
    "stable income", "extra income", "side income", "main income",
    "live on", "survive on", "pay bills",
]

MISTAKE_KEYWORDS = [
    "mistake", "error", "wrong", "bad advice", "should not",
    "avoid", "don't do", "don't make", "overcomplicating",
    "shiny object", "jumping between", "following everyone",
    "not consistent", "give up too early", "quit too early",
    "common mistake", "beginner mistake", "what not to do",
    "biggest mistake", "biggest regret", "things i wish",
    "if i could start over", "working hard not smart",
    "using the wrong", "not focusing",
]

POSITIVE_SIGNAL_KEYWORDS = [
    "made $", "earned", "success", "profit", "working well",
    "game changer", "best decision", "took off", "grew",
    "growth", "happy with", "highly recommend", "great results",
    "impressed", "amazing results", "consistent results",
    "lifestyle", "life changing", "finally working",
    "breakthrough", "booming", "record month", "best month",
    "strategy that works", "method that works",
]

NEGATIVE_SIGNAL_KEYWORDS = [
    "scam", "waste", "avoid", "not worth", "don't join",
    "didn't work", "failed", "disappointing", "regret",
    "stay away", "red flag", "overpriced", "dishonest",
    "shady", "fraud", "ripoff", "rip off", "fake",
    "cookie cutter", "template", "recycled content",
    "do not buy", "do not use", "not recommended",
    "below average", "poor quality",
]

EVIDENCE_PATTERNS = [
    r'\$\s*\d+(?:,\d{3})*(?:\.\d+)?',           # $50, $1,000, $123.45
    r'\d+\s*%',                                    # 50%
    r'\d+\s*(?:months?|years?|weeks?|days?|hours?)',  # 3 months, 2 years
    r'\d+(?:,\d{3})*\s*(?:visitors?|clicks?|sales?|leads?|conversions?|subscribers?|members?|users?|customers?|orders?)',
    r'(?:conversion|open|click|response|success|close)\s*rate[:\s]*\d+',
]

QUESTION_Q_REGEX = re.compile(r'\?')
DOLLAR_AMOUNT_REGEX = re.compile(r'\$\s*\d+(?:,\d{3})*(?:\.\d+)?')
PERCENTAGE_REGEX = re.compile(r'\d+\s*%')
TIME_PERIOD_REGEX = re.compile(r'\d+\s*(?:months?|years?|weeks?|days?|hours?)', re.IGNORECASE)


# ──────────────────────────────────────────────────────────────
#  HELPERS
# ──────────────────────────────────────────────────────────────

def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def safe_str(val: Any) -> str:
    """Return string value, handling None."""
    if val is None:
        return ""
    return str(val)


def post_text(post: dict) -> str:
    """Return combined title + selftext for analysis."""
    title = safe_str(post.get("title"))
    selftext = safe_str(post.get("selftext"))
    return f"{title} {selftext}"


def post_text_lower(post: dict) -> str:
    """Return lowercased combined text for keyword matching."""
    return post_text(post).lower()


def get_snippet(post: dict, max_len: int = 200) -> str:
    """Return a relevant text snippet from the post."""
    selftext = safe_str(post.get("selftext"))
    if len(selftext) > 10:
        return selftext[:max_len].strip()
    title = safe_str(post.get("title"))
    return title[:max_len].strip()


def confidence_for(freq: int) -> str:
    if freq >= 5:
        return CONFIDENCE_HIGH
    elif freq >= 2:
        return CONFIDENCE_MEDIUM
    return CONFIDENCE_LOW


def build_source_ref(post: dict, snippet: str = "") -> dict:
    return {
        "post_id": post.get("id", ""),
        "title": post.get("title", ""),
        "subreddit": post.get("subreddit", ""),
        "url": post.get("url", ""),
        "timestamp": post.get("created_utc", 0),
        "snippet": snippet or get_snippet(post),
    }


def normalize_phrase(phrase: str) -> str:
    """Normalize a phrase for grouping: lowercase, strip punctuation, collapse whitespace."""
    text = phrase.lower().strip()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# ──────────────────────────────────────────────────────────────
#  FINDING ACCUMULATOR
# ──────────────────────────────────────────────────────────────

class FindingAccumulator:
    """Accumulates findings of a given type, merging by normalized key."""

    def __init__(self):
        self._data: Dict[str, dict] = {}

    def add(self, key: str, finding_label: str, post: dict, snippet: str = ""):
        """Add a post to a finding group.

        Args:
            key: Normalized key used for grouping.
            finding_label: Human-readable label for the finding.
            post: The source post dict.
            snippet: Optional excerpt from the post.
        """
        if key not in self._data:
            self._data[key] = {
                "finding": finding_label,
                "frequency": 0,
                "confidence": CONFIDENCE_LOW,
                "source_posts": [],
            }
        entry = self._data[key]
        entry["frequency"] += 1
        # Avoid duplicate post refs (same post matched by multiple keywords)
        existing_ids = {r["post_id"] for r in entry["source_posts"]}
        if post.get("id", "") not in existing_ids:
            entry["source_posts"].append(build_source_ref(post, snippet))
        entry["confidence"] = confidence_for(entry["frequency"])

    def update_label(self, key: str, label: str):
        """Update the human-readable label for a finding group."""
        if key in self._data:
            self._data[key]["finding"] = label

    def results(self, min_frequency: int = 1) -> List[dict]:
        """Return sorted list of findings (most frequent first)."""
        return sorted(
            [v for v in self._data.values() if v["frequency"] >= min_frequency],
            key=lambda x: x["frequency"],
            reverse=True,
        )

    def all(self) -> Dict[str, List[dict]]:
        """Raw access to all entries by normalized key."""
        return self._data


# ──────────────────────────────────────────────────────────────
#  CLASSIFIERS
# ──────────────────────────────────────────────────────────────

def extract_recurring_questions(posts: List[dict]) -> List[dict]:
    """Find recurring questions in post titles and selftext."""
    acc = FindingAccumulator()
    for post in posts:
        title = safe_str(post.get("title")).strip()
        selftext = safe_str(post.get("selftext")).strip()
        combined = f"{title} {selftext[:300]}"  # limit context

        # Check for question mark in title
        if "?" in title:
            # Extract the question sentence
            key = normalize_phrase(title)
            acc.add(key, title, post, title)

        # Check for question starters in title or early selftext
        lower_combined = combined.lower()
        for starter in QUESTION_STARTERS:
            pattern = r'\b' + re.escape(starter) + r'\b'
            if re.search(pattern, lower_combined):
                # Build a question statement from context
                question_text = title if len(title) > 10 else combined[:120]
                key = normalize_phrase(starter + " " + question_text)
                acc.add(key, question_text, post, question_text)

    return acc.results(min_frequency=1)


def extract_pain_points(posts: List[dict]) -> List[dict]:
    """Identify recurring pain points from keyword patterns."""
    acc = FindingAccumulator()
    for post in posts:
        text_lower = post_text_lower(post)
        for kw in PAIN_POINT_KEYWORDS:
            if kw in text_lower:
                snippet = get_snippet(post, 150)
                acc.add(kw, f"Users report: {kw}", post, snippet)
    return acc.results(min_frequency=1)


def extract_frustrations(posts: List[dict]) -> List[dict]:
    """Identify strong frustration signals."""
    acc = FindingAccumulator()
    for post in posts:
        text_lower = post_text_lower(post)
        for kw in FRUSTRATION_KEYWORDS:
            if kw in text_lower:
                snippet = get_snippet(post, 150)
                acc.add(kw, f"Frustration: {kw}", post, snippet)
    return acc.results(min_frequency=1)


def extract_misconceptions(posts: List[dict]) -> List[dict]:
    """Identify posts that challenge or reveal misconceptions."""
    acc = FindingAccumulator()
    for post in posts:
        text_lower = post_text_lower(post)
        for kw in MISCONCEPTION_KEYWORDS:
            if kw in text_lower:
                snippet = get_snippet(post, 180)
                acc.add(kw, f"Misconception/skepticism: {kw}", post, snippet)
    return acc.results(min_frequency=1)


def extract_tools(posts: List[dict]) -> List[dict]:
    """Find frequently mentioned tools and platforms."""
    acc = FindingAccumulator()
    for post in posts:
        text = post_text(post)
        text_lower = text.lower()
        for tool in TOOL_KEYWORDS:
            tool_lower = tool.lower()
            if tool_lower in text_lower:
                snippet = get_snippet(post, 120)
                acc.add(tool_lower, f"Tool mentioned: {tool}", post, snippet)
    return acc.results(min_frequency=1)


def extract_competitors(posts: List[dict]) -> List[dict]:
    """Find frequently mentioned competitors or alternatives."""
    acc = FindingAccumulator()
    for post in posts:
        text_lower = post_text_lower(post)
        for comp in COMPETITOR_KEYWORDS:
            comp_lower = comp.lower()
            if comp_lower in text_lower:
                snippet = get_snippet(post, 120)
                acc.add(comp_lower, f"Competitor mentioned: {comp}", post, snippet)
    return acc.results(min_frequency=1)


def extract_desired_outcomes(posts: List[dict]) -> List[dict]:
    """Identify desired outcomes and goals users express."""
    acc = FindingAccumulator()
    for post in posts:
        text_lower = post_text_lower(post)
        for kw in OUTCOME_KEYWORDS:
            if kw in text_lower:
                snippet = get_snippet(post, 150)
                acc.add(kw, f"Desired outcome: {kw}", post, snippet)
    return acc.results(min_frequency=1)


def extract_beginner_mistakes(posts: List[dict]) -> List[dict]:
    """Identify common beginner mistakes discussed."""
    acc = FindingAccumulator()
    for post in posts:
        text_lower = post_text_lower(post)
        for kw in MISTAKE_KEYWORDS:
            if kw in text_lower:
                snippet = get_snippet(post, 180)
                acc.add(kw, f"Beginner mistake: {kw}", post, snippet)
    return acc.results(min_frequency=1)


def extract_positive_signals(posts: List[dict]) -> List[dict]:
    """Identify positive experiences, success stories, recommendations."""
    acc = FindingAccumulator()
    for post in posts:
        text_lower = post_text_lower(post)
        for kw in POSITIVE_SIGNAL_KEYWORDS:
            if kw in text_lower:
                snippet = get_snippet(post, 180)
                acc.add(kw, f"Positive: {kw}", post, snippet)
    return acc.results(min_frequency=1)


def extract_negative_signals(posts: List[dict]) -> List[dict]:
    """Identify warnings, complaints, and negative experiences."""
    acc = FindingAccumulator()
    for post in posts:
        text_lower = post_text_lower(post)
        for kw in NEGATIVE_SIGNAL_KEYWORDS:
            if kw in text_lower:
                snippet = get_snippet(post, 180)
                acc.add(kw, f"Negative/warning: {kw}", post, snippet)
    return acc.results(min_frequency=1)


def extract_representative_quotes(posts: List[dict]) -> List[dict]:
    """Select representative quotes from the most substantive posts."""
    scored = []
    for post in posts:
        selftext = safe_str(post.get("selftext")).strip()
        title = safe_str(post.get("title")).strip()
        if len(selftext) < 100:
            continue
        # Score by length and engagement
        score = len(selftext) + (post.get("score", 0) * 10) + (post.get("num_comments", 0) * 5)
        scored.append({
            "finding": selftext[:300].strip(),
            "frequency": 1,
            "confidence": CONFIDENCE_LOW,
            "source_posts": [build_source_ref(post, selftext[:300])],
            "_score": score,
        })

    scored.sort(key=lambda x: x["_score"], reverse=True)
    top = scored[:30]

    # Assign confidence: top quartile = high
    if top:
        quartile = max(len(top) // 4, 1)
        for i, entry in enumerate(top):
            if i < quartile:
                entry["confidence"] = CONFIDENCE_HIGH
            elif i < quartile * 2:
                entry["confidence"] = CONFIDENCE_MEDIUM

    for entry in top:
        del entry["_score"]

    return top


def extract_supporting_evidence(posts: List[dict]) -> List[dict]:
    """Extract posts containing concrete data points and evidence."""
    acc = FindingAccumulator()
    for post in posts:
        text = post_text(post)
        lower = text.lower()
        snippets = []

        # Dollar amounts
        dollars = DOLLAR_AMOUNT_REGEX.findall(text)
        for d in dollars:
            snip = get_snippet(post, 120)
            key = "dollar_" + d.replace(" ", "").replace("$", "").replace(",", "")
            acc.add(key, f"Evidence: {d} mentioned", post, snip)

        # Percentages
        pcts = PERCENTAGE_REGEX.findall(text)
        for p in pcts:
            snip = get_snippet(post, 120)
            key = "pct_" + p.replace("%", "").strip()
            acc.add(key, f"Evidence: {p} mentioned", post, snip)

        # Time periods
        periods = TIME_PERIOD_REGEX.findall(text)
        for p in periods:
            snip = get_snippet(post, 120)
            key = "time_" + normalize_phrase(p)
            acc.add(key, f"Evidence: {p} mentioned", post, snip)

    return acc.results(min_frequency=1)


# ──────────────────────────────────────────────────────────────
#  MAIN PROCESSOR
# ──────────────────────────────────────────────────────────────

EXTRACTORS = {
    "recurring_questions": extract_recurring_questions,
    "pain_points": extract_pain_points,
    "frustrations": extract_frustrations,
    "misconceptions": extract_misconceptions,
    "frequently_mentioned_tools": extract_tools,
    "frequently_mentioned_competitors": extract_competitors,
    "desired_outcomes": extract_desired_outcomes,
    "common_beginner_mistakes": extract_beginner_mistakes,
    "positive_signals": extract_positive_signals,
    "negative_signals": extract_negative_signals,
    "representative_quotes": extract_representative_quotes,
    "supporting_evidence": extract_supporting_evidence,
}


def process_discovery_package(input_path: str, output_dir: str) -> str:
    """Run the full CI processor pipeline.

    Args:
        input_path: Path to the Discovery Package JSON file.
        output_dir: Directory to save the CI output.

    Returns:
        Path to the saved CI output file.
    """
    if not os.path.exists(input_path):
        print(f"ERROR: Discovery Package not found: {input_path}")
        sys.exit(1)

    with open(input_path) as f:
        discovery = json.load(f)

    posts = discovery.get("posts", [])
    meta = discovery.get("discovery_metadata", {})

    pillar_name = meta.get("pillar_name", "unknown")
    pillar_slug = meta.get("pillar_slug", "unknown")
    total_posts = len(posts)

    print(f"Community Intelligence Processor")
    print(f"  Input:  {input_path}")
    print(f"  Pillar: {pillar_name} ({pillar_slug})")
    print(f"  Posts:  {total_posts}")
    print()

    # Run all extractors
    findings: Dict[str, List[dict]] = {}
    extractor_names = list(EXTRACTORS.keys())

    for i, (name, extractor) in enumerate(EXTRACTORS.items(), 1):
        label = name.replace("_", " ").title()
        print(f"  [{i}/{len(EXTRACTORS)}] Extracting {label}...", end=" ")
        sys.stdout.flush()
        results = extractor(posts)
        findings[name] = results
        total_findings = sum(len(v) for v in findings.values())
        print(f"{len(results)} findings (cumulative: {total_findings})")

    # Count unique source posts across all findings
    all_source_ids: Set[str] = set()
    total_finding_entries = 0
    for category, items in findings.items():
        for item in items:
            total_finding_entries += 1
            for ref in item.get("source_posts", []):
                all_source_ids.add(ref.get("post_id", ""))

    # Build the CI output
    output = {
        "ci_metadata": {
            "pillar_name": pillar_name,
            "pillar_slug": pillar_slug,
            "source": os.path.basename(input_path),
            "source_path": input_path,
            "total_posts_analyzed": total_posts,
            "generated_at": now_iso(),
            "processor_version": "1.0.0",
        },
        "findings": findings,
        "summary": {
            "categories": len(EXTRACTORS),
            "total_finding_entries": total_finding_entries,
            "unique_source_posts": len(all_source_ids),
            "coverage_percent": round(len(all_source_ids) / max(total_posts, 1) * 100, 1),
        },
    }

    # Save
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{pillar_slug}-community-intelligence.json"
    out_path = os.path.join(output_dir, filename)
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\n  Output: {out_path}")
    print(f"  Size:   {os.path.getsize(out_path) / 1024:.1f} KB")
    print(f"  Done.")

    return out_path


def print_overview(output: dict):
    """Print a concise overview of the CI data."""
    meta = output["ci_metadata"]
    summary = output["summary"]

    print(f"\n{'=' * 60}")
    print(f"COMMUNITY INTELLIGENCE")
    print(f"{'=' * 60}")
    print(f"  Pillar:       {meta['pillar_name']} ({meta['pillar_slug']})")
    print(f"  Source:       {meta['source']}")
    print(f"  Posts:        {meta['total_posts_analyzed']}")
    print(f"  Generated:    {meta['generated_at']}")
    print()
    print(f"  Categories:   {summary['categories']}")
    print(f"  Total finds:  {summary['total_finding_entries']}")
    print(f"  Unique posts: {summary['unique_source_posts']} ({summary['coverage_percent']}%)")
    print()

    # Per-category breakdown
    categories = list(output["findings"].keys())
    for i, cat in enumerate(categories, 1):
        items = output["findings"][cat]
        label = cat.replace("_", " ").title()
        # Count how many source posts in this category
        post_ids: Set[str] = set()
        for item in items:
            for ref in item.get("source_posts", []):
                post_ids.add(ref.get("post_id", ""))
        high = sum(1 for f in items if f["confidence"] == "high")
        med = sum(1 for f in items if f["confidence"] == "medium")
        low = sum(1 for f in items if f["confidence"] == "low")
        print(f"  {i:2d}. {label:<33s} {len(items):4d} findings (H:{high} M:{med} L:{low})")

    print(f"{'=' * 60}")


def main():
    args = sys.argv[1:]

    if not args:
        # Default: pick the first discovery package found
        discovery_dir = os.path.join(os.getcwd(), "research/output/discovery")
        if not os.path.exists(discovery_dir):
            print("ERROR: No discovery packages found. Run the Discovery Runner first.")
            sys.exit(1)
        files = [f for f in os.listdir(discovery_dir) if f.endswith("-discovery.json")]
        if not files:
            print("ERROR: No discovery packages found in", discovery_dir)
            sys.exit(1)
        input_path = os.path.join(discovery_dir, files[0])
        print(f"Auto-selected: {input_path}")
    else:
        input_path = args[0]

    output_dir = os.path.join(os.getcwd(), "research/output/community-intelligence")

    out_path = process_discovery_package(input_path, output_dir)

    with open(out_path) as f:
        output = json.load(f)
    print_overview(output)


if __name__ == "__main__":
    main()

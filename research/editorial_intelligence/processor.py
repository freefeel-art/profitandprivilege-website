#!/usr/bin/env python3
"""
Editorial Intelligence Processor.

Transforms Community Intelligence Reports into structured Editorial Intelligence.

Responsibilities:
    - Cluster related findings into topical groups
    - Prioritise clusters by community frequency and emotional intensity
    - Identify recurring narratives
    - Identify thematic gaps
    - Generate article concepts from each cluster
    - Recommend content format for each concept
    - Estimate effort level

Input:  research/output/community-intelligence-reports/{pillar}-community-intelligence-report.json
Output: research/output/editorial-intelligence/{pillar}-editorial-intelligence-report.json
"""

from __future__ import annotations

import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Set, Tuple


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def safe_str(val: Any) -> str:
    if val is None:
        return ""
    return str(val)


def load_ci_report(path: str) -> dict:
    if not os.path.exists(path):
        print(f"ERROR: CI Report not found: {path}")
        sys.exit(1)
    with open(path) as f:
        return json.load(f)


# ──────────────────────────────────────────────────────────────
#  CLUSTER ANALYSIS
# ──────────────────────────────────────────────────────────────

def cluster_findings(report: dict) -> List[dict]:
    """Cluster related findings across CI categories into topical groups.

    Uses heuristic grouping:
    - Findings mentioning the same keywords/phrases belong together
    - Community overlap between findings
    - CI category as initial grouping signal
    """
    sections = report.get("sections", {})
    exec_summary = report.get("executive_summary", {})

    clusters = []
    cluster_id = 0

    # Define cluster boundaries from CI sections
    cluster_definitions = [
        {
            "name": "Getting Started & Beginner Struggles",
            "source_categories": ["recurring_questions", "pain_points", "common_beginner_mistakes"],
            "keywords": ["beginner", "start", "no experience", "no money", "no audience",
                         "overwhelmed", "confused", "where to", "first", "new to"],
        },
        {
            "name": "Traffic & Audience Building",
            "source_categories": ["pain_points", "frustrations", "recurring_questions"],
            "keywords": ["traffic", "audience", "followers", "visitors", "clicks", "views",
                         "promote", "reach", "exposure", "discover"],
        },
        {
            "name": "Email & List Building",
            "source_categories": ["pain_points", "frustrations", "recurring_questions"],
            "keywords": ["email", "list", "subscriber", "open rate", "sequence",
                         "newsletter", "autoresponder", "drip"],
        },
        {
            "name": "Tool Selection & Evaluation",
            "source_categories": ["frequently_mentioned_tools", "recurring_questions", "pain_points"],
            "keywords": ["tool", "software", "platform", "best", "compare", "vs", "review",
                         "which", "recommend", "worth"],
        },
        {
            "name": "Trust & Credibility Concerns",
            "source_categories": ["misconceptions", "negative_signals", "frustrations"],
            "keywords": ["scam", "legit", "trust", "honest", "fake", "shady", "fraud",
                         "too good", "skeptical", "doubt", "worth it", "overrated"],
        },
        {
            "name": "Income & Monetization",
            "source_categories": ["desired_outcomes", "positive_signals", "supporting_evidence"],
            "keywords": ["income", "money", "earn", "make", "profit", "revenue", "passive",
                         "full time", "side hustle", "financial", "dollars", "month"],
        },
        {
            "name": "Content Creation & Strategy",
            "source_categories": ["recurring_questions", "pain_points", "positive_signals"],
            "keywords": ["content", "write", "blog", "post", "article", "video", "social media",
                         "strategy", "niche", "topic", "keyword"],
        },
        {
            "name": "Competitor & Program Comparisons",
            "source_categories": ["frequently_mentioned_competitors", "frequently_mentioned_tools",
                                  "recurring_questions"],
            "keywords": ["vs", "alternative", "better", "compare", "competitor", "choice",
                         "switch", "migrate", "instead"],
        },
    ]

    for cd in cluster_definitions:
        matched_findings = []
        matched_categories = set()
        total_frequency = 0
        total_confidence_score = 0.0
        source_posts: Set[str] = set()

        for cat_key in cd["source_categories"]:
            cat_data = sections.get(cat_key, {})
            findings = cat_data.get("findings", [])
            for finding in findings:
                text = safe_str(finding.get("finding", "")).lower()
                freq = finding.get("frequency", 0)
                conf = finding.get("confidence", "low")
                conf_score = {"high": 3.0, "medium": 1.5, "low": 0.5}.get(conf, 0.5)

                for kw in cd["keywords"]:
                    if kw in text:
                        matched_findings.append(finding)
                        matched_categories.add(cat_key)
                        total_frequency += freq
                        total_confidence_score += conf_score * freq
                        for ref in finding.get("source_posts", []):
                            pid = safe_str(ref.get("post_id"))
                            if pid:
                                source_posts.add(pid)
                        break

        if matched_findings and len(source_posts) >= 2:
            cluster_id += 1
            avg_confidence = round(total_confidence_score / max(total_frequency, 1), 1)
            intensity = "high" if avg_confidence >= 2.0 else "medium" if avg_confidence >= 1.0 else "low"
            clusters.append({
                "cluster_id": f"CLU-{cluster_id:03d}",
                "name": cd["name"],
                "source_categories": sorted(matched_categories),
                "matched_findings_count": len(matched_findings),
                "total_signal_frequency": total_frequency,
                "unique_posts_contributing": len(source_posts),
                "confidence_score": avg_confidence,
                "intensity": intensity,
                "keywords": cd["keywords"],
                "sample_findings": [
                    {"finding": f.get("finding", ""), "frequency": f.get("frequency", 0),
                     "confidence": f.get("confidence", "low")}
                    for f in matched_findings[:5]
                ],
            })

    # Sort by signal frequency descending
    clusters.sort(key=lambda c: c["total_signal_frequency"], reverse=True)

    # Assign priority ranks
    for i, c in enumerate(clusters, 1):
        c["priority_rank"] = i

    return clusters


# ──────────────────────────────────────────────────────────────
#  ARTICLE CONCEPT GENERATION
# ──────────────────────────────────────────────────────────────

def generate_article_concepts(clusters: List[dict], exec_summary: dict) -> List[dict]:
    """Generate article concepts from each cluster."""
    format_map = {
        "Getting Started & Beginner Struggles": "Guide",
        "Traffic & Audience Building": "Guide",
        "Email & List Building": "Guide",
        "Tool Selection & Evaluation": "Comparison",
        "Trust & Credibility Concerns": "Myth-busting",
        "Income & Monetization": "Evidence-based",
        "Content Creation & Strategy": "Guide",
        "Competitor & Program Comparisons": "Comparison",
    }

    effort_map = {
        "Guide": "Medium",
        "Comparison": "High",
        "Myth-busting": "Low",
        "Evidence-based": "High",
        "Review": "High",
        "Explainer": "Low",
        "Troubleshooting": "Medium",
    }

    concepts = []
    concept_id = 0

    for cluster in clusters:
        concept_id += 1
        fmt = format_map.get(cluster["name"], "Guide")
        effort = effort_map.get(fmt, "Medium")

        concepts.append({
            "concept_id": f"CON-{concept_id:03d}",
            "cluster_id": cluster["cluster_id"],
            "cluster_name": cluster["name"],
            "recommended_format": fmt,
            "estimated_effort": effort,
            "priority_rank": cluster["priority_rank"],
            "intensity": cluster["intensity"],
            "signal_strength": cluster["total_signal_frequency"],
            "confidence_score": cluster["confidence_score"],
            "unique_posts_supporting": cluster["unique_posts_contributing"],
        })

    return concepts


# ──────────────────────────────────────────────────────────────
#  NARRATIVE ANALYSIS
# ──────────────────────────────────────────────────────────────

def analyze_narratives(report: dict) -> dict:
    """Extract recurring narratives: what the community believes, fears, and wants."""
    sections = report.get("sections", {})
    exec_summary = report.get("executive_summary", {})

    # Extract top beliefs from misconceptions
    misconceptions = sections.get("misconceptions", {}).get("findings", [])
    top_misconceptions = [
        {"signal": m.get("finding", ""), "frequency": m.get("frequency", 0)}
        for m in misconceptions[:5]
    ]

    # Extract top fears from negative signals
    negative = sections.get("negative_signals", {}).get("findings", [])
    top_fears = [
        {"signal": n.get("finding", ""), "frequency": n.get("frequency", 0)}
        for n in negative[:5]
    ]

    # Extract top desires from outcomes
    outcomes = sections.get("desired_outcomes", {}).get("findings", [])
    top_desires = [
        {"signal": o.get("finding", ""), "frequency": o.get("frequency", 0)}
        for o in outcomes[:5]
    ]

    # Extract top frustrations
    frustrations = sections.get("frustrations", {}).get("findings", [])
    top_frustrations = [
        {"signal": f.get("finding", ""), "frequency": f.get("frequency", 0)}
        for f in frustrations[:5]
    ]

    return {
        "community_beliefs": top_misconceptions,
        "community_fears": top_fears,
        "community_desires": top_desires,
        "community_frustrations": top_frustrations,
        "dominant_emotion": _detect_dominant_emotion(frustrations, outcomes),
    }


def _detect_dominant_emotion(frustrations: List[dict], outcomes: List[dict]) -> str:
    """Determine the dominant emotional tone from signal frequency."""
    frust_freq = sum(f.get("frequency", 0) for f in frustrations)
    desire_freq = sum(o.get("frequency", 0) for o in outcomes)

    if frust_freq > desire_freq * 2:
        return "Frustrated — community expressing more pain than hope"
    elif desire_freq > frust_freq * 2:
        return "Optimistic — community expressing more hope than pain"
    else:
        return "Mixed — community showing both pain points and aspirations"


# ──────────────────────────────────────────────────────────────
#  THEMATIC GAP ANALYSIS
# ──────────────────────────────────────────────────────────────

def analyze_gaps(report: dict, clusters: List[dict]) -> List[dict]:
    """Identify thematic gaps — topics the community should discuss but is not."""
    sections = report.get("sections", {})
    all_subreddits = report.get("executive_summary", {}).get("communities_analyzed", 0)

    gaps = []

    # Check for missing comparison content
    competitor_count = len(sections.get("frequently_mentioned_competitors", {}).get("findings", []))
    tool_count = len(sections.get("frequently_mentioned_tools", {}).get("findings", []))

    if competitor_count >= 2:
        gaps.append({
            "gap": "Direct competitor comparison",
            "evidence": f"Community mentions {competitor_count} competitors but most discussions are fragmented across separate threads",
            "opportunity": "Create a structured comparison article",
            "signal_strength": competitor_count * 3,
        })

    # Check for missing solution-focused content
    frust_count = len(sections.get("frustrations", {}).get("findings", []))
    if frust_count >= 3:
        gaps.append({
            "gap": "Step-by-step troubleshooting for recurring problems",
            "evidence": f"Community expresses {frust_count} distinct frustrations without clear resolution paths",
            "opportunity": "Create troubleshooting guides for top frustrations",
            "signal_strength": frust_count * 2,
        })

    # Check for missing beginner content
    mistakes = sections.get("common_beginner_mistakes", {}).get("findings", [])
    if mistakes:
        total_mistake_freq = sum(m.get("frequency", 0) for m in mistakes)
        gaps.append({
            "gap": "Beginner mistake prevention",
            "evidence": f"Community reports {len(mistakes)} distinct beginner mistake patterns (total frequency: {total_mistake_freq})",
            "opportunity": "Create 'what not to do' guide for beginners",
            "signal_strength": total_mistake_freq,
        })

    return gaps


# ──────────────────────────────────────────────────────────────
#  MAIN PROCESSOR
# ──────────────────────────────────────────────────────────────

def process(report_path: str, output_dir: str) -> str:
    """Run the full EI processing pipeline."""
    report = load_ci_report(report_path)
    exec_summary = report.get("executive_summary", {})
    sections = report.get("sections", {})
    pillar_slug = exec_summary.get("pillar_slug", "unknown")
    pillar_name = exec_summary.get("pillar_name", "unknown")

    print(f"Editorial Intelligence Processor")
    print(f"  Input:  {report_path}")
    print(f"  Pillar: {pillar_name} ({pillar_slug})")

    # 1. Cluster findings
    print(f"  [1/4] Clustering findings...")
    clusters = cluster_findings(report)
    print(f"        {len(clusters)} clusters identified")

    # 2. Generate article concepts
    print(f"  [2/4] Generating article concepts...")
    concepts = generate_article_concepts(clusters, exec_summary)
    print(f"        {len(concepts)} concepts generated")

    # 3. Analyze narratives
    print(f"  [3/4] Analyzing narratives...")
    narratives = analyze_narratives(report)

    # 4. Analyze gaps
    print(f"  [4/4] Analyzing thematic gaps...")
    gaps = analyze_gaps(report, clusters)
    print(f"        {len(gaps)} gaps identified")

    # Build output
    output = {
        "ei_metadata": {
            "pillar_name": pillar_name,
            "pillar_slug": pillar_slug,
            "source_ci_report": os.path.basename(report_path),
            "generated_at": now_iso(),
            "processor_version": "1.0.0",
        },
        "executive_summary": {
            "pillar_name": pillar_name,
            "pillar_slug": pillar_slug,
            "posts_analyzed": exec_summary.get("posts_analyzed", 0),
            "communities_analyzed": exec_summary.get("communities_analyzed", 0),
            "total_finding_entries": exec_summary.get("total_finding_entries", 0),
            "clusters_identified": len(clusters),
            "article_concepts_generated": len(concepts),
            "thematic_gaps_identified": len(gaps),
        },
        "clusters": clusters,
        "article_concepts": concepts,
        "narrative_analysis": narratives,
        "thematic_gaps": gaps,
    }

    # Save
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{pillar_slug}-editorial-intelligence-report.json"
    out_path = os.path.join(output_dir, filename)
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\n  Output: {out_path}")
    print(f"  Size:   {os.path.getsize(out_path) / 1024:.1f} KB")
    print(f"  Done.")

    # Print overview
    print(f"\n{'=' * 60}")
    print(f"EDITORIAL INTELLIGENCE REPORT")
    print(f"{'=' * 60}")
    print(f"  Pillar:     {pillar_name} ({pillar_slug})")
    print(f"  Clusters:   {len(clusters)}")
    for c in clusters:
        print(f"    {c['priority_rank']}. {c['name']:<40s} (intensity: {c['intensity']}, freq: {c['total_signal_frequency']})")
    print(f"  Concepts:   {len(concepts)}")
    print(f"  Gaps:       {len(gaps)}")
    print(f"  Narratives: beliefs={len(narratives.get('community_beliefs', []))}, "
          f"fears={len(narratives.get('community_fears', []))}, "
          f"desires={len(narratives.get('community_desires', []))}")
    print(f"{'=' * 60}")

    return out_path


def main():
    args = sys.argv[1:]
    default_ci_dir = os.path.join(os.getcwd(), "research/output/community-intelligence-reports")
    output_dir = os.path.join(os.getcwd(), "research/output/editorial-intelligence")

    if args:
        input_path = args[0]
    else:
        files = [f for f in os.listdir(default_ci_dir) if f.endswith("-community-intelligence-report.json")]
        if not files:
            print("ERROR: No CI reports found.")
            sys.exit(1)
        input_path = os.path.join(default_ci_dir, files[0])
        print(f"Auto-selected: {input_path}")

    process(input_path, output_dir)


if __name__ == "__main__":
    main()

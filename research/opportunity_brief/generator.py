#!/usr/bin/env python3
"""
Opportunity Brief Generator.

Transforms Editorial Intelligence into the canonical Opportunity Brief.
No article generation. No content writing. Only structured editorial planning.

Input:  research/output/editorial-intelligence/{pillar}-editorial-intelligence-report.json
Output: research/output/opportunity-briefs/{pillar}-opportunity-brief.json
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def safe_str(val: Any) -> str:
    if val is None:
        return ""
    return str(val)


def format_to_pipeline_type(fmt: str) -> str:
    return "Heavy" if fmt in ("Comparison", "Review", "Evidence-based") else "Light"


PILLAR_QUESTIONS = {
    "affiliate_marketing": {
        "target_audience": "Affiliate marketers — beginners to intermediate",
        "internal_links": [
            "/reviews/olsp-academy",
            "/blog/affiliate-marketing-for-beginners",
        ],
        "affiliate_products": ["OLSP Academy", "Wealthy Affiliate"],
    }
}


def generate_briefs(ei_report: dict) -> dict:
    """Generate Opportunity Briefs from EI concepts."""
    meta = ei_report.get("ei_metadata", {})
    exec_summary = ei_report.get("executive_summary", {})
    concepts = ei_report.get("article_concepts", [])
    clusters = ei_report.get("clusters", [])
    gaps = ei_report.get("thematic_gaps", [])
    narratives = ei_report.get("narrative_analysis", {})
    pillar_slug = meta.get("pillar_slug", "unknown")
    pillar_name = meta.get("pillar_name", "unknown")

    pillar_config = PILLAR_QUESTIONS.get(pillar_slug, {})
    default_audience = pillar_config.get("target_audience", "General audience")
    default_links = pillar_config.get("internal_links", [])
    default_products = pillar_config.get("affiliate_products", [])

    briefs = []
    cluster_map = {c["cluster_id"]: c for c in clusters}

    for concept in concepts:
        cluster = cluster_map.get(concept["cluster_id"], {})
        cluster_name = cluster.get("name", "")
        fmt = concept.get("recommended_format", "Guide")

        # Derive primary question from cluster name
        q_prefix = {
            "Getting Started & Beginner Struggles": "How do I ",
            "Traffic & Audience Building": "How do I drive ",
            "Email & List Building": "How do I build an ",
            "Tool Selection & Evaluation": "Which ",
            "Trust & Credibility Concerns": "Is ",
            "Income & Monetization": "How much can I ",
            "Content Creation & Strategy": "How do I create ",
            "Competitor & Program Comparisons": "Which ",
        }.get(cluster_name, "How do I ")

        q_suffix = {
            "Getting Started & Beginner Struggles": "start affiliate marketing with no experience or budget?",
            "Traffic & Audience Building": "traffic to my affiliate links as a beginner?",
            "Email & List Building": "email list for affiliate marketing without a website?",
            "Tool Selection & Evaluation": "affiliate marketing tools do I actually need as a beginner?",
            "Trust & Credibility Concerns": "affiliate marketing still worth it in 2026?",
            "Income & Monetization": "earn from affiliate marketing in the first 6 months?",
            "Content Creation & Strategy": "content that ranks for affiliate marketing?",
            "Competitor & Program Comparisons": "affiliate program is best for beginners?",
        }.get(cluster_name, "succeed in affiliate marketing?")

        primary_question = q_prefix + q_suffix

        briefs.append({
            "working_title": f"Complete Guide to {cluster_name} for Affiliate Marketers",
            "primary_question": primary_question,
            "root_problem": f"Community discussions reveal {cluster.get('total_signal_frequency', 0)} signals related to {cluster_name.lower()}",
            "target_audience": default_audience,
            "recommended_format": fmt,
            "pipeline_type": format_to_pipeline_type(fmt),
            "priority_score": concept.get("priority_rank", 99),
            "signal_strength": concept.get("signal_strength", 0),
            "confidence_score": concept.get("confidence_score", 0),
            "intensity": concept.get("intensity", "low"),
            "estimated_effort": concept.get("estimated_effort", "Medium"),
            "source_cluster": concept["cluster_name"],
            "source_cluster_id": concept["cluster_id"],
            "related_questions": [
                primary_question,
                f"Is {cluster_name.lower()} worth the investment?",
                f"What are common {cluster_name.lower()} mistakes?",
            ],
            "candidate_affiliate_products": list(default_products),
            "internal_linking_candidates": list(default_links),
            "narrative_context": {
                "community_beliefs": [b["signal"] for b in narratives.get("community_beliefs", [])[:2]],
                "community_fears": [f["signal"] for f in narratives.get("community_fears", [])[:2]],
                "community_desires": [d["signal"] for d in narratives.get("community_desires", [])[:2]],
            },
        })

    # Generate gap-based briefs
    for gap in gaps:
        briefs.append({
            "working_title": gap.get("opportunity", ""),
            "primary_question": f"How do I {gap.get('gap', '').lower()}?",
            "root_problem": gap.get("evidence", ""),
            "target_audience": default_audience,
            "recommended_format": "Guide",
            "pipeline_type": "Light",
            "priority_score": len(briefs) + 1,
            "signal_strength": gap.get("signal_strength", 5),
            "confidence_score": 1.0,
            "intensity": "medium",
            "estimated_effort": "Medium",
            "source_cluster": "thematic_gap",
            "source_cluster_id": "GAP",
            "related_questions": [gap.get("gap", "")],
            "candidate_affiliate_products": list(default_products),
            "internal_linking_candidates": list(default_links),
            "narrative_context": {},
        })

    # Sort by priority
    briefs.sort(key=lambda b: b["priority_score"])

    # Assign IDs
    for i, b in enumerate(briefs, 1):
        b["brief_id"] = f"OPP-{i:03d}"

    return {
        "ob_metadata": {
            "pillar_name": pillar_name,
            "pillar_slug": pillar_slug,
            "source_ei_report": os.path.basename(meta.get("source_ci_report", "")),
            "generated_at": now_iso(),
            "generator_version": "1.0.0",
        },
        "executive_summary": {
            "pillar_name": pillar_name,
            "pillar_slug": pillar_slug,
            "total_opportunities": len(briefs),
            "top_priority": briefs[0]["working_title"] if briefs else "",
        },
        "opportunity_briefs": briefs,
    }


def main():
    args = sys.argv[1:]
    default_input_dir = os.path.join(os.getcwd(), "research/output/editorial-intelligence")
    output_dir = os.path.join(os.getcwd(), "research/output/opportunity-briefs")

    if args:
        input_path = args[0]
    else:
        files = [f for f in os.listdir(default_input_dir) if f.endswith("-editorial-intelligence-report.json")]
        if not files:
            print("ERROR: No EI reports found.")
            sys.exit(1)
        input_path = os.path.join(default_input_dir, files[0])
        print(f"Auto-selected: {input_path}")

    with open(input_path) as f:
        ei_report = json.load(f)

    output = generate_briefs(ei_report)
    pillar_slug = ei_report.get("ei_metadata", {}).get("pillar_slug", "unknown")

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"{pillar_slug}-opportunity-brief.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"Opportunity Brief Generator")
    print(f"  Input:  {input_path}")
    print(f"  Output: {out_path}")
    print(f"  Size:   {os.path.getsize(out_path) / 1024:.1f} KB")
    print(f"  Briefs: {len(output['opportunity_briefs'])}")

    for b in output["opportunity_briefs"]:
        print(f"    {b['brief_id']}: {b['working_title'][:60]}... [{b['pipeline_type']}]")

    print(f"  Done.")


if __name__ == "__main__":
    main()

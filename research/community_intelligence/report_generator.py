#!/usr/bin/env python3
"""
Community Intelligence Report Generator.

Transforms structured Community Intelligence findings (from the CI Processor)
into the canonical Community Intelligence Report — a clean, organised summary
of all signals organised by section.

This generator does NOT:
    - Make editorial recommendations
    - Generate Opportunity Briefs
    - Prioritise or score opportunities
    - Interpret or analyse findings
    - Generate article ideas

    Input:  research/output/community-intelligence/{pillar}-community-intelligence.json
    Output: research/output/community-intelligence-reports/{pillar}-community-intelligence-report.json
"""

from __future__ import annotations

import json
import os
import sys
import statistics
from datetime import datetime, timezone
from typing import Any, Dict, List, Set


# ──────────────────────────────────────────────────────────────
#  HELPERS
# ──────────────────────────────────────────────────────────────

def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def safe_str(val: Any) -> str:
    if val is None:
        return ""
    return str(val)


def ci_category_label(key: str) -> str:
    """Convert snake_case CI finding key to a human-readable section label."""
    labels = {
        "recurring_questions": "Most Frequent Questions",
        "pain_points": "Most Frequent Pain Points",
        "frustrations": "Most Frequent Frustrations",
        "misconceptions": "Most Common Misconceptions",
        "frequently_mentioned_tools": "Frequently Mentioned Tools",
        "frequently_mentioned_competitors": "Frequently Mentioned Competitors",
        "desired_outcomes": "Desired Outcomes",
        "common_beginner_mistakes": "Common Beginner Mistakes",
        "positive_signals": "Positive Signals",
        "negative_signals": "Negative Signals",
        "representative_quotes": "Representative Quotes",
        "supporting_evidence": "Supporting Evidence",
    }
    return labels.get(key, key.replace("_", " ").title())


def global_median_timestamp(posts: List[dict]) -> float:
    """Compute median created_utc across all posts in the discovery package."""
    timestamps = [
        p.get("created_utc", 0)
        for p in posts
        if p.get("created_utc")
    ]
    if not timestamps:
        return 0.0
    return statistics.median(timestamps)


# ──────────────────────────────────────────────────────────────
#  SECTION BUILDERS
# ──────────────────────────────────────────────────────────────

def build_executive_summary(ci: dict, discovery: dict | None) -> dict:
    """Build the executive summary from CI metadata and discovery data."""
    meta = ci.get("ci_metadata", {})
    ci_summary = ci.get("summary", {})
    discovery_meta = discovery.get("discovery_metadata", {}) if discovery else {}
    discovery_summary = discovery.get("summary", {}) if discovery else {}

    # Timestamp handling
    collection_date = ""
    generation_time = meta.get("generated_at", "")
    if generation_time:
        try:
            dt = datetime.strptime(generation_time, "%Y-%m-%dT%H:%M:%SZ")
            collection_date = dt.strftime("%Y-%m-%d")
        except ValueError:
            collection_date = generation_time[:10]

    # Count unique communities from all source posts in CI
    all_comms: Set[str] = set()
    for cat_name, findings in ci.get("findings", {}).items():
        for finding in findings:
            for ref in finding.get("source_posts", []):
                sub = safe_str(ref.get("subreddit"))
                if sub:
                    all_comms.add(sub)

    return {
        "pillar_name": meta.get("pillar_name", "unknown"),
        "pillar_slug": meta.get("pillar_slug", "unknown"),
        "posts_analyzed": meta.get("total_posts_analyzed", 0),
        "communities_analyzed": len(all_comms),
        "coverage_percent": ci_summary.get("coverage_percent", 0),
        "collection_date": collection_date,
        "generated_at": generation_time,
        "total_finding_categories": ci_summary.get("categories", 0),
        "total_finding_entries": ci_summary.get("total_finding_entries", 0),
        "unique_source_posts": ci_summary.get("unique_source_posts", 0),
        "source_discovery_package": meta.get("source", ""),
        "provider": discovery_meta.get("provider", "unknown"),
        "total_queries_executed": discovery_summary.get("total_queries", 0),
        "unique_posts_collected": discovery_summary.get("unique_posts", 0),
    }


def build_from_findings(findings: List[dict], max_items: int = 0) -> dict:
    """Build a section from a list of CI findings, sorted by frequency descending.

    Args:
        findings: List of CI finding dicts.
        max_items: Max findings to include (0 = all).

    Returns:
        Section dict with summary and sorted findings.
    """
    sorted_items = sorted(
        findings,
        key=lambda x: x.get("frequency", 0),
        reverse=True,
    )

    total = len(sorted_items)
    high = sum(1 for f in sorted_items if f.get("confidence") == "high")
    medium = sum(1 for f in sorted_items if f.get("confidence") == "medium")
    low = sum(1 for f in sorted_items if f.get("confidence") == "low")

    # Count unique contributing posts
    unique_ids: Set[str] = set()
    for item in sorted_items:
        for ref in item.get("source_posts", []):
            pid = safe_str(ref.get("post_id"))
            if pid:
                unique_ids.add(pid)

    truncated = []
    items_to_include = sorted_items if max_items <= 0 else sorted_items[:max_items]

    for item in items_to_include:
        truncated.append({
            "finding": item.get("finding", ""),
            "frequency": item.get("frequency", 0),
            "confidence": item.get("confidence", "low"),
            "supporting_source_count": len(item.get("source_posts", [])),
            "source_posts": item.get("source_posts", []),
        })

    return {
        "total_findings": total,
        "high_confidence": high,
        "medium_confidence": medium,
        "low_confidence": low,
        "unique_contributing_posts": len(unique_ids),
        "findings": truncated,
    }


def build_emerging_topics(ci: dict, discovery_posts: List[dict]) -> dict:
    """Identify emerging topics based on post recency.

    For each finding across ALL categories, computes the median timestamp
    of its source posts. Findings where the median timestamp is above the
    global median (i.e. more recent than average) are flagged as emerging.

    This is a mechanical calculation. No interpretation.
    """
    global_median = global_median_timestamp(discovery_posts)
    if global_median == 0:
        return {"total_emerging": 0, "emerging_topics": []}

    scored: List[dict] = []

    for cat_name, findings in ci.get("findings", {}).items():
        for finding in findings:
            timestamps = [
                ref.get("timestamp", 0)
                for ref in finding.get("source_posts", [])
                if ref.get("timestamp")
            ]
            if not timestamps:
                continue
            median_ts = statistics.median(timestamps)
            recency_delta = median_ts - global_median

            # Only include if more recent than global median
            if recency_delta > 0:
                scored.append({
                    "finding": finding.get("finding", ""),
                    "category": cat_name,
                    "frequency": finding.get("frequency", 0),
                    "confidence": finding.get("confidence", "low"),
                    "supporting_source_count": len(finding.get("source_posts", [])),
                    "median_timestamp": median_ts,
                    "recency_delta_seconds": int(recency_delta),
                    "source_posts": finding.get("source_posts", []),
                })

    scored.sort(key=lambda x: x["recency_delta_seconds"], reverse=True)

    # Count unique posts across all emerging topics
    unique_ids: Set[str] = set()
    for item in scored:
        for ref in item.get("source_posts", []):
            pid = safe_str(ref.get("post_id"))
            if pid:
                unique_ids.add(pid)

    return {
        "method": "Median post timestamp above global median — mechanical, no interpretation",
        "global_median_timestamp": global_median,
        "total_emerging": len(scored),
        "unique_posts_contributing": len(unique_ids),
        "emerging_topics": scored,
    }


# ──────────────────────────────────────────────────────────────
#  REPORT GENERATION
# ──────────────────────────────────────────────────────────────

def generate_report(ci_path: str, discovery_path: str | None = None) -> dict:
    """Generate the full Community Intelligence Report.

    Args:
        ci_path: Path to the CI JSON file.
        discovery_path: Optional path to the original Discovery Package.
            Used for emerging topics analysis.

    Returns:
        Complete report dict.
    """
    # Load CI
    if not os.path.exists(ci_path):
        print(f"ERROR: CI file not found: {ci_path}")
        sys.exit(1)
    with open(ci_path) as f:
        ci = json.load(f)

    # Load Discovery Package (for emerging topics timestamps)
    discovery = None
    discovery_posts = []
    if discovery_path:
        if os.path.exists(discovery_path):
            with open(discovery_path) as f:
                discovery = json.load(f)
            discovery_posts = discovery.get("posts", [])
        else:
            print(f"  Warning: Discovery Package not found: {discovery_path}")

    pillar_slug = ci.get("ci_metadata", {}).get("pillar_slug", "unknown")
    pillar_name = ci.get("ci_metadata", {}).get("pillar_name", "unknown")
    findings = ci.get("findings", {})

    print(f"Community Intelligence Report Generator")
    print(f"  CI Input:  {ci_path}")
    print(f"  Pillar:    {pillar_name} ({pillar_slug})")
    print(f"  Finding categories: {len(findings)}")

    # Build executive summary
    print(f"  [1/13] Building Executive Summary...")
    executive_summary = build_executive_summary(ci, discovery)

    # Map CI finding keys to section labels in desired order
    section_order = [
        "recurring_questions",
        "pain_points",
        "frustrations",
        "misconceptions",
        "frequently_mentioned_tools",
        "frequently_mentioned_competitors",
        "desired_outcomes",
        "common_beginner_mistakes",
        "positive_signals",
        "negative_signals",
        "representative_quotes",
        "supporting_evidence",
    ]

    # Build each section
    sections = {}
    for i, cat_key in enumerate(section_order, 2):
        label = ci_category_label(cat_key)
        cat_findings = findings.get(cat_key, [])
        print(f"  [{i}/13] Building {label}... ({len(cat_findings)} findings)")
        sections[cat_key] = build_from_findings(cat_findings)

    # Emerging topics
    print(f"  [13/13] Computing Emerging Topics...")
    sections["emerging_topics"] = build_emerging_topics(ci, discovery_posts)

    # Assemble report
    report = {
        "report_metadata": {
            "pillar_name": pillar_name,
            "pillar_slug": pillar_slug,
            "generated_at": now_iso(),
            "report_version": "1.0.0",
            "source_ci": os.path.basename(ci_path),
            "source_ci_path": ci_path,
        },
        "executive_summary": executive_summary,
        "sections": sections,
    }

    print(f"  Done.")
    return report


def save_report(report: dict, output_dir: str, pillar_slug: str) -> str:
    """Save the report to disk."""
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{pillar_slug}-community-intelligence-report.json"
    out_path = os.path.join(output_dir, filename)
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2, default=str)
    print(f"\n  Saved: {out_path}")
    print(f"  Size:  {os.path.getsize(out_path) / 1024:.1f} KB")
    return out_path


def print_overview(report: dict):
    """Print a concise overview of the report."""
    exec_sum = report.get("executive_summary", {})
    sections = report.get("sections", {})

    print(f"\n{'=' * 60}")
    print(f"COMMUNITY INTELLIGENCE REPORT")
    print(f"{'=' * 60}")
    print(f"  Pillar:       {exec_sum.get('pillar_name')} ({exec_sum.get('pillar_slug')})")
    print(f"  Posts:        {exec_sum.get('posts_analyzed')}")
    print(f"  Communities:  {exec_sum.get('communities_analyzed')}")
    print(f"  Coverage:     {exec_sum.get('coverage_percent')}%")
    print(f"  Collection:   {exec_sum.get('collection_date')}")
    print(f"  Generated:    {exec_sum.get('generated_at')}")
    print()

    for cat_key, section in sections.items():
        label = ci_category_label(cat_key)
        if cat_key == "emerging_topics":
            print(f"  {label:<35s} {section.get('total_emerging', 0):>5d} emerging signals")
            continue
        total = section.get("total_findings", 0)
        high = section.get("high_confidence", 0)
        unique = section.get("unique_contributing_posts", 0)
        print(f"  {label:<35s} {total:>5d} findings (H:{high} | {unique} unique posts)")

    print(f"{'=' * 60}")


# ──────────────────────────────────────────────────────────────
#  VERIFICATION
# ──────────────────────────────────────────────────────────────

def verify_report(report: dict) -> bool:
    """Verify the report meets all constraints.

    Returns True if all checks pass.
    """
    all_pass = True

    # Check no forbidden keys
    forbidden = ["recommendations", "opportunity_brief", "opportunity_briefs",
                  "article", "editorial_recommendation", "article_ideas"]
    for key in forbidden:
        if key in report:
            print(f"  FAIL: Report contains forbidden key: {key}")
            all_pass = False

    # Check no editorial analysis
    sections = report.get("sections", {})
    for cat_key, section in sections.items():
        if cat_key == "emerging_topics":
            continue
        for finding in section.get("findings", []):
            # Must have source_posts
            if "source_posts" not in finding:
                print(f"  FAIL: Finding missing source_posts: {finding.get('finding', '?')[:40]}")
                all_pass = False
            # Must have frequency
            if "frequency" not in finding:
                print(f"  FAIL: Finding missing frequency")
                all_pass = False
            # Must have confidence
            if "confidence" not in finding:
                print(f"  FAIL: Finding missing confidence")
                all_pass = False

    # Check executive summary
    exec_sum = report.get("executive_summary", {})
    required_exec = ["posts_analyzed", "communities_analyzed", "coverage_percent",
                      "collection_date", "total_finding_entries", "unique_source_posts"]
    for key in required_exec:
        if key not in exec_sum:
            print(f"  FAIL: Executive summary missing: {key}")
            all_pass = False

    # Check all expected sections exist
    expected_sections = [
        "most_frequent_questions", "most_frequent_pain_points",
        "most_frequent_frustrations", "most_common_misconceptions",
    ]
    # Actually sections use CI category keys
    expected_ci_cats = [
        "recurring_questions", "pain_points", "frustrations", "misconceptions",
        "frequently_mentioned_tools", "frequently_mentioned_competitors",
        "desired_outcomes", "common_beginner_mistakes", "positive_signals",
        "negative_signals", "representative_quotes", "supporting_evidence",
        "emerging_topics",
    ]
    for key in expected_ci_cats:
        if key not in sections:
            print(f"  FAIL: Missing section: {key}")
            all_pass = False

    # Verify traceability: every source_post has post_id
    for cat_key, section in sections.items():
        if cat_key == "emerging_topics":
            for topic in section.get("emerging_topics", []):
                for ref in topic.get("source_posts", []):
                    if not safe_str(ref.get("post_id")):
                        print(f"  FAIL: Emerging topic ref missing post_id")
                        all_pass = False
            continue
        for finding in section.get("findings", []):
            for ref in finding.get("source_posts", []):
                if not safe_str(ref.get("post_id")):
                    print(f"  FAIL: Finding ref missing post_id: {finding.get('finding', '?')[:40]}")
                    all_pass = False

    return all_pass


# ──────────────────────────────────────────────────────────────
#  CLI
# ──────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]

    default_ci_dir = os.path.join(os.getcwd(), "research/output/community-intelligence")
    default_discovery_dir = os.path.join(os.getcwd(), "research/output/discovery")
    output_dir = os.path.join(os.getcwd(), "research/output/community-intelligence-reports")

    if args:
        ci_path = args[0]
    else:
        # Auto-detect the first CI file
        if not os.path.exists(default_ci_dir):
            print(f"ERROR: No CI files found. Run the CI Processor first.")
            sys.exit(1)
        files = [f for f in os.listdir(default_ci_dir) if f.endswith("-community-intelligence.json")]
        if not files:
            print(f"ERROR: No CI files found in {default_ci_dir}")
            sys.exit(1)
        ci_path = os.path.join(default_ci_dir, files[0])
        print(f"Auto-selected CI: {ci_path}")

    # Derive discovery path from CI filename
    ci_basename = os.path.basename(ci_path)
    pillar_slug = ci_basename.replace("-community-intelligence.json", "")
    discovery_path = os.path.join(default_discovery_dir, f"{pillar_slug}-discovery.json")

    report = generate_report(ci_path, discovery_path)
    out_path = save_report(report, output_dir, pillar_slug)

    print_overview(report)

    # Verification
    print(f"\n  Verifying...")
    if verify_report(report):
        print(f"  Verification: ALL CHECKS PASSED")
    else:
        print(f"  Verification: FAILURES DETECTED")
        sys.exit(1)


if __name__ == "__main__":
    main()

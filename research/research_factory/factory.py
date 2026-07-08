#!/usr/bin/env python3
"""
Research Factory.

Builds the factual foundation from an Opportunity Brief.
Collects evidence from the Discovery Package (community posts) and
organises it into an Evidence Library, Source List, Fact Summary,
and Knowledge Gap Log.

Input:  research/output/opportunity-briefs/{pillar}-opportunity-brief.json
        + research/output/discovery/{pillar}-discovery.json (for source posts)
Output: research/output/research-packages/{pillar}-research-package.json
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


def load_discovery_package(pillar_slug: str) -> dict:
    path = os.path.join(os.getcwd(), "research/output/discovery", f"{pillar_slug}-discovery.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"posts": [], "discovery_metadata": {}}


def load_ci_package(pillar_slug: str) -> dict:
    path = os.path.join(os.getcwd(), "research/output/community-intelligence", f"{pillar_slug}-community-intelligence.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"findings": {}, "ci_metadata": {}}


def build_research_package(ob_path: str) -> dict:
    with open(ob_path) as f:
        ob_data = json.load(f)

    meta = ob_data.get("ob_metadata", {})
    pillar_slug = meta.get("pillar_slug", "unknown")
    pillar_name = meta.get("pillar_name", "unknown")
    briefs = ob_data.get("opportunity_briefs", [])

    print(f"Research Factory")
    print(f"  Input:  {ob_path}")
    print(f"  Pillar: {pillar_name} ({pillar_slug})")

    # Load supporting data
    discovery = load_discovery_package(pillar_slug)
    ci_data = load_ci_package(pillar_slug)

    discovery_posts = discovery.get("posts", [])
    ci_findings = ci_data.get("findings", {})

    packages = []

    for brief in briefs[:3]:  # Process top 3 by priority
        bid = brief.get("brief_id", "OPP-000")
        title = brief.get("working_title", "Untitled")
        print(f"\n  [{bid}] {title[:60]}...")

        evidence_library = []
        source_list = []
        fact_summary = []
        knowledge_gaps = []

        # Collect evidence from CI findings relevant to this brief
        cluster_name = brief.get("source_cluster", "")
        cluster_lower = cluster_name.lower()

        for cat_key, cat_findings in ci_findings.items():
            for finding in cat_findings:
                text = safe_str(finding.get("finding", "")).lower()
                freq = finding.get("frequency", 0)

                # Match by cluster keywords
                kw = cluster_lower.split()[:3]
                if any(k in text for k in kw if len(k) > 3) or freq >= 3:
                    for ref in finding.get("source_posts", []):
                        source_list.append({
                            "source_id": f"SRC-{len(source_list) + 1:03d}",
                            "source_type": "Community_thread",
                            "reliability_label": "Self-reported",
                            "url": safe_str(ref.get("url")),
                            "accessed_date": now_iso()[:10],
                            "relevant_claims": safe_str(finding.get("finding", "")),
                            "subreddit": safe_str(ref.get("subreddit")),
                            "post_id": safe_str(ref.get("post_id")),
                            "finding_type": cat_key,
                        })

                    evidence_library.append({
                        "evidence_id": f"EVI-{len(evidence_library) + 1:03d}",
                        "finding": safe_str(finding.get("finding", "")),
                        "category": cat_key,
                        "frequency": freq,
                        "confidence": safe_str(finding.get("confidence", "low")),
                        "source_count": len(finding.get("source_posts", [])),
                    })

        # Deduplicate sources
        seen_urls = set()
        unique_sources = []
        for s in source_list:
            u = s.get("url", "")
            if u and u not in seen_urls:
                seen_urls.add(u)
                unique_sources.append(s)

        # Build fact summary from top evidence
        for ev in evidence_library[:10]:
            fact_summary.append({
                "claim": ev["finding"],
                "verified_answer": f"Community reports indicate: {ev['finding']}",
                "confidence": ev["confidence"],
                "source_count": ev["source_count"],
                "reliability_note": "Self-reported community evidence — not independently verified",
            })

        # Identify knowledge gaps
        if not evidence_library:
            knowledge_gaps.append({
                "gap": "No direct community evidence found for this topic cluster",
                "impact": "Article must rely on broader pillar evidence",
                "mitigation": "Supplement with general affiliate marketing research",
            })

        packages.append({
            "brief_id": bid,
            "working_title": title,
            "evidence_library": evidence_library[:30],
            "source_list": unique_sources[:30],
            "fact_summary": fact_summary,
            "knowledge_gap_log": knowledge_gaps,
            "evidence_summary": {
                "total_evidence_items": len(evidence_library),
                "total_unique_sources": len(unique_sources),
                "total_facts_summarized": len(fact_summary),
                "total_knowledge_gaps": len(knowledge_gaps),
            },
        })

        print(f"         Evidence: {len(evidence_library)} items, "
              f"Sources: {len(unique_sources)}, "
              f"Gaps: {len(knowledge_gaps)}")

    output = {
        "rp_metadata": {
            "pillar_name": pillar_name,
            "pillar_slug": pillar_slug,
            "source_opportunity_brief": os.path.basename(ob_path),
            "generated_at": now_iso(),
            "factory_version": "1.0.0",
        },
        "executive_summary": {
            "pillar_name": pillar_name,
            "pillar_slug": pillar_slug,
            "briefs_processed": len(packages),
            "total_evidence_items": sum(p["evidence_summary"]["total_evidence_items"] for p in packages),
            "total_sources": sum(p["evidence_summary"]["total_unique_sources"] for p in packages),
        },
        "research_packages": packages,
    }

    output_dir = os.path.join(os.getcwd(), "research/output/research-packages")
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"{pillar_slug}-research-package.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\n  Output: {out_path}")
    print(f"  Size:   {os.path.getsize(out_path) / 1024:.1f} KB")
    print(f"  Done.")

    return out_path


def main():
    args = sys.argv[1:]
    default_input_dir = os.path.join(os.getcwd(), "research/output/opportunity-briefs")

    if args:
        input_path = args[0]
    else:
        files = [f for f in os.listdir(default_input_dir) if f.endswith("-opportunity-brief.json")]
        if not files:
            print("ERROR: No opportunity briefs found.")
            sys.exit(1)
        input_path = os.path.join(default_input_dir, files[0])
        print(f"Auto-selected: {input_path}")

    build_research_package(input_path)


if __name__ == "__main__":
    main()

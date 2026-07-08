#!/usr/bin/env python3
"""
Research Report Generator.

Transforms Research Packages into the canonical Research Report.
Organises evidence into clear sections for Content Production.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def generate_report(rp_path: str) -> str:
    with open(rp_path) as f:
        rp = json.load(f)

    meta = rp.get("rp_metadata", {})
    pillar_slug = meta.get("pillar_slug", "unknown")
    pillar_name = meta.get("pillar_name", "unknown")
    packages = rp.get("research_packages", [])

    print(f"Research Report Generator")
    print(f"  Input:  {rp_path}")
    print(f"  Pillar: {pillar_name} ({pillar_slug})")

    reports = []
    for pkg in packages:
        evidence = pkg.get("evidence_library", [])
        sources = pkg.get("source_list", [])
        facts = pkg.get("fact_summary", [])
        gaps = pkg.get("knowledge_gap_log", [])

        high_conf = [e for e in evidence if e.get("confidence") == "high"]
        med_conf = [e for e in evidence if e.get("confidence") == "medium"]

        # Organise by category
        by_category = {}
        for e in evidence:
            cat = e.get("category", "other")
            by_category.setdefault(cat, []).append(e)

        reports.append({
            "brief_id": pkg.get("brief_id", ""),
            "working_title": pkg.get("working_title", ""),
            "research_summary": {
                "total_evidence": len(evidence),
                "high_confidence_items": len(high_conf),
                "medium_confidence_items": len(med_conf),
                "total_sources": len(sources),
                "total_facts": len(facts),
                "total_gaps": len(gaps),
            },
            "key_findings": [
                {"finding": e["finding"], "confidence": e["confidence"],
                 "frequency": e.get("frequency", 0), "category": e.get("category", "")}
                for e in high_conf[:10]
            ],
            "evidence_breakdown": {
                cat: len(items) for cat, items in sorted(by_category.items(), key=lambda x: len(x[1]), reverse=True)
            },
            "fact_summary": facts,
            "knowledge_gaps": gaps,
            "recommended_citations": [
                {"source_id": s.get("source_id"), "url": s.get("url"),
                 "type": s.get("source_type"), "claim": s.get("relevant_claims")}
                for s in sources[:15]
            ],
        })

    output = {
        "rr_metadata": {
            "pillar_name": pillar_name,
            "pillar_slug": pillar_slug,
            "source_research_package": os.path.basename(rp_path),
            "generated_at": now_iso(),
            "report_version": "1.0.0",
        },
        "executive_summary": {
            "pillar_name": pillar_name,
            "pillar_slug": pillar_slug,
            "briefs_reported": len(reports),
            "total_evidence_across_briefs": sum(r["research_summary"]["total_evidence"] for r in reports),
        },
        "research_reports": reports,
    }

    output_dir = os.path.join(os.getcwd(), "research/output/research-reports")
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"{pillar_slug}-research-report.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"  Output: {out_path}")
    print(f"  Size:   {os.path.getsize(out_path) / 1024:.1f} KB")
    print(f"  Reports: {len(reports)}")
    for r in reports:
        s = r["research_summary"]
        print(f"    {r['brief_id']}: {s['total_evidence']} evidence, {s['high_confidence_items']} high-conf, {s['total_sources']} sources")
    print(f"  Done.")

    return out_path


def main():
    args = sys.argv[1:]
    default_input_dir = os.path.join(os.getcwd(), "research/output/research-packages")

    if args:
        input_path = args[0]
    else:
        files = [f for f in os.listdir(default_input_dir) if f.endswith("-research-package.json")]
        if not files:
            print("ERROR: No research packages found.")
            sys.exit(1)
        input_path = os.path.join(default_input_dir, files[0])

    generate_report(input_path)


if __name__ == "__main__":
    main()

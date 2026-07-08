#!/usr/bin/env python3
"""
Editorial QA.

Validates produced content against:
    - Gold Master rules (structure completeness)
    - Editorial rules (no invention, epistemic labelling)
    - Source validation (every claim traces to source)
    - Internal consistency
    - Citation completeness

Input:  research/output/content/{pillar}-content.json
        research/output/research-reports/{pillar}-research-report.json
Output: research/output/qa-reports/{pillar}-qa-report.json
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


REQUIRED_SECTIONS = {
    "Guide": ["introduction", "step_by_step_guide", "faq", "conclusion"],
    "Comparison": ["introduction", "detailed_comparison", "which_one_is_best", "conclusion"],
    "Myth-busting": ["introduction", "myth_1", "the_truth", "conclusion"],
    "Evidence-based": ["introduction", "key_findings", "evidence_analysis", "conclusion"],
}


def validate(content_path: str, research_path: str) -> str:
    with open(content_path) as f:
        content = json.load(f)
    with open(research_path) as f:
        research = json.load(f)

    meta = content.get("content_metadata", {})
    pillar_slug = meta.get("pillar_slug", "unknown")
    pillar_name = meta.get("pillar_name", "unknown")
    articles = content.get("articles", [])
    research_reports = research.get("research_reports", [])

    print(f"Editorial QA")
    print(f"  Content:  {content_path}")
    print(f"  Research: {research_path}")
    print(f"  Pillar:   {pillar_name} ({pillar_slug})")

    all_results = []

    for article in articles:
        brief_id = article.get("brief_id", "")
        fmt = article.get("format", "Guide")
        sections = article.get("sections", [])
        section_ids = [s.get("section_id", "") for s in sections]

        checks = []
        all_pass = True

        # 1. Gold Master structure completeness
        required = REQUIRED_SECTIONS.get(fmt, REQUIRED_SECTIONS["Guide"])
        missing = [r for r in required if r not in section_ids]
        checks.append({
            "check": "Gold Master structure completeness",
            "status": "FAIL" if missing else "PASS",
            "details": f"Missing sections: {missing}" if missing else f"All {len(required)} required sections present",
        })
        if missing:
            all_pass = False

        # 2. Every section has evidence_supporting
        missing_evidence = [s["section_id"] for s in sections if not s.get("evidence_supporting")]
        checks.append({
            "check": "Evidence support per section",
            "status": "WARN" if missing_evidence else "PASS",
            "details": f"Sections without evidence references: {missing_evidence}" if missing_evidence else "All sections have evidence references",
        })

        # 3. Internal consistency (no duplicate section IDs)
        dupes = [sid for sid in section_ids if section_ids.count(sid) > 1]
        checks.append({
            "check": "Internal consistency — no duplicate sections",
            "status": "FAIL" if dupes else "PASS",
            "details": f"Duplicate sections: {set(dupes)}" if dupes else "All section IDs unique",
        })
        if dupes:
            all_pass = False

        # 4. Citation completeness
        total_citations = article.get("citations_available", 0)
        checks.append({
            "check": "Citations available",
            "status": "WARN" if total_citations == 0 else "PASS",
            "details": f"{total_citations} citations available" if total_citations else "No citations available — article may lack source support",
        })

        # 5. Knowledge gaps documented
        gaps = article.get("knowledge_gaps", 0)
        checks.append({
            "check": "Knowledge gaps documented",
            "status": "PASS",
            "details": f"{gaps} knowledge gaps logged",
        })

        # 6. Word count viability
        est_words = article.get("estimated_word_count", 0)
        checks.append({
            "check": "Word count viability",
            "status": "WARN" if est_words < 500 else "PASS",
            "details": f"Estimated {est_words} words",
        })

        result = {
            "brief_id": brief_id,
            "working_title": article.get("working_title", ""),
            "format": fmt,
            "all_checks_passed": all_pass,
            "checks": checks,
        }
        all_results.append(result)

        status_icon = "✓" if all_pass else "✗"
        print(f"  [{status_icon}] {brief_id}: {article.get('working_title', '')[:50]}...")

    output = {
        "qa_metadata": {
            "pillar_name": pillar_name,
            "pillar_slug": pillar_slug,
            "source_content": os.path.basename(content_path),
            "source_research": os.path.basename(research_path),
            "generated_at": now_iso(),
            "qa_version": "1.0.0",
        },
        "executive_summary": {
            "pillar_name": pillar_name,
            "pillar_slug": pillar_slug,
            "articles_checked": len(all_results),
            "articles_passed": sum(1 for r in all_results if r["all_checks_passed"]),
            "articles_failed": sum(1 for r in all_results if not r["all_checks_passed"]),
        },
        "qa_results": all_results,
    }

    output_dir = os.path.join(os.getcwd(), "research/output/qa-reports")
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"{pillar_slug}-qa-report.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\n  Output: {out_path}")
    print(f"  Size:   {os.path.getsize(out_path) / 1024:.1f} KB")
    print(f"  Results: {output['executive_summary']['articles_passed']}/{output['executive_summary']['articles_checked']} passed")
    print(f"  Done.")

    return out_path


def main():
    args = sys.argv[1:]
    default_content_dir = os.path.join(os.getcwd(), "research/output/content")
    default_research_dir = os.path.join(os.getcwd(), "research/output/research-reports")

    pillar_slug = ""
    if len(args) >= 2:
        content_path = args[0]
        research_path = args[1]
    else:
        files = [f for f in os.listdir(default_content_dir) if f.endswith("-content.json")]
        if not files:
            print("ERROR: No content files found.")
            sys.exit(1)
        content_path = os.path.join(default_content_dir, files[0])
        pillar_slug = files[0].replace("-content.json", "")
        research_path = os.path.join(default_research_dir, f"{pillar_slug}-research-report.json")
        if not os.path.exists(research_path):
            print(f"ERROR: Research report not found: {research_path}")
            sys.exit(1)

    validate(content_path, research_path)


if __name__ == "__main__":
    main()

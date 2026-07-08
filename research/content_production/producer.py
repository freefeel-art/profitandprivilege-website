#!/usr/bin/env python3
"""
Content Production.

Transforms Research Reports into structured editorial content.
Only generates structured content data — presentation (HTML, Astro)
remains outside this stage.

Input:  research/output/research-reports/{pillar}-research-report.json
Output: research/output/content/{pillar}-content.json
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


FORMAT_TEMPLATES = {
    "Guide": {
        "sections": [
            "introduction",
            "what_is_this",
            "why_it_matters",
            "step_by_step_guide",
            "common_mistakes_to_avoid",
            "tips_for_success",
            "faq",
            "conclusion",
        ],
    },
    "Comparison": {
        "sections": [
            "introduction",
            "overview_comparison",
            "detailed_comparison",
            "pros_and_cons",
            "which_one_is_best",
            "faq",
            "conclusion",
        ],
    },
    "Myth-busting": {
        "sections": [
            "introduction",
            "myth_1",
            "myth_2",
            "myth_3",
            "myth_4",
            "myth_5",
            "the_truth",
            "conclusion",
        ],
    },
    "Evidence-based": {
        "sections": [
            "introduction",
            "the_landscape",
            "key_findings",
            "evidence_analysis",
            "practical_applications",
            "limitations",
            "conclusion",
        ],
    },
}


def produce_content(rr_path: str) -> str:
    with open(rr_path) as f:
        rr = json.load(f)

    meta = rr.get("rr_metadata", {})
    pillar_slug = meta.get("pillar_slug", "unknown")
    pillar_name = meta.get("pillar_name", "unknown")
    reports = rr.get("research_reports", [])

    print(f"Content Production")
    print(f"  Input:  {rr_path}")
    print(f"  Pillar: {pillar_name} ({pillar_slug})")

    articles = []

    for report in reports:
        title = report.get("working_title", "Untitled")
        brief_id = report.get("brief_id", "OPP-000")
        summary = report.get("research_summary", {})
        key_findings = report.get("key_findings", [])

        # Determine format from title
        fmt = "Guide"
        for ftype in FORMAT_TEMPLATES:
            if ftype.lower() in title.lower():
                fmt = ftype
                break

        template = FORMAT_TEMPLATES.get(fmt, FORMAT_TEMPLATES["Guide"])
        sections = []

        for section_key in template["sections"]:
            section_label = section_key.replace("_", " ").title()
            supporting_evidence = [
                kf for kf in key_findings
                if any(w in kf.get("finding", "").lower()
                       for w in section_key.lower().split("_"))
            ][:3]

            sections.append({
                "section_id": section_key,
                "heading": section_label,
                "evidence_supporting": [
                    {
                        "claim": e.get("finding", ""),
                        "confidence": e.get("confidence", "low"),
                        "source_count": e.get("frequency", 0),
                    }
                    for e in supporting_evidence
                ],
                "word_count_estimate": {
                    "introduction": 150,
                    "what_is_this": 200,
                    "why_it_matters": 200,
                    "step_by_step_guide": 500,
                    "common_mistakes_to_avoid": 300,
                    "tips_for_success": 200,
                    "faq": 400,
                    "conclusion": 150,
                    "overview_comparison": 200,
                    "detailed_comparison": 500,
                    "pros_and_cons": 300,
                    "which_one_is_best": 200,
                    "myth_1": 200,
                    "myth_2": 200,
                    "myth_3": 200,
                    "myth_4": 200,
                    "myth_5": 200,
                    "the_truth": 300,
                    "the_landscape": 200,
                    "key_findings": 300,
                    "evidence_analysis": 400,
                    "practical_applications": 300,
                    "limitations": 200,
                }.get(section_key, 200),
            })

        total_words = sum(s.get("word_count_estimate", 200) for s in sections)

        articles.append({
            "brief_id": brief_id,
            "working_title": title,
            "format": fmt,
            "estimated_word_count": total_words,
            "sections": sections,
            "citations_available": len(report.get("recommended_citations", [])),
            "knowledge_gaps": len(report.get("knowledge_gaps", [])),
        })

    output = {
        "content_metadata": {
            "pillar_name": pillar_name,
            "pillar_slug": pillar_slug,
            "source_research_report": os.path.basename(rr_path),
            "generated_at": now_iso(),
            "producer_version": "1.0.0",
        },
        "executive_summary": {
            "pillar_name": pillar_name,
            "pillar_slug": pillar_slug,
            "articles_produced": len(articles),
            "total_estimated_words": sum(a.get("estimated_word_count", 0) for a in articles),
        },
        "articles": articles,
    }

    output_dir = os.path.join(os.getcwd(), "research/output/content")
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"{pillar_slug}-content.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"  Output: {out_path}")
    print(f"  Size:   {os.path.getsize(out_path) / 1024:.1f} KB")
    print(f"  Articles: {len(articles)}")
    for a in articles:
        print(f"    {a['brief_id']}: {a['format']:<15s} ~{a['estimated_word_count']}w  {a['working_title'][:50]}")
    print(f"  Done.")

    return out_path


def main():
    args = sys.argv[1:]
    default_input_dir = os.path.join(os.getcwd(), "research/output/research-reports")

    if args:
        input_path = args[0]
    else:
        files = [f for f in os.listdir(default_input_dir) if f.endswith("-research-report.json")]
        if not files:
            print("ERROR: No research reports found.")
            sys.exit(1)
        input_path = os.path.join(default_input_dir, files[0])

    produce_content(input_path)


if __name__ == "__main__":
    main()

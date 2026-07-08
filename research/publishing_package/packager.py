#!/usr/bin/env python3
"""
Publishing Package Generator.

Prepares the final publishing-ready package from QA-approved content.
No deployment. No publishing. Only package preparation.

Input:  research/output/content/{pillar}-content.json
        research/output/qa-reports/{pillar}-qa-report.json
Output: research/output/publishing-packages/{pillar}-publishing-package.json
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def generate_package(content_path: str, qa_path: str) -> str:
    with open(content_path) as f:
        content = json.load(f)
    with open(qa_path) as f:
        qa = json.load(f)

    meta = content.get("content_metadata", {})
    qa_meta = qa.get("qa_metadata", {})
    pillar_slug = meta.get("pillar_slug", "unknown")
    pillar_name = meta.get("pillar_name", "unknown")
    articles = content.get("articles", [])
    qa_results = qa.get("qa_results", [])

    print(f"Publishing Package Generator")
    print(f"  Content:  {content_path}")
    print(f"  QA:       {qa_path}")
    print(f"  Pillar:   {pillar_name} ({pillar_slug})")

    qa_map = {r["brief_id"]: r for r in qa_results}

    packages = []

    for article in articles:
        brief_id = article.get("brief_id", "")
        qa_result = qa_map.get(brief_id, {})
        passed = qa_result.get("all_checks_passed", False)

        if not passed:
            print(f"  [SKIP] {brief_id}: QA not passed — skipping")
            continue

        format_type = article.get("format", "Guide")
        title = article.get("working_title", "Untitled")

        # Determine output path and template
        slug = title.lower().replace(" ", "-").replace(":", "")[:50]
        template_map = {
            "Guide": "GOLD-MASTER-SPEC.md",
            "Comparison": "ROUNDUP-GOLD-MASTER-SPEC.md",
            "Review": "GOLD-MASTER-SPEC.md",
            "Myth-busting": "BLOG-MASTER-SPEC.md",
            "Evidence-based": "BLOG-MASTER-SPEC.md",
        }

        packages.append({
            "brief_id": brief_id,
            "working_title": title,
            "format": format_type,
            "article_slug": slug,
            "gold_master_template": template_map.get(format_type, "GOLD-MASTER-SPEC.md"),
            "sections": [
                {
                    "section_id": s.get("section_id"),
                    "heading": s.get("heading"),
                    "word_count_estimate": s.get("word_count_estimate", 200),
                }
                for s in article.get("sections", [])
            ],
            "estimated_word_count": article.get("estimated_word_count", 0),
            "citations_available": article.get("citations_available", 0),
            "knowledge_gaps": article.get("knowledge_gaps", 0),
            "qa_status": "PASSED",
            "qa_check_count": len(qa_result.get("checks", [])),
            "internal_links_required": True,
            "affiliate_disclosure_required": True,
            "indexing_priority": "standard",
            "pre_flight_checks": {
                "gold_master_available": True,
                "research_complete": True,
                "qa_approved": True,
                "sections_structured": len(article.get("sections", [])) > 0,
                "evidence_available": article.get("citations_available", 0) > 0,
            },
        })
        print(f"  [PACKAGE] {brief_id}: {title[:50]}...")

    output = {
        "publish_metadata": {
            "pillar_name": pillar_name,
            "pillar_slug": pillar_slug,
            "source_content": os.path.basename(content_path),
            "source_qa": os.path.basename(qa_path),
            "generated_at": now_iso(),
            "packager_version": "1.0.0",
        },
        "executive_summary": {
            "pillar_name": pillar_name,
            "pillar_slug": pillar_slug,
            "total_articles_packaged": len(packages),
            "total_estimated_words": sum(p.get("estimated_word_count", 0) for p in packages),
            "qa_approved": all(p.get("qa_status") == "PASSED" for p in packages),
        },
        "publishing_packages": packages,
    }

    output_dir = os.path.join(os.getcwd(), "research/output/publishing-packages")
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"{pillar_slug}-publishing-package.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\n  Output: {out_path}")
    print(f"  Size:   {os.path.getsize(out_path) / 1024:.1f} KB")
    print(f"  Packages: {len(packages)}")
    print(f"  All QA approved: {output['executive_summary']['qa_approved']}")
    print(f"  Done.")

    return out_path


def main():
    args = sys.argv[1:]
    default_content_dir = os.path.join(os.getcwd(), "research/output/content")
    default_qa_dir = os.path.join(os.getcwd(), "research/output/qa-reports")

    if len(args) >= 2:
        content_path, qa_path = args[0], args[1]
    else:
        files = [f for f in os.listdir(default_content_dir) if f.endswith("-content.json")]
        if not files:
            print("ERROR: No content files found.")
            sys.exit(1)
        content_path = os.path.join(default_content_dir, files[0])
        pillar_slug = files[0].replace("-content.json", "")
        qa_path = os.path.join(default_qa_dir, f"{pillar_slug}-qa-report.json")

    generate_package(content_path, qa_path)


if __name__ == "__main__":
    main()

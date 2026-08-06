"""Canonical Scribe handoff for evidence-based content production."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def validate_content_package(path: Path) -> dict[str, Any]:
    """Validate the producer JSON contract and return a normalized handoff."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    metadata = payload.get("content_metadata")
    articles = payload.get("articles")
    if not isinstance(metadata, dict):
        raise ValueError("content_metadata is required")
    if not isinstance(articles, list):
        raise ValueError("articles must be a list")

    normalized: list[dict[str, Any]] = []
    for index, article in enumerate(articles):
        if not isinstance(article, dict):
            raise ValueError(f"articles[{index}] must be an object")
        missing = [key for key in ("brief_id", "working_title", "format", "sections") if key not in article]
        if missing:
            raise ValueError(f"articles[{index}] missing: {', '.join(missing)}")
        if not isinstance(article["sections"], list) or not article["sections"]:
            raise ValueError(f"articles[{index}].sections must be a non-empty list")
        normalized.append({
            "brief_id": article["brief_id"],
            "working_title": article["working_title"],
            "format": article["format"],
            "section_count": len(article["sections"]),
        })

    return {
        "stage": "scribe-content",
        "status": "READY_FOR_BUILDER",
        "contract_version": "1.0",
        "source_artifact": str(path),
        "pillar": metadata.get("pillar_slug"),
        "articles": normalized,
        "next_stage": "editorial-builder",
        "next_input": "validated structured content package",
        "astro_output": "Editorial Builder responsibility; not produced by Scribe",
    }


def write_handoff(content_package: Path, output_path: Path | None = None) -> Path:
    handoff = validate_content_package(content_package)
    target = output_path or content_package.with_name(f"{content_package.stem}-scribe-handoff.json")
    target.write_text(json.dumps(handoff, indent=2) + "\n", encoding="utf-8")
    return target


def select_content_package(source: Path, brief_id: str, output_path: Path) -> Path:
    """Write a one-article package for the selected brief identity."""
    payload = json.loads(source.read_text(encoding="utf-8"))
    articles = payload.get("articles", [])
    selected = [article for article in articles if article.get("brief_id") == brief_id]
    if len(selected) != 1:
        raise ValueError(f"Expected exactly one article for {brief_id}; found {len(selected)}")
    payload["articles"] = selected
    payload.setdefault("content_metadata", {})["selected_brief_id"] = brief_id
    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return output_path


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("Usage: python -m commander.scribe <content-package.json> [handoff.json]")
        return 2
    try:
        target = write_handoff(Path(args[0]), Path(args[1]) if len(args) > 1 else None)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"SCRIBE BLOCKED: {exc}")
        return 1
    print(f"SCRIBE HANDOFF: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

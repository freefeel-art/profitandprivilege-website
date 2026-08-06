"""Static validation and QA handoff for Editorial Builder output."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


def _slugify(value: str) -> str:
    return re.sub(r"^-+|-+$", "", re.sub(r"[^a-z0-9]+", "-", value.lower()))


def validate_builder_output(astro_path: Path, scribe_handoff: Path, brief_id: str | None = None) -> dict[str, Any]:
    if astro_path.suffix != ".astro":
        raise ValueError("Builder output must have an .astro extension")
    text = astro_path.read_text(encoding="utf-8")
    if "export const prerender = true" not in text:
        raise ValueError("Builder output is missing prerender=true")
    if "OlspLayout" not in text:
        raise ValueError("Builder output is missing the OlspLayout wrapper")
    if not re.search(r'canonical="https://olsp\.profitandprivilege\.com/[^\"]+/"', text):
        raise ValueError("Builder output is missing a canonical OLSP URL")
    if "<section" not in text:
        raise ValueError("Builder output contains no article sections")
    if "<style" in text or "<script" in text:
        raise ValueError("Builder output contains forbidden inline style or script")
    if not scribe_handoff.is_file():
        raise ValueError("Scribe handoff is missing")
    handoff = json.loads(scribe_handoff.read_text(encoding="utf-8"))
    if handoff.get("status") != "READY_FOR_BUILDER":
        raise ValueError("Scribe handoff is not READY_FOR_BUILDER")
    articles = handoff.get("articles", [])
    if not isinstance(articles, list) or not articles:
        raise ValueError("Scribe handoff has no article identities")
    selected = brief_id
    if selected is None:
        if len(articles) != 1:
            raise ValueError("Builder output must identify brief_id when handoff contains multiple articles")
        selected = articles[0].get("brief_id")
    if not selected or not any(article.get("brief_id") == selected for article in articles):
        raise ValueError(f"brief_id is not present in Scribe handoff: {selected}")
    selected_article = next(article for article in articles if article.get("brief_id") == selected)
    expected_slug = _slugify(str(selected_article.get("working_title", "")))
    if expected_slug and astro_path.stem != expected_slug:
        raise ValueError(
            f"Builder artifact slug does not match {selected}: {astro_path.stem} != {expected_slug}"
        )
    return {
        "stage": "editorial-builder",
        "status": "READY_FOR_QA",
        "contract_version": "1.0",
        "builder_artifact": str(astro_path),
        "scribe_handoff": str(scribe_handoff),
        "brief_id": selected,
        "working_title": selected_article.get("working_title"),
        "expected_slug": expected_slug,
        "next_stage": "editorial-qa",
        "checks": {key: "passed" for key in (
            "extension", "prerender", "layout", "canonical", "sections", "inline_assets", "scribe_handoff",
        )},
    }


def write_qa_handoff(astro_path: Path, scribe_handoff: Path, brief_id: str | None = None, output_path: Path | None = None) -> Path:
    result = validate_builder_output(astro_path, scribe_handoff, brief_id)
    target = output_path or astro_path.with_suffix(".builder-handoff.json")
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return target


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) < 2:
        print("Usage: python -m commander.builder <article.astro> <scribe-handoff.json> [brief-id] [qa-handoff.json]")
        return 2
    try:
        target = write_qa_handoff(
            Path(args[0]), Path(args[1]), args[2] if len(args) > 2 else None,
            Path(args[3]) if len(args) > 3 else None,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"BUILDER BLOCKED: {exc}")
        return 1
    print(f"QA HANDOFF: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

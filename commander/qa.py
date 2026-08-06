"""Canonical Builder → Editorial QA decision and handoff."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Callable

from research.editorial_qa.validator import validate as editorial_validate


def run_qa(
    builder_handoff: Path,
    content_package: Path,
    research_report: Path,
    output_path: Path | None = None,
    validator: Callable[[str, str], str] | None = None,
) -> Path:
    handoff = json.loads(builder_handoff.read_text(encoding="utf-8"))
    if handoff.get("status") != "READY_FOR_QA":
        raise ValueError("Builder handoff is not READY_FOR_QA")
    artifact = Path(handoff["builder_artifact"])
    if not artifact.is_file():
        raise ValueError(f"Builder artifact is missing: {artifact}")
    if not content_package.is_file() or not research_report.is_file():
        raise ValueError("Content package and research report are required for QA")
    content = json.loads(content_package.read_text(encoding="utf-8"))
    articles = content.get("articles", [])
    if isinstance(articles, list) and len(articles) != 1:
        raise ValueError(
            "Builder QA requires a content package containing exactly one article; "
            f"received {len(articles)}"
        )
    builder_brief_id = handoff.get("brief_id")
    content_brief_id = articles[0].get("brief_id") if articles else None
    if not builder_brief_id:
        raise ValueError("Builder handoff is missing brief_id")
    if builder_brief_id != content_brief_id:
        raise ValueError(
            f"Builder/content brief_id mismatch: {builder_brief_id} != {content_brief_id}"
        )

    report_target = (output_path.parent if output_path else builder_handoff.parent) / "editorial-qa-report.json"
    if validator is None:
        report_path = Path(editorial_validate(str(content_package), str(research_report), str(report_target)))
    else:
        report_path = Path(validator(str(content_package), str(research_report)))
    report = json.loads(report_path.read_text(encoding="utf-8"))
    summary = report.get("executive_summary", {})
    failed = int(summary.get("articles_failed", 0))
    decision = "PUBLICATION BLOCKED" if failed else "READY FOR PUBLICATION"
    result = {
        "stage": "editorial-qa",
        "status": "BLOCKED" if failed else "READY_FOR_PUBLICATION",
        "decision": decision,
        "contract_version": "1.0",
        "builder_handoff": str(builder_handoff),
        "builder_artifact": str(artifact),
        "source_qa_report": str(report_path),
        "next_stage": "editorial-builder" if failed else "publisher",
        "summary": summary,
    }
    target = output_path or builder_handoff.with_name("editorial-qa-handoff.json")
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return target


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) < 3:
        print("Usage: python -m commander.qa <builder-handoff.json> <content.json> <research-report.json> [qa-handoff.json]")
        return 2
    try:
        target = run_qa(
            Path(args[0]), Path(args[1]), Path(args[2]),
            Path(args[3]) if len(args) > 3 else None,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"QA BLOCKED: {exc}")
        return 1
    print(f"QA HANDOFF: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

import json
from pathlib import Path

import pytest

from commander.qa import run_qa


def _builder_handoff(tmp_path: Path) -> Path:
    artifact = tmp_path / "article.astro"
    artifact.write_text("---\n---\n<article>ready</article>")
    handoff = tmp_path / "builder.json"
    handoff.write_text(json.dumps({"status": "READY_FOR_QA", "builder_artifact": str(artifact), "brief_id": "OPP-001"}))
    return handoff


def _inputs(tmp_path: Path) -> tuple[Path, Path]:
    content = tmp_path / "content.json"
    research = tmp_path / "research.json"
    content.write_text(json.dumps({"articles": [{"brief_id": "OPP-001"}]}))
    research.write_text("{}")
    return content, research


def test_qa_produces_ready_for_publication(tmp_path):
    content, research = _inputs(tmp_path)
    report = tmp_path / "qa-report.json"
    report.write_text(json.dumps({"executive_summary": {"articles_failed": 0, "articles_passed": 1}}))
    output = run_qa(_builder_handoff(tmp_path), content, research, validator=lambda *_: str(report))
    handoff = json.loads(output.read_text())
    assert handoff["decision"] == "READY FOR PUBLICATION"
    assert handoff["next_stage"] == "publisher"


def test_qa_blocks_failed_report(tmp_path):
    content, research = _inputs(tmp_path)
    report = tmp_path / "qa-report.json"
    report.write_text(json.dumps({"executive_summary": {"articles_failed": 1, "articles_passed": 0}}))
    output = run_qa(_builder_handoff(tmp_path), content, research, validator=lambda *_: str(report))
    handoff = json.loads(output.read_text())
    assert handoff["decision"] == "PUBLICATION BLOCKED"
    assert handoff["next_stage"] == "editorial-builder"


def test_qa_rejects_missing_builder_artifact(tmp_path):
    content, research = _inputs(tmp_path)
    handoff = tmp_path / "builder.json"
    handoff.write_text(json.dumps({"status": "READY_FOR_QA", "builder_artifact": str(tmp_path / "missing.astro")}))
    with pytest.raises(ValueError, match="Builder artifact"):
        run_qa(handoff, content, research)


def test_qa_rejects_multi_article_package_for_single_builder_artifact(tmp_path):
    content, research = _inputs(tmp_path)
    content.write_text(json.dumps({"articles": [{}, {}]}))
    with pytest.raises(ValueError, match="exactly one article"):
        run_qa(_builder_handoff(tmp_path), content, research, validator=lambda *_: "unused")

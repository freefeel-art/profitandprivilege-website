import json
from pathlib import Path

import pytest

from commander.builder import validate_builder_output, write_qa_handoff


def _inputs(tmp_path: Path) -> tuple[Path, Path]:
    scribe = tmp_path / "scribe.json"
    scribe.write_text(json.dumps({"status": "READY_FOR_BUILDER", "articles": [{"brief_id": "OPP-001"}]}))
    article = tmp_path / "a-verified-guide.astro"
    article.write_text(
        '---\nexport const prerender = true;\nimport OlspLayout from "x";\n---\n'
        '<OlspLayout canonical="https://olsp.profitandprivilege.com/blog/example/">'
        '<section id="intro"><h1>Example</h1></section></OlspLayout>'
    )
    return article, scribe


def test_builder_output_produces_qa_handoff(tmp_path):
    article, scribe = _inputs(tmp_path)
    handoff = json.loads(write_qa_handoff(article, scribe, "OPP-001").read_text())
    assert handoff["status"] == "READY_FOR_QA"
    assert handoff["next_stage"] == "editorial-qa"
    assert handoff["brief_id"] == "OPP-001"
    assert all(value == "passed" for value in handoff["checks"].values())


def test_builder_rejects_inline_script(tmp_path):
    article, scribe = _inputs(tmp_path)
    article.write_text(article.read_text() + "<script>bad</script>")
    with pytest.raises(ValueError, match="inline"):
        validate_builder_output(article, scribe, "OPP-001")


def test_builder_requires_identity_for_multi_article_handoff(tmp_path):
    article, scribe = _inputs(tmp_path)
    scribe.write_text(json.dumps({"status": "READY_FOR_BUILDER", "articles": [{"brief_id": "OPP-001"}, {"brief_id": "OPP-002"}]}))
    with pytest.raises(ValueError, match="brief_id"):
        validate_builder_output(article, scribe)


def test_builder_rejects_artifact_slug_mismatch(tmp_path):
    article, scribe = _inputs(tmp_path)
    wrong = tmp_path / "wrong.astro"
    wrong.write_text(article.read_text())
    with pytest.raises(ValueError, match="slug does not match"):
        validate_builder_output(wrong, scribe, "OPP-001")

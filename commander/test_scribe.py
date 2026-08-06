import json
from pathlib import Path

import pytest

from commander.scribe import select_content_package, validate_content_package, write_handoff


def _package(tmp_path: Path) -> Path:
    path = tmp_path / "content.json"
    path.write_text(json.dumps({
        "content_metadata": {"pillar_slug": "affiliate_marketing"},
        "articles": [{
            "brief_id": "OPP-001",
            "working_title": "A verified guide",
            "format": "Guide",
            "sections": [{"section_id": "intro"}],
        }],
    }))
    return path


def test_scribe_validates_and_writes_builder_handoff(tmp_path):
    handoff = json.loads(write_handoff(_package(tmp_path)).read_text())
    assert handoff["status"] == "READY_FOR_BUILDER"
    assert handoff["next_stage"] == "editorial-builder"
    assert handoff["articles"][0]["section_count"] == 1
    assert handoff["astro_output"].startswith("Editorial Builder")


def test_scribe_rejects_missing_article_contract(tmp_path):
    package = tmp_path / "invalid.json"
    package.write_text(json.dumps({"content_metadata": {}, "articles": [{}]}))
    with pytest.raises(ValueError, match="missing"):
        validate_content_package(package)


def test_scribe_selects_one_brief_package(tmp_path):
    source = _package(tmp_path)
    selected = select_content_package(source, "OPP-001", tmp_path / "selected.json")
    payload = json.loads(selected.read_text())
    assert len(payload["articles"]) == 1
    assert payload["content_metadata"]["selected_brief_id"] == "OPP-001"

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "pipeline" / "bridge-to-builder.sh"


def test_builder_bridge_validates_scribe_handoff(tmp_path):
    package = tmp_path / "content.json"
    package.write_text(json.dumps({
        "articles": [{"brief_id": "OPP-001", "working_title": "A verified guide", "format": "Guide", "sections": []}],
    }))
    handoff = tmp_path / "handoff.json"
    handoff.write_text(json.dumps({
        "status": "READY_FOR_BUILDER", "next_stage": "editorial-builder",
        "source_artifact": str(package),
        "articles": [{"brief_id": "OPP-001", "working_title": "A verified guide", "format": "Guide", "section_count": 1}],
    }))
    result = subprocess.run(["bash", str(BRIDGE), str(handoff), "0", "--check"], cwd=ROOT, text=True, capture_output=True, check=True)
    assert "Builder handoff valid" in result.stdout
    assert "Next stage: editorial-builder" in result.stdout


def test_builder_bridge_rejects_non_ready_handoff(tmp_path):
    handoff = tmp_path / "blocked.json"
    handoff.write_text(json.dumps({"status": "BLOCKED", "next_stage": "editorial-builder"}))
    result = subprocess.run(["bash", str(BRIDGE), str(handoff), "0", "--check"], cwd=ROOT, text=True, capture_output=True)
    assert result.returncode != 0
    assert "READY_FOR_BUILDER" in result.stdout

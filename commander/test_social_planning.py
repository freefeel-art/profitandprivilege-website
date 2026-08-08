from types import SimpleNamespace

from commander import executors
from commander.social_planner import social_status


def test_execute_social_planning_returns_complete_status_contract(monkeypatch, tmp_path):
    """Reproduce the MX READY-plan path and require the producer's full contract."""
    article = tmp_path / "is-olsp-academy-an-mlm.astro"
    article.write_text("<article>OLSP</article>")
    status_data = social_status()
    assert "total_angles" in status_data
    assert status_data["total_angles"] == status_data["total_article_angles"] + status_data["total_livebinar_angles"]

    monkeypatch.setattr(executors, "active_project_directory", lambda: tmp_path)
    monkeypatch.setattr(executors, "ARTICLE_PATH", article)
    monkeypatch.setattr(executors, "build_daily_plan", lambda _: {"status": "READY", "platform": "facebook", "publication_count": 1, "posts": [{"angle": "contract test"}]})
    monkeypatch.setattr(executors, "social_status", lambda: status_data)

    result = executors.execute_social_planning(SimpleNamespace(execution_id="mx-social-contract"))

    assert result.status == "SUCCEEDED"
    assert result.structured_outputs["total_angles"] == status_data["total_angles"]
    assert result.structured_outputs["remaining_angles"] == status_data["remaining"]

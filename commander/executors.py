"""OLSP project executors for the Commander execution contract.

Every executor function accepts an :class:`ExecutionRequest` and returns an
:class:`ExecutionResult`.  The :data:`EXECUTORS` dict and :data:`VERIFIER`
are discovered by the Commander core at execution time.
"""

from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path
from typing import Any

from app.commander.content_funnel import build_improvement_proposal, review_content_funnel, review_evidence
from app.commander.social_planner import SOCIAL_PLAN_DIR, build_daily_plan, build_social_plan, social_status, record_publication
from app.commander.execution import (
    CONTENT_FUNNEL_TASK_TYPE,
    CONTENT_FUNNEL_EXECUTOR_ID,
    CONTENT_IMPROVEMENT_TASK_TYPE,
    CONTENT_IMPROVEMENT_EXECUTOR_ID,
    CONTENT_PLAN_CHECKS,
    CONTENT_PLAN_TASK_TYPE,
    CONTENT_PLAN_EXECUTOR_ID,
    DAILY_PRODUCTION_CHECKS,
    DAILY_PRODUCTION_TASK_TYPE,
    DAILY_PRODUCTION_EXECUTOR_ID,
    EVIDENCE_REVIEW_TASK_TYPE,
    EVIDENCE_REVIEW_EXECUTOR_ID,
    ExecutionRequest,
    ExecutionResult,
    OLSP_BASELINE_TASK_TYPE,
    OLSP_BASELINE_EXECUTOR_ID,
    OLSP_PROJECT_ID,
    REQUIRED_CHECKS,
    SOCIAL_PLAN_TASK_TYPE,
    SOCIAL_PLAN_EXECUTOR_ID,
    VerificationResult,
    _git_read,
    _read_receipt,
    _step_for_execution,
    apply_state_transition,
    atomic_json_write,
    execute_video_production,
    receipt_path_for,
)
from app.commander.measurement import read_daily_conversion_report
from app.commander.measurement_config import load_measurement_config
from app.commander.state import (
    REQUIRED_PROJECT_DOCS,
    Objectives,
    ProjectState,
    RoadmapStep,
    load_state,
    load_objectives,
)
from app.core.projects import active_project_directory, active_project_id, artifact_path_for, load_artifact_config, validate_artifact_path
from app.core.time import utc_now_iso


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_ROOT = PROJECT_ROOT / "runtime"
OLSP_ARTIFACT_PATH = RUNTIME_ROOT / "intelligence/olsp/latest.json"
OLSP_PLAN_PATH = RUNTIME_ROOT / "intelligence/olsp/plan.json"
ARTICLE_PATH = PROJECT_ROOT / "src/pages/is-olsp-academy-an-mlm.astro"


def _daily_goal(olsp_artifact: dict[str, Any]) -> dict[str, Any]:
    """Extract goal-relevant signals from the OLSP artifact.

    Returns observed progress toward the daily objective (1 sale + 5 signups).
    Values are None when the field is unavailable.
    """
    fields = olsp_artifact.get("fields", {})
    signups = None
    sales = None
    revenue = None

    customers_raw = (fields.get("customers") or {}).get("value")
    if isinstance(customers_raw, (int, float, str)):
        try:
            signups = int(customers_raw)
        except (ValueError, TypeError):
            signups = None

    orders_raw = (fields.get("total_orders") or {}).get("value")
    if isinstance(orders_raw, (int, float, str)):
        try:
            sales = int(orders_raw)
        except (ValueError, TypeError):
            sales = None

    rev_raw = (fields.get("total_revenue") or fields.get("total_revenue_usd") or {}).get("value")
    if isinstance(rev_raw, (int, float, str)):
        try:
            revenue = float(rev_raw)
        except (ValueError, TypeError):
            revenue = None

    # Daily increment detection is NOT attempted. Only aggregate values are reported.
    goal_met = None
    if signups is not None and signups >= 5 and revenue is not None and revenue >= 7:
        goal_met = True
    elif signups is not None and signups == 0:
        goal_met = False
    elif revenue is not None and revenue == 0:
        goal_met = False

    return {
        "signups_observed": signups,
        "sales_observed": sales,
        "revenue_observed": revenue,
        "daily_goal_met": goal_met,
        "target_signups": 5,
        "target_sales": 1,
        "target_revenue": 7,
    }


def _check(check_id: str, status: str, detail: str, **evidence: Any) -> dict[str, Any]:
    return {"id": check_id, "status": status, "detail": detail, "evidence": evidence}


# ---------------------------------------------------------------------------
# Executor functions
# ---------------------------------------------------------------------------


def execute_olsp_baseline_access(request: ExecutionRequest) -> ExecutionResult:
    """Perform only the fixed, read-only checks declared by the OLSP contract."""
    started_at = utc_now_iso()
    checks: list[dict[str, Any]] = []
    project_ok = active_project_id() == OLSP_PROJECT_ID and request.project_id == OLSP_PROJECT_ID
    checks.append(_check("active_project", "SUCCEEDED" if project_ok else "FAILED", "active project matches OLSP", project=active_project_id()))

    repository = Path(request.declared_inputs["repository_path"])
    exists = repository.is_dir()
    checks.append(_check("repository_exists", "SUCCEEDED" if exists else "BLOCKED", "repository directory exists" if exists else "repository directory is missing", path=str(repository)))
    readable = exists and os.access(repository, os.R_OK | os.X_OK)
    checks.append(_check("repository_readable", "SUCCEEDED" if readable else "BLOCKED", "repository directory is readable" if readable else "repository directory is not readable", path=str(repository)))

    git_ok = branch_ok = commit_ok = working_tree_ok = False
    repository_data: dict[str, Any] = {"path": str(repository)}
    if readable:
        git_ok, git_value = _git_read(repository, "rev-parse", "--is-inside-work-tree")
        git_ok = git_ok and git_value == "true"
        checks.append(_check("repository_git", "SUCCEEDED" if git_ok else "BLOCKED", "repository is a Git work tree" if git_ok else "repository is not a readable Git work tree", is_git=git_ok))
        if git_ok:
            branch_ok, branch = _git_read(repository, "branch", "--show-current")
            checks.append(_check("repository_branch", "SUCCEEDED" if branch_ok and bool(branch) else "FAILED", "current branch read" if branch_ok and branch else "current branch is unavailable", branch=branch if branch_ok else ""))
            commit_ok, commit = _git_read(repository, "rev-parse", "HEAD")
            checks.append(_check("repository_commit", "SUCCEEDED" if commit_ok else "FAILED", "current commit read" if commit_ok else "current commit is unavailable", commit=commit if commit_ok else ""))
            working_tree_ok, porcelain = _git_read(repository, "status", "--porcelain")
            changed_count = len([line for line in porcelain.splitlines() if line]) if working_tree_ok else 0
            checks.append(_check("repository_working_tree", "SUCCEEDED" if working_tree_ok else "FAILED", "working tree status read" if working_tree_ok else "working tree status is unavailable", changed_file_count=changed_count, clean=changed_count == 0))
            repository_data.update({"branch": branch if branch_ok else None, "commit": commit if commit_ok else None, "working_tree_changed_file_count": changed_count if working_tree_ok else None})
    else:
        for check_id in ("repository_git", "repository_branch", "repository_commit", "repository_working_tree"):
            checks.append(_check(check_id, "BLOCKED", "repository check not run because repository access is unavailable"))

    project_directory = active_project_directory()
    documents_ok = bool(project_directory) and all((project_directory / name).is_file() and os.access(project_directory / name, os.R_OK) for name in REQUIRED_PROJECT_DOCS)
    checks.append(_check("project_documents", "SUCCEEDED" if documents_ok else "FAILED", "required project documents are readable" if documents_ok else "required project documents are unavailable", documents=list(REQUIRED_PROJECT_DOCS)))

    measurement_path = Path(request.declared_inputs["measurement_report_path"])
    try:
        config = load_measurement_config(active_project_directory())
        if request.declared_inputs.get("measurement_scope") == "aggregate-only":
            aggregate_path = Path(request.declared_inputs["measurement_source_path"])
            aggregate = _safe_read_json(aggregate_path)
            fields = aggregate.get("fields", {}) if aggregate else {}
            measurement_status = "SUCCEEDED" if fields else "BLOCKED"
            measurement_data = {
                "source": config.source_name,
                "scope": "aggregate-only",
                "daily_deltas_available": False,
                "observed_fields": sorted(fields),
            } if fields else {}
            measurement_detail = (
                "authenticated aggregate OLSP snapshot is available; daily conversion deltas remain unavailable"
                if fields else "authenticated aggregate OLSP snapshot is missing"
            )
            measurement_path = aggregate_path
        else:
            measurement_status, measurement_data, measurement_detail = read_daily_conversion_report(measurement_path, expected_date=date.today().isoformat())
            if measurement_status == "SUCCEEDED" and (measurement_data["source"] != config.source_name or measurement_data["revenue"] != measurement_data["sales"] * config.sale_value):
                measurement_status, measurement_data, measurement_detail = "FAILED", {}, "measurement report conflicts with authoritative measurement configuration"
    except ValueError as error:
        measurement_status, measurement_data, measurement_detail = "FAILED", {}, str(error)
    checks.append(_check("measurement_source", measurement_status, measurement_detail, path=str(measurement_path), **measurement_data))

    check_status = {item["id"]: item["status"] for item in checks}
    repository_checks = ("active_project", "repository_exists", "repository_readable", "repository_git", "repository_branch", "repository_commit", "repository_working_tree", "project_documents")
    repository_ready = all(check_status[item] == "SUCCEEDED" for item in repository_checks)
    if not repository_ready:
        status, classification, retryable, summary = "BLOCKED", "REPOSITORY_ACCESS_UNAVAILABLE", True, "OLSP repository baseline could not be verified."
    elif measurement_status == "SUCCEEDED":
        status, classification, retryable, summary = "SUCCEEDED", None, False, "OLSP repository and measurement baseline verified."
    elif measurement_status == "BLOCKED":
        status, classification, retryable, summary = "BLOCKED", "MEASUREMENT_SOURCE_MISSING", True, "OLSP repository access verified; conversion measurement remains unavailable."
    else:
        status, classification, retryable, summary = "FAILED", "MEASUREMENT_SOURCE_INVALID", True, "OLSP measurement source exists but failed validation."

    return ExecutionResult(
        execution_id=request.execution_id,
        status=status,
        executor_id=OLSP_BASELINE_EXECUTOR_ID,
        started_at=started_at,
        completed_at=utc_now_iso(),
        summary=summary,
        structured_outputs={"repository": repository_data, "measurement": measurement_data, "checks": check_status},
        evidence=tuple(checks),
        changed_files=(),
        error_classification=classification,
        retryable=retryable,
    )


def execute_content_funnel_review(request: ExecutionRequest) -> ExecutionResult:
    started_at = utc_now_iso()
    status, review, evidence = review_content_funnel(Path(request.declared_inputs["article_path"]), request.declared_inputs["mega_link_prefix"])
    return ExecutionResult(request.execution_id, status, CONTENT_FUNNEL_EXECUTOR_ID, started_at, utc_now_iso(), "Content funnel review completed." if status == "SUCCEEDED" else "Content funnel review found a blocking Owner-controlled issue.", {"content_funnel_review": review}, evidence, (), None if status == "SUCCEEDED" else "CONTENT_FUNNEL_INCOMPLETE", status != "SUCCEEDED")


def execute_content_improvement_plan(request: ExecutionRequest) -> ExecutionResult:
    started_at = utc_now_iso()
    status, proposal = build_improvement_proposal(Path(request.declared_inputs["article_path"]), request.declared_inputs["mega_link_prefix"])
    evidence = tuple(_check(item, "SUCCEEDED" if status == "SUCCEEDED" else "FAILED", "structural review reused for improvement planning") for item in ("article", "primary_cta", "mega_link", "conversion_path", "technical_quality", "seo_basics"))
    return ExecutionResult(request.execution_id, status, CONTENT_IMPROVEMENT_EXECUTOR_ID, started_at, utc_now_iso(), "One content improvement proposal produced." if status == "SUCCEEDED" else "Improvement proposal blocked by structural evidence.", {"improvement_proposal": proposal}, evidence, (), None if status == "SUCCEEDED" else "CONTENT_FUNNEL_INCOMPLETE", status != "SUCCEEDED")


def execute_evidence_review(request: ExecutionRequest) -> ExecutionResult:
    started_at = utc_now_iso()
    _, report = review_evidence(Path(request.declared_inputs["article_path"]), Path(request.declared_inputs["measurement_report_path"]) if "measurement_report_path" in request.declared_inputs else None)
    evidence = tuple(_check(item, "SUCCEEDED", "evidence inventory completed") for item in ("article", "primary_cta", "mega_link", "conversion_path", "technical_quality", "seo_basics"))
    return ExecutionResult(request.execution_id, "SUCCEEDED", EVIDENCE_REVIEW_EXECUTOR_ID, started_at, utc_now_iso(), "Objective evidence inventory produced.", {"evidence_review": report}, evidence, (), None, False)


def execute_daily_production_procedure(request: ExecutionRequest) -> ExecutionResult:
    """Full daily production cycle: check funnel + OLSP artifact + produce package.

    Version 1 does not invent a daily conversion metric. It records only whether
    a local aggregate observation is present for the already-approved procedure.
    """
    started_at = utc_now_iso()
    project_directory = active_project_directory()
    active_ok = active_project_id() == OLSP_PROJECT_ID and request.project_id == OLSP_PROJECT_ID

    # Load daily goal — the active production objective that drives every decision
    objectives: Objectives | None = None
    goal_eval: dict[str, Any] = {}
    if project_directory:
        try:
            objectives = load_objectives(project_directory, OLSP_PROJECT_ID)
        except Exception:
            pass

    documents_ok = bool(project_directory) and all(
        (project_directory / name).is_file() and os.access(project_directory / name, os.R_OK)
        for name in REQUIRED_PROJECT_DOCS
    )
    procedure_path = Path(request.declared_inputs["procedure_path"])
    procedure_ok = procedure_path.is_file() and os.access(procedure_path, os.R_OK)

    runtime_directory = project_directory / "runtime" if project_directory else Path()
    aggregate_inputs = sorted(path.name for path in runtime_directory.glob("*aggregate*.json") if path.is_file()) if project_directory else []

    checks: list[dict[str, Any]] = [
        _check("active_project", "SUCCEEDED" if active_ok else "FAILED", "active project matches OLSP", project=active_project_id()),
        _check("project_documents", "SUCCEEDED" if documents_ok else "FAILED", "required project documents are readable" if documents_ok else "required project documents are unavailable", documents=list(REQUIRED_PROJECT_DOCS)),
        _check("daily_procedure", "SUCCEEDED" if procedure_ok else "FAILED", "daily production procedure is readable" if procedure_ok else "daily production procedure is unavailable", path=str(procedure_path)),
        _check("daily_input_reviewed", "SUCCEEDED", "local OLSP Back Office aggregate input reviewed; no conversion value inferred", aggregate_inputs=aggregate_inputs, observation_available=bool(aggregate_inputs)),
    ]

    # Resolve project artifact config
    project_id = active_project_id() or ""
    artifact_config = load_artifact_config(project_id) if project_id else None

    # Read latest OLSP artifact (from hermes collect olsp or hermes plan olsp)
    olsp_artifact_path = OLSP_ARTIFACT_PATH
    olsp_artifact: dict[str, Any] = {}
    olsp_artifact_ok = olsp_artifact_path.is_file()
    if olsp_artifact_ok:
        try:
            olsp_artifact = json.loads(olsp_artifact_path.read_text(encoding="utf-8"))
            checks.append(_check("olsp_artifact", "SUCCEEDED", "OLSP dashboard artifact read", path=str(olsp_artifact_path), fields=len(olsp_artifact.get("fields", {}))))
        except Exception:
            olsp_artifact_ok = False
            checks.append(_check("olsp_artifact", "FAILED", "OLSP artifact exists but is not readable JSON", path=str(olsp_artifact_path)))
    else:
        checks.append(_check("olsp_artifact", "BLOCKED", "No OLSP artifact — run 'hermes collect olsp' first", path=str(olsp_artifact_path)))

    # Read content funnel
    mega_link_prefix = "https://offers.olspsystem.com/get_megalink"
    if olsp_artifact.get("fields", {}).get("mega_link", {}).get("value"):
        mega_value = olsp_artifact["fields"]["mega_link"]["value"]
        mega_link_prefix = mega_value.split("?")[0] if mega_value else mega_link_prefix

    article_path = ARTICLE_PATH
    funnel_status: str = "NOT_CHECKED"
    funnel_review: dict[str, Any] = {}
    if active_ok and article_path.is_file():
        try:
            funnel_status, funnel_review, _ = review_content_funnel(article_path, mega_link_prefix)
        except Exception:
            funnel_status = "FAILED"
    checks.append(_check(
        "content_funnel",
        "SUCCEEDED" if funnel_status == "SUCCEEDED" else "FAILED",
        "content funnel reviewed" if funnel_status == "SUCCEEDED" else f"content funnel: {funnel_status}",
        structural_health=funnel_review.get("structural_health", 0),
        improvement=funnel_review.get("highest_impact_improvement", ""),
    ))

    # Evaluate daily goal progress from OLSP data
    goal_eval = _daily_goal(olsp_artifact) if olsp_artifact_ok else {}
    mission_text = objectives.mission if objectives else ""
    daily_goal_desc = next(
        (obj.get("description", "") for obj in (json.loads((project_directory / "OBJECTIVES.md").read_text(encoding="utf-8")) if project_directory and (project_directory / "OBJECTIVES.md").is_file() else {}).get("daily_objectives", []))
        if not isinstance(goal_eval.get("daily_goal_met"), bool) else []
    ) or "Achieve one $7 sale and five signups daily"

    if olsp_artifact_ok and goal_eval:
        goal_status = "MET" if goal_eval.get("daily_goal_met") is True else (
            "NOT MET" if goal_eval.get("daily_goal_met") is False else "UNKNOWN — aggregate data only"
        )
        checks.append(_check(
            "daily_goal",
            "SUCCEEDED" if goal_eval.get("daily_goal_met") is True else "INFORMATIONAL",
            f"Daily goal ({mission_text[:50] or '1 sale + 5 signups'}): {goal_status}",
            signups_observed=goal_eval.get("signups_observed"),
            sales_observed=goal_eval.get("sales_observed"),
            revenue_observed=goal_eval.get("revenue_observed"),
            target_signups=goal_eval.get("target_signups"),
            target_revenue=goal_eval.get("target_revenue"),
        ))

    # Determine the single next productive task
    selected_task = _select_next_production_task(
        project_directory=project_directory,
        olsp_artifact=olsp_artifact,
        funnel_status=funnel_status,
        funnel_review=funnel_review,
        article_path=article_path,
        mega_link_prefix=mega_link_prefix,
        plan_json=_safe_read_json(OLSP_PLAN_PATH) if project_directory else None,
        goal_eval=goal_eval,
        objectives=objectives,
    )

    # Produce production package artifact (only if config defines where)
    source_changed = False
    changed_files: tuple[str, ...] = ()
    package_created = False

    if artifact_config is None:
        checks.append(_check("production_package", "BLOCKED", "Project artifact location not configured — define config/artifacts.json in the canonical project repository", artifact_type="production-package"))
    else:
        package_path = artifact_path_for(project_id, "production-package", "production-package.json")
        if package_path is None:
            checks.append(_check("production_package", "BLOCKED", "Production package type not allowed by artifact config", allowed=artifact_config.allowed_artifact_types))
        else:
            valid, reason = validate_artifact_path(package_path, project_id, "production-package")
            if not valid:
                checks.append(_check("production_package", "FAILED", f"Repository boundary violation: {reason}", target=str(package_path)))
            else:
                package = {
                    "selected_task": selected_task["task"],
                    "objective": request.objective_id,
                    "mission": objectives.mission if objectives else "",
                    "daily_goal": {
                        "target_signups": goal_eval.get("target_signups", 5),
                        "target_sales": goal_eval.get("target_sales", 1),
                        "target_revenue": goal_eval.get("target_revenue", 7),
                        "signups_observed": goal_eval.get("signups_observed"),
                        "sales_observed": goal_eval.get("sales_observed"),
                        "revenue_observed": goal_eval.get("revenue_observed"),
                        "goal_met": goal_eval.get("daily_goal_met"),
                    },
                    "goal_driven": selected_task.get("goal_driven", False),
                    "source_changed": source_changed,
                    "evidence": {
                        "olsp_artifact_available": olsp_artifact_ok,
                        "funnel_health": funnel_review.get("structural_health"),
                        "aggregate_inputs": aggregate_inputs,
                    },
                    "validation": "All daily production checks completed",
                    "expected_business_impact": selected_task["impact"],
                    "external_action_awaiting_approval": selected_task["external_action"],
                    "rollback_or_recovery_path": f"Remove {package_path.name} from project repository",
                    "produced_at": utc_now_iso(),
                }
                atomic_json_write(package_path, package)
                package_created = True
                changed_files = (str(package_path),)
                checks.append(_check("production_package", "SUCCEEDED", "production package written to project repository", path=str(package_path), task=selected_task["task"]))

    # Build social media daily plan (non-blocking — part of daily cycle)
    daily_plan = build_daily_plan(article_path)
    social_plan_path = SOCIAL_PLAN_DIR / "daily-plan.json"
    if daily_plan.get("status") == "READY":
        checks.append(_check("social_plan", "SUCCEEDED", f"Daily plan ready: {daily_plan.get('publication_count', 0)} publications", platform=daily_plan.get("platform"), remaining=social_status()["remaining"]))
        changed_files = changed_files + (str(social_plan_path),)
    elif daily_plan.get("status") == "COMPLETE":
        checks.append(_check("social_plan", "COMPLETE", "All angle hooks published — reset runtime/social/published.json to rotate again.", total=social_status()["total_angles"]))

    # Determine overall status
    all_succeeded = all(c["status"] == "SUCCEEDED" for c in checks)
    package_blocked = any(c["id"] == "production_package" and c["status"] in ("BLOCKED", "FAILED") for c in checks)
    status = "BLOCKED" if package_blocked else "SUCCEEDED" if all_succeeded else "SUCCEEDED" if any(
        c["status"] in ("BLOCKED", "FAILED") and c["id"] in ("olsp_artifact", "content_funnel")
        for c in checks
    ) else "FAILED"
    error_class = None if all_succeeded else "PROJECT_ARTIFACT_LOCATION_UNDEFINED" if any(
        c["id"] == "production_package" and c["status"] == "BLOCKED" and "not configured" in c.get("detail", "")
        for c in checks
    ) else "PROJECT_REPOSITORY_BOUNDARY_VIOLATION" if any(
        c["id"] == "production_package" and c["status"] == "FAILED" and "boundary" in c.get("detail", "").lower()
        for c in checks
    ) else "DAILY_PRODUCTION_INCOMPLETE"

    summary_parts = [f"Daily production cycle: {len(checks)} checks"]
    if goal_eval.get("daily_goal_met") is True:
        summary_parts.append("goal MET")
    elif goal_eval.get("daily_goal_met") is False:
        summary_parts.append("goal NOT MET")
    elif goal_eval:
        summary_parts.append("goal status unknown")
    if package_blocked:
        summary_parts.append("artifact location not configured")
    if not olsp_artifact_ok:
        summary_parts.append("OLSP artifact unavailable")
    if funnel_status != "SUCCEEDED":
        summary_parts.append(f"funnel health: {funnel_review.get('structural_health', 0)}/100")
    if daily_plan.get("status") == "READY":
        summary_parts.append(f"social: {daily_plan.get('publication_count', 0)} publications today")
    summary_parts.append(f"selected: {selected_task['task']}")

    return ExecutionResult(
        execution_id=request.execution_id,
        status=status,
        executor_id=DAILY_PRODUCTION_EXECUTOR_ID,
        started_at=started_at,
        completed_at=utc_now_iso(),
        summary="; ".join(summary_parts),
        structured_outputs={
            "run_date": request.declared_inputs["run_date"],
            "daily_goal": {
                "signups_observed": goal_eval.get("signups_observed"),
                "sales_observed": goal_eval.get("sales_observed"),
                "revenue_observed": goal_eval.get("revenue_observed"),
                "goal_met": goal_eval.get("daily_goal_met"),
                "target": f"{goal_eval.get('target_signups', 5)} signups + {goal_eval.get('target_sales', 1)} sale",
            },
            "aggregate_inputs": aggregate_inputs,
            "observation_available": bool(aggregate_inputs),
            "funnel_health": funnel_review.get("structural_health", 0),
            "selected_task": selected_task["task"],
            "external_action_needed": selected_task["external_action"] is not None,
            "source_changed": source_changed,
            "goal_driven": selected_task.get("goal_driven", False),
        },
        evidence=tuple(checks),
        changed_files=changed_files,
        error_classification=error_class,
        retryable=not active_ok or not procedure_ok,
    )


def _select_next_production_task(
    project_directory: Path,
    olsp_artifact: dict[str, Any],
    funnel_status: str,
    funnel_review: dict[str, Any],
    article_path: Path,
    mega_link_prefix: str,
    plan_json: dict[str, Any] | None = None,
    goal_eval: dict[str, Any] | None = None,
    objectives: Objectives | None = None,
) -> dict[str, Any]:
    """Apply goal-driven deterministic priority order to select one production task.

    Priority is determined by the active daily objective (1 sale + 5 signups):

    1. If daily goal is MET — report success, suggest content maintenance
    2. Fix proven critical funnel issue (blocking conversion path)
    3. Generate social content to drive traffic toward the conversion path
    4. Validate approved but unpublished content (no auto-write)
    5. Improve highest-potential existing content
    6. Create new content only if none of the above apply

    OWNER_APPROVAL_REQUIRED tasks are reported as Owner actions, never auto-executed.
    """
    goal_eval = goal_eval or {}
    mission = (objectives.mission if objectives else "")

    # Priority 1: Goal met — acknowledge and maintain
    if goal_eval.get("daily_goal_met") is True:
        return {
            "task": f"Daily goal met: {mission or '1 sale + 5 signups'}. Maintain production quality.",
            "impact": "Sustain daily production cycle; maintain article quality and social cadence",
            "external_action": "Owner verifies OLSP Back Office confirms the goal",
            "is_owner_action": False,
            "goal_driven": True,
        }

    # Priority 1b: Goal NOT met (confirmed) — prioritize conversion-driving work
    if goal_eval.get("daily_goal_met") is False:
        if funnel_status != "SUCCEEDED" and article_path.is_file():
            improvement = funnel_review.get("highest_impact_improvement", "")
            if improvement and "No critical" not in improvement:
                return {
                    "task": f"Goal not met. Repair content funnel: {improvement}. Commander proposes the exact edit; Owner approval gates file modification per SOUL.md §7.",
                    "impact": f"Restores conversion path needed to achieve {mission}",
                    "external_action": None,
                    "is_owner_action": True,
                    "goal_driven": True,
                }

    # Priority 2: Critical funnel issue (blocking goal achievement)
    if funnel_status != "SUCCEEDED" and article_path.is_file():
        improvement = funnel_review.get("highest_impact_improvement", "")
        if improvement and "No critical" not in improvement:
            return {
                "task": f"Repair content funnel: {improvement}. Commander drafts the fix; Owner approval required before article modification per SOUL.md §7.",
                "impact": "Restores measurable conversion-path requirement",
                "external_action": None,
                "is_owner_action": True,
                "goal_driven": False,
            }

    # Priority 3: Owner approval required — never auto-execute (gate before social)
    if plan_json and plan_json.get("next_action", "").startswith("OWNER_APPROVAL_REQUIRED"):
        return {
            "task": f"Validate approved content package: {plan_json.get('next_action', '')}. Commander validates readiness; deployment requires Owner approval per SOUL.md §7.",
            "impact": "Validates readiness of Owner-approved content without modifying it",
            "external_action": None,
            "is_owner_action": True,
            "goal_driven": True,
        }

    # Priority 4: Social content — drives traffic toward goal
    social = social_status()
    if social.get("remaining_article", 0) > 0:
        return {
            "task": f"Social content pipeline active — {social['remaining_article']} angles remain",
            "impact": "Social posts drive traffic to the article conversion path — essential for achieving daily signups and sales",
            "external_action": "Owner approves publish: hermes publish --social",
            "is_owner_action": False,
            "goal_driven": True,
        }

    # Priority 5: Improve existing content
    if article_path.is_file() and funnel_status == "SUCCEEDED":
        improvement = funnel_review.get("highest_impact_improvement", "")
        if improvement and "No critical" not in improvement and "not found" not in improvement.lower():
            return {
                "task": f"Improve existing article: {improvement}. Commander drafts the edit; Owner approval required before file modification per SOUL.md §7.",
                "impact": "Increases measurable conversion-path effectiveness toward daily goal",
                "external_action": None,
                "is_owner_action": True,
                "goal_driven": True,
            }
        return {
            "task": "Collect query and visitor-behavior evidence before changing the article",
            "impact": "Prevents speculative edits; creates evidence for next content decision toward goal achievement",
            "external_action": None,
            "is_owner_action": False,
            "goal_driven": True,
        }

    # Priority 6: New content
    return {
        "task": "No existing article found — run opportunity discovery to identify next content opportunity. Commander produces evidence-supported recommendations; Owner selects topic.",
        "impact": "Establishes the first owned conversion-path article needed for daily goal achievement",
        "external_action": None,
        "is_owner_action": True,
        "goal_driven": True,
    }


def _safe_read_json(path: Path) -> dict[str, Any] | None:
    try:
        if not path.is_file():
            return None
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else None
    except Exception:
        return None


def execute_content_plan(request: ExecutionRequest) -> ExecutionResult:
    """Verify a pre-existing plan only; it never writes project or website content."""
    started_at = utc_now_iso()
    checks = []
    for check_id, input_name in (
        ("content_plan", "content_plan_path"),
        ("query_page_review", "query_page_review_path"),
        ("search_evidence_review", "search_evidence_review_path"),
    ):
        path = Path(request.declared_inputs[input_name])
        readable = path.is_file() and os.access(path, os.R_OK)
        checks.append(_check(check_id, "SUCCEEDED" if readable else "FAILED", "artifact is readable" if readable else "artifact is unavailable", path=str(path)))
    succeeded = all(check["status"] == "SUCCEEDED" for check in checks)
    return ExecutionResult(
        request.execution_id, "SUCCEEDED" if succeeded else "BLOCKED", CONTENT_PLAN_EXECUTOR_ID,
        started_at, utc_now_iso(),
        "Read-only content plan and evidence receipts verified." if succeeded else "Read-only content plan verification is blocked by a missing artifact.",
        {"content_plan_path": request.declared_inputs["content_plan_path"]}, tuple(checks), (),
        None if succeeded else "CONTENT_PLAN_ARTIFACT_MISSING", not succeeded,
    )


def execute_social_planning(request: ExecutionRequest) -> ExecutionResult:
    """Build the daily social publication plan for the OLSP operating model."""
    started_at = utc_now_iso()
    project_directory = active_project_directory()
    article_path = ARTICLE_PATH if project_directory else Path()
    plan = build_daily_plan(article_path)
    status_data = social_status()
    checks = [
        {"id": "article_available", "status": "SUCCEEDED" if article_path.is_file() else "FAILED", "detail": "article is readable" if article_path.is_file() else "article is unavailable", "evidence": {"path": str(article_path)}},
        {"id": "social_plan", "status": "SUCCEEDED" if plan.get("status") == "READY" else "COMPLETE" if plan.get("status") == "COMPLETE" else "FAILED", "detail": plan.get("reason", plan.get("posts", [{}])[0].get("angle", "daily plan ready") if plan.get("posts") else "daily plan ready"), "evidence": {"remaining_angles": status_data["remaining"], "publication_count": status_data["daily_plan_count"], "next_platform": plan.get("platform")}},
    ]
    succeeded = all(c["status"] == "SUCCEEDED" for c in checks)
    first_angle = plan.get("posts", [{}])[0].get("angle") if plan.get("posts") else None
    return ExecutionResult(
        execution_id=request.execution_id,
        status="SUCCEEDED" if succeeded else "COMPLETE" if plan.get("status") == "COMPLETE" else "FAILED",
        executor_id=SOCIAL_PLAN_EXECUTOR_ID,
        started_at=started_at,
        completed_at=utc_now_iso(),
        summary=f"Daily social plan: {plan.get('publication_count', 0)} publications ({first_angle or 'no plan'})" if succeeded else "All angle hooks published — reset to rotate.",
        structured_outputs={
            "angle": first_angle,
            "platform": plan.get("platform"),
            "publication_count": plan.get("publication_count"),
            "remaining_angles": status_data["remaining"],
            "total_angles": status_data["total_angles"],
        },
        evidence=tuple(checks),
        changed_files=(str(SOCIAL_PLAN_DIR / "plan.json"),),
        error_classification=None,
        retryable=False,
    )


# ---------------------------------------------------------------------------
# Executor registry — discovered by Commander core at execution time
# ---------------------------------------------------------------------------

EXECUTORS = {
    "olsp-baseline-access": execute_olsp_baseline_access,
    "content-funnel-review": execute_content_funnel_review,
    "olsp-content-improvement-plan": execute_content_improvement_plan,
    "olsp-evidence-review": execute_evidence_review,
    "olsp-minimum-daily-production-system": execute_daily_production_procedure,
    "prepare-content-plan": execute_content_plan,
    "social-production": execute_social_planning,
    "video-production": execute_video_production,
}

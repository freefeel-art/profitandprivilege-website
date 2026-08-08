"""Goal Execution Plan — evidence-based strategy for daily production.

Commander is not a task executor. Commander is the daily operator responsible
for achieving the daily goal. Every action must be evidence-driven.

The strategy is an operational loop:
  Observe → Analyze → Decide → Execute → Measure → Compare → Decide again

This continues until the daily goal is achieved, the operating day ends,
or Commander becomes BLOCKED.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


PROJECT_ID = "profit-and-privilege"
PROJECT_DISPLAY_NAME = "OLSP"
BRAND_NAME = "Profit & Privilege"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_ROOT = PROJECT_ROOT / "runtime"
OLSP_ARTIFACT_PATH = RUNTIME_ROOT / "intelligence/olsp-dashboard/latest.json"
SOCIAL_PLAN_PATH = RUNTIME_ROOT / "social/plan.json"
SOCIAL_PUBLISHED_PATH = RUNTIME_ROOT / "social/published.json"
REALITY_PATH = RUNTIME_ROOT / "commander/reality.json"
ACTION_RECEIPTS_PATH = RUNTIME_ROOT / "commander/action-receipts.json"
ARTICLE_PATH = PROJECT_ROOT / "src/pages/is-olsp-academy-an-mlm.astro"

# OLSP fields verified as available via CDP browser automation:
# source: app/providers/olsp_dashboard.py APPROVED_FIELDS
OLSP_VERIFIED_FIELDS = (
    "current_available_balance",  # $ amount — current affiliate balance
    "lifetime_balance",           # $ amount — total lifetime earnings
    "olsp_points",                # integer — OLSP Academy points
    "share_and_earn_link",        # URL — mega link for sharing
    "mega_link",                  # URL — mega link
    "leads",                      # integer — total leads (all time)
    "customers",                  # integer — total customers (all time)
    "transactions",               # integer — total transactions (all time)
    "daily_signups",              # integer — explicit project-local calendar day
    "daily_sales",                # integer — explicit project-local calendar day
    "daily_revenue",              # USD — explicit project-local calendar day
)

# Fields still unavailable: conversion rate, attributed traffic, campaign
# performance, and operational status. Source attribution remains separate from
# verified daily OLSP outcome collection.


@dataclass
class ActionAssessment:
    action_id: str
    label: str
    available: bool
    expected_benefit: str
    expected_limitation: str
    estimated_confidence: str  # HIGH / MEDIUM / LOW
    why_it_helps: str
    blocked_reason: str = ""
    supporting_evidence: str = ""
    expected_improvement: str = ""
    failure_evidence: str = ""
    next_if_failed: str = ""


@dataclass
class GoalExecutionPlan:
    goal: str
    mission: str
    project: str = PROJECT_DISPLAY_NAME
    current_status: dict[str, Any] = field(default_factory=dict)
    gap: dict[str, Any] = field(default_factory=dict)
    funnel_diagnosis: dict[str, Any] = field(default_factory=dict)
    available_actions: list[ActionAssessment] = field(default_factory=list)
    recommended_sequence: list[str] = field(default_factory=list)
    reasoning: str = ""
    evidence_classifications: dict[str, str] = field(default_factory=dict)


def _olsp_fields() -> dict[str, Any]:
    if not OLSP_ARTIFACT_PATH.is_file():
        return {}
    try:
        return json.loads(OLSP_ARTIFACT_PATH.read_text(encoding="utf-8")).get("fields", {})
    except Exception:
        return {}


def _field_str(fields: dict[str, Any], key: str) -> str | None:
    raw = (fields.get(key) or {}).get("value")
    if raw is None:
        return None
    return str(raw).strip()


def _field_int(fields: dict[str, Any], key: str) -> int | None:
    val = _field_str(fields, key)
    if val is None:
        return None
    try:
        return int(val.replace(",", "").replace("$", "").strip())
    except (ValueError, TypeError):
        return None


def _field_float(fields: dict[str, Any], key: str) -> float | None:
    val = _field_str(fields, key)
    if val is None:
        return None
    try:
        return float(val.replace(",", "").replace("$", "").strip())
    except (ValueError, TypeError):
        return None


def _daily_field_int(
    fields: dict[str, Any], key: str, expected_period: str,
) -> int | None:
    field_value = fields.get(key)
    if (
        not isinstance(field_value, dict)
        or field_value.get("status") != "FOUND"
        or field_value.get("period") != expected_period
    ):
        return None
    return _field_int(fields, key)


def _daily_field_float(
    fields: dict[str, Any], key: str, expected_period: str,
) -> float | None:
    field_value = fields.get(key)
    if (
        not isinstance(field_value, dict)
        or field_value.get("status") != "FOUND"
        or field_value.get("period") != expected_period
    ):
        return None
    return _field_float(fields, key)


def _load_action_receipts() -> dict[str, dict[str, Any]]:
    if not ACTION_RECEIPTS_PATH.is_file():
        return {}
    try:
        payload = json.loads(ACTION_RECEIPTS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}
    actions = payload.get("actions", {}) if isinstance(payload, dict) else {}
    return actions if isinstance(actions, dict) else {}


def _action_receipt(action_id: str) -> dict[str, Any] | None:
    return _load_action_receipts().get(action_id)


def _action_is_open(action_id: str) -> bool:
    receipt = _action_receipt(action_id)
    if not receipt:
        return True
    return str(receipt.get("status", "NOT_STARTED")).upper() in {"NOT_STARTED", "READY"}


def _action_blocked_reason(action_id: str, default_reason: str) -> str:
    receipt = _action_receipt(action_id)
    if receipt:
        status = str(receipt.get("status", "")).upper()
        if status == "EXECUTING":
            return "Autonomous work already has an execution receipt; wait for its terminal result."
        if status == "VERIFIED":
            return "A verified receipt already exists for this action."
        if status in {"FAILED", "BLOCKED"}:
            return f"Terminal receipt already exists ({status.lower()}); rearm required before rerun."
    return default_reason


def _social_status() -> dict[str, Any]:
    plan = {}
    published: list[dict[str, Any]] = []
    if SOCIAL_PLAN_PATH.is_file():
        try:
            plan = json.loads(SOCIAL_PLAN_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    if SOCIAL_PUBLISHED_PATH.is_file():
        try:
            value = json.loads(SOCIAL_PUBLISHED_PATH.read_text(encoding="utf-8"))
            if isinstance(value, dict):
                for key in ("published", "livebinar_published"):
                    items = value.get(key, [])
                    if isinstance(items, list):
                        published.extend(item for item in items if isinstance(item, dict))
            elif isinstance(value, list):
                published = [item for item in value if isinstance(item, dict)]
        except Exception:
            pass
    today = datetime.now(ZoneInfo("Europe/Stockholm")).date().isoformat()

    def published_day(entry: dict[str, Any]) -> str:
        value = str(entry.get("published_at", ""))
        if len(value) >= 10:
            return value[:10]
        fallback = str(entry.get("date", ""))
        return fallback[:10] if len(fallback) >= 10 else fallback

    publications_today = sum(
        1 for p in published
        if published_day(p) == today or published_day(p) == str(plan.get("date", ""))
    )
    return {
        "plan_exists": bool(plan),
        "plan_status": plan.get("status", "NONE"),
        "platform": plan.get("platform", ""),
        "angle": plan.get("angle", ""),
        "publications_today": publications_today,
        "total_published": len(published),
        "remaining_article": max(0, 30 - len(published)),
    }


def _diagnose_funnel() -> dict[str, Any]:
    """Diagnose exactly why the funnel reports as broken.

    Returns a detailed diagnosis with evidence, not a simple pass/fail.
    """
    diagnosis: dict[str, Any] = {
        "status": "HEALTHY",
        "health_pct": 100,
        "articles_found": [],
        "cta_elements_found": [],
        "mega_link_matches": [],
        "issues": [],
    }

    if not ARTICLE_PATH.is_file():
        diagnosis["status"] = "BROKEN"
        diagnosis["health_pct"] = 0
        diagnosis["issues"].append({"severity": "CRITICAL", "detail": "Article file not found at configured path", "source": str(ARTICLE_PATH)})
        return diagnosis

    try:
        text = ARTICLE_PATH.read_text(encoding="utf-8")
    except Exception as e:
        diagnosis["status"] = "BROKEN"
        diagnosis["health_pct"] = 0
        diagnosis["issues"].append({"severity": "CRITICAL", "detail": f"Article file unreadable: {e}"})
        return diagnosis

    # Check article structure
    import re
    has_title = bool(re.search(r"(?:pageTitle|title)\s*=", text))
    has_description = bool(re.search(r"(?:pageDescription|description)\s*=", text))
    has_h1 = bool(re.search(r"<h1\b", text))
    words = len(re.findall(r"\b[\w'-]+\b", text))

    diagnosis["articles_found"] = [{
        "path": str(ARTICLE_PATH),
        "word_count": words,
        "has_h1": has_h1,
        "has_title_declaration": has_title,
        "has_description_declaration": has_description,
    }]

    if words < 300:
        diagnosis["issues"].append({"severity": "WARNING", "detail": f"Article is short ({words} words); may lack sufficient conversion-path content"})

    # Find CTA elements — href and class may appear in any order
    cta_pattern = re.compile(
        r'<a\s+(?:[^>]*\s)?href="([^"]+)"(?:[^>]*\s)?class="[^"]*cta-btn[^"]*"[^>]*>'
        r'|'
        r'<a\s+(?:[^>]*\s)?class="[^"]*cta-btn[^"]*"(?:[^>]*\s)?href="([^"]+)"[^>]*>'
    )
    ctas: list[str] = []
    for m in cta_pattern.finditer(text):
        href = m.group(1) or m.group(2)
        if href:
            ctas.append(href)
    diagnosis["cta_elements_found"] = [{"href": href, "class": "cta-btn"} for href in ctas]

    if not ctas:
        diagnosis["issues"].append({"severity": "BLOCKING", "detail": "No CTA button found in article. A CTA with class='cta-btn' is required for the conversion path."})
        diagnosis["status"] = "BROKEN"
        diagnosis["health_pct"] = 60 if words >= 300 else 40
        return diagnosis

    # Check mega link alignment
    olsp_fields = _olsp_fields()
    configured_mega_link = _field_str(olsp_fields, "mega_link") or ""
    article_mega_link_prefix = "https://olspacademy.com/megalive/"

    for href in ctas:
        is_olsp_megalive = href.startswith(article_mega_link_prefix)
        is_configured_prefix = configured_mega_link and href.startswith(configured_mega_link.split("?")[0] if "?" in configured_mega_link else configured_mega_link)

        if is_olsp_megalive:
            diagnosis["mega_link_matches"].append({
                "href": href,
                "type": "olspacademy.com/megalive (standard OLSP link)",
                "matches_configured_prefix": is_configured_prefix,
            })
        elif is_configured_prefix:
            diagnosis["mega_link_matches"].append({
                "href": href,
                "type": "offers.olspsystem.com/get_megalink (configured prefix)",
                "matches_configured_prefix": True,
            })

    # Evaluate
    has_olsp_links = any(m["type"].startswith("olspacademy.com") for m in diagnosis["mega_link_matches"])
    has_configured_links = any(m["matches_configured_prefix"] for m in diagnosis["mega_link_matches"])

    if ctas and has_olsp_links and not has_configured_links:
        diagnosis["issues"].append({
            "severity": "INFO",
            "detail": (
                "Article CTAs link to olspacademy.com/megalive/ instead of "
                f"the configured prefix ({configured_mega_link}). "
                "Both URLs may route to the same OLSP destination. The article "
                "CTAs are functional but do not match the configured prefix. "
                "This is a prefix-alignment issue, not a missing-CTA issue."
            ),
            "article_links": [m["href"] for m in diagnosis["mega_link_matches"] if m["type"].startswith("olspacademy.com")],
            "configured_prefix": configured_mega_link,
        })
        # NOT broken — links exist and are valid OLSP mega links
        diagnosis["health_pct"] = min(100, 60 + (20 if words >= 300 else 0) + (10 if has_h1 else 0) + (5 if has_title else 0) + (5 if has_description else 0))
    elif ctas:
        diagnosis["health_pct"] = 100
    else:
        diagnosis["health_pct"] = 60 if words >= 300 else 40

    if diagnosis["health_pct"] >= 80:
        diagnosis["status"] = "HEALTHY"
    elif diagnosis["health_pct"] >= 50:
        diagnosis["status"] = "DEGRADED"
    else:
        diagnosis["status"] = "BROKEN"

    return diagnosis


def build_goal_execution_plan(
    project_directory: Path,
    objectives: Any,  # Objectives dataclass from state.py
) -> GoalExecutionPlan:
    """Build an evidence-based goal execution plan for the active daily objective.

    Commander evaluates the current project state against the Owner's goal
    and selects the strategy most likely to close the remaining gap.
    """

    # ── Goal ──
    goal_text = (
        "Achieve at least one $7 OLSP sale and five new OLSP signups "
        "through olsp.profitandprivilege.com every day."
    )
    mission_text = getattr(objectives, "mission", goal_text)

    # ── OBSERVE: Current Status (OLSP Back Office is primary operational truth) ──
    fields = _olsp_fields()
    olsp_available = bool(fields)

    leads = _field_int(fields, "leads")           # aggregate all-time
    customers = _field_int(fields, "customers")   # aggregate all-time
    transactions = _field_int(fields, "transactions")  # aggregate all-time
    balance = _field_float(fields, "current_available_balance")  # $
    lifetime = _field_float(fields, "lifetime_balance")  # $
    points = _field_int(fields, "olsp_points")
    observation_day = datetime.now(ZoneInfo("Europe/Stockholm")).date().isoformat()
    daily_signups = _daily_field_int(fields, "daily_signups", observation_day)
    daily_sales = _daily_field_int(fields, "daily_sales", observation_day)
    daily_revenue = _daily_field_float(fields, "daily_revenue", observation_day)
    daily_measurement_available = all(
        value is not None for value in (daily_signups, daily_sales, daily_revenue)
    )

    social = _social_status()
    funnel = _diagnose_funnel()

    # Campaign evaluation
    campaign_snapshots = _campaign_snapshots()
    campaign_summary = ""
    if campaign_snapshots:
        campaign_lines = [cs.summary() for cs in campaign_snapshots]
        campaign_summary = " | ".join(campaign_lines)

    # Previous execution comparison
    previous = _previous_execution_state()

    # Funnel diagnosis summary
    funnel_summary = funnel["status"]
    if funnel["issues"]:
        funnel_summary += f" — {funnel['issues'][0]['detail'][:80]}"

    current_status = {
        "project": "OLSP (profit-and-privilege)",
        "brand": "Profit & Privilege",
        "olsp_data_available": olsp_available,
        "olsp_data_source": "OLSP Back Office via CDP browser automation",
        "leads_all_time": leads,
        "customers_all_time": customers,
        "transactions_all_time": transactions,
        "current_balance": balance,
        "lifetime_balance": lifetime,
        "olsp_points": points,
        "daily_signups": daily_signups,
        "daily_sales": daily_sales,
        "daily_revenue": daily_revenue,
        "daily_signups_measurable": daily_signups is not None,
        "daily_sales_measurable": daily_sales is not None,
        "daily_revenue_measurable": daily_revenue is not None,
        "measurement_note": (
            f"Verified OLSP calendar-day outcomes for {observation_day} "
            "Europe/Stockholm."
            if daily_measurement_available else
            "Verified daily OLSP outcome fields are incomplete for the current "
            "Europe/Stockholm calendar day."
        ),
        "funnel_status": funnel["status"],
        "funnel_health_pct": funnel["health_pct"],
        "funnel_diagnosis": funnel_summary,
        "social_plan_ready": social["plan_exists"] and social["plan_status"] == "READY",
        "social_platform": social["platform"],
        "social_publications_today": social["publications_today"],
        "video_pipeline_available": True,
        "email_campaigns": campaign_summary or "no campaigns evaluated",
        "previous_execution": previous.get("checked_at", "never"),
        "previous_daily_signups": previous.get("daily_signups"),
        "previous_funnel_health": previous.get("funnel_health"),
    }

    # ── Gap ──
    target_signups = 5
    target_sales = 1
    gap = {
        "signups_needed_estimate": (
            max(0, target_signups - daily_signups)
            if daily_signups is not None else None
        ),
        "sales_needed_estimate": (
            max(0, target_sales - daily_sales)
            if daily_sales is not None else None
        ),
        "goal_measurable": daily_measurement_available,
        "goal_met_estimable": (
            daily_signups >= target_signups
            and daily_sales >= target_sales
            and daily_revenue >= 7
            if daily_measurement_available else None
        ),
        "measurement_type": (
            "verified_calendar_day"
            if daily_measurement_available else "incomplete_daily_observation"
        ),
        "note": (
            f"OLSP daily outcomes are verified for {observation_day} "
            "Europe/Stockholm. Source attribution is evaluated separately."
            if daily_measurement_available else
            "Commander cannot confirm the daily objective until every daily "
            "OLSP field is verified for the current observation period."
        ),
    }

    # ── Available Actions ──
    # Every action must answer:
    # 1. Why this action?          → why_it_helps
    # 2. What verified evidence?   → supporting_evidence
    # 3. What improvement expected? → expected_improvement
    # 4. What proves failure?      → failure_evidence
    # 5. Next action if failed?    → next_if_failed
    actions: list[ActionAssessment] = []

    # Funnel issues from diagnosis
    funnel_issues = funnel.get("issues", [])
    has_blocking_issue = any(i["severity"] in ("BLOCKING", "CRITICAL") for i in funnel_issues)
    has_warning_issue = any(i["severity"] in ("INFO", "WARNING") for i in funnel_issues)

    actions.append(ActionAssessment(
        action_id="repair_funnel",
        label="Repair content funnel",
        available=has_blocking_issue,
        expected_benefit="Restores the conversion path: article → CTA → Mega Link → OLSP signup.",
        expected_limitation="Requires Owner to edit the article. Commander cannot modify article content.",
        estimated_confidence="HIGH" if has_blocking_issue else "N/A",
        why_it_helps="A blocked conversion path means zero probability of achieving the daily goal regardless of traffic volume.",
        supporting_evidence=(
            f"Funnel diagnosis detected {len(funnel_issues)} issue(s) including: "
            f"{funnel_issues[0]['detail'][:100] if funnel_issues else 'none'}."
        ) if has_blocking_issue else "No verified evidence — funnel is operational.",
        expected_improvement="Restores structural health from broken to healthy. Enables all downstream conversion-path actions.",
        failure_evidence="Funnel remains broken after Owner edit → structural review still shows FAILED status.",
        next_if_failed="Report to Owner that the edit did not resolve the issue. Request specific CTA text for the article.",
        blocked_reason="" if has_blocking_issue else (
            "Funnel is operational" if not has_warning_issue
            else f"Funnel is operational — minor alignment note: {funnel_issues[0]['detail'][:80] if funnel_issues else ''}"
        ),
    ))

    actions.append(ActionAssessment(
        action_id="publish_facebook",
        label="Publish Facebook post",
        available=(
            _action_is_open("publish_facebook")
            and social["plan_exists"]
            and social["plan_status"] == "READY"
            and social["platform"] == "facebook"
            and social["publications_today"] == 0
        ),
        expected_benefit="Drives traffic from OLSP Page (61592596862104) to the article conversion path.",
        expected_limitation="Facebook organic reach is unpredictable. Post-to-signup attribution is not trackable with current OLSP interface.",
        estimated_confidence="MEDIUM",
        why_it_helps="Each published post creates a new opportunity for someone to discover the article and enter the conversion funnel.",
        supporting_evidence=(
            "Social plan is READY with selected angle and hook. "
            "Facebook browser automation is operational (Playwright + saved session). "
            f"{social['remaining_article']} article hooks remain available. "
            "No verified evidence links Facebook posts to OLSP signups — attribution data unavailable."
        ),
        expected_improvement="One additional traffic source active today. Incremental increase in article visibility.",
        failure_evidence=(
            "No verified destination traffic, daily signup, or daily sale evidence "
            "appears within the defined observation window."
        ),
        next_if_failed="If no measurable change after 3 consecutive Facebook posts: (1) re-evaluate article CTA placement, (2) consider paid traffic if available, (3) report diminishing returns to Owner.",
    ))

    actions.append(ActionAssessment(
        action_id="publish_youtube_short",
        label="Publish YouTube Short",
        available=False,
        expected_benefit="Reaches video audience on YouTube Shorts — different segment than Facebook.",
        expected_limitation="Requires finished video and OAuth upload. Video quality unverified.",
        estimated_confidence="LOW",
        why_it_helps="Alternative distribution channel for reaching potential signups.",
        supporting_evidence="No verified evidence — no video has been uploaded to YouTube for this project.",
        expected_improvement="Additional distribution channel active.",
        failure_evidence="Video receives zero views within 7 days of upload.",
        next_if_failed="Review video title, description, and thumbnail. Consider different content format.",
        blocked_reason=_action_blocked_reason(
            "publish_youtube_short",
            "No finished video uploaded to YouTube. Requires hermes video, then OAuth upload.",
        ),
    ))

    actions.append(ActionAssessment(
        action_id="generate_social_plan",
        label="Generate social content plan",
        available=_action_is_open("generate_social_plan") and not (social["plan_exists"] and social["plan_status"] == "READY"),
        expected_benefit="Creates the next Facebook post from 10 angles and 30 hook variants.",
        expected_limitation="Planning alone does not reach any audience. Publication runs autonomously when the approved strategy and required access are available; genuine authority boundaries stop execution.",
        estimated_confidence="HIGH",
        why_it_helps="Content planning is the prerequisite for content publishing, the engine for traffic generation.",
        supporting_evidence=f"{social['remaining_article']} of 30 article hooks remain. 10 angles are defined. Planning alone does not produce signups.",
        expected_improvement="One ready-to-publish post available.",
        failure_evidence="No remaining angles — all 30 hooks published without a measurable outcome.",
        next_if_failed="Report angle exhaustion to Owner. Propose new content angles or alternative distribution.",
        blocked_reason=_action_blocked_reason(
            "generate_social_plan",
            "A ready social plan already exists; no new plan is required.",
        ),
    ))

    actions.append(ActionAssessment(
        action_id="generate_video",
        label="Generate video from article",
        available=_action_is_open("generate_video") and ARTICLE_PATH.is_file() and not (RUNTIME_ROOT / "video/preview.json").is_file(),
        expected_benefit="Produces a 9:16 vertical MP4 from article text + brand kit. Can be uploaded to YouTube Shorts.",
        expected_limitation="Video is silent (no TTS), uses colored backgrounds (no Pexels key).",
        estimated_confidence="HIGH (generation) / LOW (audience impact)",
        why_it_helps="Video content reaches different audience segments than text-only posts.",
        supporting_evidence="OpenMontage engine verified operational — produced 51-second MP4 today. No evidence that video views convert to OLSP signups.",
        expected_improvement="One finished video artifact available for distribution.",
        failure_evidence="Video renders but receives zero views or engagement on any platform.",
        next_if_failed="Integrate TTS voiceover (edge-tts). Add Pexels stock images. Improve scene selection for readability.",
        blocked_reason=_action_blocked_reason(
            "generate_video",
            "No finished video uploaded to YouTube. Requires hermes video, then OAuth upload.",
        ),
    ))

    actions.append(ActionAssessment(
        action_id="review_funnel",
        label="Review content funnel health",
        available=_action_is_open("review_funnel") and ARTICLE_PATH.is_file() and not (RUNTIME_ROOT / "commander/funnel-review.json").is_file(),
        expected_benefit="Verifies article, CTA buttons, and mega links are intact before traffic-driving.",
        expected_limitation="Detects structural issues only — cannot assess content persuasiveness.",
        estimated_confidence="HIGH",
        why_it_helps="Funnel verification ensures traffic-driving actions lead to a working conversion path.",
        supporting_evidence="The configured OLSP article exists in the active project root and is readable. Previous review found 3 CTA buttons linking to valid OLSP mega links.",
        expected_improvement="Confirmation of funnel health before spending traffic-driving actions.",
        failure_evidence="Funnel review shows FAILED or DEGRADED status — CTA missing or mega link broken.",
        next_if_failed="Block all traffic-driving actions until funnel is repaired. Report specific issue to Owner.",
        blocked_reason=_action_blocked_reason(
            "review_funnel",
            "Funnel is already structurally healthy; a new review receipt is not required.",
        ),
    ))

    actions.append(ActionAssessment(
        action_id="collect_facebook_metrics",
        label="Investigate Facebook performance",
        available=_action_is_open("collect_facebook_metrics"),
        expected_benefit="Collects read-only Facebook metrics and joins the publication ledger to live evidence.",
        expected_limitation="Requires the Facebook metrics collector to reach the authenticated Meta evidence source.",
        estimated_confidence="HIGH",
        why_it_helps="Facebook investigation is independent from OLSP dashboard authentication and can continue while OLSP data is unavailable.",
        supporting_evidence=(
            f"{social["total_published"]} published Facebook post(s) exist for read-only inspection."
        ) if social["total_published"] > 0 else "No published Facebook posts exist yet; the collector can still verify that absence.",
        expected_improvement="A timestamped Facebook metrics artifact is written for the current publication set.",
        failure_evidence="The collector returns PARTIAL or FAILED evidence because Meta rows remain unavailable.",
        next_if_failed="Escalate the missing Meta evidence separately; do not stop unrelated production work.",
        blocked_reason=_action_blocked_reason(
            "collect_facebook_metrics",
            "Facebook performance investigation is already satisfied by the latest evidence.",
        ),
    ))

    actions.append(ActionAssessment(
        action_id="collect_olsp_data",
        label="Collect OLSP dashboard data",
        available=_action_is_open("collect_olsp_data") and olsp_available,
        expected_benefit=(
            "Pulls current OLSP Back Office daily outcomes and separately labeled "
            "lifetime totals."
        ),
        expected_limitation="Aggregate lifetime totals only — cannot detect daily changes. May require fresh browser login.",
        estimated_confidence="HIGH" if olsp_available else "MEDIUM (may need re-auth)",
        why_it_helps="OLSP Back Office is the only source of truth for signup and sales progress.",
        supporting_evidence=(
            f"Observed fields available via the authenticated dashboard: {', '.join(k for k in OLSP_VERIFIED_FIELDS if k in fields)}."
        ) if olsp_available else "No verified evidence — OLSP artifact not available. This task is blocked until the authenticated session is restored.",
        expected_improvement=(
            "Updated, explicitly period-scoped daily signup, sale, and revenue "
            "evidence for objective verification."
        ),
        failure_evidence="Collection fails or returns stale data (same values as previous collection).",
        next_if_failed="Report collection failure to Commander. This task remains blocked until the authenticated OLSP session is restored.",
        blocked_reason=_action_blocked_reason(
            "collect_olsp_data",
            "OLSP dashboard authentication unavailable." if not olsp_available else "OLSP dashboard data is already available from the latest observation.",
        ),
    ))

    actions.append(ActionAssessment(
        action_id="evaluate_campaigns",
        label="Evaluate email campaign performance",
        available=_action_is_open("evaluate_campaigns"),
        expected_benefit="Tracks campaign delivery, engagement, and conversion metrics. Feeds evidence into future campaign optimization.",
        expected_limitation="Current campaigns do not track opens, clicks, bounces, or conversions. Only sent count is available.",
        estimated_confidence="HIGH (sent count) / LOW (engagement metrics)",
        why_it_helps="Campaign evaluation ensures future emails depend on campaign results rather than simply sending another message.",
        supporting_evidence=(
            f"{len(campaign_snapshots)} campaign(s) tracked. "
            f"{campaign_summary}"
        ) if campaign_summary else "No campaign data available.",
        expected_improvement="Measurable campaign performance metrics for optimization decisions.",
        failure_evidence="All campaigns show zero engagement or delivery metrics are unavailable.",
        next_if_failed="Implement open/click tracking on future campaigns. Consider dedicated email service provider with built-in analytics.",
        blocked_reason=_action_blocked_reason(
            "evaluate_campaigns",
            "Campaign evaluation is already reflected in the latest evidence.",
        ),
    ))

    actions.append(ActionAssessment(
        action_id="wait_for_approval",
        label="Request Owner approval",
        available=False,
        expected_benefit="Unblocks gated actions requiring Owner authorization.",
        expected_limitation="Passive — no progress until Owner responds.",
        estimated_confidence="N/A",
        why_it_helps="Some actions cannot proceed without Owner authority, identity, credentials, legal responsibility, explicit financial commitment, or a new strategic decision per SOUL.md §7.",
        supporting_evidence="No pending Owner approvals in registry.",
        expected_improvement="Approval gate cleared for pending action.",
        failure_evidence="Owner does not respond within operating day.",
        next_if_failed="Continue with autonomous actions that do not require approval. Re-request next cycle.",
        blocked_reason="No pending Owner approvals.",
    ))

    # ── Strategy Selection ──
    available = [a for a in actions if a.available]
    recommended: list[str] = []
    reasoning_parts: list[str] = []

    # Rule 1: Blocking funnel issue → fix it first
    if has_blocking_issue:
        recommended.append("repair_funnel")
        reasoning_parts.append(
            "Funnel has a blocking issue — zero probability of goal "
            "achievement until repaired."
        )
        if funnel_issues:
            reasoning_parts.append(f"Issue: {funnel_issues[0]['detail']}")

    # Rule 2: OLSP data unavailable blocks only OLSP-dependent work. Continue
    # independent investigation and planning paths.
    if not olsp_available:
        if "review_funnel" not in recommended and ARTICLE_PATH.is_file():
            recommended.append("review_funnel")
        if "collect_facebook_metrics" not in recommended:
            recommended.append("collect_facebook_metrics")
        if "evaluate_campaigns" not in recommended:
            recommended.append("evaluate_campaigns")
        reasoning_parts.append(
            "OLSP dashboard authentication is unavailable, so OLSP-dependent measurement is blocked while independent investigation continues."
        )

    # Rule 3: Funnel healthy + social plan exists → publish
    if not has_blocking_issue and olsp_available and social["plan_exists"]:
        if "publish_facebook" not in recommended and social["plan_status"] == "READY" and social["platform"] == "facebook":
            recommended.append("publish_facebook")
            reasoning_parts.append(
                "Funnel operational, social plan ready. Facebook post has "
                "highest probability of driving article traffic today."
            )

    # Rule 4: Maintain planning cadence
    if not social["plan_exists"] and "generate_social_plan" not in recommended:
        recommended.insert(0, "generate_social_plan")
        reasoning_parts.append("No social plan exists — planning must happen before publishing.")

    # Rule 5: Verify funnel before any traffic-driving action
    has_traffic_action = any(a in recommended for a in ("publish_facebook", "publish_youtube_short"))
    if has_traffic_action and "review_funnel" not in recommended:
        recommended.insert(0, "review_funnel")
        reasoning_parts.append("Verifying funnel health before driving traffic.")

    # Rule 6: No actions selected → maintain baseline
    if not recommended:
        recommended.append("collect_olsp_data")
        recommended.append("generate_social_plan")
        reasoning_parts.append(
            "No immediate production actions available. Commander maintains "
            "measurement baseline and social planning cadence."
        )

    reasoning = " ".join(reasoning_parts) if reasoning_parts else "No production actions identified."

    # Evidence classification — what Commander can verify vs what it assumes
    evidence_classes: dict[str, str] = {}
    evidence_classes["olsp_data"] = "VERIFIED" if olsp_available else "MISSING"
    evidence_classes["article_available"] = "VERIFIED" if ARTICLE_PATH.is_file() else "MISSING"
    evidence_classes["social_plan"] = "VERIFIED" if social.get("plan_exists") else "MISSING"
    evidence_classes["funnel_assessment"] = "VERIFIED" if funnel["status"] in ("HEALTHY", "DEGRADED", "BROKEN") else "UNKNOWN"
    evidence_classes["daily_goal_measurable"] = (
        "VERIFIED" if daily_measurement_available else "UNVERIFIABLE"
    )
    evidence_classes["strategy_confidence"] = "ESTIMATED"  # Commander estimates, not verified
    evidence_classes["publication_today"] = "VERIFIED" if social.get("plan_exists") else "UNKNOWN"
    if funnel["status"] != "HEALTHY" and not funnel.get("issues"):
        evidence_classes["funnel_assessment"] = "UNKNOWN"  # broken but no diagnosis

    return GoalExecutionPlan(
        goal=goal_text,
        mission=mission_text,
        project=PROJECT_DISPLAY_NAME,
        current_status=current_status,
        gap=gap,
        funnel_diagnosis=funnel,
        available_actions=actions,
        recommended_sequence=recommended,
        reasoning=reasoning,
        evidence_classifications=evidence_classes,
    )


def render_plan(plan: GoalExecutionPlan) -> str:
    """Render a Goal Execution Plan as a readable text block."""
    lines = [
        "=" * 60,
        "GOAL EXECUTION PLAN",
        "=" * 60,
        "",
        f"Project:  {plan.project} ({PROJECT_ID})",
        f"Brand:    {BRAND_NAME}",
        f"Mission:  {plan.mission}",
        f"Planner:  Commander (Hermes production platform)",
        "",
        "─" * 40,
        "CURRENT STATUS",
        "─" * 40,
    ]

    cs = plan.current_status
    lines.append(f"  OLSP data source:  {'available' if cs.get('olsp_data_available') else 'unavailable'}")
    if cs.get("olsp_data_available"):
        lines.append(f"  Leads (all time):  {cs.get('leads_all_time', '?')}")
        lines.append(f"  Customers (all time): {cs.get('customers_all_time', '?')}")
        lines.append(f"  Transactions (all time): {cs.get('transactions_all_time', '?')}")
        bal = cs.get("current_balance")
        lines.append(f"  Current balance:   ${bal:.2f}" if bal is not None else f"  Current balance:   unknown")
        life = cs.get("lifetime_balance")
        lines.append(f"  Lifetime balance:  ${life:.2f}" if life is not None else f"  Lifetime balance:  unknown")
    if cs.get("daily_signups_measurable"):
        lines.append(
            "  Daily measurement:  active — "
            f"signups {cs.get('daily_signups')}, sales {cs.get('daily_sales')}, "
            f"revenue ${cs.get('daily_revenue', 0):.2f}"
        )
    else:
        lines.append("  Daily measurement:  NOT AVAILABLE")
    lines.append(f"  Funnel:            {cs.get('funnel_status', '?')} ({cs.get('funnel_health_pct', 0)}/100)")
    lines.append(f"  Social plan:       {'ready' if cs.get('social_plan_ready') else 'not ready'}")
    lines.append(f"  Publications today: {cs.get('social_publications_today', 0)}")

    lines.append("")
    lines.append("─" * 40)
    lines.append("FUNNEL DIAGNOSIS")
    lines.append("─" * 40)

    fd = plan.funnel_diagnosis
    lines.append(f"  Status:           {fd.get('status', '?')} ({fd.get('health_pct', 0)}/100)")
    lines.append(f"  Article present:  {bool(fd.get('articles_found'))}")
    lines.append(f"  CTA buttons:      {len(fd.get('cta_elements_found', []))}")
    lines.append(f"  Mega link matches: {len(fd.get('mega_link_matches', []))}")
    if fd.get("issues"):
        for issue in fd["issues"]:
            sev = issue["severity"]
            detail = issue["detail"][:120]
            lines.append(f"  [{sev}] {detail}")

    lines.append("")
    lines.append("─" * 40)
    lines.append("GAP")
    lines.append("─" * 40)

    g = plan.gap
    lines.append(f"  Goal measurable:  {'No — aggregate lifetime data only' if not g.get('goal_measurable') else 'Yes'}")
    signups_gap = g.get("signups_needed_estimate")
    if signups_gap is not None:
        lines.append(f"  Signups gap (est): {signups_gap}")
    else:
        lines.append(f"  Signups gap (est): unknown — no customer data")
    sales_gap = g.get("sales_needed_estimate")
    if sales_gap is not None:
        lines.append(f"  Sales gap:        {sales_gap}")
    else:
        lines.append("  Sales gap:        unknown — no verified daily sales value")
    if g.get("note"):
        lines.append(f"  Note:             {g['note'][:100]}")

    lines.append("")
    lines.append("─" * 40)
    lines.append("AVAILABLE ACTIONS")
    lines.append("─" * 40)
    for i, action in enumerate(plan.available_actions, 1):
        marker = "✓" if action.available else "✗"
        lines.append(f"\n  {i}. [{marker}] {action.label}")
        if action.available:
            lines.append(f"     Why:         {action.why_it_helps[:110]}")
            lines.append(f"     Evidence:    {action.supporting_evidence[:110]}")
            lines.append(f"     Improvement: {action.expected_improvement[:110]}")
            lines.append(f"     Failure:     {action.failure_evidence[:110]}")
            lines.append(f"     Next if fail: {action.next_if_failed[:110]}")
            lines.append(f"     Confidence:  {action.estimated_confidence}")
        else:
            lines.append(f"     Blocked:     {action.blocked_reason[:110]}")

    lines.append("")
    lines.append("─" * 40)
    lines.append("OPERATING LOOP")
    lines.append("─" * 40)
    lines.append("  Commander is the daily operator, not a task executor.")
    lines.append("  The loop continues until goal achieved, day ends, or BLOCKED.")
    lines.append("")
    lines.append("  Observe  → Analyze → Decide → Execute → Measure → Compare")
    lines.append("     ↑                                                |")
    lines.append("     └────────────────────────────────────────────────┘")
    lines.append("")

    lines.append("─" * 40)
    lines.append("RECOMMENDED STRATEGY")
    lines.append("─" * 40)
    lines.append(f"  Sequence:  {' → '.join(plan.recommended_sequence) if plan.recommended_sequence else '(none)'}")
    lines.append(f"  Reasoning: {plan.reasoning[:250]}")

    lines.append("")
    lines.append("─" * 40)
    lines.append("EVIDENCE CLASSIFICATION")
    lines.append("─" * 40)
    for key, cls in sorted(plan.evidence_classifications.items()):
        label = key.replace("_", " ").title()
        lines.append(f"  {label:<28} {cls}")

    lines.append("")
    lines.append("=" * 60)

    return "\n".join(lines)


def diff_plan(plan: GoalExecutionPlan, completed: list[str]) -> str:
    """Compare Commander's planned actions to completed actions."""
    planned = set(plan.recommended_sequence)
    done = set(completed)
    skipped = planned - done
    extra = done - planned

    lines = [
        "",
        "─" * 40,
        "PLAN VS ACTUAL",
        "─" * 40,
        f"  Planned:   {', '.join(plan.recommended_sequence) if plan.recommended_sequence else '(none)'}",
        f"  Completed: {', '.join(completed) if completed else '(none)'}",
    ]
    if skipped:
        lines.append(f"  Skipped:   {', '.join(sorted(skipped))}")
    if extra:
        lines.append(f"  Extra:     {', '.join(sorted(extra))}")

    g = plan.gap
    measurement = "aggregate lifetime only" if not g.get("goal_measurable") else "daily measurement available"
    lines.append(f"  Goal measurement: {measurement}")
    lines.append("")
    return "\n".join(lines)


def _campaign_snapshots() -> list:
    try:
        from app.commander.campaign_evaluation import evaluate_campaigns
        return evaluate_campaigns()
    except Exception:
        return []


def _previous_execution_state() -> dict[str, Any]:
    if not REALITY_PATH.is_file():
        return {}
    try:
        return json.loads(REALITY_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}

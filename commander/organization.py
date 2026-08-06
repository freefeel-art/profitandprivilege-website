"""Canonical project role bindings for the single-Commander organization.

This registry binds human-readable operating roles to existing project
entrypoints. It deliberately does not create new execution mechanisms.
"""

from __future__ import annotations

from typing import Final


ROLE_BINDINGS: Final[dict[str, dict[str, object]]] = {
    "commander": {
        "status": "operational",
        "entrypoints": ("hermes next", "hermes run"),
        "implementation": "app/commander/",
        "owner": "Commander",
    },
    "scout": {
        "status": "conditional",
        "entrypoints": (
            "research/discovery/runner.py",
            "research/community_intelligence/processor.py",
        ),
        "implementation": "research/",
        "owner": "Commander",
        "limitation": "Community collection remains manual and is not a Commander executor.",
    },
    "reach": {
        "status": "operational",
        "entrypoints": (
            "commander/executors.py:execute_daily_production_procedure",
            "commander/executors.py:execute_social_planning",
            "commander/goal_plan.py",
        ),
        "implementation": "commander/",
        "owner": "Commander",
    },
    "scribe": {
        "status": "operational",
        "entrypoints": (
            "commander/scribe.py",
            "research/content_production/producer.py",
            "bash pipeline/bridge-to-builder.sh",
        ),
        "implementation": "research/content_production/ and pipeline/",
        "owner": "Commander",
        "limitation": "Scribe emits a validated content package; Editorial Builder remains a separate downstream Astro stage.",
    },
    "coder": {
        "status": "conditional",
        "entrypoints": ("/home/yampa/projects/active/hermes/agents/coder/run.sh --check",),
        "implementation": "/home/yampa/projects/active/hermes/agents/coder/run.sh",
        "owner": "Commander",
        "limitation": "Read-only canonical-root check is verified; interactive editing depends on the local Aider installation.",
    },
    "measurement": {
        "status": "operational",
        "entrypoints": (
            "app/providers/olsp_dashboard.py",
            "app/providers/ga4_metrics.py",
            "commander/measurement.py",
        ),
        "implementation": "app/providers/ and commander/",
        "owner": "Commander",
        "limitation": "External or incomplete period-scoped evidence remains partial.",
    },
    "publisher": {
        "status": "conditional",
        "entrypoints": ("node publishing/publish.cjs",),
        "implementation": "publishing/publish.cjs",
        "owner": "Commander",
        "limitation": "QA evidence and the production deployment invoker must both be available.",
    },
}


def get_role_binding(role: str) -> dict[str, object]:
    """Return a defensive copy of one canonical role binding."""
    try:
        binding = ROLE_BINDINGS[role]
    except KeyError as exc:
        raise KeyError(f"Unknown Commander role: {role}") from exc
    return dict(binding)


def operational_roles() -> tuple[str, ...]:
    """Return roles with a currently usable project entrypoint."""
    return tuple(
        role for role, binding in ROLE_BINDINGS.items()
        if binding["status"] == "operational"
    )

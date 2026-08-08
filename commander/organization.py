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
        "status": "operational",
        "entrypoints": ("/home/Yampa/hermes/agents/scout/run.sh",),
        "implementation": "/home/Yampa/hermes/agents/scout/",
        "owner": "Commander",
        "limitation": "Individual sources may return a truthful external blocker; Commander must select another executable channel.",
    },
    "community_manager": {
        "status": "operational",
        "entrypoints": ("/home/Yampa/hermes/agents/community_manager/run.sh",),
        "implementation": "/home/Yampa/hermes/agents/community_manager/",
        "owner": "Commander",
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
        "status": "operational",
        "entrypoints": ("/home/Yampa/hermes/agents/coder/run.sh --assignment",),
        "implementation": "/home/Yampa/hermes/agents/coder/",
        "owner": "Commander",
        "limitation": "Repairs require a bounded assignment and verification command.",
    },
    "measurement": {
        "status": "operational",
        "entrypoints": (
            "/home/Yampa/hermes/agents/measurement/run.sh",
            "/home/Yampa/hermes/hermes collect olsp",
        ),
        "implementation": "app/providers/ and commander/",
        "owner": "Commander",
        "limitation": "External or incomplete period-scoped evidence remains partial.",
    },
    "publisher": {
        "status": "conditional",
        "entrypoints": ("/home/Yampa/hermes/agents/publisher/run.sh",),
        "implementation": "/home/Yampa/hermes/agents/publisher/",
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

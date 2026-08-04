"""GoHighLevel read-only audit for profit-and-privilege project.

Prints a comprehensive snapshot of the GHL account state without making any writes.
"""

import json
import logging
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
import requests
from app.core.projects import active_project_runtime_directory

load_dotenv()

logger = logging.getLogger(__name__)

BASE = "https://services.leadconnectorhq.com"
VERSION = "2021-07-28"
LOCATION_ID = "GSInZxexJyODz5tKWVuH"


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {os.getenv('GHL_TOKEN', '')}",
        "Accept": "application/json",
        "Version": VERSION,
    }


def _get(path: str, params: dict | None = None) -> dict | list | None:
    url = f"{BASE}{path}"
    try:
        r = requests.get(url, headers=_headers(), params=params, timeout=15)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def audit() -> dict[str, Any]:
    """Return full read-only snapshot."""
    results: dict[str, Any] = {"audited_at": datetime.now(timezone.utc).isoformat()}

    # ── Location ──
    loc = _get(f"/locations/{LOCATION_ID}")
    results["location"] = loc.get("location", loc) if loc else None

    # ── Contacts ──
    contacts_sample = _get("/contacts/", params={"locationId": LOCATION_ID, "limit": 50})
    total = 0
    emails = 0
    no_email = 0
    sample_contacts = []
    if contacts_sample:
        total = contacts_sample.get("meta", {}).get("total", len(contacts_sample.get("contacts", [])))
        for c in contacts_sample.get("contacts", [])[:50]:
            entry = {
                "id": c.get("id"),
                "name": f"{c.get('firstName', '')} {c.get('lastName', '')}".strip(),
                "email": c.get("email") or None,
                "phone": c.get("phone") or None,
                "tags": c.get("tags", []),
                "created": c.get("dateAdded"),
            }
            sample_contacts.append(entry)
            if c.get("email"):
                emails += 1
            else:
                no_email += 1
    results["contacts"] = {
        "total": total,
        "sample_size": len(sample_contacts),
        "with_email": emails,
        "without_email": no_email,
        "sample": sample_contacts[:5],
    }

    # ── Tags ──
    tags_data = _get("/locations/" + LOCATION_ID + "/tags")
    all_tags = []
    if tags_data:
        all_tags = tags_data.get("tags", tags_data if isinstance(tags_data, list) else [])
    tag_names = {t.get("name", t.get("id", "?")): 0 for t in all_tags if isinstance(t, dict)}
    results["tags"] = {
        "total": len(tag_names),
        "names": sorted(tag_names.keys())[:30],
    }

    # ── Funnels ──
    funnels_data = _get("/funnels/funnel/list", params={"locationId": LOCATION_ID, "limit": 25})
    funnels = []
    if funnels_data:
        for f in funnels_data.get("funnels", []):
            steps = f.get("steps", [])
            funnels.append({
                "name": f.get("name"),
                "url": f.get("url"),
                "step_count": len(steps),
                "step_names": [s.get("name", "?")[:50] for s in steps[:5]],
                "type": f.get("type", "?"),
            })
    results["funnels"] = {
        "total": len(funnels),
        "list": funnels,
    }

    # ── Workflows ──
    wf_data = _get("/workflows/", params={"locationId": LOCATION_ID, "limit": 25})
    workflows = []
    if wf_data:
        for w in wf_data.get("workflows", []):
            workflows.append({
                "name": w.get("name"),
                "status": w.get("status"),
                "trigger": str(w.get("triggerType", "?")) if "triggerType" in w else "?",
                "created": w.get("createdAt"),
            })
    results["workflows"] = {
        "total": len(workflows),
        "list": workflows,
    }

    # ── Campaigns (email templates) ──
    camp_data = _get("/campaigns/", params={"locationId": LOCATION_ID, "limit": 25})
    campaigns = []
    if camp_data:
        for cm in camp_data.get("campaigns", []):
            campaigns.append({"name": cm.get("name"), "status": cm.get("status"), "created": cm.get("createdAt")})
    results["campaigns"] = {"total": len(campaigns), "list": campaigns}

    # ── Calendars ──
    cal_data = _get("/calendars/", params={"locationId": LOCATION_ID})
    calendars = []
    if cal_data:
        for cl in cal_data.get("calendars", []):
            calendars.append({"name": cl.get("name"), "slug": cl.get("slug"), "created": cl.get("createdAt")})
    results["calendars"] = {"total": len(calendars), "list": calendars}

    # ── Opportunities / Pipelines ──
    pipe_data = _get("/pipelines/", params={"locationId": LOCATION_ID})
    pipelines = []
    if pipe_data:
        for pp in pipe_data.get("pipelines", []):
            stages = [(s.get("name"), s.get("opportunities", 0)) for s in pp.get("stages", [])]
            pipelines.append({"name": pp.get("name"), "stages": stages})
    results["pipelines"] = {"total": len(pipelines), "list": pipelines}

    # ── Surveys ──
    survey_data = _get("/surveys/", params={"locationId": LOCATION_ID, "limit": 25})
    surveys = []
    if survey_data:
        for sv in survey_data.get("surveys", []):
            surveys.append({"name": sv.get("name"), "created": sv.get("createdAt")})
    results["surveys"] = {"total": len(surveys), "list": surveys}

    return results


def print_audit(report: dict[str, Any]) -> None:
    """Pretty-print the audit report."""
    print("=" * 60)
    print("GoHighLevel Read-Only Audit")
    print(f"  Location: {report.get('location', {}).get('name', '?')}")
    print(f"  Audited:  {report['audited_at']}")
    print("=" * 60)

    c = report.get("contacts", {})
    print(f"\n─── CONTACTS ({c.get('total', 0)} total) ───")
    print(f"  With email: {c.get('with_email', 0)}  Without: {c.get('without_email', 0)}")
    for s in c.get("sample", [])[:3]:
        print(f"  {s['name'][:25]:25s} | {s.get('email') or 'no email':35s} | tags={s['tags'][:3]}")

    t = report.get("tags", {})
    print(f"\n─── TAGS ({t.get('total', 0)} total) ───")
    names = t.get("names", [])
    if names:
        for n in names[:20]:
            print(f"  {n}")
    else:
        print("  Ei tageja")

    f = report.get("funnels", {})
    print(f"\n─── FUNNELS ({f.get('total', 0)} total) ───")
    for fn in f.get("list", []):
        print(f"  [{fn['type']}] {fn['name'][:50]:50s} {fn['step_count']} steps")
        if fn["step_names"]:
            print(f"    Steps: {', '.join(fn['step_names'][:3])}")

    wf = report.get("workflows", {})
    print(f"\n─── WORKFLOWS ({wf.get('total', 0)} total) ───")
    for w in wf.get("list", []):
        status = w.get("status", "?")
        print(f"  [{status}] {w['name'][:60]:60s} trigger={w.get('trigger', '?')}")

    cm = report.get("campaigns", {})
    print(f"\n─── CAMPAIGNS ({cm.get('total', 0)} total) ───")
    for c in cm.get("list", []):
        print(f"  [{c.get('status', '?')}] {c['name'][:60]}")

    cl = report.get("calendars", {})
    print(f"\n─── CALENDARS ({cl.get('total', 0)} total) ───")
    for c in cl.get("list", []):
        print(f"  {c['name'][:50]:50s} slug={c.get('slug', '?')}")

    pp = report.get("pipelines", {})
    print(f"\n─── PIPELINES ({pp.get('total', 0)} total) ───")
    for p in pp.get("list", []):
        print(f"  {p['name'][:40]:40s} stages={p.get('stages', [])}")

    sv = report.get("surveys", {})
    print(f"\n─── SURVEYS ({sv.get('total', 0)} total) ───")
    for s in sv.get("list", []):
        print(f"  {s['name'][:60]}")

    print("\n" + "=" * 60)
    print("Audit complete — no writes performed")
    print("=" * 60)


if __name__ == "__main__":
    report = audit()
    print_audit(report)

    out_path = active_project_runtime_directory() / "ghl_audit.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str))
    print(f"\nFull report saved: {out_path}")

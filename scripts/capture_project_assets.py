#!/usr/bin/env python3
"""Capture OLSP screenshots for the Profit & Privilege visual asset library.

Public pages are captured headlessly. Authenticated pages require the
persistent Chrome profile at config/storage_state.json or the OLSP
dashboard browser profile.
"""

import sys
from datetime import datetime, timezone
from pathlib import Path

from app.commander.visual_library import ProjectAssetLibrary, VisualAsset


PUBLIC_PAGES = [
    {
        "id": "olsp-mlm-review-article",
        "url": "https://olsp.profitandprivilege.com/is-olsp-academy-an-mlm/",
        "category": "landing-pages",
        "description": "The full OLSP Academy MLM review article on profitandprivilege.com",
        "tags": ("article", "review", "olsp", "mlm", "landing"),
        "topics": ("landing-pages", "sales-pages"),
    },
    {
        "id": "olsp-homepage",
        "url": "https://olspacademy.com",
        "category": "landing-pages",
        "description": "OLSP Academy official homepage",
        "tags": ("homepage", "olsp", "official"),
        "topics": ("landing-pages",),
    },
    {
        "id": "olsp-mega-link-landing",
        "url": "https://olspacademy.com/megalive/",
        "category": "mega-link",
        "description": "OLSP Mega Link landing page — the primary conversion path",
        "tags": ("mega-link", "landing", "signup", "conversion"),
        "topics": ("mega-link", "landing-pages", "sign.up"),
    },
    {
        "id": "olsp-affiliate-page",
        "url": "https://olspacademy.com/affiliate",
        "category": "landing-pages",
        "description": "OLSP Academy affiliate program page",
        "tags": ("affiliate", "program", "olsp"),
        "topics": ("landing-pages", "affiliate"),
    },
    {
        "id": "profit-and-privilege-home",
        "url": "https://profitandprivilege.com",
        "category": "branding",
        "description": "Profit & Privilege project website homepage",
        "tags": ("brand", "homepage", "profit-and-privilege"),
        "topics": ("landing-pages", "branding"),
    },
]


AUTHENTICATED_PAGES = [
    {
        "id": "olsp-dashboard-home",
        "url": "https://olspacademy.com/app",
        "category": "dashboard",
        "description": "OLSP Academy dashboard — affiliate overview",
        "tags": ("dashboard", "affiliate", "overview"),
        "topics": ("dashboard",),
    },
    {
        "id": "olsp-dashboard-leads",
        "url": "https://olspacademy.com/affiliate/leads",
        "category": "dashboard",
        "description": "OLSP Academy — affiliate leads page",
        "tags": ("dashboard", "leads", "affiliate"),
        "topics": ("dashboard",),
    },
    {
        "id": "olsp-dashboard-customers",
        "url": "https://olspacademy.com/affiliate/customers",
        "category": "dashboard",
        "description": "OLSP Academy — affiliate customers page",
        "tags": ("dashboard", "customers", "affiliate"),
        "topics": ("dashboard", "commission"),
    },
    {
        "id": "olsp-dashboard-transactions",
        "url": "https://olspacademy.com/affiliate/transactions",
        "category": "dashboard",
        "description": "OLSP Academy — affiliate transactions page",
        "tags": ("dashboard", "transactions", "revenue"),
        "topics": ("dashboard", "commission"),
    },
    {
        "id": "olsp-dashboard-promote",
        "url": "https://olspacademy.com/affiliate/promote",
        "category": "dashboard",
        "description": "OLSP Academy — affiliate promote/mega link page",
        "tags": ("dashboard", "promote", "mega-link"),
        "topics": ("dashboard", "mega-link"),
    },
    {
        "id": "olsp-live-webinar",
        "url": "https://olspacademy.com/c/livebinar",
        "category": "webinars",
        "description": "OLSP Academy live webinar page",
        "tags": ("webinar", "live", "training"),
        "topics": ("webinars",),
        "refresh": "auto-refresh",
    },
]


def _capture_public_assets(asset_lib: ProjectAssetLibrary) -> int:
    """Capture public pages and register them in the asset library."""
    captured = 0
    for spec in PUBLIC_PAGES:
        asset_path = asset_lib.assets_dir / "screenshots" / spec["category"] / f"{spec['id']}.png"
        if asset_path.exists():
            continue

        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(viewport={"width": 1080, "height": 1920})
                page.goto(spec["url"], wait_until="domcontentloaded", timeout=30_000)
                page.wait_for_timeout(2000)
                asset_path.parent.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(asset_path), full_page=False)
                browser.close()
        except Exception as exc:
            print(f"  SKIP {spec['id']}: {exc}", file=sys.stderr)
            continue

        if asset_path.is_file():
            asset = VisualAsset(
                id=spec["id"],
                path=str(asset_path.relative_to(asset_lib.assets_dir)),
                category=spec["category"],
                description=spec["description"],
                source_url=spec["url"],
                captured_at=datetime.now(timezone.utc).isoformat(),
                tags=tuple(spec.get("tags", [])),
                article_topics=tuple(spec.get("topics", [])),
                refresh_policy=spec.get("refresh", "persistent"),
                format="png",
            )
            asset_lib.add_asset(asset)
            captured += 1
            print(f"  OK {spec['id']} -> {asset.path}")
    return captured


def _register_authenticated_entries(asset_lib: ProjectAssetLibrary) -> int:
    """Register authenticated page entries as uncaptured (placeholder)."""
    registered = 0
    for spec in AUTHENTICATED_PAGES:
        asset_path = asset_lib.assets_dir / "screenshots" / spec["category"] / f"{spec['id']}.png"
        existing = asset_lib.list_assets()
        if any(a.id == spec["id"] for a in existing):
            continue
        asset = VisualAsset(
            id=spec["id"],
            path=str(asset_path.relative_to(asset_lib.assets_dir)),
            category=spec["category"],
            description=spec["description"],
            source_url=spec["url"],
            captured_at="",
            tags=tuple(spec.get("tags", [])),
            article_topics=tuple(spec.get("topics", [])),
            refresh_policy=spec.get("refresh", "persistent"),
            format="png",
        )
        asset_lib.add_asset(asset)
        registered += 1
        print(f"  REGISTERED {spec['id']} — needs authenticated capture")
    return registered


def build_asset_library(project_dir: str | Path) -> dict:
    """Capture all available screenshots and populate the asset index."""
    asset_lib = ProjectAssetLibrary(Path(project_dir))
    print("Capturing public pages...")
    public_count = _capture_public_assets(asset_lib)
    print(f"  {public_count} public screenshots captured")
    print("Registering authenticated pages...")
    auth_count = _register_authenticated_entries(asset_lib)
    print(f"  {auth_count} authenticated entries registered")
    total = asset_lib.asset_count()
    print(f"\nTotal assets in library: {total}")
    return {
        "public_captured": public_count,
        "authenticated_registered": auth_count,
        "total": total,
        "inventory": asset_lib.inventory(),
    }


if __name__ == "__main__":
    from app.core.projects import active_project_directory
    project_directory = active_project_directory()
    if project_directory is None:
        raise RuntimeError("No active project selected")
    result = build_asset_library(str(project_directory))
    print()
    print("Inventory:")
    for cat, ids in result["inventory"].items():
        print(f"  {cat}: {len(ids)} assets")
        for aid in ids:
            print(f"    - {aid}")

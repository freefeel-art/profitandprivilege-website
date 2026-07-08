#!/usr/bin/env python3
"""
Discovery Runner — bridges the Discovery Query Library with Discovery Providers.

Workflow:
    1. Load configuration
    2. Load pillar from Discovery Query Library
    3. For every problem in every cluster, execute each search query
    4. Tag each returned post with its source (query, cluster, problem)
    5. Deduplicate identical posts by Reddit post ID
    6. Save everything inside one Discovery Package

This component ONLY collects data.
No scoring, no clustering, no editorial analysis.
Community Intelligence begins AFTER this step.
"""

from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set

from research.discovery.loader import DiscoveryLoader


def load_config(path: str) -> dict:
    """Load runner configuration from a JSON file."""
    if not os.path.exists(path):
        print(f"ERROR: Config file not found: {path}")
        sys.exit(1)
    with open(path) as f:
        return json.load(f)


def resolve_provider(provider_name: str):
    """Import and return the provider module by name."""
    if provider_name == "scrape_creators":
        from research.discovery.providers import scrape_creators
        return scrape_creators
    print(f"ERROR: Unknown provider: {provider_name}")
    sys.exit(1)


def now_iso() -> str:
    """Return current UTC timestamp as ISO 8601 string."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def deduplicate_posts(posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Deduplicate posts by Reddit post ID, keeping first occurrence."""
    seen: Set[str] = set()
    unique: List[Dict[str, Any]] = []
    for post in posts:
        pid = post.get("id", "")
        if pid and pid not in seen:
            seen.add(pid)
            unique.append(post)
    return unique


def run_discovery(config: dict) -> dict:
    """Execute one full discovery cycle for the configured pillar.

    Args:
        config: Dict with keys:
            - provider (str): provider module name
            - pillar_slug (str): pillar slug in the Discovery Query Library
            - limit (int): max posts to request per query

    Returns:
        A Discovery Package dict with all collected data.
    """
    provider_name = config.get("provider", "scrape_creators")
    pillar_slug = config.get("pillar_slug", "")
    limit = config.get("limit", 20)

    if not pillar_slug:
        print("ERROR: No pillar_slug in config")
        sys.exit(1)

    # Load pillar from Discovery Query Library
    loader = DiscoveryLoader()
    pillar = loader.get_pillar(pillar_slug)
    if pillar is None:
        print(f"ERROR: Unknown pillar slug: {pillar_slug}")
        print(f"  Available: {loader.list_pillar_slugs()}")
        sys.exit(1)

    # Resolve and initialise provider
    provider = resolve_provider(provider_name)

    print(f"Starting discovery for: {pillar.name} ({pillar.slug})")
    print(f"  Provider: {provider_name}")
    print(f"  Clusters: {len(pillar.clusters)}")

    # Execute all queries
    queries_executed: List[dict] = []
    all_posts: List[Dict[str, Any]] = []
    total_queries = 0

    for cluster in pillar.clusters:
        print(f"\n  Cluster: {cluster.name}")
        for problem in cluster.problems:
            print(f"    Problem: {problem.description[:60]}...")
            for query in problem.search_queries:
                total_queries += 1
                print(f"      [{total_queries}] Query: {query[:70]}...", end=" ")
                sys.stdout.flush()

                result = provider.search(query, limit=limit)

                # Tag each post with its source context
                for post in result.posts:
                    post["_discovery"] = {
                        "pillar_slug": pillar_slug,
                        "pillar_name": pillar.name,
                        "cluster": cluster.name,
                        "problem": problem.description,
                        "matched_query": query,
                        "provider": provider_name,
                        "timestamp": now_iso(),
                    }

                all_posts.extend(result.posts)
                queries_executed.append({
                    "query": query,
                    "cluster": cluster.name,
                    "problem": problem.description,
                    "success": result.success,
                    "status_code": result.status_code,
                    "response_time_seconds": result.response_time_seconds,
                    "posts_found": len(result.posts),
                    "error": result.error,
                })

                status = f"OK ({len(result.posts)} posts)"
                if result.success:
                    print(f" {status}")
                else:
                    print(f" FAILED ({result.status_code}: {str(result.error)[:50]})")

    # Deduplicate all collected posts
    before_dedup = len(all_posts)
    unique_posts = deduplicate_posts(all_posts)
    duplicates_removed = before_dedup - len(unique_posts)

    # Collect all unique subreddits
    subreddits: Set[str] = set()
    for p in unique_posts:
        sub = p.get("subreddit", "")
        if sub:
            subreddits.add(sub)

    # Build the discovery package
    package = {
        "discovery_metadata": {
            "pillar_name": pillar.name,
            "pillar_slug": pillar.slug,
            "pillar_description": pillar.description,
            "provider": provider_name,
            "config_used": {
                "limit": limit,
                "pillar_slug": pillar_slug,
                "provider": provider_name,
            },
            "timestamp": now_iso(),
        },
        "queries_executed": queries_executed,
        "summary": {
            "total_queries": total_queries,
            "queries_succeeded": sum(1 for q in queries_executed if q["success"]),
            "queries_failed": sum(1 for q in queries_executed if not q["success"]),
            "total_raw_posts": before_dedup,
            "unique_posts": len(unique_posts),
            "duplicates_removed": duplicates_removed,
            "subreddits_covered": len(subreddits),
            "providers_used": [provider_name],
        },
        "subreddits": sorted(subreddits),
        "posts": unique_posts,
    }

    return package


def save_package(package: dict, output_dir: str, pillar_slug: str):
    """Save the discovery package to a JSON file."""
    out_dir = os.path.join(os.getcwd(), output_dir)
    os.makedirs(out_dir, exist_ok=True)
    filename = f"{pillar_slug}-discovery.json"
    filepath = os.path.join(out_dir, filename)
    with open(filepath, "w") as f:
        json.dump(package, f, indent=2, default=str)
    print(f"\n  Saved: {filepath}")
    return filepath


def print_summary(package: dict):
    """Print a human-readable summary of the discovery run."""
    meta = package["discovery_metadata"]
    s = package["summary"]
    subreddits = package.get("subreddits", [])

    print(f"\n{'=' * 60}")
    print(f"DISCOVERY COMPLETE")
    print(f"{'=' * 60}")
    print(f"  Pillar:     {meta['pillar_name']} ({meta['pillar_slug']})")
    print(f"  Provider:   {meta['provider']}")
    print(f"  Timestamp:  {meta['timestamp']}")
    print(f"")
    print(f"  Queries:    {s['total_queries']} total "
          f"({s['queries_succeeded']} OK, {s['queries_failed']} failed)")
    print(f"  Raw posts:  {s['total_raw_posts']}")
    print(f"  Unique:     {s['unique_posts']} "
          f"(removed {s['duplicates_removed']} duplicates)")
    print(f"  Subreddits: {s['subreddits_covered']}")
    print(f"  Providers:  {', '.join(s['providers_used'])}")
    print(f"")
    if subreddits:
        print(f"  Communities ({len(subreddits)}):")
        for sub in subreddits[:10]:
            print(f"    r/{sub}")
        if len(subreddits) > 10:
            print(f"    ... and {len(subreddits) - 10} more")
    print(f"{'=' * 60}")


def main():
    # Default config path relative to this file
    default_config = os.path.join(
        os.path.dirname(__file__), "config.json"
    )

    config_path = sys.argv[1] if len(sys.argv) > 1 else default_config
    override_pillar = sys.argv[2] if len(sys.argv) > 2 else None

    config = load_config(config_path)

    # Allow CLI override: python runner.py config.json lead_generation
    if override_pillar:
        config["pillar_slug"] = override_pillar

    package = run_discovery(config)

    output_dir = config.get("output_dir", "research/output/discovery")
    save_package(package, output_dir, config["pillar_slug"])

    print_summary(package)


if __name__ == "__main__":
    main()

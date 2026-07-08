#!/usr/bin/env python3
"""
Test the Discovery Query Library.

Loads all registered pillars and prints the hierarchy:
    Pillar → Clusters → Problems → Search Queries

Verifies that all data loads correctly without errors.
"""

from research.discovery.loader import DiscoveryLoader, load_all
from research.discovery.models import Pillar


def count_queries(pillar: Pillar) -> int:
    total = 0
    for cluster in pillar.clusters:
        for problem in cluster.problems:
            total += len(problem.search_queries)
    return total


def print_pillar(pillar: Pillar, indent: str = ""):
    qty = count_queries(pillar)
    print(f"{indent}PILLAR: {pillar.name} (slug: {pillar.slug})")
    print(f"{indent}  Description: {pillar.description[:80]}...")
    print(f"{indent}  Clusters: {len(pillar.clusters)}")
    print(f"{indent}  Total search queries: {qty}")
    if pillar.brands:
        print(f"{indent}  Brands: {', '.join(pillar.brands)}")

    for cluster in pillar.clusters:
        print(f"\n{indent}  ── CLUSTER: {cluster.name}")
        print(f"{indent}      {cluster.description[:80]}...")
        for problem in cluster.problems:
            print(f"\n{indent}      PROBLEM: {problem.description}")
            for q in problem.search_queries:
                print(f"{indent}        → {q}")
            comms = ", ".join(problem.communities)
            print(f"{indent}        Communities: {comms}")


def main():
    print("=" * 72)
    print("DISCOVERY QUERY LIBRARY — DATA LOAD TEST")
    print("=" * 72)

    # Test 1: load_all()
    print("\n\n--- Test 1: load_all() ---")
    all_pillars = load_all()
    print(f"  Pillars loaded: {len(all_pillars)}")
    for p in all_pillars:
        print(f"    - {p.name} ({p.slug})")

    # Test 2: DiscoveryLoader
    print("\n\n--- Test 2: DiscoveryLoader ---")
    loader = DiscoveryLoader()
    slugs = loader.list_pillar_slugs()
    print(f"  Pillar slugs: {slugs}")

    # Test 3: get_pillar
    print("\n\n--- Test 3: get_pillar() ---")
    for slug in slugs:
        p = loader.get_pillar(slug)
        assert p is not None, f"Missing pillar: {slug}"
        print(f"  ✓ {slug}: {p.name} ({len(p.clusters)} clusters)")

    # Test 4: detailed print of all pillars
    print("\n\n--- Test 4: Full Hierarchy ---")
    for pillar in all_pillars:
        print()
        print("─" * 72)
        print_pillar(pillar)
        print()

    # Test 5: search_queries_for_pillar()
    print("\n\n--- Test 5: search_queries_for_pillar() ---")
    for slug in slugs:
        queries = loader.search_queries_for_pillar(slug)
        print(f"  {slug}: {len(queries)} queries")

    # Test 6: communities_for_pillar()
    print("\n\n--- Test 6: communities_for_pillar() ---")
    for slug in slugs:
        comms = loader.communities_for_pillar(slug)
        print(f"  {slug}: {len(comms)} unique communities")
        print(f"    {', '.join(comms[:5])}{'...' if len(comms) > 5 else ''}")

    # Test 7: search_inputs_for_ci()
    print("\n\n--- Test 7: search_inputs_for_ci() ---")
    for slug in slugs:
        ci_input = loader.search_inputs_for_ci(slug)
        assert ci_input is not None
        assert "pillar" in ci_input
        assert "search_queries" in ci_input
        assert "communities" in ci_input
        assert "clusters" in ci_input
        print(f"  ✓ {slug}: CI input structure valid ({len(ci_input['search_queries'])} queries, {len(ci_input['communities'])} communities)")

    # Summary
    total_pillars = len(all_pillars)
    total_clusters = sum(len(p.clusters) for p in all_pillars)
    total_problems = sum(len(c.problems) for p in all_pillars for c in p.clusters)
    total_queries = sum(count_queries(p) for p in all_pillars)

    print(f"\n{'=' * 72}")
    print("SUMMARY")
    print(f"  Pillars:  {total_pillars}")
    print(f"  Clusters: {total_clusters}")
    print(f"  Problems: {total_problems}")
    print(f"  Queries:  {total_queries}")
    print("  Status:   ALL TESTS PASSED ✓")
    print("=" * 72)


if __name__ == "__main__":
    main()

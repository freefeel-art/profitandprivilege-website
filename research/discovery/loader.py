from __future__ import annotations

from typing import Dict, List, Optional

from research.discovery.models import Cluster, Pillar, Problem
from research.discovery.registry import PILLAR_REGISTRY


class DiscoveryLoader:
    """Loader/helper that Community Intelligence can consume.

    Provides structured access to content pillars, clusters, problems,
    search queries, and target communities — all organized by the
    approved opportunity-first discovery hierarchy.
    """

    def __init__(self):
        self._pillars: Dict[str, Pillar] = {
            p.slug: p for p in PILLAR_REGISTRY
        }

    def list_pillars(self) -> List[Pillar]:
        """Return all registered pillars."""
        return list(self._pillars.values())

    def list_pillar_slugs(self) -> List[str]:
        """Return all pillar slugs."""
        return list(self._pillars.keys())

    def get_pillar(self, slug: str) -> Optional[Pillar]:
        """Get a single pillar by slug."""
        return self._pillars.get(slug)

    def get_cluster(self, pillar_slug: str, cluster_name: str) -> Optional[Cluster]:
        """Get a specific cluster within a pillar."""
        pillar = self.get_pillar(pillar_slug)
        if pillar is None:
            return None
        for c in pillar.clusters:
            if c.name == cluster_name:
                return c
        return None

    def search_queries_for_pillar(self, pillar_slug: str) -> List[str]:
        """Return all search queries across all clusters in a pillar (flat list)."""
        pillar = self.get_pillar(pillar_slug)
        if pillar is None:
            return []
        queries: List[str] = []
        for cluster in pillar.clusters:
            for problem in cluster.problems:
                queries.extend(problem.search_queries)
        return queries

    def search_queries_for_cluster(self, pillar_slug: str, cluster_name: str) -> List[str]:
        """Return all search queries for one cluster."""
        cluster = self.get_cluster(pillar_slug, cluster_name)
        if cluster is None:
            return []
        queries: List[str] = []
        for problem in cluster.problems:
            queries.extend(problem.search_queries)
        return queries

    def communities_for_pillar(self, pillar_slug: str) -> List[str]:
        """Return all unique target communities across a pillar."""
        pillar = self.get_pillar(pillar_slug)
        if pillar is None:
            return []
        communities: set = set()
        for cluster in pillar.clusters:
            for problem in cluster.problems:
                communities.update(problem.communities)
        return sorted(communities)

    def search_inputs_for_ci(self, pillar_slug: str) -> Optional[dict]:
        """Return a structure ready for Community Intelligence consumption.

        Returns a dict matching the proposed CI input format from the
        Discovery Search Strategy document.
        """
        pillar = self.get_pillar(pillar_slug)
        if pillar is None:
            return None
        all_queries = self.search_queries_for_pillar(pillar_slug)
        all_communities = self.communities_for_pillar(pillar_slug)
        return {
            "pillar": pillar.name,
            "slug": pillar.slug,
            "description": pillar.description,
            "search_queries": all_queries,
            "communities": all_communities,
            "brands": pillar.brands,
            "clusters": [
                {
                    "name": c.name,
                    "description": c.description,
                    "problems": [
                        {
                            "description": p.description,
                            "search_queries": p.search_queries,
                            "communities": p.communities,
                        }
                        for p in c.problems
                    ],
                }
                for c in pillar.clusters
            ],
        }


def load_all() -> List[Pillar]:
    """Simple convenience: return all pillars (no DiscoveryLoader needed)."""
    return list(PILLAR_REGISTRY)


def load_pillar(slug: str) -> Optional[Pillar]:
    """Simple convenience: get one pillar by slug."""
    for p in PILLAR_REGISTRY:
        if p.slug == slug:
            return p
    return None

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Problem:
    """A user problem / pain point within a topic cluster."""

    description: str
    search_queries: List[str]
    communities: List[str]


@dataclass
class Cluster:
    """A topic cluster within a content pillar."""

    name: str
    description: str
    problems: List[Problem]


@dataclass
class Pillar:
    """A content pillar — the top-level editorial domain."""

    name: str
    slug: str
    description: str
    clusters: List[Cluster]
    brands: List[str] = field(default_factory=list)

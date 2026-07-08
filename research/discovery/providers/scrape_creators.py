"""Scrape Creators provider — calls the Reddit search API.

This is the current (and only) Discovery provider.
Wraps the Reddit search endpoint to return clean post data
that the Discovery Runner can aggregate and deduplicate.
"""

from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

API_BASE = "https://api.scrapecreators.com/v1"


@dataclass
class ProviderResult:
    """Result from a single provider query execution."""

    query: str
    success: bool
    status_code: Optional[int]
    response_time_seconds: float
    posts: List[Dict[str, Any]] = field(default_factory=list)
    error: Optional[str] = None


def _load_env():
    """Load .env from project root (simple parser, no deps)."""
    env_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "..", ".env"
    )
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())


def reddit_search(query: str, limit: int = 20) -> ProviderResult:
    """Search Reddit for posts matching the query.

    Args:
        query: Natural-language search phrase.
        limit: Approximate max posts to request.

    Returns:
        ProviderResult with raw post data or error details.
    """
    params = {
        "query": query,
        "sort": "relevance",
        "timeframe": "all",
        "trim": "true",
    }
    url = f"{API_BASE}/reddit/search?{urllib.parse.urlencode(params)}"
    headers = {
        "x-api-key": os.environ.get("SCRAPECREATORS_API_KEY", ""),
        "Accept": "application/json",
    }
    req = urllib.request.Request(url, headers=headers)
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            elapsed = time.time() - t0
            raw = json.loads(resp.read())
            posts = raw.get("posts", [])
            return ProviderResult(
                query=query,
                success=True,
                status_code=resp.status,
                response_time_seconds=round(elapsed, 2),
                posts=posts,
            )
    except urllib.error.HTTPError as e:
        elapsed = time.time() - t0
        body = e.read().decode("utf-8", errors="replace")
        return ProviderResult(
            query=query,
            success=False,
            status_code=e.code,
            response_time_seconds=round(elapsed, 2),
            error=body,
        )
    except Exception as e:
        elapsed = time.time() - t0
        return ProviderResult(
            query=query,
            success=False,
            status_code=None,
            response_time_seconds=round(elapsed, 2),
            error=str(e),
        )


def search(query: str, limit: int = 20) -> ProviderResult:
    """Public interface: execute a single search query.

    Ensures the API key is loaded before making the call.
    """
    _load_env()
    api_key = os.environ.get("SCRAPECREATORS_API_KEY", "")
    if not api_key:
        return ProviderResult(
            query=query,
            success=False,
            status_code=None,
            response_time_seconds=0.0,
            error="SCRAPECREATORS_API_KEY not set",
        )
    return reddit_search(query, limit=limit)

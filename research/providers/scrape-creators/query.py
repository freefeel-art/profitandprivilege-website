#!/usr/bin/env python3
"""
Scrape Creators — experimental Community Intelligence provider (PoC).

Calls the Reddit search endpoint and returns raw JSON.
No summarization, no scoring, no editorial analysis.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.parse
import urllib.error

API_BASE = "https://api.scrapecreators.com/v1"


def load_env():
    """Load .env from project root if present (simple parser, no deps)."""
    env_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())


def reddit_search(keyword: str):
    """Search Reddit for posts matching keyword via Scrape Creators."""
    params = {
        "query": keyword,
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
            raw = resp.read()
            elapsed = time.time() - t0
            data = json.loads(raw)
            return {
                "test": {
                    "keyword": keyword,
                    "endpoint": "Reddit Search",
                    "url": url,
                    "success": True,
                    "status_code": resp.status,
                    "response_time_seconds": round(elapsed, 2),
                    "response_size_bytes": len(raw),
                },
                "raw_response": data,
            }
    except urllib.error.HTTPError as e:
        elapsed = time.time() - t0
        body = e.read().decode("utf-8", errors="replace")
        return {
            "test": {
                "keyword": keyword,
                "endpoint": "Reddit Search",
                "url": url,
                "success": False,
                "status_code": e.code,
                "response_time_seconds": round(elapsed, 2),
                "response_size_bytes": len(body),
                "error": body,
            },
            "raw_response": None,
        }
    except Exception as e:
        elapsed = time.time() - t0
        return {
            "test": {
                "keyword": keyword,
                "endpoint": "Reddit Search",
                "url": url,
                "success": False,
                "status_code": None,
                "response_time_seconds": round(elapsed, 2),
                "response_size_bytes": 0,
                "error": str(e),
            },
            "raw_response": None,
        }


def save_output(result: dict, slug: str):
    """Save raw result to research/output/."""
    out_dir = os.path.join(os.path.dirname(__file__), "..", "..", "output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"scrape-creators-test-{slug}.json")
    with open(path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"  Saved: {path}")
    return path


def print_summary(result: dict):
    """Print a brief human-readable summary."""
    t = result.get("test", {})
    kw = t.get("keyword", "?")
    if not t.get("success"):
        print(f"  [{kw}] FAILED (HTTP {t.get('status_code')}): {str(t.get('error', ''))[:120]}")
        return
    raw = result.get("raw_response", {})
    posts = raw.get("posts", [])
    credits = raw.get("credits_remaining", "?")
    print(f"  [{kw}] OK — {len(posts)} posts, {raw.get('comments_count', 0)} comments, {credits} credits remaining")
    print(f"  Time: {t['response_time_seconds']}s | Size: {t['response_size_bytes']} bytes")
    if posts:
        subs = set(p.get("subreddit", "?") for p in posts if p.get("subreddit"))
        print(f"  Subreddits ({len(subs)}): {', '.join(sorted(subs))}")
        print(f"  Top post: {posts[0].get('title', 'N/A')[:100]}")
        # Print all titles for quick scan
        for i, p in enumerate(posts[:5], 1):
            title = p.get("title", "N/A")
            sub = p.get("subreddit", "?")
            score = p.get("score", "?")
            print(f"    {i}. [{sub}] (score:{score}) {title[:90]}")


def run_test(keyword: str):
    """Run one test end-to-end."""
    slug = keyword.lower().replace(" ", "-").replace("/", "-")
    print(f"\n{'─'*60}")
    result = reddit_search(keyword)
    print_summary(result)
    save_output(result, slug)
    return result


def main():
    load_env()
    api_key = os.environ.get("SCRAPECREATORS_API_KEY", "")
    if not api_key:
        print("ERROR: SCRAPECREATORS_API_KEY not set.")
        sys.exit(1)
    print(f"API key: {api_key[:4]}...{api_key[-4:]}")
    keywords = [
        "OLSP Academy",
        "Affiliate Marketing",
        "Lead Generation",
    ]
    results = []
    for kw in keywords:
        results.append(run_test(kw))
    print(f"\n{'='*60}")
    print(f"ALL TESTS COMPLETE — {sum(1 for r in results if r['test']['success'])}/{len(results)} passed")


if __name__ == "__main__":
    main()

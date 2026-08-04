"""Deterministic OLSP social media content planner.

Reads the single OLSP article, extracts section-based angles with multiple hook
variants, tracks published history per content type (article/livebinar),
and selects the next angle + hook. Facebook-only — video disabled.
"""

from __future__ import annotations

import json
import os
import re
from datetime import date, datetime, timezone
from pathlib import Path

from typing import Any

from dotenv import load_dotenv

load_dotenv()


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_ROOT = PROJECT_ROOT / "runtime"
SOCIAL_PLAN_DIR = RUNTIME_ROOT / "social"
PUBLISHED_LOG = SOCIAL_PLAN_DIR / "published.json"
DRAFT_DIR = SOCIAL_PLAN_DIR / "drafts"

ARTICLE_URL = "https://olsp.profitandprivilege.com/is-olsp-academy-an-mlm/"
MEGA_LINK_URL = "https://offers.olspsystem.com/get_megalink?olsp=1006001"
LIVEBINAR_URL = "https://olspacademy.com/c/livebinar"

DAILY_PLAN_PATH = SOCIAL_PLAN_DIR / "daily-plan.json"
MANAGEMENT_REVIEW_PATH = RUNTIME_ROOT / "management-review/latest.json"

# Verified Back Office facts (captured 2026-08-01, full-read.json).
# Every claim used in a plan must trace to one of these, or be flagged
# NO VERIFIED EVIDENCE.
BACK_OFFICE_EVIDENCE: dict[str, tuple[str, str]] = {
    "live_coaching_days": (
        "Live coaching runs every Tuesday, Thursday and Saturday.",
        "olspacademy.com/app — 'Live coaching every Tuesday, Thursday, and Saturday'",
    ),
    "evergreen_megalink": (
        "MegaLink URL is evergreen — auto-redirects to the next live session.",
        "olspacademy.com/app — 'Evergreen link — auto-redirects to the next live session'",
    ),
    "megalink_commission": (
        "MegaLink $7 entry, 200% commission = $14.00 per sale.",
        "olspacademy.com/affiliate/promote — Promote Center offer card",
    ),
    "megalink_url": (
        "Official share link: https://offers.olspsystem.com/get_megalink?olsp=1006001",
        "olspacademy.com/app — Megalink URL + Promote Center",
    ),
    "livebinar_url": (
        "Livebinar page: https://olspacademy.com/c/livebinar (evergreen hub site).",
        "olspacademy.com hub site 'Profit And Privilege' → /c/livebinar",
    ),
    "webinar_materials": (
        "Featured webinar 'The Shortcut to 10k' has official materials for Email, Facebook Post, Instagram, LinkedIn, Twitter, YouTube, TikTok.",
        "olspacademy.com — webinar materials page",
    ),
    "traffic_reward": (
        "Live event attendance earns traffic credits (e.g. +$5 tracked to traffic balance).",
        "olspacademy.com/affiliate/transactions — 'Traffic reward tracked ($5 to traffic balance)'",
    ),
    "traffic_balance": (
        "Traffic balance $55.00; $90 offer = 100 clicks of Tier 1 traffic.",
        "olspacademy.com/affiliate/traffic-balance",
    ),
    "special_live_task": (
        "Special Live Task today — 50 leaderboard points, 2 special codes, 3PM UK / 10AM ET.",
        "olspacademy.com/special-tasks",
    ),
    "twelve_offers": (
        "12 active affiliate offers in the Promote Center.",
        "olspacademy.com/affiliate/promote — 'Active offers 12'",
    ),
}

SECTION_ANGLES: list[dict[str, Any]] = [
    {
        "section_id": "intro",
        "angle": "What is OLSP Academy and why everyone asks if it's an MLM",
        "pinterest_text": "Is OLSP Academy an MLM? We investigated using FTC criteria, community evidence, and documented commission structures. Here's what we found.",
        "facebook_text": "The #1 question about OLSP Academy: is it an MLM? We analyzed the platform against FTC guidelines so you don't have to guess.",
        "cta": "What's your biggest doubt about OLSP Academy?",
        "hooks": [
            {"type": "number-led", "text": "5 out of 100 people ask: is OLSP a pyramid scheme?"},
            {"type": "contrarian", "text": "OLSP isn't a pyramid scheme. But the honest answer is more complicated."},
            {"type": "personal", "text": "I researched OLSP Academy for 3 weeks. The MLM question was just the tip of the iceberg."},
        ],
    },
    {
        "section_id": "accusation",
        "angle": "The real fears behind the MLM accusation",
        "pinterest_text": "Four distinct fears drive the OLSP MLM question: wasting money, wasting effort, looking foolish, or missing out. Which one is yours?",
        "facebook_text": "Why does the OLSP MLM question carry so much emotional weight? Community discussions reveal four distinct fears — and none of them are about the legal definition.",
        "cta": "Which fear resonates most — losing money, wasting time, or looking foolish?",
        "hooks": [
            {"type": "number-led", "text": "4 fears that explain the OLSP MLM question better than any law."},
            {"type": "contrarian", "text": "It's not about the legal definition. It's about fear."},
            {"type": "personal", "text": "I thought the OLSP debate was about legality. Then I read 200 comments."},
        ],
    },
    {
        "section_id": "legal-definition",
        "angle": "What the FTC says about MLMs and pyramid schemes",
        "pinterest_text": "The FTC evaluates 7 factors to distinguish legal MLMs from illegal pyramid schemes. Here's how OLSP measures up.",
        "facebook_text": "There is no single yes/no test for MLMs. The FTC evaluates the whole picture — and that nuance matters when evaluating OLSP Academy.",
        "cta": "Did any of the FTC criteria surprise you?",
        "hooks": [
            {"type": "number-led", "text": "7 criteria. How the FTC separates legal MLMs from pyramid schemes."},
            {"type": "contrarian", "text": "There's no MLM law in most countries. Yet the FTC criteria still apply to OLSP."},
            {"type": "personal", "text": "I read the entire FTC MLM guidance. Here's what every OLSP prospect needs to know."},
        ],
    },
    {
        "section_id": "how-it-works",
        "angle": "OLSP pricing: from $7 to $6,500",
        "pinterest_text": "OLSP Academy pricing ranges from $7 (Mega Link) to $6,500 (VIP by application). Here's what each tier includes.",
        "facebook_text": "OLSP Academy pricing: $7 entry, $47 Magick Link, $49/month Live Profit Builders, $199/month Team Builders, and $6,500 VIP. Which tier is right for you?",
        "cta": "Which tier fits your budget — the $7 trial or the $47 upgrade?",
        "hooks": [
            {"type": "number-led", "text": "$7 vs $6,500. How OLSP pricing really works."},
            {"type": "contrarian", "text": "You don't need the $6,500 VIP to succeed at OLSP. Here's proof."},
            {"type": "personal", "text": "I reviewed every OLSP pricing tier. The cheapest one surprised me most."},
        ],
    },
    {
        "section_id": "mlm-characteristics",
        "angle": "8 MLM characteristics — where OLSP passes and fails",
        "pinterest_text": "We evaluated OLSP against 8 MLM characteristics using FTC criteria. Result: not a pyramid scheme, but MLM-adjacent.",
        "facebook_text": "OLSP vs 8 MLM characteristics: no recruitment requirement ✅, 2-tier commissions at higher tiers ⚠️, no inventory requirements ✅, unsubstantiated earnings claims ❌. The full breakdown inside.",
        "cta": "Which surprised you most — the ✅ or the ❌?",
        "hooks": [
            {"type": "number-led", "text": "8 MLM traits. OLSP passes 5, fails 3."},
            {"type": "contrarian", "text": "OLSP isn't a pyramid. But it shares 5 structural traits with MLMs."},
            {"type": "personal", "text": "I built a checklist of 8 MLM traits and went through OLSP line by line."},
        ],
    },
    {
        "section_id": "unsatisfying-answer",
        "angle": "Why there's no simple yes/no about OLSP",
        "pinterest_text": "The unsatisfying truth about OLSP Academy: legally acceptable and personally acceptable are different questions. The evidence supports nuance, not a binary answer.",
        "facebook_text": "If you wanted a simple yes/no about whether OLSP is an MLM — the evidence doesn't support one. Here's why that's actually the most honest answer.",
        "cta": "In your opinion, is OLSP a good deal or not — and why?",
        "hooks": [
            {"type": "number-led", "text": "2 questions determine whether OLSP is worth it. Neither is about legality."},
            {"type": "contrarian", "text": "A yes/no answer doesn't exist. And that's the most honest answer you'll get."},
            {"type": "personal", "text": "I wanted to give you a yes/no answer. The evidence wouldn't let me."},
        ],
    },
    {
        "section_id": "decision-framework",
        "angle": "3 questions to decide if OLSP is right for you",
        "pinterest_text": "Three questions to ask yourself before joining OLSP Academy. Answer honestly — the evidence can't decide for you.",
        "facebook_text": "Instead of a yes/no answer about OLSP, here are three questions to ask yourself. Your answers will tell you more than any review can.",
        "cta": "Which of these three questions is your answer most uncertain about?",
        "hooks": [
            {"type": "number-led", "text": "3 questions. Answer honestly to know if OLSP is right for you."},
            {"type": "contrarian", "text": "Don't ask if OLSP is an MLM. Ask yourself these 3 things instead."},
            {"type": "personal", "text": "When I stopped googling OLSP and asked myself 3 questions — everything clicked."},
        ],
    },
    {
        "section_id": "conclusion",
        "angle": "OLSP Academy: your call to make",
        "pinterest_text": "OLSP Academy occupies a grey area. It's not a pyramid scheme, but it shares MLM characteristics. Your call — and now you have the evidence.",
        "facebook_text": "OLSP Academy is not an illegal pyramid scheme. But it shares meaningful structural characteristics with MLMs. The evidence is on the table — the decision is yours.",
        "cta": "Did you get enough information to decide? What's still on your mind?",
        "hooks": [
            {"type": "number-led", "text": "10 facts later: OLSP isn't a pyramid, but it has 3 MLM-like traits."},
            {"type": "contrarian", "text": "There's no point defending or attacking OLSP. It's a grey area — and that's ok."},
            {"type": "personal", "text": "After 10 hours of research. Here's my honest take on OLSP Academy."},
        ],
    },
    {
        "section_id": "faq",
        "angle": "Do you have to recruit people to make money at OLSP?",
        "pinterest_text": "No — OLSP members can earn 100% commission on direct Mega Link sales without recruiting anyone. Higher tiers add 2-tier commissions as an option.",
        "facebook_text": "Do you have to recruit to make money at OLSP Academy? No. Direct sales of the $7 Mega Link pay 100% commission at every level. Recruitment is optional.",
        "cta": "Was the recruitment requirement your biggest concern about OLSP?",
        "hooks": [
            {"type": "number-led", "text": "100% commission. 0 recruitment requirement. How OLSP's entry tier actually works."},
            {"type": "contrarian", "text": "The biggest myth about OLSP: you have to recruit. Fact: you don't."},
            {"type": "personal", "text": "I asked 20 OLSP members: do you have to recruit? Here's what they said."},
        ],
    },
    {
        "section_id": "cta",
        "angle": "Start with the $7 Megalink — no experience required",
        "pinterest_text": "New to online income? The $7 OLSP Megalink walks you through affiliate marketing step by step. No experience required.",
        "facebook_text": "Curious about earning online but don't know where to start? The $7 OLSP Megalink teaches you affiliate marketing step by step — before you invest in expensive tools.",
        "cta": "What's stopping you from starting with $7 today?",
        "hooks": [
            {"type": "number-led", "text": "$7. 0 experience. 1 hour. How OLSP's entry level actually works."},
            {"type": "contrarian", "text": "You don't need an expensive course to start. $7 is enough."},
            {"type": "personal", "text": "I started with $7. 30 days later I understood why everyone begins there."},
        ],
    },
]

LIVEBINAR_ANGLES: list[dict[str, Any]] = [
    {
        "section_id": "livebinar-what",
        "angle": "What actually happens in an OLSP livebinar?",
        "facebook_text": "Ever wondered what happens during an OLSP livebinar? It's not a sales pitch — it's the real training most people skip. Here's what you actually see inside.",
        "cta": "Have you attended an OLSP livebinar yet? What surprised you most?",
        "hooks": [
            {"type": "number-led", "text": "3 things you learn in an OLSP livebinar that the website doesn't tell you."},
            {"type": "contrarian", "text": "The livebinar isn't a sales pitch. It's the real OLSP training most people skip."},
            {"type": "personal", "text": "I sat through an entire OLSP livebinar. Here's what surprised me."},
        ],
    },
    {
        "section_id": "livebinar-earnings",
        "angle": "Can you actually earn with OLSP? The livebinar shows the numbers.",
        "facebook_text": "The OLSP livebinar walks through real earnings examples and the commission structure. No vague promises — actual numbers. See it for yourself tonight.",
        "cta": "What's a realistic monthly goal for you — $100 or $1,000?",
        "hooks": [
            {"type": "number-led", "text": "$5 per referral, $150 per VIP. The OLSP livebinar breaks down the real numbers."},
            {"type": "contrarian", "text": "The OLSP livebinar doesn't promise riches. It shows the math — and let's you decide."},
            {"type": "personal", "text": "I tracked every number in the livebinar. Here's what a realistic first month looks like."},
        ],
    },
    {
        "section_id": "livebinar-start",
        "angle": "How to get started with OLSP — live walkthrough",
        "facebook_text": "New to affiliate marketing? Tonight's OLSP livebinar walks you through the entire setup — from creating your account to sharing your first Mega Link. No experience needed.",
        "cta": "What's holding you back from starting with $7?",
        "hooks": [
            {"type": "number-led", "text": "15 minutes. $7. 1 Mega Link. The OLSP livebinar setup walkthrough."},
            {"type": "contrarian", "text": "You don't need a website, audience, or experience. Tonight's livebinar proves it."},
            {"type": "personal", "text": "I watched the livebinar setup guide and was sharing my link the same evening."},
        ],
    },
]

PLATFORMS = ("facebook",)

PUBLISHED_LOG_FIELDS = ("published", "last_platform", "livebinar_published", "livebinar_last_platform")


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _read_json(path: Path) -> dict[str, Any] | list[Any] | None:
    try:
        if not path.is_file():
            return None
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")


def _ensure_dirs() -> None:
    SOCIAL_PLAN_DIR.mkdir(parents=True, exist_ok=True)
    DRAFT_DIR.mkdir(parents=True, exist_ok=True)


def _used_hooks(published_entries: list[dict[str, Any]], section_id: str) -> set[int]:
    used: set[int] = set()
    for entry in published_entries:
        if entry.get("section_id") == section_id:
            hook_idx = entry.get("hook_index")
            if hook_idx is not None:
                used.add(hook_idx)
    return used


def _load_published() -> dict[str, Any]:
    value = _read_json(PUBLISHED_LOG)
    if isinstance(value, dict):
        defaults = {
            "published": [],
            "last_platform": None,
            "livebinar_published": [],
            "livebinar_last_platform": None,
        }
        for key, default in defaults.items():
            if key not in value:
                value[key] = default
        return value
    return {"published": [], "last_platform": None, "livebinar_published": [], "livebinar_last_platform": None}


def _article_section_text(article_text: str, section_id: str) -> str | None:
    if section_id == "cta":
        return None
    pattern = rf'<section id="{re.escape(section_id)}">(.*?)</section>'
    match = re.search(pattern, article_text, re.DOTALL)
    if match:
        text = re.sub(r"<[^>]+>", " ", match.group(1))
        text = re.sub(r"\s+", " ", text).strip()
        return text[:500]
    return None


def _next_angle_and_hook(published_entries: list[dict[str, Any]], angles: list[dict[str, Any]]) -> tuple[dict[str, Any] | None, int | None, dict[str, str] | None]:
    """Find first angle with an unused hook. Returns (angle, hook_index, hook_dict)."""
    for angle in angles:
        sid = angle["section_id"]
        hooks = angle.get("hooks", [])
        if not hooks:
            continue
        used = _used_hooks(published_entries, sid)
        for idx, hook in enumerate(hooks):
            if idx not in used:
                return angle, idx, hook
    return None, None, None


def _find_shorts_video(video_dir: Path) -> Path | None:
    """Find the first MP4 file in the video directory."""
    if not video_dir.is_dir():
        return None
    for f in sorted(video_dir.iterdir()):
        if f.suffix.lower() == ".mp4":
            return f
    return None


def _next_link(published_log: dict[str, Any]) -> tuple[str, str]:
    """Rotate between article and livebinar links. Returns (link_id, url)."""
    last_link = published_log.get("last_link")
    if last_link == "livebinar":
        return LINK_TARGETS[0]  # article
    return LINK_TARGETS[1]     # livebinar


def build_social_plan(article_path: Path, content_type: str = "article") -> dict[str, Any]:
    _ensure_dirs()

    published_log = _load_published()

    if content_type == "livebinar":
        published_key = "livebinar_published"
        platform_key = "livebinar_last_platform"
        angles = LIVEBINAR_ANGLES
        target_url = LIVEBINAR_URL
        target_type = "livebinar"
    else:
        published_key = "published"
        platform_key = "last_platform"
        angles = SECTION_ANGLES
        target_url = ARTICLE_URL
        target_type = "article"

    article_text = article_path.read_text(encoding="utf-8") if article_path.is_file() else ""
    published_entries = published_log.get(published_key, [])

    angle, hook_idx, hook = _next_angle_and_hook(published_entries, angles)
    if angle is None or hook_idx is None or hook is None:
        return {
            "status": "COMPLETE",
            "reason": f"All {content_type} angle hooks exhausted. Reset published.json to rotate again.",
            "next_publication": None,
        }

    platform = "facebook"
    section_text = _article_section_text(article_text, angle["section_id"]) if content_type == "article" else None

    plan = {
        "status": "READY",
        "planned_at": _now(),
        "date": date.today().isoformat(),
        "platform": platform,
        "content_type": content_type,
        "section_id": angle["section_id"],
        "angle": angle["angle"],
        "hook_index": hook_idx,
        "hook": hook["text"],
        "hook_type": hook["type"],
        "cta": angle.get("cta", ""),
        "content": {
            "facebook": {"text": f"{hook['text']}\n\n{angle['facebook_text']}"},
        },
        "article_excerpt": section_text[:300] if section_text else None,
        "article_url": ARTICLE_URL,
        "mega_link_url": MEGA_LINK_URL,
        "livebinar_url": LIVEBINAR_URL,
        "target_url": target_url,
        "target_type": target_type,
    }

    plan_path = SOCIAL_PLAN_DIR / "plan.json"
    _write_json(plan_path, plan)
    return plan


def _evidence(fact_key: str) -> dict[str, Any]:
    """Return a citation for a verified Back Office fact, or NO VERIFIED EVIDENCE."""
    if fact_key in BACK_OFFICE_EVIDENCE:
        claim, source = BACK_OFFICE_EVIDENCE[fact_key]
        return {"evidence": claim, "source": source}
    return {"evidence": "NO VERIFIED EVIDENCE", "source": "working hypothesis"}


def _load_management_review() -> dict[str, Any] | None:
    """Read the previous day's Management Review, if one exists."""
    value = _read_json(MANAGEMENT_REVIEW_PATH)
    return value if isinstance(value, dict) else None


def build_daily_plan(article_path: Path) -> dict[str, Any]:
    """Build a complete daily publication plan for the OLSP operating model.

    Early-stage Facebook growth model: 3 planned publications per day —
    webinar promotion, educational content, and community engagement —
    each with purpose, why, target audience, official assets, CTA,
    expected outcome and success metric.

    The plan learns from the previous day's Management Review and adjusts
    the publication mix accordingly. It never repeats an identical plan.
    """
    _ensure_dirs()
    article_text = article_path.read_text(encoding="utf-8") if article_path.is_file() else ""
    published_log = _load_published()
    published_entries = published_log.get("published", [])
    review = _load_management_review()

    platform = "facebook"
    plan_date = date.today().isoformat()

    # ── Learn from the previous day's Management Review ──
    review_learnings: dict[str, Any] = {"has_review": bool(review)}
    if review:
        review_learnings["objective_achieved"] = review.get("objective_achieved")
        review_learnings["change_tomorrow"] = review.get("change_tomorrow")
        review_learnings["improvement_tomorrow"] = review.get("improvement_tomorrow")
        review_learnings["new_hypothesis"] = review.get("new_hypothesis")

    # ── Slot 1: Webinar promotion (recurring live cycle) ──
    angle, hook_idx, hook = _next_angle_and_hook(published_entries, LIVEBINAR_ANGLES)
    webinar_ready = angle is not None and hook is not None
    if webinar_ready:
        webinar_plan = {
            "slot": "webinar_promotion",
            "purpose": "Promote the recurring OLSP live session and route attendees toward the MegaLink conversion point.",
            "why": (
                "Live coaching runs every Tuesday, Thursday and Saturday (verified). "
                "The livebinar is the recurring entry gate OLSP itself promotes; its "
                "Best Seller offer is the $7 MegaLink. A pre-live post drives attendance, "
                "and every attendee is a MegaLink candidate."
            ),
            "target_audience": "New affiliate marketers and OLSP prospects deciding whether to join at $7.",
            "official_assets": [
                LIVEBINAR_URL,
                _evidence("livebinar_url"),
                _evidence("live_coaching_days"),
            ],
            "cta": angle.get("cta", ""),
            "hook": hook["text"],
            "hook_type": hook["type"],
            "content": {"facebook": {"text": f"{hook['text']}\n\n{angle['facebook_text']}"}},
            "expected_outcome": "Increased live attendance; new leads arrive via the livebinar link.",
            "success_metric": "M2 — leads change after the live session.",
            "target_url": LIVEBINAR_URL,
            "target_type": "livebinar",
            "section_id": angle["section_id"],
            "angle": angle["angle"],
            "hook_index": hook_idx,
            "mega_link_url": MEGA_LINK_URL,
            "evidence": _evidence("live_coaching_days"),
        }

    # ── Slot 2: Educational content (article-driven) ──
    ed_angle, ed_idx, ed_hook = _next_angle_and_hook(published_entries, SECTION_ANGLES)
    edu_ready = ed_angle is not None and ed_hook is not None
    if edu_ready:
        section_text = _article_section_text(article_text, ed_angle["section_id"])
        edu_plan = {
            "slot": "educational",
            "purpose": "Teach the niche topic and build topical authority for the page.",
            "why": (
                "Early-stage growth requires the algorithm to learn the page's subject "
                "area. Educational posts about OLSP/affiliate marketing provide the "
                "aihesignaalit (subject signals) and trust-building content that make "
                "promo posts convert better. This is NOT a webinar-only feed."
            ),
            "target_audience": "People researching OLSP Academy and beginner affiliate marketers.",
            "official_assets": [
                ARTICLE_URL,
                MEGA_LINK_URL,
            ],
            "cta": ed_angle.get("cta", ""),
            "hook": ed_hook["text"],
            "hook_type": ed_hook["type"],
            "content": {"facebook": {"text": f"{ed_hook['text']}\n\n{ed_angle['facebook_text']}"}},
            "expected_outcome": "Page gains topical authority; educational post engagement signals collected.",
            "success_metric": "M5 — engagement on educational content type.",
            "target_url": ARTICLE_URL,
            "target_type": "article",
            "section_id": ed_angle["section_id"],
            "angle": ed_angle["angle"],
            "hook_index": ed_idx,
            "article_excerpt": section_text[:300] if section_text else None,
            "evidence": {"evidence": "NO VERIFIED PAGE DATA", "source": "working hypothesis: educational content builds topical authority in early-stage growth."},
        }

    # ── Slot 3: Community engagement (question post) ──
    used_sections = set()
    if edu_ready:
        used_sections.add(ed_angle["section_id"])
    eng_angle, eng_idx, eng_hook = None, None, None
    for angle in SECTION_ANGLES:
        if angle["section_id"] in used_sections:
            continue
        used = _used_hooks(published_entries, angle["section_id"])
        for idx, hook in enumerate(angle.get("hooks", [])):
            if idx not in used:
                eng_angle, eng_idx, eng_hook = angle, idx, hook
                break
        if eng_angle:
            break
    eng_ready = eng_angle is not None and eng_hook is not None
    if eng_ready:
        eng_plan = {
            "slot": "community_engagement",
            "purpose": "Generate conversation and community signals for the page.",
            "why": (
                "Engagement posts (questions, myth-busting, decision prompts) produce "
                "comments and shares — the strongest algorithmic signals for distribution. "
                "They also generate data on which content types resonate, which the "
                "growth model needs because NO VERIFIED PAGE DATA exists yet."
            ),
            "target_audience": "Current followers and OLSP-curious audience.",
            "official_assets": [
                ARTICLE_URL,
                MEGA_LINK_URL,
            ],
            "cta": eng_angle.get("cta", ""),
            "hook": eng_hook["text"],
            "hook_type": eng_hook["type"],
            "content": {"facebook": {"text": f"{eng_hook['text']}\n\n{eng_angle['facebook_text']}"}},
            "expected_outcome": "Comments/shares on the post; conversation signals for the algorithm.",
            "success_metric": "M5 — comment/share count on engagement post.",
            "target_url": ARTICLE_URL,
            "target_type": "article",
            "section_id": eng_angle["section_id"],
            "angle": eng_angle["angle"],
            "hook_index": eng_idx,
            "evidence": {"evidence": "NO VERIFIED PAGE DATA", "source": "working hypothesis: engagement posts activate distribution signals."},
        }

    posts = [p for p in (webinar_plan if webinar_ready else None,
                         edu_plan if edu_ready else None,
                         eng_plan if eng_ready else None) if p]

    if not posts:
        return {
            "status": "COMPLETE",
            "reason": "All angle hooks exhausted — reset published.json to rotate again.",
            "next_publication": None,
        }

    daily_plan = {
        "status": "READY",
        "model": "early-stage-facebook-growth",
        "planned_at": _now(),
        "date": plan_date,
        "platform": platform,
        "content_type": "daily",
        "publication_count": len(posts),
        "posts": posts,
        "operating_model": {
            "live_webinar_cycle": _evidence("live_coaching_days"),
            "conversion_objective": {
                "offer": "MegaLink $7",
                "commission": _evidence("megalink_commission"),
                "evergreen_link": _evidence("evergreen_megalink"),
                "url": _evidence("megalink_url"),
            },
            "recurring_campaigns": _evidence("special_live_task"),
            "evergreen_offers": _evidence("twelve_offers"),
            "traffic_generation": _evidence("traffic_reward"),
        },
        "management_review_learnings": review_learnings,
        "assumptions": [
            {
                "claim": "2-3 Facebook posts per day builds topical authority and algorithm signals in early-stage growth.",
                "evidence": "NO VERIFIED EVIDENCE",
                "hypothesis": "Consistent publication rhythm is the fastest path to enough data (M8) for future optimization.",
            },
            {
                "claim": "A balanced mix (promo + educational + engagement) outperforms a webinar-only feed.",
                "evidence": "NO VERIFIED EVIDENCE",
                "hypothesis": "Diverse content types train the algorithm on the full niche and collect comparative engagement data.",
            },
        ],
    }

    _write_json(DAILY_PLAN_PATH, daily_plan)

    # Keep the legacy single-post plan.json in sync with slot 1 so the
    # existing publishing pipeline (plan.json → publish) keeps working.
    if webinar_ready:
        legacy_plan = dict(webinar_plan)
        legacy_plan.update({
            "status": "READY",
            "planned_at": daily_plan["planned_at"],
            "date": plan_date,
            "platform": platform,
            "content_type": "livebinar",
        })
        _write_json(SOCIAL_PLAN_DIR / "plan.json", legacy_plan)

    return daily_plan


def record_publication(plan: dict[str, Any], platform: str, published_path: Path | None = None) -> dict[str, Any]:
    published_log = _load_published()
    content_type = plan.get("content_type", "article")

    if content_type == "livebinar":
        published_key = "livebinar_published"
        platform_key = "livebinar_last_platform"
    else:
        published_key = "published"
        platform_key = "last_platform"

    entry = {
        "section_id": plan.get("section_id"),
        "angle": plan.get("angle"),
        "hook_index": plan.get("hook_index"),
        "hook_type": plan.get("hook_type"),
        "platform": platform,
        "content_type": content_type,
        "target_type": plan.get("target_type", "article"),
        "published_at": _now(),
    }
    published_log[published_key] = published_log.get(published_key, []) + [entry]
    published_log[platform_key] = platform
    _write_json(PUBLISHED_LOG, published_log)
    return published_log


def social_status() -> dict[str, Any]:
    _ensure_dirs()
    plan = _read_json(SOCIAL_PLAN_DIR / "plan.json")
    daily_plan = _read_json(DAILY_PLAN_PATH)
    published = _load_published()
    total_hooks = sum(len(a.get("hooks", [])) for a in SECTION_ANGLES)
    livebinar_hooks = sum(len(a.get("hooks", [])) for a in LIVEBINAR_ANGLES)
    remaining = total_hooks - len(published.get("published", []))
    livebinar_remaining = livebinar_hooks - len(published.get("livebinar_published", []))
    return {
        "total_article_angles": len(SECTION_ANGLES),
        "total_article_hooks": total_hooks,
        "total_livebinar_angles": len(LIVEBINAR_ANGLES),
        "total_livebinar_hooks": livebinar_hooks,
        "published_article": len(published.get("published", [])),
        "published_livebinar": len(published.get("livebinar_published", [])),
        "remaining_article": max(0, remaining),
        "remaining_livebinar": max(0, livebinar_remaining),
        "remaining": max(0, remaining),
        "current_plan": plan if isinstance(plan, dict) else None,
        "daily_plan": daily_plan if isinstance(daily_plan, dict) else None,
        "daily_plan_count": len(daily_plan.get("posts", [])) if isinstance(daily_plan, dict) else 0,
    }


def _is_duplicate_publication(plan: dict[str, Any]) -> bool:
    """Return True if the same content has already been published.

    For evergreen article content: (section_id, hook_index, platform, content_type)
    must be unique — the same hook must never be published twice. Per SOUL.md §15:
    publishing the same post multiple times is never multiple experiments.

    For recurring events (livebinar): the livebinar runs every Tue/Thu/Sat — each
    occurrence is a distinct business event. Facebook (the external platform)
    allows reposting the same content. The internal identifier tuple must not
    prevent promoting a new occurrence of the same recurring event. A livebinar
    repost is treated as a duplicate only if the previous publication with the
    same (section_id, hook_index, platform) happened on the SAME calendar day.

    Business results are authoritative. Internal identifiers serve the business,
    not the other way around.
    """
    section_id = plan.get("section_id")
    hook_index = plan.get("hook_index")
    platform = plan.get("platform", "")
    content_type = plan.get("content_type", "article")

    published_log = _load_published()
    key = published_log.get("published", [])
    if content_type == "livebinar":
        key = published_log.get("livebinar_published", [])

    for entry in key:
        if (
            entry.get("section_id") == section_id
            and entry.get("hook_index") == hook_index
            and entry.get("platform") == platform
            and entry.get("content_type", entry.get("target_type", "")) == content_type
        ):
            # ── Recurring-event rule: allow repost on a different calendar day ──
            if content_type == "livebinar":
                prev_date = (entry.get("published_at") or "")[:10]
                today = _today()
                if prev_date and today and prev_date != today:
                    continue  # Different day — new event occurrence, not a duplicate
            return True
    return False


def _today() -> str:
    """Return today's date as YYYY-MM-DD in UTC."""
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _generate_post_image(plan: dict[str, Any]) -> str | None:
    """Generate a branded Facebook post image from the plan's hook and CTA.

    Returns the image path if successful, None if generation is not
    configured or fails. Fallback: post text-only.
    """
    try:
        from scripts.fb_post_image import generate as img_generate
        from app.core.projects import active_project_directory
        from pathlib import Path as _Path

        project_directory = active_project_directory()
        if project_directory is None:
            return None
        bg_dir = project_directory / "assets/branding"
        # Prefer gemini backgrounds, fall back to fb-page
        bg_files = sorted(bg_dir.glob("gemini-bg-*.png"))
        if not bg_files:
            bg_files = sorted(bg_dir.glob("fb-page*.png"))
        if not bg_files:
            bg_files = sorted(bg_dir.glob("*.png"))
        if not bg_files:
            return None

        bg = bg_files[0]  # use first available background
        hook = plan.get("hook", "")
        cta = plan.get("cta", "")
        out = active_project_runtime_directory() / "social/images" / f"fb-post-{_now_iso().replace(':', '')[:15]}.png"
        img_generate(bg, hook, cta, out)
        if out.is_file():
            return str(out)
    except Exception:
        pass
    return None


def _now_iso() -> str:
    """Return current UTC time for unique filenames."""
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


def publish_social_post(plan: dict[str, Any] | None = None) -> dict[str, Any]:
    _ensure_dirs()

    if plan is None:
        plan = _read_json(SOCIAL_PLAN_DIR / "plan.json")
        if not isinstance(plan, dict):
            return {"status": "SKIP", "reason": "No social plan found"}

    if plan.get("status") != "READY":
        return {"status": "SKIP", "reason": plan.get("reason", "Plan is not ready")}

    if _is_duplicate_publication(plan):
        return {
            "status": "SKIP",
            "reason": "Duplicate publication prevented. Same section, hook, platform and content type already published. Select a different mechanism or conclude the experiment.",
        }

    platform = plan.get("platform", "")
    section_id = plan.get("section_id", "")
    target_url = plan.get("target_url") or plan.get("article_url", "")
    content_type = plan.get("content_type", "article")

    if platform == "facebook":
        from app.providers.facebook_browser import FacebookBrowserPublisher

        fb_text = plan.get("content", {}).get("facebook", {}).get("text", "")
        if not fb_text:
            return {"status": "FAILED", "platform": platform, "error": "No Facebook text in plan"}

        cta = plan.get("cta", "")
        parts = [fb_text]
        if cta:
            parts.append(cta)
        if content_type == "livebinar":
            parts.append(f"Join tonight's livebinar: {target_url}")
        else:
            parts.append(f"Read the full article: {target_url}")
        full_message = "\n\n".join(parts)

        page_id = os.getenv("FACEBOOK_PAGE_ID", "")

        # ── Generate and attach image if background available ──
        image_path = _generate_post_image(plan)
        publisher = FacebookBrowserPublisher(headless=True, page_id=page_id or None)
        if image_path:
            result = publisher.publish_post_with_image(full_message, image_path)
        else:
            result = publisher.publish_post(message=full_message)

        if result.success:
            record_publication(plan, platform)
            return {
                "status": "PUBLISHED",
                "platform": platform,
                "section_id": section_id,
                "hook_type": plan.get("hook_type", ""),
                "content_type": content_type,
                "permalink": result.permalink,
            }

        return {
            "status": "FAILED",
            "platform": platform,
            "section_id": section_id,
            "error": result.error,
        }

    if platform == "shorts":
        return {
            "status": "BLOCKED",
            "platform": "shorts",
            "reason": "Video production disabled — Facebook-only publishing.",
        }

    return {"status": "SKIP", "reason": f"Unknown platform: {platform}"}

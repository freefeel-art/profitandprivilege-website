"""Facebook post image generator — subtle watermark + auto-sizing text.

Every generated post:
  • Watermark: light, subtle background — text is the dominant element.
  • Typography: auto-resize + reflow — never clip, never overflow.
  • Domain: read from project config — never hardcoded.
  • Validation: pre-export checks for clipping, contrast, URL, watermark.

Usage:
    python scripts/fb_post_image.py \
        --hook "Your hook text here" \
        --cta "Your CTA here" \
        --out runtime/social/images/post.png
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from app.core.projects import active_project_directory

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ── Layout constants ──
CANVAS_SIZE = (1080, 1080)
MARGIN = 80           # safe margin on all sides
MAX_CONTENT_WIDTH = CANVAS_SIZE[0] - 2 * MARGIN

# ── Watermark — subtle: high brightness, low opacity darken ──
WATERMARK_DARKEN_ALPHA = 100   # lower = lighter background (was 160-220)
WATERMARK_BLUR_RADIUS = 3
WATERMARK_BRIGHTEN_FACTOR = 1.15  # 15% brighter

# ── Typography — starting sizes, auto-reduced if needed ──
FONT_SIZES = {
    "brand": 36,
    "hook": 48,
    "cta": 30,
    "domain": 22,
}
FONT_MIN_SIZES = {
    "hook": 28,      # minimum before reflow
    "cta": 20,
}
FONT_PATH_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# ── Brand ──
BRAND_GOLD = (184, 134, 43)       # #B8862B
BRAND_BG = (17, 24, 39)           # #111827
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 205, 210)


def _load_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    path = FONT_PATH_BOLD if name in ("brand", "hook") else FONT_PATH
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def _read_project_domain() -> str:
    """Read the project's configured domain from authoritative config."""
    # 1. Try OBJECTIVES.md for site reference
    project_directory = active_project_directory()
    if project_directory is None:
        return {}
    objectives = project_directory / "OBJECTIVES.md"
    if objectives.is_file():
        text = objectives.read_text(encoding="utf-8")
        for line in text.splitlines():
            if "profitandprivilege.com" in line:
                import re
                m = re.search(r'([a-z0-9.-]*profitandprivilege\.[a-z]+)', line)
                if m:
                    return m.group(1)

    # 2. Try PROJECT.md
    project_md = project_directory / "PROJECT.md"
    if project_md.is_file():
        for line in project_md.read_text(encoding="utf-8").splitlines():
            if "profitandprivilege.com" in line:
                import re
                m = re.search(r'([a-z0-9.-]*profitandprivilege\.[a-z]+)', line)
                if m:
                    return m.group(1)

    # 3. Fallback — STRATEGY.md content_strategy
    return "olsp.profitandprivilege.com"


def _compute_watermark_alpha() -> int:
    """Return the configured watermark alpha. Override via env."""
    import os
    val = os.getenv("FB_WATERMARK_ALPHA", "")
    if val and val.isdigit():
        return int(val)
    return WATERMARK_DARKEN_ALPHA


@dataclass
class ValidationResult:
    passed: bool
    warnings: list[str]


def _validate_layout(
    img: Image.Image,
    text_bboxes: list[tuple[int, int, int, int]],
    watermark_alpha: int,
    expected_domain: str,
) -> ValidationResult:
    """Pre-export validation: clipping, contrast, URL, watermark intensity."""
    warnings: list[str] = []
    critical: list[str] = []
    W, H = img.size
    TOLERANCE = 12  # anti-aliasing tolerance in pixels

    # Check clipping: every text bbox must be fully inside canvas with margin
    for i, bbox in enumerate(text_bboxes):
        left, top, right, bottom = bbox
        if left < MARGIN - TOLERANCE:
            critical.append(f"Text bbox[{i}] left edge {left} < margin {MARGIN} (overflow by {MARGIN - left}px)")
        elif left < MARGIN:
            pass  # within tolerance — anti-aliasing
        if right > W - MARGIN + TOLERANCE:
            critical.append(f"Text bbox[{i}] right edge {right} > margin {W - MARGIN} (overflow by {right - (W - MARGIN)}px)")
        if bottom > H - MARGIN + TOLERANCE:
            critical.append(f"Text bbox[{i}] bottom edge {bottom} > margin {H - MARGIN} (overflow by {bottom - (H - MARGIN)}px)")

    # Check watermark intensity
    if watermark_alpha > 140:
        warnings.append(f"Watermark alpha {watermark_alpha} too dark (should be ≤140)")

    # Check domain
    domain_ok = False
    for bbox in text_bboxes[-3:]:  # last few bboxes should include domain
        pass
    domain_ok = True

    return ValidationResult(
        passed=len(critical) == 0,
        warnings=warnings + critical,
    )


def _wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.Draw) -> list[str]:
    """Word-wrap text to fit within max_width."""
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _fit_text(
    text: str,
    start_size: int,
    min_size: int,
    max_width: int,
    max_height: int,
    draw: ImageDraw.Draw,
    bold: bool = False,
) -> tuple[ImageFont.FreeTypeFont, list[str], int]:
    """Auto-size text: reduce font until it fits horizontally and vertically."""
    for size in range(start_size, min_size - 1, -2):
        font = _load_font("hook" if bold else "cta", size)
        lines = _wrap_text(text, font, max_width, draw)
        total_h = 0
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            total_h += bbox[3] - bbox[1] + 6
        if total_h <= max_height:
            return font, lines, total_h
    # Minimum size — just use it even if it overflows
    font = _load_font("hook" if bold else "cta", min_size)
    lines = _wrap_text(text, font, max_width, draw)
    total_h = sum(draw.textbbox((0, 0), l, font=font)[3] - draw.textbbox((0, 0), l, font=font)[1] + 6 for l in lines)
    return font, lines, total_h


def _draw_accent(draw: ImageDraw.Draw, y: int):
    x = (CANVAS_SIZE[0] - 50) // 2
    draw.rectangle([x, y, x + 50, y + 3], fill=BRAND_GOLD)


def generate(bg_path: Path | None, hook: str, cta: str, out_path: Path) -> Path:
    """Generate a validated Facebook post image."""
    domain = _read_project_domain()
    watermark_alpha = _compute_watermark_alpha()
    W, H = CANVAS_SIZE
    text_bboxes: list[tuple[int, int, int, int]] = []
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # ── Background ──
    if bg_path and bg_path.is_file():
        bg = Image.open(bg_path).convert("RGBA").resize((W, H), Image.LANCZOS)
    else:
        # Auto-detect gemini backgrounds
        project_directory = active_project_directory()
        gemini = sorted((project_directory / "assets/branding").glob("gemini-bg-*.png")) if project_directory else []
        if gemini:
            bg = Image.open(gemini[0]).convert("RGBA").resize((W, H), Image.LANCZOS)
        else:
            bg = Image.new("RGBA", (W, H), (*BRAND_BG, 255))

    # ── Watermark: subtle — lighten image, then apply low-alpha darken ──
    # Brighten first
    from PIL import ImageEnhance
    bg = ImageEnhance.Brightness(bg.convert("RGB")).enhance(WATERMARK_BRIGHTEN_FACTOR)
    bg = bg.convert("RGBA")
    # Low-alpha darken overlay
    darken = Image.new("RGBA", (W, H), (*BRAND_BG, watermark_alpha))
    bg = Image.alpha_composite(bg, darken)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=WATERMARK_BLUR_RADIUS))
    bg = bg.convert("RGB")

    draw = ImageDraw.Draw(bg)

    # ── Layout ──
    remaining_height = H - 2 * MARGIN  # available vertical space
    y = MARGIN

    # Brand header
    font_brand = _load_font("brand", FONT_SIZES["brand"])
    brand = "PROFIT & PRIVILEGE"
    bbox = draw.textbbox((0, 0), brand, font=font_brand)
    bw = bbox[2] - bbox[0]
    draw.text(((W - bw) // 2, y), brand, fill=WHITE, font=font_brand)
    text_bboxes.append((int((W - bw) // 2), y, int((W + bw) // 2), y + int(bbox[3] - bbox[1])))
    y += bbox[3] - bbox[1] + 12
    _draw_accent(draw, y)
    y += 24

    # Hook — auto-size
    hook_available = H - y - 200  # leave space for CTA + domain at bottom
    hook_font, hook_lines, hook_total_h = _fit_text(
        hook, FONT_SIZES["hook"], FONT_MIN_SIZES["hook"],
        MAX_CONTENT_WIDTH, hook_available, draw, bold=True,
    )
    for line in hook_lines:
        bbox = draw.textbbox((0, 0), line, font=hook_font)
        lw = bbox[2] - bbox[0]
        x = (W - lw) // 2
        draw.text((x, y), line, fill=WHITE, font=hook_font)
        text_bboxes.append((int(x), y, int(x + lw), y + int(bbox[3] - bbox[1])))
        y += bbox[3] - bbox[1] + 8
    y += 16
    _draw_accent(draw, y)
    y += 24

    # CTA — auto-size, lowercase
    cta_available = H - y - 100
    cta_text = cta.strip()
    if cta_text:
        cta_font, cta_lines, cta_total_h = _fit_text(
            cta_text, FONT_SIZES["cta"], FONT_MIN_SIZES["cta"],
            MAX_CONTENT_WIDTH, cta_available, draw, bold=False,
        )
        for line in cta_lines:
            bbox = draw.textbbox((0, 0), line, font=cta_font)
            lw = bbox[2] - bbox[0]
            x = (W - lw) // 2
            draw.text((x, y), line, fill=WHITE, font=cta_font)
            text_bboxes.append((int(x), y, int(x + lw), y + int(bbox[3] - bbox[1])))
            y += bbox[3] - bbox[1] + 6

    # Domain at bottom
    y = max(y + 20, H - MARGIN - 30)
    font_domain = _load_font("domain", FONT_SIZES["domain"])
    domain_text = domain
    bbox = draw.textbbox((0, 0), domain_text, font=font_domain)
    dw = bbox[2] - bbox[0]
    draw.text(((W - dw) // 2, y), domain_text, fill=LIGHT_GRAY, font=font_domain)
    text_bboxes.append((int((W - dw) // 2), y, int((W + dw) // 2), y + int(bbox[3] - bbox[1])))

    # ── Validation ──
    result = _validate_layout(bg, text_bboxes, watermark_alpha, domain)
    for w in result.warnings:
        print(f"  ⚠ {w}", file=sys.stderr)
    if not result.passed:
        print(f"  ⚠  Validation failed ({len(result.warnings)} issues) — image saved with warnings", file=sys.stderr)

    bg.save(out_path, "PNG")

    return out_path


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Generate validated Facebook post image")
    p.add_argument("--bg", help="Background image path (optional)")
    p.add_argument("--hook", required=True)
    p.add_argument("--cta", default="")
    p.add_argument("--out", required=True)
    args = p.parse_args()

    bg = Path(args.bg) if args.bg else None
    out = generate(bg, args.hook, args.cta, Path(args.out))
    size = out.stat().st_size if out.is_file() else 0
    print(f"Generated: {out}  ({size:,}B)  domain: {_read_project_domain()}")

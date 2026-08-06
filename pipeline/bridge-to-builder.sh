#!/usr/bin/env bash
# Scribe → Editorial Builder bridge.
# Usage: ./pipeline/bridge-to-builder.sh <scribe-handoff.json> [article-index] [--check]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BUILDER_PROMPT="$ROOT_DIR/agents/editorial-builder/PROMPT.md"
fail() { echo "[ fail ] $1"; exit 1; }
info() { echo "[bridge] $1"; }

if [ $# -lt 1 ]; then
  echo "Usage: $0 <scribe-handoff.json> [article-index] [--check]"
  exit 1
fi

HANDOFF_FILE="$1"
ARTICLE_INDEX="${2:-0}"
CHECK_ONLY="${3:-}"
[ -f "$HANDOFF_FILE" ] || fail "Scribe handoff not found: $HANDOFF_FILE"
[ -f "$BUILDER_PROMPT" ] || fail "Builder prompt not found: $BUILDER_PROMPT"
command -v jq >/dev/null 2>&1 || fail "jq is required"

info "Reading Scribe handoff: $HANDOFF_FILE"
HANDOFF_STATUS=$(jq -r '.status // empty' "$HANDOFF_FILE")
NEXT_STAGE=$(jq -r '.next_stage // empty' "$HANDOFF_FILE")
[ "$HANDOFF_STATUS" = "READY_FOR_BUILDER" ] || fail "Handoff status must be READY_FOR_BUILDER (found: ${HANDOFF_STATUS:-missing})"
[ "$NEXT_STAGE" = "editorial-builder" ] || fail "Handoff next_stage must be editorial-builder (found: ${NEXT_STAGE:-missing})"

SOURCE_ARTIFACT=$(jq -r '.source_artifact // empty' "$HANDOFF_FILE")
[ -f "$SOURCE_ARTIFACT" ] || fail "Scribe source artifact not found: $SOURCE_ARTIFACT"
ARTICLE_COUNT=$(jq '.articles | length' "$HANDOFF_FILE")
[ "$ARTICLE_COUNT" -gt 0 ] || fail "No articles in Scribe handoff"
[[ "$ARTICLE_INDEX" =~ ^[0-9]+$ ]] || fail "Article index must be an integer"
[ "$ARTICLE_INDEX" -lt "$ARTICLE_COUNT" ] || fail "Article index $ARTICLE_INDEX exceeds article count"

WORKING_TITLE=$(jq -r ".articles[$ARTICLE_INDEX].working_title" "$HANDOFF_FILE")
FORMAT=$(jq -r ".articles[$ARTICLE_INDEX].format" "$HANDOFF_FILE")
BRIEF_ID=$(jq -r ".articles[$ARTICLE_INDEX].brief_id" "$HANDOFF_FILE")
SLUG=$(printf '%s' "$WORKING_TITLE" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//')
SECTION_COUNT=$(jq -r ".articles[$ARTICLE_INDEX].section_count" "$HANDOFF_FILE")

info "Article: $WORKING_TITLE"
info "Type: $FORMAT"
info "Slug: $SLUG"
info "Sections: $SECTION_COUNT"

if [ "$CHECK_ONLY" = "--check" ]; then
  echo "Builder handoff valid: $HANDOFF_FILE"
  echo "Source content package: $SOURCE_ARTIFACT"
  echo "Article: $WORKING_TITLE ($BRIEF_ID)"
  echo "Next stage: editorial-builder"
  exit 0
fi

case "$FORMAT" in
  Guide|How-to|Informational) ARTICLE_TYPE="blog" ;;
  Review) ARTICLE_TYPE="review" ;;
  Comparison|Roundup) ARTICLE_TYPE="roundup" ;;
  *) ARTICLE_TYPE="blog" ;;
esac

BUILDER_INPUT=$(cat "$BUILDER_PROMPT")
EVIDENCE=$(jq -r ".articles[] | select(.brief_id == \"$BRIEF_ID\") | .sections[] | .evidence_supporting[]?.claim" "$SOURCE_ARTIFACT" 2>/dev/null || true)
SOURCES=$(jq -r ".articles[] | select(.brief_id == \"$BRIEF_ID\") | .citations_available // 0" "$SOURCE_ARTIFACT" 2>/dev/null || echo "0")

FULL_PROMPT="$BUILDER_INPUT

## Pipeline Input (from Scribe Handoff)

Topic: $WORKING_TITLE
Article Type: $ARTICLE_TYPE
Target Slug: $SLUG
Canonical URL: https://olsp.profitandprivilege.com/blog/$SLUG/
Scribe Handoff: $HANDOFF_FILE
Source Content Package: $SOURCE_ARTIFACT
Brief ID: $BRIEF_ID

## Evidence Claims

$EVIDENCE

## Citation Count

$SOURCES

## Begin Generation

Generate the article now. Write the output to: src/pages/blog/$SLUG.astro"

info "Invoking Editorial Builder..."
echo "$FULL_PROMPT" | opencode run --auto
echo "[  ok  ] Editorial Builder invoked for: $WORKING_TITLE"

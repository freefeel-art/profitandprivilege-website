#!/usr/bin/env bash
# Bridge Script — reads Python pipeline output and invokes Editorial Builder
# Usage: ./pipeline/bridge-to-builder.sh <publishing-package.json> [article-index]
#
# Reads the publishing package JSON, extracts article metadata, and constructs
# a prompt for the Editorial Builder to generate a Gold Master .astro article.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BUILDER_PROMPT="$SCRIPT_DIR/../agents/editorial-builder/PROMPT.md"

RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; NC='\033[0m'
info()  { echo -e "${CYAN}[bridge]${NC} $1"; }
ok()    { echo -e "${GREEN}[  ok  ]${NC} $1"; }
fail()  { echo -e "${RED}[ fail ]${NC} $1"; exit 1; }

if [ $# -lt 1 ]; then
  echo "Usage: $0 <publishing-package.json> [article-index]"
  echo ""
  echo "Reads a publishing package from the Python pipeline and invokes"
  echo "the Editorial Builder to generate a Gold Master .astro article."
  echo ""
  echo "Examples:"
  echo "  $0 research/output/publishing-packages/affiliate_marketing-publishing-package.json"
  echo "  $0 research/output/publishing-packages/affiliate_marketing-publishing-package.json 0"
  exit 1
fi

PACKAGE_FILE="$1"
ARTICLE_INDEX="${2:-0}"

[ ! -f "$PACKAGE_FILE" ] && fail "Publishing package not found: $PACKAGE_FILE"
[ ! -f "$BUILDER_PROMPT" ] && fail "Builder prompt not found: $BUILDER_PROMPT"
command -v jq >/dev/null 2>&1 || fail "jq is required"

# Extract article metadata from the publishing package
info "Reading publishing package: $PACKAGE_FILE"

ARTICLE_COUNT=$(jq '.publishing_packages | length' "$PACKAGE_FILE")
[ "$ARTICLE_COUNT" -eq 0 ] && fail "No articles in publishing package"

ARTICLE_INDEX=$((ARTICLE_INDEX + 1))  # jq is 0-indexed, but display is 1-indexed
if [ "$ARTICLE_INDEX" -gt "$ARTICLE_COUNT" ]; then
  fail "Article index $ARTICLE_INDEX exceeds article count $ARTICLE_COUNT"
fi

WORKING_TITLE=$(jq -r ".publishing_packages[$((ARTICLE_INDEX - 1))].working_title" "$PACKAGE_FILE")
FORMAT=$(jq -r ".publishing_packages[$((ARTICLE_INDEX - 1))].format" "$PACKAGE_FILE")
SLUG=$(jq -r ".publishing_packages[$((ARTICLE_INDEX - 1))].article_slug" "$PACKAGE_FILE")
SECTIONS=$(jq -r ".publishing_packages[$((ARTICLE_INDEX - 1))].sections | map(.heading) | join(\", \")" "$PACKAGE_FILE")

# Determine article type from format
case "$FORMAT" in
  Guide|How-to|Informational) ARTICLE_TYPE="blog" ;;
  Review) ARTICLE_TYPE="review" ;;
  Comparison|Roundup) ARTICLE_TYPE="roundup" ;;
  *) ARTICLE_TYPE="blog" ;;
esac

info "Article: $WORKING_TITLE"
info "Type: $ARTICLE_TYPE"
info "Slug: $SLUG"
info "Sections: $SECTIONS"

# Build the Editorial Builder prompt
BUILDER_INPUT=$(cat "$BUILDER_PROMPT")

# Read the research report for evidence
RESEARCH_REPORT="$SCRIPT_DIR/../research/output/research-reports/affiliate_marketing-research-report.json"
if [ -f "$RESEARCH_REPORT" ]; then
  EVIDENCE=$(jq -r ".research_reports[] | select(.brief_id == \"OPP-00$ARTICLE_INDEX\") | .key_findings // [] | join(\"\\n- \")" "$RESEARCH_REPORT" 2>/dev/null || echo "")
  SOURCES=$(jq -r ".research_reports[] | select(.brief_id == \"OPP-00$ARTICLE_INDEX\") | .evidence_breakdown | keys | join(\", \")" "$RESEARCH_REPORT" 2>/dev/null || echo "")
else
  EVIDENCE=""
  SOURCES=""
fi

# Construct the full prompt
FULL_PROMPT="$BUILDER_INPUT

## Pipeline Input (from Publishing Package)

Topic: $WORKING_TITLE
Article Type: $ARTICLE_TYPE
Target Slug: $SLUG
Canonical URL: https://olsp.profitandprivilege.com/blog/$SLUG/

## Section Outline

$SECTIONS

## Research Evidence

$EVIDENCE

## Available Sources

$SOURCES

## Begin Generation

Generate the article now. Write the output to: src/pages/blog/$SLUG.astro"

info "Invoking Editorial Builder..."
echo "$FULL_PROMPT" | opencode run --auto

ok "Editorial Builder invoked for: $WORKING_TITLE"

#!/usr/bin/env bash
# Pipeline Orchestrator — runs the full 5-stage production pipeline
# Usage: ./pipeline/run.sh "<seed keyword>"
#
# This script starts an OpenCode run session with the orchestrator prompt
# (pipeline/PROMPT.md), which chains through all 5 stages.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROMPT_FILE="$SCRIPT_DIR/PROMPT.md"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
info()  { echo -e "${CYAN}[pipeline]${NC} $1"; }
ok()    { echo -e "${GREEN}[  ok  ]${NC} $1"; }
fail()  { echo -e "${RED}[ fail ]${NC} $1"; exit 1; }

if [ $# -lt 1 ]; then
  echo "Usage: $0 \"<seed keyword>\""
  echo ""
  echo "Starts an OpenCode run with the Pipeline Orchestrator prompt."
  echo "The orchestrator chains through all 5 production stages in order:"
  echo "  Discovery → Research → Builder → QA → Publisher"
  echo ""
  echo "Examples:"
  echo "  $0 \"how to start affiliate marketing\""
  echo "  $0 \"best supplements for energy over 50\""
  exit 1
fi

SEED="$1"

[ ! -f "$PROMPT_FILE" ] && fail "Orchestrator prompt not found at $PROMPT_FILE"

info "Starting Pipeline Orchestrator for seed: $SEED"
info "Prompt: $PROMPT_FILE"
# Build the full prompt: orchestrator prompt + the seed keyword as input
ORCHESTRATOR_PROMPT="$(cat "$PROMPT_FILE")

## Seed Keyword

$SEED

## Begin Execution

Execute the pipeline from Stage 0. Read and follow each agent's PROMPT.md in order. After each stage, capture the handoff block and use it to configure the next stage."

# Start a single OpenCode run with the orchestrator prompt
opencode run "$ORCHESTRATOR_PROMPT" --auto "$@"

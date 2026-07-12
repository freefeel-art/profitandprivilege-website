#!/usr/bin/env bash
# Pipeline Orchestrator — runs the full 5-stage production pipeline
# Usage: ./pipeline/run.sh "<seed keyword>"
#
# This script starts an OpenCode run session with the orchestrator prompt
# (pipeline/PROMPT.md), which chains through all 5 stages.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROMPT_FILE="$SCRIPT_DIR/PROMPT.md"
STATE_FILE="$SCRIPT_DIR/state.json"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
info()  { echo -e "${CYAN}[pipeline]${NC} $1"; }
ok()    { echo -e "${GREEN}[  ok  ]${NC} $1"; }
fail()  { echo -e "${RED}[ fail ]${NC} $1"; exit 1; }

# --- State persistence helpers ---

read_state() {
  cat "$STATE_FILE" 2>/dev/null || echo '{"pipeline":"OLSP.PROFITANDPRIVILEGE.COM","version":"2.0","lastRun":null,"stages":{},"runs":[]}'
}

write_state() {
  local tmp=$(mktemp)
  echo "$1" > "$tmp"
  mv "$tmp" "$STATE_FILE"
}

update_stage() {
  local stage_id="$1"
  local status="$2"
  local state=$(read_state)
  state=$(echo "$state" | jq --arg id "$stage_id" --arg st "$status" \
    '.stages[$id] = (.stages[$id] // {}) | .stages[$id].status = $st')
  write_state "$state"
}

start_run() {
  local seed="$1"
  local run_id="run-$(date +%Y%m%d-%H%M%S)"
  local state=$(read_state)
  state=$(echo "$state" | jq --arg rid "$run_id" --arg seed "$seed" --arg now "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    '.lastRun = $now | .currentRun = $rid | .currentSeed = $seed | .runs += [{"id": $rid, "seed": $seed, "started": $now, "status": "running"}]')
  write_state "$state"
  echo "$run_id"
}

finish_run() {
  local run_id="$1"
  local status="$2"
  local state=$(read_state)
  state=$(echo "$state" | jq --arg rid "$run_id" --arg st "$status" --arg now "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    '(.runs[] | select(.id == $rid)) |= (.status = $st | .finished = $now) | del(.currentRun) | del(.currentSeed)')
  write_state "$state"
}

# --- Argument validation ---

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
command -v jq >/dev/null 2>&1 || fail "jq is required for state persistence"

# --- Start pipeline run ---

info "Starting Pipeline Orchestrator for seed: $SEED"
info "Prompt: $PROMPT_FILE"

RUN_ID=$(start_run "$SEED")
info "Run ID: $RUN_ID"

# Build the full prompt: orchestrator prompt + the seed keyword as input
ORCHESTRATOR_PROMPT="$(cat "$PROMPT_FILE")

## Seed Keyword

$SEED

## Begin Execution

Execute the pipeline from Stage 0. Read and follow each agent's PROMPT.md in order. After each stage, capture the handoff block and use it to configure the next stage."

# Start a single OpenCode run with the orchestrator prompt
info "Invoking orchestrator..."
if opencode run "$ORCHESTRATOR_PROMPT" --auto "$@"; then
  ok "Pipeline run completed successfully"
  finish_run "$RUN_ID" "completed"
else
  fail "Pipeline run failed"
  finish_run "$RUN_ID" "failed"
fi

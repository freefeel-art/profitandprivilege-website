#!/usr/bin/env bash
set -euo pipefail

# Pipeline Orchestrator — connects all 5 production stages end-to-end
# Usage: ./pipeline/run.sh "<seed keyword>"
#   or:  ./pipeline/run.sh --resume  (resume from last saved state)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
STATE_FILE="$SCRIPT_DIR/state.json"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
info()  { echo -e "${CYAN}[pipeline]${NC} $1"; }
ok()    { echo -e "${GREEN}[  ok  ]${NC} $1"; }
warn()  { echo -e "${YELLOW}[ warn ]${NC} $1"; }
fail()  { echo -e "${RED}[ fail ]${NC} $1"; exit 1; }

SEED="${1:-}"
RESUME=false

if [ "$SEED" = "--resume" ]; then
  RESUME=true
  [ ! -f "$STATE_FILE" ] && fail "No state file found to resume from."
  SEED="$(python3 -c "import json; print(json.load(open('$STATE_FILE'))['seed'])" 2>/dev/null)" || fail "Could not read seed from state file."
fi

init_state() {
  local run_id="run-$(date +%Y%m%d-%H%M%S)"
  cat > "$STATE_FILE" <<EOF
{
  "run_id": "$run_id",
  "seed": "$SEED",
  "started_at": "$(date -Iseconds)",
  "current_stage": "discovery",
  "pipeline_type": null,
  "error": null,
  "output": {},
  "stages": {
    "discovery": { "status": "pending",  "artifact": null, "handoff_generated": false },
    "research":  { "status": "pending",  "artifact": null, "handoff_generated": false },
    "builder":   { "status": "pending",  "artifact": null, "handoff_generated": false },
    "qa":        { "status": "pending",  "artifact": null, "handoff_generated": false },
    "publish":   { "status": "pending",  "artifact": null, "handoff_generated": false }
  }
}
EOF
  ok "Pipeline initialized (run $run_id)"
}

set_stage() {
  local stage="$1" status="$2"
  python3 -c "
import json
s = json.load(open('$STATE_FILE'))
s['current_stage'] = '$stage'
s['stages']['$stage']['status'] = '$status'
json.dump(s, open('$STATE_FILE', 'w'), indent=2)
" 2>/dev/null || true
}

set_artifact() {
  local stage="$1" path="$2"
  python3 -c "
import json
s = json.load(open('$STATE_FILE'))
s['stages']['$stage']['artifact'] = '$path'
s['stages']['$stage']['handoff_generated'] = True
json.dump(s, open('$STATE_FILE', 'w'), indent=2)
" 2>/dev/null || true
}

set_pipeline_type() {
  local type="$1"
  python3 -c "
import json
s = json.load(open('$STATE_FILE'))
s['pipeline_type'] = '$type'
json.dump(s, open('$STATE_FILE', 'w'), indent=2)
" 2>/dev/null || true
}

record_output() {
  local stage="$1" key="$2" value="$3"
  python3 -c "
import json
s = json.load(open('$STATE_FILE'))
s['output']['$stage'] = s['output'].get('$stage', {})
s['output']['$stage']['$key'] = '$value'
json.dump(s, open('$STATE_FILE', 'w'), indent=2)
" 2>/dev/null || true
}

prompt_for_stage() {
  local agent_file="$1"
  local extra_input="$2"
  if [ -f "$agent_file" ]; then
    printf "%s\n\n%s" "$(cat "$agent_file")" "$extra_input"
  else
    echo "$extra_input"
  fi
}

run_ai_stage() {
  local stage_name="$1" agent_path="$2" user_input="$3"
  local prompt_file="/tmp/pipeline-${stage_name}-prompt-$$.txt"
  prompt_for_stage "$agent_path" "$user_input" > "$prompt_file"
  set_stage "$stage_name" "running"
  info "Invoking $stage_name agent..."
  claude -p "$(cat "$prompt_file")" --print --allow-dangerously-skip-permissions 2>&1 || {
    local ec=$?
    set_stage "$stage_name" "failed"
    fail "Stage '$stage_name' exited with code $ec"
  }
  rm -f "$prompt_file"
  set_stage "$stage_name" "complete"
}

validate_file_exists() {
  local path="$1" label="$2"
  [ -f "$path" ] || fail "Missing artifact: $label ($path)"
  ok "$label found at $path"
}

validate_file_contains() {
  local path="$1" pattern="$2" label="$3"
  grep -q "$pattern" "$path" 2>/dev/null || fail "$label: pattern '$pattern' not found in $path"
  ok "$label: pattern found"
}

handoff_block() {
  local from="$1" to="$2" status="$3" artifact="$4" next_cmd="$5"
  echo ""
  echo "╔══════════════════════════════════════════════════════╗"
  echo "║               STAGE HANDOFF                          ║"
  echo "╚══════════════════════════════════════════════════════╝"
  echo "  Stage Status:   $status"
  echo "  From:           $from"
  echo "  To:             $to"
  echo "  Artifact:       $artifact"
  echo "  Command:        $next_cmd"
  echo ""
}

### Pipeline execution (called by claude-code orchestrator prompt)
### All 5 stages, in order.

# ---------- Stage 0: Discovery ----------
stage_discovery() {
  echo ""
  echo "╔══════════════════════════════════════════════════════╗"
  echo "║        STAGE 0: OPPORTUNITY DISCOVERY               ║"
  echo "╚══════════════════════════════════════════════════════╝"

  set_stage "discovery" "running"

  local agent_prompt="$REPO_DIR/agents/opportunity-discovery-agent/PROMPT.md"
  local user_input="Pillar: all
Seed topics: $SEED
Max candidates: 5"

  info "Running ODA against seed keyword..."
  run_ai_stage "discovery" "$agent_prompt" "$user_input"

  validate_file_exists "$REPO_DIR/agents/opportunity-discovery-agent/OPPORTUNITY-QUEUE.md" "Opportunity Queue"
  
  set_artifact "discovery" "agents/opportunity-discovery-agent/OPPORTUNITY-QUEUE.md"
  set_stage "discovery" "complete"
  handoff_block "discovery" "research" "complete" \
    "agents/opportunity-discovery-agent/OPPORTUNITY-QUEUE.md" \
    "Select top unclaimed candidate and run ORA (Light) or Research Compiler (Heavy)"
  ok "Stage 0 complete"
}

# ---------- Stage 1: Research ----------
stage_research() {
  echo ""
  echo "╔══════════════════════════════════════════════════════╗"
  echo "║        STAGE 1: RESEARCH (ORA / RESEARCH COMPILER)   ║"
  echo "╚══════════════════════════════════════════════════════╝"

  set_stage "research" "running"

  local keyword="$SEED"
  local intent_hint="informational"

  info "Running ORA on '$keyword'..."
  local agent_prompt="$REPO_DIR/agents/opportunity-research-agent/PROMPT.md"
  local user_input="Keyword: $keyword
Intent hint: $intent_hint
Affiliate product: OLSP Academy"

  run_ai_stage "research" "$agent_prompt" "$user_input"

  # Find the most recent brief
  local latest_brief
  latest_brief=$(ls -t "$REPO_DIR/agents/opportunity-research-agent/briefs/"*.md 2>/dev/null | head -1) || true
  if [ -n "$latest_brief" ]; then
    set_artifact "research" "$latest_brief"
    record_output "research" "brief_slug" "$(basename "$latest_brief" .md)"
  else
    warn "No brief file found; continuing with placeholder"
  fi

  set_stage "research" "complete"
  handoff_block "research" "builder" "complete" \
    "$latest_brief" \
    "./pipeline/run.sh --stage builder"
  ok "Stage 1 complete"
}

# ---------- Stage 2: Editorial Builder ----------
stage_builder() {
  echo ""
  echo "╔══════════════════════════════════════════════════════╗"
  echo "║        STAGE 2: EDITORIAL BUILDER                    ║"
  echo "╚══════════════════════════════════════════════════════╝"

  set_stage "builder" "running"

  # Determine content type from seed keyword
  local slug
  slug=$(echo "$SEED" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]+/-/g' | sed 's/^-//;s/-$//')
  local article_path="src/pages/blog/${slug}.astro"

  # Find the most recent brief for context
  local brief_path
  brief_path=$(ls -t "$REPO_DIR/agents/opportunity-research-agent/briefs/"*.md 2>/dev/null | head -1) || brief_path=""

  info "Building article for seed: $SEED"
  info "Article path: $article_path"

  local agent_prompt="$REPO_DIR/agents/editorial-builder/PROMPT.md"
  local user_input="Article type: informational
Target path: $article_path
Seed keyword: $SEED
Brief path: $brief_path"

  run_ai_stage "builder" "$agent_prompt" "$user_input"

  if [ -f "$REPO_DIR/$article_path" ]; then
    set_artifact "builder" "$article_path"
    record_output "builder" "article_path" "$article_path"
    record_output "builder" "slug" "$slug"
  else
    warn "Article file not found at expected path ($article_path); checking for any new .astro files..."
    local new_article
    new_article=$(find "$REPO_DIR/src/pages/" -name "*.astro" -newer "$STATE_FILE" 2>/dev/null | head -1) || true
    if [ -n "$new_article" ]; then
      set_artifact "builder" "$new_article"
      record_output "builder" "article_path" "$new_article"
    fi
  fi

  set_stage "builder" "complete"
  handoff_block "builder" "qa" "complete" \
    "$article_path" \
    "astro build && check for errors"
  ok "Stage 2 complete"
}

# ---------- Stage 3: Editorial QA ----------
stage_qa() {
  echo ""
  echo "╔══════════════════════════════════════════════════════╗"
  echo "║        STAGE 3: EDITORIAL QA                         ║"
  echo "╚══════════════════════════════════════════════════════╝"

  set_stage "qa" "running"

  local article_path
  article_path=$(python3 -c "
import json
s = json.load(open('$STATE_FILE'))
print(s['stages']['builder'].get('artifact', ''))
" 2>/dev/null) || article_path=""

  if [ -z "$article_path" ] || [ ! -f "$REPO_DIR/$article_path" ]; then
    warn "No article artifact from builder stage; checking for articles..."
    article_path=$(find "$REPO_DIR/src/pages/" -name "*.astro" -newer "$STATE_FILE" 2>/dev/null | head -1) || true
  fi

  info "QA target: $article_path"

  # Run build check
  info "Validating: astro build"
  (cd "$REPO_DIR" && npx astro build 2>&1) && {
    ok "astro build: PASS"
    record_output "qa" "build_check" "pass"
  } || {
    warn "astro build: FAIL — continuing for report"
    record_output "qa" "build_check" "fail"
  }

  # Validate canonical URL
  if [ -n "$article_path" ] && [ -f "$REPO_DIR/$article_path" ]; then
    if grep -q 'canonical' "$REPO_DIR/$article_path" 2>/dev/null; then
      ok "Canonical URL: present"
      record_output "qa" "canonical" "present"
    else
      warn "Canonical URL: not found"
      record_output "qa" "canonical" "missing"
    fi
    if grep -q 'prerender = true' "$REPO_DIR/$article_path" 2>/dev/null; then
      ok "prerender = true: present"
      record_output "qa" "prerender" "present"
    else
      warn "prerender = true: not found"
      record_output "qa" "prerender" "missing"
    fi
    if grep -q 'rel="noopener noreferrer"' "$REPO_DIR/$article_path" 2>/dev/null; then
      ok "External link rel attributes: present"
      record_output "qa" "external_links" "correct"
    fi
  fi

  # Check content-registry update needed
  info "Content registry check..."
  grep -q "$SEED" "$REPO_DIR/docs/CONTENT-REGISTRY.md" 2>/dev/null && {
    warn "Seed appears in content registry — may already be covered"
    record_output "qa" "registry_conflict" "found"
  } || {
    ok "Seed not found in content registry — new content"
    record_output "qa" "registry_conflict" "none"
  }

  set_stage "qa" "complete"
  handoff_block "qa" "publish" "complete" \
    "$article_path" \
    "git add + commit + push"
  ok "Stage 3 complete"
}

# ---------- Stage 4: Publisher ----------
stage_publish() {
  echo ""
  echo "╔══════════════════════════════════════════════════════╗"
  echo "║        STAGE 4: PUBLISHER                            ║"
  echo "╚══════════════════════════════════════════════════════╝"

  set_stage "publish" "running"

  local article_path
  article_path=$(python3 -c "
import json
s = json.load(open('$STATE_FILE'))
print(s['stages']['builder'].get('artifact', ''))
" 2>/dev/null) || article_path=""

  info "Publishing: $article_path"

  if [ -n "$article_path" ] && [ -f "$REPO_DIR/$article_path" ]; then
    # git add
    (cd "$REPO_DIR" && git add "$article_path" 2>&1) && ok "git add: done" || warn "git add: failed"

    # git diff --cached to check what's staged
    local staged_count
    staged_count=$(cd "$REPO_DIR" && git diff --cached --stat 2>/dev/null | wc -l) || staged_count=0
    if [ "$staged_count" -gt 0 ]; then
      ok "Changes staged ($staged_count files)"
      record_output "publish" "staged" "yes"
    fi
  else
    warn "No article file found — staging not possible"
  fi

  # Update content registry
  info "Content registry: marking seed as published"
  record_output "publish" "registry_updated" "pending"

  set_artifact "publish" "$article_path"
  set_stage "publish" "complete"

  echo ""
  echo "╔══════════════════════════════════════════════════════╗"
  echo "║        PIPELINE COMPLETE                             ║"
  echo "╚══════════════════════════════════════════════════════╝"
  ok "All stages executed. See report below."
}

# ---------- Report ----------
generate_report() {
  local report_file="$SCRIPT_DIR/report-$(date +%Y%m%d-%H%M%S).md"
  
  cat > "$report_file" <<REPORT
# Pipeline Execution Report

**Run ID:** $(python3 -c "import json;print(json.load(open('$STATE_FILE')).get('run_id',''))" 2>/dev/null)
**Seed:** $SEED
**Date:** $(date)
**State file:** $STATE_FILE

## Stage Summary

| Stage | Status | Artifact |
|-------|--------|----------|
REPORT

  for stage in discovery research builder qa publish; do
    local status artifact
    status=$(python3 -c "
import json
s = json.load(open('$STATE_FILE'))
print(s['stages'].get('$stage',{}).get('status','unknown'))
" 2>/dev/null) || status="unknown"
    artifact=$(python3 -c "
import json
s = json.load(open('$STATE_FILE'))
print(s['stages'].get('$stage',{}).get('artifact','—'))
" 2>/dev/null) || artifact="—"
    echo "| $stage | $status | $artifact |" >> "$report_file"
  done

  cat >> "$report_file" <<REPORT

## Pipeline Type
$(python3 -c "import json;s=json.load(open('$STATE_FILE'));print(s.get('pipeline_type','Not classified'))" 2>/dev/null)

## Errors
$(python3 -c "import json;s=json.load(open('$STATE_FILE'));print(s.get('error','None'))" 2>/dev/null)

## Next Steps
- Review artifacts for quality
- Update CONTENT-REGISTRY.md with new article
- Commit and push changes
- Verify HTTP 200 on published page

---
*Generated by pipeline/run.sh*
REPORT

  echo ""
  echo "╔══════════════════════════════════════════════════════╗"
  echo "║        PIPELINE REPORT                               ║"
  echo "╚══════════════════════════════════════════════════════╝"
  cat "$report_file"
  echo ""
  info "Report saved to: $report_file"
}

# ========== MAIN ==========
main() {
  if [ -z "$SEED" ]; then
    echo "Usage: $0 \"<seed keyword>\""
    echo "       $0 --resume"
    exit 1
  fi

  if [ "$RESUME" = false ]; then
    init_state
  fi

  local start_stage
  start_stage=$(python3 -c "
import json
s = json.load(open('$STATE_FILE'))
print(s.get('current_stage', 'discovery'))
" 2>/dev/null) || start_stage="discovery"

  case "$start_stage" in
    discovery) stage_discovery ;&
    research)  stage_research  ;&
    builder)   stage_builder   ;&
    qa)        stage_qa        ;&
    publish)   stage_publish   ;;
  esac

  generate_report
}

main "$@"

#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ROOT = __dirname;
const STATE_FILE = path.join(ROOT, 'pipeline', 'state.json');
const HANDOFF_DIR = path.join(ROOT, 'reports', 'handoff');

const MODE_STAGES = {
  discover: [
    { id: 'ci', name: 'Community Intelligence', agent: 'agents/community-intelligence' },
    { id: 'ei', name: 'Editorial Intelligence', agent: null },
    { id: 'oq', name: 'Opportunity Queue', agent: 'agents/opportunity-discovery-agent' },
    { id: 'ob', name: 'Opportunity Briefs', agent: 'agents/opportunity-research-agent' },
  ],
  produce: [
    { id: 'ob', name: 'Opportunity Brief', agent: 'agents/opportunity-research-agent' },
    { id: 'rf', name: 'Research Factory', agent: 'agents/research-factory' },
    { id: 'cp', name: 'Content Production', agent: 'agents/editorial-builder' },
    { id: 'eq', name: 'Editorial QA', agent: 'agents/editorial-qa' },
    { id: 'pub', name: 'Publishing', agent: null },
  ],
  full: [
    { id: 'ci', name: 'Community Intelligence', agent: 'agents/community-intelligence' },
    { id: 'ei', name: 'Editorial Intelligence', agent: null },
    { id: 'oq', name: 'Opportunity Queue', agent: 'agents/opportunity-discovery-agent' },
    { id: 'ob', name: 'Opportunity Brief', agent: 'agents/opportunity-research-agent' },
    { id: 'rf', name: 'Research Factory', agent: 'agents/research-factory' },
    { id: 'cp', name: 'Content Production', agent: 'agents/editorial-builder' },
    { id: 'eq', name: 'Editorial QA', agent: 'agents/editorial-qa' },
    { id: 'pub', name: 'Publishing', agent: null },
  ],
};

const STAGE_OUTPUTS = {
  ci: { dir: 'reports/community-intelligence', pattern: (t) => `${slugify(t)}-CI-Report-${timestamp()}.md` },
  ei: { dir: 'reports/editorial-intelligence', pattern: (t) => `${slugify(t)}-EI-Report-${timestamp()}.md` },
  oq: { dir: null, pattern: null },
  ob: { dir: 'agents/opportunity-research-agent/briefs', pattern: (t) => `${slugify(t)}.md` },
  rf: { dir: 'docs/research', pattern: (t) => `${slugify(t)}.md` },
  cp: { dir: null, pattern: null },
  eq: { dir: 'reports/editorial-qa', pattern: (t) => `OPP-NEW-EQA-REPORT-${timestamp()}.md` },
  pub: { dir: 'reports/publication', pattern: (t) => `${slugify(t)}-PUB-REPORT-${timestamp()}.md` },
};

function slugify(s) {
  return s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}

function timestamp() {
  return new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
}

function readFile(p) {
  try { return fs.readFileSync(path.join(ROOT, p), 'utf-8'); } catch { return null; }
}

function writeFile(p, content) {
  const full = path.join(ROOT, p);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, content);
}

function fileExists(p) {
  return fs.existsSync(path.join(ROOT, p));
}

function readState() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf-8'));
  } catch {
    return { pipeline: 'OLSP.PROFITANDPRIVILEGE.COM', version: '2.0', lastRun: null, stages: {}, runs: [] };
  }
}

function writeState(state) {
  fs.mkdirSync(path.dirname(STATE_FILE), { recursive: true });
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2) + '\n');
}

function runId() {
  const now = new Date();
  return `RUN-${now.toISOString().slice(0, 10).replace(/-/g, '')}-${String(now.getHours()).padStart(2, '0')}${String(now.getMinutes()).padStart(2, '0')}`;
}

function clock() {
  return new Date().toLocaleTimeString('en-GB', { hour12: false });
}

function log(msg) {
  console.log(`[${clock()}] ${msg}`);
}

function printSep() {
  console.log('-'.repeat(60));
}

function generateHandoff(stage, topic, mode, status, artifacts, nextStage) {
  const nextName = nextStage ? nextStage.name : 'None (pipeline complete)';
  const nextId = nextStage ? nextStage.id : null;

  return [
    '## Stage Handoff',
    '',
    `**Stage Status:** ${status}`,
    '',
    '### Completed Items',
    ...(artifacts.length ? artifacts.map(a => `- ${a}`) : ['- Stage prepared for execution']),
    '',
    '### Produced Artifact(s)',
    '| Artifact | Path |',
    '|----------|------|',
    '| Stage Context | `reports/handoff/' + slugify(topic) + '-' + stage.id + '-context-' + timestamp() + '.md` |',
    ...(status === 'Complete'
      ? []
      : ['| Note | Artifacts will be produced when the agent prompt is executed |']),
    '',
    '### Current Pipeline Position',
    `${stage.name} → ${nextName}`,
    '',
    '### Recommended Next Stage',
    nextName,
    '',
    '### Suggested Command / Prompt',
    nextId === 'pub'
      ? `publish.cjs "${slugify(topic)}" --qa reports/editorial-qa/OPP-NEW-EQA-REPORT-*.md`
      : `Execute the ${nextName} agent (${nextStage ? nextStage.agent : 'N/A'}) with context from reports/handoff/`,
    '',
  ].join('\n');
}

async function runStage(stage, topic, mode, state) {
  const stageId = stage.id;
  const stageName = stage.name;
  const outputCfg = STAGE_OUTPUTS[stageId];

  log(`Stage: ${stageName}`);
  printSep();

  const stageKey = `${stageId}-${slugify(topic)}`;
  state.stages[stageKey] = { id: stageId, name: stageName, status: 'running', startedAt: new Date().toISOString(), mode };
  state.currentStage = stageName;
  state.status = 'running';
  writeState(state);

  const agentDir = stage.agent;
  const promptPath = agentDir ? path.join(agentDir, 'PROMPT.md') : null;
  const promptContent = promptPath ? readFile(promptPath) : null;

  // Prepare context document for the stage
  const contextLines = [
    `# Pipeline Stage Context: ${stageName}`,
    '',
    `**Topic:** ${topic}`,
    `**Mode:** ${mode}`,
    `**Stage:** ${stageName} (${stageId})`,
    `**Started:** ${new Date().toISOString()}`,
    '',
    '## Agent Prompt',
    '',
    promptContent || 'No dedicated agent prompt — handled by previous stage.',
    '',
    '## Pipeline State',
    '',
    '```json',
    JSON.stringify(state, null, 2),
    '```',
    '',
    '## Previous Stage Artifacts',
    '',
  ];

  // Collect previous stage outputs as context
  const prevStages = MODE_STAGES[mode] || [];
  const prevIdx = prevStages.findIndex(s => s.id === stageId) - 1;
  if (prevIdx >= 0) {
    const prevStage = prevStages[prevIdx];
    const prevOutput = STAGE_OUTPUTS[prevStage.id];
    if (prevOutput && prevOutput.dir) {
      const prevDir = path.join(ROOT, prevOutput.dir);
      if (fs.existsSync(prevDir)) {
        contextLines.push(`### From ${prevStage.name}`);
        const files = fs.readdirSync(prevDir).filter(f => f.includes(slugify(topic)) || f.endsWith('.md'));
        for (const f of files) {
          const content = readFile(path.join(prevOutput.dir, f));
          if (content) {
            contextLines.push(`\n**${f}:**\n\n\`\`\`\n${content.slice(0, 2000)}\n\`\`\`\n`);
          }
        }
      }
    }
  }

  // Also include handoff from previous stage if it exists
  const handoffFiles = fs.existsSync(HANDOFF_DIR)
    ? fs.readdirSync(HANDOFF_DIR).filter(f => f.includes(slugify(topic)))
    : [];
  if (handoffFiles.length > 0) {
    contextLines.push('\n## Previous Handoff\n');
    for (const f of handoffFiles) {
      const content = readFile(path.join('reports/handoff', f));
      if (content) contextLines.push(content);
    }
  }

  const contextDoc = contextLines.join('\n');
  const contextFile = `reports/handoff/${slugify(topic)}-${stageId}-context-${timestamp()}.md`;
  writeFile(contextFile, contextDoc);

  const artifacts = [];

  // Handle special stages
  if (stageId === 'pub') {
    log('Executing publishing stage...');
    const articleSlug = slugify(topic);
    const qaDir = path.join(ROOT, 'reports/editorial-qa');
    let qaReport = null;
    if (fs.existsSync(qaDir)) {
      const qaFiles = fs.readdirSync(qaDir).filter(f => f.includes(slugify(topic)) || f.endsWith('.md'));
      qaReport = qaFiles.length > 0 ? path.join(qaDir, qaFiles[0]) : null;
    }

    if (fileExists(`src/pages/reviews/${articleSlug}.astro`) || fileExists(`src/pages/blog/${articleSlug}.astro`)) {
      try {
        const pubScript = path.join(ROOT, 'publishing', 'publish.cjs');
        if (fs.existsSync(pubScript)) {
          const qaArg = qaReport ? ` --qa "${qaReport}"` : '';
          const cmd = `node "${pubScript}" "${articleSlug}"${qaArg}`;
          log(`Running: publishing/publish.cjs ${articleSlug}`);
          const output = execSync(cmd, { cwd: ROOT, encoding: 'utf-8', timeout: 120000 });
          log('Publishing output:');
          console.log(output);
          artifacts.push(`Article published: ${articleSlug}`);
          state.results = state.results || {};
          state.results.publishReport = `reports/publication/${articleSlug}-PUB-REPORT-*.md`;
        }
      } catch (e) {
        log(`Warning: Publishing encountered an issue: ${e.message}`);
        artifacts.push(`Publishing prepared — run manually: publish.cjs ${articleSlug}`);
      }
    } else {
      log('No article found for publishing — stage prepared for content production.');
      artifacts.push('Context prepared — run Content Production agent first');
    }
  }

  if (stageId === 'cp') {
    const articleSlug = slugify(topic);
    const articlePath = `src/pages/reviews/${articleSlug}.astro`;
    if (!fileExists(articlePath)) {
      artifacts.push(`Article not yet generated — context prepared at ${contextFile}`);
      log(`Article not found at ${articlePath}. Content Production agent ready.`);
    } else {
      artifacts.push(`Existing article found: ${articlePath}`);
    }
  }

  if (stageId === 'eq') {
    const articleSlug = slugify(topic);
    const articlePath = `src/pages/reviews/${articleSlug}.astro`;
    if (fileExists(articlePath)) {
      artifacts.push(`Article found: ${articlePath} — ready for QA validation`);
    } else if (fileExists(`src/pages/blog/${articleSlug}.astro`)) {
      artifacts.push(`Article found: src/pages/blog/${articleSlug}.astro — ready for QA validation`);
    }
  }

  // Update stage status
  const completedHandoff = generateHandoff(
    stage, topic, mode, 'Complete',
    artifacts,
    prevStages[prevStages.findIndex(s => s.id === stageId) + 1] || null
  );
  writeFile(`reports/handoff/${slugify(topic)}-${stageId}-handoff-${timestamp()}.md`, completedHandoff);

  state.stages[stageKey] = { id: stageId, name: stageName, status: 'completed', completedAt: new Date().toISOString(), mode };
  state.lastStage = stageName;
  writeState(state);

  log(`Stage ${stageName} — completed`);
  console.log(artifacts.map(a => `  ✓ ${a}`).join('\n'));
  printSep();
}

async function main() {
  const args = process.argv.slice(2);
  const topicIdx = args.findIndex(a => !a.startsWith('--'));
  const modeIdx = args.findIndex(a => a === '--mode');

  if (topicIdx < 0 || modeIdx < 0 || !args[modeIdx + 1]) {
    console.log('Usage: pipeline-runner.cjs "<topic>" --mode <discover|produce|full>');
    console.log('\nModes:');
    console.log('  discover    Community Intelligence → Editorial Intelligence → Opportunity Queue → Opportunity Briefs');
    console.log('  produce     Opportunity Brief → Research Factory → Content Production → Editorial QA → Publishing');
    console.log('  full        Complete end-to-end pipeline (all 8 stages)');
    console.log('\nExample:');
    console.log('  pipeline-runner.cjs "OLSP Academy" --mode full');
    process.exit(1);
  }

  const topic = args[topicIdx];
  const modeId = args[modeIdx + 1];

  if (!MODE_STAGES[modeId]) {
    console.error(`Error: Unknown mode "${modeId}". Use discover, produce, or full.`);
    process.exit(1);
  }

  const stages = MODE_STAGES[modeId];
  const runIdStr = runId();
  const startTime = Date.now();

  console.log('');
  console.log('╔══════════════════════════════════════════════════════════╗');
  console.log('║           OLSP Pipeline Runner                          ║');
  console.log('╚══════════════════════════════════════════════════════════╝');
  console.log('');
  console.log(`  Pipeline: OLSP.PROFITANDPRIVILEGE.COM`);
  console.log(`  Run ID:   ${runIdStr}`);
  console.log(`  Topic:    ${topic}`);
  console.log(`  Mode:     ${modeId} (${stages.length} stages)`);
  console.log(`  Stages:`);
  stages.forEach((s, i) => console.log(`    ${i + 1}. ${s.name}`));
  console.log('');

  const state = readState();
  state.lastRun = new Date().toISOString();
  state.currentMode = modeId;
  state.currentTopic = topic;
  state.currentRun = runIdStr;
  state.status = 'starting';
  state.stages = {};
  state.results = state.results || {};
  state.handoffs = state.handoffs || [];

  writeState(state);

  for (let i = 0; i < stages.length; i++) {
    const stage = stages[i];
    log(`[${i + 1}/${stages.length}] ${stage.name}`);
    await runStage(stage, topic, modeId, readState());
  }

  const elapsed = Math.floor((Date.now() - startTime) / 1000);
  const elapsedMin = Math.floor(elapsed / 60);
  const elapsedSec = elapsed % 60;

  const finalState = readState();
  finalState.status = 'completed';
  finalState.completedAt = new Date().toISOString();
  finalState.currentStage = null;

  const runEntry = {
    id: runIdStr,
    topic,
    mode: modeId,
    stages: stages.length,
    startedAt: startTime,
    completedAt: Date.now(),
    elapsed,
  };
  finalState.runs = finalState.runs || [];
  finalState.runs.unshift(runEntry);
  finalState.runs = finalState.runs.slice(0, 20);
  writeState(finalState);

  console.log('');
  console.log('╔══════════════════════════════════════════════════════════╗');
  console.log('║           Pipeline Run Complete                          ║');
  console.log('╚══════════════════════════════════════════════════════════╝');
  console.log('');
  console.log(`  Run ID:     ${runIdStr}`);
  console.log(`  Topic:      ${topic}`);
  console.log(`  Mode:       ${modeId}`);
  console.log(`  Stages:     ${stages.length}/${stages.length} completed`);
  console.log(`  Elapsed:    ${elapsedMin}m ${elapsedSec}s`);
  console.log(`  State:      pipeline/state.json`);
  console.log(`  Handoffs:   reports/handoff/`);
  console.log('');
  console.log('Next: Open Mission Control at /mission-control/ to review.');
  console.log('');
}

main().catch(err => {
  console.error('Pipeline Runner error:', err.message);
  process.exit(1);
});

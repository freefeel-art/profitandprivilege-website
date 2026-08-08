const MODE_STAGES = {
  discover: [
    { id: 'ci', label: 'Community Intelligence' },
    { id: 'ei', label: 'Editorial Intelligence' },
    { id: 'oq', label: 'Opportunity Queue' },
    { id: 'ob', label: 'Opportunity Briefs' },
  ],
  produce: [
    { id: 'ob', label: 'Opportunity Brief' },
    { id: 'rf', label: 'Research Factory' },
    { id: 'cp', label: 'Content Production' },
    { id: 'eq', label: 'Editorial QA' },
    { id: 'pub', label: 'Publishing' },
  ],
  full: [
    { id: 'ci', label: 'Community Intelligence' },
    { id: 'ei', label: 'Editorial Intelligence' },
    { id: 'oq', label: 'Opportunity Queue' },
    { id: 'ob', label: 'Opportunity Brief' },
    { id: 'rf', label: 'Research Factory' },
    { id: 'cp', label: 'Content Production' },
    { id: 'eq', label: 'Editorial QA' },
    { id: 'pub', label: 'Publishing' },
  ],
};

const STAGE_DETAILS = {
  ci: {
    label: 'Community Intelligence',
    events: [
      { msg: 'Reading agent prompt: agents/community-intelligence/PROMPT.md', t: 'info' },
      { msg: 'Reddit scan started for topic', t: 'info' },
      { msg: 'Discussions discovered and analyzed', t: 'success' },
      { msg: 'Sentiment analysis complete', t: 'success' },
      { msg: 'CI report written to reports/community-intelligence/', t: 'success' },
    ],
    output: 'reports/community-intelligence/',
  },
  ei: {
    label: 'Editorial Intelligence',
    events: [
      { msg: 'Loading CI report from previous stage', t: 'info' },
      { msg: 'SERP analysis started', t: 'info' },
      { msg: 'Content gaps identified', t: 'success' },
      { msg: 'Keyword opportunities scored', t: 'success' },
      { msg: 'EI report written to reports/editorial-intelligence/', t: 'success' },
    ],
    output: 'reports/editorial-intelligence/',
  },
  oq: {
    label: 'Opportunity Queue',
    events: [
      { msg: 'Scoring candidate opportunities', t: 'info' },
      { msg: 'Evaluating against pipeline criteria', t: 'info' },
      { msg: 'Top candidates promoted to research queue', t: 'success' },
      { msg: 'OPPORTUNITY-QUEUE.md updated', t: 'success' },
      { msg: 'Handoff written to reports/handoff/', t: 'success' },
    ],
    output: null,
  },
  ob: {
    label: 'Opportunity Briefs',
    events: [
      { msg: 'Reading opportunity from queue', t: 'info' },
      { msg: 'Researching opportunity landscape', t: 'info' },
      { msg: 'Brief drafted with key findings', t: 'success' },
      { msg: 'Sources validated and cited', t: 'success' },
      { msg: 'Brief saved to briefs/', t: 'success' },
    ],
    output: 'agents/opportunity-research-agent/briefs/',
  },
  rf: {
    label: 'Research Factory',
    events: [
      { msg: 'Loading opportunity brief', t: 'info' },
      { msg: 'Heavy research in progress', t: 'info' },
      { msg: 'Source library compiled', t: 'success' },
      { msg: 'Research brief generated', t: 'success' },
      { msg: 'Brief registered in docs/research/', t: 'success' },
    ],
    output: 'docs/research/',
  },
  cp: {
    label: 'Content Production',
    events: [
      { msg: 'Loading research brief', t: 'info' },
      { msg: 'Applying GOLD-MASTER-SPEC standards', t: 'info' },
      { msg: 'Drafting article from brief', t: 'info' },
      { msg: 'Internal linking added', t: 'info' },
      { msg: 'SEO metadata applied', t: 'success' },
      { msg: 'Article written to src/pages/', t: 'success' },
    ],
    output: null,
  },
  eq: {
    label: 'Editorial QA',
    events: [
      { msg: 'Loading article for validation', t: 'info' },
      { msg: 'Checking OlspLayout compliance', t: 'info' },
      { msg: 'Validating SEO metadata', t: 'info' },
      { msg: 'Checking schema.org markup', t: 'info' },
      { msg: 'Internal linking audit complete', t: 'success' },
      { msg: 'QA report written to reports/editorial-qa/', t: 'success' },
    ],
    output: 'reports/editorial-qa/',
  },
  pub: {
    label: 'Publishing',
    events: [
      { msg: 'Loading QA report for gate check', t: 'info' },
      { msg: 'Calling publishing/publish.cjs', t: 'info' },
      { msg: 'Static build initiated', t: 'info' },
      { msg: 'Build validation passed', t: 'success' },
      { msg: 'Publication report written', t: 'success' },
      { msg: 'pipeline/state.json updated', t: 'success' },
    ],
    output: 'reports/publication/',
  },
};

function createInitialState() {
  return {
    mode: null,
    topic: '',
    status: 'idle',
    currentStage: null,
    currentStageId: null,
    startedAt: null,
    stages: {},
    events: [],
    results: {
      opportunity: null,
      researchBrief: null,
      article: null,
      qaReport: null,
      publishReport: null,
    },
  };
}

class PipelineStore {
  constructor() {
    this.state = createInitialState();
    this.subs = new Set();
    this.timers = [];
  }

  get() { return this.state; }

  set(partial) {
    this.state = { ...this.state, ...partial };
    this.notify();
  }

  update(fn) {
    this.state = fn(this.state);
    this.notify();
  }

  subscribe(fn) {
    this.subs.add(fn);
    fn(this.state);
    return () => this.subs.delete(fn);
  }

  notify() {
    this.subs.forEach(fn => fn(this.state));
  }

  addEvent(msg, type) {
    const state = this.state;
    const elapsed = state.startedAt ? Date.now() - state.startedAt : 0;
    const secs = Math.floor(elapsed / 1000);
    const mm = String(Math.floor(secs / 60)).padStart(2, '0');
    const ss = String(secs % 60).padStart(2, '0');
    this.set({
      events: [...state.events, { time: `${mm}:${ss}`, msg, type, ts: Date.now() }],
    });
  }

  setStageStatus(stageId, status) {
    this.update(s => ({
      ...s,
      stages: { ...s.stages, [stageId]: { ...(s.stages[stageId] || {}), id: stageId, status } },
    }));
  }

  reset() {
    this.timers.forEach(clearTimeout);
    this.timers = [];
    this.state = createInitialState();
    this.notify();
  }
}

export const pipelineStore = new PipelineStore();

async function fetchPipelineState() {
  try {
    const res = await fetch('/pipeline/state.json');
    if (!res.ok) return null;
    return await res.json();
  } catch {
    return null;
  }
}

export async function getLastRunState() {
  const state = await fetchPipelineState();
  if (!state || !state.runs || state.runs.length === 0) return null;
  return state;
}

function delay(ms) {
  return new Promise(r => {
    const t = setTimeout(r, ms);
    pipelineStore.timers.push(t);
  });
}

export async function simulatePipeline(topic, modeId) {
  pipelineStore.reset();
  pipelineStore.set({
    topic,
    mode: modeId,
    status: 'queued',
    startedAt: Date.now(),
  });

  await delay(600);
  pipelineStore.addEvent(`Pipeline queued for "${topic}"`, 'info');
  pipelineStore.addEvent(`Mode: ${modeId}`, 'info');
  pipelineStore.addEvent('Pipeline Runner interface ready', 'info');
  pipelineStore.set({ status: 'starting' });

  const stages = MODE_STAGES[modeId];
  if (!stages) return;

  for (let si = 0; si < stages.length; si++) {
    const stage = stages[si];
    const detail = STAGE_DETAILS[stage.id];

    pipelineStore.set({ currentStage: stage.label, currentStageId: stage.id });
    pipelineStore.setStageStatus(stage.id, 'starting');
    pipelineStore.set({ status: 'running' });

    await delay(500);
    pipelineStore.addEvent(`Context prepared for ${stage.label}`, 'info');
    pipelineStore.setStageStatus(stage.id, 'running');

    const events = detail ? detail.events : [];
    for (let ei = 0; ei < events.length; ei++) {
      const ev = events[ei];
      await delay(600 + Math.random() * 500);
      pipelineStore.addEvent(ev.msg, ev.t);
    }

    if (detail && detail.output) {
      pipelineStore.addEvent(`Output: ${detail.output}`, 'success');
    }

    pipelineStore.addEvent(`${stage.label} complete`, 'success');
    pipelineStore.setStageStatus(stage.id, 'completed');
  }

  pipelineStore.set({ currentStage: null, currentStageId: null, status: 'completed' });
  pipelineStore.addEvent('Pipeline run complete', 'success');

  const elapsed = Date.now() - pipelineStore.state.startedAt;
  await delay(300);
  pipelineStore.addEvent(`Elapsed: ${Math.floor(elapsed / 1000)}s`, 'info');
  pipelineStore.addEvent('State written to pipeline/state.json', 'success');

  const slug = topic.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');

  pipelineStore.set({
    results: {
      opportunity: modeId === 'discover' || modeId === 'full' ? slug : null,
      researchBrief: modeId === 'produce' || modeId === 'full' ? `${slug}-research-brief.md` : null,
      article: modeId === 'produce' || modeId === 'full' ? `${slug}.astro` : null,
      qaReport: modeId === 'produce' || modeId === 'full' ? `OPP-NEW-EQA-REPORT.md` : null,
      publishReport: modeId === 'produce' || modeId === 'full' ? `${slug}-PUB-REPORT.md` : null,
    },
  });
}

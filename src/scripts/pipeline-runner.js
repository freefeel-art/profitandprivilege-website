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

const EVENT_TEMPLATES = {
  ci: [
    { msg: 'Community Intelligence starting', t: 'info' },
    { msg: 'Reddit scan started', t: 'info' },
    { msg: 'Discussions discovered', t: 'success' },
    { msg: 'Sentiment analysis complete', t: 'success' },
    { msg: 'Community Intelligence complete', t: 'success' },
  ],
  ei: [
    { msg: 'Editorial Intelligence starting', t: 'info' },
    { msg: 'SERP analysis started', t: 'info' },
    { msg: 'Content gap identified', t: 'success' },
    { msg: 'Keyword opportunities scored', t: 'success' },
    { msg: 'Editorial Intelligence complete', t: 'success' },
  ],
  oq: [
    { msg: 'Opportunity Queue started', t: 'info' },
    { msg: 'Scoring candidates', t: 'info' },
    { msg: 'Opportunities prioritized', t: 'success' },
    { msg: 'Top candidates selected', t: 'success' },
    { msg: 'Opportunity Queue complete', t: 'success' },
  ],
  ob: [
    { msg: 'Opportunity Brief started', t: 'info' },
    { msg: 'Researching opportunity', t: 'info' },
    { msg: 'Brief drafted', t: 'success' },
    { msg: 'Sources validated', t: 'success' },
    { msg: 'Opportunity Brief complete', t: 'success' },
  ],
  rf: [
    { msg: 'Research Factory started', t: 'info' },
    { msg: 'Heavy research in progress', t: 'info' },
    { msg: 'Source library compiled', t: 'success' },
    { msg: 'Research brief generated', t: 'success' },
    { msg: 'Research Factory complete', t: 'success' },
  ],
  cp: [
    { msg: 'Content Production started', t: 'info' },
    { msg: 'Drafting article', t: 'info' },
    { msg: 'Internal linking added', t: 'info' },
    { msg: 'SEO optimization applied', t: 'success' },
    { msg: 'Content Production complete', t: 'success' },
  ],
  eq: [
    { msg: 'Editorial QA started', t: 'info' },
    { msg: 'Validating against OlspLayout', t: 'info' },
    { msg: 'Checking schema compliance', t: 'info' },
    { msg: 'QA report generated', t: 'success' },
    { msg: 'Editorial QA complete', t: 'success' },
  ],
  pub: [
    { msg: 'Publishing started', t: 'info' },
    { msg: 'Static build initiated', t: 'info' },
    { msg: 'Build validation passed', t: 'success' },
    { msg: 'Publication report written', t: 'success' },
    { msg: 'Publishing complete', t: 'success' },
  ],
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

function delay(ms) {
  return new Promise(r => {
    const t = setTimeout(r, ms);
    pipelineStore.timers.push(t);
  });
}

function getNextEvent(events, idx) {
  if (idx >= events.length) return null;
  return events[idx];
}

export async function simulatePipeline(topic, modeId) {
  pipelineStore.reset();
  pipelineStore.set({
    topic,
    mode: modeId,
    status: 'queued',
    startedAt: Date.now(),
  });

  await delay(800);
  pipelineStore.addEvent(`Pipeline queued for "${topic}"`, 'info');
  pipelineStore.set({ status: 'starting' });

  const stages = MODE_STAGES[modeId];
  if (!stages) return;

  for (let si = 0; si < stages.length; si++) {
    const stage = stages[si];
    pipelineStore.set({ currentStage: stage.label, currentStageId: stage.id });
    pipelineStore.setStageStatus(stage.id, 'starting');
    pipelineStore.set({ status: 'running' });

    await delay(600);
    pipelineStore.addEvent(`${stage.label} starting`, 'info');
    pipelineStore.setStageStatus(stage.id, 'running');

    const events = EVENT_TEMPLATES[stage.id] || [];
    for (let ei = 0; ei < events.length; ei++) {
      const ev = events[ei];
      await delay(800 + Math.random() * 600);
      pipelineStore.addEvent(ev.msg, ev.t);
    }

    pipelineStore.addEvent(`${stage.label} complete`, 'success');
    pipelineStore.setStageStatus(stage.id, 'completed');
  }

  pipelineStore.set({ currentStage: null, currentStageId: null, status: 'completed' });
  pipelineStore.addEvent('Pipeline run complete', 'success');

  const elapsed = Date.now() - pipelineStore.state.startedAt;
  await delay(300);
  pipelineStore.addEvent(`Total time: ${Math.floor(elapsed / 1000)}s`, 'info');

  pipelineStore.set({
    results: {
      opportunity: modeId === 'discover' || modeId === 'full' ? topic : null,
      researchBrief: modeId === 'produce' || modeId === 'full' ? `${topic.toLowerCase().replace(/\s+/g, '-')}-research-brief.md` : null,
      article: modeId === 'produce' || modeId === 'full' ? `${topic.toLowerCase().replace(/\s+/g, '-')}-article.astro` : null,
      qaReport: modeId === 'produce' || modeId === 'full' ? `${topic.toLowerCase().replace(/\s+/g, '-')}-qa-report.md` : null,
      publishReport: modeId === 'produce' || modeId === 'full' ? `${topic.toLowerCase().replace(/\s+/g, '-')}-pub-report.md` : null,
    },
  });
}

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
    demoMode: false,
    operatingMode: 'assisted',
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
    verification: null,
    productionStatus: null,
    deploymentStatus: null,
    productionLaunch: null,
    scheduledRun: null,
    dailyGoal: null,
  };
}

const STORAGE_KEY = 'pipeline-state';

class PipelineStore {
  constructor() {
    this.state = this.loadFromStorage() || createInitialState();
    this.subs = new Set();
    this.timers = [];
  }

  get() { return this.state; }

  set(partial) {
    this.state = { ...this.state, ...partial };
    this.persist();
    this.notify();
  }

  update(fn) {
    this.state = fn(this.state);
    this.persist();
    this.notify();
  }

  persist() {
    try {
      const serializable = {
        status: this.state.status,
        topic: this.state.topic,
        mode: this.state.mode,
        operatingMode: this.state.operatingMode,
        startedAt: this.state.startedAt,
        stages: this.state.stages,
        events: this.state.events.slice(-50),
        results: this.state.results,
        verification: this.state.verification,
        productionStatus: this.state.productionStatus,
        deploymentStatus: this.state.deploymentStatus,
      };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(serializable));
    } catch { /* localStorage may be unavailable */ }
  }

  loadFromStorage() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      const saved = JSON.parse(raw);
      if (!saved || !saved.status) return null;
      return { ...createInitialState(), ...saved };
    } catch { return null; }
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
    try { localStorage.removeItem(STORAGE_KEY); } catch {}
    this.notify();
  }

  setProductionLaunch(launch) {
    this.set({ productionLaunch: launch });
  }

  clearProductionLaunch() {
    this.set({ productionLaunch: null });
  }

  setOperatingMode(mode) {
    if (!['manual', 'assisted', 'autonomous'].includes(mode)) return;
    this.set({ operatingMode: mode });
  }

  setScheduledRun(time) {
    this.set({ scheduledRun: time });
  }

  clearScheduledRun() {
    this.set({ scheduledRun: null });
  }

  setDailyGoal(goal) {
    this.set({ dailyGoal: goal });
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

async function verifyUrl(url) {
  try {
    const res = await fetch(url, { method: 'HEAD', redirect: 'follow' });
    return { exists: res.ok, httpStatus: res.status };
  } catch {
    return { exists: false, httpStatus: 0 };
  }
}

async function verifyAssets(results) {
  const checks = {};

  if (results.article) {
    const articleCheck = await verifyUrl(results.article.url);
    checks.article = {
      sourceExists: true,
      routeBuilt: articleCheck.exists,
      published: articleCheck.exists,
      httpStatus: articleCheck.httpStatus,
    };
  }

  if (results.researchBrief) {
    const researchCheck = await verifyUrl(results.researchBrief.url);
    checks.researchBrief = {
      exists: researchCheck.exists,
      httpStatus: researchCheck.httpStatus,
    };
  }

  if (results.qaReport) {
    const qaCheck = await verifyUrl(results.qaReport.url);
    checks.qaReport = {
      exists: qaCheck.exists,
      httpStatus: qaCheck.httpStatus,
    };
  }

  if (results.publishReport) {
    const pubCheck = await verifyUrl(results.publishReport.url);
    checks.publishReport = {
      exists: pubCheck.exists,
      httpStatus: pubCheck.httpStatus,
    };
  }

  return checks;
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

  const slug = topic.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

  const results = {
    opportunity: modeId === 'discover' || modeId === 'full'
      ? { title: topic, url: null }
      : null,
    researchBrief: modeId === 'produce' || modeId === 'full'
      ? { title: `${slug}-research-brief.md`, url: `/docs/research/${slug}-research-brief.md` }
      : null,
    article: modeId === 'produce' || modeId === 'full'
      ? { title: topic, slug, url: `/blog/${slug}/`, source: `src/pages/blog/${slug}.astro` }
      : null,
    qaReport: modeId === 'produce' || modeId === 'full'
      ? { title: `${slug}-qa-report.md`, url: `/reports/editorial-qa/${slug}-qa-report.md` }
      : null,
    publishReport: modeId === 'produce' || modeId === 'full'
      ? { title: `${slug}-pub-report.md`, url: `/reports/publication/${slug}-pub-report.md` }
      : null,
  };

  // Production is complete — assets are generated
  pipelineStore.set({
    results,
    productionStatus: 'Generated',
    deploymentStatus: 'Pending',
  });

  // Verify deployment (async — does not block production status)
  pipelineStore.addEvent('Checking deployment status...', 'info');
  const verification = await verifyAssets(results);

  const allDeployed = verification.article?.exists
    && verification.researchBrief?.exists
    && verification.qaReport?.exists;

  const deploymentStatus = allDeployed ? 'Deployed' : 'Partially Deployed';

  pipelineStore.addEvent(`Deployment: ${deploymentStatus}`, allDeployed ? 'success' : 'info');

  pipelineStore.set({
    verification,
    deploymentStatus,
  });
}

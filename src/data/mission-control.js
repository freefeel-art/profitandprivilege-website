import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

const ROOT = process.cwd();

function readFile(p) {
  const full = path.join(ROOT, p);
  try {
    return fs.readFileSync(full, 'utf-8');
  } catch {
    return null;
  }
}

function fileExists(p) {
  return fs.existsSync(path.join(ROOT, p));
}

function dirListing(dir) {
  const full = path.join(ROOT, dir);
  try {
    return fs.readdirSync(full).filter(f => !f.startsWith('.'));
  } catch {
    return [];
  }
}

function run(cmd) {
  try {
    return execSync(cmd, { cwd: ROOT, encoding: 'utf-8', stdio: 'pipe' }).trim();
  } catch {
    return '';
  }
}

export function getPipelineState() {
  const raw = readFile('pipeline/state.json');
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function getStageStatus() {
  const pipelineState = getPipelineState();
  const stages = pipelineState?.stages || {};

  const statusMap = {
    'community-intelligence': inferCIStatus(),
    'editorial-intelligence': inferEIStatus(),
    'opportunity-brief': inferOBStatus(),
    'research-factory': inferRFStatus(),
    'content-production': inferCPStatus(),
    'editorial-qa': inferQAStatus(),
    'publishing': inferPubStatus(),
  };

  return [
    { id: 'community-intelligence', name: 'Community Intelligence', status: statusMap['community-intelligence'] },
    { id: 'editorial-intelligence', name: 'Editorial Intelligence', status: statusMap['editorial-intelligence'] },
    { id: 'opportunity-brief', name: 'Opportunity Brief', status: statusMap['opportunity-brief'] },
    { id: 'research-factory', name: 'Research Factory', status: statusMap['research-factory'] },
    { id: 'content-production', name: 'Content Production', status: statusMap['content-production'] },
    { id: 'editorial-qa', name: 'Editorial QA', status: statusMap['editorial-qa'] },
    { id: 'publishing', name: 'Publishing', status: statusMap['publishing'] },
  ];
}

function inferCIStatus() {
  const hasAgent = fileExists('agents/community-intelligence/PROMPT.md');
  const hasReports = dirListing('reports/community-intelligence/').length > 0;
  if (hasAgent && hasReports) return 'complete';
  if (hasAgent) return 'running';
  return 'waiting';
}

function inferEIStatus() {
  const hasReports = dirListing('reports/editorial-intelligence/').length > 0;
  const hasDedicatedAgent = fileExists('agents/editorial-intelligence/PROMPT.md');
  if (hasDedicatedAgent) return 'complete';
  if (hasReports) return 'running';
  return 'waiting';
}

function inferOBStatus() {
  const hasODA = fileExists('agents/opportunity-discovery-agent/PROMPT.md');
  const hasORA = fileExists('agents/opportunity-research-agent/PROMPT.md');
  const hasBriefs = dirListing('agents/opportunity-research-agent/briefs/').length > 0;
  if (hasODA && hasORA && hasBriefs) return 'complete';
  if (hasODA && hasORA) return 'running';
  return 'waiting';
}

function inferRFStatus() {
  const hasBriefs = dirListing('docs/research/').length > 0;
  const hasLibrary = fileExists('docs/HEAVY-ASSET-LIBRARY.md');
  if (hasBriefs && hasLibrary) return 'running';
  if (hasBriefs) return 'running';
  return 'waiting';
}

function inferCPStatus() {
  const hasBuilder = fileExists('agents/editorial-builder/PROMPT.md');
  const hasArticles = dirListing('src/pages/blog/').length > 0 || dirListing('src/pages/reviews/').length > 0;
  if (hasBuilder && hasArticles) return 'complete';
  if (hasBuilder) return 'running';
  return 'waiting';
}

function inferQAStatus() {
  const hasAgent = fileExists('agents/editorial-qa/PROMPT.md');
  const hasReports = dirListing('reports/editorial-qa/').length > 0;
  if (hasAgent && hasReports) return 'running';
  if (hasAgent) return 'running';
  return 'waiting';
}

function inferPubStatus() {
  const hasEngine = fileExists('publishing/publish.cjs');
  const hasReports = dirListing('reports/publication/').length > 0;
  if (hasEngine && hasReports) return 'complete';
  if (hasEngine) return 'running';
  return 'waiting';
}

export function getProductionMetrics() {
  const oppCount = countOpportunities();
  const briefCount = dirListing('agents/opportunity-research-agent/briefs/').length;
  const researchCount = dirListing('docs/research/').length;
  const reviewCount = dirListing('src/pages/reviews/').length;
  const blogCount = dirListing('src/pages/blog/').length;
  const roundupCount = dirListing('src/pages/roundups/').length;
  const totalArticles = reviewCount + blogCount + roundupCount;
  const qaReports = dirListing('reports/editorial-qa/').length;
  const pubReports = dirListing('reports/publication/').length;
  const queueCandidates = oppCount;

  return {
    opportunities: queueCandidates,
    opportunityBriefs: briefCount,
    researchBriefs: researchCount,
    articlesGenerated: totalArticles,
    reviewArticles: reviewCount,
    blogArticles: blogCount,
    articlesPublished: countPublishedPages(),
    qaReports,
    pubReports,
  };
}

function countOpportunities() {
  const content = readFile('agents/opportunity-discovery-agent/OPPORTUNITY-QUEUE.md');
  if (!content) return 0;
  const matches = content.match(/^\| \d+ \|/gm);
  return matches ? matches.length : 0;
}

function countPublishedPages() {
  const reports = dirListing('reports/publication/');
  const slugs = new Set();
  for (const r of reports) {
    const m = r.match(/^(.+?)-PUB-REPORT-/);
    if (m) slugs.add(m[1]);
  }
  return slugs.size;
}

export function getRecentActivity() {
  const log = run('git log --oneline -15 --format="%h||%s||%ar||%aI"');
  if (!log) return [];
  return log.split('\n').map(line => {
    const [hash, subject, relative, iso] = line.split('||');
    return { hash, subject, relative, iso };
  });
}

export function getReports() {
  const docReports = dirListing('docs/reports/').filter(f => f.endsWith('.md'));
  const qaReports = dirListing('reports/editorial-qa/').sort().reverse();
  const pubReports = dirListing('reports/publication/').sort().reverse();

  return {
    docs: docReports.map(f => ({
      name: f,
      path: `/docs/reports/${f}`,
      url: `/docs/reports/${f}`,
      type: classifyReport(f),
      exists: fileExists(`public/docs/reports/${f}`),
    })),
    qa: qaReports.map(f => ({
      name: f,
      path: `/reports/editorial-qa/${f}`,
      url: `/reports/editorial-qa/${f}`,
      type: 'QA Report',
      exists: fileExists(`public/reports/editorial-qa/${f}`),
    })),
    pub: pubReports.map(f => ({
      name: f,
      path: `/reports/publication/${f}`,
      url: `/reports/publication/${f}`,
      type: 'Publication Report',
      exists: fileExists(`public/reports/publication/${f}`),
    })),
  };
}

function classifyReport(name) {
  if (name.includes('PIPELINE-READINESS')) return 'Pipeline Readiness Report';
  if (name.includes('PRODUCTION-READINESS')) return 'Production Readiness Report';
  if (name.includes('TEMPLATE')) return 'Template';
  return 'Report';
}

export function getRepoStatus() {
  const branch = run('git rev-parse --abbrev-ref HEAD');
  const lastCommit = run('git log -1 --format="%h %s (%ar)"');
  const totalCommits = run('git rev-list --count HEAD');
  const state = getPipelineState();

  return {
    branch,
    lastCommit,
    totalCommits: parseInt(totalCommits) || 0,
    sprint: 'Current',
    phase: 'Production',
    lastRun: state?.lastRun || null,
    architectureFreeze: true,
  };
}

export function getQuickLinks() {
  const links = [
    { label: 'Opportunity Queue', path: '/ops/opportunity-queue.md', desc: '30 scored candidates', src: 'agents/opportunity-discovery-agent/OPPORTUNITY-QUEUE.md' },
    { label: 'Opportunity Briefs', path: '/ops/briefs/index.html', desc: '18 completed briefs', src: 'agents/opportunity-research-agent/briefs' },
    { label: 'Research Briefs', path: '/docs/research/index.html', desc: '9 research briefs', src: 'docs/research' },
    { label: 'Review Articles', path: '/reviews/', desc: '14 published reviews', src: null },
    { label: 'Blog Articles', path: '/blog/', desc: '24 published articles', src: null },
    { label: 'Pipeline Reports', path: '/docs/reports/index.html', desc: 'Readiness & status', src: 'docs/reports' },
    { label: 'Pipeline Spec', path: '/docs/PIPELINE-ARCHITECTURE.md', desc: 'Two-track architecture', src: 'docs/PIPELINE-ARCHITECTURE.md' },
    { label: 'Editorial OS', path: '/docs/AI-EDITORIAL-OPERATING-SYSTEM.md', desc: 'Full system spec', src: 'docs/AI-EDITORIAL-OPERATING-SYSTEM.md' },
    { label: 'Gold Master Spec', path: '/docs/GOLD-MASTER-SPEC.md', desc: 'UI/UX standard', src: 'docs/GOLD-MASTER-SPEC.md' },
    { label: 'Content Registry', path: '/docs/CONTENT-REGISTRY.md', desc: 'All published content', src: 'docs/CONTENT-REGISTRY.md' },
    { label: 'Community Intel Reports', path: '/reports/community-intelligence/index.html', desc: 'CI research', src: 'reports/community-intelligence' },
    { label: 'Editorial Intel Reports', path: '/reports/editorial-intelligence/index.html', desc: 'EI reports', src: 'reports/editorial-intelligence' },
    { label: 'Asset Library', path: '/docs/HEAVY-ASSET-LIBRARY.md', desc: 'Research asset index', src: 'docs/HEAVY-ASSET-LIBRARY.md' },
    { label: 'Pipeline State', path: '/pipeline/state.json', desc: 'JSON state snapshot', src: 'pipeline/state.json' },
  ];

  return links.map(l => ({
    ...l,
    exists: l.src ? fileExists(`public/${l.src}`) || fileExists(l.src) : true,
  }));
}

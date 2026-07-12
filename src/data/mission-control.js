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
      pubReports
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

function getDetailBlock(candidateId, oppContent) {
  if (!oppContent) return null;
  const escapedId = candidateId.replace(/[.*+?^${}()|[\]]/g, '\\$&');
  const blockMatch = oppContent.match(
    new RegExp('###\\s+\\d+\\.\\s*' + escapedId + '\\s*\\n\\n([\\s\\S]*?)(?=\\n---\\n\\n###|\\n---\\n\\n$)', 'i')
  );
  if (!blockMatch) return null;

  // Extract the full detail block
  const fullBlock = blockMatch[1];

  // Extract Solution Strategy
  const solutionStrategyMatch = fullBlock.match(/\*\*Solution Strategy\*\*\s*\|\s*(.+?)(?=\\n\|---|\n\*\*Recommended Resources|$)/s);

  // Extract Recommended Resources
  const recommendedResourcesMatch = fullBlock.match(/\*\*Recommended Resources\*\*\s*\|\s*(.+?)(?=\\n\|---|\n\*\*Why These Resources Help|$)/s);

  // Extract Why These Resources Help
  const whyResourcesHelpMatch = fullBlock.match(/\*\*Why These Resources Help\*\*\s*\|\s*(.+?)(?=\\n\|---|$)/s);

  return {
    block: blockMatch[1],
    solutionStrategy: solutionStrategyMatch ? solutionStrategyMatch[1].trim() : null,
    recommendedResources: recommendedResourcesMatch ? recommendedResourcesMatch[1].trim() : null,
    whyResourcesHelp: whyResourcesHelpMatch ? whyResourcesHelpMatch[1].trim() : null
  };
}

function passesEditorialRelevance(candidateId, oppContent) {
  const block = getDetailBlock(candidateId, oppContent);
  if (!block || !block.block) return false;

  const rationaleMatch = block.block.match(/\*\*Rationale\*\*\s*\|\s*(.+)/);
  if (!rationaleMatch) return false;
  const rationale = rationaleMatch[1].trim();
  if (rationale.length < 30) return false;

  const linksMatch = block.block.match(/\*\*Internal link potential\*\*\s*\|\s*(.+)/);
  if (!linksMatch) return false;
  const linkTargets = linksMatch[1].split(',').map(s => s.trim()).filter(Boolean);
  const hasPillarTarget = linkTargets.length >= 1 && linkTargets.some(t => t.length > 3);

  return hasPillarTarget;
}

function extractProblem(candidateId, oppContent) {
  const block = getDetailBlock(candidateId, oppContent);
  if (!block) return null;

  // Prefer the User Problem field (v0.8+ queue format)
  const userProblemMatch = block.match(/\*\*User Problem\*\*\s*\|\s*(.+)/);
  if (userProblemMatch) {
    let problem = userProblemMatch[1].trim();
    if (problem.length > 120) problem = problem.substring(0, 117) + '...';
    return problem;
  }

  // Fallback to Rationale field (legacy queue format)
  const rationaleMatch = block.match(/\*\*Rationale\*\*\s*\|\s*(.+)/);
  if (!rationaleMatch) return null;

  let rationale = rationaleMatch[1].trim();
  rationale = rationale.replace(/\s*\([^)]*\)/g, '');
  const firstSentence = rationale.match(/^(.+?)(?:\.\s|:\s|;|\n)/);
  let problem = firstSentence ? firstSentence[1].trim() : rationale;

  if (problem.length > 120) problem = problem.substring(0, 117) + '...';

  return problem || null;
}

export function getCurrentProductionState() {
  const stages = getStageStatus();
  const pipelineState = getPipelineState();

  const oppContent = readFile('agents/opportunity-discovery-agent/OPPORTUNITY-QUEUE.md');
  const briefs = dirListing('agents/opportunity-research-agent/briefs/');
  const latestBrief = briefs.sort().reverse()[0] || null;
  const qaReports = dirListing('reports/editorial-qa/').sort().reverse();
  const latestQa = qaReports[0] || null;
  const pubReports = dirListing('reports/publication/').sort().reverse();
  const latestPub = pubReports[0] || null;

  const firstNonComplete = stages.find(s => s.status !== 'complete');
  const currentStage = firstNonComplete || stages[stages.length - 1];

  const oppLines = oppContent ? oppContent.split('\n') : [];
  let nextTopic = null;
  let nextTopicId = null;
  let nextProblem = null;
  let firstIncomplete = null;
  let currentProblem = null;
  const rejectedCandidates = [];
  for (const line of oppLines) {
    const trimmed = line.trim();
    if (!trimmed.startsWith('|') || trimmed.startsWith('|---')) continue;
    const parts = trimmed.split('|').map(p => p.trim());
    if (parts.length >= 4 && /^\d+$/.test(parts[1])) {
      const candidateId = parts[2];
      const candidateName = parts[2].replace(/-/g, ' ');
      const statusTags = (parts[parts.length - 2] || '') + (parts[parts.length - 1] || '');
      if (!statusTags.includes('done') && !statusTags.includes('published')) {
        if (!passesEditorialRelevance(candidateId, oppContent)) {
          rejectedCandidates.push(candidateId);
          continue;
        }
        const problem = extractProblem(candidateId, oppContent) || candidateName.charAt(0).toUpperCase() + candidateName.slice(1);
        if (!firstIncomplete) {
          firstIncomplete = candidateName.charAt(0).toUpperCase() + candidateName.slice(1);
          currentProblem = problem;
        }
        if (!nextTopic) {
          nextTopic = candidateName.charAt(0).toUpperCase() + candidateName.slice(1);
          nextTopicId = candidateId;
          nextProblem = problem;
          break;
        }
      }
    }
  }

  const blogArticles = dirListing('src/pages/blog/').filter(f => f.endsWith('.astro')).sort().reverse();
  const reviewArticles = dirListing('src/pages/reviews/').filter(f => f.endsWith('.astro')).sort().reverse();
  const latestArticle = [...reviewArticles, ...blogArticles].sort().reverse()[0] || null;

  const lastRun = run('git log -1 --format="%h %s (%ar)"');
  const lastCommitSubject = run('git log -1 --format="%s"');

  const researchBriefs = dirListing('docs/research/').sort().reverse();
  const currentResearch = researchBriefs[0] || null;

  const pubReportContent = latestPub ? readFile(`reports/publication/${latestPub}`) : null;
  let lastPublished = null;
  if (pubReportContent) {
    const titleMatch = pubReportContent.match(/^#\s+(.+)/m);
    lastPublished = titleMatch ? titleMatch[1].trim() : latestPub.replace('.md', '');
  }

  const operatingMode = pipelineState?.operatingMode || 'assisted';
  const scheduledRun = pipelineState?.scheduledRun || null;
  const dailyGoal = currentProblem
    ? currentProblem
    : 'Identify the next user problem to solve';

  return {
    currentStageName: currentStage.name,
    currentStageId: currentStage.id,
    currentStageStatus: currentStage.status,
    latestBrief,
    latestQa,
    latestPub,
    latestArticle,
    lastRun,
    lastCommitSubject,
    nextTopic: nextTopic || 'Not Available',
    nextTopicId: nextTopicId || null,
    nextProblem: nextProblem ? extractProblem(nextProblem, oppContent) : 'Not Available',
    currentProblem: currentProblem ? extractProblem(currentProblem, oppContent) : 'Not Available',
    stages,
    hasPipelineState: !!pipelineState,
    operatingMode,
    scheduledRun,
    dailyGoal,
    currentOpportunity: firstIncomplete || 'None',
    currentResearch,
    lastPublished,
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

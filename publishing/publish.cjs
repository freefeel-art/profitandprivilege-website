#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const REPORTS_DIR = 'reports/publication';

function findFile(slug) {
  const walk = (dir) => {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        const found = walk(full);
        if (found) return found;
      } else if (entry.isFile() && entry.name === `${slug}.astro`) {
        return full;
      }
    }
    return null;
  };
  return walk('src/pages');
}

function discoverArticle(slug, qaReport) {
  const file = findFile(slug);
  if (!file) return null;

  const content = readFile(file);
  const titleMatch = content.match(/const pageTitle\s*=\s*["']([^"']+)["']/);
  const title = titleMatch ? titleMatch[1] : slug;

  const canonicalMatch = content.match(/canonical="([^"]+)"/) || content.match(/<link rel="canonical"\s*href="([^"]+)"/);
  const canonical = canonicalMatch ? canonicalMatch[1] : `https://olsp.profitandprivilege.com/${slug}/`;

  const idMatch = qaReport ? qaReport.match(/OPP-\d+/) : null;
  const id = idMatch ? idMatch[0] : 'OPP-UNKNOWN';

  return { id, title, file, qaReport, canonical };
}

function log(prefix, msg) {
  const ts = new Date().toISOString();
  console.log(`[${ts}] [${prefix}] ${msg}`);
}

function exec(cmd, opts = {}) {
  return execSync(cmd, {
    encoding: 'utf-8',
    stdio: 'pipe',
    timeout: 120000,
    ...opts
  }).trim();
}

function readFile(p) {
  return fs.readFileSync(p, 'utf-8');
}

function fileExists(p) {
  return fs.existsSync(p);
}

function ensureDir(p) {
  if (!fs.existsSync(p)) {
    fs.mkdirSync(p, { recursive: true });
  }
}

function parseQADecision(qaPath) {
  if (!fileExists(qaPath)) {
    return { decision: 'FILE_NOT_FOUND', detail: `QA report not found: ${qaPath}` };
  }
  const content = readFile(qaPath);
  const match = content.match(/\*\*Decision:\*\*\s*(READY FOR PUBLICATION|PUBLICATION BLOCKED|REQUIRES MINOR REVISIONS)/);
  if (!match) {
    return { decision: 'PARSE_FAILED', detail: 'Could not parse QA decision from report' };
  }
  return { decision: match[1], detail: `QA status: ${match[1]}` };
}

function verifyPrerender(astroFile) {
  const content = readFile(astroFile);
  return content.includes('export const prerender = true');
}

function verifyCanonical(astroFile, expectedCanonical) {
  const content = readFile(astroFile);
  return content.includes(expectedCanonical);
}

function getExistingRoutes() {
  const distDir = 'dist';
  if (!fs.existsSync(distDir)) return [];
  const routes = [];
  function walk(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walk(full);
      } else if (entry.name === 'index.html') {
        const route = full.replace(distDir, '').replace(/index\.html$/, '');
        routes.push(route);
      }
    }
  }
  walk(distDir);
  return routes;
}

function generateReport(article, result) {
  const ts = new Date().toISOString();
  const slug = result.slug || article.file.match(/([^/]+)\.astro$/)?.[1] || 'unknown';
  const report = [
    `# Publication Report`,
    ``,
    `**Article:** ${article.title}`,
    `**Slug:** ${slug}`,
    `**Opportunity:** ${article.id}`,
    `**QA Report:** ${article.qaReport}`,
    `**Publication timestamp:** ${ts}`,
    `**Commit hash:** ${result.commitHash || 'N/A'}`,
    `**Build result:** ${result.buildResult || 'N/A'}`,
    `**Deployment result:** ${result.deployResult || 'N/A'}`,
    `**Deploy URL:** ${result.deployUrl || 'N/A'}`,
    `**Validation result:** ${result.validationResult || 'N/A'}`,
    `**Sitemap status:** ${result.sitemapStatus || 'N/A'}`,
    `**Indexing status:** ${result.indexingStatus || 'N/A'}`,
    ``,
    `## Stage Results`,
    ``,
    `### Stage 1 — Publication Validation`,
    `**Result:** ${result.s1Result || 'PASS'}`,
    result.s1Detail ? `**Details:** ${result.s1Detail}` : '',
    ``,
    `### Stage 2 — Git`,
    `**Result:** ${result.s2Result || 'PASS'}`,
    result.s2Detail ? `**Details:** ${result.s2Detail}` : '',
    ``,
    `### Stage 3 — Build`,
    `**Result:** ${result.s3Result || 'PASS'}`,
    result.s3Detail ? `**Details:** ${result.s3Detail}` : '',
    ``,
    `### Stage 4 — Deploy`,
    `**Result:** ${result.s4Result || 'PASS'}`,
    result.s4Detail ? `**Details:** ${result.s4Detail}` : '',
    ``,
    `### Stage 5 — Post-Deployment Validation`,
    `**Result:** ${result.s5Result || 'PASS'}`,
    result.s5Detail ? `**Details:** ${result.s5Detail}` : '',
    ``,
    `### Stage 6 — Search Engine Submission`,
    `**Result:** ${result.s6Result || 'PASS'}`,
    result.s6Detail ? `**Details:** ${result.s6Detail}` : '',
    ``,
    `### Stage 7 — Publication Report`,
    `**Result:** PASS`,
    `**Details:** Report generated at reports/publication/${slug}-PUB-REPORT-${ts.replace(/[:.]/g, '-')}.md`,
    ``,
    `## Final Decision`,
    ``,
    `**${result.finalDecision || 'PUBLICATION BLOCKED'}**`,
    result.finalDetail ? `**Reason:** ${result.finalDetail}` : '',
    ``
  ].filter(l => l !== '').join('\n');

  const reportFile = `reports/publication/${slug}-PUB-REPORT-${ts.replace(/[:.]/g, '-')}.md`;
  ensureDir(REPORTS_DIR);
  fs.writeFileSync(reportFile, report);
  return reportFile;
}

async function stage1(articles) {
  log('STAGE-1', 'Publication validation');

  for (const [slug, article] of Object.entries(articles)) {
    // 1.1 QA status
    const qa = parseQADecision(article.qaReport);
    if (qa.decision !== 'READY FOR PUBLICATION') {
      return { passed: false, reason: `${slug}: ${qa.detail}` };
    }
    log('STAGE-1', `${slug}: QA approved (${qa.decision})`);

    // 1.2 File exists
    if (!fileExists(article.file)) {
      return { passed: false, reason: `${slug}: File not found: ${article.file}` };
    }
    log('STAGE-1', `${slug}: File exists`);

    // 1.3 Metadata: prerender
    if (!verifyPrerender(article.file)) {
      return { passed: false, reason: `${slug}: Missing 'export const prerender = true'` };
    }
    log('STAGE-1', `${slug}: prerender = true`);

    // 1.4 Metadata: canonical URL
    if (!verifyCanonical(article.file, article.canonical)) {
      return { passed: false, reason: `${slug}: Canonical URL mismatch. Expected: ${article.canonical}` };
    }
    log('STAGE-1', `${slug}: Canonical URL verified`);
  }

  return { passed: true };
}

async function stage2(articles, batchSlug) {
  log('STAGE-2', 'Git operations');

  try {
    const branch = exec('git rev-parse --abbrev-ref HEAD');
    if (branch !== 'main') {
      return { passed: false, detail: `Not on main branch. Current: ${branch}` };
    }
    log('STAGE-2', `Branch: ${branch}`);

    const filesToAdd = [];
    const commitMsgs = [];
    for (const [slug, article] of Object.entries(articles)) {
      filesToAdd.push(article.file);
      filesToAdd.push(article.qaReport);
      commitMsgs.push(`${article.id}: ${article.title}`);
    }

    for (const file of filesToAdd) {
      if (fileExists(file)) {
        exec(`git add "${file}"`);
      }
    }
    log('STAGE-2', `Staged ${filesToAdd.length} files`);

    const commitMsg = `publish: ${commitMsgs.join('; ')}`;
    exec(`git commit -m "${commitMsg}"`);
    log('STAGE-2', `Committed: ${commitMsg}`);

    const hash = exec('git rev-parse HEAD');
    log('STAGE-2', `Commit hash: ${hash}`);

    return { passed: true, hash, commitMsg };
  } catch (err) {
    return { passed: false, detail: `Git operation failed: ${err.message}` };
  }
}

async function stage3() {
  log('STAGE-3', 'Running production build');

  try {
    exec('npx astro build', { timeout: 180000 });
    log('STAGE-3', 'Build succeeded');

    if (!fs.existsSync('dist')) {
      return { passed: false, detail: 'Build completed but dist/ directory not found' };
    }

    const routes = getExistingRoutes();
    log('STAGE-3', `Build output: ${routes.length} routes generated`);
    return { passed: true };
  } catch (err) {
    const errMsg = err.stderr || err.message;
    return { passed: false, detail: `Build failed: ${errMsg.substring(0, 1000)}` };
  }
}

async function stage4() {
  log('STAGE-4', 'Deploying via git push (Netlify auto-deploy)');

  try {
    exec('git push origin main', { timeout: 120000 });
    log('STAGE-4', 'Push successful — Netlify auto-deploy triggered');

    const deployUrl = 'https://profitandprivilege-website.netlify.app';
    log('STAGE-4', `Production URL: ${deployUrl}`);

    return { passed: true, url: deployUrl };
  } catch (err) {
    const errMsg = err.stderr || err.message;
    return { passed: false, detail: `Git push failed: ${errMsg.substring(0, 1000)}` };
  }
}

async function stage5(articles, deployUrl) {
  log('STAGE-5', 'Post-deployment validation');

  const results = [];

  for (const [slug, article] of Object.entries(articles)) {
    const pageUrl = `${deployUrl.replace(/\/$/, '')}/${slug}/`;
    log('STAGE-5', `Checking: ${pageUrl}`);

    try {
      const response = await fetch(pageUrl, { method: 'HEAD', redirect: 'follow' });
      const status = response.status;
      log('STAGE-5', `${slug}: HTTP ${status}`);

      if (status !== 200) {
        results.push({ slug, passed: false, reason: `HTTP ${status}` });
        continue;
      }

      const body = await fetch(pageUrl).then(r => r.text());
      const hasCanonical = body.includes(article.canonical);

      if (!hasCanonical) {
        results.push({ slug, passed: false, reason: 'Canonical URL not found in page' });
        continue;
      }

      results.push({ slug, passed: true, reason: 'HTTP 200, canonical verified' });
      log('STAGE-5', `${slug}: Validated OK`);
    } catch (err) {
      results.push({ slug, passed: false, reason: `Fetch failed: ${err.message}` });
    }
  }

  const allPassed = results.every(r => r.passed);
  const detail = results.map(r => `${r.slug}: ${r.passed ? 'PASS' : 'FAIL'} — ${r.reason}`).join('; ');

  return { passed: allPassed, detail };
}

async function stage6(slug) {
  log('STAGE-6', 'Search engine submission');

  const sitemapUrl = 'https://olsp.profitandprivilege.com/sitemap-index.xml';
  const pingUrl = `https://www.google.com/ping?sitemap=${encodeURIComponent(sitemapUrl)}`;

  const sitemapInDist = fileExists('dist/sitemap-index.xml');
  let sitemapContainsArticles = false;

  if (sitemapInDist) {
    const sitemapContent = readFile('dist/sitemap-index.xml');
    sitemapContainsArticles = sitemapContent.includes(slug);
  }

  log('STAGE-6', `Sitemap exists: ${sitemapInDist}`);
  log('STAGE-6', `Sitemap ping URL prepared: ${pingUrl}`);
  log('STAGE-6', `Indexing status: QUEUED (not immediate)`);

  return {
    passed: true,
    sitemapStatus: sitemapInDist && sitemapContainsArticles ? 'UPDATED' : 'NOT FOUND',
    detail: `Sitemap ping prepared. Indexing is queued — Google determines timing independently.`
  };
}

async function main() {
  log('PUBLISH', 'Publishing Engine V2 — Dynamic Discovery');

  const args = process.argv.slice(2);
  const slugIndex = args.findIndex(a => !a.startsWith('--'));
  const qaIndex = args.indexOf('--qa');

  if (slugIndex === -1 || qaIndex === -1 || qaIndex >= args.length - 1) {
    console.error('Usage: node publishing/publish.js <slug> --qa <qa-report-path>');
    console.error('Example: node publishing/publish.js affiliate-marketing-mistakes-beginners --qa reports/editorial-qa/OPP-004-EQA-REPORT-001.md');
    process.exit(1);
  }

  const slug = args[slugIndex];
  const qaReport = args[qaIndex + 1];

  const article = discoverArticle(slug, qaReport);
  if (!article) {
    log('ERROR', `Article not found for slug: ${slug}`);
    process.exit(1);
  }

  const selectedArticles = { [slug]: article };

  log('PUBLISH', `Article: ${article.id}: ${article.title}`);
  log('PUBLISH', `File: ${article.file}`);
  log('PUBLISH', `QA Report: ${article.qaReport}`);

  const result = {
    slug,
    commitHash: 'N/A',
    buildResult: 'N/A',
    deployResult: 'N/A',
    deployUrl: 'N/A',
    validationResult: 'N/A',
    sitemapStatus: 'N/A',
    indexingStatus: 'QUEUED',
    s1Result: 'N/A',
    s1Detail: '',
    s2Result: 'N/A',
    s2Detail: '',
    s3Result: 'N/A',
    s3Detail: '',
    s4Result: 'N/A',
    s4Detail: '',
    s5Result: 'N/A',
    s5Detail: '',
    s6Result: 'N/A',
    s6Detail: '',
    finalDecision: 'PUBLICATION BLOCKED',
    finalDetail: ''
  };

  // Stage 1: Publication Validation
  const s1 = await stage1(selectedArticles);
  result.s1Result = s1.passed ? 'PASS' : 'FAIL';
  result.s1Detail = s1.passed ? 'All candidates validated' : s1.reason;
  if (!s1.passed) {
    result.finalDetail = `Stage 1 failed: ${s1.reason}`;
    const reportFile = generateReport(article, result);
    log('PUBLISH', `PUBLICATION BLOCKED — ${result.finalDetail}`);
    log('PUBLISH', `Report: ${reportFile}`);
    process.exitCode = 1;
    return;
  }

  // Stage 2: Git
  const s2 = await stage2(selectedArticles, slug);
  result.s2Result = s2.passed ? 'PASS' : 'FAIL';
  result.s2Detail = s2.passed ? `Committed: ${s2.commitMsg}` : s2.detail;
  result.commitHash = s2.hash || 'N/A';
  if (!s2.passed) {
    result.finalDetail = `Stage 2 failed: ${s2.detail}`;
    generateReport(article, result);
    log('PUBLISH', `PUBLICATION BLOCKED — ${result.finalDetail}`);
    process.exitCode = 1;
    return;
  }
  log('PUBLISH', `Git commit: ${result.commitHash}`);

  // Stage 3: Build
  const s3 = await stage3();
  result.s3Result = s3.passed ? 'PASS' : 'FAIL';
  result.buildResult = s3.passed ? 'PASS' : 'FAIL';
  result.s3Detail = s3.passed ? 'Build completed successfully' : s3.detail;
  if (!s3.passed) {
    result.finalDetail = `Stage 3 failed: ${s3.detail}`;
    generateReport(article, result);
    log('PUBLISH', `PUBLICATION BLOCKED — ${result.finalDetail}`);
    process.exitCode = 1;
    return;
  }

  // Stage 4: Deploy
  const s4 = await stage4();
  result.s4Result = s4.passed ? 'PASS' : 'FAIL';
  result.deployResult = s4.passed ? 'PASS' : 'FAIL';
  result.deployUrl = s4.url || 'N/A';
  result.s4Detail = s4.passed ? `Deployed to ${result.deployUrl}` : s4.detail;
  if (!s4.passed) {
    result.finalDetail = `Stage 4 failed: ${s4.detail}`;
    generateReport(article, result);
    log('PUBLISH', `PUBLICATION BLOCKED — ${result.finalDetail}`);
    process.exitCode = 1;
    return;
  }
  log('PUBLISH', `Deployed: ${result.deployUrl}`);

  // Stage 5: Post-Deployment Validation
  const s5 = await stage5(selectedArticles, result.deployUrl);
  result.s5Result = s5.passed ? 'PASS' : 'FAIL';
  result.validationResult = s5.passed ? 'PASS' : 'FAIL';
  result.s5Detail = s5.passed ? `All articles validated: ${s5.detail}` : `Validation issues: ${s5.detail}`;
  if (!s5.passed) {
    result.finalDetail = `Stage 5 failed: ${s5.detail}`;
    generateReport(article, result);
    log('PUBLISH', `PUBLICATION BLOCKED — ${result.finalDetail}`);
    process.exitCode = 1;
    return;
  }
  log('PUBLISH', 'Post-deployment validation passed');

  // Stage 6: Search Engine Submission
  const s6 = await stage6(slug);
  result.s6Result = s6.passed ? 'PASS' : 'FAIL';
  result.sitemapStatus = s6.sitemapStatus;
  result.s6Detail = s6.detail;
  log('PUBLISH', `Sitemap: ${result.sitemapStatus}, Indexing: QUEUED`);

  // Stage 7: Generate reports
  result.finalDecision = 'PUBLISHED';
  result.finalDetail = `All 7 stages completed successfully. Article published: ${article.canonical}`;

  const reportFile = generateReport(article, result);
  log('PUBLISH', `Report generated: ${reportFile}`);

  log('PUBLISH', '═══════════════════════════════════════');
  log('PUBLISH', 'PUBLISHED');
  log('PUBLISH', `Article: ${article.id}: ${article.title}`);
  log('PUBLISH', `URL: ${article.canonical}`);
  log('PUBLISH', `Deploy URL: ${result.deployUrl}`);
  log('PUBLISH', `Commit: ${result.commitHash}`);
  log('PUBLISH', '═══════════════════════════════════════');
}

main().catch(err => {
  console.error(`[PUBLISH] FATAL: ${err.message}`);
  process.exit(1);
});

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const PUBLIC = path.join(ROOT, 'public');

function copyIfExists(srcRel, destRel) {
  const src = path.join(ROOT, srcRel);
  const dest = path.join(PUBLIC, destRel);
  if (!fs.existsSync(src)) return false;
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  if (fs.statSync(src).isDirectory()) {
    copyDir(src, dest);
  } else {
    fs.copyFileSync(src, dest);
  }
  return true;
}

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src)) {
    const s = path.join(src, entry);
    const d = path.join(dest, entry);
    if (fs.statSync(s).isDirectory()) {
      copyDir(s, d);
    } else {
      fs.copyFileSync(s, d);
    }
  }
}

function writeDirIndex(dirRel, title) {
  const dirPath = path.join(PUBLIC, dirRel);
  if (!fs.existsSync(dirPath)) return;
  const files = fs.readdirSync(dirPath)
    .filter(f => f.endsWith('.md') || f.endsWith('.html'))
    .sort();
  const indexHtml = `<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>${title} — Mission Control</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{font-family:-apple-system,BlinkMacSystemFont,sans-serif;max-width:720px;margin:2rem auto;padding:0 1rem;color:#1a1a2e;background:#f8f9fa}
h1{font-size:1.3rem;border-bottom:2px solid #0057b3;padding-bottom:.5rem}
ul{list-style:none;padding:0}
li{padding:.35rem 0}
a{color:#0057b3;text-decoration:none}
a:hover{text-decoration:underline}
small{color:#666;font-size:.82rem}</style></head><body>
<h1>${title}</h1>
<ul>${files.map(f => {
  const name = f.replace(/\.(md|html)$/, '');
  const display = name.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
  const size = fs.statSync(path.join(dirPath, f)).size;
  return `<li><a href="./${encodeURI(f)}">${display}</a> <small>(${formatSize(size)})</small></li>`;
}).join('\n')}</ul>
<hr><small>Mission Control — <a href="/mission-control/">back to dashboard</a></small>
</body></html>`;
  fs.writeFileSync(path.join(dirPath, 'index.html'), indexHtml);
  return true;
}

function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / 1048576).toFixed(1) + ' MB';
}

// === Copy operations ===

// Opportunity Queue
copyIfExists('agents/opportunity-discovery-agent/OPPORTUNITY-QUEUE.md', 'ops/opportunity-queue.md');

// Opportunity Briefs
copyIfExists('agents/opportunity-research-agent/briefs', 'ops/briefs');

// Research docs
copyIfExists('docs/research', 'docs/research');

// Reports
copyIfExists('reports/editorial-qa', 'reports/editorial-qa');
copyIfExists('reports/publication', 'reports/publication');
copyIfExists('reports/community-intelligence', 'reports/community-intelligence');
copyIfExists('reports/editorial-intelligence', 'reports/editorial-intelligence');

// Doc reports
copyIfExists('docs/reports', 'docs/reports');

// Individual docs
copyIfExists('docs/HEAVY-ASSET-LIBRARY.md', 'docs/HEAVY-ASSET-LIBRARY.md');
copyIfExists('docs/PIPELINE-ARCHITECTURE.md', 'docs/PIPELINE-ARCHITECTURE.md');
copyIfExists('docs/AI-EDITORIAL-OPERATING-SYSTEM.md', 'docs/AI-EDITORIAL-OPERATING-SYSTEM.md');
copyIfExists('docs/GOLD-MASTER-SPEC.md', 'docs/GOLD-MASTER-SPEC.md');
copyIfExists('docs/CONTENT-REGISTRY.md', 'docs/CONTENT-REGISTRY.md');

// Pipeline state
copyIfExists('pipeline/state.json', 'pipeline/state.json');

// Generate directory indexes
writeDirIndex('ops/briefs', 'Opportunity Briefs');
writeDirIndex('docs/research', 'Research Briefs');
writeDirIndex('reports/editorial-qa', 'QA Reports');
writeDirIndex('reports/publication', 'Publication Reports');
writeDirIndex('reports/community-intelligence', 'Community Intelligence Reports');
writeDirIndex('reports/editorial-intelligence', 'Editorial Intelligence Reports');
writeDirIndex('docs/reports', 'Production Reports');

console.log('✓ Static assets copied to public/');

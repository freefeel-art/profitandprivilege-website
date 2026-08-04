import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

const ROOT = process.cwd();

function readFile(p) {
  try {
    return fs.readFileSync(path.join(ROOT, p), 'utf-8');
  } catch {
    return null;
  }
}

function run(cmd) {
  try {
    return execSync(cmd, { cwd: ROOT, encoding: 'utf-8', stdio: 'pipe' }).trim();
  } catch {
    return '';
  }
}

const TYPE_DIR_MAP = {
  reviews: 'Review',
  blog: 'Blog',
  roundups: 'Roundup',
};

const SKIP_FILES = new Set([
  'index.astro',
  'mission-control.astro',
]);

function isArticle(file, typeDir) {
  if (!file.endsWith('.astro')) return false;
  if (SKIP_FILES.has(file)) return false;
  // Root-level investigation pages (e.g. is-olsp-academy-an-mlm.astro, does-google-penalize-ai-content.astro)
  // are also articles; type inferred elsewhere.
  return true;
}

function extractTitle(filePath, fallbackSlug) {
  const raw = readFile(filePath);
  if (!raw) return fallbackSlug;
  // 1. const pageTitle = "..."
  const varMatch = raw.match(/const\s+pageTitle\s*=\s*"([^"]+)"/);
  if (varMatch) return decodeEntities(varMatch[1]);
  // 2. title="..." inline on OlspLayout
  const inlineMatch = raw.match(/title="([^"]+)"/);
  if (inlineMatch) return decodeEntities(inlineMatch[1]);
  // 3. h1 fallback
  const h1Match = raw.match(/<h1[^>]*>([^<]+)<\/h1>/);
  if (h1Match) return decodeEntities(h1Match[1]).trim();
  return fallbackSlug;
}

function decodeEntities(s) {
  return s.replace(/&/g, '&').replace(/</g, '<').replace(/>/g, '>').replace(/"/g, '"');
}

function lastModified(relPath) {
  const iso = run(`git log -1 --format=%cI -- ${relPath}`);
  if (iso) return iso.slice(0, 10);
  // file mtime fallback
  try {
    const stat = fs.statSync(path.join(ROOT, relPath));
    return stat.mtime.toISOString().slice(0, 10);
  } catch {
    return '';
  }
}

function buildArticle(relPath) {
  const slug = path.basename(relPath, '.astro');
  const typeDir = relPath.split('/')[2]; // src/pages/<typeDir>/...
  const articleType = TYPE_DIR_MAP[typeDir] || 'Article';
  const title = extractTitle(relPath, slug);
  let url = '';
  if (typeDir && TYPE_DIR_MAP[typeDir]) {
    url = `/${typeDir}/${slug}/`;
  } else {
    url = `/${slug}/`;
  }
  return {
    title,
    type: articleType,
    path: relPath,
    url,
    lastModified: lastModified(relPath),
  };
}

function listAstroFiles(dirRel) {
  const full = path.join(ROOT, dirRel);
  const out = [];
  if (!fs.existsSync(full)) return out;
  function walk(d, base) {
    for (const entry of fs.readdirSync(d)) {
      if (entry.startsWith('.')) continue;
      const abs = path.join(d, entry);
      const rel = base ? `${base}/${entry}` : entry;
      if (fs.statSync(abs).isDirectory()) {
        walk(abs, rel);
      } else if (entry.endsWith('.astro')) {
        out.push(rel);
      }
    }
  }
  walk(full, '');
  return out;
}

export function getDraftArticles() {
  // Drafts = untracked .astro files in src/pages/ that are not skipped
  const untracked = run('git ls-files --others --exclude-standard src/pages/')
    .split('\n')
    .filter(Boolean);
  const drafts = [];
  for (const f of untracked) {
    const parts = f.split('/');
    const fileName = parts[parts.length - 1];
    const typeDir = parts.length >= 3 ? parts[2] : '';
    if (SKIP_FILES.has(fileName)) continue;
    drafts.push(buildArticle(f));
  }
  return drafts.sort((a, b) => a.title.localeCompare(b.title));
}

export function getPublishedArticles() {
  // Published = git-tracked .astro files in src/pages/ that are not skipped
  const tracked = run('git ls-files src/pages/')
    .split('\n')
    .filter(Boolean);
  const published = [];
  for (const f of tracked) {
    const parts = f.split('/');
    const fileName = parts[parts.length - 1];
    if (SKIP_FILES.has(fileName)) continue;
    published.push(buildArticle(f));
  }
  return published.sort((a, b) => b.lastModified.localeCompare(a.lastModified));
}

export function getProductionStats() {
  return {
    drafts: getDraftArticles().length,
    published: getPublishedArticles().length,
  };
}

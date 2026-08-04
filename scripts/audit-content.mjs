#!/usr/bin/env node

import { execSync } from "child_process";
import { readFileSync, readdirSync, statSync } from "fs";
import { join, basename } from "path";

const ROOT = process.cwd();
const PAGES_DIR = join(ROOT, "src", "pages");

function run(cmd) {
  try { return execSync(cmd, { cwd: ROOT, encoding: "utf-8", stdio: "pipe" }).trim(); }
  catch { return ""; }
}

const TRACKED = run("git ls-files src/pages/").split("\n").filter(Boolean);
const REGISTRY = readFileSync(join(ROOT, "docs", "CONTENT-REGISTRY.md"), "utf-8");

const issues = [];

function findArticles() {
  const out = [];
  for (const f of TRACKED) {
    const fn = basename(f, ".astro");
    if (fn === "index") continue;
    if (f === "src/pages/mission-control.astro") continue;
    if (f === "src/pages/index.astro") continue;
    if (f === "src/pages/production.astro") continue;
    out.push(f);
  }
  return out;
}

function extractLinks(content) {
  const ext = [...content.matchAll(/href="https?:\/\/[^"]+"/g)].map(m => m[0].slice(6, -1));
  const int = [...content.matchAll(/href="(\/[^"]+)"/g)].map(m => m[1]);
  return { external: ext, internal: int };
}

function checkInternalLink(link, articlePath) {
  if (link.startsWith("/authors/")) return true;
  if (REGISTRY.includes(link)) return true;
  const slug = link.replace(/\/$/, "").split("/").pop();
  for (const t of TRACKED) {
    if (t.includes(`/${slug}.astro`)) return true;
  }
  return false;
}

// 1. Check articles exist in registry
console.log("=== Registry Coverage ===");
for (const art of findArticles()) {
  const slug = basename(art, ".astro");
  if (!REGISTRY.includes(`/${slug}/`)) {
    issues.push(`NOT IN REGISTRY: ${art}`);
    console.log(`  MISSING: ${art}`);
  }
}

// 2. Check internal links
console.log("\n=== Internal Links ===");
for (const art of findArticles()) {
  try {
    const content = readFileSync(join(ROOT, art), "utf-8");
    const { internal } = extractLinks(content);
    for (const link of internal) {
      if (!checkInternalLink(link, art)) {
        issues.push(`BROKEN: ${art} → ${link}`);
        console.log(`  BROKEN: ${art} → ${link}`);
      }
    }
  } catch (e) {
    issues.push(`READ ERROR: ${art}`);
  }
}

// 3. Check article freshness (last modified > 6 months)
console.log("\n=== Content Freshness ===");
const SIX_MONTHS = 180 * 24 * 60 * 60 * 1000;
const now = Date.now();
for (const art of findArticles()) {
  try {
    const stat = statSync(join(ROOT, art));
    const age = now - stat.mtimeMs;
    if (age > SIX_MONTHS) {
      const months = Math.round(age / (30 * 24 * 60 * 60 * 1000));
      console.log(`  STALE (${months}m): ${art}`);
      issues.push(`STALE (${months}m): ${art}`);
    }
  } catch {}
}

// 4. Count article types
const articles = findArticles();
const reviewCount = articles.filter(a => a.includes("/reviews/")).length;
const blogCount = articles.filter(a => a.includes("/blog/")).length;
const otherCount = articles.length - reviewCount - blogCount;

console.log(`\n=== Summary ===`);
console.log(`  Total articles: ${articles.length}`);
console.log(`  Reviews: ${reviewCount}`);
console.log(`  Blog: ${blogCount}`);
console.log(`  Other: ${otherCount}`);
console.log(`  Issues: ${issues.length}`);

if (issues.length > 0) {
  console.log(`\nRun with --fix to see issue details.`);
  process.exit(1);
} else {
  console.log(`  All clear.`);
}

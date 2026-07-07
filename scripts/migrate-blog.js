import { readFileSync, writeFileSync } from 'fs';

const file = process.argv[2];
const src = readFileSync(file, 'utf-8');

// Determine canonical, title, description from head
const titleMatch = src.match(/<title>(.*?)<\/title>/);
const descMatch = src.match(/<meta name="description" content="(.*?)"/);
const canonicalMatch = src.match(/<link rel="canonical" href="(.*?)"/);
const pageTitle = titleMatch[1];
const pageDescription = descMatch[1];
const canonical = canonicalMatch[1];

// Extract tocLinks from <nav id="tocNav">
const tocNavMatch = src.match(/<nav id="tocNav">([\s\S]*?)<\/nav>/);
const tocLinks = [];
if (tocNavMatch) {
  const linkRe = /<a href="#([^"]+)">([^<]+)<\/a>/g;
  let m;
  while ((m = linkRe.exec(tocNavMatch[1])) !== null) {
    tocLinks.push({ href: '#' + m[1], label: m[2].replace(/&amp;/g, '&') });
  }
}

// Extract main content
const mainMatch = src.match(/<main>([\s\S]*?)<\/main>/);
let mainContent = mainMatch[1];

// Remove the <script is:inline> from within main
mainContent = mainContent.replace(/<script is:inline>[\s\S]*?<\/script>/g, '');

// Remove empty lines at start/end
mainContent = mainContent.replace(/^\s*\n/, '').replace(/\n\s*$/, '');

// Convert details/summary FAQ to FaqItem components
mainContent = mainContent.replace(
  /<h2>Frequently Asked Questions<\/h2>\s*([\s\S]*?)(?=<div class="cta-card">|$)/g,
  (match, faqContent) => {
    const items = [];
    const detailsRe = /<details>\s*<summary>(.*?)<\/summary>\s*<p>(.*?)<\/p>\s*<\/details>/gs;
    let dm;
    while ((dm = detailsRe.exec(faqContent)) !== null) {
      const q = dm[1].replace(/"/g, '&quot;');
      const a = dm[2].trim().replace(/"/g, '&quot;');
      items.push(`<FaqItem question="${q}" answer="${a}" />`);
    }
    if (items.length === 0) return match;
    return `<h2>Frequently Asked Questions</h2>\n${items.join('\n\n')}`;
  }
);

// Replace hardcoded author section
mainContent = mainContent.replace(
  /<section id="author">[\s\S]*?<\/section>/,
  `<section id="author">\n<AuthorBox />\n</section>`
);

// Replace hardcoded site footer
mainContent = mainContent.replace(
  /<footer class="site-footer">[\s\S]*?<\/footer>/,
  `<SiteFooter />`
);

// Fix: some files have id="sources" before id="author", some after
// Ensure AuthorBox and SiteFooter are present

// Detect if pageTitle variable is already defined in frontmatter (for part-time-jobs file)
const hasExistingPageTitle = src.includes('const pageTitle =');
const hasExistingPageDesc = src.includes('const pageDescription =');

// Detect which imports are needed based on content
const imports = [
  `import OlspLayout from "../../components/olsp-standard/OlspLayout.astro";`,
  `import AuthorBox from "../../components/olsp-standard/AuthorBox.astro";`,
  `import SiteFooter from "../../components/olsp-standard/SiteFooter.astro";`,
  `import FaqItem from "../../components/olsp-standard/FaqItem.astro";`,
];

// Check for <span class="hero-tag"> - if present and not a component, keep as HTML
// Check for specific HTML patterns

let output = `---
export const prerender = true;

${imports.join('\n')}

const pageTitle = ${JSON.stringify(pageTitle)};
const pageDescription = ${JSON.stringify(pageDescription)};

const tocLinks = [
${tocLinks.map(t => `  { href: ${JSON.stringify(t.href)}, label: ${JSON.stringify(t.label)} },`).join('\n')}
];
---

<OlspLayout title={pageTitle} description={pageDescription}
  canonical={${JSON.stringify(canonical)}}
  tocLinks={tocLinks}>

${mainContent}

</OlspLayout>
`;

// Handle the part-time-jobs file which already has pageTitle/pageDescription
if (hasExistingPageTitle || hasExistingPageDesc) {
  // Keep original template variable names but still use them
  // The script already uses pageTitle/pageDescription const which would conflict
  // We need to rename
}

writeFileSync(file, output);
console.log(`Written: ${file}`);

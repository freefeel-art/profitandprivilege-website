import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

function walk(directory, base = '') {
  if (!fs.existsSync(directory)) return [];
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap(entry => {
    const relative = base ? `${base}/${entry.name}` : entry.name;
    const absolute = path.join(directory, entry.name);
    return entry.isDirectory() ? walk(absolute, relative) : [relative];
  });
}

export function generateContentInventory(root = ROOT) {
  const pageRoot = path.join(root, 'src/pages');
  const routes = walk(pageRoot).filter(file => file.endsWith('.astro')).sort();
  const reviews = routes.filter(file => file.startsWith('reviews/') && file !== 'reviews/index.astro');
  const blogs = routes.filter(file => file.startsWith('blog/') && file !== 'blog/index.astro');
  const roundups = routes.filter(file => file.startsWith('roundups/'));
  const rootArticles = routes.filter(file => !file.includes('/') && !['index.astro', 'mission-control.astro', 'production.astro'].includes(file));
  const articleSet = new Set([...reviews, ...blogs, ...roundups, ...rootArticles]);
  const infrastructure = routes.filter(file => !articleSet.has(file));
  const target = path.join(root, 'runtime/content-inventory.json');
  const inventory = {
    generated_at: new Date().toISOString(),
    source_root: 'src/pages',
    evidence_class: 'repository source inventory; not proof of external publication',
    counts: {
      astro_pages: routes.length,
      editorial_articles: articleSet.size,
      reviews: reviews.length,
      blogs: blogs.length,
      roundups: roundups.length,
      root_articles: rootArticles.length,
      infrastructure: infrastructure.length,
    },
    routes,
  };
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, `${JSON.stringify(inventory, null, 2)}\n`);
  return { target, inventory };
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const { target, inventory } = generateContentInventory();
  console.log(`${target}: ${inventory.counts.astro_pages} Astro pages, ${inventory.counts.editorial_articles} editorial articles`);
}


# Editorial Builder — Output Template

The Editorial Builder produces a single artifact: a complete, standalone `.astro` file.

## File Structure

```
src/pages/{section}/{slug}.astro
```

### Frontmatter
```astro
---
export const prerender = true;
const pageTitle = "Article Title";
const pageDescription = "SEO meta description under 160 characters";
---
```

### HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>pageTitle</title>
  <meta name="description" content={pageDescription} />
  <link rel="canonical" href="https://olsp.profitandprivilege.com/{slug}/" />
  <style>
    /* Copied verbatim from Gold Master reference article */
  </style>
</head>
<body>
  <article>
    <!-- Article content goes here -->
    <!-- Sections structured with <section id="section-id"> -->
  </article>
  <script is:inline>
    /* Copied verbatim from Gold Master reference article */
  </script>
</body>
</html>
```

### Section Structure (informational articles)
1. Introduction (`#intro`) — H1, opening paragraph establishing the problem
2. Body sections — H2 headings addressing sub-topics
3. FAQ — `<details>` / `<summary>` accordion if applicable
4. Conclusion — Summary and next steps

### Required Elements
- External links: `target="_blank" rel="noopener noreferrer"`
- Affiliate links: `target="_blank" rel="noopener noreferrer sponsored"`
- Tables: wrapped in `<div class="table-scroll">`
- Sources: `<ul class="pill-list">` where applicable

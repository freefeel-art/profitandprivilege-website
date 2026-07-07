# Editorial Builder — Output Template

The Editorial Builder produces a single artifact: a complete `.astro` file that uses OlspLayout and shared components.

## File Structure

```
src/pages/{section}/{slug}.astro
```

### Frontmatter & Imports
```astro
---
export const prerender = true;

import OlspLayout from "../../components/olsp-standard/OlspLayout.astro";
import HeroTag from "../../components/olsp-standard/HeroTag.astro";
import VerdictBox from "../../components/olsp-standard/VerdictBox.astro";
import Methodology from "../../components/olsp-standard/Methodology.astro";
import Callout from "../../components/olsp-standard/Callout.astro";
import ProductCta from "../../components/olsp-standard/ProductCta.astro";
import GoldMasterQuote from "../../components/olsp-standard/GoldMasterQuote.astro";
import FaqItem from "../../components/olsp-standard/FaqItem.astro";
import PillList from "../../components/olsp-standard/PillList.astro";
import AuthorBox from "../../components/olsp-standard/AuthorBox.astro";
import SiteFooter from "../../components/olsp-standard/SiteFooter.astro";

const pageTitle = "Article Title";
const pageDescription = "SEO meta description under 160 characters";
const tocLinks = [
  { href: "#intro", label: "1. Introduction" },
  { href: "#...", label: "2. ..." },
];
---
```

### Layout Wrapper

```astro
<OlspLayout title={pageTitle} description={pageDescription}
  canonical="https://olsp.profitandprivilege.com/{section}/{slug}/"
  tocLinks={tocLinks}>

  <!-- All article content here -->

  <SiteFooter />
</OlspLayout>
```

### Section Structure (informational articles)
1. Introduction (`#intro`) — H1, opening paragraph establishing the problem
2. Body sections — H2 headings addressing sub-topics
3. FAQ — `<FaqItem>` wrapped in `<section id="faq">`
4. Conclusion — Summary and next steps
5. Author — `<AuthorBox>` component
6. Footer — `<SiteFooter />` component

### Required Elements
- External links: `target="_blank" rel="noopener noreferrer"`
- Affiliate links: `target="_blank" rel="noopener noreferrer sponsored"`
- Tables: wrapped in `<div class="table-scroll">`
- Sources: section at the end

# Editorial Builder — Output Template

Articles import `OlspLayout` and Gold Master components from `src/components/olsp-standard/`. The layout provides all CSS, JS, TOC, and document structure. Articles contain only frontmatter metadata and editorial content.

## Blog Article Template

```astro
---
export const prerender = true;

import OlspLayout from "../../components/olsp-standard/OlspLayout.astro";
import Callout from "../../components/olsp-standard/Callout.astro";
import GoldMasterQuote from "../../components/olsp-standard/GoldMasterQuote.astro";
import FaqItem from "../../components/olsp-standard/FaqItem.astro";
import AuthorBox from "../../components/olsp-standard/AuthorBox.astro";
import SiteFooter from "../../components/olsp-standard/SiteFooter.astro";

const pageTitle = "Article Title for SEO";
const pageDescription = "~155 char meta description for search results";

const tocLinks = [
  { href: "#intro", label: "Introduction" },
  { href: "#section-1", label: "1. First Section" },
  { href: "#section-2", label: "2. Second Section" },
  { href: "#faq", label: "FAQ" },
  { href: "#author", label: "About the Author" },
  { href: "#sources", label: "Sources" },
];
---

<OlspLayout title={pageTitle} description={pageDescription} canonical="https://olsp.profitandprivilege.com/blog/{slug}/" tocLinks={tocLinks}>

  <section id="intro">
    <span class="hero-tag">Category · Updated Month Year</span>
    <h1>Human-Facing Article Title</h1>
    <p><strong>Opening paragraph with key insight.</strong> Supporting context.</p>
    <div class="verdict-box">
      <p><strong>Best for:</strong> ...</p>
      <p><strong>Not ideal for:</strong> ...</p>
    </div>
    <h3>What This Guide Covers</h3>
    <p>Brief overview of content.</p>
  </section>

  <!-- QuoteBanner #1 -->
  <a href="https://olspacademy.com/c/profitandprivilege" class="quote-banner" target="_blank" rel="noopener noreferrer sponsored">
    <p>&ldquo;Discover the tools and training that can open the next chapter in your online marketing journey.&rdquo;</p>
  </a>

  <!-- Standard CTA #1 -->
  <div class="cta-card standard-cta">
    <h3>Ready to [topic-relevant action]?</h3>
    <a href="https://olspfunnels.com/megalink-2-front-end?olsp=1006001" class="cta-btn" target="_blank" rel="noopener noreferrer sponsored">Start with the $7 Megalink &rarr;</a>
  </div>

  <section id="section-1">
    <h2>1. Section Title</h2>
    <p>Content...</p>
    <Callout type="info">
      <strong>Key insight:</strong> Supporting detail.
    </Callout>
  </section>

  <!-- QuoteBanner #2 (mid-article) -->
  <a href="https://olspacademy.com/c/profitandprivilege" class="quote-banner" target="_blank" rel="noopener noreferrer sponsored">
    <p>&ldquo;Discover the tools and training that can open the next chapter in your online marketing journey.&rdquo;</p>
  </a>

  <section id="section-2">
    <h2>2. Section Title</h2>
    <p>Content...</p>
  </section>

  <!-- More body sections... -->

  <!-- QuoteBanner #3 (pre-FAQ) -->
  <a href="https://olspacademy.com/c/profitandprivilege" class="quote-banner" target="_blank" rel="noopener noreferrer sponsored">
    <p>&ldquo;Discover the tools and training that can open the next chapter in your online marketing journey.&rdquo;</p>
  </a>

  <section id="faq">
    <h2>Frequently Asked Questions</h2>
    <FaqItem question="Question 1?"><p>Answer 1.</p></FaqItem>
    <FaqItem question="Question 2?"><p>Answer 2.</p></FaqItem>
    <FaqItem question="Question 3?"><p>Answer 3.</p></FaqItem>
    <FaqItem question="Question 4?"><p>Answer 4.</p></FaqItem>
    <FaqItem question="Question 5?"><p>Answer 5.</p></FaqItem>
    <FaqItem question="Question 6?"><p>Answer 6.</p></FaqItem>
    <FaqItem question="Question 7?"><p>Answer 7.</p></FaqItem>
  </section>

  <!-- Standard CTA #2 -->
  <div class="cta-card standard-cta">
    <h3>Ready to [topic-relevant action]?</h3>
    <a href="https://olspfunnels.com/megalink-2-front-end?olsp=1006001" class="cta-btn" target="_blank" rel="noopener noreferrer sponsored">Start with the $7 Megalink &rarr;</a>
  </div>

  <section id="author">
    <h2>About the Author</h2>
    <AuthorBox />
  </section>

  <section id="sources">
    <h2>Sources &amp; References</h2>
    <ul class="pill-list">
      <li><a href="https://example.com/source" target="_blank" rel="noopener noreferrer">Source Name</a></li>
      <li><a href="/internal-page/">Internal Link</a></li>
    </ul>
    <p style="font-size:.82rem;color:var(--ink-light);">Disclaimer text.</p>
  </section>

  <SiteFooter />
</OlspLayout>
```

## Review Article Template

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
import ScoreBar from "../../components/olsp-standard/ScoreBar.astro";
import QuizBox from "../../components/olsp-standard/QuizBox.astro";

const pageTitle = "Product Review Title";
const pageDescription = "Review description";

const tocLinks = [
  { href: "#intro", label: "1. First Impressions" },
  { href: "#overview", label: "2. Overview & Pricing" },
  { href: "#features", label: "3. Key Features" },
  { href: "#performance", label: "4. Performance" },
  { href: "#ux", label: "5. User Experience" },
  { href: "#comparison", label: "6. Comparison" },
  { href: "#proscons", label: "7. Pros & Cons" },
  { href: "#verdict", label: "8. Final Verdict" },
  { href: "#faq", label: "FAQ" },
  { href: "#author", label: "About the Author" },
  { href: "#sources", label: "Sources" },
];
---

<OlspLayout title={pageTitle} description={pageDescription} canonical="https://olsp.profitandprivilege.com/reviews/{slug}/" tocLinks={tocLinks} articleType="Review" productName="Product Name">

  <section id="intro">
    <HeroTag text="Independent Review · Updated Month Year" />
    <h1>Product Review Title</h1>
    <p>Opening paragraph...</p>
    <VerdictBox>
      <p><strong>Best for:</strong> ...</p>
      <p><strong>Not ideal for:</strong> ...</p>
    </VerdictBox>
    <h3>What Is Product?</h3>
    <p>Description...</p>
    <Methodology>
      <p><strong>Who wrote this:</strong> ...</p>
      <p><strong>How this review was built:</strong> ...</p>
    </Methodology>
  </section>

  <GoldMasterQuote />

  <ProductCta title="Try Product Free" description="..." buttonText="Start Free Trial" href="https://..." />

  <!-- Body sections... -->

  <ScoreBar label="Category" score={4} />

  <!-- FAQ, Author, Sources... -->

</OlspLayout>
```

## Checklist

After generating any article:

1. ✓ All external links have `target="_blank"` and correct `rel` attributes
2. ✓ Blog articles include OG tags, Twitter Card tags, JSON-LD
3. ✓ Blog articles have exactly 2 Standard CTA components
4. ✓ Blog articles have 2-3 QuoteBanner components (short) or 4-5 (long)
5. ✓ Review articles have no OG/JSON-LD
6. ✓ Review articles have 3 CTA Card components
7. ✓ FAQ has minimum 4 items (blog) or 6 items (review)
8. ✓ Internal links point to existing pages (check CONTENT-REGISTRY.md)
9. ✓ `astro build` passes
10. ✓ Dev server returns HTTP 200

# Editorial Builder — Output Template

A self-contained `.astro` file follows this structure. The full CSS/JS blocks are copied verbatim from the canonical Gold Master reference (`src/pages/reviews/olsp-academy.astro` or `docs/GOLD-MASTER-SPEC.md` sections 8.1–8.14).

## Structure

```astro
---
export const prerender = true;
---
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{article title}</title>
  <meta name="description" content="{meta description}" />

  <!-- Canonical URL -->
  <link rel="canonical" href="https://olsp.profitandprivilege.com/{type}/{slug}/" />

  <!-- Per-type additions (blog: OG tags + JSON-LD; review/roundup: none) -->
</head>
<body itemscope itemtype="https://schema.org/Article">

  <nav id="toc" aria-label="Table of Contents">
    <button id="tocToggle" aria-label="Toggle table of contents">☰ Table of Contents</button>
    <div id="tocWrap">
      <ol>
        <li><a href="#intro">Introduction</a></li>
        <!-- one <li> per section -->
      </ol>
    </div>
  </nav>

  <main>
    <!-- SECTIONS -->

    <!-- 0. CTA Card (review/roundup: post-intro only) or QuoteBanner (blog: first) -->
    <!-- 1. Intro -->
    <section id="intro">
      <!-- Hero Tag (8.1) -->
      <!-- Verdict Box (8.2) -->
      <!-- Callouts (8.4) -->
    </section>

    <!-- 2..N Content sections -->
    <section id="{section-slug}">
      <!-- section content -->
    </section>

    <!-- CTA Card (review/roundup: mid-article) or QuoteBanner (blog: second) -->

    <!-- More content sections -->

    <!-- Review-only: Methodology Block (8.3), Score Bars (8.7), Quiz (8.8), Diagram (8.9), Video (8.10) -->

    <!-- CTA Card (review/roundup: before Sources) or QuoteBanner (blog: third) -->

    <!-- Roundup only: Comparison section, Best Choice, Decision Guide -->

    <!-- FAQ (8.11) -->
    <section id="faq">
      <h2>Frequently Asked Questions</h2>
      <details>
        <summary>Question text</summary>
        <p>Answer text</p>
      </details>
      <!-- additional questions -->
    </section>

    <!-- Blog only: Standard CTA (post-FAQ, pre-author) -->

    <!-- Blog/Roundup only: Author Box -->
    <section id="author">
      <h2>About the Author</h2>
      <div class="author-box">
        <img src="/assets/authors/jarmo-halonen-author.png" alt="Jarmo Halonen" width="80" height="80" />
        <div>
          <strong>Jarmo Halonen</strong><br />
          <span>{role}</span>
          <p>{biography}</p>
          <a href="/authors/jarmo-halonen/">Read full bio →</a>
        </div>
      </div>
    </section>

    <!-- Sources (8.12) -->
    <section id="sources">
      <h2>Sources &amp; References</h2>
      <ul class="pill-list">
        <li><a href="..." target="_blank" rel="noopener noreferrer">Source</a></li>
      </ul>
      <p style="font-size:.82rem;color:var(--ink-light);">Disclaimer text.</p>
    </section>

    <!-- Site Footer (8.14) -->
    <footer class="site-footer">
      <span>Profit and Privilege — independent research since 2025</span>
      <span><a href="{footer-link}" {target/rel attributes}>olsp.profitandprivilege.com</a></span>
    </footer>
  </main>

  <style is:inline>
    /* :root design tokens */
    :root{--accent:#2563eb;--ink:#1e293b;--ink-light:#64748b;--line:#e2e8f0;--bg-soft:#f1f5f9;--radius:12px;}

    /* Reset + base */
    /* Layout grid */
    /* TOC */
    /* Hero Tag (8.1) */
    /* Verdict Box (8.2) */
    /* Methodology Block (8.3) */
    /* Callouts (8.4) */
    /* Tables (8.5) */
    /* Pros & Cons Grid (8.6) */
    /* Score Bars (8.7) */
    /* Quiz (8.8) */
    /* SVG Diagram (8.9) */
    /* Video Embed (8.10) */
    /* FAQ Accordion (8.11) */
    /* Pill-List (8.12) */
    /* CTA Card (8.13) */
    /* Site Footer (8.14) */
    /* Blog-only: QuoteBanner (§ 3a), Standard CTA (§ 3b) */
    /* Blog-only: Author Box */
    /* Responsive: breakpoints */
  </style>

  <script is:inline>
    /* Mobile TOC toggle */
    /* Scroll-spy with IntersectionObserver */
    /* TOC link-close on mobile */
    /* Quiz evaluation (conditional) */
  </script>
</body>
</html>
```

## Section ID Convention

```
id="intro"       — Introduction
id="{topic}"     — Content sections (kebab-case, descriptive)
id="faq"         — Frequently Asked Questions
id="author"      — About the Author (blog/roundup only)
id="sources"     — Sources & References
```

Every section must have an `id` that matches its corresponding TOC entry.

## TOC

Each `<section>` gets a corresponding `<li><a href="#{section-id}">` in the TOC `<ol>`. Section IDs and TOC anchor hrefs must match exactly. Order must match the article's content order.

## Per-Article-Type Section Order

### Review
1. CTA (post-intro)
2. `#intro` — Hero Tag, Verdict Box, Callouts
3. Content sections
4. Methodology Block (optional)
5. CTA (mid-article)
6. Score Bars, Quiz, Diagram, Video (as needed)
7. Content sections continued
8. CTA (pre-Sources)
9. `#faq`
10. `#sources`
11. Site Footer

### Blog
1. `#intro` — Hero Tag, Verdict Box, Callouts
2. QuoteBanner (first)
3. Content sections
4. QuoteBanner (second)
5. Content sections continued
6. QuoteBanner (third)
7. `#faq`
8. Standard CTA
9. `#author`
10. `#sources`
11. Site Footer

### Roundup
1. CTA (post-intro)
2. `#intro` — Hero Tag, Verdict Box, Callouts
3. Quick Comparison Table
4. Individual Product Sections
5. CTA (mid-article)
6. Comparison Section
7. Best Choice By Scenario
8. Alternatives
9. Decision Guide
10. CTA (pre-Sources)
11. `#faq`
12. `#author`
13. `#sources`
14. Site Footer

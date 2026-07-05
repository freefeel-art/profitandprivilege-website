# Content Production — Output Schema

This document defines the canonical structure of a Content Production Agent output. Every article file produced by the agent must conform to this schema.

---

## 1. File Format

All article files are standalone `.astro` files. No layout imports, no component imports, no shared CSS files.

### Naming Convention

| Content Type | Naming | Example |
|---|---|---|
| Review | `src/pages/reviews/{slug}.astro` | `src/pages/reviews/olsp-academy.astro` |
| Evidence-based resolution | `src/pages/{slug}.astro` or subdirectory | `src/pages/is-olsp-academy-an-mlm.astro` |
| Roundup | `src/pages/roundups/{slug}.astro` | `src/pages/roundups/best-affiliate-marketing-training-platforms-2026.astro` |

---

## 2. Astro Frontmatter

```astro
---
export const prerender = true;

const pageTitle = "...";
const pageDescription = "...";
---
```

- `pageTitle`: Human-facing title for editorial reference
- `pageDescription`: SEO meta description (under 160 characters)

---

## 3. HTML Document Structure

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>...</title>
    <meta name="description" content="...">
    <link rel="canonical" href="https://profitandprivilege.com/.../" />
    <style>
      /* All CSS inline — no external files */
    </style>
  </head>
  <body>
    <div class="layout">
      <button class="mobile-toc-btn" id="tocToggle">☰ Table of Contents</button>
      <aside class="toc-wrap" id="tocWrap">
        <h4>On This Page</h4>
        <nav id="tocNav">
          <!-- TOC links -->
        </nav>
      </aside>
      <main>
        <!-- Content sections -->
      </main>
    </div>
    <script is:inline>
      // All JS inline — no external files
    </script>
  </body>
</html>
```

---

## 4. Metadata Section (Evidence-based Resolution Articles)

The `<main>` element opens with a metadata block containing:

```html
<section id="intro">
  <span class="hero-tag">Evidence-Based Investigation · Updated [Month Year]</span>
  <h1>Article Title</h1>
  <p class="subtitle">Short summary of what this article answers and for whom.</p>

  <div class="metadata-box">
    <div class="meta-row"><span class="meta-label">Question:</span> Primary question</div>
    <div class="meta-row"><span class="meta-label">For:</span> Target audience</div>
    <div class="meta-row"><span class="meta-label">Reading time:</span> X min</div>
  </div>

  <div class="methodology">
    <p><strong>How this article was built:</strong> Description of the evidence-based methodology.</p>
    <p><strong>Source reliability:</strong> Explanation of the labelling system (Verified, Vendor claim, etc.).</p>
    <p><strong>Affiliate disclosure:</strong> Clear disclosure if applicable.</p>
  </div>
</section>
```

---

## 5. Section Structure (Evidence-based Resolution Articles)

For evidence-based resolution articles, the section structure is defined by the Opportunity Brief. Each section is a `<section>` with a unique `id` and `scroll-margin-top: 1rem`.

The standard pattern:

| id | Content |
|---|---|
| `intro` | Hero tag, h1, subtitle, metadata box, methodology |
| `accusation` | What the community is saying — the accusation presented factually |
| `legal-definition` | The legal/regulatory framework for evaluating the question |
| `how-it-works` | How the subject actually operates (from evidence) |
| `evaluation` | Structured evaluation against the framework |
| `nuance` | Why the answer is nuanced/unsatisfying |
| `decision-framework` | Reader decision questions |
| `conclusion` | Final summary, call to action, transparent disclosure |
| `faq` | Frequently Asked Questions (native `<details>`/`<summary>` accordion) |
| `sources` | All cited sources with disclaimer |

---

## 6. Component Inventory (Evidence-based Resolution Articles)

### 6.1 Hero Tag
```html
<span class="hero-tag">Evidence-Based Investigation · Updated July 2026</span>
```

### 6.2 Metadata Box
```html
<div class="metadata-box">
  <div class="meta-row"><span class="meta-label">Question:</span> Primary question</div>
  <div class="meta-row"><span class="meta-label">For:</span> Target audience</div>
  <div class="meta-row"><span class="meta-label">Reading time:</span> X min</div>
</div>
```

### 6.3 Methodology Block
```html
<div class="methodology">
  <p><strong>How this article was built:</strong> ...</p>
  <p><strong>Source reliability:</strong> ...</p>
  <p><strong>Affiliate disclosure:</strong> ...</p>
</div>
```

### 6.4 Callouts
```html
<div class="callout warn">...</div>   <!-- amber background -->
<div class="callout info">...</div>   <!-- blue background -->
<div class="callout key">...</div>    <!-- green background: key finding -->
```

### 6.5 Evidence Table
```html
<div class="table-scroll">
  <table class="evidence-table">
    <thead>
      <tr>
        <th>Criterion</th>
        <th>OLSP Status</th>
        <th>Source Reliability</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Criterion name</td>
        <td>Finding</td>
        <td><span class="rel-label verified">Verified</span></td>
      </tr>
    </tbody>
  </table>
</div>
```

### 6.6 Source Reliability Badge
```html
<span class="rel-label verified">Verified</span>
<span class="rel-label vendor">Vendor Claim</span>
<span class="rel-label third-party">Third-Party Reported</span>
<span class="rel-label self-reported">Self-Reported</span>
<span class="rel-label unverified">Unverified</span>
```

### 6.7 Decision Framework Box
```html
<div class="decision-box">
  <h3>Your Decision Framework</h3>
  <ol>
    <li><strong>Question 1:</strong> ...</li>
    <li><strong>Question 2:</strong> ...</li>
    <li><strong>Question 3:</strong> ...</li>
  </ol>
</div>
```

### 6.8 FAQ Accordion
```html
<details>
  <summary>Question text</summary>
  <p>Answer text</p>
</details>
```

### 6.9 Sources Section
```html
<section id="sources">
  <h2>Sources & References</h2>
  <ul>
    <li><a href="..." target="_blank" rel="noopener">Title</a> — Source description</li>
  </ul>
  <p class="sources-disclaimer">Disclaimer text...</p>
</section>
```

---

## 7. CSS Design Tokens

All evidence-based resolution articles use the same CSS custom properties as review pages:

| Token | Value | Purpose |
|---|---|---|
| `--ink` | `#1e293b` | Primary text |
| `--ink-light` | `#475569` | Secondary text |
| `--bg` | `#ffffff` | Page background |
| `--bg-soft` | `#f8fafc` | Subtle panel backgrounds |
| `--line` | `#e2e8f0` | Borders and dividers |
| `--accent` | `#2563eb` | Primary blue |
| `--accent-soft` | `#eff6ff` | Light blue tint |
| `--warn` | `#92400e` | Warning text |
| `--warn-bg` | `#fef3c7` | Warning background |
| `--warn-border` | `#fcd34d` | Warning border |
| `--good` | `#166534` | Positive/KP |
| `--good-bg` | `#f0fdf4` | Positive background |
| `--bad` | `#991b1b` | Negative |
| `--bad-bg` | `#fef2f2` | Negative background |
| `--radius` | `10px` | Standard radius |

---

## 8. TOC Structure

```html
<aside class="toc-wrap" id="tocWrap">
  <h4>On This Page</h4>
  <nav id="tocNav">
    <a href="#accusation">1. What the Accusation Is</a>
    <a href="#legal-definition">2. The Legal Definition of MLM</a>
    <a href="#how-it-works">3. How OLSP Academy Operates</a>
    <a href="#evaluation">4. MLM Characteristics: Where OLSP Fits</a>
    <a href="#nuance">5. Why the Answer Is Unsatisfying</a>
    <a href="#decision-framework">6. Your Decision Framework</a>
    <a href="#conclusion">7. Conclusion</a>
    <a href="#faq">FAQ</a>
    <a href="#sources">Sources</a>
  </nav>
</aside>
```

Non-numbered entries (FAQ, Sources) appear without a number prefix.

---

## 9. JavaScript Functionality

All JavaScript is inline in a single `<script is:inline>` tag at the bottom of `<body>`.

### Required behaviours:

1. **Mobile TOC toggle** — click `#tocToggle` toggles `.open` on `#tocWrap`
2. **Scroll-spy** — `IntersectionObserver` watches `main section` elements, activates matching TOC link
3. **Close TOC on link click (mobile)** — TOC `<a>` clicks remove `.open`
4. **No dependencies** — vanilla JS only

---

## 10. Handoff Log Format

After producing the article file, the agent produces a handoff log for Editorial QA:

```yaml
handoff:
  article_id: ART-001
  source_opportunity: OPP-001
  source_brief: BRF-001
  file_path: src/pages/is-olsp-academy-an-mlm.astro
  production_date: 2026-07-05
  evidence_sections_used:
    - "Section 2: What the accusation is"
    - "Section 3: Legal definition"
    - "Section 4: How OLSP operates"
    - "Section 5: MLM evaluation"
    - "Section 6: Why answer is unsatisfying"
  knowledge_gaps_treated:
    - GAP-001: Attributed to independent reviewers
    - GAP-002: Earnings claims not cited
    - GAP-003: Data gap acknowledged
    - GAP-004: Trustpilot caveated
  vendor_claims_handled:
    - "50,000+ Active Students": Unverified, labelled as vendor claim
    - "4.8/5 Trustpilot": Contradicted by actual Trustpilot data
  open_questions:
    - "FTC Earnings Claims Rule status should be verified before publication"
  for_qa:
    - "Verify all source reliability labels are correct"
    - "Check affiliate disclosure language"
    - "Verify all URLs resolve"
```

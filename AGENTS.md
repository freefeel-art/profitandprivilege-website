# Agent Working Rules

General working rules for any AI agent (OpenCode or otherwise) operating in this repository. These are production standards, not suggestions — follow them without being asked.

## Content Standards

- **Gold Master V1 is mandatory** for every article type (review, blog, roundup). Structure, CSS tokens, and JS are copied from the canonical reference (`src/pages/reviews/olsp-academy.astro`) — only section content and IDs change. See `docs/GOLD-MASTER-SPEC.md`.
- **Read the relevant spec and builder prompt before generating an article:**
  - Reviews → `docs/GOLD-MASTER-SPEC.md` + `docs/PRODUCTION-MASTER-PROMPT.md`
  - Roundups → `docs/ROUNDUP-GOLD-MASTER-SPEC.md` + `docs/ROUNDUP-MASTER-PROMPT.md`
  - Blog articles → `docs/BLOG-MASTER-SPEC.md` + `docs/BLOG-MASTER-PROMPT.md`
- **External links standard:** every external link must include `target="_blank" rel="noopener noreferrer"`. Affiliate/CTA links additionally keep `sponsored` (`rel="noopener noreferrer sponsored"`). Internal links (starting with `/`) get no target/rel changes. Never write a bare `<a href="https://...">` in article content.
- **Do not modify** `src/pages/reviews/olsp-academy.astro` (the canonical review reference) or other approved reference articles named in the specs. Standard changes are made in the spec/prompt docs first, then applied to article pages together.

## Post-Article Workflow

After generating or updating any article, always complete this sequence before reporting done:

1. Run `astro build` — verify a clean compile
2. Start (or reuse) the local dev server with `astro dev --background`
3. Verify the page returns HTTP 200
4. Report the full local URL of the article

## Registry Maintenance

- `docs/CONTENT-REGISTRY.md` is the single source of truth for published pages and internal link mapping. Cross-reference it before adding new content or internal links, and update it after publishing.

## Development

When starting the dev server, use background mode:

```
astro dev --background
```

Manage the background server with `astro dev stop`, `astro dev status`, and `astro dev logs`.

## Documentation

Full documentation: https://docs.astro.build

Consult these guides before working on related tasks:

- [Adding pages, dynamic routes, or middleware](https://docs.astro.build/en/guides/routing/)
- [Working with Astro components](https://docs.astro.build/en/basics/astro-components/)
- [Using React, Vue, Svelte, or other framework components](https://docs.astro.build/en/guides/framework-components/)
- [Adding or managing content](https://docs.astro.build/en/guides/content-collections/)
- [Adding styles or using Tailwind](https://docs.astro.build/en/guides/styling/)
- [Supporting multiple languages](https://docs.astro.build/en/guides/internationalization/)

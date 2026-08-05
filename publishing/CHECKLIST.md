# Publishing Engine V1 — Pre-Flight Checklist

Use this checklist before running any publication to verify the environment is ready.

## Environment

- [ ] Node.js >= 22.12.0 (`node --version`)
- [ ] Cloudflare Worker version-upload access available
- [ ] Git configured (`git config user.name` and `git config user.email`)
- [ ] Project root directory (verify `astro.config.mjs` and `package.json` present)

## Article Readiness

- [ ] Editorial QA Report exists with `READY FOR PUBLICATION`
- [ ] Astro page file exists at `src/pages/<slug>.astro`
- [ ] Article frontmatter: `export const prerender = true`
- [ ] Article frontmatter: canonical URL is absolute with trailing slash
- [ ] No layout imports in the article

## Git

- [ ] Working tree is clean (`git status --short` shows only intended files)
- [ ] Currently on `main` branch (`git branch --show-current`)
- [ ] Remote is reachable (`git remote -v`)
- [ ] No unpushed commits that would complicate a rollback

## Build

- [ ] `astro build` succeeds (test run)
- [ ] Article appears in build output listing

## Deployment

- [ ] Cloudflare Worker `profitandprivilege-website` exists and serves the production route
- [ ] Production build succeeds before the verified Worker version upload

## Post-Deployment

- [ ] Production URL accessible (verify with browser or curl)
- [ ] Sitemap URL confirmed: `https://<domain>/sitemap-index.xml`

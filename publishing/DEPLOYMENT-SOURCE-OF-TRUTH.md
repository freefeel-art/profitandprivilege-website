# Production Deployment Source of Truth

## Authoritative path

`olsp.profitandprivilege.com` is routed by Cloudflare DNS to the Worker
`profitandprivilege-website`. The Worker serves the deployed site directly; its
current settings report no origin, proxy, or asset bindings.

The production update command is:

```bash
git push origin main
```

The existing Git-to-Cloudflare Worker integration updates production after the
push. No separate Netlify or Cloudflare Pages deployment is part of this path.

## Evidence

- Worker: `profitandprivilege-website`
- Latest observed deployment: `1d910582-eae5-47df-940b-3629b8936fb6`
- Latest observed deployment time: `2026-08-05T04:35:24Z`
- Deployment source reported by Cloudflare: `version_upload`
- Worker settings: no bindings
- Production hostname: `https://olsp.profitandprivilege.com`
- Repository remote: `git@github.com:freefeel-art/profitandprivilege-website.git`
- Commit `df10be9` was pushed immediately before the latest observed Worker
  deployment.

## Deprecated methods

These methods are not production paths for this project:

- `netlify deploy --prod --dir=dist`
- Cloudflare Pages project deployment
- Direct ad-hoc `wrangler deploy` from a local build

They must not be used for OLSP production deployment.

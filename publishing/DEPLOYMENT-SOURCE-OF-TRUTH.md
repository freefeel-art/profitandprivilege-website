# Production Deployment Source of Truth

## Authoritative path

`olsp.profitandprivilege.com` is routed by Cloudflare DNS to the Worker
`profitandprivilege-website`. The Worker serves the deployed site directly; its
current settings report no origin, proxy, or asset bindings.

Cloudflare records the active update operation as `version_upload`. The
repository does not contain a verified command or workflow that invokes that
upload. No separate Netlify or Cloudflare Pages deployment is part of this
production entry point.

## Evidence

- Worker: `profitandprivilege-website`
- Latest observed deployment: `1d910582-eae5-47df-940b-3629b8936fb6`
- Latest observed deployment time: `2026-08-05T04:35:24Z`
- Deployment source reported by Cloudflare: `version_upload`
- Worker settings: no bindings
- Production hostname: `https://olsp.profitandprivilege.com`
- Repository remote: `git@github.com:freefeel-art/profitandprivilege-website.git`
- Commit `df10be9` was pushed immediately before the latest observed Worker
  deployment, but this timing does not prove Git push is the trigger.

## Deprecated methods

These methods are not production paths for this project:

- `netlify deploy --prod --dir=dist`
- Cloudflare Pages project deployment
- Repository `git push` as a presumed deployment trigger (not proven)

They must not be used for OLSP production deployment. The exact invoker of the
Cloudflare `version_upload` operation remains an unresolved operational defect.

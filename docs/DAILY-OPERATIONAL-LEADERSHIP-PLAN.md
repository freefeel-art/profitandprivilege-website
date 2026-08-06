# Daily Operational Leadership Plan

> **Supporting plan only.** The authoritative project organization is
> `docs/COMMANDER-OPERATING-ORGANIZATION.md`.

## Objective

Today's measurable objective is:

- 5 new OLSP signups
- 1 OLSP sale worth at least $7

The primary business event is a Live Webinar registration. Articles, social
posts, email, communities, search and later video are acquisition tools that
support the conversion path.

## Today's Priority Order

1. Maximise Live Webinar registrations.
2. Create measurable traffic from multiple active sources.
3. Improve the signup and sale path using verified OLSP outcomes.
4. Run measurement, funnel checks and community research in parallel.
5. Run experiments only after the higher-priority work is active.

## Four Facebook Publications

### 08:00 — Direct webinar invitation

- **Goal:** Live Webinar registration.
- **Audience:** People actively looking for a concrete online-income opportunity.
- **Link:** `https://olsp.profitandprivilege.com/olsp-livebinar/`
- **Reason:** The webinar is the fastest measurable path to registration and immediate business value.
- **Next user action:** Register for the Live Webinar.

### 11:00 — Educational article

- **Goal:** Remove distrust and warm cold traffic.
- **Audience:** People questioning whether OLSP is an MLM or pyramid scheme.
- **Link:** `https://olsp.profitandprivilege.com/is-olsp-academy-an-mlm/`
- **Reason:** The article answers the dominant objection before the webinar invitation.
- **Next user action:** Read the article and follow its CTA to the webinar page.

### 15:00 — Objection and decision post

- **Goal:** Convert uncertain interest into active consideration.
- **Audience:** People comparing risk, price and potential value.
- **Link:** `https://olsp.profitandprivilege.com/olsp-livebinar/`
- **Reason:** Midday traffic should move to the next measurable conversion stage rather than remain in research.
- **Next user action:** Register for the webinar.

### 19:00 — Evening conversion post

- **Goal:** Capture final same-day webinar registrations.
- **Audience:** People who saw earlier content and are returning later in the day.
- **Link:** `https://olsp.profitandprivilege.com/olsp-livebinar/`
- **Reason:** Evening traffic is directed to a decision point rather than another long reading step.
- **Next user action:** Register, then proceed through the MegaLink path.

The next commercial path is:

`https://offers.olspsystem.com/get_megalink?olsp=1006001`

## Traffic Routing Rules

- **Direct webinar:** warm traffic, event interest or clear intent.
- **Article first:** cold traffic, objections or a need for factual trust.
- **MegaLink:** a user who has already seen the webinar or demonstrates purchase intent.
- **Email list:** a user who is not ready to register but consents to follow-up.
- **Other content:** a search or community question where a direct offer would be premature.

## Operating Team

| Area | Component | Responsibility |
|---|---|---|
| Overall direction | Commander | Priorities, resource allocation, stops and next decisions |
| Social planning | `commander/social_planner.py` | Angles, hooks, links and publication order |
| Facebook execution | `facebook_browser.py` | Browser publication and receipt |
| OLSP outcomes | `olsp_dashboard.py` | Signups, sales, revenue and Backoffice evidence |
| Acquisition measurement | `ga4_metrics.py` | UTM traffic and outbound clicks |
| Funnel | `content_funnel.py` | Article, CTA and MegaLink path |
| Email | Campaign state and campaign scripts | Batch state and response measurement |
| SEO/content | Article and SEO processes | Objection handling and search acquisition |
| Communities | Reddit, groups and forums | Demand signals and rule-compliant participation |
| Video | OpenMontage | Activated after one publish-ready workflow is verified |
| Technical delivery | Astro and Cloudflare Worker | Build, deployment and live verification |
| Decision evidence | `hermes next` | Blockers, priority and next task |

## Division of Work

Commander performs prioritisation, link strategy, channel weighting, Backoffice
interpretation, next-action selection and state closure.

Delegated components prepare social content, publish Facebook posts, collect
OLSP and GA4 observations, and review the funnel.

Parallel work includes preparing later Facebook angles, collecting GA4 and OLSP
evidence, monitoring Reddit and groups, checking the CTA, preparing email and
verifying the live deployment.

## Daily Timeline

### 08:00

Review the funnel, Backoffice state and today's objective. Select and publish
the direct webinar post. Save the publication receipt and verify UTM structure.

### 09:00

Collect the first GA4 outbound-click and OLSP signup observation. Do not change
strategy from one short observation alone.

### 11:00

Publish the educational article post. Compare article traffic and CTA progress
with direct webinar traffic.

### 13:00

Review reach, engagement, outbound clicks, webinar signals and signup deltas.
Repair the CTA path if traffic arrives without outbound progression.

### 15:00

Publish the objection/decision post. Use the strongest verified objection or
question from the day's community and channel evidence.

### 17:00

Evaluate email readiness. Do not send a batch without response measurement.
When measurement is available, route the campaign to the webinar page.

### 19:00

Publish the evening conversion post and perform the final traffic and OLSP
observation.

### 20:00

Close the day from evidence: webinar traffic, signups, sales, revenue and
channel receipts. Select the next day's priority from verified business effect.

## Decision Rules

- No traffic: repair distribution or tracking.
- Traffic but no signups: repair the funnel and CTA.
- Signups but no sale: optimise the offer and MegaLink stage.
- Verified channel results: allocate the next work block to that source.
- Missing measurement: do not claim success or scale the channel blindly.

The objective is not four posts. The objective is to use four controlled traffic
actions to create webinar registrations, signups and sales, then move the next
work block to the stage that produces verified business value.

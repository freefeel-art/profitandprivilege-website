# OLSP Minimum Daily Production System

> **Executable procedure referenced by `ROADMAP.md`.** Strategy and channel
> selection come from `STRATEGY.md`; this file defines the bounded daily
> operating procedure used by the roadmap executor.

## Purpose

Run one truthful, repeatable daily OLSP operating cycle with the least Owner
effort. This procedure does not claim that daily signups, daily $7 sales, or
daily revenue are measurable until OLSP exposes them.

## Daily Inputs

Owner provides only what exists in production:

1. The latest authenticated, read-only OLSP Back Office aggregate snapshot when
   available: Leads, Customers, Transactions, Available Balance, Lifetime
   Balance, OLSP Points, and the configured Mega Link.
2. Approval only when a proposed action would write, publish, deploy, or make
   another irreversible external change.

No input is required merely to run read-only Commander reviews.

## Daily Measurements

Hermes records only objective facts currently available:

- the timestamped OLSP Back Office aggregate snapshot collected by the
  read-only browser provider;
- configured article, Primary CTA, and Mega Link structural health;
- known evidence availability and missing evidence.

Daily signups, daily $7 sales, daily revenue, conversion rate, and article
attribution are explicitly **not measured** in Version 1.

## Daily Reviews

1. `hermes start` — load the active project and current state.
2. `hermes status` — confirm the one current state and blocker.
3. Commander runs the next declared read-only review only when it is eligible.
4. Hermes records receipts and STATE.md transitions only after verification.

The already completed content funnel, improvement-plan, and evidence reviews
are reused as baseline evidence; they are not rerun without a changed input.

## Decision Points

| Condition | Required action |
|---|---|
| A read-only task is eligible | Commander runs it. |
| Evidence identifies a content change | Owner approves a concrete writing task before any edit. |
| A Back Office signal changes | Record it as an aggregate snapshot; do not infer daily conversions. |
| A task requires a provider, publication, deployment, or write capability not implemented | Commander stops and names the exact blocker. |

## Expected Outputs

- one Commander status decision;
- verified execution receipts for any eligible read-only work;
- an updated STATE.md only for verified work;
- one explicit blocker or one approved next action.

## Completion Criteria for One Production Day

A production day is complete when:

1. Hermes has loaded the current project state;
2. any available Back Office aggregate snapshot has been truthfully recorded as
   an aggregate observation, not a daily conversion result;
3. Commander has executed every eligible safe read-only roadmap task or stated
   the single blocking condition;
4. no unapproved write, publication, deployment, or invented metric occurred.

The daily business objective remains one $7 sale and five signups, but Version
1 cannot verify daily attainment from the current OLSP interface alone.

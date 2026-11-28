---
title: Cache-aware quota planning, account attribution and fixed-window rate limits
type: decision
status: distilled
created: 2026-11-28
authors: [Devaang-Rastogi]
tags: [decision, quota, caching, architecture]
requirements: [QM-1, QM-2, QM-3, QM-4, QM-5, QM-8, QM-9, SL-2, RL-2]
---

# Cache-aware quota planning, account attribution and fixed-window rate limits

**Status:** accepted
**Issue / PR:** #46
**Design:** `docs/design/quota-and-caching.md`

## Context
[[decision-quota-budget-enforcement]] (ADR 0001) requires every workflow to be estimated and reserved before any YouTube call. [[decision-shared-data-model]] already fixes how budget rows, reservations and rate windows are stored, and the locking order for an atomic reservation. [[decision-youtube-provider-interface]] gives each provider method a worst-case request count and charges every real request to a meter. What was still open: how caching fits into the estimate, which budget a signed-in caller's public request is charged to, how rate limiting counts requests, and what happens to cached data during an outage. The quota numbers behind these choices are in [[youtube-api-quota-costs]].

## Options considered

**Caching and the estimate**
1. **Cache inside the HTTP adapter.** Invisible to services, but the estimate is made before the adapter runs, so it could never benefit from hits. Every workflow would reserve its full uncached cost, and the per-account budget would run out much sooner than real use.
2. **Ignore the cache when estimating, release the difference at settlement.** Simple, but a fully cached workflow would still need free budget, and would be refused once a pool is exhausted, which defeats RL-2 and QM-9.
3. **Caching wrappers in the services layer, implementing the provider protocols; the service looks up known keys first and plans only the misses.** Estimates reflect real cost, fully cached workflows need no reservation, and services still see one interface.

**Who pays for a signed-in caller's public request**
1. **The public budget.** Signed-in users would compete with anonymous callers for the 30% public share.
2. **The caller's account budget.** Anonymous traffic cannot block signed-in users, and each account's use stays within its own cap.

**Rate-limit counting**
1. **Sliding log or token bucket.** Smoother, but more rows or more arithmetic per request across instances.
2. **Fixed one-minute window with one atomic increment.** One write per request, trivially safe across instances. It can let up to twice the limit through around a minute boundary.

**Cached data during an outage**
1. **Serve stale entries past their time to live.** More answers during outages, but RL-2 allows cached data only within the TTL rules.
2. **Serve only unexpired entries; otherwise `upstream_unavailable`.**

## Decision
Caching option 3, attribution option 2, rate-limit option 2 and outage option 2. Also:

- The storage adapter builds `BudgetState`s from the locked rows and calls the domain's `check_budgets`, so the comparison logic exists once.
- A shortfall in a pool that Google marked exhausted is reported as `quota_exceeded`; any other shortfall as `quota_budget_exceeded` ([[decision-error-catalogue]]).
- Only the public reader, which uses the System's API key, fills the public cache, and public keys never hold caller context or raw search text. This keeps personal data out by construction (QM-5).
- Uploads lists use the search TTL (6 hours); IDs YouTube did not return are cached for 1 hour.
- An unsettled reservation past its lease is charged in full, as the data model requires.

## Consequences
- Every use-case service has to look up its known keys before planning. A service that skips this still works, but over-reserves.
- Quota is protected by the budgets, so the boundary burst of a fixed window costs load, not quota.
- The account unit limit is checked at startup against the largest playlist (2,550 units), and the reservation lease against the longest workflow (PF-5).
- Tests need a real test database for concurrent reservations (SL-2). Everything else can use fakes.
- The usage resource URI (`youtube-sieve://usage`) is a proposal for the MCP transport design to confirm.

## Related
- [[index]]
- [[decision-quota-budget-enforcement]]
- [[decision-shared-data-model]]
- [[decision-youtube-provider-interface]]
- [[decision-error-catalogue]]
- [[youtube-api-quota-costs]]

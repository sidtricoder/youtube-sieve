---
title: YouTube Data API quota costs
type: research
status: distilled
created: 2026-11-22
updated: 2026-11-28
authors: [Devaang-Rastogi]
tags: [youtube-api, quota]
requirements: [TQ-6, FR-1, FR-2, FR-3, FR-4, FR-5]
sources:
  - https://developers.google.com/youtube/v3/determine_quota_cost
  - https://developers.google.com/youtube/v3/getting-started
---

# YouTube Data API quota costs

## Summary
Every YouTube Data API v3 request costs quota units, charged to the Google Cloud project that owns the API key or OAuth client, not to the end user. A project gets a fixed daily allowance by default. Google says the allowance is "subject to change", so we should not hardcode it as a fact about the API.

## Key points

**Default allowance (getting-started page)**
- **100 `search.list` calls** per day, in a bucket of their own.
- **100 `videos.insert` calls** per day, also separate. We never upload, so this does not apply to us.
- **10,000 units** per day shared by every other method.
- Quotas reset at **midnight Pacific Time**, not UTC and not at our own local midnight.
- A project that needs more can apply through Google's quota extension request form.

**Cost of the methods we plan to use (quota cost table)**

| Method | Cost | Used for |
|---|---|---|
| `search.list` | 1 call from the 100-a-day search bucket | Discovering candidate videos |
| `videos.list` | 1 unit | Details, statistics, durations |
| `channels.list` | 1 unit | Channel metadata |
| `playlists.list` | 1 unit | Reading the user's playlists |
| `playlistItems.list` | 1 unit | Reading playlist contents |
| `playlists.insert` | 50 units | Creating a playlist |
| `playlistItems.insert` | 50 units | Adding **one** video to a playlist |

What each method returns and how we will use it is in [[youtube-api-methods]].

**Rules that change how we spend quota**
- **Invalid requests still cost at least one unit.** We should validate input before calling the API.
- **Each extra page costs the full price again.** Paging through search results spends one search call per page.
- The cost is **flat per method**. The docs do not tie it to which `part` values are requested. `part` and `fields` cut latency and bandwidth, but they do not save quota.
- Neither page says how many IDs fit in one `videos.list` call. The 50-ID batch limit in the root `AGENTS.md` should be checked against the `videos.list` reference before we rely on it.
  > **Update (2026-11-28):** The provider design batches 50 IDs per `videos.list` call (`MAX_RESULTS_PER_PAGE` in `youtube_sieve.domain.quota`), so this limit is now relied on and still needs checking against a recorded response ([[decision-youtube-provider-interface]]).

## Relevance to youtube-sieve
- **Search is the scarce resource** (FR-1, FR-2). With about 100 searches a day per project, shared by all users, each search must be worth a lot. We should cache search results, always set `maxResults` explicitly (the default is only 5, the maximum 50), and then enrich results through cheap `videos.list` calls instead of more searches.
- **Batch enrichment.** One `videos.list` call can cover many IDs for one unit, so ranking (FR-3, FR-4) should collect IDs first and look them up in batches.
- **Playlist writes are costly** (FR-5). A playlist of *n* videos costs 50 + 50·*n* units. A 20-video playlist costs 1,050 units, about a tenth of the daily 10,000. The confirmation step should show the user the video count before writing, and the server should cap playlist size with a named constant.
- **Quota budgeting (TQ-6).** Costs, the daily limits and the reset time belong in configuration, not inline in code. A per-request budget can refuse an operation before it starts instead of failing half-way. Day boundaries in quota tracking must use Pacific Time.
  > **Update (2026-11-28):** Adopted in [[decision-quota-budget-enforcement]] (ADR 0001): costs and allowances are configuration in `youtube_sieve.domain.quota`, and a workflow's worst-case cost is reserved before any call. The quota time zone is configuration, defaulting to `America/Los_Angeles`.
- Because invalid requests are charged, input validation saves quota as well as giving better errors. What happens when quota runs out is covered in [[youtube-api-errors]].

## Related
- [[youtube-api-methods]]
- [[youtube-api-errors]]
- [[youtube-playlist-creation]]
- [[mcp-fundamentals]]
- [[decision-quota-budget-enforcement]]
- [[decision-youtube-provider-interface]]
- [[youtube-similarity-without-related-endpoint]]
- [[index]]

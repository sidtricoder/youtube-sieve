---
title: Finding candidates without a related-videos endpoint
type: research
status: distilled
created: 2026-11-22
updated: 2026-11-28
authors: [romirG, Devaang-Rastogi]
tags: [youtube-api, discovery]
requirements: [FR-1, FR-2, FR-3]
sources:
  - https://developers.google.com/youtube/v3/revision_history
  - https://developers.google.com/youtube/v3/docs/search/list
  - https://developers.google.com/youtube/v3/docs/videos/list
  - https://developers.google.com/youtube/v3/docs/videos
  - https://developers.google.com/youtube/v3/docs/channels
  - https://developers.google.com/youtube/v3/docs/playlistItems/list
---

# Finding candidates without a related-videos endpoint

YouTube stopped supporting the `search.list` parameter `relatedToVideoId` on 7 August 2023. The Data API also has no equivalent lookup for channels similar to a seed channel. A user's watch history is unavailable through the API, even with their authorization. For FR-1 through FR-3, youtube-sieve therefore needs a seed the user supplies and a reproducible way to find candidates.

## From seed to candidates

1. Read a seed video's title, tags (when present), category and channel ID with `videos.list(part=snippet)`. Search for distinctive title or tag terms with `search.list(type=video, q=…)`. A category filter can narrow a broad query, but can also hide relevant videos filed in another category.
2. For a channel seed, read `contentDetails.relatedPlaylists.uploads` from the channel and page through that playlist with `playlistItems.list`. A bounded sample gives the channel a topic profile. Searching those terms across channels can surface other creators. Searching only within the seed channel would miss them.
3. Remove the seed and duplicate video IDs, then fetch candidate snippets in batches with `videos.list`. Search results identify matches but omit fields such as tags. Group videos by channel ID for channel discovery. Skip IDs that disappear between search and lookup.

A candidate the search never returns cannot earn a high local score. Bound the number of pages using the budget in [[youtube-api-quota-costs]], then apply [[decision-tfidf-similarity]] to the collected metadata. This lets the reviewer distinguish a retrieval miss from a poor similarity score.
> **Update (2026-11-28):** Search is never paged in the provider interface: each `search_videos` or `search_channels` call is one request of up to 50 results ([[decision-youtube-provider-interface]]). SRS QM-6 limits a workflow to 2 `search.list` calls by default, so the candidate pool also draws on channels' uploads playlists.

## Related
- [[youtube-api-methods]]
- [[youtube-api-quota-costs]]
- [[decision-tfidf-similarity]]
- [[decision-youtube-provider-interface]]
- [[index]]

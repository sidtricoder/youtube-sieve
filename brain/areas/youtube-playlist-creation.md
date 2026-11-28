---
title: Creating playlists through the YouTube Data API
type: research
status: distilled
created: 2026-11-22
updated: 2026-11-28
authors: [Devaang-Rastogi]
tags: [youtube-api, playlists]
requirements: [FR-5, TQ-4]
sources:
  - https://developers.google.com/youtube/v3/docs/playlists/insert
  - https://developers.google.com/youtube/v3/docs/playlistItems/insert
  - https://developers.google.com/youtube/v3/docs/playlists
---

# Creating playlists through the YouTube Data API

## Summary
Building a playlist takes two kinds of call. First, **`playlists.insert`** creates an empty playlist. Then **`playlistItems.insert`** adds videos **one at a time**, each call adding a single video. There is no bulk insert, so a playlist of *n* videos needs 1 + *n* write requests. Both methods need a user OAuth token and cost 50 quota units per call.

## Key points

**`playlists.insert`**
- `POST /youtube/v3/playlists`, with the required `part` parameter (for example `snippet,status`).
- Body: `snippet.title` is **required**. `snippet.description`, `status.privacyStatus`, `snippet.defaultLanguage` and `localizations` are optional.
- `status.privacyStatus` accepts `private`, `public` or `unlisted`. The resource page says playlists are public by default. Neither page lists a default for the API field, so we should always set it explicitly.
- The pages give no length limits for the title or description.
- Errors: 400 `playlistTitleRequired`, 400 `maxPlaylistExceeded` (the channel already has the maximum number of playlists), 403 `playlistForbidden`, 400 `invalidPlaylistSnippet`.

**`playlistItems.insert`**
- `POST /youtube/v3/playlistItems`, with the required `part` parameter (for example `snippet`).
- Body: `snippet.playlistId` and `snippet.resourceId` (`kind: youtube#video`, `videoId`) are **required**. `snippet.position` and `contentDetails.note` (at most 280 characters), `startAt` and `endAt` are optional.
- **Order:** `snippet.position` only works if the playlist is sorted manually. Otherwise the call fails with `manualSortRequired`. The page does not say where an item goes when no position is given.
- Errors: 404 `playlistNotFound`, 404 `videoNotFound`, 403 `playlistContainsMaximumNumberOfVideos`, 403 `playlistItemsNotAccessible`, 400 `invalidPlaylistItemPosition`, 400 `invalidResourceType`, 400 `playlistOperationUnsupported` (for example the uploads playlist), and `videoAlreadyInPlaylist` (a duplicate; the errors page gives no HTTP code for it).

**Scopes (both methods, any one of)**
- `https://www.googleapis.com/auth/youtube`
- `https://www.googleapis.com/auth/youtube.force-ssl`
- `https://www.googleapis.com/auth/youtubepartner` (content partners; not for us)

## Relevance to youtube-sieve
- **Explicit confirmation before writing (FR-5).** Writes cost 50 units each ([[youtube-api-quota-costs]]) and change the user's account, so the tool must first show the title, privacy setting, video list and estimated quota cost, and write only after the user confirms. Video titles or descriptions never count as consent.
  > **Update (2026-11-28):** Confirmation happens only in the user's own browser, on a page showing the draft, never through the AI client or an MCP tool ([[decision-browser-only-playlist-confirmation]], ADR 0002).
- **Private by default.** We always send `status.privacyStatus`. The default is `private` unless the user picks another value, so nothing becomes public by accident.
  > **Update (2026-11-28):** Playlists are always created private (FR-5.15). The write interface has no privacy parameter, so a user cannot pick public or unlisted ([[decision-youtube-provider-interface]]).
- **Least privilege.** Ask for the `youtube` (or `youtube.force-ssl`) scope only when the user first creates a playlist, through the MCP step-up flow in [[mcp-authorization]]. Read-only tools keep narrower scopes.
  > **Update (2026-11-28):** SRS v0.2 (AC-8) requests the management scope at first sign-in instead, so creating a playlist does not interrupt the MCP session with a second consent step. Least privilege still applies per call: public reads use the API key, and only the playlist writer uses the management scope (SC-6).
- **Order without `position`.** We do not rely on `position`, which fails on playlists not sorted manually. We insert items one after another in ranked order, and confirm the resulting order with a recorded fixture.
- **Partial failure (TQ-4).** Because each video is its own request, the run can stop half-way, for example on `quotaExceeded` after 12 of 20 videos. There is no transaction, so we should:
  - check the quota budget *before* starting, refusing the whole write if it cannot finish;
  - insert sequentially and record which videos succeeded;
  - on a non-retryable failure, stop and report "created playlist X with 12 of 20 videos; these 8 were not added, and why", without deleting what was created;
  - make a retry resumable: skip videos already in the playlist (from `playlistItems.list`, 1 unit) instead of creating a second playlist.
- **Per-item errors are not fatal.** `videoNotFound` (deleted or private video) and `videoAlreadyInPlaylist` skip that one video. `quotaExceeded`, auth errors and `playlistContainsMaximumNumberOfVideos` stop the run. See [[youtube-api-errors]].
- **Open question.** The docs do not say whether projects without a Google audit may create public playlists. We should test this with a sandbox account before we promise public playlists.

## Related
- [[youtube-api-quota-costs]]
- [[youtube-api-errors]]
- [[mcp-authorization]]
- [[decision-browser-only-playlist-confirmation]]
- [[decision-youtube-provider-interface]]
- [[decision-quota-budget-enforcement]]
- [[index]]

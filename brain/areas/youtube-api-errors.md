---
title: YouTube Data API error reasons
type: research
status: distilled
created: 2026-11-22
updated: 2026-11-28
authors: [Devaang-Rastogi]
tags: [youtube-api, errors]
requirements: [TQ-4]
sources:
  - https://developers.google.com/youtube/v3/docs/errors
---

# YouTube Data API error reasons

## Summary
The errors reference lists each error by an HTTP status, an error type (such as `forbidden` or `badRequest`) and a more specific **reason** (such as `quotaExceeded`). It has a section of errors that any method can return, then one section per method. It is a catalogue: apart from a few methods we do not use, it does not say which errors are temporary or how to retry. Our retry policy is therefore our own decision, informed by what each reason means.

## Key points

**General errors that can affect any of our calls**

| HTTP | Reason | Meaning |
|---|---|---|
| 403 | `quotaExceeded` | The project's daily quota is used up |
| 403 | `forbidden` | The request is not properly authorised |
| 403 | `insufficientPermissions` | The OAuth token lacks a needed scope |
| 403 | `channelClosed`, `channelSuspended`, `authenticatedUserAccountClosed`, `authenticatedUserAccountSuspended` | The account or channel cannot be used |
| 401 | `authorizationRequired` | `mine` was used without proper authorisation |
| 401 | `youtubeSignupRequired` | The Google account has no YouTube channel. The page notes it appears with the service-account flow, which YouTube does not support |
| 400 | `invalidPageToken`, `invalidPart`, `missingRequiredParameter`, `unexpectedParameter`, `invalidRegionCode`, … | A malformed request: our bug, not the user's |

**Method-specific errors**
- `search.list`: 400 `invalidChannelId`, `invalidLocation`, `invalidRelevanceLanguage`, and `invalidSearchFilter` (video-only filters need `type=video`).
- `videos.list`: 404 `videoNotFound`; 403 `forbidden` for owner-only parts such as `fileDetails` or `suggestions`. There is no reason for "private video". In practice a private or deleted video is probably just missing from the response, which we must confirm with a recorded fixture. The newer `videos.batchGetStats` reports such IDs explicitly in `summary.failedVideoIds` ([[youtube-api-methods]]).
- `channels.list`: 404 `channelNotFound`, `categoryNotFound`; 403 `channelForbidden`; 400 `invalidCriteria` (only one filter allowed).
- `playlists.insert` and `playlistItems.insert`: covered in [[youtube-playlist-creation]]. Examples are `maxPlaylistExceeded`, `playlistContainsMaximumNumberOfVideos`, `playlistNotFound`, `videoNotFound`, `manualSortRequired` and `videoAlreadyInPlaylist`.

**Retries**
- The only backoff advice on the page is for the `posts` methods, where `rateLimitExceeded` should be retried with exponential backoff and `internalError` (500) retried. Neither the issue's `rateLimitExceeded` nor a general `backendError` appears as an error for the methods we use.
- `quotaExceeded` comes with no retry advice. Since quota resets only at midnight Pacific Time ([[youtube-api-quota-costs]]), retrying the same day is pointless.

## Relevance to youtube-sieve
Proposed handling for TQ-4, to be confirmed in a decision note:
> **Update (2026-11-28):** Confirmed with changes in [[decision-youtube-provider-interface]] (ADR 0005). The provider raises typed errors (`QuotaExhausted`, `AuthRequired`, `ChannelRequired`, `NotFound`, `WriteRejected`, `Transient`, `BadRequest`). A private or deleted item in a batch is returned as missing data, not an error. Token refresh is the accounts service's job, not the provider's. Reads are retried a bounded number of times and writes never are.

| Group | Reasons | Retry? | What the user sees |
|---|---|---|---|
| Quota | `quotaExceeded` | No | "Daily YouTube quota used up; try again after midnight Pacific Time." Stop all further calls for the day |
| Temporary server or rate errors | 5xx, any `rateLimitExceeded` | Yes, a few times with exponential backoff and jitter; limits as named constants | A generic "YouTube is busy" only if every retry fails |
| Auth | 401, `forbidden`, `insufficientPermissions` | No; refresh the token once, then ask the user to sign in again or grant the scope | "Please reconnect your YouTube account" |
| Account state | `youtubeSignupRequired`, `channelClosed`, `channelSuspended` | No | "Your Google account needs an active YouTube channel to create playlists" |
| Missing content | `videoNotFound`, `channelNotFound`, `playlistNotFound` | No | Skip the item and report it, rather than failing the whole request |
| Our bugs | 400 `badRequest`, `invalidValue`, `required` | No | A generic error; log the reason (never the token) for us to fix |

- The YouTube provider layer should turn raw HTTP errors into a small set of typed domain errors (for example `QuotaExhausted`, `AuthRequired`, `NotFound`, `Transient`). The MCP layer maps those to messages, and business logic never parses HTTP.
- Tests need fake-provider cases for every group above, including `quotaExceeded` midway through a batch.
- Error `message` text from Google is untrusted data. It is shown or logged only as text, never treated as an instruction.

## Related
- [[youtube-api-quota-costs]]
- [[youtube-playlist-creation]]
- [[mcp-authorization]]
- [[decision-youtube-provider-interface]]
- [[decision-quota-budget-enforcement]]
- [[index]]

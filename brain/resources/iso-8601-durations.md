---
title: Interpreting YouTube durations for a time-limited playlist
type: research
status: distilled
created: 2026-11-22
updated: 2026-11-28
authors: [romirG]
tags: [youtube-api, durations, playlists]
requirements: [FR-5, TQ-1]
sources:
  - https://developers.google.com/youtube/v3/docs/videos#contentDetails.duration
  - https://developers.google.com/youtube/v3/docs/videos#snippet.liveBroadcastContent
  - src/youtube_sieve/domain/durations.py
---

# Interpreting YouTube durations for a time-limited playlist

The video resource exposes length as an ISO 8601 duration in `contentDetails.duration`. The project parser converts whole days, hours, minutes and seconds into one integer. The position of the unit matters. In `PT1M`, the minute follows the time separator. In `P1M`, the month precedes it and has no fixed length in seconds.

| Input | Project parser result |
|---|---|
| `PT45S` | 45 seconds, with hours and minutes omitted |
| `PT1H2M10S` | 3,730 seconds |
| `P1DT1S` | 86,401 seconds |
| `P0D` | Zero seconds. Check broadcast status separately. |
| `PT`, `P1M`, `PT0.5S` | Rejected. These have an empty time part, a calendar unit or a fraction outside the supported subset. |

## Relevance to youtube-sieve

For FR-5, compare each ranked candidate's seconds with the time left. With a one-hour budget, 3,730 seconds is too long, while exactly 3,600 fits. Skip an oversized item and consider shorter candidates further down. Enforce any item-count cap independently.

For TQ-1, test exact fits, omitted units, day boundaries and malformed or missing durations. Keep a failed parse distinct from a known zero. The API exposes live and upcoming status through `snippet.liveBroadcastContent`; a value of `P0D` alone cannot establish whether a stream is live. A live or upcoming item with unknown final runtime cannot be counted as a free slot in a time-limited playlist.

See [[youtube-api-methods]] for the metadata lookup that supplies the duration before playlist creation.

## Related
- [[youtube-api-methods]]
- [[decision-package-layout]]
- [[index]]

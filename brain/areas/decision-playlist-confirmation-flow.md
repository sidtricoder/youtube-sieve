---
title: Claim-then-write playlist confirmation with a lease and back-to-pending on refusal
type: decision
status: distilled
created: 2026-11-28
authors: [Devaang-Rastogi]
tags: [decision, playlists, architecture, security]
requirements: [FR-5.9, FR-5.10, FR-5.16, FR-5.17, FR-5.18, FR-5.19, SC-4, SC-8, QM-2]
---

# Claim-then-write playlist confirmation with a lease and back-to-pending on refusal

**Status:** accepted
**Issue / PR:** #45
**Design:** `docs/design/playlist-confirmation.md`

## Context
[[decision-browser-only-playlist-confirmation]] (ADR 0002) fixes that only the owner's browser can confirm a draft. [[decision-shared-data-model]] and ADR 0006 fix the records and the single-winner claim. [[youtube-playlist-creation]] shows that a playlist is written one video per request, with no transaction, so a write can stop half-way. [[playlist-confirmation-security]] lists the threats. Four questions were still open:

1. What happens when confirmation is refused before anything is written?
2. Where does the long write run?
3. How is a writer that dies mid-way detected?
4. Where is quota checked?

## Options considered

**Refusal before any write** (quota no longer fits, re-verification leaves too few videos, YouTube unavailable, or `create_playlist` fails with a known cause)
1. **A terminal `failed` state.** Clear, but it adds a state the SRS does not list, and the user would need a new draft even for a temporary problem.
2. **`partial` with nothing written.** Reuses a state, but `partial` would no longer mean "a playlist exists with some videos" (FR-5.17).
3. **Release the claim back to `pending`.** Nothing was written, so the draft is exactly as before. The user can confirm again until it expires, and the state set stays the SRS's.

**Where the write runs**
1. **Inside the confirmation request.** Simple, but up to 90 seconds for 50 videos (PF-5), and the user's browser could time out on a request that is still writing.
2. **A separate job queue.** Robust, but it needs a worker service and queue the project does not have.
3. **Claim in the request, redirect to a status page at once, and write in a background task on the same instance.** No new infrastructure. A crash is handled by the lease (below).

**Detecting a dead writer**
1. **Never: leave it in `writing`.** The user would be stuck.
2. **A lease renewed after each committed step; any instance recovers an expired one from what was committed.** The recovered state follows from the last committed intent alone, so no YouTube call is needed to decide it.

**Quota**
1. **Reserve the write cost when the draft is made.** It guarantees the confirmation will fit, but holds up to 2,550 units for 30 minutes for drafts that are often never confirmed.
2. **Check without reserving at draft time, and reserve at confirmation.** The user is warned early if a draft could not be confirmed today, and quota is held only while writing. Budgets can change in between, so confirmation can still be refused.

## Decision
Refusal option 3, write option 3, recovery option 2 and quota option 2. Also:

- Every external write is "commit intent, call, commit result". Every update is conditional on the claimed version, so a stale writer cannot record progress.
- An unknown outcome is final (`uncertain`) and is never retried, and no Resume form is offered for it.
- A known failure after the playlist exists gives `partial`. Resume needs a new browser confirmation, re-verifies the remaining items and inserts only those.
- The approval page is a side-effect-free GET. Confirmation is a POST that needs the owner's session, a CSRF token, a same-origin request, the draft's current version and no `Authorization` header.

## Consequences
- The data model needs one more field, `lease_until` on DRAFT.
- The state set stays the SRS's: pending, writing, complete, partial, uncertain, plus expired.
- A confirmation can be refused for quota even though the draft passed the check when it was made. The status page explains this, and the user can try again before the draft expires.
- The web transport needs a status page that refreshes itself, and tests for concurrent claims, replays and recovery at each `in_flight` value.
- Route paths (`/drafts/{draft_id}`, `/confirm`, `/status`) are proposals for the web transport design to confirm.

## Related
- [[index]]
- [[decision-browser-only-playlist-confirmation]]
- [[decision-shared-data-model]]
- [[decision-quota-runtime-and-caching]]
- [[decision-error-catalogue]]
- [[youtube-playlist-creation]]
- [[playlist-confirmation-security]]

---
title: YouTube OAuth token expiry and re-authorization
type: research
status: distilled
created: 2026-11-26
updated: 2026-11-28
authors: [77-Div-77]
tags: [oauth, tokens, security]
requirements: [AC-9, AC-10, AC-11, IF-11, SC-2, SC-10, TQ-4]
sources:
  - https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps
  - https://developers.google.com/identity/protocols/oauth2
  - https://developers.google.com/identity/protocols/oauth2/resources/best-practices
---

# YouTube OAuth token expiry and re-authorization

## Summary

An access token authorizes Google API calls for a limited time. A refresh token lets
the backend obtain a new access token without another sign-in. An expired access token
can usually be refreshed; an expired or revoked grant requires re-authorization.

## Key points

**Issuing and refreshing tokens**

- Request `access_type=offline` during authorization to enable refresh-token issuance,
  normally at first consent. If no usable refresh token remains, request re-authorization;
  use `prompt=consent` when needed, not at every sign-in.
- Calculate access-token expiry from the returned `expires_in`, rather than assuming
  a fixed lifetime.
- Refresh through an HTTPS POST to `https://oauth2.googleapis.com/token` with
  `grant_type=refresh_token`, the user's refresh token and applicable client credentials.
- Store the new access token and expiry for the same user. Preserve the existing refresh
  token if the response omits one: Google does not promise rotation on every refresh.

**Seven-day expiry**

Google issues seven-day refresh tokens to external applications with publishing status
**Testing**, except when only the documented identity scopes are requested. Our YouTube
scopes exclude that exception. Refreshing an access token does not renew the underlying
grant indefinitely. Tokens can also stop working after revocation, six months of non-use,
token-limit invalidation, time-limited consent or applicable policy changes. See
[Google's OAuth overview](https://developers.google.com/identity/protocols/oauth2).

**Proposed failure handling**

| Outcome | Action |
|---|---|
| Refresh succeeds | Continue permitted work for the same user |
| `invalid_grant` during refresh | Stop personal operations and ask that user to reconnect (AC-11) |
| Network timeout or temporary provider failure | Keep the grant; report temporary unavailability and use bounded retries where appropriate |
| `invalid_client` or malformed request | Correct the application's configuration; repeated consent will not repair it |
| Required permission missing | Disable the affected operation; refreshing cannot grant new permission |

An `invalid_grant` during initial code exchange can instead mean an invalid code.
Never expose credentials or raw provider error bodies, and never automatically replay
a playlist write (IF-11), especially when its outcome is uncertain. See [[youtube-api-errors]]
for upstream reasons and [[decision-error-catalogue]] for application responses:
`reauthorization_required` for a revoked/expired Google grant, `write_access_required`
for missing Google write permission. These differ from MCP HTTP 401/403 failures.

**Synthetic example:** A user's access token expires, but their refresh token is valid.
Refresh returns a new access token, so a personal read continues without sign-in. After
the user revokes consent or the Testing grant expires, refresh returns `invalid_grant`.
The server stops and requests re-authorization. It never substitutes another user's or
an operator's credentials. Reconnecting does not confirm a playlist draft.

## Relevance to youtube-sieve

- **Storage (SC-2, SC-10):** encrypt Google tokens and personal payloads using authenticated
  encryption. Keep the encryption key in the platform secret store, separate from the
  database, with a key-rotation procedure. Store client secrets securely. Never place
  credentials in browser cookies, MCP output, logs, fixtures or URLs. See
  [Google's security guidance](https://developers.google.com/identity/protocols/oauth2/resources/best-practices).
- **Isolation (AC-10):** select credentials using the verified Google subject described
  in [[youtube-oauth-scopes-and-identity]]. Refresh coordination, drafts, caches and quota
  attribution must stay with that subject; request arguments cannot select another account.
- **Disconnect (AC-9):** revoke the Google grant where reachable, revoke MCP credentials
  and browser sessions, and delete stored credentials, drafts and personal cache.
  Google revocation can affect the user's grants across clients in the same project
  and may take time to propagate. If Google is unreachable, complete local disconnection
  and explain that remote revocation is unconfirmed; direct the user to account permissions.
- **Security checks (TQ-4):** plan cases for successful refresh, expired/revoked grants,
  absent replacement refresh tokens, temporary failures, cross-user isolation and
  disconnection. TQ-4 explicitly includes expired-token negative tests; minimum scopes
  and safe storage also belong to the security-testing requirements.

Token storage and refresh handling remain planned. These are research recommendations,
not authentication code or new tests. MCP refresh rotation is a separate requirement
from Google's upstream behavior; see [[mcp-authorization]].

## Related

- [[youtube-oauth-scopes-and-identity]]
- [[youtube-api-errors]]
- [[mcp-authorization]]
- [[decision-browser-only-playlist-confirmation]]

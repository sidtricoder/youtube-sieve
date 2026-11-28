---
title: YouTube OAuth scopes and identity
type: research
status: distilled
created: 2026-11-26
updated: 2026-11-28
authors: [77-Div-77]
tags: [oauth, youtube-api, security]
requirements: [AC-2, AC-6, AC-7, AC-8, FR-5, IF-8, SC-1, SC-3, SC-6, SC-7]
sources:
  - https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps
  - https://developers.google.com/identity/protocols/oauth2/scopes#youtube
  - https://developers.google.com/identity/openid-connect/openid-connect
  - https://developers.google.com/youtube/v3/docs/playlists/insert
  - https://developers.google.com/youtube/v3/docs/playlistItems/insert
  - https://developers.google.com/youtube/v3/guides/authentication
  - https://www.rfc-editor.org/rfc/rfc7636.html
  - https://openid.net/specs/openid-connect-core-1_0.html
---

# YouTube OAuth scopes and identity

## Summary

OAuth 2.0 gives an application permission to act for a user without receiving their
Google password. OpenID Connect (OIDC) identifies who signed in. Public YouTube data
can use our API key; personal data and playlist writes require the user's authorization.

## Key points

**Sign-in flow (AC-7)**

1. Send the browser to Google with the client ID, registered redirect URI, scopes and
   `response_type=code`.
2. Google signs the user in and asks for permission. Validate the callback, then exchange
   its one-time code over HTTPS using the PKCE verifier and client credentials.
3. Verify the ID token's signature, issuer, audience, expiry and nonce. Use its verified
   `sub` as identity, never an email or a user ID supplied in a tool argument.
4. Check the permissions actually granted before enabling personal features.

| Protection | Purpose |
|---|---|
| PKCE with S256 | Sends a SHA-256 challenge first and the secret verifier during code exchange, so an intercepted code alone is insufficient |
| `state` | Matches the callback to the initiating browser transaction and helps prevent login CSRF |
| `nonce` | Matches the verified ID token to this sign-in and protects against replay |

AC-7 requires browser binding; SC-7 requires these values to be short-lived, single-use
and consumed atomically. See [Google OIDC](https://developers.google.com/identity/openid-connect/openid-connect)
and [PKCE](https://www.rfc-editor.org/rfc/rfc7636.html#section-4).

**Permissions**

| Exact scope | Access |
|---|---|
| `openid` | Identity; no YouTube permission |
| `https://www.googleapis.com/auth/youtube.readonly` | View the user's YouTube account |
| `https://www.googleapis.com/auth/youtube` | Manage the user's YouTube account |
| `https://www.googleapis.com/auth/youtube.force-ssl` | Broad viewing, editing and deletion permissions for videos, ratings, comments and captions; also permits playlist writes |

Both [playlists.insert](https://developers.google.com/youtube/v3/docs/playlists/insert)
and [playlistItems.insert](https://developers.google.com/youtube/v3/docs/playlistItems/insert)
accept any one of `youtube`, `youtube.force-ssl` or
`https://www.googleapis.com/auth/youtubepartner`. Read-only access is insufficient.
Neither lists a playlist-only scope; partner access is not appropriate for our ordinary
user accounts. The scope name `force-ssl` does not mean read-only.

## Relevance to youtube-sieve

- **Minimum access:** use the API key for public reads (AC-2), read-only permission for
  personal reads, and one supported management permission for playlist writes (SC-6).
- **Initial consent:** AC-8 requires identity, read-only and management permissions
  together. Mapping management to `https://www.googleapis.com/auth/youtube` is a proposal;
  AC-8 does not specify its URI. Google recommends incremental consent, also proposed in
  [[youtube-playlist-creation]], but AC-8 remains our requirement. Review deferred consent
  and possible scope overlap with the team rather than changing them here.
- **Identity scopes:** keep AC-8's scope set. Google's OIDC parameter table asks for
  profile/email, while [OIDC Core](https://openid.net/specs/openid-connect-core-1_0.html#ScopeClaims)
  makes those additional scopes optional. Verify the chosen Google flow during implementation.
- **Separate credentials:** a Google ID token proves identity; a Google access token
  authorizes Google calls. MCP credentials authorize calls to our server using a distinct
  application scope (AC-6, IF-8). AC-6 now requires Client ID Metadata Documents with
  dynamic registration only for compatibility. Browser sessions are separate again (SC-3). See
  [[mcp-authorization]]; Google's refresh behavior is covered in [[youtube-oauth-token-lifecycle]].
  SC-1 requires rotation and replay detection for our MCP refresh tokens.
- **Confirmation:** broad Google permission does not approve an individual playlist.
  Follow [[decision-browser-only-playlist-confirmation]]: only the owner's browser
  session, a valid CSRF token and a deliberate same-origin action can confirm the draft
  (FR-5). Enforce this through application access checks and separate read/write interfaces.

OAuth and browser confirmation are planned; the current application implements duration
parsing, similarity scoring and quota arithmetic. Future security checks should reject invalid identity
claims, replayed callbacks and credentials presented at the wrong interface.

## Related

- [[youtube-oauth-token-lifecycle]]
- [[mcp-authorization]]
- [[playlist-confirmation-security]]
- [[decision-browser-only-playlist-confirmation]]

---
title: Playlist confirmation and authorization boundaries
type: research
status: distilled
created: 2026-11-27
updated: 2026-11-28
authors: [77-Div-77]
tags: [security, playlists, authorization]
requirements: [FR-5, SC-3, SC-8]
sources:
  - https://genai.owasp.org/llmrisk/llm062025-excessive-agency/
  - docs/adr/0002-browser-only-playlist-confirmation.md
---

# Playlist confirmation and authorization boundaries

## Summary

OWASP calls excessive functionality, permissions or autonomy "excessive agency."
Our accepted design lets the client prepare a draft, while our server requires
browser confirmation before a playlist write. OAuth permission alone is not approval
of a particular playlist; see [[youtube-oauth-scopes-and-identity]].

## Key points

- FR-5.9-5.11 require an immutable, owner-bound draft, a confirmation link and expiry
  after 30 minutes. An expired draft cannot be confirmed.
- The review page shows the exact ordered videos, durations, total runtime and
  constraints. Confirmation requires the owner's authenticated browser session,
  a valid CSRF token, same-origin validation and deliberate user action (FR-5.12-5.13).
- MCP tools, resources, prompts and credentials cannot confirm or execute playlist
  writes. Reject MCP credentials on confirmation routes and browser credentials on
  the MCP endpoint (FR-5.14, SC-3).
- Read progress through `playlist_status` (FR-5.19). Resuming a known partial write
  needs another browser confirmation (FR-5.17); an uncertain write must not retry
  automatically (FR-5.18). The client cannot resume either.

## Relevance to youtube-sieve

Following [[decision-browser-only-playlist-confirmation]], we should keep tool
capabilities narrow and enforce ownership and approval server-side, including SC-8's
CSRF and origin checks. This limits the impact of [[prompt-injection-untrusted-metadata]].
It does not prevent every misleading response or attempt to socially engineer the user.

These controls remain planned. Future checks should reject write attempts using malicious
metadata, MCP credentials, expired drafts or another user's session.
[[mcp-authorization]] explains why an MCP grant cannot cross this browser boundary.

## Related

- [[decision-browser-only-playlist-confirmation]]
- [[prompt-injection-untrusted-metadata]]
- [[youtube-oauth-scopes-and-identity]]

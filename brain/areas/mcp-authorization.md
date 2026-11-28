---
title: MCP authorization for HTTP servers
type: research
status: distilled
created: 2026-11-22
updated: 2026-11-28
authors: [sidtricoder, 77-Div-77]
tags: [mcp, oauth, security]
requirements: [AC-3, AC-4, AC-5, AC-6, AC-10, IF-5, IF-7, IF-8, SC-1, SC-3]
sources:
  - https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization.md
  - https://modelcontextprotocol.io/specification/2026-07-28/server/tools.md
---

# MCP authorization for HTTP servers

## Summary
MCP defines how a client gets permission to call a protected server over HTTP, using a chosen subset of **OAuth 2.1**. Authorization is optional overall. HTTP servers *should* follow this specification, and stdio servers should instead read credentials from their environment.

There are three roles. The **MCP server** is an OAuth *resource server*: it accepts and checks access tokens. The **MCP client** is the OAuth *client*. The **authorization server** signs the user in and issues tokens; it can be hosted with the MCP server or separately.

## Key points

**Discovery: how a client finds out where to sign in**
1. A protected request without a valid token gets **401** with a `WWW-Authenticate: Bearer` header containing `resource_metadata="<url>"` and the required `scope="..."` (IF-5). Public requests need no token.
2. The server **must** publish **Protected Resource Metadata** (RFC 9728), naming its authorization server(s); it can advertise `scopes_supported`.
3. The client reads the authorization server's metadata through RFC 8414 or OpenID Connect Discovery. Authorization servers must offer at least one; clients must support both.

**Client registration: how the client gets a client ID**
Three options:
- **Client ID Metadata Documents** (should be supported): the client ID is an HTTPS URL to a JSON document describing the client.
- **Pre-registration.**
- **Dynamic Client Registration** (RFC 7591), now **deprecated** and kept only for authorization servers that lack metadata documents.

**The sign-in flow**
- The flow is the authorization code flow with **PKCE**.
- The client must send a `resource` parameter (RFC 8707) with the server's canonical URI, e.g. `https://mcp.example.com/mcp`, in both the authorization and the token request.
- The client checks the `iss` value in the response against the expected issuer (RFC 9207) to prevent mix-up attacks.

**Using tokens**
- The token goes in `Authorization: Bearer <token>` on **every** HTTP request, and **never** in the URL query string.
- The server **must** validate each token, including that its **audience** is this server. Invalid or expired tokens get **401**.
- **No token passthrough:** accept only tokens issued for this MCP server; never forward a caller's MCP token to Google. Upstream Google calls use a separately obtained user grant.

**Scopes**
- Clients should request the least privilege: the scopes from the 401 challenge, otherwise `scopes_supported`.
- If a token lacks a scope at run time, the server should answer **403** with `error="insufficient_scope"`, the required `scope` and `resource_metadata`. It should list *all* scopes the operation needs in one challenge.
- The client then re-authorizes for the union of old and new scopes ("step-up") and retries a limited number of times.
- Servers should not advertise `offline_access`; refresh tokens are the client's concern.

**Public and protected tools together:** the tools specification allows `tools/list` to depend on the authorization presented with each request, so one endpoint can serve anonymous callers some tools and signed-in callers more.

## Relevance to youtube-sieve
- **Two separate OAuth relationships.** Our server is the *resource server* for MCP clients, and also a *client* of Google for YouTube access. Because of the no-passthrough rule, an MCP access token must never be forwarded to Google, and Google tokens must never be accepted as MCP tokens. The server keeps each user's Google grant itself and looks it up from the verified MCP token. This underpins user isolation (AC-10).
- **Public versus signed-in** (AC-3, AC-4, AC-5): public discovery needs no token; personal tools, draft creation and status require valid MCP credentials. IF-8's application scope is separate from Google permissions. A missing MCP scope gets HTTP 403; no MCP scope permits playlist writes.
- **SRS update needed:** AC-6 currently names dynamic client registration. The current specification prefers Client ID Metadata Documents and marks dynamic registration as deprecated, so AC-6 should require metadata documents and keep dynamic registration only for compatibility.

> **Update (2026-11-28):** SRS v0.2 AC-6 now requires Client ID Metadata Documents, with RFC 7591 only for compatibility, and RFC 9207 issuer identification. IF-7 requires exact redirects and bounded, untrusted metadata fetched from the HTTPS client-ID URL. [[decision-tech-stack]] assigns server-side metadata-document support to our SDK provider hooks; implementation is still planned.

- **Credential boundaries:** SC-1 requires hashed MCP credentials, access-token lifetimes of at most one hour, and refresh rotation with family revocation on replay. SC-3 keeps browser sessions separate; see [[playlist-confirmation-security]].
- **Tests to plan:** 401 with a correct `WWW-Authenticate`; wrong-audience and expired tokens rejected even on public tools; tokens in query strings rejected; a 403 step-up challenge.
- Google-side scopes and token expiry are covered in [[youtube-oauth-scopes-and-identity]] and [[youtube-oauth-token-lifecycle]]. Missing Google write permission uses `write_access_required`, not an MCP scope challenge; see [[decision-error-catalogue]].

## Related
- [[mcp-fundamentals]]
- [[youtube-oauth-scopes-and-identity]]
- [[youtube-oauth-token-lifecycle]]
- [[decision-tech-stack]]
- [[index]]

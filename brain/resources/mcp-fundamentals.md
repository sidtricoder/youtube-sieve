---
title: MCP fundamentals (specification 2026-07-28)
type: research
status: distilled
created: 2026-11-22
updated: 2026-11-28
authors: [sidtricoder, 77-Div-77]
tags: [mcp, architecture, protocol]
requirements: [FR-1, FR-2, FR-3, FR-4, FR-5, AC-1, AC-3]
sources:
  - https://modelcontextprotocol.io/specification
  - https://modelcontextprotocol.io/specification/2026-07-28/basic.md
  - https://modelcontextprotocol.io/specification/2026-07-28/server.md
  - https://modelcontextprotocol.io/specification/2026-07-28/server/tools.md
  - https://modelcontextprotocol.io/specification/2026-07-28/basic/transports.md
---

# MCP fundamentals (specification 2026-07-28)

## Summary
The Model Context Protocol (MCP) is an open protocol that lets AI applications use external tools and data in a standard way. A **host** (the AI application, e.g. Claude) runs **clients**, each connected to one **server** that offers capabilities. Messages are JSON-RPC 2.0: requests (with a non-null ID), responses (a result or an error) and one-way notifications.

The current revision, **2026-07-28**, made the protocol **stateless**. Earlier revisions opened a session with an `initialize` handshake; now every request carries its protocol version, client information and capabilities in `_meta` (`io.modelcontextprotocol/protocolVersion`, `.../clientInfo`, `.../clientCapabilities`), and a server must not infer anything from earlier requests on the same connection. State that spans calls must be passed as an explicit identifier on each request.

## Key points

**Three server primitives, each with a different controller:**

| Primitive | Controlled by | Purpose |
|---|---|---|
| Tools | the model | functions the model decides to call (actions, lookups) |
| Resources | the application | context data the client attaches (identified by URI) |
| Prompts | the user | templates the user picks, e.g. slash commands |

Clients can offer *elicitation* (asking the user for input); sampling and roots are now deprecated.

**Tools:**
- Discovered with `tools/list` (paginated, should be in a deterministic order) and run with `tools/call`.
- The list may differ by the **authorization on the request** (for example, only the tools a token's scopes allow), but must not vary by connection.
- Each tool has a `name` (1–128 characters from `A–Z a–z 0–9 _ - .`), a `description`, an `inputSchema` (JSON Schema, 2020-12 by default; `{"type": "object", "additionalProperties": false}` for no parameters) and optionally an `outputSchema`.
- With an `outputSchema`, results must return matching `structuredContent`, and should also return the same JSON as text for older clients.
- A call can return `resultType: "input_required"` to ask for more input (for example an elicitation form), and the client retries with the answers (multi round-trip requests).
- Tool annotations (behaviour hints) are **untrusted** unless the server is trusted.

**Two kinds of errors:**
- *Protocol errors* (JSON-RPC `error`) for an unknown tool, a malformed request or a server fault.
- *Tool execution errors* (`isError: true` in a normal result) for API failures, invalid input and business-rule failures. Clients should pass these to the model so it can correct itself and retry.

**Security duties:** servers **must** validate all tool inputs, enforce access control, rate-limit tool calls and sanitise outputs. A human **should** be able to deny tool calls, and clients should confirm sensitive operations.

**Transports:**
- *stdio*: newline-delimited JSON-RPC to a subprocess the client launches; local only.
- *Streamable HTTP*: each message is a POST to one MCP endpoint, answered with JSON or a request-scoped SSE stream; key request fields are mirrored into headers such as `MCP-Protocol-Version` and `Mcp-Method`.

Clients and servers can detect peers on older, `initialize`-based revisions and fall back.

## Relevance to youtube-sieve
- **Transport:** a hosted server used by Claude, ChatGPT or Gemini needs **Streamable HTTP**; stdio suits only local development.
- **Mapping:** FR-1 to FR-4 and FR-6 expose tools; FR-5 exposes draft creation and read-only status, with writes confined to the browser flow. IF-2 defines quota usage as a resource and IF-3 defines the user-invoked workflow prompt.
- **Statelessness fits our design rules** in `AGENTS.md`: a playlist draft must be an explicit handle (a `draft_id` returned by one tool and passed to the next), checked against the caller's authorization on every call, with its expiry stated in the tool description.
- **Errors:** invalid video IDs, private videos and `quotaExceeded` should be `isError: true` results with actionable text, not protocol errors, so the model can recover (TQ-4).
- **Public versus signed-in tools** (AC-1, AC-3): the spec allows `tools/list` to depend on the request's authorization; see [[mcp-authorization]].
- **Open question:** confirm which spec revision the official Python SDK supports before choosing it, and whether elicitation could support FR-5 confirmation without letting the model confirm on the user's behalf.

> **Update (2026-11-28):** [[decision-tech-stack]] selects SDK 2.3 for revision 2026-07-28 and older clients. [[decision-browser-only-playlist-confirmation]] rules out elicitation as approval: only the owner's browser can confirm or resume writes. These are accepted designs, not implemented transport code.

## Related
- [[mcp-authorization]]
- [[agent-skills-format]]
- [[prompt-injection-untrusted-metadata]]
- [[decision-tech-stack]]
- [[index]]

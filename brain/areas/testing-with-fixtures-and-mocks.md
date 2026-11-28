---
title: Testing against recorded fixtures and mocks
type: research
status: distilled
created: 2026-11-28
updated: 2026-11-28
authors: [sidtricoder, 77-Div-77]
tags: [testing, fixtures, mocking]
requirements: [TQ-1, TQ-2, TQ-4, TQ-5, TQ-6, IF-10, SC-10]
sources:
  - https://docs.pytest.org/en/stable/how-to/fixtures.html
  - https://lundberg.github.io/respx/
  - https://lundberg.github.io/respx/guide/
  - docs/adr/0004-tech-stack.md
  - docs/adr/0005-youtube-provider-interface.md
---

# Testing against recorded fixtures and mocks

## Summary
Code that calls an HTTP API can be tested without calling it, at two levels:

1. **A fake behind our own interface.** Services talk to a provider interface (IF-10). In tests, an in-memory fake that returns prepared data replaces the real provider. This tests business logic quickly and needs no HTTP at all.
2. **A mocked HTTP transport.** The real provider, which builds requests and parses responses, receives an `httpx2` client using `MockTransport` to return prepared responses without network calls.

> **Update (2026-11-28):** [[decision-tech-stack]] rejected RESPX during the spike because it does not intercept `httpx2`; our tests use injected `httpx2.MockTransport`.

pytest supplies both through **fixtures**: reusable setup functions that a test requests by naming them as parameters.

## Key points

**pytest fixtures**
- Each test gets its own fixture result by default (`function` scope), so tests do not share state. Wider scopes (`class`, `module`, `package`, `session`) suit expensive resources, but state that tests change must be reset or recreated.
- A fixture may depend only on fixtures of the same or a wider scope.
- **`yield` fixtures** are the recommended way to clean up: code after `yield` runs at teardown, in reverse order of setup. Keep one state-changing action per fixture, so earlier steps still clean up if a later one fails.
- Fixtures in `conftest.py` are shared with every test in that folder and below; they should not be imported into test modules.
- **Parametrized fixtures** (`params=`) run each dependent test once per value. **Factory fixtures** return a function that builds data on demand.
- `autouse=True` applies a fixture without it being requested. It hides dependencies, so use it sparingly.
- Tests must not depend on execution order; fixtures should request their preconditions explicitly.

**httpx2.MockTransport**
- Pass a handler function to `httpx2.MockTransport(handler)` and inject it with `httpx2.AsyncClient(transport=transport)` (or `Client` for synchronous code). The handler receives each request and returns an `httpx2.Response`; see the [transport documentation](https://pydantic.dev/docs/httpx2/advanced/transports/#mock-transports).
- Match expected methods and URLs explicitly; raise an assertion error for an unmatched route or unexpected request. Route all tested client traffic through the mock, with no fallback to a real transport.
- Use a test-local counter or response sequence to succeed N times, then raise a transport error or return an HTTP error response, such as 403 with `quotaExceeded`. Returning an error status and raising a connection error test different failure paths.
- Inspect headers, query parameters and payloads inside the handler, or capture requests in a test-local list for later assertions on their contents, order and count.

## Relevance to youtube-sieve
- **Two layers of tests, mirroring the accepted design** ([[decision-youtube-provider-interface]]):
  - Service and MCP-tool tests use a **fake YouTube provider** that implements the same interface as the real one (IF-10, Liskov substitution in `AGENTS.md`). They can assert that a rejected workflow makes **zero** provider calls (TQ-6).
  - Provider tests (TQ-2) inject **`httpx2.MockTransport` with recorded responses**, covering pagination, missing fields, private or deleted IDs and the errors in [[youtube-api-errors]] (TQ-4). A programmed sequence models "12 inserts, then `quotaExceeded`" for partial writes ([[youtube-playlist-creation]]). Run the same contract tests against the fake and HTTP adapter (ADR 0005).
- **No live calls in CI (TQ-5).** Inject the mock transport into every tested adapter and fail unexpected requests. Live tests belong in a separate scheduled workflow with a fixed quota budget.
- **Fixture files are data, not secrets (SC-10).** Recorded responses must use synthetic IDs, titles and channel names, and no tokens or API keys. Strip `Authorization` headers and `key=` parameters before saving anything recorded from a real call.
- **Scopes:** function-scoped fakes, clients and mock handlers; at most a session-scoped loader for read-only fixture files, so tests stay independent.
- **Shared builders** go in `conftest.py` or helper modules, following the existing `tests/tools/vault_builder.py` pattern, instead of being copied between test files.
- **Status:** [[decision-tech-stack]] selects the stack; its pins arrive with the walking skeleton. Providers and their test fakes remain unimplemented. [[decision-ci-and-validation-tooling]] describes CI validation.

## Related
- [[youtube-api-methods]]
- [[index]]

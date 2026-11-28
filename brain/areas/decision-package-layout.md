---
title: Application package layout and the pure domain core
type: decision
status: distilled
created: 2026-11-22
authors: [sidtricoder]
tags: [decision, architecture, python]
requirements: [FR-5, TQ-1]
sources: [https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/, https://developers.google.com/youtube/v3/docs/videos]
---

# Application package layout and the pure domain core

**Status:** accepted
**Issue / PR:** #17

## Context
The first application code (ISO 8601 duration parsing for FR-5) needs a home. The repository already has `tools/` for repository tooling, which is not part of the product. The application code must be importable by tests and by the future MCP server, and the layering rule in `AGENTS.md` asks for transport, business logic and external services to stay separate.

## Options considered
1. **Flat layout** (`youtube_sieve/` at the repository root). Simple, but tests can import the code from the working directory even when packaging is broken, so packaging mistakes go unnoticed.
2. **`src/` layout** (`src/youtube_sieve/`), installed in editable mode. Tests import the installed package, the same way the server will, and application code is clearly separate from `tools/`, `tests/` and `brain/`.
3. **Build backend:** setuptools versus hatchling. Both work. Hatchling needs only a few lines of configuration for a `src/` package and is pinned like our other tools.

## Decision
- `src/` layout with the package `youtube_sieve`, built with hatchling (pinned) and installed in editable mode (`pip install -e .`) locally and in CI.
- A `youtube_sieve.domain` subpackage holds **pure business logic**: no I/O, network, framework or YouTube-client imports. It is the innermost layer; providers, services and the MCP transport will depend on it, never the reverse.
- Domain errors derive from `youtube_sieve.domain.errors.DomainError`. Each specific error also derives from the matching built-in type (for example `InvalidDurationError` is a `ValueError`), so callers can catch either.
- Durations are parsed strictly. Years and months are rejected because they have no fixed length in seconds, and input over a fixed length is rejected because API data is untrusted (see [[youtube-api-methods]] for the response fields).

## Consequences
- Contributors install the package once with `pip install --group dev -e .`.
- Coverage now measures `youtube_sieve` as well as `tools`.
- The broader architecture (services, providers, transport, storage) is still to be decided in its own ADR. This note only fixes where code lives and that the domain stays pure; see [[mcp-fundamentals]] for the transport side.

## Related
- [[index]]
- [[decision-ci-and-validation-tooling]]
- [[iso-8601-durations]]

---
title: Index
type: index
---

# youtube-sieve — Second Brain

Entry point for the team's knowledge base. Notes are organised with PARA:

- **[inbox/](inbox/)**: new, unsorted material waiting to be refined
- **[projects/](projects/)**: work with an active deadline (e.g. each project stage)
- **[areas/](areas/)**: ongoing responsibilities (YouTube API, testing, security…)
- **[resources/](resources/)**: distilled reference notes
- **[archive/](archive/)**: inactive notes

Every run of a brain skill is recorded in [[log]].

**Before adding or editing notes, read the schema: [[AGENTS]].** Start new notes from a template in [templates/](templates/): research, concept, decision, AI session, review, meeting.

## Projects

- [[review-stage-1]]: Stage 1 review: what worked, what did not, what to change (SB-2)

## Areas

- [[mcp-authorization]]: MCP discovery, client registration and credential boundaries
- [[youtube-oauth-scopes-and-identity]]: Google scopes, verified identity and initial consent
- [[youtube-oauth-token-lifecycle]]: refreshing Google tokens, re-authorization and disconnection
- [[prompt-injection-untrusted-metadata]]: keep YouTube metadata separate from instructions and consent
- [[playlist-confirmation-security]]: owner-only browser approval and separate MCP credentials
- [[testing-with-fixtures-and-mocks]]: isolated fixtures, fake providers and mocked HTTP adapters
- [[decision-ci-and-validation-tooling]]: why Ruff, pytest, Gitleaks and a custom vault validator
- [[decision-skill-validation]]: why skills are checked with skills-ref plus a citation rule
- [[decision-package-layout]]: `src/` layout and a pure domain core
- [[decision-quota-budget-enforcement]]: reject workflows before any API call if they would exceed the quota budget (ADR 0001)
- [[decision-browser-only-playlist-confirmation]]: playlists are confirmed only in the owner's browser (ADR 0002)
- [[decision-tfidf-similarity]]: how metadata similarity is computed, and why without scikit-learn
- [[decision-layered-architecture]]: six layers, ports and adapters, and the import rules between them (ADR 0003)
- [[decision-tech-stack]]: MCP SDK 2.3, FastAPI and httpx2, and what the spike found (ADR 0004)
- [[decision-youtube-provider-interface]]: separate read and write protocols, bound credentials, metered calls and typed errors (ADR 0005)
- [[decision-error-catalogue]]: one catalogue of error codes, mapped in the services layer, with a structured error object

## Resources

- [[mcp-fundamentals]]: stateless MCP requests, tools, transports and project mapping
- [[para-method]]: how PARA works and how this vault applies it
- [[agent-skills-format]]: SKILL.md fields and limits, progressive disclosure and validation

# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- ADR 0006 selects the database, data-access layer and migration workflow (#42).
- Logical data model with entity relationships, field protection, retention and transaction boundaries (#41).
- Team skill for answering questions and drafting documents from cited vault notes, with a logged playlist-confirmation trial (#49).
- Local FastAPI server with a configurable bind address and port and a public health check (#47).
- Requirements traceability matrix and contributor guidance for keeping it current (#55).

- Software Requirements Specification in `docs/srs.md`, converted from the Word document, with its figures (#32).
- Research note on testing against recorded fixtures and mocks, completing #14.
- ADR 0003: layered ports-and-adapters architecture with fixed import rules, and its decision note (#39).
- ADR 0004: MCP Python SDK 2.3, FastAPI and httpx2, from a spike on branch `spike/38-mcp-sdk`, and its decision note (#38).
- YouTube provider interface design in `docs/design/provider-interface.md`: read and write protocols, quota cost and failure modes of each method, typed provider errors, the in-memory fake and a class diagram; ADR 0005 and its decision note (#40).
- `brain-refine` skill: check inbox notes against sources and later decisions, merge duplicates, fix links, file them in PARA folders and update the index; trial run refined `agent-skills-format` into `resources/` (#48).
- Error catalogue in `docs/design/errors.md`: every error code with its channel, message pattern, retryability and details, the mapping from domain and provider errors, and logging rules; and its decision note (#43).

### Changed

- `README.md` now has project status, a quick start, the check commands and links to the key documents (#35).
- `CONTRIBUTING.md` has a one-time git setup section, including `fetch.prune` (#35).
- `CONTRIBUTING.md` describes the team's merge-commit workflow: merging `main` into branches, resolving `CHANGELOG.md` conflicts, stacked pull requests, and Conventional Commits on every commit (#37).
- SRS v0.2: AC-3, AC-6, IF-7 and A-2 follow MCP specification 2026-07-28 (stateless requests; Client ID Metadata Documents preferred over deprecated dynamic client registration). §3.8, QM-1, QM-2, QM-3, QM-6 and DC-2 use Google's two quota allowances: 100 `search.list` calls and 10,000 units a day. The per-account default budget is raised to 3,000 units so the largest playlist fits (#32).
- The provider design's error table now points to the codes in the error catalogue instead of provisional ones (#43).
- The seven YouTube API, duration and similarity research notes are refined out of `brain/inbox/` into `brain/areas/` and `brain/resources/`, with dated update lines where later decisions changed them, and linked from `brain/index.md` (#50).

### Fixed

- Run-log rows for the brain-ingest runs in #25 and #27 (#35).
- Traceability links and the run log updated after the #50 notes moved (#77).

## [0.1.0] - 2026-11-27

Stage 1 (requirements) release.

### Added

- Stage 1 review note in `brain/projects/` (#30).
- Knowledge-base vault in `brain/` with PARA folders, index and run log (#1).
- Pull request template, issue forms, contributing guide and this changelog (#3).
- Root `AGENTS.md`, knowledge-base schema in `brain/AGENTS.md` and note templates, including code-design, scalability and testing rules, and decision notes (#5).
- CI pipeline: Ruff lint and format, pytest with coverage, knowledge-base schema validation and Gitleaks secret scanning (#7).
- `tools/validate_brain.py`, which checks every note against `brain/AGENTS.md` (#7).
- `brain-ingest` skill for capturing sources as schema-valid inbox notes (#9).
- `tools/validate_skills.py` and an *Agent Skills* CI job: specification checks via `skills-ref`, plus each skill must cite a distilled note (#9).
- Concept note on the PARA method and a decision note on skill validation (#9).
- Research notes on MCP fundamentals, MCP authorization and the Agent Skills format (#11).
- Research notes on YouTube Data API quota costs, API methods, error reasons and playlist creation (#12).
- Application package `youtube_sieve` in a `src/` layout, with a pure `domain` layer (#17).
- ISO 8601 duration parsing for YouTube video lengths, `parse_duration` (#17).
- `docs/adr/` with ADR 0001 (enforce quota budgets before API calls) and ADR 0002 (browser-only playlist confirmation), and their decision notes (#19).
- TF-IDF and cosine similarity ranking in the domain layer, `rank_by_similarity`, with Unicode-aware tokenisation and weighted fields (#21).
- Quota arithmetic in the domain layer: cost table with separate unit and search-call pools, worst-case estimates, Pacific-time quota day, budget checks across layered budgets and settlement (#23).
- `tzdata` runtime dependency so time zones work on Windows (#23).
- Research note on TF-IDF and cosine similarity (#13).
- Research notes on YouTube OAuth scopes and identity, and token expiry and re-authorization (#14).
- Research notes on prompt injection through YouTube metadata and playlist confirmation security (#14).

### Fixed

- Run-log row for the TF-IDF research note now links its pull request, #26 (#30).

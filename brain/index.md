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

- [[decision-storage]]: database profiles, transaction primitives and migration tooling (ADR 0006)
- [[decision-shared-data-model]]: owner deletion and shared quota accounting

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
- [[decision-quota-runtime-and-caching]]: cache-aware quota planning, account attribution, fixed-window rate limits and outage behaviour
- [[youtube-api-quota-costs]]: daily allowances, the separate search bucket, per-method costs and how they shape spending
- [[youtube-api-methods]]: the Data API methods we call, their parameters and parts, and what each is used for
- [[youtube-api-errors]]: Google's error reasons for our methods and how each group is handled
- [[youtube-playlist-creation]]: creating a playlist and adding videos one per call, scopes, errors and partial failure
- [[youtube-similarity-without-related-endpoint]]: finding candidate videos and channels without a related-videos endpoint

## Resources

- [[para-method]]: how PARA works and how this vault applies it
- [[agent-skills-format]]: SKILL.md fields and limits, progressive disclosure and validation
- [[iso-8601-durations]]: how YouTube's ISO 8601 durations convert to seconds, and the edge cases the parser rejects
- [[tfidf-cosine-similarity]]: a worked TF-IDF and cosine example over video metadata

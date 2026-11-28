# Architecture Decision Records

An Architecture Decision Record (ADR) captures one significant decision: the context that forced it, what was decided, and its consequences. ADRs are short, numbered and never rewritten after acceptance. A changed decision gets a new ADR that supersedes the old one.

The full reasoning, including every option considered, lives in a **decision note** in `brain/`. Each ADR cites at least one distilled note (SB-3), so this folder is the formal summary and the brain holds the working detail.

## Index

| ADR | Title | Status |
|---|---|---|
| [0001](0001-enforce-quota-budget-before-api-calls.md) | Enforce quota budgets before calling the YouTube API | Accepted |
| [0002](0002-browser-only-playlist-confirmation.md) | Confirm playlist creation only in the user's browser | Accepted |
| [0003](0003-layered-architecture.md) | Use a layered ports-and-adapters architecture | Accepted |
| [0004](0004-tech-stack.md) | Build on MCP Python SDK 2.3, FastAPI and httpx2 | Accepted |
| [0005](0005-youtube-provider-interface.md) | Reach YouTube through separate read and write protocols with typed errors | Accepted |
| [0006](0006-storage.md) | Use SQLAlchemy Core transactions and Alembic migrations | Accepted |

## Writing a new ADR

1. Write the decision note first, in `brain/areas/` or `brain/projects/`, following `brain/AGENTS.md`.
2. Copy the template below to `NNNN-short-title.md`, using the next free number.
3. Add it to the index above, and open a pull request like any other change.

```markdown
# NNNN. Title in the imperative

- **Status:** Proposed | Accepted | Superseded by [NNNN](NNNN-title.md)
- **Date:** YYYY-MM-DD
- **Decision note:** [`brain/areas/decision-<slug>.md`](../../brain/areas/decision-<slug>.md)
- **Requirements:** FR-1, TQ-6

## Context
What forces a decision now? Constraints and facts, with sources.

## Decision
What we will do, stated plainly.

## Consequences
What becomes easier, what becomes harder, and the follow-up work.
```

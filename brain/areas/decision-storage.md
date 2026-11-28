---
title: Use SQLAlchemy Core and Alembic for shared storage
type: decision
status: distilled
created: 2026-11-28
authors: [romirG]
tags: [decision, architecture, storage]
requirements: [DC-5, SC-5, SL-2, QM-4]
---

# Use SQLAlchemy Core and Alembic for shared storage

**Issue:** #42. **ADR:** `docs/adr/0006-storage.md`.

The shared data model needs transactions that work across service instances. For example, two workers can reserve the last search call of the day at the same time. Both must check the global and caller budgets, and only one may commit. Ownership, deletion and the two allowance counters are defined in [[decision-shared-data-model]] and [[decision-quota-budget-enforcement]].

| Question | Options and trade-offs | Choice |
|---|---|---|
| Which database runs locally? | Local PostgreSQL exercises production constraints and row locks but requires a database service. SQLite needs only a file but serializes writers and cannot establish that PostgreSQL row locks work. | Neon PostgreSQL with pooled connections in production (DC-5). Offer SQLite through an explicit local profile. Use disposable PostgreSQL for integration, migration and concurrency tests. |
| How should repositories issue queries? | Direct Psycopg gives precise SQL and locking but leaves binding conventions, result mapping and the second dialect to each repository. An ORM maps object graphs conveniently but implicit flushes obscure the order of writes. Core provides bound parameters and explicit statements, affected rows and transaction boundaries. | SQLAlchemy Core with Psycopg 3 for PostgreSQL. Keep dialect-specific locking inside the storage adapter from [[decision-layered-architecture]]. |
| How should the schema evolve? | Handwritten numbered SQL scripts give complete control, but the project would need its own revision tracking and dialect handling. Automatic table creation handles new databases but cannot safely evolve stored data. Alembic tracks reviewed revisions and can express both schema and data changes. | Keep a single Alembic revision chain in version control. Review generated operations and explicitly write data backfills. Test upgrades from the previous revision as well as an empty database. |

## Consequences

Services express operations such as reserving quota and consuming a refresh token through storage ports. The adapter owns the transaction for the whole operation. This keeps domain tests fast with fakes and gives integration tests a real commit boundary. Maintaining an explicit local SQLite path adds migration and locking tests. A successful SQLite run gives no evidence about competing PostgreSQL sessions.

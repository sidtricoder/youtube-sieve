---
title: Separate owner records from shared quota counters
type: decision
status: distilled
created: 2026-11-28
authors: [romirG]
tags: [decision, architecture, storage]
requirements: [SE-2, SL-1, SL-2, PV-1, PV-2, PV-3, QM-1, QM-4, SC-1, SC-2]
---

# Separate owner records from shared quota counters

**Status:** Proposed in #41.

A single per-user usage history would make disconnect easy but lose the project's consumption when a user leaves. A shared counter alone cannot enforce the account cap. The proposed data model reserves against both the global day and the caller's layer in one transaction. Disconnect deletes the personal layer after accounting for outstanding calls in the aggregate. This preserves the preflight guarantee in [[decision-quota-budget-enforcement]].

Keep ownership, deadlines and workflow state queryable under opaque keys. Seal the personal payloads and retain only lookup digests for credentials that the server verifies. This lets the storage adapter expire a draft or serialize a confirmation without inspecting its video metadata. The ports and adapters follow [[decision-layered-architecture]].

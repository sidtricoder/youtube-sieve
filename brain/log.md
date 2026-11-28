---
title: Log
type: log
---

# Brain run log

One line per brain-ingest / brain-refine / brain-query run, newest last.

Format: `YYYY-MM-DD | skill | author | what changed | PR`

| Date | Skill | Author | Change | PR |
|---|---|---|---|---|
| 2026-11-19 | setup | team | Created PARA folders, index and log | — |
| 2026-11-22 | brain-ingest | sidtricoder | added [[mcp-fundamentals]], [[mcp-authorization]], [[agent-skills-format]] | PR #15 |
| 2026-11-22 | brain-ingest | Devaang-Rastogi | added [[youtube-api-quota-costs]], [[youtube-api-methods]], [[youtube-api-errors]], [[youtube-playlist-creation]] | PR #16 |
| 2026-11-22 | brain-ingest | romirG | added [[tfidf-cosine-similarity]] | PR #26 |
| 2026-11-22 | brain-ingest | romirG | added [[youtube-similarity-without-related-endpoint]] | PR #25 |
| 2026-11-22 | brain-ingest | romirG | added [[iso-8601-durations]] | PR #27 |
| 2026-11-26 | brain-ingest | 77-Div-77 | added [[youtube-oauth-scopes-and-identity]], [[youtube-oauth-token-lifecycle]] | PR #28 |
| 2026-11-27 | brain-ingest | 77-Div-77 | added [[prompt-injection-untrusted-metadata]], [[playlist-confirmation-security]] | PR #29 |
| 2026-11-28 | brain-ingest | sidtricoder | added [[testing-with-fixtures-and-mocks]] | PR #34 |
| 2026-11-28 | brain-refine | sidtricoder | refined [[agent-skills-format]] → resources/ (trial run of the skill) | PR #61 |
| 2026-11-28 | brain-refine | 77-Div-77 | refined [[mcp-fundamentals]] → resources/; [[mcp-authorization]], [[youtube-oauth-scopes-and-identity]], [[youtube-oauth-token-lifecycle]], [[prompt-injection-untrusted-metadata]], [[playlist-confirmation-security]], [[testing-with-fixtures-and-mocks]] → areas/; checked sources and later decisions, fixed links and indexed all seven | PR #69 |
| 2026-11-28 | brain-query | romirG | Who may confirm a playlist draft under the accepted design? Only the signed-in draft owner can confirm in their browser. The AI presents the approval link and can read the draft status. [[decision-browser-only-playlist-confirmation]] | #49 (PR pending) |
| 2026-11-28 | brain-refine | Devaang-Rastogi | refined [[youtube-api-quota-costs]], [[youtube-api-methods]], [[youtube-api-errors]], [[youtube-playlist-creation]], [[youtube-similarity-without-related-endpoint]] → areas/; [[iso-8601-durations]], [[tfidf-cosine-similarity]] → resources/ | PR #72 |

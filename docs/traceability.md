# Requirements traceability

The [SRS](srs.md) defines the requirements. This matrix records evidence on `main` through PR #67. A test link covers only the behaviour named in its row. **Planned** means the requirement still needs implementation or verification. A dash marks an unassigned issue or an evidence link that does not yet exist.

## Walkthrough: from a requirement to evidence

For DC-3, [issue #21][i21] led to [PR #22][p22]. In [the ranking tests][rank-tests], `test_rare_shared_term_beats_common_shared_term` checks that a distinctive shared term outranks a common one. The [decision note][rank] explains the weighting and links the research. The [brain-ingest skill][ingest] captured that research under [issue #13][i13] in [PR #26][p26]. The product video-to-playlist skill (SK-1) is still planned.

## SRS coverage

### Assumptions

| Requirement | Evidence and remaining work | Issue | Merged PR | Tests, design or notes |
|---|---|---|---|---|
| A-1 · Google account | SRS assumption | — | — | — |
| A-2 · MCP client | SRS assumption | — | — | — |
| A-3 · Testing user limits | SRS assumption | — | — | — |
| A-4 · Untrusted text | SRS assumption | — | — | — |

### AC · Access control

| Requirement | Evidence and remaining work | Issue | Merged PR | Tests, design or notes |
|---|---|---|---|---|
| AC-1 · Tier allow-list | Auth research; implementation planned | [#11][i11], [#44][i44] | [#15][p15] | [MCP authorization][auth] |
| AC-2 · Public credentials | Identity research; flow planned | [#14][i14], [#44][i44] | [#28][p28] | [Google scopes][identity] |
| AC-3 · Anonymous discovery | Auth research; implementation planned | [#11][i11], [#44][i44] | [#15][p15] | [MCP authorization][auth] |
| AC-4 · Sign-in challenge | Auth research; implementation planned | [#11][i11], [#44][i44] | [#15][p15] | [MCP authorization][auth] |
| AC-5 · Invalid tokens | Auth research; implementation planned | [#11][i11], [#44][i44] | [#15][p15] | [MCP authorization][auth] |
| AC-6 · MCP authorization | Auth research; implementation planned | [#11][i11], [#44][i44] | [#15][p15] | [MCP authorization][auth] |
| AC-7 · Google sign-in | Identity research; flow planned | [#14][i14], [#44][i44] | [#28][p28] | [Google scopes][identity] |
| AC-8 · Consent scopes | Identity research; flow planned | [#14][i14], [#44][i44] | [#28][p28] | [Google scopes][identity] |
| AC-9 · Disconnect | Token lifecycle researched; enforcement planned | [#14][i14], [#44][i44] | [#28][p28] | [Token lifecycle][tokens] |
| AC-10 · Subject isolation | Token lifecycle researched; enforcement planned | [#14][i14], [#44][i44] | [#28][p28] | [Token lifecycle][tokens] |
| AC-11 · Expired grant | Token lifecycle researched; enforcement planned | [#14][i14], [#44][i44] | [#28][p28] | [Token lifecycle][tokens] |
| AC-12 · Missing channel | Error contract designed; runtime planned | [#43][i43] | [#67][p67] | [Error catalogue][errors] |
| AC-13 · Verified identity | Planned | — | — | — |

### FR-1 · Similar videos

| Requirement | Evidence and remaining work | Issue | Merged PR | Tests, design or notes |
|---|---|---|---|---|
| FR-1.1 · Video input | Planned | — | — | — |
| FR-1.2 · Seed metadata | Retrieval strategy researched; pipeline planned | [#13][i13] | [#25][p25] | [Candidate discovery][channels] |
| FR-1.3 · Candidate discovery | Retrieval strategy researched; pipeline planned | [#13][i13] | [#25][p25] | [Candidate discovery][channels] |
| FR-1.4 · Candidate scores | Text scorer tested; workflow planned | [#21][i21] | [#22][p22] | [Ranking tests][rank-tests], [Ranking decision][rank] |
| FR-1.5 · Missing text | Empty text tested; confidence flag planned | [#21][i21] | [#22][p22] | [Ranking tests][rank-tests] |
| FR-1.6 · Exclusions | Seed and duplicate exclusion tested; availability checks planned | [#21][i21] | [#22][p22] | [Ranking tests][rank-tests] |
| FR-1.7 · Result order | Deterministic ordering tested; result contract planned | [#21][i21] | [#22][p22] | [Ranking tests][rank-tests] |
| FR-1.8 · Personalisation disclosure | Planned | — | — | — |

### FR-2 · Similar channels

| Requirement | Evidence and remaining work | Issue | Merged PR | Tests, design or notes |
|---|---|---|---|---|
| FR-2.1 · Channel resolution | Planned | — | — | — |
| FR-2.2 · Channel profile | Retrieval strategy researched; pipeline planned | [#13][i13] | [#25][p25] | [Candidate discovery][channels] |
| FR-2.3 · Candidate search | Retrieval strategy researched; pipeline planned | [#13][i13] | [#25][p25] | [Candidate discovery][channels] |
| FR-2.4 · Profile similarity | Text scorer tested; workflow planned | [#21][i21] | [#22][p22] | [Ranking tests][rank-tests], [Ranking decision][rank] |
| FR-2.5 · Exclusions | Seed and duplicate exclusion tested; availability checks planned | [#21][i21] | [#22][p22] | [Ranking tests][rank-tests] |
| FR-2.6 · Result fields | Planned | — | — | — |
| FR-2.7 · Hidden channel data | Planned | — | — | — |

### FR-3 · Recommendations

| Requirement | Evidence and remaining work | Issue | Merged PR | Tests, design or notes |
|---|---|---|---|---|
| FR-3.1 · Account sources | Planned | — | — | — |
| FR-3.2 · Sample bounds | Planned | — | — | — |
| FR-3.3 · Interest profile | Planned | — | — | — |
| FR-3.4 · Candidate ranking | Text scorer tested; workflow planned | [#21][i21] | [#22][p22] | [Ranking tests][rank-tests], [Ranking decision][rank] |
| FR-3.5 · Explanations | Planned | — | — | — |
| FR-3.6 · Sparse account data | Planned | — | — | — |

### FR-4 · Engagement analysis

| Requirement | Evidence and remaining work | Issue | Merged PR | Tests, design or notes |
|---|---|---|---|---|
| FR-4.1 · Activity sources | Planned | — | — | — |
| FR-4.2 · Channel and category shares | Planned | — | — | — |
| FR-4.3 · Duration bands | Planned | — | — | — |
| FR-4.4 · Activity trends | Planned | — | — | — |
| FR-4.5 · Period comparison | Planned | — | — | — |
| FR-4.6 · Date validation | Planned | — | — | — |

### FR-5 · Playlist creation

| Requirement | Evidence and remaining work | Issue | Merged PR | Tests, design or notes |
|---|---|---|---|---|
| FR-5.1 · Constraint parsing | Duration parser tested; constraint handling planned | [#17][i17], [#13][i13] | [#18][p18], [#27][p27] | [Duration tests][duration-tests], [Duration research][duration] |
| FR-5.2 · Strict limits | Planned | — | — | — |
| FR-5.3 · Candidate ranking | Text scorer tested; workflow planned | [#21][i21] | [#22][p22] | [Ranking tests][rank-tests], [Ranking decision][rank] |
| FR-5.4 · Subset selection | Planned | — | — | — |
| FR-5.5 · Duration ceiling | Planned | — | — | — |
| FR-5.6 · Infeasible constraints | Planned | — | — | — |
| FR-5.7 · Playlist order | Planned | — | — | — |
| FR-5.8 · Constraint report | Planned | — | — | — |
| FR-5.9 · Immutable draft | Browser confirmation boundary designed; workflow planned | [#19][i19], [#45][i45] | [#20][p20] | [ADR 0002][confirm] |
| FR-5.10 · Expiry | Browser confirmation boundary designed; workflow planned | [#19][i19], [#45][i45] | [#20][p20] | [ADR 0002][confirm] |
| FR-5.11 · Confirmation link | Browser confirmation boundary designed; workflow planned | [#19][i19], [#45][i45] | [#20][p20] | [ADR 0002][confirm] |
| FR-5.12 · Browser confirmation | Browser confirmation boundary designed; workflow planned | [#19][i19], [#45][i45] | [#20][p20] | [ADR 0002][confirm] |
| FR-5.13 · Owner and CSRF checks | Browser confirmation boundary designed; workflow planned | [#19][i19], [#45][i45] | [#20][p20] | [ADR 0002][confirm] |
| FR-5.14 · Confirmation boundary | Browser confirmation boundary designed; workflow planned | [#19][i19], [#45][i45] | [#20][p20] | [ADR 0002][confirm] |
| FR-5.15 · Ordered writes | Browser confirmation boundary designed; workflow planned | [#19][i19], [#45][i45] | [#20][p20] | [ADR 0002][confirm] |
| FR-5.16 · Atomic progress | Browser confirmation boundary designed; workflow planned | [#19][i19], [#45][i45] | [#20][p20] | [ADR 0002][confirm] |
| FR-5.17 · Resume | Browser confirmation boundary designed; workflow planned | [#19][i19], [#45][i45] | [#20][p20] | [ADR 0002][confirm] |
| FR-5.18 · Uncertain writes | Browser confirmation boundary designed; workflow planned | [#19][i19], [#45][i45] | [#20][p20] | [ADR 0002][confirm] |
| FR-5.19 · Status and readback | Browser confirmation boundary designed; workflow planned | [#19][i19], [#45][i45] | [#20][p20] | [ADR 0002][confirm] |

### FR-6 and FR-7 supporting functions

| Requirement | Evidence and remaining work | Issue | Merged PR | Tests, design or notes |
|---|---|---|---|---|
| FR-6 · Video summary | Planned | — | — | — |
| FR-7 · Playlist analysis | Planned | — | — | — |

### QM · Quota and rate management

| Requirement | Evidence and remaining work | Issue | Merged PR | Tests, design or notes |
|---|---|---|---|---|
| QM-1 · Daily ledger | Quota day and reset tested; ledger planned | [#23][i23], [#46][i46] | [#24][p24] | [Quota tests][quota-tests], [ADR 0001][quota] |
| QM-2 · Preflight estimate | Cost and budget comparisons tested; enforcement planned | [#19][i19], [#23][i23] | [#20][p20], [#24][p24] | [Quota tests][quota-tests], [ADR 0001][quota] |
| QM-3 · Caller budgets | Cost and budget comparisons tested; enforcement planned | [#19][i19], [#23][i23] | [#20][p20], [#24][p24] | [Quota tests][quota-tests], [ADR 0001][quota] |
| QM-4 · Atomic reservations | Settlement arithmetic tested; atomic persistence designed | [#23][i23], [#46][i46], [#42][i42] | [#24][p24] | [Quota tests][quota-tests], [ADR 0001][quota], [ADR 0006](adr/0006-storage.md) |
| QM-5 · Metadata cache | Planned | [#46][i46] | — | — |
| QM-6 · Call batching | Batch cost arithmetic tested; provider calls planned | [#23][i23], [#40][i40] | [#24][p24], [#63][p63] | [Quota tests][quota-tests], [ADR 0005][provider] |
| QM-7 · Usage report | Planned | — | — | — |
| QM-8 · Rate limits | Error contract designed; runtime planned | [#43][i43] | [#67][p67] | [Error catalogue][errors] |
| QM-9 · Upstream exhaustion | Error contract designed; runtime planned | [#43][i43] | [#67][p67] | [Error catalogue][errors] |

### SK-1 · Video-to-playlist skill

| Requirement | Evidence and remaining work | Issue | Merged PR | Tests, design or notes |
|---|---|---|---|---|
| SK-1.1 · Skill package | Skill format researched; product workflow planned | [#11][i11], [#48][i48] | [#15][p15], [#61][p61] | [Skill format][skill-format] |
| SK-1.2 · Untrusted metadata | Threat researched; product safeguards planned | [#14][i14] | [#29][p29] | [Untrusted metadata][metadata] |
| SK-1.3 · Metadata-only claims | Planned | — | — | — |
| SK-1.4 · Explicit constraints | Planned | — | — | — |

### IF · Interfaces

| Requirement | Evidence and remaining work | Issue | Merged PR | Tests, design or notes |
|---|---|---|---|---|
| IF-1 · Accessible pages | Planned | — | — | — |
| IF-2 · MCP resources | Planned | — | — | — |
| IF-3 · Workflow prompt | Planned | — | — | — |
| IF-4 · Structured responses | Error contract designed; runtime planned | [#43][i43] | [#67][p67] | [Error catalogue][errors] |
| IF-5 · Bearer challenge | Planned | — | — | — |
| IF-6 · Discovery 404s | Planned | — | — | — |
| IF-7 · Client registration | Identity research; flow planned | [#14][i14], [#44][i44] | [#28][p28] | [Google scopes][identity] |
| IF-8 · Scopes | Identity research; flow planned | [#14][i14], [#44][i44] | [#28][p28] | [Google scopes][identity] |
| IF-9 · Browser routes | Health route tested; other browser routes planned | [#19][i19], [#45][i45], [#47][i47] | [#20][p20] | [ADR 0002][confirm], [Server tests](../tests/test_server.py) |
| IF-10 · YouTube provider | Provider contract designed; adapters planned | [#40][i40] | [#63][p63] | [ADR 0005][provider] |
| IF-11 · Outbound requests | Provider contract designed; adapters planned | [#40][i40] | [#63][p63] | [ADR 0005][provider] |
| IF-12 · Transport | Stack selected; service integration planned | [#38][i38], [#47][i47] | [#59][p59] | [ADR 0004][stack] |

### PF · Performance

| Requirement | Evidence and remaining work | Issue | Merged PR | Tests, design or notes |
|---|---|---|---|---|
| PF-1 · Cached reads | Planned | — | — | — |
| PF-2 · Uncached reads | Planned | — | — | — |
| PF-3 · Draft latency | Planned | — | — | — |
| PF-4 · Account analysis | Planned | — | — | — |
| PF-5 · Playlist writes | Planned | — | — | — |
| PF-6 · Local requests | Local health handler tested; p95 latency verification planned | [#47][i47] | — | [Server tests](../tests/test_server.py) |
| PF-7 · Authorization overhead | Planned | — | — | — |
| PF-8 · Cold start | Planned | — | — | — |
| PF-9 · Concurrency | Planned | — | — | — |
| PF-10 · Resident memory | Planned | — | — | — |
| PF-11 · Registered accounts | Planned | — | — | — |
| PF-12 · Account storage | Planned | — | — | — |

### DC · Design constraints

| Requirement | Evidence and remaining work | Issue | Merged PR | Tests, design or notes |
|---|---|---|---|---|
| DC-1 · Official API | Provider contract designed; adapters planned | [#40][i40] | [#63][p63] | [ADR 0005][provider] |
| DC-2 · Quota allowances | Cost and budget comparisons tested; enforcement planned | [#19][i19], [#23][i23] | [#20][p20], [#24][p24] | [Quota tests][quota-tests], [ADR 0001][quota] |
| DC-3 · Metadata similarity | TF-IDF ranking tested; discovery workflows planned | [#13][i13], [#21][i21] | [#22][p22], [#25][p25], [#26][p26] | [Ranking tests][rank-tests], [Ranking decision][rank], [Candidate discovery][channels] |
| DC-4 · Python stack | Stack selected; service integration planned | [#38][i38], [#47][i47] | [#59][p59] | [ADR 0004][stack] |
| DC-5 · Database | Storage backend and migration policy decided; adapter planned | [#42][i42] | — | [ADR 0006](adr/0006-storage.md) |
| DC-6 · Google data policy | Planned | — | — | — |

### SC · Security

| Requirement | Evidence and remaining work | Issue | Merged PR | Tests, design or notes |
|---|---|---|---|---|
| SC-1 · MCP credentials | Identity research; flow planned | [#14][i14], [#44][i44] | [#28][p28] | [Google scopes][identity] |
| SC-2 · Encryption | Token lifecycle researched; enforcement planned | [#14][i14], [#44][i44] | [#28][p28] | [Token lifecycle][tokens] |
| SC-3 · Session cookies | Identity research; flow planned | [#14][i14], [#44][i44] | [#28][p28] | [Google scopes][identity] |
| SC-4 · Prompt injection | Threat researched; product safeguards planned | [#14][i14] | [#29][p29] | [Untrusted metadata][metadata] |
| SC-5 · Input validation | Parameter binding specified; implementation planned | [#42][i42] | — | [ADR 0006](adr/0006-storage.md) |
| SC-6 · Least privilege | Identity research; flow planned | [#14][i14], [#44][i44] | [#28][p28] | [Google scopes][identity] |
| SC-7 · Redirects and replay | Identity research; flow planned | [#14][i14], [#44][i44] | [#28][p28] | [Google scopes][identity] |
| SC-8 · CSRF and origin | Browser confirmation boundary designed; workflow planned | [#19][i19], [#45][i45] | [#20][p20] | [ADR 0002][confirm] |
| SC-9 · Response headers | Planned | — | — | — |
| SC-10 · Secret handling | Secret scan in CI; safe error contract designed | [#7][i7], [#43][i43] | [#8][p8], [#67][p67] | [CI workflow][ci], [Error catalogue][errors] |
| SC-11 · Dependency security | Planned | — | — | — |

### PV · Privacy

| Requirement | Evidence and remaining work | Issue | Merged PR | Tests, design or notes |
|---|---|---|---|---|
| PV-1 · Data minimisation | Planned | — | — | — |
| PV-2 · Retention | Planned | — | — | — |
| PV-3 · Account deletion | Token lifecycle researched; enforcement planned | [#14][i14], [#44][i44] | [#28][p28] | [Token lifecycle][tokens] |
| PV-4 · Purpose limitation | Planned | — | — | — |
| PV-5 · Privacy notice | Planned | — | — | — |
| PV-6 · Operator access | Planned | — | — | — |

### RL · Reliability

| Requirement | Evidence and remaining work | Issue | Merged PR | Tests, design or notes |
|---|---|---|---|---|
| RL-1 · Availability | Planned | — | — | — |
| RL-2 · Upstream failures | Error contract designed; runtime planned | [#43][i43] | [#67][p67] | [Error catalogue][errors] |

### SL · Scalability

| Requirement | Evidence and remaining work | Issue | Merged PR | Tests, design or notes |
|---|---|---|---|---|
| SL-1 · Stateless instances | Architecture documented; deployment and integration planned | [#39][i39] | [#58][p58] | [ADR 0003][layers] |
| SL-2 · Atomic coordination | Transaction boundaries specified; concurrency tests planned | [#23][i23], [#46][i46], [#42][i42] | [#24][p24] | [Quota tests][quota-tests], [ADR 0001][quota], [ADR 0006](adr/0006-storage.md) |

### MT · Maintainability

| Requirement | Evidence and remaining work | Issue | Merged PR | Tests, design or notes |
|---|---|---|---|---|
| MT-1 · Layer boundaries | Architecture documented; deployment and integration planned | [#39][i39] | [#58][p58] | [ADR 0003][layers] |

### PT · Portability

| Requirement | Evidence and remaining work | Issue | Merged PR | Tests, design or notes |
|---|---|---|---|---|
| PT-1 · Container delivery | Environment-based server configuration tested; container delivery planned | [#39][i39], [#47][i47] | [#58][p58] | [ADR 0003][layers], [Server tests](../tests/test_server.py) |

### IO · Interoperability

| Requirement | Evidence and remaining work | Issue | Merged PR | Tests, design or notes |
|---|---|---|---|---|
| IO-1 · MCP interoperability | Stack selected; service integration planned | [#38][i38], [#47][i47] | [#59][p59] | [ADR 0004][stack] |

### US · Usability

| Requirement | Evidence and remaining work | Issue | Merged PR | Tests, design or notes |
|---|---|---|---|---|
| US-1 · Disclosures | Planned | — | — | — |
| US-2 · Actionable errors | Error contract designed; runtime planned | [#43][i43] | [#67][p67] | [Error catalogue][errors] |

## Team skills and delivery evidence

The team uses these skills to maintain the notes that product requirements cite.

| Requirement | Evidence and remaining work | Issue | Merged PR | Tests, design or notes |
|---|---|---|---|---|
| SB-1, SB-3, SB-5 · Capture | Inbox capture, schema and skill validation in CI | [#1][i1], [#7][i7], [#9][i9] | [#2][p2], [#8][p8], [#10][p10] | [brain-ingest][ingest], [Vault tests][vault-tests], [Skill validation tests][skill-tests], [Validation decision][skill-validation], [PARA][para] |
| SB-3 · Refine | Trial moved the skill-format note into resources | [#48][i48] | [#61][p61] | [brain-refine][refine], [Skill validation tests][skill-tests], [Skill format][skill-format] |
| SE-5 · Traceability | Maintain this matrix as requirements and evidence change | [#55][i55] | — | [SRS](srs.md) |

## Updating the matrix

In each PR, find the affected SRS IDs and update their rows. Link the issue and PR, the test that demonstrates the behaviour, and any relevant skill, brain note or ADR. Describe exactly what the test verifies and keep unfinished work marked planned. Add the PR number after opening the PR and before review. When the SRS changes, add or retire rows in the same change.

[i11]: https://github.com/sidtricoder/youtube-sieve/issues/11
[i44]: https://github.com/sidtricoder/youtube-sieve/issues/44
[p15]: https://github.com/sidtricoder/youtube-sieve/pull/15
[i14]: https://github.com/sidtricoder/youtube-sieve/issues/14
[p28]: https://github.com/sidtricoder/youtube-sieve/pull/28
[i43]: https://github.com/sidtricoder/youtube-sieve/issues/43
[p67]: https://github.com/sidtricoder/youtube-sieve/pull/67
[i13]: https://github.com/sidtricoder/youtube-sieve/issues/13
[p25]: https://github.com/sidtricoder/youtube-sieve/pull/25
[i21]: https://github.com/sidtricoder/youtube-sieve/issues/21
[p22]: https://github.com/sidtricoder/youtube-sieve/pull/22
[i17]: https://github.com/sidtricoder/youtube-sieve/issues/17
[p18]: https://github.com/sidtricoder/youtube-sieve/pull/18
[p27]: https://github.com/sidtricoder/youtube-sieve/pull/27
[i19]: https://github.com/sidtricoder/youtube-sieve/issues/19
[i45]: https://github.com/sidtricoder/youtube-sieve/issues/45
[p20]: https://github.com/sidtricoder/youtube-sieve/pull/20
[i23]: https://github.com/sidtricoder/youtube-sieve/issues/23
[i46]: https://github.com/sidtricoder/youtube-sieve/issues/46
[p24]: https://github.com/sidtricoder/youtube-sieve/pull/24
[i40]: https://github.com/sidtricoder/youtube-sieve/issues/40
[p63]: https://github.com/sidtricoder/youtube-sieve/pull/63
[i48]: https://github.com/sidtricoder/youtube-sieve/issues/48
[p61]: https://github.com/sidtricoder/youtube-sieve/pull/61
[p29]: https://github.com/sidtricoder/youtube-sieve/pull/29
[i38]: https://github.com/sidtricoder/youtube-sieve/issues/38
[i47]: https://github.com/sidtricoder/youtube-sieve/issues/47
[p59]: https://github.com/sidtricoder/youtube-sieve/pull/59
[p26]: https://github.com/sidtricoder/youtube-sieve/pull/26
[i42]: https://github.com/sidtricoder/youtube-sieve/issues/42
[i7]: https://github.com/sidtricoder/youtube-sieve/issues/7
[p8]: https://github.com/sidtricoder/youtube-sieve/pull/8
[i39]: https://github.com/sidtricoder/youtube-sieve/issues/39
[p58]: https://github.com/sidtricoder/youtube-sieve/pull/58
[i1]: https://github.com/sidtricoder/youtube-sieve/issues/1
[i9]: https://github.com/sidtricoder/youtube-sieve/issues/9
[p2]: https://github.com/sidtricoder/youtube-sieve/pull/2
[p10]: https://github.com/sidtricoder/youtube-sieve/pull/10
[i55]: https://github.com/sidtricoder/youtube-sieve/issues/55
[rank-tests]: ../tests/domain/test_similarity.py
[duration-tests]: ../tests/domain/test_durations.py
[quota-tests]: ../tests/domain/test_quota.py
[vault-tests]: ../tests/tools/test_validate_brain.py
[skill-tests]: ../tests/tools/test_validate_skills.py
[ingest]: ../skills/brain-ingest/SKILL.md
[refine]: ../skills/brain-refine/SKILL.md
[rank]: ../brain/areas/decision-tfidf-similarity.md
[duration]: ../brain/inbox/iso-8601-durations.md
[quota]: adr/0001-enforce-quota-budget-before-api-calls.md
[confirm]: adr/0002-browser-only-playlist-confirmation.md
[layers]: adr/0003-layered-architecture.md
[stack]: adr/0004-tech-stack.md
[provider]: adr/0005-youtube-provider-interface.md
[errors]: design/errors.md
[auth]: ../brain/inbox/mcp-authorization.md
[identity]: ../brain/inbox/youtube-oauth-scopes-and-identity.md
[tokens]: ../brain/inbox/youtube-oauth-token-lifecycle.md
[metadata]: ../brain/inbox/prompt-injection-untrusted-metadata.md
[channels]: ../brain/inbox/youtube-similarity-without-related-endpoint.md
[skill-format]: ../brain/resources/agent-skills-format.md
[para]: ../brain/resources/para-method.md
[skill-validation]: ../brain/areas/decision-skill-validation.md
[ci]: ../.github/workflows/ci.yml

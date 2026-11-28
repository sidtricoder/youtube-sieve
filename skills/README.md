# Agent Skills

Each folder here is an [Agent Skill](https://agentskills.io/specification): a `SKILL.md` with instructions an AI agent loads when a task calls for it. Skills serve one of two audiences, declared in every skill's frontmatter as `metadata.audience`.

| Audience | Who uses it | Served by the MCP server? |
|---|---|---|
| `product` | End users' AI clients (Claude, ChatGPT, Gemini) working with youtube-sieve's MCP tools | **Yes**, as an MCP resource and prompt (IF-2, IF-3) |
| `team` | The team's own coding agents, while developing youtube-sieve | **Never**: development tooling only |

## Skills

| Skill | Audience | Purpose |
|---|---|---|
| [`brain-ingest`](brain-ingest/SKILL.md) | team | Capture a source into `brain/inbox/` as schema-valid notes |
| [`brain-refine`](brain-refine/SKILL.md) | team | Check, merge, link and file inbox notes as distilled notes |
| [`brain-query`](brain-query/SKILL.md) | team | Answer questions and draft documents from distilled notes, with citations |

Planned: `local-check` (team, #52) and `video-to-playlist` (product, SK-1).

## Rules

- Every skill declares `metadata.audience: product` or `metadata.audience: team`.
- Every skill cites at least one distilled note in `brain/` with a `[[wikilink]]` in its body (SB-3).
- The MCP server must serve **only** `product` skills. `tools.validate_skills.skills_by_audience()` lists skills by audience for that purpose.

CI checks the specification and both project rules with `python -m tools.validate_skills`.

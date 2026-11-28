---
title: Validating Agent Skills with skills-ref plus a project citation rule
type: decision
status: distilled
created: 2026-11-22
updated: 2026-11-28
authors: [sidtricoder]
tags: [decision, ci, skills]
requirements: [SB-3, SB-5, SK-1, IF-2, IF-3]
sources: [https://agentskills.io/specification, https://pypi.org/project/skills-ref/]
---

# Validating Agent Skills with skills-ref plus a project citation rule

**Status:** accepted
**Issue / PR:** #9; skill audience: #62

## Context
Every skill must be checked in CI: its `SKILL.md` frontmatter and naming must follow the Agent Skills specification, and the project requires each skill to cite at least one distilled note (SB-3). The specification has detailed rules: name length and characters, no consecutive hyphens, the name matching its directory, description length limits and the set of allowed fields.

## Options considered
1. **Write our own specification checks.** Full control, but it duplicates rules that already have an official implementation, and our copy would drift as the specification changes.
2. **Use the official `skills-ref` reference library for the specification, and add only the project rule ourselves.** The specification checks are maintained by its authors; our code covers only what is specific to this repository.
3. **Call the `agentskills validate` command from CI.** Simple, but the citation rule would still need separate code, and two tools would report problems in two formats.

## Decision
Option 2. `tools/validate_skills.py` calls `skills_ref.validate()` for each skill directory, then applies the citation rule by reusing the vault parsing and link handling from `tools/validate_brain.py` (see [[decision-ci-and-validation-tooling]]). Both validators share one `Problem` record and one reporting function, so output looks the same in CI.

## Consequences
- `skills-ref` is pinned (0.1.1, Apache-2.0) in the `dev` dependency group; upgrading it may add new specification checks.
- A skill's citation counts only if it is a `[[wikilink]]` in the body (not in frontmatter or code) to a note with `status: distilled`, which the vault validator separately confirms is in a PARA folder.
- Shared validator code lives in `tools/problems.py` and `tools/reporting.py`.

## Addendum: each skill declares its audience (#62)
The skills folder holds two kinds of skill: **product** skills such as `video-to-playlist` (SK-1), which the MCP server serves to end users' AI clients as a resource and a prompt (IF-2, IF-3), and **team** skills such as the brain skills and `local-check`, which are development tooling. Without a marker, a server could serve team tooling to every client.

- **Options:** separate folders (`skills/product/`, `skills/team/`) or a frontmatter field. Separate folders would break the one-folder-per-skill layout that the validator and the Agent Skills format assume ([[agent-skills-format]]). The specification's `metadata` map is meant for exactly this kind of client-specific property.
- **Decision:** every skill declares `metadata.audience: product` or `team`. `tools/validate_skills.py` rejects a missing or unknown value, and `skills_by_audience()` gives the server the list of `product` skills to serve. `skills/README.md` lists every skill with its audience.

## Related
- [[index]]
- [[para-method]]
- [[agent-skills-format]]

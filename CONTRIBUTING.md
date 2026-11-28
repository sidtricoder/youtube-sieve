# Contributing to youtube-sieve

Thanks for contributing. This document describes how work moves from an idea to `main`.

## Workflow at a glance

1. **Open an issue** using a template. Describe the context, scope and acceptance criteria.
2. **Create a branch** from an up-to-date `main`.
3. **Commit** in small, logical steps using Conventional Commits.
4. **Open a pull request** that closes the issue, and request a reviewer.
5. **Address review**, get at least one approval and green checks.
6. **Merge with a merge commit.** GitHub deletes the branch automatically.

`main` is protected: nobody pushes to it directly, including administrators.

## Issues

- Every change starts with an issue, including documentation and knowledge-base notes.
- Add labels for **type** (`type: feature`, `type: bug`, `type: docs`, `type: chore`, `type: test`, `type: ci`) and **area** (`area: architecture`, `area: brain`, `area: mcp`, `area: repo`).
- Assign the issue to yourself before starting, so work is not duplicated.
- Reference SRS requirement IDs (for example `FR-1`) where relevant.

## Branches

Name branches `<type>/<issue-number>-<short-slug>`:

```
feat/12-similar-videos
fix/31-duration-parsing
docs/8-tfidf-research-note
chore/3-governance-files
```

Keep branches short-lived.

### Keeping a branch up to date

If `main` moves ahead while you work, **merge `main` into your branch**. Do not rebase a branch that is already pushed: rebasing rewrites commits that reviewers have commented on and needs a force-push.

```bash
git fetch origin
git merge origin/main
```

The most common conflict is in `CHANGELOG.md`, where several pull requests add a line to the same list under `[Unreleased]`. Keep **both** sides' lines, remove the conflict markers, and make sure each list heading (`### Added`, `### Changed`, `### Fixed`) appears only once.

### Stacked pull requests

When one change builds on another that is still in review, branch from the first branch and open the second pull request against it, not against `main`. Say "Stacked on #n" in the description. Merge them in order: when the first is merged and its branch deleted, GitHub retargets the next one to `main`.

## Commits

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<optional scope>): <imperative summary, at most 72 characters>

<optional body explaining why>
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`, `perf`.
Write in the imperative mood ("add", not "added"). Do not mix unrelated changes in one commit.

Because pull requests are merged with a merge commit, **every commit on your branch lands on `main` as it is**. Each one must follow this format, not only the pull request title. Tidy work-in-progress commits before asking for review.

## Pull requests

- Update the affected rows in the [traceability matrix](docs/traceability.md) with the issue, PR and verification evidence before requesting review.

- One issue per pull request. Aim for fewer than about 400 changed lines.
- Fill in every section of the template, and write `Closes #<n>`.
- Open a **draft** pull request early if you want feedback on direction.
- The pull request title follows Conventional Commits too; it appears in the merge commit (`Merge pull request #n …`) and in the pull request list.
- Merge with **Create a merge commit** once the pull request is approved and CI is green. The branch is deleted automatically after merging.

## Review

- Every pull request needs **at least one approval from someone other than the author**.
- Reviewers check correctness, tests, readability and security; linters handle style.
- Keep comments about the code. Prefix minor points with `nit:` and explain the reason for a requested change.
- Authors reply to or resolve every comment. Authors never merge without an approval.

## Definition of Done

A change is done when:

- [ ] the issue's acceptance criteria are all met;
- [ ] tests are added or updated and pass;
- [ ] documentation and `CHANGELOG.md` are updated;
- [ ] CI is green;
- [ ] it has been reviewed and approved.

## AI-assisted work

AI coding assistants are welcome, but the author is responsible for every merged line.

- Disclose AI assistance in the pull request.
- A human reviews every AI-generated change.
- Never paste secrets, tokens or credentials into an AI tool.
- Record significant AI sessions in the knowledge base (`brain/`).

## One-time git setup

```bash
git config --global fetch.prune true   # forget branches deleted on GitHub after their PR merges
git config user.name  "Your Name"      # in this repository: the name and email of your GitHub account,
git config user.email "you@example.com"  # so commits are attributed to you
```

Without `fetch.prune`, pulling a branch that was merged and deleted on GitHub fails with "couldn't find remote ref".

## Running checks locally

CI runs these on every pull request; run them before you push. You need Python 3.12 and pip 25.1 or newer.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --group dev -e .   # dev tools + the package in editable mode

ruff check .                      # lint
ruff format .                     # format (CI runs: ruff format --check .)
pytest --cov                      # tests, fails below 90% coverage
python -m tools.validate_brain    # knowledge-base schema
python -m tools.validate_skills   # Agent Skills: specification + cites a distilled note
```

## Skills

Agent Skills live in `skills/<name>/SKILL.md` and follow the [Agent Skills specification](https://agentskills.io/specification). Each skill must cite at least one distilled note in `brain/` with a `[[wikilink]]` in its body, and declare its audience as `metadata.audience`: `product` for skills the MCP server serves to AI clients, or `team` for development tooling (see `skills/README.md`). CI checks all three.

## Security

Never commit secrets, OAuth client files, tokens or real user data. `.env` and `client_secret*.json` are ignored by git; use `.env.example` for documented placeholders.

# youtube-sieve

An MCP server that lets an AI client (Claude, ChatGPT, Gemini) find, analyse and curate YouTube videos for a user, ranking them by objective metadata instead of engagement, using only the official YouTube Data API v3. Playlists are created in the user's account only after they confirm in their own browser.

Team NimbleNibble, Software Engineering Lab, IIIT-Bangalore.

## Status

**Stage 1 (requirements) complete; Stage 2 (design) in progress.** The pure domain layer exists: ISO 8601 duration parsing, TF-IDF similarity ranking and quota budget arithmetic. The YouTube provider, MCP server, sign-in and playlist pages are not built yet. See [`CHANGELOG.md`](CHANGELOG.md).

## Quick start

Requires Python 3.12 and pip 25.1 or newer.

```bash
git clone https://github.com/sidtricoder/youtube-sieve.git
cd youtube-sieve
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -c requirements.lock --group dev -e .
```

Start the local HTTP server:

```bash
python -m youtube_sieve
```

From another terminal, run `curl http://127.0.0.1:8000/health`. A running server
returns HTTP 200 and `{"status":"ok"}`. Press Ctrl+C in the server terminal to stop it.
To change the bind address or port, export the variables shown in [.env.example](.env.example)
before starting the server.

Run the same checks as CI:

```bash
ruff check . && ruff format --check .
pytest --cov
python -m tools.validate_brain
python -m tools.validate_skills
```

## Documentation

| Document | What it covers |
|---|---|
| [`docs/srs.md`](docs/srs.md) | Software Requirements Specification: every requirement and its ID |
| [`docs/adr/`](docs/adr/README.md) | Architecture Decision Records |
| [`brain/index.md`](brain/index.md) | Team knowledge base (Obsidian vault): research and decision notes |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Issues, branches, commits, pull requests, review, local checks |
| [`AGENTS.md`](AGENTS.md) | Instructions for AI coding agents, and design and testing rules |
| [`skills/`](skills/) | Agent Skills, such as `brain-ingest` |

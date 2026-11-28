"""Validate every Agent Skill under skills/.

Two layers of rules:
1. The Agent Skills specification, checked by the official `skills-ref` reference library.
2. Project rules: each SKILL.md cites at least one distilled note in the knowledge base (SB-3),
   contains no broken [[wikilinks]], and declares its audience in `metadata.audience`:
   `product` skills are served to AI clients by the MCP server; `team` skills are development
   tooling and are never served. Vault parsing is reused from tools.validate_brain.

Usage: python -m tools.validate_skills [--skills DIR] [--brain DIR]
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Iterable
from pathlib import Path, PurePosixPath

from skills_ref import validate as validate_specification

from tools.problems import Problem
from tools.reporting import report
from tools.validate_brain import Note, Vault, link_targets, load_vault, parse_note

DEFAULT_SKILLS = Path("skills")
DEFAULT_VAULT = Path("brain")
SKILL_FILE = "SKILL.md"
AUDIENCE_KEY = "audience"
AUDIENCES = frozenset({"product", "team"})
AUDIENCE_HINT = "product (served to AI clients) or team (development tooling)"


def skill_directories(skills_root: Path) -> list[Path]:
    """Each visible subdirectory of the skills folder is one skill."""
    return sorted(p for p in skills_root.iterdir() if p.is_dir() and not p.name.startswith("."))


def _display_path(skills_root: Path, path: Path) -> PurePosixPath:
    return PurePosixPath(skills_root.name, *path.relative_to(skills_root).parts)


def read_skill(skill_md: Path) -> Note:
    """Parse a SKILL.md into frontmatter and body, with the vault's parser."""
    return parse_note(PurePosixPath(SKILL_FILE), skill_md.read_text(encoding="utf-8"))


def check_citations(body: str, vault: Vault) -> Iterable[str]:
    """Body links must resolve, and at least one must point at a distilled note."""
    targets = [t for t in link_targets(body) if t]
    known, distilled = vault.known_targets(), vault.distilled_names()
    for target in targets:
        if target not in known:
            yield f"broken link [[{target}]]: no note or attachment with that name in brain/"
    if not any(t in distilled for t in targets):
        yield "skill must cite at least one distilled note in brain/ with [[...]] (SB-3)"


def declared_audience(frontmatter: dict) -> object:
    """The raw `metadata.audience` value, or None when it is not declared."""
    metadata = frontmatter.get("metadata")
    return metadata.get(AUDIENCE_KEY) if isinstance(metadata, dict) else None


def check_audience(frontmatter: dict | None) -> Iterable[str]:
    """`metadata.audience` must be one of AUDIENCES. Missing frontmatter is a spec error."""
    if frontmatter is None:
        return
    audience = declared_audience(frontmatter)
    if audience is None:
        yield f"skill must declare metadata.audience: {AUDIENCE_HINT}"
    elif audience not in AUDIENCES:
        yield f"metadata.audience is {audience!r}; use {AUDIENCE_HINT}"


def skills_by_audience(skills_root: Path) -> dict[str, list[str]]:
    """Skill names grouped by declared audience; skills without a valid audience are left out."""
    grouped: dict[str, list[str]] = {audience: [] for audience in sorted(AUDIENCES)}
    for directory in skill_directories(skills_root):
        skill_md = directory / SKILL_FILE
        frontmatter = read_skill(skill_md).frontmatter if skill_md.is_file() else None
        audience = declared_audience(frontmatter) if frontmatter else None
        if audience in AUDIENCES:
            grouped[audience].append(directory.name)
    return grouped


def validate_skill(skill_dir: Path, skills_root: Path, vault: Vault | None) -> list[Problem]:
    skill_md = skill_dir / SKILL_FILE
    shown = _display_path(skills_root, skill_md if skill_md.is_file() else skill_dir)
    messages = list(validate_specification(skill_dir))
    if skill_md.is_file():
        skill = read_skill(skill_md)
        messages.extend(check_audience(skill.frontmatter))
        if vault is not None:
            messages.extend(check_citations(skill.body, vault))
    return [Problem(shown, message) for message in messages]


def validate(skills_root: Path, vault_root: Path) -> list[Problem]:
    if not skills_root.is_dir():
        return [
            Problem(
                PurePosixPath(skills_root.name), f"skills folder '{skills_root}' does not exist"
            )
        ]
    directories = skill_directories(skills_root)
    if not directories:
        return [Problem(PurePosixPath(skills_root.name), "no skills found")]
    problems: list[Problem] = []
    vault = load_vault(vault_root) if vault_root.is_dir() else None
    if vault is None:
        problems.append(
            Problem(
                PurePosixPath(vault_root.name), f"vault directory '{vault_root}' does not exist"
            )
        )
    for directory in directories:
        problems.extend(validate_skill(directory, skills_root, vault))
    return sorted(set(problems))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Agent Skills under skills/.")
    parser.add_argument("--skills", type=Path, default=DEFAULT_SKILLS, help="skills folder")
    parser.add_argument("--brain", type=Path, default=DEFAULT_VAULT, help="knowledge-base vault")
    args = parser.parse_args(argv)
    return report(validate(args.skills, args.brain), args.skills, "CONTRIBUTING.md")


if __name__ == "__main__":
    sys.exit(main())

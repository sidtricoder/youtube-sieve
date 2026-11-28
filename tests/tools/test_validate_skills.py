"""Unit tests for tools/validate_skills.py."""

from pathlib import Path, PurePosixPath

import pytest

from tests.tools.vault_builder import Vault
from tools import validate_skills as vs

DISTILLED_NOTE = "tfidf-cosine-similarity"  # created in resources/ by Vault
CITATION = f"Based on [[{DISTILLED_NOTE}]].\n"


class Repo:
    """A throwaway repository with a valid vault and a skills folder."""

    def __init__(self, root: Path):
        self.root = root
        self.vault = Vault(root / "brain")
        self.skills = root / "skills"
        self.skills.mkdir()

    def skill(self, name: str, body: str = CITATION, *, frontmatter: str | None = None) -> Path:
        directory = self.skills / name
        directory.mkdir(parents=True, exist_ok=True)
        if frontmatter is None:
            frontmatter = (
                f"name: {name}\ndescription: Does one thing. Use when testing.\n"
                "metadata:\n  audience: team"
            )
        path = directory / "SKILL.md"
        path.write_text(f"---\n{frontmatter}\n---\n\n# {name}\n\n{body}", encoding="utf-8")
        return path

    def problems(self) -> list[str]:
        return [str(p) for p in vs.validate(self.skills, self.root / "brain")]


@pytest.fixture
def repo(tmp_path: Path) -> Repo:
    return Repo(tmp_path)


def assert_single_problem(repo: Repo, *fragments: str) -> None:
    problems = repo.problems()
    assert len(problems) == 1, problems
    for fragment in fragments:
        assert fragment in problems[0], problems


# --- Discovery ------------------------------------------------------------------------------


def test_valid_skill_has_no_problems(repo):
    repo.skill("brain-ingest")
    assert repo.problems() == []


def test_several_valid_skills_have_no_problems(repo):
    for name in ("brain-ingest", "brain-refine", "local-check"):
        repo.skill(name)
    assert repo.problems() == []


def test_missing_skills_folder_is_reported(tmp_path):
    Vault(tmp_path / "brain")
    problems = [str(p) for p in vs.validate(tmp_path / "skills", tmp_path / "brain")]
    assert len(problems) == 1 and "does not exist" in problems[0]


def test_empty_skills_folder_is_reported(repo):
    assert_single_problem(repo, "no skills")


def test_files_directly_in_skills_folder_are_ignored(repo):
    repo.skill("brain-ingest")
    (repo.skills / "README.md").write_text("# Skills\n", encoding="utf-8")
    assert repo.problems() == []


def test_hidden_directories_are_ignored(repo):
    repo.skill("brain-ingest")
    (repo.skills / ".cache").mkdir()
    assert repo.problems() == []


def test_skill_directory_without_skill_md_is_reported(repo):
    repo.skill("brain-ingest")
    (repo.skills / "brain-query").mkdir()
    assert_single_problem(repo, "brain-query", "SKILL.md")


# --- Agent Skills specification (delegated to skills-ref) -----------------------------------


@pytest.mark.parametrize(
    ("directory", "frontmatter", "fragment"),
    [
        ("brain-ingest", "name: Brain-Ingest\ndescription: d", "lowercase"),
        ("brain-ingest", "name: other-name\ndescription: d", "must match"),
        ("brain-ingest", "name: brain-ingest", "description"),
        ("brain-ingest", "name: brain-ingest\ndescription: d\nauthor: me", "Unexpected"),
        ("brain-ingest", "name: brain-ingest\ndescription: " + "x" * 1025, "1024"),
        ("brain--ingest", "name: brain--ingest\ndescription: d", "consecutive"),
    ],
)
def test_specification_violations_are_reported(repo, directory, frontmatter, fragment):
    repo.skill(directory, frontmatter=frontmatter)
    problems = repo.problems()
    assert any(fragment in p and directory in p for p in problems), problems


def test_skill_md_without_frontmatter_is_reported(repo):
    directory = repo.skills / "brain-ingest"
    directory.mkdir()
    (directory / "SKILL.md").write_text(CITATION, encoding="utf-8")
    problems = repo.problems()
    assert any("frontmatter" in p for p in problems), problems


def test_optional_specification_fields_are_accepted(repo):
    frontmatter = (
        "name: brain-ingest\ndescription: Does one thing.\nlicense: MIT\n"
        "compatibility: Requires Python 3.12\nmetadata:\n  owner: team\n  audience: product"
    )
    repo.skill("brain-ingest", frontmatter=frontmatter)
    assert repo.problems() == []


# --- Project rule: cite at least one distilled note (SB-3) ----------------------------------


def test_skill_without_any_note_link_is_reported(repo):
    repo.skill("brain-ingest", body="No citation here.\n")
    assert_single_problem(repo, "brain-ingest", "distilled note")


def test_skill_citing_only_an_inbox_note_is_reported(repo):
    repo.vault.note("inbox/raw-capture.md", status="inbox")
    repo.skill("brain-ingest", body="See [[raw-capture]].\n")
    assert_single_problem(repo, "distilled note")


def test_skill_citing_only_an_archived_note_is_reported(repo):
    repo.vault.note("archive/old-idea.md", status="archived")
    repo.skill("brain-ingest", body="See [[old-idea]].\n")
    assert_single_problem(repo, "distilled note")


def test_skill_citing_only_special_files_is_reported(repo):
    repo.skill("brain-ingest", body="See [[index]] and [[AGENTS]].\n")
    assert_single_problem(repo, "distilled note")


def test_one_distilled_citation_among_others_is_enough(repo):
    repo.vault.note("inbox/raw-capture.md", status="inbox")
    repo.skill("brain-ingest", body=f"See [[index]], [[raw-capture]]. {CITATION}")
    assert repo.problems() == []


@pytest.mark.parametrize(
    "link",
    [
        f"[[{DISTILLED_NOTE}|alias]]",
        f"[[{DISTILLED_NOTE}#Summary]]",
        f"[[{DISTILLED_NOTE}.md]]",
        f"[[{DISTILLED_NOTE.upper()}]]",
    ],
)
def test_citation_link_forms_resolve(repo, link):
    repo.skill("brain-ingest", body=f"{link}\n")
    assert repo.problems() == []


def test_broken_link_in_skill_is_reported(repo):
    repo.skill("brain-ingest", body=f"{CITATION}See [[missing-note]].\n")
    assert_single_problem(repo, "broken link", "missing-note")


def test_citation_inside_code_does_not_count(repo):
    repo.skill("brain-ingest", body=f"`[[{DISTILLED_NOTE}]]`\n\n```\n[[{DISTILLED_NOTE}]]\n```\n")
    assert_single_problem(repo, "distilled note")


def test_citation_in_frontmatter_does_not_count(repo):
    frontmatter = (
        f"name: brain-ingest\ndescription: Uses [[{DISTILLED_NOTE}]].\nmetadata:\n  audience: team"
    )
    repo.skill("brain-ingest", body="No citation.\n", frontmatter=frontmatter)
    assert_single_problem(repo, "distilled note")


def test_missing_vault_is_reported(tmp_path):
    (tmp_path / "skills" / "brain-ingest").mkdir(parents=True)
    (tmp_path / "skills" / "brain-ingest" / "SKILL.md").write_text(
        f"---\nname: brain-ingest\ndescription: d\n---\n{CITATION}", encoding="utf-8"
    )
    problems = [str(p) for p in vs.validate(tmp_path / "skills", tmp_path / "brain")]
    assert any("vault" in p and "does not exist" in p for p in problems), problems


# --- Project rule: every skill declares its audience ----------------------------------------


@pytest.mark.parametrize("audience", sorted(vs.AUDIENCES))
def test_each_documented_audience_is_accepted(repo, audience):
    frontmatter = f"name: brain-ingest\ndescription: d\nmetadata:\n  audience: {audience}"
    repo.skill("brain-ingest", frontmatter=frontmatter)
    assert repo.problems() == []


def test_skill_without_metadata_is_reported(repo):
    repo.skill("brain-ingest", frontmatter="name: brain-ingest\ndescription: d")
    assert_single_problem(repo, "brain-ingest", "audience")


def test_skill_with_metadata_but_no_audience_is_reported(repo):
    repo.skill(
        "brain-ingest", frontmatter="name: brain-ingest\ndescription: d\nmetadata:\n  stage: x"
    )
    assert_single_problem(repo, "audience", "product", "team")


@pytest.mark.parametrize("value", ["Team", "public", "users", "''"])
def test_unknown_audience_is_reported(repo, value):
    frontmatter = f"name: brain-ingest\ndescription: d\nmetadata:\n  audience: {value}"
    repo.skill("brain-ingest", frontmatter=frontmatter)
    assert_single_problem(repo, "audience")


def test_audience_outside_metadata_does_not_count(repo):
    repo.skill("brain-ingest", frontmatter="name: brain-ingest\ndescription: d\naudience: team")
    problems = repo.problems()
    assert any("audience" in p and "metadata" in p for p in problems), problems


def test_audience_problem_is_reported_alongside_other_problems(repo):
    repo.skill(
        "brain-ingest", body="No citation.\n", frontmatter="name: brain-ingest\ndescription: d"
    )
    problems = repo.problems()
    assert any("audience" in p for p in problems) and any("distilled note" in p for p in problems)


def test_skills_by_audience_lists_each_skill(repo):
    repo.skill("brain-ingest")
    repo.skill(
        "video-to-playlist",
        frontmatter=("name: video-to-playlist\ndescription: d\nmetadata:\n  audience: product"),
    )
    assert vs.skills_by_audience(repo.skills) == {
        "product": ["video-to-playlist"],
        "team": ["brain-ingest"],
    }


@pytest.mark.parametrize(
    "frontmatter",
    [
        "name: brain-ingest\ndescription: d",
        "name: brain-ingest\ndescription: d\nmetadata:\n  audience: public",
        "name: brain-ingest\ndescription: d\nmetadata:\n  audience: Team",
    ],
)
def test_skills_by_audience_skips_skills_without_a_valid_audience(repo, frontmatter):
    repo.skill("brain-ingest", frontmatter=frontmatter)
    assert vs.skills_by_audience(repo.skills) == {"product": [], "team": []}


def test_skills_by_audience_skips_directories_without_skill_md(repo):
    repo.skill("brain-ingest")
    (repo.skills / "empty-folder").mkdir()
    assert vs.skills_by_audience(repo.skills) == {"product": [], "team": ["brain-ingest"]}


def test_repository_skills_all_declare_an_audience():
    root = Path(__file__).resolve().parents[2]
    grouped = vs.skills_by_audience(root / "skills")
    declared = sorted(name for names in grouped.values() for name in names)
    assert declared == sorted(p.name for p in vs.skill_directories(root / "skills"))


# --- Reporting and CLI ----------------------------------------------------------------------


def test_problem_path_is_relative_to_repository(repo):
    repo.skill("brain-ingest", body="No citation.\n")
    problem = vs.validate(repo.skills, repo.root / "brain")[0]
    assert problem.path == PurePosixPath("skills/brain-ingest/SKILL.md")


def test_problems_from_all_skills_are_reported_and_sorted(repo):
    repo.skill("zeta-skill", body="none\n")
    repo.skill("alpha-skill", body="none\n")
    paths = [p.path for p in vs.validate(repo.skills, repo.root / "brain")]
    assert len(paths) == 2 and paths == sorted(paths)


def test_main_returns_zero_for_valid_skills(repo, capsys):
    repo.skill("brain-ingest")
    args = ["--skills", str(repo.skills), "--brain", str(repo.root / "brain")]
    assert vs.main(args) == 0
    assert "no problems" in capsys.readouterr().out


def test_main_returns_one_and_lists_problems(repo, capsys):
    repo.skill("brain-ingest", body="none\n")
    args = ["--skills", str(repo.skills), "--brain", str(repo.root / "brain")]
    assert vs.main(args) == 1
    out = capsys.readouterr().out
    assert "skills/brain-ingest/SKILL.md" in out and "1 problem" in out


def test_main_uses_repository_defaults(repo, monkeypatch):
    repo.skill("brain-ingest")
    monkeypatch.chdir(repo.root)
    assert vs.main([]) == 0


def test_repository_skills_are_valid():
    root = Path(__file__).resolve().parents[2]
    assert [str(p) for p in vs.validate(root / "skills", root / "brain")] == []

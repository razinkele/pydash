import subprocess
import re
import pytest
from pathlib import Path


def _run_git(cmd):
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True)
        return out.strip()
    except Exception:
        return None


def _is_release_context():
    # Determine whether we're running on main branch or tag push (where we want strict checks)
    github_ref = subprocess.os.environ.get("GITHUB_REF", "")
    if github_ref.startswith("refs/tags/"):
        return True
    if github_ref == "refs/heads/main":
        return True
    # Fallback: check local branch name
    branch = _run_git(["git", "rev-parse", "--abbrev-ref", "HEAD"]) or ""
    return branch == "main"


def test_changelog_has_release_section_for_tag_or_is_present():
    # Only enforce on main or tag pushes (release validation contexts)
    if not _is_release_context():
        pytest.skip("Not running in release-validation context; skipping CHANGELOG presence check")

    # Ensure CHANGELOG.md exists and is non-empty
    changelog = Path("CHANGELOG.md")
    assert changelog.exists(), "CHANGELOG.md is missing; please add a changelog"
    content = changelog.read_text(encoding="utf8").strip()
    assert content, "CHANGELOG.md is empty; please add recent release notes"

    # If running on a tag, ensure there's a section for that tag
    github_ref = subprocess.os.environ.get("GITHUB_REF", "")
    if github_ref and github_ref.startswith("refs/tags/"):
        tag = github_ref.replace("refs/tags/", "")
    else:
        # fallback: try to find the most recent tag that matches v* and assert changelog contains it
        tag = _run_git(["git", "describe", "--tags", "--abbrev=0"]) or ""

    if tag:
        # Accept headings like '## vX.Y.Z' or '## X.Y.Z'
        pattern = re.compile(rf"^##\s+v?{re.escape(tag.lstrip('v'))}", re.IGNORECASE | re.MULTILINE)
        assert pattern.search(content), (
            f"CHANGELOG.md does not contain a section for tag '{tag}'. Add a '## {tag}' section."
        )


def test_commits_since_last_tag_follow_conventional_commits():
    # Only enforce conventional commits in release-validation contexts (main or tag pushes)
    if not _is_release_context():
        pytest.skip("Not running in release-validation context; skipping conventional commit checks")

    # Skip if git not available
    if not _run_git(["git", "rev-parse", "--git-dir"]):
        pytest.skip("git not available in environment")

    # Find the most recent tag (v*). If none, check last 50 commits
    last_tag = _run_git(["git", "describe", "--tags", "--abbrev=0"]) or None
    if last_tag:
        rev_range = f"{last_tag}..HEAD"
    else:
        # use a reasonable default range
        rev_range = "HEAD~50..HEAD"

    log = _run_git(["git", "log", "--pretty=%s", rev_range])
    if not log:
        pytest.skip("No commits in range to check for conventional commits")

    subjects = [s.strip() for s in log.splitlines() if s.strip()]
    # Conventional commit regex (simple): type(scope)?: description
    cc_re = re.compile(r"^(feat|fix|docs|style|refactor|perf|test|chore|build|ci)(\([^)]+\))?:\s+.+", re.IGNORECASE)

    bad = [s for s in subjects if not cc_re.match(s)]
    if bad:
        bad_preview = "\n".join(bad[:10])
        pytest.fail(
            "Found commit messages that do not follow Conventional Commits spec:\n" + bad_preview
        )

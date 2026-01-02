import subprocess
import pytest


def _run_git_cmd(cmd):
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True)
        return out.strip()
    except Exception:
        return None


def test_release_tags_are_annotated():
    # Ensure git is available and we can list tags
    git_dir = _run_git_cmd(["git", "rev-parse", "--git-dir"])
    if not git_dir:
        pytest.skip("git not available in the environment")

    tags_out = _run_git_cmd(["git", "tag", "--list", "v*"])
    if not tags_out:
        pytest.skip("No tags matching 'v*' found; skipping tag annotation check")

    tags = [t.strip() for t in tags_out.splitlines() if t.strip()]
    assert tags, "No release tags found"

    non_annotated = []
    empty_messages = []

    for tag in tags:
        typ = _run_git_cmd(["git", "cat-file", "-t", tag])
        # annotated tags have type 'tag'
        if typ != "tag":
            non_annotated.append((tag, typ))
            continue
        # check message content
        msg = _run_git_cmd(["git", "tag", "-l", "--format=%(contents)", tag]) or ""
        if not msg.strip():
            empty_messages.append(tag)

    if non_annotated:
        pytest.fail(
            "Found non-annotated release tags: "
            + ", ".join(f"{t} (type={typ})" for t, typ in non_annotated)
        )

    if empty_messages:
        pytest.fail("Found annotated tags with empty messages: " + ", ".join(empty_messages))

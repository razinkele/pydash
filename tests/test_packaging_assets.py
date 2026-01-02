import tarfile
import zipfile
from pathlib import Path
import pytest


def test_assets_in_built_distributions(tmp_path):
    build = pytest.importorskip("build")

    project_root = Path(__file__).resolve().parents[1]
    dist_dir = tmp_path / "dist"
    dist_dir.mkdir()

    builder = build.ProjectBuilder(str(project_root))
    # Build sdist and wheel into temporary dist dir
    sdist_path = builder.build("sdist", str(dist_dir))
    wheel_path = builder.build("wheel", str(dist_dir))

    # Check wheel (zip archive)
    with zipfile.ZipFile(str(wheel_path), "r") as zf:
        names = zf.namelist()
        assert any(
            "bs4dash_controlbar.js" in n for n in names
        ), f"bs4dash_controlbar.js not found in wheel: {wheel_path}"

    # Check sdist (tar.gz)
    with tarfile.open(str(sdist_path), "r:gz") as tf:
        names = tf.getnames()
        assert any(
            "bs4dash_controlbar.js" in n for n in names
        ), f"bs4dash_controlbar.js not found in sdist: {sdist_path}"

"""Consistency tests: README claims must match real runs and real numbers."""

import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def test_readme_quoted_output_matches_real_run() -> None:
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    run = subprocess.run(
        [sys.executable, "-m", "rig_ai.cli", "score", "-f", str(REPO / "examples" / "calibration" / "solid.txt")],
        capture_output=True, text=True, check=True,
    )
    assert "RIG Prompt Score: 18/40 (D)" in readme
    assert "RIG Prompt Score: 18/40 (D)" in run.stdout
    assert "Actionability   9/10" in readme
    assert "Actionability   9/10" in run.stdout


def test_readme_calibration_table_matches_expected_json() -> None:
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    expected = json.loads((REPO / "examples" / "calibration" / "expected.json").read_text(encoding="utf-8"))
    for name, want in expected.items():
        if name.startswith("_"):
            continue
        assert f"| {name} | {want['total']} | {want['grade']} |" in readme


def test_readme_template_count_is_real() -> None:
    from rig_ai.prompt_engine import PromptEngine

    readme = (REPO / "README.md").read_text(encoding="utf-8")
    assert len(PromptEngine._load_templates()) == 20
    assert "20 prompt templates" in readme


def test_changelog_version_matches_package() -> None:
    changelog = (REPO / "CHANGELOG.md").read_text(encoding="utf-8")
    pyproject = (REPO / "pyproject.toml").read_text(encoding="utf-8")
    pkg_version = re.search(r'^version = "([^"]+)"', pyproject, re.M).group(1)
    assert f"## [{pkg_version}]" in changelog


def test_readme_copy_rules() -> None:
    readme = (REPO / "README.md").read_text(encoding="utf-8").lower()
    for word in ("unlock", "empower", "synergy", "leverage", "disrupt",
                 "hustle", "utilize", "iterate", "optimize"):
        assert word not in readme, word
    assert "—" not in readme

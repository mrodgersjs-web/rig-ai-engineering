"""Tests for the rig-ai command line."""

import json

import pytest

from rig_ai.cli import main


def test_score_prints_total_and_grade(capsys) -> None:
    code = main(["score", "-p", "Write tests for src/util.py covering the parse error path."])
    out = capsys.readouterr().out
    assert code == 0
    assert "RIG Prompt Score:" in out
    assert "/40" in out


def test_score_json(capsys) -> None:
    code = main(["score", "-p", "Add a --json flag to cli.py.", "--json"])
    out = json.loads(capsys.readouterr().out)
    assert code == 0
    assert out["total"] == sum(out[a] for a in ("specificity", "doctrine", "context", "actionability"))


def test_score_requires_input(monkeypatch) -> None:
    import sys

    class Tty:
        def isatty(self) -> bool:
            return True

    monkeypatch.setattr(sys, "stdin", Tty())
    code = main(["score"])
    assert code == 1


def test_enhance_and_fix(capsys) -> None:
    assert main(["enhance", "-p", "fix the bug"]) == 0
    assert "Acceptance criteria" in capsys.readouterr().out
    assert main(["fix", "-p", "hi, can you just fix it?"]) == 0
    assert capsys.readouterr().out.strip()


def test_doctor_reports_healthy(capsys) -> None:
    assert main(["doctor"]) == 0
    assert "HEALTHY" in capsys.readouterr().out


def test_suggest_returns_templates(capsys) -> None:
    assert main(["suggest", "write unit tests"]) == 0
    out = capsys.readouterr().out
    assert "unit-test" in out


def test_axes_prints_rubric(capsys) -> None:
    assert main(["axes"]) == 0
    out = capsys.readouterr().out
    assert "Specificity" in out
    assert "Grade bands" in out


def test_axes_json(capsys) -> None:
    assert main(["axes", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert len(out["axes"]) == 4
    assert out["grade_bands"]


def test_score_from_file(tmp_path, capsys) -> None:
    f = tmp_path / "p.txt"
    f.write_text("Implement rate limiting in src/api.py with a 100 req/min cap.", encoding="utf-8")
    assert main(["score", "--file", str(f), "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["total"] > 0


def test_unknown_command() -> None:
    with pytest.raises(SystemExit):
        main([])

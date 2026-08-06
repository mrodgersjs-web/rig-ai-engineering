"""Tests for the RIG Prompt Intelligence Engine."""

import pytest

from rig_ai import prompt_engine


def test_score_returns_four_axes():
    result = prompt_engine.score("Write a Python function that returns the sum of two integers.")
    assert "specificity" in result
    assert "doctrine" in result
    assert "context" in result
    assert "actionability" in result
    assert "total" in result
    assert "feedback" in result
    assert "grade" in result
    for axis in ("specificity", "doctrine", "context", "actionability"):
        assert 0 <= result[axis] <= 10
    assert result["total"] == sum(result[a] for a in ("specificity", "doctrine", "context", "actionability"))


def test_score_empty_prompt():
    result = prompt_engine.score("")
    assert result["total"] == 0
    assert result["grade"] == "F"


def test_enhance_returns_longer_prompt():
    original = "fix the bug"
    enhanced = prompt_engine.enhance(original)
    assert len(enhanced) > len(original)
    assert "Acceptance criteria" in enhanced or "Verification" in enhanced


def test_enhance_adds_lattice_coordinate():
    enhanced = prompt_engine.enhance("fix the bug in user auth")
    assert "[D1]" in enhanced


def test_fix_handles_common_issues():
    rough = "hi, can you just simply fix it?"
    fixed = prompt_engine.fix_prompt(rough)
    assert "hi," not in fixed.lower()
    assert "simply" not in fixed.lower()
    assert "just" not in fixed.lower() or "just" in fixed.lower() and "adjust" in fixed.lower()
    assert "Acceptance criteria" in fixed or "Verification" in fixed


def test_doctor_is_healthy():
    diag = prompt_engine.doctor()
    assert diag["score_works"] is True
    assert diag["enhance_works"] is True
    assert diag["fix_works"] is True
    assert diag["templates_count"] >= 20


def test_suggest_returns_templates():
    matches = prompt_engine.suggest("write tests for a function")
    assert isinstance(matches, dict)
    assert len(matches) > 0
    assert any("test" in k for k in matches)


@pytest.mark.parametrize(
    "prompt,expected_axis_min",
    [
        # Highly specific, contextual, actionable prompt should score well on specificity/actionability.
        (
            "Refactor src/auth.py line 42 to use bcrypt. Add unit tests in test_auth.py and verify all tests pass.",
            {"specificity": 6, "actionability": 6},
        ),
        # RIG-doctrine-rich prompt should score well on doctrine.
        (
            "[L7] Finalize the deployment. Acceptance criteria: tests pass, no regressions, ProofPacket signed.",
            {"doctrine": 7},
        ),
    ],
)
def test_sensible_scores_for_real_prompts(prompt, expected_axis_min):
    result = prompt_engine.score(prompt)
    for axis, minimum in expected_axis_min.items():
        assert result[axis] >= minimum, f"{axis} scored {result[axis]}, expected >= {minimum}"

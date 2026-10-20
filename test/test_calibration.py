"""Calibration tests: known prompts must keep their measured scores.

examples/calibration/ holds three prompts (weak, solid, strong) and the scores
the engine produced for them. If a scoring change moves any of these numbers,
the change is deliberate and expected.json is updated in the same commit.
"""

import json
from pathlib import Path

from rig_ai import score

CALIBRATION = Path(__file__).resolve().parent.parent / "examples" / "calibration"


def test_calibration_scores_match_expected() -> None:
    expected = json.loads((CALIBRATION / "expected.json").read_text(encoding="utf-8"))
    expected.pop("_about", None)
    assert set(expected) == {"weak.txt", "solid.txt", "strong.txt"}
    for name, want in expected.items():
        prompt = (CALIBRATION / name).read_text(encoding="utf-8")
        got = score(prompt)
        for key in ("specificity", "doctrine", "context", "actionability", "total", "grade"):
            assert got[key] == want[key], f"{name}: {key} moved ({want[key]} -> {got[key]})"


def test_calibration_ladder_orders_quality() -> None:
    expected = json.loads((CALIBRATION / "expected.json").read_text(encoding="utf-8"))
    expected.pop("_about", None)
    totals = [expected[n]["total"] for n in ("weak.txt", "solid.txt", "strong.txt")]
    assert totals[0] < totals[1] < totals[2]
    assert expected["strong.txt"]["grade"] == "A+"
    assert expected["weak.txt"]["grade"] == "F"


def test_scores_are_deterministic() -> None:
    prompt = (CALIBRATION / "solid.txt").read_text(encoding="utf-8")
    assert score(prompt) == score(prompt)

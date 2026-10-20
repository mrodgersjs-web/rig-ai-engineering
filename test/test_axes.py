"""Tests for the axis registry: the definitions behind every score."""

from rig_ai import prompt_engine
from rig_ai.axes import AXES, AXIS_BY_ID, GRADE_BANDS, grade_for, rubric_text


def test_registry_has_the_four_axes() -> None:
    assert [a.id for a in AXES] == ["specificity", "doctrine", "context", "actionability"]
    assert all(a.max_score == 10 for a in AXES)


def test_every_marker_exists_in_the_engine() -> None:
    marker_maps = {
        "specificity": prompt_engine.SPECIFICITY_MARKERS,
        "doctrine": prompt_engine.DOCTRINE_MARKERS,
        "context": prompt_engine.CONTEXT_MARKERS,
        "actionability": prompt_engine.ACTIONABILITY_MARKERS,
    }
    for axis in AXES:
        assert set(axis.markers) == set(marker_maps[axis.id]), axis.id


def test_grade_bands_match_the_engine() -> None:
    for total in range(0, 41):
        assert grade_for(total) == prompt_engine.PromptEngine._grade(total)


def test_grade_band_floors_are_descending() -> None:
    floors = [floor for floor, _, _ in GRADE_BANDS]
    assert floors == sorted(floors, reverse=True)
    assert floors[-1] == 0


def test_rubric_text_covers_every_axis() -> None:
    text = rubric_text()
    for axis in AXES:
        assert axis.name in text
        assert axis.question in text
    assert "Grade bands" in text
    assert AXIS_BY_ID["context"].id == "context"

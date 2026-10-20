"""Tests for the template library and suggestion matching."""

from rig_ai import prompt_engine
from rig_ai.prompt_engine import PromptEngine


def test_library_has_twenty_templates() -> None:
    templates = PromptEngine._load_templates()
    assert len(templates) == 20
    assert len(set(templates)) == 20
    assert all(t.strip() for t in templates.values())


def test_suggest_finds_the_obvious_template() -> None:
    matches = PromptEngine.suggest("write unit tests for the parser")
    assert "unit-test" in matches
    assert len(matches) <= 5


def test_suggest_with_no_overlap_is_empty() -> None:
    assert PromptEngine.suggest("") == {}


def test_doctor_is_healthy() -> None:
    checks = prompt_engine.doctor()
    assert checks["engine_module"] is True
    assert checks["templates_load"] is True
    assert checks["templates_count"] == 20
    assert checks["score_works"] is True
    assert checks["enhance_works"] is True
    assert checks["fix_works"] is True

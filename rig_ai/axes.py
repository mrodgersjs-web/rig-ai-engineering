"""Axis definitions for the 4-axis prompt rubric.

This registry is the single source of truth for what each axis measures, which
markers feed it, and how the 0-10 score is derived. The CLI (`rig-ai axes`),
the docs, and the tests all read from here.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class Axis:
    id: str
    name: str
    question: str
    markers: Tuple[str, ...]
    what_high_scores_mean: str
    what_low_scores_mean: str
    max_score: int = 10

    def to_dict(self) -> Dict[str, object]:
        return {
            "id": self.id,
            "name": self.name,
            "question": self.question,
            "markers": list(self.markers),
            "what_high_scores_mean": self.what_high_scores_mean,
            "what_low_scores_mean": self.what_low_scores_mean,
            "max_score": self.max_score,
        }


AXES: Tuple[Axis, ...] = (
    Axis(
        id="specificity",
        name="Specificity",
        question="How concrete and precise is the prompt?",
        markers=("numbers", "code_refs", "output_format", "verification", "constraints", "reasoning", "examples"),
        what_high_scores_mean="Names exact files, numbers, formats, constraints, or examples to aim at.",
        what_low_scores_mean="Could apply to any task; the agent has to guess the target.",
    ),
    Axis(
        id="doctrine",
        name="Doctrine",
        question="Does the prompt carry workflow structure and acceptance criteria?",
        markers=("rig_terms", "lattice", "acceptance", "scope", "verification_block"),
        what_high_scores_mean="States acceptance criteria, scope boundaries, and a stage coordinate (like D1 or L7).",
        what_low_scores_mean="No definition of done and no boundary on the work.",
    ),
    Axis(
        id="context",
        name="Context",
        question="Is the prompt grounded in real project state?",
        markers=("file_refs", "skill_refs", "prior_work", "project_meta", "data_refs"),
        what_high_scores_mean="References the files, skills, prior work, or data the answer must build on.",
        what_low_scores_mean="The agent must answer from nothing but the sentence itself.",
    ),
    Axis(
        id="actionability",
        name="Actionability",
        question="Is the next action obvious?",
        markers=("action_verbs", "sequence", "conditionals", "negatives", "directives"),
        what_high_scores_mean="Starts with a verb, sequences the steps, and says what to produce or verify.",
        what_low_scores_mean="Reads like a thought or a question, not a task.",
    ),
)

GRADE_BANDS: Tuple[Tuple[int, str, str], ...] = (
    (36, "A+", "Operator grade"),
    (32, "A", "Strong"),
    (28, "B", "Solid"),
    (22, "C", "Needs work"),
    (16, "D", "Weak"),
    (0, "F", "Rewrite required"),
)

AXIS_BY_ID: Dict[str, Axis] = {a.id: a for a in AXES}


def grade_for(total: int) -> str:
    """Return the grade letter for a total score out of 40."""
    for floor, grade, _label in GRADE_BANDS:
        if total >= floor:
            return grade
    return "F"


def rubric_text() -> str:
    """Render the rubric as plain text for the CLI."""
    lines = ["4-axis prompt rubric (each axis 0-10, total out of 40)", ""]
    for axis in AXES:
        lines.append(f"{axis.name} ({axis.id})")
        lines.append(f"  Measures: {axis.question}")
        lines.append(f"  Markers:  {', '.join(axis.markers)}")
        lines.append(f"  High:     {axis.what_high_scores_mean}")
        lines.append(f"  Low:      {axis.what_low_scores_mean}")
        lines.append("")
    lines.append("Grade bands")
    for floor, grade, label in GRADE_BANDS:
        lines.append(f"  {floor:>2}+ : {grade:<2} {label}")
    return "\n".join(lines)

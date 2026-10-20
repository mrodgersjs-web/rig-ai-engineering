"""Tests for the canned blocks enhance() appends: acceptance criteria and
context guidance, and the no-doubling rule for prompts that already carry them.
"""

from rig_ai import enhance


def test_enhance_appends_acceptance_block() -> None:
    out = enhance("fix the login bug in src/auth.py")
    assert "Acceptance criteria:" in out


def test_enhance_appends_context_block_for_thin_prompts() -> None:
    out = enhance("fix the bug")
    assert "Context to include:" in out


def test_enhance_does_not_double_existing_blocks() -> None:
    prompt = (
        "Fix the parser crash in src/parser.py.\n\nAcceptance criteria:\n- Covered.\n"
        "\nContext to include:\n- src/parser.py\n"
    )
    out = enhance(prompt)
    assert out.count("Acceptance criteria:") == 1
    assert out.count("Context to include:") == 1


def test_enhance_keeps_the_objective() -> None:
    out = enhance("add a --verbose flag to cli.py")
    assert "add a --verbose flag to cli.py" in out.lower()

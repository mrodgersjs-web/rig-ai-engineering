"""Tests for ACCEPTANCE_BLOCK and CONTEXT_BLOCK, the canned blocks that

enhance() appends to a thin prompt. They are module constants so they can be
tested and edited in one place. Asserted here: enhance() appends both blocks,
and a prompt that already carries them is not doubled up.
"""

from rig_ai import enhance
from rig_ai.prompt_engine import ACCEPTANCE_BLOCK, CONTEXT_BLOCK


def test_enhance_appends_acceptance_block() -> None:
    out = enhance("fix the login bug in src/auth.py")
    assert ACCEPTANCE_BLOCK.strip() in out


def test_enhance_appends_context_block_for_thin_prompts() -> None:
    out = enhance("fix the bug")
    assert CONTEXT_BLOCK.strip() in out


def test_enhance_does_not_double_existing_blocks() -> None:
    prompt = f"Fix the parser crash in src/parser.py.{ACCEPTANCE_BLOCK}{CONTEXT_BLOCK}"
    out = enhance(prompt)
    assert out.count("Acceptance criteria:") == 1
    assert out.count("Context to include:") == 1


def test_enhance_keeps_the_objective() -> None:
    out = enhance("add a --verbose flag to cli.py")
    assert "add a --verbose flag to cli.py" in out.lower()

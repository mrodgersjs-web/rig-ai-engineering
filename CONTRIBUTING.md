# Contributing

## Bar

1. Scores stay deterministic: same input, same output, no network calls.
2. `pytest -q --cov=rig_ai` passes and `ruff check .` is clean.
3. README claims must match runnable commands; `test/test_docs.py` enforces
   the quoted output.
4. Any scoring change updates `examples/calibration/expected.json` in the
   same commit and says why in the commit message.

## Flow

1. Fork or branch from `main`.
2. Add or adjust tests for the change.
3. Run `pytest -q --cov=rig_ai` and `ruff check .`.
4. Open a PR with: what changed, how verified, score impact.

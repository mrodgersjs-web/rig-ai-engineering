# Copilot instructions

## What this repo is

`rig-ai-engineering` is a prompt scoring and rewriting toolkit. The `rig_ai`
package scores a prompt on four axes (Specificity, Doctrine, Context,
Actionability) out of 40, rewrites weak prompts with acceptance criteria, and
suggests matching templates. The CLI is `rig-ai`.

## Layout

- `rig_ai/` - package: `axes.py` (the rubric), `prompt_engine.py` (scoring and
  rewriting), `templates.py`, `cli.py`.
- `test/` - pytest suite: axes, calibration scores, prompt engine, templates,
  CLI, docs claims, repo hygiene.
- `examples/calibration/` - `weak.txt`, `solid.txt`, `strong.txt` with
  `expected.json` pinning their scores; the suite fails if a score drifts.
- `docs/` - architecture, rubric notes, public boundary.
- `.github/workflows/` - `ci.yml` (lint, tests, a real score run) and
  `rig-lattice.yml`.

## Commands

Run from the repository root in a virtual environment:

```bash
pip install -e '.[dev]'    # installs pytest, pytest-cov, ruff
ruff check .               # lint
pytest -q                  # full test suite
pytest -q --cov=rig_ai
rig-ai score -f examples/calibration/strong.txt
bash scripts/smoke.sh      # smoke, when present
```

## Conventions

- Conventional commit messages: `feat:`, `fix:`, `test:`, `docs:`, `ci:`, `chore:`.
- Every behavior change lands with a test that exercises it and passes on a clean install.
- A rubric change means updating `examples/calibration/expected.json` from an
  actual `rig-ai score` run and explaining the new score in the commit, never
  editing the expected numbers to fit the code.
- No secrets, credentials, client PII or private monorepo content in any tracked
  file. No machine paths such as `/Users/...` or `~/Developer/...`.

## Truth rule

Any number in docs, comments, or commit messages must come from a command run in
this repository, for example a score printed by `rig-ai score -f
examples/calibration/strong.txt` or a test count from `pytest -q`. Quote the
command and its output rather than a memory of it.

# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.2.1] - 2026-10-19

### Added

- `.github/CODEOWNERS` assigning `*` to `@mrodgersjs-web`.
- `.github/copilot-instructions.md` (2037 bytes): what the repository is, the
  layout, the exact commands (`pip install -e '.[dev]'`, `ruff check .`,
  `pytest -q`, `pytest -q --cov=rig_ai`, `rig-ai score -f
  examples/calibration/strong.txt`), conventions (conventional commits, a test for
  every change, calibration numbers only from a real score run, no secrets, no
  machine paths) and the truth rule that every number in docs comes from a command
  run in this repository.
- `test/test_repo_hygiene.py`: 4 checks read from the files on disk that
  `.github/CODEOWNERS` assigns `*` to `@mrodgersjs-web`, that
  `.github/copilot-instructions.md` is non-empty, at most 8000 bytes and names a
  test command, that `README.md` carries a `github/actions/workflow/status` badge,
  the "Built by Mike Rodgers - rodgersintelligence.com" footer, a test command and
  only clones `mrodgersjs-web/rig-ai-engineering`, and that every job under
  `.github/workflows/` sets `timeout-minutes` and never sets `continue-on-error: true`.

### Changed

- `.github/workflows/ci.yml` and `.github/workflows/rig-lattice.yml`:
  `timeout-minutes: 15` on every job.
- `README.md`: footer is the plain literal "Built by Mike Rodgers -
  rodgersintelligence.com".

### Verified

- Fresh venv `python3.12 -m venv`, `pip install -e '.[dev]'`, `ruff check .` clean,
  `pytest -q --cov=rig_ai` 44 passed with 90 percent coverage, and
  `rig-ai score -f examples/calibration/strong.txt` prints "RIG Prompt Score:
  38/40 (A+)", the figure the README quotes.

## [0.2.0] - 2026-10-19

### Added
- `rig_ai/axes.py`: the axis registry (definitions, markers, grade bands) as
  the single source of truth for the rubric, with `rig-ai axes` to print it
  and `rig-ai axes --json` for machines.
- Calibration set in `examples/calibration/`: weak, solid and strong prompts
  with the scores the engine produced, pinned by tests so rubric changes are
  deliberate.
- Test suites for the axis registry, the CLI, the template library and the
  calibration set (8 tests to 34).
- docs/axes.md rubric reference.
- Community files: code of conduct, security policy, contributing guide,
  issue templates, pull request template, Dependabot config.

### Fixed
- `suggest("")` returned unrelated templates; an empty query now returns none.

### Changed
- Package metadata: version 0.2.0, dev extras now include pytest-cov and
  ruff, typed package marker (`py.typed`), ruff configuration.
- README rewritten with real command output; the previous example score was
  not reproducible and has been replaced with measured numbers.
- CI runs ruff and pytest with coverage across Python 3.10 to 3.13.

## [0.1.0] - 2026-09-12

### Added
- 4-axis deterministic prompt scorer, enhancer, fixer, template suggestion,
  doctor command, and the 20-template library.

# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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

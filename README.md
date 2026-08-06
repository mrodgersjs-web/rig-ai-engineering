# RIG AI Engineering — Prompt Intelligence Engine

Local-first prompt engineering for AI agents and LLM workflows. **Score, enhance, and fix prompts deterministically** before they ship to any model — no network or LLM required.

This package packages the RIG Prompt Intelligence Engine as a public, installable Python library. It is the same scoring rubric used to harden prompts across the RIG fleet (Jake, Hermes, Codex, Claude Code).

## The 4-axis scoring rubric

Every prompt is scored 0–10 on four axes, for a total out of 40.

| Axis | What it measures | High-signal markers |
|---|---|---|
| **Specificity** | Concreteness and precision | numbers, file paths, output format, constraints, examples, verification |
| **Doctrine** | RIG / agentic structure | lattice coordinates (`D1`, `L7`, etc.), acceptance criteria, scope, verification, success criteria |
| **Context** | Grounding in real project state | file references, skill loads, prior work, project/repo terms |
| **Actionability** | Clarity of next action | action verbs, sequenced steps, conditions, directives, negatives |

Total scores map to grades:

- `36–40` → A+ (Operator Grade)
- `32–35` → A
- `28–31` → B
- `22–27` → C
- `16–21` → D
- `0–15`  → F (Rewrite Required)

## Install

```bash
pip install rig-ai-engineering
```

Or from source:

```bash
git clone https://github.com/mrodgersjs-web/rig-ai-engineering.git
cd rig-ai-engineering
pip install -e ".[dev]"
```

## CLI usage

The package installs a `rig-ai` command.

### `score`

```bash
rig-ai score -p "Write a Python function that returns the sum of two integers."
```

Output:

```text
RIG Prompt Score: 18/40 (C)

  Specificity     5/10 — Moderate specificity (numbers, output_format). Add file paths, line numbers, or exact output format.
  Doctrine        3/10 — Add RIG doctrine: success criteria, scope boundaries, verification steps, or a lattice coordinate (e.g., D1, L7).
  Context         3/10 — Missing context. Reference files (#file:), skills, prior work, or project state so the agent can ground its answer.
  Actionability   7/10 — Some actionability (action_verbs). Add explicit first step or success condition.
```

Use `--json` for machine-readable output:

```bash
rig-ai score -p "Refactor auth.py to use bcrypt" --json
```

### `enhance`

```bash
rig-ai enhance -p "fix the bug"
```

Returns a restructured prompt with a lattice coordinate, acceptance criteria, context guidance, and verification.

### `fix`

```bash
rig-ai fix -p "hi, can you just simply fix it?"
```

Strips conversational openers, filler adverbs, and vague pronouns, then runs the enhanced structure.

### `doctor`

```bash
rig-ai doctor
```

Health check for the engine, templates, and core functions.

### `suggest`

```bash
rig-ai suggest "write unit tests"
```

Returns the top 5 matching prompt templates from the built-in library.

## Programmatic usage

```python
from rig_ai import score, enhance, fix_prompt

result = score("Refactor src/auth.py to use bcrypt.")
print(result["total"])  # 18
print(result["grade"])  # C

better = enhance("fix the bug")
fixed = fix_prompt("hi, can you just simply fix it?")
```

## Template library

`rig_ai/templates.py` contains 20 reusable templates keyed by task type:

- `code-review`, `unit-test`, `refactor`, `debug`
- `feature-design`, `api-design`, `doc-update`
- `performance-audit`, `security-review`, `dependency-upgrade`
- `data-pipeline`, `prompt-optimize`, `onboarding`
- `incident-response`, `release-notes`, `competitor-analysis`
- `user-story`, `migration-plan`, `cli-tool`, `schema-design`

## Determinism guarantee

The core engine uses only regex heuristics, string length, and word counts. It does not call any model, API, or external service. Scores are fully reproducible for the same input.

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT © Mike Rodgers

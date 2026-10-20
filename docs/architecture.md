# Architecture

## One-liner

A prompt goes in, four axis scores and a grade come out, and weak prompts come
back rewritten. Everything is local string work.

## Flow

```text
prompt -> marker scan (4 axes) -> 0-10 per axis -> total / 40 -> grade
prompt -> enhance/fix rewrite -> prompt with criteria and verification
```

1. `rig_ai/prompt_engine.py` scans each axis's marker regexes
   (case-insensitive), maps hits to a base score with diminishing returns,
   applies the length adjustment, and sums the four axes.
2. `rig_ai/axes.py` defines what each axis means, its markers, and the grade
   bands. `rig-ai axes` prints it; `test/test_axes.py` keeps the registry, the
   engine and the docs in agreement.
3. `enhance()` strips conversational openers, adds a stage coordinate, the
   canned acceptance and context blocks (module constants), and a verification
   prompt when none is present. `fix_prompt()` first repairs filler, vague
   pronouns and ellipses, then runs `enhance()`.
4. `suggest()` matches a query against the 20-template library by word
   overlap and key matching. `doctor()` runs the engine end to end.

## Design notes

- Scoring is deterministic: the same prompt always gets the same score. There
  is no model call and no network access anywhere in the package.
- Scores are integers 0-10 by construction; `_axis_score` clamps.
- The calibration set in `examples/calibration/` is the regression guard:
  weak, solid and strong prompts with pinned scores, asserted by
  `test/test_calibration.py`. A rubric change must move `expected.json` in the
  same commit.
- `mcp/server.py` exposes the engine over MCP for agent harnesses; it wraps
  the same functions the CLI uses.

## Trust boundaries

- Prompts are read from arguments, files or stdin and never leave the process.
- No secrets enter prompts or config; nothing is logged anywhere.

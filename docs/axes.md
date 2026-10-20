# The 4-axis rubric

Every prompt scores 0-10 on four axes, 40 points total. The registry in
`rig_ai/axes.py` is the source of truth; `rig-ai axes` prints it, and
`test/test_axes.py` checks that the docs, the registry and the engine agree.

## Axis definitions

### Specificity

Measures: how concrete and precise is the prompt?

Markers scanned (each hit adds to the score, with diminishing returns):
`numbers`, `code_refs`, `output_format`, `verification`, `constraints`,
`reasoning`, `examples`.

High score: names exact files, numbers, formats, constraints or examples.
Low score: could apply to any task; the agent has to guess the target.

### Doctrine

Measures: does the prompt carry workflow structure and acceptance criteria?

Markers: `rig_terms`, `lattice` (stage coordinates like D1 or L7),
`acceptance`, `scope`, `verification_block`.

High score: states acceptance criteria, scope boundaries, and a stage
coordinate. Low score: no definition of done, no boundary on the work.

### Context

Measures: is the prompt grounded in real project state?

Markers: `file_refs`, `skill_refs`, `prior_work`, `project_meta`, `data_refs`.

High score: references the files, skills, prior work or data the answer must
build on. Low score: the agent answers from nothing but the sentence itself.

### Actionability

Measures: is the next action obvious?

Markers: `action_verbs` (distinct verbs count up to 3), `sequence`,
`conditionals`, `negatives`, `directives`.

High score: starts with a verb, sequences the steps, says what to produce or
verify. Low score: reads like a thought or a question, not a task.

## How a score is computed

1. Each axis scans its marker patterns (case-insensitive regex) over the text.
2. Hits map to a base score: 1 hit = 3 points, 2 = 6, 3 = 8, 4 = 9, 5+ = 10,
   then a length adjustment of up to +2 for prompts over 20 words.
3. Prompts under 8 words lose 2 points on Specificity, Context and
   Actionability. Prompts over 60 words with 0-1 hits on an axis lose 2 there.
4. The four axis scores sum to the total.

## Grade bands

| Total | Grade | Label |
| --- | --- | --- |
| 36-40 | A+ | Operator grade |
| 32-35 | A | Strong |
| 28-31 | B | Solid |
| 22-27 | C | Needs work |
| 16-21 | D | Weak |
| 0-15 | F | Rewrite required |

## Calibration

`examples/calibration/` holds three prompts with the scores the engine
produced: weak.txt (2, F), solid.txt (18, D), strong.txt (38, A+).
`expected.json` pins those numbers and `test/test_calibration.py` fails if a
scoring change moves them, so any change to the rubric is deliberate and
visible in the diff.

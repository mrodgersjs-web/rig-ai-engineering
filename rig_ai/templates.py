"""20 reusable prompt templates indexed by task type."""

TEMPLATES = {
    "code-review": """
You are a senior engineer. Review the code in #file:{file} for correctness, performance, and maintainability.

Focus areas:
- {focus_areas}

Acceptance criteria:
- Each finding includes a line reference.
- Critical bugs are flagged first.
- Suggest concrete refactors, not just observations.
""".strip(),

    "unit-test": """
Write unit tests for {target} using {framework}.

Requirements:
- Cover the happy path, edge cases, and expected failures.
- Use descriptive test names.
- Keep tests deterministic and isolated.

Acceptance criteria:
- {acceptance}
""".strip(),

    "refactor": """
Refactor {target} to improve {goal} without changing external behavior.

Constraints:
- Preserve all existing tests and behavior.
- Limit scope to {scope}.

Acceptance criteria:
- Tests still pass.
- Code is measurably simpler or faster.
- No regressions introduced.
""".strip(),

    "debug": """
[D1] Debug the failure in {target}.

Observed behavior:
- {observed}

Expected behavior:
- {expected}

Context:
- #file:{file}
- Recent changes: {changes}

Acceptance criteria:
- Root cause identified with evidence.
- Fix implemented and verified.
- Regression test added if appropriate.
""".strip(),

    "feature-design": """
Design a feature for {product} that lets users {capability}.

Constraints:
- {constraints}

Out of scope:
- {out_of_scope}

Acceptance criteria:
- Data model and API surface defined.
- Security and error handling considered.
- Implementation broken into vertical slices.
""".strip(),

    "api-design": """
Design an HTTP API endpoint for {resource}.

Requirements:
- Support {operations}.
- Return consistent error responses.

Acceptance criteria:
- OpenAPI spec included.
- Idempotency and validation rules specified.
- Example requests and responses provided.
""".strip(),

    "doc-update": """
Update the documentation for {topic} so a new teammate can understand it in under {minutes} minutes.

Sections to include:
- What it is.
- When to use it.
- How to run / integrate it.
- Common pitfalls.

Acceptance criteria:
- Accurate and complete against the current code.
- Uses examples where helpful.
""".strip(),

    "performance-audit": """
Audit the performance of {target}.

Context:
- #file:{file}
- Current latency / throughput: {baseline}
- Target latency / throughput: {target_metric}

Acceptance criteria:
- Bottlenecks identified with measurements.
- Prioritized recommendations.
- Safe changes separated from risky changes.
""".strip(),

    "security-review": """
Review {target} for security issues relevant to {threat_model}.

Scope:
- {scope}

Acceptance criteria:
- Each risk rated by severity and likelihood.
- Concrete mitigations proposed.
- No false positives without explanation.
""".strip(),

    "dependency-upgrade": """
Upgrade {package} from {old_version} to {new_version}.

Steps:
1. Read the changelog and migration guide.
2. Apply the upgrade in a branch.
3. Run the test suite.
4. Fix deprecations and breaking changes.

Acceptance criteria:
- All tests pass.
- No new warnings.
- CHANGELOG updated.
""".strip(),

    "data-pipeline": """
Build a data pipeline that ingests {source} and produces {destination}.

Requirements:
- Schema mapping: {schema}
- Failure handling: {failure_mode}
- Scheduling: {schedule}

Acceptance criteria:
- Idempotent runs.
- Observability and alerting in place.
- Backfill strategy documented.
""".strip(),

    "prompt-optimize": """
Optimize the following prompt for clarity and actionability.

Original prompt:
---
{original_prompt}
---

Return:
1. A score out of 40 across four axes (specificity, doctrine, context, actionability).
2. The improved prompt.
3. A short rationale for the changes.
""".strip(),

    "onboarding": """
Create an onboarding guide for a {role} joining {team}.

Sections:
- Day-one checklist.
- Key repositories and tools.
- First-week goals.
- Who to ask for help.

Acceptance criteria:
- New hire can complete day-one setup without asking questions.
- Links and contacts are current.
""".strip(),

    "incident-response": """
We have an active incident: {summary}.

Impact:
- {impact}

Symptoms:
- {symptoms}

Runbook:
- #file:{runbook}

Acceptance criteria:
- Mitigation steps listed in priority order.
- Communication draft for stakeholders.
- Post-incident action items captured.
""".strip(),

    "release-notes": """
Write release notes for version {version} of {project}.

Included changes:
- {changes}

Audience:
- {audience}

Acceptance criteria:
- Clear summary of user-facing changes.
- Breaking changes called out explicitly.
- Migration steps provided if needed.
""".strip(),

    "competitor-analysis": """
Analyze {competitor} as a competitor to {product}.

Dimensions:
- Positioning and messaging.
- Pricing and packaging.
- Strengths and weaknesses.
- Threat level and differentiation opportunities.

Acceptance criteria:
- Evidence-based claims.
- Actionable recommendations for {product}.
""".strip(),

    "user-story": """
Write a user story and acceptance criteria for: {feature}.

As a {persona}, I want {desire} so that {benefit}.

Acceptance criteria:
- {criteria_1}
- {criteria_2}
- {criteria_3}

Out of scope:
- {out_of_scope}
""".strip(),

    "migration-plan": """
Plan the migration from {source_system} to {target_system}.

Constraints:
- Downtime budget: {downtime}
- Rollback window: {rollback}

Acceptance criteria:
- Pre-migration, migration, and rollback steps.
- Validation checklist after cutover.
- Communication plan for stakeholders.
""".strip(),

    "cli-tool": """
Design a CLI command for {tool} that {action}.

Requirements:
- Input: {input}
- Output: {output}
- Error handling: {errors}

Acceptance criteria:
- Help text and examples included.
- Exit codes documented.
- Tests cover normal and error paths.
""".strip(),

    "schema-design": """
Design a database schema for {domain}.

Requirements:
- Support {queries}.
- Enforce {constraints}.

Acceptance criteria:
- Tables, columns, types, and indexes specified.
- Relationships and constraints documented.
- Migration script provided.
""".strip(),
}

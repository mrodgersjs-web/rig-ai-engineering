"""Deterministic prompt intelligence engine.

Scores prompts on a 4-axis rubric, enhances them, and fixes common issues.
No LLM or network access is required.
"""

import re
from dataclasses import dataclass
from typing import Optional


# Markers of high-quality prompts — tuned to reward concrete, actionable, contextualized prompts.
SPECIFICITY_MARKERS = {
    "numbers": r"\b\d+(?:\.\d+)?\b",
    "code_refs": r"\b(file|path|line|function|class|module|method|variable|snippet)\b",
    "output_format": r"\b(format|output|return|respond|produce|json|markdown|table|list)\b",
    "verification": r"\b(test|verify|validate|check|assert|confirm|ensure)\b",
    "constraints": r"\b(constraint|limit|maximum|minimum|within|bound|threshold|scope)\b",
    "reasoning": r"\b(because|since|due to|reason|cause|rationale|explain)\b",
    "examples": r"\b(example|for instance|such as|e\.g\.|i\.e\.)\b",
}

DOCTRINE_MARKERS = {
    "rig_terms": r"\b(IQRSQPI|ProofPacket|BMS|RIG|ISA|done-test|gate)\b",
    "lattice": r"\b(A[1-4]|D[1-3]|L[1-7])\b",
    "acceptance": r"\b(acceptance criteria|success criteria|definition of done|done-test)\b",
    "scope": r"\b(scope|boundary|out of scope|in scope|constraint)\b",
    "verification_block": r"\b(verify|verification|regression|test strategy|evidence)\b",
}

CONTEXT_MARKERS = {
    "file_refs": r"(#file:|@file:|/[^\s]*\.[a-z]+|\b\w+\.py\b|\b\w+\.(js|ts|tsx|jsx|md|json|yaml|toml)\b)",
    "skill_refs": r"\b(skill|skill_view|memory|session|context|knowledge)\b",
    "prior_work": r"\b(previous|earlier|last time|from session|building on|as we did|continuing)\b",
    "project_meta": r"\b(project|repo|repository|codebase|workspace|branch|commit|module)\b",
    "data_refs": r"\b(schema|table|column|field|record|dataset|document)\b",
}

ACTIONABILITY_MARKERS = {
    "action_verbs": r"\b(write|create|build|implement|refactor|fix|debug|optimize|add|remove|update|generate|produce|analyze|compare|evaluate|run|execute|ship|deploy|test|verify)\b",
    "sequence": r"\b(step|first|then|next|finally|after|before|once)\b",
    "conditionals": r"\b(if|when|unless|while|given|in case)\b",
    "negatives": r"\b(do not|don't|never|avoid|must not|should not)\b",
    "directives": r"^(?:You |Please |I need|I want|Can you|Write|Build|Implement|Fix|Refactor|Analyze|Compare)",
}

COMMON_ISSUES = [
    (r"^(hi|hello|hey|please|can you|could you)\b", "Remove the conversational opener. Start with the objective."),
    (r"\b(make it|do it|fix it|handle it)\b", "Replace vague pronouns with the specific thing to act on."),
    (r"\b(better|good|nice|clean|proper|correct)\b", "Replace subjective adjectives with measurable criteria."),
    (r"\b(just|simply|only|basically|obviously|clearly)\b", "Remove filler adverbs that add no signal."),
    (r"\.{3,}", "Replace trailing ellipses with a concrete question or directive."),
    (r"\?\s*$", "If this is a task, rephrase the question as a directive with acceptance criteria."),
]


@dataclass(frozen=True)
class ScoreResult:
    specificity: int
    doctrine: int
    context: int
    actionability: int
    total: int
    feedback: dict[str, str]
    grade: str

    def to_dict(self) -> dict:
        return {
            "specificity": self.specificity,
            "doctrine": self.doctrine,
            "context": self.context,
            "actionability": self.actionability,
            "total": self.total,
            "feedback": self.feedback,
            "grade": self.grade,
        }


class PromptEngine:
    """Deterministic prompt intelligence."""

    _TEMPLATES: Optional[dict[str, str]] = None

    @classmethod
    def _load_templates(cls) -> dict[str, str]:
        if cls._TEMPLATES is None:
            from . import templates

            cls._TEMPLATES = templates.TEMPLATES
        return cls._TEMPLATES

    # ── Scoring ──────────────────────────────────────────────────────────

    @staticmethod
    def _count_hits(text: str, markers: dict[str, str]) -> tuple[int, list[str]]:
        lower = text.lower()
        hits = 0
        found = []
        for name, pattern in markers.items():
            matches = re.findall(pattern, lower, re.IGNORECASE)
            if matches:
                # For action verbs, count distinct matches as stronger signal.
                if name == "action_verbs":
                    distinct = len(set(m.lower() for m in matches))
                    hits += min(3, distinct)
                else:
                    hits += 1
                found.append(name)
        return hits, found

    @classmethod
    def score(cls, prompt: str) -> ScoreResult:
        if not isinstance(prompt, str):
            raise TypeError("prompt must be a string")
        text = prompt.strip()
        if not text:
            return ScoreResult(
                specificity=0,
                doctrine=0,
                context=0,
                actionability=0,
                total=0,
                feedback={k: "Empty prompt." for k in ("specificity", "doctrine", "context", "actionability")},
                grade="F",
            )

        wc = len(text.split())
        length_bonus = min(2, max(-2, (wc - 20) // 20))  # small length normalization

        spec_hits, spec_found = cls._count_hits(text, SPECIFICITY_MARKERS)
        doc_hits, doc_found = cls._count_hits(text, DOCTRINE_MARKERS)
        ctx_hits, ctx_found = cls._count_hits(text, CONTEXT_MARKERS)
        act_hits, act_found = cls._count_hits(text, ACTIONABILITY_MARKERS)

        specificity = cls._axis_score(spec_hits, wc, length_bonus, spec_found)
        doctrine = cls._axis_score(doc_hits, wc, length_bonus, doc_found)
        context = cls._axis_score(ctx_hits, wc, length_bonus, ctx_found)
        actionability = cls._axis_score(act_hits, wc, length_bonus, act_found)

        # Penalize very short prompts on every axis.
        if wc < 8:
            specificity = max(0, specificity - 2)
            context = max(0, context - 2)
            actionability = max(0, actionability - 2)

        feedback = {
            "specificity": cls._specificity_feedback(specificity, spec_found, wc),
            "doctrine": cls._doctrine_feedback(doctrine, doc_found),
            "context": cls._context_feedback(context, ctx_found),
            "actionability": cls._actionability_feedback(actionability, act_found),
        }

        total = specificity + doctrine + context + actionability
        grade = cls._grade(total)
        return ScoreResult(
            specificity=specificity,
            doctrine=doctrine,
            context=context,
            actionability=actionability,
            total=total,
            feedback=feedback,
            grade=grade,
        )

    @staticmethod
    def _axis_score(hits: int, wc: int, length_bonus: int, found: list[str]) -> int:
        # Base score from marker hits, with diminishing returns.
        base = 0
        if hits >= 1:
            base += 3
        if hits >= 2:
            base += 3
        if hits >= 3:
            base += 2
        if hits >= 4:
            base += 1
        if hits >= 5:
            base += 1
        score = base + length_bonus
        # Penalize if the prompt is very long but sparse on this axis.
        if wc > 60 and hits <= 1:
            score -= 2
        return max(0, min(10, score))

    @staticmethod
    def _grade(total: int) -> str:
        if total >= 36:
            return "A+"
        if total >= 32:
            return "A"
        if total >= 28:
            return "B"
        if total >= 22:
            return "C"
        if total >= 16:
            return "D"
        return "F"

    @staticmethod
    def _specificity_feedback(score: int, found: list[str], wc: int) -> str:
        if score >= 8:
            return f"Strong specificity ({', '.join(found)}). Add numbers or exact constraints if any are still missing."
        if score >= 5:
            return f"Moderate specificity ({', '.join(found or ['some detail'])}). Add file paths, line numbers, or exact output format."
        return "Too vague. Add concrete references: file paths, data ranges, output schema, or acceptance criteria." if wc > 5 else "Too short to be specific. Expand with what, where, and in what format."

    @staticmethod
    def _doctrine_feedback(score: int, found: list[str]) -> str:
        if score >= 8:
            return f"Well aligned with RIG doctrine ({', '.join(found)})."
        if score >= 5:
            return f"Some RIG structure ({', '.join(found or ['scope/verification'])}). Add acceptance criteria or a lattice coordinate."
        return "Add RIG doctrine: success criteria, scope boundaries, verification steps, or a lattice coordinate (e.g., D1, L7)."

    @staticmethod
    def _context_feedback(score: int, found: list[str]) -> str:
        if score >= 8:
            return f"Well contextualized ({', '.join(found)})."
        if score >= 5:
            return f"Some context ({', '.join(found or ['project references'])}). Add file or skill references if relevant."
        return "Missing context. Reference files (#file:), skills, prior work, or project state so the agent can ground its answer."

    @staticmethod
    def _actionability_feedback(score: int, found: list[str]) -> str:
        if score >= 8:
            return f"Highly actionable ({', '.join(found)})."
        if score >= 5:
            return f"Some actionability ({', '.join(found or ['action verbs'])}). Add explicit first step or success condition."
        return "Weak actionability. Start with a verb and state exactly what must be produced or verified."

    # ── Enhancement ──────────────────────────────────────────────────────

    @classmethod
    def enhance(cls, prompt: str) -> str:
        """Return an improved version of the prompt using deterministic rewrites."""
        if not isinstance(prompt, str):
            raise TypeError("prompt must be a string")
        original = prompt.strip()
        if not original:
            return "[Empty prompt — describe the objective, constraints, and expected output.]"

        result = cls.score(original)
        out = original

        # Strip low-signal openers.
        out = re.sub(r"^(hi|hello|hey|please|can you|could you)[,\s]*", "", out, flags=re.IGNORECASE).strip()
        out = re.sub(r"^(i need|i want|would you|will you)\s+(you\s+)?(to\s+)?", "", out, flags=re.IGNORECASE).strip()
        # Remove stray leading punctuation left by stripping.
        out = re.sub(r"^[\s,]+", "", out)
        # Capitalize first word.
        if out:
            out = out[0].upper() + out[1:]

        # Add a lattice coordinate if none present and the prompt looks like a task.
        if result.doctrine < 6 and not re.search(r"\b(A[1-4]|D[1-3]|L[1-7])\b", original):
            lattice = cls._suggest_lattice(original)
            if lattice:
                out = f"[{lattice}] {out}"

        # Add acceptance criteria if missing.
        if "acceptance criteria" not in out.lower():
            out += "\n\nAcceptance criteria:\n- Output meets the specified format.\n- Edge cases are handled.\n- Result is verified before declaring complete."

        # Add context guidance if missing.
        if result.context < 5 and not re.search(r"(#file:|@file:|/[^\s]+\.[a-z]+)", out, re.IGNORECASE):
            out += "\n\nContext to include:\n- Relevant file paths or code snippets.\n- Any skills, prior session, or project state the agent should load."

        # Add verification if missing.
        if not re.search(r"\b(verify|validate|check|test|ensure)\b", out, re.IGNORECASE):
            out += "\n\nVerification:\n- How will you confirm this works?\n- What are the edge cases or failure modes?"

        # Fix trailing question on task prompts.
        if out.endswith("?"):
            out = out[:-1].strip() + "."

        return out.strip()

    @staticmethod
    def _suggest_lattice(prompt: str) -> Optional[str]:
        p = prompt.lower()
        if any(w in p for w in ["fix", "bug", "error", "crash", "broken"]):
            return "D1"
        if any(w in p for w in ["deploy", "release", "ship", "launch"]):
            return "L5"
        if any(w in p for w in ["research", "investigate", "explore", "analyze"]):
            return "L2"
        if any(w in p for w in ["review", "audit", "check", "inspect"]):
            return "L1"
        if any(w in p for w in ["connect", "integrate", "bridge", "link"]):
            return "L3"
        if any(w in p for w in ["iterate", "improve", "optimize", "refactor"]):
            return "L6"
        if any(w in p for w in ["finalize", "complete", "close", "lock", "done"]):
            return "L7"
        if any(w in p for w in ["delegate", "assign", "route"]):
            return "D2"
        return "A1"

    # ── Fixing ───────────────────────────────────────────────────────────

    @classmethod
    def fix_prompt(cls, prompt: str) -> str:
        """Fix common prompt issues and return a cleaned version."""
        if not isinstance(prompt, str):
            raise TypeError("prompt must be a string")
        text = prompt.strip()
        if not text:
            return cls.enhance("")

        issues = []
        cleaned = text

        # Strip conversational openers and softeners repeatedly until stable.
        prev = None
        while prev != cleaned:
            prev = cleaned
            cleaned = re.sub(
                r"^(hi|hello|hey|please|can you|could you|would you|will you|do you|i need|i want)[,\s]*",
                "",
                cleaned,
                flags=re.IGNORECASE,
            ).strip()
            cleaned = re.sub(r"^[,\s]+", "", cleaned)
        if prev and prev != text:
            issues.append("Removed conversational opener")

        # Remove filler adverbs.
        original_cleaned = cleaned
        cleaned = re.sub(r"\b(just|simply|only|basically|obviously|clearly)\b", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
        if cleaned != original_cleaned:
            issues.append("Removed filler adverbs")

        # Replace vague pronouns.
        if re.search(r"\b(make it|do it|fix it|handle it)\b", cleaned, re.IGNORECASE):
            issues.append("Replaced vague pronouns with the specific target")
            cleaned = re.sub(r"\b(it)\b", "the target", cleaned, flags=re.IGNORECASE)

        # Normalize ellipses.
        if re.search(r"\.{3,}", cleaned):
            issues.append("Replaced trailing ellipses with a directive")
            cleaned = re.sub(r"\.{3,}", ".", cleaned)

        # Capitalize and punctuate.
        if cleaned:
            cleaned = cleaned[0].upper() + cleaned[1:]
            if cleaned.endswith("?"):
                issues.append("Rephrased question as a directive")
                cleaned = cleaned[:-1].strip() + "."

        # Run through enhance to ensure structure.
        enhanced = cls.enhance(cleaned)

        # If we detected issues, prepend a concise note.
        if issues:
            note = "Fixed: " + "; ".join(issues) + "."
            enhanced = f"{note}\n\n{enhanced}"

        return enhanced

    # ── Suggest templates ────────────────────────────────────────────────

    @classmethod
    def suggest(cls, query: str) -> dict[str, str]:
        """Return the top templates matching the query."""
        templates = cls._load_templates()
        query_lower = query.lower()
        query_words = set(re.findall(r"\b\w+\b", query_lower))
        # Add simple stems so "tests" matches "test".
        stems = {w[:-1] for w in query_words if len(w) > 3 and w.endswith("s")}
        query_words |= stems
        scored = []
        for key, tmpl in templates.items():
            key_lower = key.lower()
            tmpl_lower = tmpl.lower()
            tmpl_words = set(re.findall(r"\b\w+\b", tmpl_lower))
            overlap = len(query_words & tmpl_words)
            key_match = sum(1 for w in query_words if w in key_lower or key_lower in w)
            title_match = 5 if any(w in key_lower for w in ("test", "debug", "refactor", "review", "design", "doc", "feature", "api", "security", "performance", "migration")) and query_lower in key_lower else 0
            score = overlap * 2 + key_match * 3 + title_match
            if score > 0:
                scored.append((score, key, tmpl))
        scored.sort(reverse=True)
        return {key: tmpl for _, key, tmpl in scored[:5]}

    @classmethod
    def doctor(cls) -> dict[str, bool | str]:
        """Return health diagnostics for the package."""
        checks = {
            "engine_module": False,
            "templates_load": False,
            "templates_count": 0,
            "score_works": False,
            "enhance_works": False,
            "fix_works": False,
        }
        try:
            cls.score("Write a Python function that returns the sum of two integers.")
            checks["engine_module"] = True
            checks["score_works"] = True
        except Exception as exc:
            checks["score_error"] = str(exc)

        try:
            templates = cls._load_templates()
            checks["templates_load"] = True
            checks["templates_count"] = len(templates)
        except Exception as exc:
            checks["templates_error"] = str(exc)

        try:
            cls.enhance("fix the bug")
            checks["enhance_works"] = True
        except Exception as exc:
            checks["enhance_error"] = str(exc)

        try:
            cls.fix_prompt("hi, can you just fix it?")
            checks["fix_works"] = True
        except Exception as exc:
            checks["fix_error"] = str(exc)

        return checks


# Module-level convenience functions.

def score(prompt: str) -> dict:
    """Score a prompt on the 4-axis rubric."""
    return PromptEngine.score(prompt).to_dict()


def enhance(prompt: str) -> str:
    """Return an enhanced prompt."""
    return PromptEngine.enhance(prompt)


def fix_prompt(prompt: str) -> str:
    """Return a fixed prompt."""
    return PromptEngine.fix_prompt(prompt)


def suggest(query: str) -> dict[str, str]:
    """Return matching prompt templates."""
    return PromptEngine.suggest(query)


def doctor() -> dict[str, bool | str]:
    """Run package health diagnostics."""
    return PromptEngine.doctor()

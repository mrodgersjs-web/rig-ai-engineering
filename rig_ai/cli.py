"""Command-line interface for the RIG Prompt Intelligence Engine."""

import argparse
import json
import sys
from pathlib import Path

from . import prompt_engine


def _read_input(args) -> str:
    if args.prompt:
        return args.prompt
    if args.file:
        return Path(args.file).read_text()
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    return ""


def cmd_score(args) -> int:
    text = _read_input(args)
    if not text:
        print("Error: no prompt provided (use --prompt, --file, or pipe).", file=sys.stderr)
        return 1
    result = prompt_engine.score(text)
    if args.json:
        print(json.dumps(result, indent=2))
        return 0
    print(f"RIG Prompt Score: {result['total']}/40 ({result['grade']})")
    print()
    for axis in ("specificity", "doctrine", "context", "actionability"):
        print(f"  {axis.capitalize():14} {result[axis]:2}/10 — {result['feedback'][axis]}")
    return 0


def cmd_enhance(args) -> int:
    text = _read_input(args)
    if not text:
        print("Error: no prompt provided.", file=sys.stderr)
        return 1
    enhanced = prompt_engine.enhance(text)
    if args.json:
        print(json.dumps({"original": text, "enhanced": enhanced}, indent=2))
        return 0
    print(enhanced)
    return 0


def cmd_fix(args) -> int:
    text = _read_input(args)
    if not text:
        print("Error: no prompt provided.", file=sys.stderr)
        return 1
    fixed = prompt_engine.fix_prompt(text)
    if args.json:
        print(json.dumps({"original": text, "fixed": fixed}, indent=2))
        return 0
    print(fixed)
    return 0


def cmd_doctor(_args) -> int:
    result = prompt_engine.doctor()
    if _args and _args.json:
        print(json.dumps(result, indent=2, default=str))
        return 0
    print("RIG Prompt Doctor")
    print("=" * 40)
    for key, value in result.items():
        status = "OK" if value is True or (isinstance(value, int) and value > 0) else value
        print(f"  {key:20} {status}")
    healthy = result.get("score_works") and result.get("enhance_works") and result.get("fix_works")
    print()
    print("Status:", "HEALTHY" if healthy else "UNHEALTHY")
    return 0 if healthy else 1


def cmd_suggest(args) -> int:
    query = args.query
    if not query and not sys.stdin.isatty():
        query = sys.stdin.read().strip()
    if not query:
        print("Error: no query provided.", file=sys.stderr)
        return 1
    matches = prompt_engine.suggest(query)
    if args.json:
        print(json.dumps(matches, indent=2))
        return 0
    if not matches:
        print("No matching templates found.")
        return 0
    print(f"Top templates for: {query}\n")
    for i, (key, tmpl) in enumerate(matches.items(), 1):
        preview = tmpl.replace("\n", " ")[:120]
        print(f"{i}. {key}")
        print(f"   {preview}{'...' if len(tmpl) > 120 else ''}\n")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="rig-ai",
        description="RIG AI Engineering — Prompt Intelligence Engine",
    )
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # score
    p_score = subparsers.add_parser("score", help="Score a prompt on the 4-axis rubric.")
    p_score.add_argument("--prompt", "-p", help="Prompt text to score.")
    p_score.add_argument("--file", "-f", help="Read prompt from file.")
    p_score.add_argument("--json", action="store_true", help="Output JSON.")
    p_score.set_defaults(func=cmd_score)

    # enhance
    p_enhance = subparsers.add_parser("enhance", help="Enhance a prompt deterministically.")
    p_enhance.add_argument("--prompt", "-p", help="Prompt text to enhance.")
    p_enhance.add_argument("--file", "-f", help="Read prompt from file.")
    p_enhance.add_argument("--json", action="store_true", help="Output JSON.")
    p_enhance.set_defaults(func=cmd_enhance)

    # fix
    p_fix = subparsers.add_parser("fix", help="Fix common prompt issues.")
    p_fix.add_argument("--prompt", "-p", help="Prompt text to fix.")
    p_fix.add_argument("--file", "-f", help="Read prompt from file.")
    p_fix.add_argument("--json", action="store_true", help="Output JSON.")
    p_fix.set_defaults(func=cmd_fix)

    # doctor
    p_doctor = subparsers.add_parser("doctor", help="Check package health.")
    p_doctor.add_argument("--json", action="store_true", help="Output JSON.")
    p_doctor.set_defaults(func=cmd_doctor)

    # suggest
    p_suggest = subparsers.add_parser("suggest", help="Suggest prompt templates for a task.")
    p_suggest.add_argument("query", nargs="?", help="Task description.")
    p_suggest.add_argument("--json", action="store_true", help="Output JSON.")
    p_suggest.set_defaults(func=cmd_suggest)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

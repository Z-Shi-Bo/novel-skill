from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run_script(script_name: str, args: list[str]) -> int:
    script = SCRIPTS / script_name
    cmd = [sys.executable, str(script), *args]
    return subprocess.call(cmd, cwd=str(ROOT))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unified CLI for Universal Novel Studio.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Initialize a new fiction project")
    p_init.add_argument("--workspace", default=".")
    p_init.add_argument("--templates", default="./templates")
    p_init.add_argument("--title", required=True)
    p_init.add_argument("--slug", default="")
    p_init.add_argument("--genre", default="general-fiction")
    p_init.add_argument("--style", default="default")
    p_init.add_argument("--audience", default="general")
    p_init.add_argument("--language", default="zh-CN")
    p_init.add_argument("--research-mode", default="on-demand")

    p_review = sub.add_parser("review", help="Generate review report")
    p_review.add_argument("--project", required=True)
    p_review.add_argument("--chapter", required=True)
    p_review.add_argument("--json-out", default="")

    p_diag = sub.add_parser("diagnose", help="Run diagnostics")
    p_diag.add_argument("--project", required=True)
    p_diag.add_argument("--scope", default="project", choices=["chapter", "project"])
    p_diag.add_argument("--chapter", default="0")
    p_diag.add_argument("--json-out", default="")

    p_ctx = sub.add_parser("context", help="Build context pack")
    p_ctx.add_argument("--project", required=True)
    p_ctx.add_argument("--task", required=True)
    p_ctx.add_argument("--chapter", default="0")

    p_sync = sub.add_parser("sync", help="Sync indexes")
    p_sync.add_argument("--project", required=True)

    p_research = sub.add_parser("research", help="Write research note")
    p_research.add_argument("--project", required=True)
    p_research.add_argument("--topic", required=True)
    p_research.add_argument("--question", required=True)
    p_research.add_argument("--chapter", default="")
    p_research.add_argument("--conclusion", default="")
    p_research.add_argument("--facts", default="")
    p_research.add_argument("--conflicts", default="")
    p_research.add_argument("--sources", default="")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init":
        code = run_script(
            "init_project.py",
            [
                "--workspace", args.workspace,
                "--templates", args.templates,
                "--title", args.title,
                "--slug", args.slug,
                "--genre", args.genre,
                "--style", args.style,
                "--audience", args.audience,
                "--language", args.language,
                "--research-mode", args.research_mode,
            ],
        )
    elif args.command == "review":
        cmd = ["--project", args.project, "--chapter", str(args.chapter)]
        if args.json_out:
            cmd.extend(["--json-out", args.json_out])
        code = run_script("write_review.py", cmd)
    elif args.command == "diagnose":
        cmd = ["--project", args.project, "--scope", args.scope, "--chapter", str(args.chapter)]
        if args.json_out:
            cmd.extend(["--json-out", args.json_out])
        code = run_script("diagnose_project.py", cmd)
    elif args.command == "context":
        code = run_script(
            "build_context.py",
            ["--project", args.project, "--task", args.task, "--chapter", str(args.chapter)],
        )
    elif args.command == "sync":
        code = run_script("sync_indexes.py", ["--project", args.project])
    elif args.command == "research":
        code = run_script(
            "research_context.py",
            [
                "--project", args.project,
                "--topic", args.topic,
                "--question", args.question,
                "--chapter", args.chapter,
                "--conclusion", args.conclusion,
                "--facts", args.facts,
                "--conflicts", args.conflicts,
                "--sources", args.sources,
            ],
        )
    else:
        raise SystemExit(f"unknown command: {args.command}")

    raise SystemExit(code)


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
from pathlib import Path

from common import append_markdown_row, chapter_token, dump_manifest, load_manifest, read_text, today_str, write_text


def replace_state_row(content: str, field: str, value: str) -> str:
    lines = content.splitlines()
    for index, line in enumerate(lines):
        if line.strip().startswith(f"| {field} |"):
            lines[index] = f"| {field} | {value} |"
    return "\n".join(lines)


def update_current_state(
    path: Path,
    chapter: int,
    volume: str,
    location: str,
    goal: str,
    status: str,
    known_truth: str,
    pressure: str,
) -> None:
    content = read_text(path)
    replacements = {
        "current_phase": "synced",
        "current_volume": volume,
        "current_chapter": str(chapter),
        "current_location": location,
        "active_goal": goal,
        "active_status": status,
        "known_truth": known_truth,
        "next_pressure": pressure,
        "last_synced": today_str(),
    }
    for field, value in replacements.items():
        content = replace_state_row(content, field, value)
    content = content.replace("{{TODAY}}", today_str())
    write_text(path, content)


def main() -> None:
    parser = argparse.ArgumentParser(description="Update current story state and ledgers after chapter finalization.")
    parser.add_argument("--project", required=True)
    parser.add_argument("--chapter", type=int, required=True)
    parser.add_argument("--volume", default="1")
    parser.add_argument("--location", default="TBD")
    parser.add_argument("--goal", default="TBD")
    parser.add_argument("--status", default="TBD")
    parser.add_argument("--known-truth", default="TBD")
    parser.add_argument("--pressure", default="TBD")
    parser.add_argument("--hook-id", default="")
    parser.add_argument("--hook-type", default="")
    parser.add_argument("--hook-status", default="")
    parser.add_argument("--hook-payoff", default="")
    parser.add_argument("--hook-note", default="")
    parser.add_argument("--event", default="")
    parser.add_argument("--resource-category", default="")
    parser.add_argument("--resource-delta", default="")
    args = parser.parse_args()

    project_dir = Path(args.project)
    token = chapter_token(args.chapter)

    update_current_state(
        project_dir / "05_state/current_state.md",
        args.chapter,
        str(args.volume),
        args.location,
        args.goal,
        args.status,
        args.known_truth,
        args.pressure,
    )

    if args.hook_id:
        hook_row = (
            f"| {args.hook_id} | {token} | {args.hook_type or 'hook'} | "
            f"{args.hook_status or 'active'} | {args.hook_payoff or 'TBD'} | {args.hook_note or ''} |"
        )
        append_markdown_row(project_dir / "05_state/pending_hooks.md", "hook_table", hook_row)

    if args.event:
        event_row = f"| {today_str()} | {token} | {args.event} | {args.status or 'state change'} |"
        append_markdown_row(project_dir / "05_state/timeline.md", "timeline_table", event_row)

    if args.resource_category and args.resource_delta:
        resource_row = (
            f"| {today_str()} | {token} | {args.volume} | {args.resource_category} | "
            f"{args.resource_delta} | {args.goal or ''} |"
        )
        append_markdown_row(project_dir / "05_state/resource_ledger.md", "resource_table", resource_row)

    index_path = project_dir / "03_outline/chapter_index.md"
    index_text = read_text(index_path)
    sync_row = f"| {args.chapter} | {args.volume} | {token} | done | done | done | done | synced | {today_str()} |"
    if sync_row not in index_text:
        append_markdown_row(index_path, "chapter_index", sync_row)

    manifest = load_manifest(project_dir)
    manifest["current_phase"] = "synced"
    manifest["current_volume"] = str(args.volume)
    manifest["current_chapter"] = str(args.chapter)
    manifest["last_updated"] = today_str()
    dump_manifest(project_dir, manifest)

    print(project_dir)


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
from pathlib import Path

from common import chapter_token, read_text, replace_placeholder, today_str, upsert_markdown_row, write_text


def truncate_sentences(text: str, limit: int = 3) -> list[str]:
    normalized = text.replace("。", "。\n").replace("!", "!\n").replace("？", "？\n")
    rows = [line.strip() for line in normalized.splitlines() if line.strip()]
    return rows[:limit] or ["待补充"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Create or update a chapter summary file.")
    parser.add_argument("--project", required=True)
    parser.add_argument("--chapter", type=int, required=True)
    parser.add_argument("--source", default="", help="Optional source markdown path")
    args = parser.parse_args()

    project_dir = Path(args.project)
    token = chapter_token(args.chapter)
    source_path = Path(args.source) if args.source else project_dir / f"04_manuscript/chapters/{token}.md"
    source_text = read_text(source_path)
    summary_template = read_text(Path(__file__).resolve().parents[1] / "templates" / "chapter_summary.md")
    content = replace_placeholder(summary_template, {"CHAPTER_NO": f"{args.chapter:03d}", "TODAY": today_str()})

    happened = truncate_sentences(source_text, 3)
    changed = truncate_sentences(source_text, 2)
    carry = truncate_sentences(source_text, 2)

    content = content.replace("## What Happened\n- \n", "## What Happened\n" + "\n".join(f"- {x}" for x in happened) + "\n")
    content = content.replace("## What Changed\n- \n", "## What Changed\n" + "\n".join(f"- {x}" for x in changed) + "\n")
    content = content.replace("## Carry Forward\n- \n", "## Carry Forward\n" + "\n".join(f"- {x}" for x in carry) + "\n")

    target = project_dir / f"06_reports/chapter_summaries/{token}_summary.md"
    write_text(target, content)
    summary_index = project_dir / "06_reports/chapter_summaries/summary_index.md"
    carry_value = carry[0][:40] if carry else "待补充"
    row = f"| {token} | {target.name} | {today_str()} | {carry_value} |"
    if summary_index.exists():
        upsert_markdown_row(summary_index, "summary_index", token, row)
    print(target)


if __name__ == "__main__":
    main()

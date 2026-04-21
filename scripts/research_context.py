from __future__ import annotations

import re
from pathlib import Path

from common import append_markdown_row, parser_with_project, read_text, slugify, today_str, upsert_markdown_row, write_text


def replace_section(body: str, heading: str, items: list[str]) -> str:
    bullet_block = "\n".join(f"- {item}" for item in items)
    pattern = re.compile(rf"## {re.escape(heading)}\n(?:(?!## ).*\n?)*", re.M)
    replacement = f"## {heading}\n{bullet_block}\n"
    if pattern.search(body):
        return pattern.sub(replacement, body)
    return body + "\n" + replacement


def main() -> None:
    parser = parser_with_project("Create a research note for reality-grounded fiction tasks.")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--question", required=True)
    parser.add_argument("--chapter", default="")
    parser.add_argument("--conclusion", default="")
    parser.add_argument("--facts", default="")
    parser.add_argument("--conflicts", default="")
    parser.add_argument("--sources", default="")
    args = parser.parse_args()

    project_dir = Path(args.project)
    template = read_text(Path(__file__).resolve().parents[1] / "templates" / "research_note.md")
    topic_slug = slugify(args.topic)
    note_id = f"research-{topic_slug}"
    body = template
    body = body.replace("{{NOTE_ID}}", note_id)
    body = body.replace("{{TOPIC}}", args.topic)
    body = body.replace("{{TODAY}}", today_str())
    body = replace_section(body, "Research Question", [args.question])
    body = replace_section(body, "Scene / Chapter Relevance", [args.chapter or "TBD"])
    body = replace_section(body, "Verified Conclusion", [args.conclusion or "待补充"])
    fact_lines = [item.strip() for item in args.facts.split("||") if item.strip()] or ["待补充"]
    body = replace_section(body, "Writable Facts", fact_lines)
    body = replace_section(body, "Conflicts / Caveats", [args.conflicts or "暂无"])
    source_lines = [item.strip() for item in args.sources.split("||") if item.strip()] or ["待补充"]
    body = replace_section(body, "Sources", source_lines)
    target = project_dir / f"06_reports/research/{topic_slug}.md"
    write_text(target, body)

    index_path = project_dir / "06_reports/research/research_index.md"
    if index_path.exists():
        existing = read_text(index_path)
        row = f"| {note_id} | {args.topic} | {args.chapter or 'TBD'} | {today_str()} | {(args.conclusion or '待补充')[:40]} |"
        if note_id in existing:
            upsert_markdown_row(index_path, "research_index", note_id, row)
        else:
            append_markdown_row(index_path, "research_index", row)
    print(target)


if __name__ == "__main__":
    main()

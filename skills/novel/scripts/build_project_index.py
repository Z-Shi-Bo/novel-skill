from __future__ import annotations

import json
from pathlib import Path

from common import load_manifest, markdown_table_rows, parser_with_project, read_text, write_text


def rows_to_objects(text: str, kind: str) -> list[dict]:
    rows = markdown_table_rows(text)
    if not rows:
        return []
    header = rows[0]
    items = []
    for row in rows[1:]:
        if len(row) != len(header):
            continue
        entry = {header[i]: row[i] for i in range(len(header))}
        entry["kind"] = kind
        items.append(entry)
    return items


def main() -> None:
    parser = parser_with_project("Build unified project index json from markdown indexes.")
    parser.add_argument("--out", default="")
    args = parser.parse_args()

    project_dir = Path(args.project)
    manifest = load_manifest(project_dir)

    summary_index = read_text(project_dir / "06_reports/chapter_summaries/summary_index.md")
    review_index = read_text(project_dir / "06_reports/reviews/review_index.md")
    research_index = read_text(project_dir / "06_reports/research/research_index.md")

    payload = {
        "project": manifest,
        "indexes": {
            "summary": rows_to_objects(summary_index, "summary"),
            "review": rows_to_objects(review_index, "review"),
            "research": rows_to_objects(research_index, "research"),
        },
    }

    index_dir = project_dir / "06_reports/index"
    index_dir.mkdir(parents=True, exist_ok=True)
    target = Path(args.out) if args.out else index_dir / "project_index.json"
    write_text(target, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(target)


if __name__ == "__main__":
    main()

from __future__ import annotations

from pathlib import Path

from common import chapter_token, list_recent_files, parser_with_project, read_text, write_text


def main() -> None:
    parser = parser_with_project("Export chapters or full manuscript as markdown/txt.")
    parser.add_argument("--mode", choices=["chapter", "manuscript"], default="manuscript")
    parser.add_argument("--chapter", type=int, default=0)
    parser.add_argument("--format", choices=["md", "txt"], default="md")
    args = parser.parse_args()

    project_dir = Path(args.project)
    export_dir = project_dir / "07_exports"
    export_dir.mkdir(parents=True, exist_ok=True)

    if args.mode == "chapter":
        if not args.chapter:
            raise SystemExit("--chapter is required when mode=chapter")
        token = chapter_token(args.chapter)
        source = project_dir / f"04_manuscript/chapters/{token}.md"
        content = read_text(source)
        target = export_dir / f"{token}.{args.format}"
    else:
        parts = [read_text(path) for path in list_recent_files(project_dir / "04_manuscript/chapters", "ch*.md", 999)]
        content = "\n\n".join(parts)
        target = export_dir / f"manuscript.{args.format}"

    write_text(target, content)
    print(target)


if __name__ == "__main__":
    main()

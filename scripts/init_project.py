from __future__ import annotations

import argparse
from pathlib import Path

from common import ROOT_DIRS, replace_placeholder, slugify, today_str, write_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Initialize a one-book-one-folder fiction project.")
    parser.add_argument("--workspace", required=True, help="Workspace directory that contains projects/")
    parser.add_argument("--templates", required=True, help="Template directory path")
    parser.add_argument("--title", required=True, help="Novel title")
    parser.add_argument("--slug", default="", help="Optional custom slug")
    parser.add_argument("--genre", default="general-fiction")
    parser.add_argument("--style", default="default")
    parser.add_argument("--audience", default="general")
    parser.add_argument("--language", default="zh-CN")
    parser.add_argument("--research-mode", default="on-demand")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    workspace = Path(args.workspace)
    templates = Path(args.templates)
    projects_dir = workspace / "projects"
    projects_dir.mkdir(parents=True, exist_ok=True)

    slug = args.slug or slugify(args.title)
    project_dir = projects_dir / slug
    project_dir.mkdir(parents=True, exist_ok=True)

    for rel_dir in ROOT_DIRS:
        (project_dir / rel_dir).mkdir(parents=True, exist_ok=True)

    mapping = {
        "NOVEL_TITLE": args.title,
        "NOVEL_SLUG": slug,
        "GENRE": args.genre,
        "STYLE": args.style,
        "AUDIENCE": args.audience,
        "LANGUAGE": args.language,
        "RESEARCH_MODE": args.research_mode,
        "TODAY": today_str(),
        "CHAPTER_NO": "001",
        "VOLUME_NO": "1",
    }

    file_map = {
        "project_manifest.yaml": "project_manifest.yaml",
        "project_brief.md": "01_brief/project_brief.md",
        "story_bible.md": "02_bible/story_bible.md",
        "character_cards.md": "02_bible/character_cards.md",
        "relationship_matrix.md": "02_bible/relationship_matrix.md",
        "volume_outline.md": "03_outline/volume_outline.md",
        "chapter_index.md": "03_outline/chapter_index.md",
        "current_state.md": "05_state/current_state.md",
        "pending_hooks.md": "05_state/pending_hooks.md",
        "timeline.md": "05_state/timeline.md",
        "resource_ledger.md": "05_state/resource_ledger.md",
        "summary_index.md": "06_reports/chapter_summaries/summary_index.md",
        "review_index.md": "06_reports/reviews/review_index.md",
        "research_index.md": "06_reports/research/research_index.md",
        "project_index.json": "06_reports/index/project_index.json",
    }

    for template_name, target_rel in file_map.items():
        content = (templates / template_name).read_text(encoding="utf-8")
        content = replace_placeholder(content, mapping)
        write_text(project_dir / target_rel, content)

    chapter_outline = (templates / "chapter_outline.md").read_text(encoding="utf-8")
    chapter_outline = replace_placeholder(chapter_outline, mapping)
    write_text(project_dir / "03_outline/chapter_outlines/ch001.md", chapter_outline)

    print(project_dir)


if __name__ == "__main__":
    main()

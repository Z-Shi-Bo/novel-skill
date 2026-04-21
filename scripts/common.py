from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import List

ROOT_DIRS = [
    "01_brief",
    "02_bible",
    "03_outline/chapter_outlines",
    "04_manuscript/drafts",
    "04_manuscript/chapters",
    "05_state",
    "06_reports/chapter_summaries",
    "06_reports/reviews",
    "06_reports/diagnostics",
    "06_reports/research",
    "07_exports",
]


def today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def slugify(text: str) -> str:
    value = text.strip().lower()
    value = re.sub(r"[^\w\-\s一-鿿]", "", value)
    value = re.sub(r"[\s_]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "novel-project"


def chapter_token(chapter: int | str) -> str:
    return f"ch{int(chapter):03d}"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def read_text(path: Path, default: str = "") -> str:
    return path.read_text(encoding="utf-8") if path.exists() else default


def write_text(path: Path, content: str) -> None:
    ensure_parent(path)
    path.write_text(content, encoding="utf-8")


def replace_placeholder(text: str, mapping: dict[str, str]) -> str:
    result = text
    for key, value in mapping.items():
        result = result.replace("{{" + key + "}}", value)
    return result


def load_manifest(project_dir: Path) -> dict[str, str]:
    path = project_dir / "project_manifest.yaml"
    data: dict[str, str] = {}
    for line in read_text(path).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def dump_manifest(project_dir: Path, data: dict[str, str]) -> None:
    ordered_keys = [
        "title",
        "slug",
        "genre",
        "style",
        "audience",
        "language",
        "research_mode",
        "strong_sync",
        "current_phase",
        "current_volume",
        "current_chapter",
        "last_updated",
    ]
    lines: list[str] = []
    for key in ordered_keys:
        if key in data:
            lines.append(f'{key}: "{data[key]}"')
    for key, value in data.items():
        if key not in ordered_keys:
            lines.append(f'{key}: "{value}"')
    write_text(project_dir / "project_manifest.yaml", "\n".join(lines) + "\n")


def list_recent_files(path: Path, pattern: str, limit: int) -> List[Path]:
    files = sorted(path.glob(pattern), key=lambda item: item.name)
    return files[-limit:] if limit > 0 else files


def append_markdown_row(path: Path, marker: str, row: str) -> None:
    text = read_text(path)
    lines = text.splitlines()
    start_marker = f"<!-- START:{marker} -->"
    end_marker = f"<!-- END:{marker} -->"
    start = next((i for i, line in enumerate(lines) if line.strip() == start_marker), None)
    end = next((i for i, line in enumerate(lines) if line.strip() == end_marker), None)
    if start is None or end is None or end <= start:
        raise ValueError(f"cannot find marker block: {marker} in {path}")
    insert_at = end
    for index in range(end - 1, start, -1):
        if lines[index].strip().startswith("|"):
            insert_at = index + 1
            break
    lines.insert(insert_at, row)
    write_text(path, "\n".join(lines).rstrip() + "\n")


def upsert_markdown_row(path: Path, marker: str, key: str, row: str) -> None:
    text = read_text(path)
    lines = text.splitlines()
    start_marker = f"<!-- START:{marker} -->"
    end_marker = f"<!-- END:{marker} -->"
    start = next((i for i, line in enumerate(lines) if line.strip() == start_marker), None)
    end = next((i for i, line in enumerate(lines) if line.strip() == end_marker), None)
    if start is None or end is None or end <= start:
        raise ValueError(f"cannot find marker block: {marker} in {path}")

    key_token = f"| {key} |"
    for index in range(start + 1, end):
        if key_token in lines[index]:
            lines[index] = row
            write_text(path, "\n".join(lines).rstrip() + "\n")
            return

    append_markdown_row(path, marker, row)


def markdown_table_rows(text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped:
            continue
        parts = [part.strip() for part in stripped.strip("|").split("|")]
        rows.append(parts)
    return rows


def detect_genre_profile(genre: str) -> dict[str, list[str]]:
    value = genre.lower()
    if any(key in value for key in ["玄幻", "奇幻", "fantasy"]):
        return {
            "priority_files": ["02_bible/story_bible.md", "05_state/resource_ledger.md", "05_state/pending_hooks.md"],
            "risk_tags": ["战力飘", "资源乱", "设定吃书"],
        }
    if any(key in value for key in ["历史", "年代", "period"]):
        return {
            "priority_files": ["05_state/timeline.md", "06_reports/research/research_index.md", "02_bible/story_bible.md"],
            "risk_tags": ["时间错配", "风俗错位", "时代感漂浮"],
        }
    if any(key in value for key in ["悬疑", "犯罪", "mystery", "crime"]):
        return {
            "priority_files": ["05_state/timeline.md", "06_reports/chapter_summaries/summary_index.md", "05_state/pending_hooks.md"],
            "risk_tags": ["线索硬藏", "反转靠降智", "流程失真"],
        }
    if any(key in value for key in ["科幻", "sci-fi", "science fiction"]):
        return {
            "priority_files": ["02_bible/story_bible.md", "06_reports/chapter_summaries/summary_index.md", "05_state/pending_hooks.md"],
            "risk_tags": ["概念堆砌", "硬设定打架", "解释过载"],
        }
    if any(key in value for key in ["同人", "fanfic"]):
        return {
            "priority_files": ["02_bible/character_cards.md", "02_bible/relationship_matrix.md", "06_reports/chapter_summaries/summary_index.md"],
            "risk_tags": ["OOC", "套原桥段", "世界观断层"],
        }
    if any(key in value for key in ["言情", "情感", "romance"]):
        return {
            "priority_files": ["02_bible/character_cards.md", "02_bible/relationship_matrix.md", "06_reports/chapter_summaries/summary_index.md"],
            "risk_tags": ["情绪空喊", "推进太快", "误会模板化"],
        }
    return {
        "priority_files": ["02_bible/story_bible.md", "05_state/current_state.md"],
        "risk_tags": ["上下文漂移", "闭环缺失"],
    }


def parser_with_project(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--project", required=True, help="Project directory path")
    return parser

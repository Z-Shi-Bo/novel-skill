from __future__ import annotations

import json
from pathlib import Path

from common import chapter_token, detect_genre_profile, list_recent_files, load_manifest, markdown_table_rows, parser_with_project, read_text


def recent_research_from_index(index_text: str, limit: int = 5) -> list[dict[str, str]]:
    rows = markdown_table_rows(index_text)
    items: list[dict[str, str]] = []
    for row in rows:
        if not row or row[0] == "note_id":
            continue
        if len(row) < 5:
            continue
        items.append(
            {
                "note_id": row[0],
                "topic": row[1],
                "chapter": row[2],
                "updated": row[3],
                "summary": row[4],
            }
        )
    return items[-limit:]


def score_item(task: str, chapter: int, item: dict, genre_profile: dict[str, list[str]]) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []

    kind = item.get("kind", "file")
    chapter_ref = item.get("chapter", "")
    path = item.get("path", "")

    if task == "write":
        if kind in {"summary", "outline", "hook", "state"}:
            score += 30
            reasons.append("write task prefers story-memory/control files")
    elif task == "review":
        if kind in {"review", "summary", "timeline", "hook", "state"}:
            score += 35
            reasons.append("review task prefers traceable continuity artifacts")
    elif task == "resume":
        if kind in {"summary", "review", "state"}:
            score += 28
            reasons.append("resume task prefers condensed recent context")

    if chapter_ref.startswith("ch"):
        try:
            ref_num = int(chapter_ref.replace("ch", ""))
            distance = abs(chapter - ref_num)
            score += max(0, 20 - distance * 5)
            reasons.append(f"chapter proximity={distance}")
        except ValueError:
            pass

    if any(priority in path for priority in genre_profile.get("priority_files", [])):
        score += 20
        reasons.append("matches genre priority file")

    if "index" in path:
        score += 10
        reasons.append("index-level artifact")

    if "pending_hooks" in path or kind == "hook":
        score += 8
        reasons.append("hook continuity signal")

    if "timeline" in path or kind == "timeline":
        score += 8
        reasons.append("timeline continuity signal")

    return score, reasons


def build_ranked_items(project_dir: Path, chapter: int, task: str, genre_profile: dict[str, list[str]], summaries: list[dict], project_index: dict) -> tuple[list[dict], list[dict], dict]:
    candidates: list[dict] = []

    candidates.append({
        "id": "current_state",
        "kind": "state",
        "path": str(project_dir / "05_state/current_state.md"),
        "chapter": f"ch{chapter:03d}" if chapter else "",
        "excerpt": read_text(project_dir / "05_state/current_state.md")[:400],
    })
    candidates.append({
        "id": "pending_hooks",
        "kind": "hook",
        "path": str(project_dir / "05_state/pending_hooks.md"),
        "chapter": "",
        "excerpt": read_text(project_dir / "05_state/pending_hooks.md")[:300],
    })
    candidates.append({
        "id": "timeline",
        "kind": "timeline",
        "path": str(project_dir / "05_state/timeline.md"),
        "chapter": "",
        "excerpt": read_text(project_dir / "05_state/timeline.md")[:300],
    })

    for summary in summaries:
        summary_path = Path(summary["path"])
        candidates.append({
            "id": summary_path.stem,
            "kind": "summary",
            "path": summary["path"],
            "chapter": summary_path.stem.replace("_summary", ""),
            "excerpt": summary["content"][:400],
        })

    for entry in project_index.get("indexes", {}).get("review", []):
        candidates.append({
            "id": entry.get("chapter_no", "review"),
            "kind": "review",
            "path": str(project_dir / "06_reports/reviews" / entry.get("review_file", "")),
            "chapter": entry.get("chapter_no", ""),
            "excerpt": json.dumps(entry, ensure_ascii=False),
        })

    for entry in project_index.get("indexes", {}).get("research", []):
        candidates.append({
            "id": entry.get("note_id", "research"),
            "kind": "research",
            "path": str(project_dir / "06_reports/research" / f"{entry.get('topic', '')}.md"),
            "chapter": entry.get("chapter", ""),
            "excerpt": json.dumps(entry, ensure_ascii=False),
        })

    scored = []
    for item in candidates:
        score, reasons = score_item(task, chapter, item, genre_profile)
        enriched = dict(item)
        enriched["score"] = score
        enriched["reasons"] = reasons
        scored.append(enriched)

    scored.sort(key=lambda x: x["score"], reverse=True)
    selected = scored[:6]
    rejected = scored[6:]
    scores = {item["id"]: item["score"] for item in scored}
    return selected, rejected, scores


def main() -> None:
    parser = parser_with_project("Build a minimal context pack for fiction tasks.")
    parser.add_argument("--task", required=True, help="Task type such as write/review/revise/resume")
    parser.add_argument("--chapter", type=int, default=0, help="Target chapter number")
    parser.add_argument("--summary-window", type=int, default=3)
    args = parser.parse_args()

    project_dir = Path(args.project)
    manifest = load_manifest(project_dir)
    chapter = args.chapter or int(manifest.get("current_chapter", "0") or 0)
    token = chapter_token(chapter) if chapter else ""
    genre_profile = detect_genre_profile(manifest.get("genre", ""))

    outline_path = project_dir / f"03_outline/chapter_outlines/{token}.md" if token else None
    draft_path = project_dir / f"04_manuscript/drafts/{token}_draft.md" if token else None
    final_path = project_dir / f"04_manuscript/chapters/{token}.md" if token else None
    research_index = read_text(project_dir / "06_reports/research/research_index.md")
    summary_index = read_text(project_dir / "06_reports/chapter_summaries/summary_index.md")
    review_index = read_text(project_dir / "06_reports/reviews/review_index.md")
    project_index = read_text(project_dir / "06_reports/index/project_index.json")
    project_index_data = json.loads(project_index) if project_index.strip().startswith("{") else {}

    summaries = [
        {"path": str(path), "content": read_text(path)}
        for path in list_recent_files(project_dir / "06_reports/chapter_summaries", "ch*_summary.md", args.summary_window)
    ]

    selected_items, rejected_items, scores = build_ranked_items(
        project_dir,
        chapter,
        args.task,
        genre_profile,
        summaries,
        project_index_data,
    )
    reasoning_summary = (
        f"task={args.task}; genre={manifest.get('genre', '')}; "
        f"selected={len(selected_items)}; rejected={len(rejected_items)}"
    )

    result = {
        "task_type": args.task,
        "target_chapter": chapter,
        "project_title": manifest.get("title", ""),
        "current_story_state": read_text(project_dir / "05_state/current_state.md"),
        "required_constraints": {
            "genre": manifest.get("genre", ""),
            "style": manifest.get("style", ""),
            "research_mode": manifest.get("research_mode", "on-demand"),
        },
        "genre_priority": genre_profile,
        "chapter_index_excerpt": read_text(project_dir / "03_outline/chapter_index.md")[:1500],
        "summary_index_excerpt": summary_index[:1000],
        "review_index_excerpt": review_index[:1000],
        "project_index_excerpt": project_index[:1200],
        "chapter_outline": read_text(outline_path) if outline_path and outline_path.exists() else "",
        "recent_story_memory": summaries,
        "active_hooks": read_text(project_dir / "05_state/pending_hooks.md"),
        "character_focus": read_text(project_dir / "02_bible/character_cards.md")[:1500],
        "world_rules": read_text(project_dir / "02_bible/story_bible.md")[:1500],
        "research_index_excerpt": research_index[:1000],
        "recent_research_memory": recent_research_from_index(research_index, 5),
        "research_notes": [str(p) for p in list_recent_files(project_dir / "06_reports/research", "*.md", 5)],
        "unresolved_risks": genre_profile["risk_tags"],
        "selected_items": selected_items,
        "rejected_items": rejected_items,
        "scores": scores,
        "reasoning_summary": reasoning_summary,
        "draft_excerpt": read_text(draft_path)[:1200] if draft_path and draft_path.exists() else "",
        "final_excerpt": read_text(final_path)[:1200] if final_path and final_path.exists() else "",
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

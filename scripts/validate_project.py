from __future__ import annotations

import json
import re
from pathlib import Path

from common import markdown_table_rows, parser_with_project, read_text

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def is_int_like(value: str) -> bool:
    try:
        return int(value) >= 0
    except Exception:
        return False


def parse_manifest(project_dir: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in read_text(project_dir / "project_manifest.yaml").splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def validate_manifest(project_dir: Path) -> list[str]:
    errors: list[str] = []
    data = parse_manifest(project_dir)
    required = [
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
    for key in required:
        if not data.get(key):
            errors.append(f"manifest missing required field: {key}")
    if data.get("research_mode") and data["research_mode"] not in {"off", "on-demand", "strict"}:
        errors.append("manifest research_mode must be off/on-demand/strict")
    if data.get("strong_sync") and data["strong_sync"] not in {"true", "false"}:
        errors.append("manifest strong_sync must be true/false")
    if data.get("current_volume") and not is_int_like(data["current_volume"]):
        errors.append("manifest current_volume must be a non-negative integer")
    if data.get("current_chapter") and not is_int_like(data["current_chapter"]):
        errors.append("manifest current_chapter must be a non-negative integer")
    if data.get("last_updated") and not DATE_RE.match(data["last_updated"]):
        errors.append("manifest last_updated must be YYYY-MM-DD")
    return errors


def validate_current_state(project_dir: Path, strong_sync: bool) -> list[str]:
    errors: list[str] = []
    text = read_text(project_dir / "05_state/current_state.md")
    required_fields = {
        "title",
        "current_phase",
        "current_volume",
        "current_chapter",
        "current_location",
        "active_goal",
        "active_status",
        "known_truth",
        "next_pressure",
        "last_synced",
    }
    rows = markdown_table_rows(text)
    found = {row[0] for row in rows if len(row) >= 2 and row[0] != "Field"}
    for field in required_fields:
        if field not in found:
            errors.append(f"current_state missing field: {field}")
    snapshot = {row[0]: row[1] for row in rows if len(row) >= 2 and row[0] != "Field"}
    if "current_volume" in snapshot and not is_int_like(snapshot["current_volume"]):
        errors.append("current_state current_volume must be a non-negative integer")
    if "current_chapter" in snapshot and not is_int_like(snapshot["current_chapter"]):
        errors.append("current_state current_chapter must be a non-negative integer")
    if "last_synced" in snapshot and not DATE_RE.match(snapshot["last_synced"]):
        errors.append("current_state last_synced must be YYYY-MM-DD")
    if strong_sync and "<!-- START:active_constraints -->" not in text:
        errors.append("current_state missing active_constraints start marker")
    if strong_sync and "<!-- END:active_constraints -->" not in text:
        errors.append("current_state missing active_constraints end marker")
    return errors


def validate_pending_hooks(project_dir: Path) -> list[str]:
    errors: list[str] = []
    text = read_text(project_dir / "05_state/pending_hooks.md")
    rows = markdown_table_rows(text)
    header = rows[0] if rows else []
    expected = ["hook_id", "introduced_in", "type", "status", "expected_payoff", "note"]
    if header != expected:
        errors.append("pending_hooks header does not match expected schema")
        return errors
    seen: set[str] = set()
    for row in rows[1:]:
        if len(row) < 6:
            errors.append("pending_hooks has malformed row")
            continue
        hook_id, _introduced_in, _type, status, payoff, _note = row[:6]
        if not hook_id:
            errors.append("pending_hooks hook_id cannot be empty")
        if hook_id in seen:
            errors.append(f"pending_hooks duplicate hook_id: {hook_id}")
        seen.add(hook_id)
        if status not in {"active", "resolved", "stale", "dropped"}:
            errors.append(f"pending_hooks invalid status: {status}")
        if status == "active" and not payoff:
            errors.append(f"pending_hooks active hook missing expected_payoff: {hook_id}")
    return errors


def validate_index(path: Path, expected_header: list[str], name: str) -> list[str]:
    errors: list[str] = []
    text = read_text(path)
    rows = markdown_table_rows(text)
    if not rows:
        errors.append(f"{name} is empty or missing markdown table")
        return errors
    if rows[0] != expected_header:
        errors.append(f"{name} header does not match expected schema")
    return errors


def main() -> None:
    parser = parser_with_project("Validate project schema consistency.")
    parser.add_argument("--json-out", default="")
    args = parser.parse_args()

    project_dir = Path(args.project)
    result: dict[str, list[str]] = {}

    manifest_errors = validate_manifest(project_dir)
    result["project_manifest"] = manifest_errors

    manifest = parse_manifest(project_dir)
    strong_sync = manifest.get("strong_sync", "true") == "true"

    result["current_state"] = validate_current_state(project_dir, strong_sync)
    result["pending_hooks"] = validate_pending_hooks(project_dir)
    result["chapter_index"] = validate_index(
        project_dir / "03_outline/chapter_index.md",
        ["chapter_no", "volume", "title", "outline_status", "draft_status", "review_status", "final_status", "sync_status", "last_updated"],
        "chapter_index",
    )
    result["summary_index"] = validate_index(
        project_dir / "06_reports/chapter_summaries/summary_index.md",
        ["chapter_no", "summary_file", "updated", "carry_forward"],
        "summary_index",
    )
    result["review_index"] = validate_index(
        project_dir / "06_reports/reviews/review_index.md",
        ["chapter_no", "verdict", "review_file", "updated", "highest_issue"],
        "review_index",
    )
    result["research_index"] = validate_index(
        project_dir / "06_reports/research/research_index.md",
        ["note_id", "topic", "chapter", "updated", "summary"],
        "research_index",
    )

    flat_errors = [(section, err) for section, errors in result.items() for err in errors]
    payload = {
        "project": str(project_dir),
        "ok": not flat_errors,
        "errors": result,
    }

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if flat_errors:
        print("SCHEMA_INVALID")
        for section, err in flat_errors:
            print(f"[{section}] {err}")
        raise SystemExit(1)

    print("SCHEMA_OK")


if __name__ == "__main__":
    main()

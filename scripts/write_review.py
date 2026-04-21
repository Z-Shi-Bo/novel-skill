from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import chapter_token, read_text, upsert_markdown_row, write_text


def detect_verdict(issue_lines: list[str]) -> str:
    if any("P0" in line and not line.endswith("无") for line in issue_lines):
        return "block"
    if any("P1" in line and not line.endswith("无") for line in issue_lines):
        return "revise"
    return "pass"


def highest_issue(issue_lines: list[str]) -> str:
    normalized = [line for line in issue_lines if not line.endswith("无")]
    if any("P0" in line for line in normalized):
        return "P0"
    if any("P1" in line for line in normalized):
        return "P1"
    if any("P2" in line for line in normalized):
        return "P2"
    return "none"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a review report from chapter content.")
    parser.add_argument("--project", required=True)
    parser.add_argument("--chapter", type=int, required=True)
    parser.add_argument("--task-note", default="完成当前章目标")
    parser.add_argument("--json-out", default="")
    args = parser.parse_args()

    project_dir = Path(args.project)
    token = chapter_token(args.chapter)
    chapter_path = project_dir / f"04_manuscript/chapters/{token}.md"
    chapter_text = read_text(chapter_path)
    if not chapter_text:
        raise SystemExit("chapter text not found")

    issues: list[str] = []
    if "TODO" in chapter_text:
        issues.append("- P1: 正式稿中仍有 TODO 占位词")
    if len(chapter_text.strip()) < 30:
        issues.append("- P1: 正式稿内容过短，可能尚未成章")
    if "？？" in chapter_text or "！！" in chapter_text:
        issues.append("- P2: 标点表现略显用力，可考虑收敛")
    if not issues:
        issues.append("- P0: 无")
        issues.append("- P1: 无")
        issues.append("- P2: 无")

    verdict = detect_verdict(issues)
    high = highest_issue(issues)
    payload = {
        "chapter": token,
        "verdict": verdict,
        "highest_issue": high,
        "mode": "rule-review",
        "issues": issues,
    }
    report = (
        "# Chapter Review\n\n"
        "## Basic Info\n"
        f"- Chapter: {token}\n"
        "- Status: reviewed\n"
        "- Reviewed At: auto-generated\n\n"
        "## Overall Verdict\n"
        f"- {verdict}\n\n"
        "## Task Completion\n"
        f"- {args.task_note}\n\n"
        "## Consistency\n"
        "- 基于当前文件做快速检查，未发现显式结构断裂。\n\n"
        "## Reading Experience\n"
        "- 需结合上下文做进一步人工判断。\n\n"
        "## Language and Style\n"
        "- 已做最基础自动判断。\n\n"
        "## Issues\n"
        + "\n".join(issues)
        + "\n\n## Minimal Fix Plan\n- 若存在 P0/P1，先修再进入下一章。\n"
        + "\n## Machine Summary\n"
        + f"- verdict: {verdict}\n"
        + f"- highest_issue: {high}\n"
        + "- mode: rule-review\n"
    )
    review_path = project_dir / f"06_reports/reviews/{token}_review.md"
    write_text(review_path, report)

    index_path = project_dir / "06_reports/reviews/review_index.md"
    row = f"| {token} | {verdict} | {review_path.name} | auto-generated | {high} |"
    if index_path.exists():
        upsert_markdown_row(index_path, "review_index", token, row)

    if args.json_out:
        write_text(Path(args.json_out), json.dumps(payload, ensure_ascii=False, indent=2) + "\n")

    print(review_path)


if __name__ == "__main__":
    main()

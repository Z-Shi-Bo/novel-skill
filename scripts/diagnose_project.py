from __future__ import annotations

import json
import re
from pathlib import Path

from common import chapter_token, list_recent_files, markdown_table_rows, parser_with_project, read_text, today_str, upsert_markdown_row, write_text


def count_table_rows(text: str) -> int:
    rows = []
    for line in text.splitlines():
        if line.strip().startswith("|") and "---" not in line and "Field" not in line:
            rows.append(line)
    return len(rows)


def extract_status_column(index_text: str) -> list[str]:
    values = []
    for line in index_text.splitlines():
        if not line.strip().startswith("|") or "---" in line or "chapter_no" in line:
            continue
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) >= 8:
            values.append(parts[7])
    return values


def highest_issue_label(lines: list[str]) -> str:
    normalized = [line for line in lines if not line.endswith("无")]
    if any("P0" in line for line in normalized):
        return "P0"
    if any("P1" in line for line in normalized):
        return "P1"
    if any("P2" in line for line in normalized):
        return "P2"
    return "none"


def severity_summary(lines: list[str]) -> dict[str, int]:
    summary = {"P0": 0, "P1": 0, "P2": 0}
    for line in lines:
        for key in summary:
            if key in line:
                summary[key] += 1
    return summary


def sync_summary_index(project_dir: Path) -> None:
    index_path = project_dir / "06_reports/chapter_summaries/summary_index.md"
    if not index_path.exists():
        return
    for summary_file in sorted((project_dir / "06_reports/chapter_summaries").glob("ch*_summary.md")):
        token = summary_file.stem.replace("_summary", "")
        text = read_text(summary_file)
        carry = "待补充"
        for line in text.splitlines():
            if line.startswith("- ") and "Carry Forward" not in line:
                carry = line[2:42]
        row = f"| {token} | {summary_file.name} | {today_str()} | {carry} |"
        upsert_markdown_row(index_path, "summary_index", token, row)


def sync_review_index(project_dir: Path) -> None:
    index_path = project_dir / "06_reports/reviews/review_index.md"
    if not index_path.exists():
        return
    for review_file in sorted((project_dir / "06_reports/reviews").glob("ch*_review.md")):
        token = review_file.stem.replace("_review", "")
        text = read_text(review_file)
        verdict = "unknown"
        issues: list[str] = []
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("- ") and any(flag in stripped for flag in ["pass", "revise", "block"]):
                verdict = stripped[2:]
            if "P0" in stripped or "P1" in stripped or "P2" in stripped:
                issues.append(stripped)
        highest = highest_issue_label(issues)
        row = f"| {token} | {verdict} | {review_file.name} | {today_str()} | {highest} |"
        upsert_markdown_row(index_path, "review_index", token, row)


def chapter_diag(project_dir: Path, chapter: int) -> str:
    token = chapter_token(chapter)
    issues: list[str] = []
    outline = project_dir / f"03_outline/chapter_outlines/{token}.md"
    final = project_dir / f"04_manuscript/chapters/{token}.md"
    summary = project_dir / f"06_reports/chapter_summaries/{token}_summary.md"
    review = project_dir / f"06_reports/reviews/{token}_review.md"
    draft = project_dir / f"04_manuscript/drafts/{token}_draft.md"
    state = read_text(project_dir / "05_state/current_state.md")
    hooks = read_text(project_dir / "05_state/pending_hooks.md")
    chapter_index = read_text(project_dir / "03_outline/chapter_index.md")
    final_text = read_text(final)
    review_text = read_text(review)

    if not outline.exists():
        issues.append("- P0: 缺少章纲文件")
    if not draft.exists() and not final.exists():
        issues.append("- P1: 草稿和正式稿都不存在，章节推进链未启动")
    if final.exists() and not summary.exists():
        issues.append("- P0: 正式稿存在但缺少章节摘要")
    if final.exists() and not review.exists():
        issues.append("- P1: 正式稿存在但缺少审查报告")
    if f"| current_chapter | {chapter} |" not in state:
        issues.append("- P0: 当前状态卡未同步到该章节")
    if final.exists() and token not in hooks:
        issues.append("- P2: 伏笔池中未看到该章节的显式记录，请人工确认是否无钩子变化")
    if token in final_text and "TODO" in final_text:
        issues.append("- P1: 正式稿中仍有 TODO 占位词")
    if review.exists() and not any(flag in review_text for flag in ["pass", "revise", "block"]):
        issues.append("- P1: 审查报告缺少明确 verdict")
    if token not in chapter_index and final.exists():
        issues.append("- P1: 章节索引里还没有该章节记录")
    if not issues:
        issues.append("- 无阻断问题")
    return "\n".join(issues)


def project_diag(project_dir: Path) -> str:
    issues: list[str] = []
    index_text = read_text(project_dir / "03_outline/chapter_index.md")
    summaries = list_recent_files(project_dir / "06_reports/chapter_summaries", "ch*_summary.md", 999)
    reviews = list_recent_files(project_dir / "06_reports/reviews", "ch*_review.md", 999)
    chapters = list_recent_files(project_dir / "04_manuscript/chapters", "ch*.md", 999)
    drafts = list_recent_files(project_dir / "04_manuscript/drafts", "ch*_draft.md", 999)
    hooks = read_text(project_dir / "05_state/pending_hooks.md")
    relation_rows = count_table_rows(read_text(project_dir / "02_bible/relationship_matrix.md"))
    character_rows = count_table_rows(read_text(project_dir / "02_bible/character_cards.md"))
    research_index = read_text(project_dir / "06_reports/research/research_index.md")
    statuses = extract_status_column(index_text)

    if chapters and len(summaries) < len(chapters):
        issues.append(f"- P1: 摘要覆盖不足，正式章节 {len(chapters)} 个，摘要 {len(summaries)} 个")
    if chapters and len(reviews) < len(chapters):
        issues.append(f"- P1: 审查覆盖不足，正式章节 {len(chapters)} 个，审查 {len(reviews)} 个")
    if "|---|---|---|---|---|---|---|---|---|" in index_text and len(index_text.splitlines()) <= 4:
        issues.append("- P1: 章节索引仍为空，项目缺少进度痕迹")
    if drafts and not chapters:
        issues.append("- P1: 存在草稿但没有任何正式章节，项目可能长期停留在未定稿状态")
    if "active" in hooks and ("TBD" in hooks or "待补充" in hooks):
        issues.append("- P2: 伏笔池里存在未完成字段，建议补 payoff 或备注")
    if character_rows == 0:
        issues.append("- P1: 角色卡仍为空，长篇项目容易失控")
    if relation_rows == 0:
        issues.append("- P2: 关系矩阵为空，群像推进前建议先补")
    if not research_index.strip():
        issues.append("- P2: research 索引文件为空，现实题材项目不利于复用研究结果")
    if statuses and any(status != "synced" for status in statuses if status):
        issues.append("- P2: 章节索引存在未 synced 章节，请检查闭环是否完成")
    if not issues:
        issues.append("- 项目级诊断未发现阻断问题")
    return "\n".join(issues)


def trend_diag(project_dir: Path) -> list[str]:
    issues: list[str] = []
    review_rows = markdown_table_rows(read_text(project_dir / "06_reports/reviews/review_index.md"))
    summary_rows = markdown_table_rows(read_text(project_dir / "06_reports/chapter_summaries/summary_index.md"))
    if len(review_rows) > 3:
        latest = review_rows[-3:]
        if all(len(row) >= 5 and row[4] in {"P1", "P2"} for row in latest if row[0] != "chapter_no"):
            issues.append("- P2: 最近三次审查都带问题，项目可能进入慢性失稳")
    if len(summary_rows) > 5 and len(summary_rows) - 1 < len(review_rows) - 1:
        issues.append("- P2: 摘要更新频率低于审查频率，后续恢复续写会变脆")
    return issues


def stale_hook_diag(project_dir: Path) -> list[str]:
    issues: list[str] = []
    hook_rows = markdown_table_rows(read_text(project_dir / "05_state/pending_hooks.md"))
    for row in hook_rows[1:]:
        if len(row) < 6:
            continue
        hook_id, introduced_in, _type, status, expected_payoff, _note = row[:6]
        if status == "active" and expected_payoff in {"TBD", "待补充", ""}:
            issues.append(f"- P1: 活跃 hook 缺少回收窗口：{hook_id}")
        if status == "stale":
            issues.append(f"- P2: 存在 stale hook：{hook_id}（introduced_in={introduced_in}）")
    return issues


def continuity_risk_diag(project_dir: Path) -> list[str]:
    issues: list[str] = []
    state_text = read_text(project_dir / "05_state/current_state.md")
    if "| current_phase |" not in state_text or "| current_chapter |" not in state_text:
        issues.append("- P1: 当前状态卡字段不完整，连续性风险上升")
    if count_table_rows(read_text(project_dir / "02_bible/character_cards.md")) == 0:
        issues.append("- P1: 角色卡为空，人物连续性高风险")
    if count_table_rows(read_text(project_dir / "02_bible/relationship_matrix.md")) == 0:
        issues.append("- P2: 关系矩阵为空，群像连续性风险上升")
    return issues


def main() -> None:
    parser = parser_with_project("Run chapter-level or project-level diagnostics.")
    parser.add_argument("--scope", choices=["chapter", "project"], default="project")
    parser.add_argument("--chapter", type=int, default=0)
    parser.add_argument("--json-out", default="")
    args = parser.parse_args()

    project_dir = Path(args.project)
    sync_summary_index(project_dir)
    sync_review_index(project_dir)
    if args.scope == "chapter":
        if not args.chapter:
            raise SystemExit("--chapter is required when scope=chapter")
        token = chapter_token(args.chapter)
        body = chapter_diag(project_dir, args.chapter)
        target = project_dir / f"06_reports/diagnostics/{token}_diag.md"
    else:
        lines = []
        lines.extend(project_diag(project_dir).splitlines())
        lines.extend(trend_diag(project_dir))
        lines.extend(stale_hook_diag(project_dir))
        lines.extend(continuity_risk_diag(project_dir))
        if not [line for line in lines if line.strip().startswith("- ")]:
            lines.append("- 项目级诊断未发现阻断问题")
        body = "\n".join(lines)
        target = project_dir / "06_reports/diagnostics/project_diag.md"

    issue_lines = [line for line in body.splitlines() if line.strip().startswith("- ")]
    counts = severity_summary(issue_lines)

    payload = {
        "scope": args.scope,
        "target": args.chapter if args.scope == "chapter" else "project",
        "generated_at": today_str(),
        "severity": counts,
        "findings": issue_lines,
    }

    content = (
        "# Diagnostic Report\n\n"
        "## Basic Info\n"
        f"- Scope: {args.scope}\n"
        f"- Target: {args.chapter if args.scope == 'chapter' else 'project'}\n"
        f"- Generated At: {today_str()}\n\n"
        "## Severity Summary\n"
        f"- P0: {counts['P0']}\n"
        f"- P1: {counts['P1']}\n"
        f"- P2: {counts['P2']}\n\n"
        "## Findings\n"
        f"{body}\n\n"
        "## Blocking Issues\n"
        "- 见 Findings 中 P0 项\n\n"
        "## Recommended Fixes\n"
        "- 先修 P0，再修 P1，P2 可并入润色或维护阶段。\n"
        + "\n## Machine Summary\n"
        + f"- highest_issue: {('P0' if counts['P0'] else 'P1' if counts['P1'] else 'P2' if counts['P2'] else 'none')}\n"
        + f"- p0_count: {counts['P0']}\n"
        + f"- p1_count: {counts['P1']}\n"
        + f"- p2_count: {counts['P2']}\n"
    )
    write_text(target, content)
    if args.json_out:
        write_text(Path(args.json_out), json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(target)


if __name__ == "__main__":
    main()

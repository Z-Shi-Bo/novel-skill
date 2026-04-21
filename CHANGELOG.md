# Changelog

## v1.4

- 新增 `scripts/sync_indexes.py`
- 新增 `scripts/write_review.py`
- `build_context.py` 增加题材化上下文优先级与风险标签
- `diagnose_project.py` 支持 `--json-out`
- README 增补 v1.4 说明

## v1.3

- `build_context.py` 接入 `summary_index.md`、`review_index.md`、`research_index.md`
- `diagnose_project.py` 跑诊断前自动同步 summary / review 索引
- `summary_index.md` 与 `review_index.md` 纳入项目控制面

## v1.2

- `build_context.py` 接入 `research_index.md`
- `diagnose_project.py` 增加 Severity Summary
- `chapter_summary` / `review_report` 自动索引
- `research note` 自动写入统一索引

## v1.1

- 题材适配手册增强
- research note 索引机制
- diagnose 规则增强

## v1.0

- 初版完整包：SKILL / references / templates / scripts / evals

# Index Engine

## 目标

统一管理：

- summary index
- review index
- research index
- project_index.json

## 结构

```text
06_reports/
├── chapter_summaries/
│   ├── chNNN_summary.md
│   └── summary_index.md
├── reviews/
│   ├── chNNN_review.md
│   └── review_index.md
├── research/
│   ├── *.md
│   └── research_index.md
└── index/
    └── project_index.json
```

## 同步原则

1. 先维护 markdown index。
2. 再重建 `project_index.json`。
3. context / diagnose / CLI 优先消费总索引。

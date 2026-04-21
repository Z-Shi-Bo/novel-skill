# Index Files Schema

适用文件：

- `03_outline/chapter_index.md`
- `06_reports/chapter_summaries/summary_index.md`
- `06_reports/reviews/review_index.md`
- `06_reports/research/research_index.md`

---

## 1. Chapter Index

固定表头：

| chapter_no | volume | title | outline_status | draft_status | review_status | final_status | sync_status | last_updated |

### 规则
- `chapter_no` 应为章节号或 `chNNN` 对应值
- `outline_status` / `draft_status` / `review_status` / `final_status` / `sync_status` 必须用稳定短值
- `sync_status` 推荐值：`pending` / `synced`

---

## 2. Summary Index

固定表头：

| chapter_no | summary_file | updated | carry_forward |

### 规则
- `summary_file` 应指向 `chNNN_summary.md`
- `updated` 必须是 `YYYY-MM-DD`

---

## 3. Review Index

固定表头：

| chapter_no | verdict | review_file | updated | highest_issue |

### 规则
- `verdict` 必须为 `pass` / `revise` / `block` / `unknown`
- `highest_issue` 必须为 `P0` / `P1` / `P2` / `none`

---

## 4. Research Index

固定表头：

| note_id | topic | chapter | updated | summary |

### 规则
- `note_id` 不得重复
- `topic` 非空
- `updated` 必须是 `YYYY-MM-DD`

---

## 5. 总体规则

1. 所有 index 文件都必须保留 `START/END` marker。
2. 表头字段名不得随项目私改。
3. index 属于项目控制面，不能被自由文本段落取代。

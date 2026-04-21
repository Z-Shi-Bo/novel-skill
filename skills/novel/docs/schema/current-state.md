# Current State Schema

适用文件：`05_state/current_state.md`

## 必须存在的快照字段

当前状态卡必须包含 `current_snapshot` 表格，并至少包含以下字段：

| Field | 说明 |
|---|---|
| `title` | 作品名 |
| `current_phase` | 当前阶段 |
| `current_volume` | 当前卷 |
| `current_chapter` | 当前章 |
| `current_location` | 当前地点 |
| `active_goal` | 当前目标 |
| `active_status` | 当前状态 |
| `known_truth` | 当前已知真相 |
| `next_pressure` | 当前下一压力点 |
| `last_synced` | 最后同步日期 |

## Active Constraints 区块

必须存在：

- `<!-- START:active_constraints -->`
- `<!-- END:active_constraints -->`

其中至少保留一行内容。空时也应写：`- 暂无`

## 校验规则

1. 表格必须存在且字段名稳定。
2. `current_volume` / `current_chapter` 应可解析为整数。
3. `last_synced` 应为 `YYYY-MM-DD`。
4. 如果项目 `strong_sync=true`，则不得缺失 `active_constraints` 区块。

## 常见错误

- 快照表被自由文本替代
- 缺少 `last_synced`
- 当前章已经推进，但状态卡仍停留在旧章节

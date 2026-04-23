# Accepted Sync Payload Schema

适用 skill：`novel-ainovel-bridge`

## 目标

`sync` 只接收 AI-Novel 的 accepted / final 结果，拒绝 draft / polish 中间态。

## 最小字段

- `chapter`
- `accepted`（必须为 `true`）
- `summary`
- `state_updates`
- `hook_updates`

## 推荐字段

- `payload_id`
- `chapter_revision`
- `timeline_events`
- `relationship_changes`
- `source_paths`
- `accepted_at`

## 回流目标

最常见的回流位置：

- `06_reports/chapter_summaries/chNNN_summary.md`
- `05_state/current_state.md`
- `05_state/pending_hooks.md`
- `05_state/timeline.md`（如果存在）
- `02_bible/relationship_matrix.md`（或后续关系账本）

## 原则

1. 没有 `accepted: true` 就拒绝回流。
2. draft / polish payload 不得进入 canon。
3. state / hook / timeline / relationship 的变更应可追溯到 `source_paths`。
4. 同一 `payload_id` 重复执行时，应按同一同步单元处理，不重复追加。
5. 如果没有 `payload_id`，至少用 `chapter + accepted_at + source_paths` 识别同一批 accepted 结果。
6. 同一章节出现更高 `chapter_revision` 或更晚 accepted 结果时，视为 supersede 旧结果。

## 多章节约定

1. 默认一章一份 payload 文件。
2. 一次处理多章时，按 `chapter` 升序应用。
3. 任一 payload 不是 accepted / final 时，应先报冲突，不要静默混入 canon。

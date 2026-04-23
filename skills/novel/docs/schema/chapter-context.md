# Chapter Context Schema

适用文件：`07_exports/context_packs/chNNN_context.yaml`

## 必填字段

| 字段 | 说明 | 规则 |
|---|---|---|
| `chapter` | 章节号 | 同一项目内格式保持一致 |
| `title` | 章节标题 | 非空 |
| `must_keep` | 必须保留的信息 | 至少 1 条 |
| `must_avoid` | 必须避免的走法 | 至少 1 条 |
| `emotion_target` | 情绪目标 | 非空短句 |
| `hook_goal` | 章末钩子目标 | 非空短句 |
| `continuity_notes` | 连贯性提醒 | 至少 1 条 |

## 推荐字段

- `voice_notes`
- `required_beats`
- `forbidden_moves`
- `active_hooks`
- `state_focus`

## 校验规则

1. `must_keep` / `must_avoid` / `continuity_notes` 应为列表。
2. `voice_notes` 应为 `角色名 -> list[string]` 的映射。
3. `active_hooks` 只放当前章仍在生效的钩子，不要把已回收钩子继续挂着。
4. `state_focus` 只列本章必须承接的状态变化，不要塞整本状态卡。

## 常见错误

- 把正文摘要当成 `must_keep`
- `hook_goal` 写成空泛口号
- `state_focus` 复制整份 `current_state.md`

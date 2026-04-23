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
3. `active_hooks` 只放当前章仍有效的钩子。
4. `state_focus` 只列本章要承接的状态，不复制整份状态卡。

## 常见错误

- 把 prose 样稿写进 context
- `hook_goal` 只有口号，没有动作目标
- `state_focus` 塞整页剧情复述

# Chapter Context Mapping

适用链路：

- source：`07_exports/context_packs/chNNN_context.yaml`
- target：`07_exports/ainovel_feed/chapter_context/chNNN.yaml`

## 必填字段

- `chapter`
- `title`
- `must_keep`
- `must_avoid`
- `emotion_target`
- `hook_goal`
- `continuity_notes`

## 推荐字段

- `voice_notes`
- `required_beats`
- `forbidden_moves`
- `active_hooks`
- `state_focus`

## 映射规则

1. source 与 target 字段名保持一致，不重新命名。
2. `active_hooks` 只放本章仍生效的钩子。
3. `state_focus` 只放 AI-Novel 当前章必须承接的状态变化。

## 常见错误

- 导出时把整章摘要塞进 `must_keep`
- `state_focus` 没筛选，导致 handoff 过重

# Character Card Mapping

适用链路：

- source：`02_bible/character_cards.md`
- target：`07_exports/ainovel_feed/characters.json`

## source 表头

| character_id | name | role | public_goal | hidden_drive | weakness | current_status | note |

## target 最小字段

- `character_id`
- `name`
- `aliases`
- `role`
- `public_goal`
- `hidden_drive`
- `weakness`
- `current_status`
- `description`
- `arc`
- `traits`
- `tier`
- `note`

## 映射规则

1. `character_id` / `name` / `role` 缺一不可。
2. source 表格里的目标、驱动力、弱点、状态应直接映射到 JSON，不要丢字段。
3. `traits` / `description` / `arc` 可由 source 备注与 story bible 片段补全，但不能覆盖表格里的硬约束。

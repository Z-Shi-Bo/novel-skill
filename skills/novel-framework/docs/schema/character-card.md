# Character Card Schema

适用文件：`02_bible/character_cards.md`

## 表头要求

必须存在 `character_cards` 区块，表头固定为：

| character_id | name | role | public_goal | hidden_drive | weakness | current_status | note |

## 字段说明

| 字段 | 说明 | 规则 |
|---|---|---|
| `character_id` | 角色唯一标识 | 非空且不可重复 |
| `name` | 常用名字 | 非空 |
| `role` | 叙事职责 | 非空，短标签优先 |
| `public_goal` | 对外目标 | 非空；未知时写 `TBD` |
| `hidden_drive` | 深层驱动力 | 非空；未知时写 `TBD` |
| `weakness` | 关键弱点 | 非空；未知时写 `TBD` |
| `current_status` | 当前状态 | 非空，保持短值 |
| `note` | 补充备注 | 可空 |

## 校验规则

1. 不改列名，不调换列顺序。
2. `character_id` 在全表内唯一。
3. 角色进入卷纲或章纲前，应先补齐核心字段。

## 常见错误

- 角色名变了但 `character_id` 没统一
- `current_status` 写成长段剧情
- 同一角色拆成多行却没有说明主从关系

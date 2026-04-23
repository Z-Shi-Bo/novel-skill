# Pending Hooks Schema

适用文件：`05_state/pending_hooks.md`

## 表头要求

必须存在 `hook_table` 区块，表头固定为：

| hook_id | introduced_in | type | status | expected_payoff | note |

## 字段说明

| 字段 | 说明 | 规则 |
|---|---|---|
| `hook_id` | 钩子唯一标识 | 非空 |
| `introduced_in` | 首次出现章节 | 建议 `chNNN` |
| `type` | 钩子类型 | 非空，建议短标签 |
| `status` | 当前状态 | `active` / `resolved` / `stale` / `dropped` |
| `expected_payoff` | 预期回收窗口 | 非空；未知时明确写 `TBD` |
| `note` | 备注 | 可空，但建议填写 |

## 校验规则

1. 表头必须稳定，不能私改列名。
2. `status` 必须在枚举中。
3. `hook_id` 不得重复。
4. `active` 状态的钩子不应长期保留空 `expected_payoff`。

## 常见错误

- `status` 写成自然语言句子
- 同一个 `hook_id` 多次重复
- 钩子已回收但状态仍是 `active`

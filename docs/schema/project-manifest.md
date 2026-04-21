# Project Manifest Schema

适用文件：`project_manifest.yaml`

## 必填字段

| 字段 | 类型 | 说明 | 允许值 / 规则 |
|---|---|---|---|
| `title` | string | 作品名 | 非空 |
| `slug` | string | 项目标识 | 建议 kebab-case；非空 |
| `genre` | string | 题材 | 非空 |
| `style` | string | 风格基调 | 非空 |
| `audience` | string | 目标读者 | 非空 |
| `language` | string | 输出语言 | 非空，建议 `zh-CN` |
| `research_mode` | string | 考据模式 | `off` / `on-demand` / `strict` |
| `strong_sync` | string | 强闭环开关 | `true` / `false` |
| `current_phase` | string | 当前阶段 | `initialized` / `brief` / `bible` / `characters` / `outline` / `drafted` / `reviewed` / `finalized` / `synced` |
| `current_volume` | string | 当前卷 | 必须可转为整数，且 >= 0 |
| `current_chapter` | string | 当前章 | 必须可转为整数，且 >= 0 |
| `last_updated` | string | 更新时间 | `YYYY-MM-DD` |

## 校验规则

1. 不允许缺少任一必填字段。
2. `research_mode` 必须在约定枚举中。
3. `strong_sync` 必须是字符串 `true` 或 `false`。
4. `current_volume` / `current_chapter` 必须是非负整数。
5. `last_updated` 必须符合日期格式。

## 常见错误

- `research_mode: "auto"` → 非法值
- `current_chapter: "chapter 12"` → 非法值
- `last_updated: "2026/04/21"` → 日期格式不合规
